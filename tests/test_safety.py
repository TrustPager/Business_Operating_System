"""Offline safety tests — the guarantees that keep the API key from leaking.

No network, no real key. Run:
    python -m unittest tests.test_safety
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import trustpager_api as t  # noqa: E402

# Built from fragments on purpose: a real key never appears as a contiguous
# literal in this file, so tools/check-no-secrets.py won't (correctly) flag it.
REAL_LOOKING_KEY = "tp_live" + "_AbCdEf0123456789GhIjKlMnOp"  # not a real key


class TestOfflineGuard(unittest.TestCase):
    def setUp(self):
        self._prev = os.environ.get("BOS_OFFLINE")
        os.environ["BOS_OFFLINE"] = "1"

    def tearDown(self):
        if self._prev is None:
            os.environ.pop("BOS_OFFLINE", None)
        else:
            os.environ["BOS_OFFLINE"] = self._prev

    def test_get_blocked_offline(self):
        with self.assertRaises(t.BOSError):
            t.api_get("opportunities")

    def test_post_blocked_offline(self):
        with self.assertRaises(t.BOSError):
            t.api_post("opportunities", body={"name": "x"})

    def test_offline_does_not_read_the_key(self):
        # The guard must fire BEFORE get_api_key(), so a missing key still
        # yields the offline error (never an auth path that could read a key).
        prev = os.environ.pop("TRUSTPAGER_API_KEY", None)
        try:
            with self.assertRaises(t.BOSError) as ctx:
                t.api_get("opportunities")
            self.assertIn("offline", str(ctx.exception).lower())
        finally:
            if prev is not None:
                os.environ["TRUSTPAGER_API_KEY"] = prev


class TestRedaction(unittest.TestCase):
    def test_redact_strips_real_key(self):
        out = t._redact(f"oops the key is {REAL_LOOKING_KEY} in here")
        self.assertNotIn(REAL_LOOKING_KEY, out)
        self.assertIn("REDACTED", out)

    def test_redact_leaves_bare_prefix_alone(self):
        # Docs say "your key starts with tp_live_" — that must NOT be redacted.
        text = "your key starts with tp_live_"
        self.assertEqual(t._redact(text), text)

    def test_journal_writes_redacted(self):
        with tempfile.TemporaryDirectory() as d:
            prev_dir = t.JOURNAL_DIR
            prev_flag = os.environ.pop("BOS_JOURNAL", None)
            t.JOURNAL_DIR = Path(d)
            try:
                t._record_write("POST", "email/send",
                                {"api_key": REAL_LOOKING_KEY, "to": "x@example.com"},
                                status="ok", result_id="r1")
                written = "".join(p.read_text(encoding="utf-8") for p in Path(d).glob("*.jsonl"))
                self.assertTrue(written, "journal line should have been written")
                self.assertNotIn(REAL_LOOKING_KEY, written)
                self.assertIn("REDACTED", written)
            finally:
                t.JOURNAL_DIR = prev_dir
                if prev_flag is not None:
                    os.environ["BOS_JOURNAL"] = prev_flag


if __name__ == "__main__":
    unittest.main()

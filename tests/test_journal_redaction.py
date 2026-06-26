"""Tests for the kernel redaction registry (kernel.runtime.redaction).

Redaction is a vendor-neutral mechanism: the kernel ships with an EMPTY
pattern registry. Callers (drivers) register the secret shapes they care
about via register_secret_pattern(); redact() then masks every registered
pattern. A token that nobody registered is left untouched.

Offline-safe: no network, no key. Run:
    python -m unittest tests.test_journal_redaction
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kernel.runtime import redaction  # noqa: E402


class TestRedactionRegistry(unittest.TestCase):
    def setUp(self):
        # Each test starts from a clean registry so order can't leak state.
        self._saved = redaction._snapshot_patterns()
        redaction._reset_patterns()

    def tearDown(self):
        redaction._restore_patterns(self._saved)

    def test_registered_pattern_is_masked(self):
        redaction.register_secret_pattern(r"SEKRET_[0-9]{4}")
        out = redaction.redact("here is SEKRET_1234 in the text")
        self.assertNotIn("SEKRET_1234", out)
        self.assertIn("REDACTED", out)

    def test_unregistered_token_is_left_intact(self):
        # Empty registry: nothing should be masked.
        text = "this PLAIN_5678 token was never registered"
        self.assertEqual(redaction.redact(text), text)

    def test_multiple_registered_patterns_all_apply(self):
        redaction.register_secret_pattern(r"AAA_[0-9]+")
        redaction.register_secret_pattern(r"BBB_[0-9]+")
        out = redaction.redact("first AAA_11 then BBB_22 done")
        self.assertNotIn("AAA_11", out)
        self.assertNotIn("BBB_22", out)
        self.assertEqual(out.count("REDACTED"), 2)

    def test_redact_handles_none_and_empty(self):
        # Best-effort: falsy input passes straight through, never raises.
        self.assertIsNone(redaction.redact(None))
        self.assertEqual(redaction.redact(""), "")

    def test_duplicate_registration_is_idempotent(self):
        redaction.register_secret_pattern(r"DUP_[0-9]+")
        redaction.register_secret_pattern(r"DUP_[0-9]+")
        out = redaction.redact("token DUP_99 here")
        # Masked once, not double-substituted into garbage.
        self.assertNotIn("DUP_99", out)
        self.assertEqual(out.count("REDACTED"), 1)


if __name__ == "__main__":
    unittest.main()

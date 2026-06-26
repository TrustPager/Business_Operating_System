"""Transport-seam tests for the vendor-neutral kernel HTTP layer.

These exercise kernel.runtime.transport.request directly, with a fabricated
DriverConfig (no real vendor) so the kernel stays provider-agnostic:

  (a) BOS_OFFLINE=1  -> request raises BEFORE the key_resolver is ever called
      (the offline guard must run first so a real key is never read in CI).
  (b) offline unset  -> a monkeypatched _http returning a fake 200 body flows
      back through as a parsed dict.
  (c) a 202 fake     -> returns ApprovalPending carrying cfg.approval_url.
  (d) a mocked HTTPError code -> the cfg.error_map message is used.

Offline-safe: no network, no key. Run:
    python -m unittest tests.test_transport_offline
"""

import io
import os
import sys
import unittest
import urllib.error
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kernel.runtime import redaction, transport  # noqa: E402
from kernel.runtime.errors import BOSError  # noqa: E402


def _make_cfg(key_flag):
    """Build a fabricated, vendor-neutral DriverConfig.

    key_flag is a mutable list; key_resolver flips key_flag[0] = True so a test
    can assert whether the key was ever read.
    """
    def resolver():
        key_flag[0] = True
        return "fake_key_value"

    return transport.DriverConfig(
        base_url="https://example.invalid/api",
        key_resolver=resolver,
        secret_pattern=r"fakesecret_[A-Za-z0-9]{6,}",
        error_map={
            401: "Bad fake key (401).",
            402: "Fake billing problem (402).",
            422: "Validation failed (422). {detail}{available}",
        },
        approval_url="https://example.invalid/approvals",
    )


class _FakeResp:
    """Minimal stand-in for the urlopen context-manager response."""

    def __init__(self, status, body: bytes):
        self.status = status
        self._body = body

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class TestTransportOffline(unittest.TestCase):
    def setUp(self):
        # Isolate the redaction registry: DriverConfig.__post_init__ registers
        # its secret_pattern, and we don't want that to leak across tests.
        self._saved_patterns = redaction._snapshot_patterns()
        self._prev_offline = os.environ.get("BOS_OFFLINE")
        self._saved_http = transport._http

    def tearDown(self):
        redaction._restore_patterns(self._saved_patterns)
        transport._http = self._saved_http
        if self._prev_offline is None:
            os.environ.pop("BOS_OFFLINE", None)
        else:
            os.environ["BOS_OFFLINE"] = self._prev_offline

    # (a) offline guard fires before the key is read ------------------------
    def test_offline_raises_before_key_resolver(self):
        os.environ["BOS_OFFLINE"] = "1"
        key_read = [False]
        cfg = _make_cfg(key_read)
        with self.assertRaises(BOSError) as ctx:
            transport.request(cfg, "GET", "ping")
        self.assertIn("offline", str(ctx.exception).lower())
        self.assertFalse(key_read[0], "key_resolver must NOT run when offline")

    # (b) happy-path 200 flows through --------------------------------------
    def test_200_flows_through(self):
        os.environ.pop("BOS_OFFLINE", None)
        key_read = [False]
        cfg = _make_cfg(key_read)

        def fake_http(req, timeout):
            return _FakeResp(200, b'{"data": [{"id": "x1"}]}')

        transport._http = fake_http
        out = transport.request(cfg, "GET", "ping")
        self.assertEqual(out, {"data": [{"id": "x1"}]})
        self.assertTrue(key_read[0], "key_resolver should run on a live call")

    # (c) 202 -> ApprovalPending carrying cfg.approval_url ------------------
    def test_202_returns_approval_pending(self):
        os.environ.pop("BOS_OFFLINE", None)
        key_read = [False]
        cfg = _make_cfg(key_read)

        def fake_http(req, timeout):
            return _FakeResp(202, b'{"approval_id": "appr-9"}')

        transport._http = fake_http
        out = transport.request(cfg, "POST", "things", body={"k": "v"})
        self.assertIsInstance(out, transport.ApprovalPending)
        self.assertEqual(out.approval_id, "appr-9")
        self.assertEqual(out.approval_url, "https://example.invalid/approvals")

    # (d) error_map message is used on a mocked HTTPError code --------------
    def test_error_map_message_used(self):
        os.environ.pop("BOS_OFFLINE", None)
        key_read = [False]
        cfg = _make_cfg(key_read)

        def fake_http(req, timeout):
            raise urllib.error.HTTPError(
                url="https://example.invalid/api/ping",
                code=401,
                msg="Unauthorized",
                hdrs=None,
                fp=io.BytesIO(b'{"error": {"message": "nope"}}'),
            )

        transport._http = fake_http
        with self.assertRaises(BOSError) as ctx:
            transport.request(cfg, "GET", "ping")
        self.assertIn("Bad fake key (401).", str(ctx.exception))

    def test_422_available_hint_surfaces_via_template(self):
        # The {available} placeholder fills from error.details.available when the
        # server sends it, and stays empty otherwise (no cross-code leak).
        os.environ.pop("BOS_OFFLINE", None)
        key_read = [False]
        cfg = _make_cfg(key_read)

        def fake_http(req, timeout):
            raise urllib.error.HTTPError(
                url="https://example.invalid/api/things",
                code=422,
                msg="Unprocessable",
                hdrs=None,
                fp=io.BytesIO(
                    b'{"error": {"message": "bad stage", '
                    b'"details": {"available": ["a", "b"]}}}'
                ),
            )

        transport._http = fake_http
        with self.assertRaises(BOSError) as ctx:
            transport.request(cfg, "POST", "things", body={"stage": "z"})
        msg = str(ctx.exception)
        self.assertIn("bad stage", msg)
        self.assertIn("Valid options", msg)
        self.assertIn("'a', 'b'", msg)

    def test_unmapped_error_falls_back_to_generic(self):
        # 404 isn't in this cfg's error_map -> kernel generic message, no vendor.
        os.environ.pop("BOS_OFFLINE", None)
        key_read = [False]
        cfg = _make_cfg(key_read)

        def fake_http(req, timeout):
            raise urllib.error.HTTPError(
                url="https://example.invalid/api/ping",
                code=404,
                msg="Not Found",
                hdrs=None,
                fp=io.BytesIO(b'{}'),
            )

        transport._http = fake_http
        with self.assertRaises(BOSError) as ctx:
            transport.request(cfg, "GET", "ping")
        # Generic kernel message mentions the HTTP code and path, not a vendor.
        msg = str(ctx.exception)
        self.assertIn("404", msg)
        self.assertNotIn("trustpager", msg.lower())


if __name__ == "__main__":
    unittest.main()

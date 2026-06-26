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

    # --- 5xx sentinel + exact-code precedence (vendor-neutral) -------------
    # These lock in _format_http_error's lookup order: an exact int code wins,
    # then (for 500-599 only) the "5xx" string sentinel, then the GENERIC
    # kernel fallback. The kernel file holds NO vendor literal, so we drive it
    # entirely with a synthetic cfg and never import the TrustPager driver.
    #
    # Note: a 503 must clear retries to reach the formatter. The retry path
    # (transport.request, 5xx branch) recurses up to DEFAULT_RETRIES_ON_5XX
    # times with time.sleep(2**attempt). To keep these tests fast and offline
    # we pass _attempt past that ceiling so the first raised HTTPError formats
    # immediately — we're testing the formatter, not the backoff.

    def _make_cfg_with_map(self, error_map):
        """A fabricated, vendor-neutral cfg whose error_map we control."""
        return transport.DriverConfig(
            base_url="https://example.invalid/api",
            key_resolver=lambda: "fake_key_value",
            secret_pattern=r"fakesecret_[A-Za-z0-9]{6,}",
            error_map=error_map,
            approval_url="https://example.invalid/approvals",
        )

    def _raise_http(self, code, body: bytes):
        """Return a fake _http that raises HTTPError(code) with a JSON body."""
        def fake_http(req, timeout):
            raise urllib.error.HTTPError(
                url="https://example.invalid/api/ping",
                code=code,
                msg="Synthetic",
                hdrs=None,
                fp=io.BytesIO(body),
            )
        return fake_http

    def test_5xx_sentinel_fires_and_echoes_detail(self):
        # A "5xx" sentinel template (no exact 503 key) handles a 503, echoing
        # the server-body message via {detail}.
        os.environ.pop("BOS_OFFLINE", None)
        cfg = self._make_cfg_with_map({"5xx": "Upstream said: {detail}"})
        transport._http = self._raise_http(
            503, b'{"error": {"message": "gateway exploded"}}'
        )
        with self.assertRaises(BOSError) as ctx:
            transport.request(cfg, "GET", "ping",
                              _attempt=transport.DEFAULT_RETRIES_ON_5XX)
        msg = str(ctx.exception)
        self.assertIn("Upstream said: gateway exploded", msg)

    def test_exact_code_shadows_5xx_sentinel(self):
        # An exact 503 entry must win over the "5xx" sentinel.
        os.environ.pop("BOS_OFFLINE", None)
        cfg = self._make_cfg_with_map({503: "exact 503 msg", "5xx": "sentinel msg"})
        transport._http = self._raise_http(503, b'{}')
        with self.assertRaises(BOSError) as ctx:
            transport.request(cfg, "GET", "ping",
                              _attempt=transport.DEFAULT_RETRIES_ON_5XX)
        msg = str(ctx.exception)
        self.assertIn("exact 503 msg", msg)
        self.assertNotIn("sentinel msg", msg)

    def test_5xx_sentinel_band_boundary(self):
        # With a "5xx" sentinel present: a 503 uses it, but a 600 is OUT of the
        # 500-599 band and falls to the GENERIC kernel message instead.
        os.environ.pop("BOS_OFFLINE", None)
        cfg = self._make_cfg_with_map({"5xx": "sentinel msg"})

        # 503 -> sentinel.
        transport._http = self._raise_http(503, b'{}')
        with self.assertRaises(BOSError) as ctx:
            transport.request(cfg, "GET", "ping",
                              _attempt=transport.DEFAULT_RETRIES_ON_5XX)
        self.assertIn("sentinel msg", str(ctx.exception))

        # 600 -> out of band -> generic kernel fallback, no sentinel, no vendor.
        # (600 is not 5xx, so no retry path applies and _attempt is irrelevant.)
        transport._http = self._raise_http(600, b'{}')
        with self.assertRaises(BOSError) as ctx:
            transport.request(cfg, "GET", "ping")
        msg = str(ctx.exception)
        self.assertNotIn("sentinel msg", msg)
        self.assertIn("600", msg)
        self.assertIn("ping", msg)
        self.assertNotIn("trustpager", msg.lower())

    def test_no_sentinel_5xx_falls_back_to_generic(self):
        # Empty error_map -> a 503 has neither an exact key nor a "5xx" sentinel,
        # so the GENERIC vendor-neutral server-error message is used.
        os.environ.pop("BOS_OFFLINE", None)
        cfg = self._make_cfg_with_map({})
        transport._http = self._raise_http(
            503, b'{"error": {"message": "boom"}}'
        )
        with self.assertRaises(BOSError) as ctx:
            transport.request(cfg, "GET", "ping",
                              _attempt=transport.DEFAULT_RETRIES_ON_5XX)
        msg = str(ctx.exception)
        self.assertIn("server error (503)", msg)
        self.assertIn("ping", msg)
        self.assertNotIn("trustpager", msg.lower())

    def test_exact_429_template_renders(self):
        # An exact 429 template renders (echoing {detail}); 429 must clear its
        # own retry ceiling (DEFAULT_RETRIES_ON_429) to reach the formatter.
        os.environ.pop("BOS_OFFLINE", None)
        cfg = self._make_cfg_with_map({429: "Slow down: {detail}"})
        transport._http = self._raise_http(
            429, b'{"error": {"message": "too many"}}'
        )
        with self.assertRaises(BOSError) as ctx:
            transport.request(cfg, "GET", "ping",
                              _attempt=transport.DEFAULT_RETRIES_ON_429)
        self.assertIn("Slow down: too many", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

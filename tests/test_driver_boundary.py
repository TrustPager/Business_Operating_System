"""THE P0 GATE — proof the kernel is genuinely vendor-neutral.

Tasks 0-4 split the monolith into a vendor-neutral kernel (kernel/runtime/*)
and a TrustPager driver (drivers/trustpager/*). The whole point of P0 is that a
SECOND driver can be built on the kernel WITHOUT touching TrustPager. This test
is the proof: it stands up a minimal no-op driver (drivers/_noop) that wires the
kernel exactly like a real driver would — its own DriverConfig + a journaled
write through the transport — and asserts that exercising it pulls in NO
TrustPager code at all.

Two assertions make this a genuine gate (not trivially true):

  (1) record_write fired exactly once. The write went THROUGH the kernel journal,
      proving the no-op driver uses the same journaled-write seam a real driver
      does — not a side path that fakes the audit trail.
  (2) No module containing "trustpager" is present in sys.modules after importing
      and exercising the no-op driver. We purge any already-loaded trustpager
      modules FIRST (a prior test in the same run could have imported them), so
      this check actually proves the no-op driver didn't re-import them — it isn't
      satisfied just because the run happens to have started clean.

Network indirection: this test exercises the REAL request()->_http path with
_http mocked to a fake 200 — so it must NOT set BOS_OFFLINE (the offline guard
would short-circuit request() before _http and the journaled write would never
reach the transport). No socket is opened because _http is patched. The test is
self-contained and deterministic: it saves/restores _http, record_write, and
BOS_OFFLINE, and journals to a temp dir so it never writes the real audit trail.

Run:
    python -m unittest tests.test_driver_boundary
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kernel.runtime import journal as kjournal  # noqa: E402
from kernel.runtime import transport as ktransport  # noqa: E402


class _FakeResp:
    """Minimal stand-in for the urlopen context-manager response.

    Mirrors what transport.request expects: a context manager whose .status is
    the HTTP code and whose .read() yields the raw JSON body bytes.
    """

    def __init__(self, status, body: bytes):
        self.status = status
        self._body = body

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class TestDriverBoundary(unittest.TestCase):
    def setUp(self):
        self._prev_offline = os.environ.get("BOS_OFFLINE")
        self._saved_http = ktransport._http
        self._saved_record_write = kjournal.record_write
        self._tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        ktransport._http = self._saved_http
        kjournal.record_write = self._saved_record_write
        if self._prev_offline is None:
            os.environ.pop("BOS_OFFLINE", None)
        else:
            os.environ["BOS_OFFLINE"] = self._prev_offline
        self._tmp.cleanup()

    def test_noop_driver_exercises_kernel_without_trustpager(self):
        # Exercise the REAL request()->_http path: _http is mocked, but the
        # offline guard must stay OFF or it short-circuits request() before _http
        # and the journaled write never reaches the transport.
        os.environ.pop("BOS_OFFLINE", None)

        # (2) precondition: purge any already-loaded trustpager modules so a prior
        # test in the same run can't mask the result. The post-call assertion then
        # genuinely proves the no-op driver did NOT re-import TrustPager.
        for m in list(sys.modules):
            if "trustpager" in m:
                del sys.modules[m]

        # Import the no-op driver fresh, AFTER the purge.
        import drivers._noop as noop

        # Mock the network seam: a fake 200 carrying a data.id body, matching what
        # request() parses on the happy path.
        def fake_http(req, timeout):
            return _FakeResp(200, b'{"data": {"id": "noop-ok"}}')

        ktransport._http = fake_http

        # Spy on the kernel journal: the no-op driver journals THROUGH the kernel,
        # so record_write must fire here. Route to a temp dir so the real audit
        # trail is never touched (record_write swallows errors, so this also keeps
        # the spy from depending on a writable journal home).
        calls = []
        real_record_write = self._saved_record_write

        def spy_record_write(*args, **kwargs):
            calls.append((args, kwargs))
            kwargs.setdefault("journal_dir", Path(self._tmp.name))
            return real_record_write(*args, **kwargs)

        kjournal.record_write = spy_record_write

        result = noop.write_ping({"hello": "world"})

        # The journaled write came back through the kernel transport (fake 200).
        self.assertEqual(result, {"data": {"id": "noop-ok"}})

        # (1) GATE ASSERTION ONE: the write was journaled THROUGH the kernel,
        # exactly once.
        self.assertEqual(
            len(calls), 1,
            f"record_write should fire exactly once for one journaled write; "
            f"saw {len(calls)} call(s)",
        )

        # (2) GATE ASSERTION TWO: building + exercising the no-op driver pulled in
        # NO TrustPager code. With the pre-import purge above, this is a real
        # proof, not a trivially-true check.
        self.assertFalse(
            any("trustpager" in m for m in sys.modules),
            "no-op driver pulled in TrustPager — kernel is not vendor-neutral",
        )


if __name__ == "__main__":
    unittest.main()

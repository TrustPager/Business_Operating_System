"""Driver tests for drivers/trustpager — auth, catalog, secret registration.

These pin the behaviour Task 3 extracts out of tools/trustpager_api.py into the
TrustPager driver. They are vendor-specific (they live with the driver, not the
kernel) and fully offline: no network, no real key.

  (a) resolve_path("scheduling", path_contains="bookings") -> "scheduling/bookings"
      against an INLINE fixture catalog (the catalog cache is monkeypatched so
      no fetch fires).
  (b) get_api_key() returns $TRUSTPAGER_API_KEY when it is set.
  (c) importing/constructing the driver registers the tp_ secret pattern, so a
      tp_live_... key redacts.

Run:
    python -m unittest tests.test_trustpager_driver
"""

import os
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from drivers.trustpager import catalog as tp_catalog  # noqa: E402
from drivers.trustpager import auth as tp_auth  # noqa: E402
from kernel.runtime.redaction import redact  # noqa: E402

# Built from fragments on purpose so a real-looking key never appears as a
# contiguous literal (keeps tools/check-no-secrets.py honest).
REAL_LOOKING_KEY = "tp_live" + "_AbCdEf0123456789GhIjKlMnOp"  # not a real key

# A minimal catalog with the scheduling resource whose endpoint path matches a
# PATH_OVERRIDES key, so resolve_path exercises the override + ships the slash.
FIXTURE_CATALOG = {
    "resources": [
        {
            "id": "scheduling",
            "label": "Scheduling",
            "endpoints": [
                {"method": "GET", "path": "/scheduling-bookings"},
                {"method": "GET", "path": "/scheduling-availability"},
            ],
        }
    ]
}


class TestResolvePath(unittest.TestCase):
    def setUp(self):
        # Force the catalog offline: prime the in-process memo with the fixture
        # so get_catalog() never touches disk or network.
        self._saved_cache = tp_catalog._catalog_cache
        tp_catalog._catalog_cache = FIXTURE_CATALOG

    def tearDown(self):
        tp_catalog._catalog_cache = self._saved_cache

    def test_resolve_path_scheduling_bookings(self):
        # The fixture endpoint is the dashed docs-bug shape; PATH_OVERRIDES must
        # turn it into the slashed path the live API actually serves.
        self.assertEqual(
            tp_catalog.resolve_path("scheduling", path_contains="bookings"),
            "scheduling/bookings",
        )


class TestGetApiKey(unittest.TestCase):
    def test_env_var_wins(self):
        prev = os.environ.get("TRUSTPAGER_API_KEY")
        os.environ["TRUSTPAGER_API_KEY"] = REAL_LOOKING_KEY
        try:
            self.assertEqual(tp_auth.get_api_key(), REAL_LOOKING_KEY)
        finally:
            if prev is None:
                os.environ.pop("TRUSTPAGER_API_KEY", None)
            else:
                os.environ["TRUSTPAGER_API_KEY"] = prev


class TestSecretRegistration(unittest.TestCase):
    def test_importing_driver_registers_tp_pattern(self):
        # Importing drivers.trustpager constructs TP_CFG, whose
        # DriverConfig.__post_init__ registers the tp_ pattern. A real-looking
        # key must therefore redact.
        import drivers.trustpager  # noqa: F401  (import for the side effect)

        out = redact(f"leaked {REAL_LOOKING_KEY} here")
        self.assertNotIn(REAL_LOOKING_KEY, out)
        self.assertIn("REDACTED", out)

    def test_bare_prefix_not_redacted(self):
        # "your key starts with tp_live_" must NOT be redacted (the pattern needs
        # a real token after the prefix).
        text = "your key starts with tp_live_"
        self.assertEqual(redact(text), text)


if __name__ == "__main__":
    unittest.main()

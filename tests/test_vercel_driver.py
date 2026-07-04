"""Offline-safe: no network, no key. Run: BOS_OFFLINE=1 python -m unittest tests.test_vercel_driver

The vercel driver is DOCUMENTATION ONLY — a top-level ``DRIVER`` dict, no
``DriverConfig`` and no transport (mirrors drivers/meta-ads/__init__.py). These
tests pin the two facts the connector gate and the launch-my-site frontmatter
lean on — a ``keyed_cli`` kind and a ``key`` credential — and prove the boundary
that importing it pulls in NO other vendor driver (the same seam the P0
driver-boundary test protects for trustpager).
"""

import importlib
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


class TestVercelDriver(unittest.TestCase):
    def test_exposes_keyed_cli_driver_dict(self):
        mod = importlib.import_module("drivers.vercel")
        self.assertTrue(hasattr(mod, "DRIVER"))
        self.assertEqual(mod.DRIVER["kind"], "keyed_cli")
        self.assertEqual(mod.DRIVER["credential"], "key")

    def test_pulls_in_no_other_vendor(self):
        # Purge every already-loaded drivers.* module so a prior test in the same
        # run can't mask the result — then importing drivers.vercel alone must not
        # re-import trustpager or meta-ads.
        for m in [m for m in list(sys.modules) if m.startswith("drivers.")]:
            del sys.modules[m]
        importlib.import_module("drivers.vercel")
        self.assertNotIn("drivers.trustpager", sys.modules)  # boundary: no cross-vendor import
        self.assertNotIn("drivers.meta_ads", sys.modules)


if __name__ == "__main__":
    unittest.main()

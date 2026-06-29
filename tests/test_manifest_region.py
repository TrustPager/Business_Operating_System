"""Tests for the requires_region optional manifest key (P5 Task 1.1).

requires_region gates a skill to a specific region. The only allowed value is
AU (for now). When absent the manifest is still valid. When present with an
unknown value, or when given a list instead of a scalar, the validator returns
errors.

Offline-safe: no network, no key. Run:
    BOS_OFFLINE=1 python -m unittest tests.test_manifest_region -v
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
from manifest import validate_manifest  # noqa: E402


def _base() -> dict:
    """Minimal valid manifest matching the spec given in the task."""
    return {
        "function_slot": "money",
        "requires_driver": "none",
        "requires_credential": "none",
        "data_path": "reasoning_only",
    }


class TestRequiresRegion(unittest.TestCase):
    def test_requires_region_au_validates_clean(self):
        """A manifest with requires_region: AU must return no errors."""
        meta = _base()
        meta["requires_region"] = "AU"
        self.assertEqual(validate_manifest(meta), [])

    def test_requires_region_absent_validates_clean(self):
        """A manifest without requires_region must return no errors."""
        meta = _base()
        self.assertNotIn("requires_region", meta)
        self.assertEqual(validate_manifest(meta), [])

    def test_requires_region_unknown_value_is_an_error(self):
        """A manifest with requires_region set to an unknown value must fail."""
        meta = _base()
        meta["requires_region"] = "US"
        errors = validate_manifest(meta)
        self.assertTrue(errors, "expected at least one error for unknown region 'US'")
        self.assertTrue(
            any("requires_region" in e for e in errors),
            f"expected 'requires_region' in error messages, got: {errors}",
        )

    def test_requires_region_list_is_an_error(self):
        """requires_region must be a scalar; a list value must fail."""
        meta = _base()
        meta["requires_region"] = ["AU"]
        errors = validate_manifest(meta)
        self.assertTrue(errors, "expected at least one error when requires_region is a list")
        self.assertTrue(
            any("requires_region" in e for e in errors),
            f"expected 'requires_region' in error messages, got: {errors}",
        )


if __name__ == "__main__":
    unittest.main()

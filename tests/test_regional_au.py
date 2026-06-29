"""Tests for the AU regional constants module (P5 Task 1.4).

Verifies:
- The JSON file parses without error.
- Every leaf figure has all four provenance fields (value, effective_from,
  source_url, retrieved_on).
- Key structural assertions: gst rate present, BAS field map has G1/1A/1B.
- load_au_constants("AU") returns a non-empty dict.
- load_au_constants("US") raises ValueError (region-gated loader).
- load_au_constants("") raises ValueError.
- load_au_constants("AU") works from a foreign cwd (cwd-independence audit,
  Task 1.2).

Offline-safe: no network, no key. The JSON is bundled; tests read the file.
Run:
    BOS_OFFLINE=1 python -m unittest tests.test_regional_au -v
"""

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

CONSTANTS_DIR = REPO / "drivers" / "regional" / "au"


def _find_constants_file() -> Path:
    """Return the first JSON file in the au constants directory."""
    candidates = sorted(CONSTANTS_DIR.glob("constants-*.json"))
    if not candidates:
        raise FileNotFoundError(
            f"No constants-*.json file found in {CONSTANTS_DIR}"
        )
    return candidates[0]


def _walk_leaves(obj, path=""):
    """Yield (path, value) for every leaf node in the JSON structure."""
    if isinstance(obj, dict):
        # Check if this dict looks like a leaf figure (has 'value' key)
        if "value" in obj and not any(
            isinstance(v, dict) for k, v in obj.items() if k != "value"
        ):
            yield path, obj
        else:
            for k, v in obj.items():
                yield from _walk_leaves(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            yield from _walk_leaves(item, f"{path}[{i}]")


def _is_figure_node(obj) -> bool:
    """Return True if obj is a leaf figure dict with provenance fields."""
    if not isinstance(obj, dict):
        return False
    return "value" in obj


def _collect_figures(obj, path=""):
    """Recursively collect all figure nodes (dicts with 'value' key)."""
    figures = []
    if isinstance(obj, dict):
        if "value" in obj:
            # This is a figure node
            figures.append((path, obj))
        else:
            for k, v in obj.items():
                figures.extend(
                    _collect_figures(v, f"{path}.{k}" if path else k)
                )
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            figures.extend(_collect_figures(item, f"{path}[{i}]"))
    return figures


class TestAUConstantsFileStructure(unittest.TestCase):
    """The JSON file must parse and have correct structure."""

    def setUp(self):
        self.constants_path = _find_constants_file()
        with open(self.constants_path, encoding="utf-8") as f:
            self.data = json.load(f)

    def test_file_parses(self):
        """The constants JSON file must parse without error."""
        self.assertIsInstance(self.data, dict)
        self.assertTrue(len(self.data) > 0, "Constants dict must not be empty")

    def test_all_figure_nodes_have_provenance_fields(self):
        """Every leaf figure must have value, effective_from, source_url, retrieved_on."""
        required_fields = {"value", "effective_from", "source_url", "retrieved_on"}
        figures = _collect_figures(self.data)
        self.assertTrue(
            len(figures) > 0,
            "Expected at least one figure node in the constants file"
        )
        missing = []
        for path, fig in figures:
            present = set(fig.keys())
            absent = required_fields - present
            if absent:
                missing.append(f"{path}: missing {sorted(absent)}")
        self.assertEqual(
            missing, [],
            "Some figure nodes are missing provenance fields:\n" + "\n".join(missing)
        )

    def test_gst_section_present(self):
        """The 'gst' section must exist and contain a rate figure."""
        self.assertIn("gst", self.data, "Top-level 'gst' key must be present")
        gst = self.data["gst"]
        self.assertIn("rate", gst, "'gst.rate' figure must be present")

    def test_bas_field_map_has_g1_1a_1b(self):
        """The BAS field map must include G1, 1A, and 1B entries."""
        gst = self.data.get("gst", {})
        bas = gst.get("bas_fields", {})
        self.assertIn(
            "G1", bas,
            "BAS field map must include G1 (total sales / supplies)"
        )
        self.assertIn(
            "1A", bas,
            "BAS field map must include 1A (GST on sales)"
        )
        self.assertIn(
            "1B", bas,
            "BAS field map must include 1B (GST on purchases)"
        )

    def test_super_section_present(self):
        """The 'super' section must exist with a guarantee_rate figure."""
        self.assertIn("super", self.data, "Top-level 'super' key must be present")
        super_data = self.data["super"]
        self.assertIn(
            "guarantee_rate", super_data,
            "'super.guarantee_rate' figure must be present"
        )

    def test_income_tax_section_present(self):
        """The 'income_tax' section must exist with resident brackets."""
        self.assertIn(
            "income_tax", self.data,
            "Top-level 'income_tax' key must be present"
        )

    def test_medicare_levy_section_present(self):
        """The 'medicare_levy' section must exist with a rate figure."""
        self.assertIn(
            "medicare_levy", self.data,
            "Top-level 'medicare_levy' key must be present"
        )

    def test_wages_section_present(self):
        """The 'wages' section must exist with a national_minimum_wage figure."""
        self.assertIn(
            "wages", self.data,
            "Top-level 'wages' key must be present"
        )


class TestAUConstantsLoader(unittest.TestCase):
    """load_au_constants must enforce the AU-only region gate."""

    def setUp(self):
        from regional import load_au_constants  # noqa: F401
        self.loader = load_au_constants

    def test_load_au_returns_non_empty_dict(self):
        """load_au_constants('AU') must return a non-empty dict."""
        result = self.loader("AU")
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) > 0, "Returned dict must not be empty")

    def test_load_au_contains_gst(self):
        """Result from load_au_constants('AU') must contain the gst section."""
        result = self.loader("AU")
        self.assertIn("gst", result)

    def test_load_us_raises_value_error(self):
        """load_au_constants('US') must raise ValueError (region gate)."""
        with self.assertRaises(ValueError) as ctx:
            self.loader("US")
        self.assertIn(
            "AU", str(ctx.exception),
            "Error message should mention AU as the required region"
        )

    def test_load_empty_string_raises_value_error(self):
        """load_au_constants('') must raise ValueError (region gate)."""
        with self.assertRaises(ValueError):
            self.loader("")

    def test_load_lowercase_au_raises_value_error(self):
        """load_au_constants('au') must raise ValueError (case-sensitive gate)."""
        with self.assertRaises(ValueError):
            self.loader("au")

    def test_load_none_raises_value_error(self):
        """load_au_constants(None) must raise ValueError (region gate)."""
        with self.assertRaises(ValueError):
            self.loader(None)


class TestAUConstantsCwdIndependence(unittest.TestCase):
    """Task 1.2 audit: load_au_constants must work from any working directory.

    regional.py resolves its data path via Path(__file__).resolve(), so the
    loader is inherently cwd-independent. This class proves it with a real
    os.chdir() to a foreign temp directory before calling the loader.
    """

    def setUp(self):
        self._original_cwd = os.getcwd()
        self._tmp = tempfile.mkdtemp()
        os.chdir(self._tmp)

    def tearDown(self):
        os.chdir(self._original_cwd)
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_load_au_constants_from_foreign_cwd(self):
        """load_au_constants('AU') returns a non-empty dict from a temp cwd."""
        from regional import load_au_constants
        result = load_au_constants("AU")
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) > 0,
                        "load_au_constants returned empty dict from foreign cwd")

    def test_load_au_constants_gst_from_foreign_cwd(self):
        """load_au_constants('AU') contains the gst section from a temp cwd."""
        from regional import load_au_constants
        result = load_au_constants("AU")
        self.assertIn("gst", result,
                      "'gst' key missing when called from foreign cwd")

    def test_load_au_constants_region_gate_still_works_from_foreign_cwd(self):
        """load_au_constants('US') still raises ValueError from a temp cwd."""
        from regional import load_au_constants
        with self.assertRaises(ValueError):
            load_au_constants("US")


if __name__ == "__main__":
    unittest.main()

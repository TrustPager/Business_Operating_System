"""Offline-safe: no network, no key. Run: BOS_OFFLINE=1 python -m unittest tests.test_check_connectors"""
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _load_cc():
    """Load tools/check-connectors.py (hyphenated filename) as a module.

    A hyphen is illegal in an import statement, so importlib.import_module can
    never reach it; a from-file spec is the only way to load it by path.
    """
    spec = importlib.util.spec_from_file_location(
        "check_connectors", REPO / "tools" / "check-connectors.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestSafetyParity(unittest.TestCase):
    def test_gate_passes_clean_on_real_tree(self):
        r = subprocess.run([sys.executable, "tools/check-connectors.py"], cwd=REPO,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_reads_never_call_from_driver_dict(self):
        cc = _load_cc()
        drivers = cc._load_driver_dicts()
        self.assertIn("meta-ads", drivers)
        self.assertNotIn("_template", drivers)          # underscore dirs skipped
        self.assertNotIn("trustpager", drivers)         # no DRIVER dict -> grandfathered
        self.assertIn("mcp__meta-ads__ads_activate_entity", drivers["meta-ads"]["never_call"])


if __name__ == "__main__":
    unittest.main()

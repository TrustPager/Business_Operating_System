"""Offline-safe: no network, no key. Run: BOS_OFFLINE=1 python -m unittest tests.test_check_connectors"""
import importlib.util
import subprocess
import sys
import tempfile
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
        self.assertNotIn("_noop", drivers)              # underscore dirs skipped (exists on disk)
        self.assertNotIn("trustpager", drivers)         # no DRIVER dict -> grandfathered
        self.assertIn("mcp__meta-ads__ads_activate_entity", drivers["meta-ads"]["never_call"])


class TestDriverDiscoveryHardening(unittest.TestCase):
    """M-1 (AnnAssign) and M-2 (non-dict guard) against a synthetic drivers/ tree.

    Points the module's REPO_ROOT at a temp dir so _load_driver_dicts scans our
    fixtures instead of the real repo. Offline, no network, no real driver code run.
    """

    def _load_dicts_over(self, drivers_layout: dict) -> dict:
        cc = _load_cc()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for drv_id, body in drivers_layout.items():
                pkg = root / "drivers" / drv_id
                pkg.mkdir(parents=True)
                (pkg / "__init__.py").write_text(body, encoding="utf-8")
            cc.REPO_ROOT = root
            return cc._load_driver_dicts()

    def test_annotated_driver_is_picked_up(self):
        # M-1: `DRIVER: dict = {...}` (AnnAssign) must be discovered, not silently
        # skipped — a missed forbidden surface is a false-negative on a safety gate.
        drivers = self._load_dicts_over({
            "annotated": 'DRIVER: dict = {"never_call": ["mcp__annotated__zap"]}\n',
        })
        self.assertIn("annotated", drivers)
        self.assertEqual(drivers["annotated"]["never_call"], ["mcp__annotated__zap"])

    def test_bare_annotation_binds_nothing(self):
        # `DRIVER: dict` with no value assigns nothing — must not appear.
        drivers = self._load_dicts_over({"empty": "DRIVER: dict\n"})
        self.assertNotIn("empty", drivers)

    def test_non_dict_driver_is_skipped_without_raising(self):
        # M-2: a non-dict DRIVER (here a list) must be skipped, never crash the gate.
        drivers = self._load_dicts_over({
            "listy": 'DRIVER = ["not", "a", "dict"]\n',
            "good": 'DRIVER = {"never_call": ["mcp__good__zap"]}\n',
        })
        self.assertNotIn("listy", drivers)
        self.assertIn("good", drivers)  # the good driver alongside it is still read


# --- Task 2: structural conformance over --root fixture trees ----------------
#
# The real gate scans the repo, so conformance is exercised against self-contained
# fixture trees under tests/fixtures/connectors/ via the new --root flag. Each good
# tree exits 0; each broken tree exits 2 and names the failing rule in its output.

_FIX = REPO / "tests" / "fixtures" / "connectors"


def _run(root):
    """Run the checker over a fixture --root, capturing stdout/stderr + exit code."""
    return subprocess.run(
        [sys.executable, "tools/check-connectors.py", "--root", str(root)],
        cwd=REPO, capture_output=True, text=True,
    )


class TestConformance(unittest.TestCase):
    def test_good_claude_mcp_passes(self):
        r = _run(_FIX / "good-claude-mcp")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_good_keyed_cli_passes(self):
        # The second connected kind, exercising the data_path: local contract branch.
        r = _run(_FIX / "good-keyed-cli")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_bad_kind_fails(self):
        r = _run(_FIX / "bad-kind")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("kind", r.stdout)

    def test_bad_requires_driver_fails(self):
        r = _run(_FIX / "bad-requires-driver")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("requires_driver", r.stdout)

    def test_missing_connect_md_fails(self):
        r = _run(_FIX / "missing-connect-md")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("connect.md", r.stdout)

    def test_missing_card_fails(self):
        r = _run(_FIX / "missing-card")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("card", r.stdout)

    def test_bad_frontmatter_fails(self):
        r = _run(_FIX / "bad-frontmatter")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        # The connected frontmatter contract covers credential/data_path/uses_tools;
        # this fixture trips data_path and a foreign uses_tools entry.
        self.assertIn("data_path", r.stdout)
        self.assertIn("uses_tools", r.stdout)

    def test_bad_credential_fails(self):
        # Complements bad-frontmatter: isolates the requires_credential sub-rule of
        # the connected frontmatter contract (data_path + uses_tools are valid here).
        r = _run(_FIX / "bad-credential")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("requires_credential", r.stdout)


if __name__ == "__main__":
    unittest.main()

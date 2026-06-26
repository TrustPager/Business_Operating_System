"""Regression test for tools/check-kernel-clean.py.

Makes the kernel-cleanliness checker itself trustworthy: a checker with no
teeth is worse than none. This plants a known vendor literal into a temp
"kernel-like" directory and asserts the scan flags it, then asserts a clean
file passes. If this test ever goes green against a planted literal, the CI
gate is lying.

Offline-safe: no network, no key. Run:
    python -m unittest tests.test_check_kernel_clean
"""

import importlib.util
import pathlib
import tempfile
import unittest

# The script filename is kebab-case (can't `import` it directly), so load it
# as a module by path — the same trick the rest of the suite uses for tools/.
_CHECKER_PATH = (
    pathlib.Path(__file__).resolve().parent.parent
    / "tools" / "check-kernel-clean.py"
)
_spec = importlib.util.spec_from_file_location("check_kernel_clean", _CHECKER_PATH)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


class TestCheckKernelClean(unittest.TestCase):
    def test_planted_literal_is_flagged(self):
        # Each planted literal should be caught by the case-insensitive scan.
        planted = [
            "X = 'tp_live_planted'",
            "Y = 'TP_TEST_planted'",
            "Z = 'https://api.trustpager.com/v1'",
            "W = open('bos.json')",
            "V = 'this is TrustPager code'",
        ]
        for snippet in planted:
            with self.subTest(snippet=snippet):
                with tempfile.TemporaryDirectory() as d:
                    root = pathlib.Path(d)
                    bad = root / "leak.py"
                    bad.write_text(snippet + "\n", encoding="utf-8")
                    findings = _mod.scan_dir(root)
                    self.assertTrue(
                        findings,
                        f"scan_dir failed to flag a planted literal: {snippet!r}",
                    )
                    # Finding should name the offending file and line.
                    joined = "\n".join(findings)
                    self.assertIn("leak.py", joined)

    def test_clean_file_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            (root / "clean.py").write_text(
                "def add(a, b):\n    return a + b  # vendor-neutral, no literals\n",
                encoding="utf-8",
            )
            findings = _mod.scan_dir(root)
            self.assertEqual(findings, [], f"clean file flagged: {findings}")

    def test_only_python_files_scanned(self):
        # A non-.py file containing a literal must not trip the scan.
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            (root / "notes.txt").write_text("tp_live_planted\n", encoding="utf-8")
            findings = _mod.scan_dir(root)
            self.assertEqual(findings, [], f"non-py file flagged: {findings}")


if __name__ == "__main__":
    unittest.main()

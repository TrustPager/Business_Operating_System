"""Tests for the 'tool' subcommand added to tools/run.py (Task 1.3a).

Covers:
  1. Happy path: 'tool finance_calc pmt ...' runs and exits 0 with JSON output.
  2. Unknown tool exits 2 with a clear error message.
  3. Path-traversal attempts are rejected with exit 2 (../setup, foo/bar, absolute).
  4. Regression: bare skill-name dispatch and --list are unchanged by the new mode.

Offline-safe: no network, no CRM key.
Run:
    BOS_OFFLINE=1 python -m unittest tests.test_run_tool_mode
"""

import json
import subprocess
import sys
import unittest
from importlib import util as importutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RUN_PY = REPO / "tools" / "run.py"


def _lib(name: str) -> bool:
    try:
        spec = importutil.find_spec(name)
        return spec is not None
    except (ImportError, ValueError):
        return False


HAS_NUMPY_FINANCIAL = _lib("numpy_financial")


def _run(args: list[str]) -> subprocess.CompletedProcess:
    """Invoke run.py as a subprocess with the given argument list."""
    return subprocess.run(
        [sys.executable, str(RUN_PY), *args],
        capture_output=True, text=True
    )


# ---------------------------------------------------------------------------
# 1. Happy path: tool subcommand runs finance_calc and returns JSON
# ---------------------------------------------------------------------------

@unittest.skipUnless(HAS_NUMPY_FINANCIAL, "numpy-financial not installed")
class TestToolHappyPath(unittest.TestCase):
    """'tool finance_calc pmt ...' runs the tool and returns valid JSON."""

    def test_tool_finance_calc_pmt_exits_0(self):
        proc = _run(["tool", "finance_calc", "pmt",
                     "--rate", "0.01", "--nper", "12", "--pv", "10000"])
        self.assertEqual(proc.returncode, 0,
                         f"expected exit 0; stderr:\n{proc.stderr}")

    def test_tool_finance_calc_pmt_json_result(self):
        proc = _run(["tool", "finance_calc", "pmt",
                     "--rate", "0.01", "--nper", "12", "--pv", "10000"])
        self.assertEqual(proc.returncode, 0, f"stderr:\n{proc.stderr}")
        data = json.loads(proc.stdout)
        self.assertIn("result", data)
        self.assertAlmostEqual(data["result"], 888.49, places=1)

    def test_tool_finance_calc_py_extension_accepted(self):
        """Both 'finance_calc' and 'finance_calc.py' resolve to the same script."""
        proc = _run(["tool", "finance_calc.py", "pmt",
                     "--rate", "0.01", "--nper", "12", "--pv", "10000"])
        self.assertEqual(proc.returncode, 0,
                         f"extension form should work; stderr:\n{proc.stderr}")
        data = json.loads(proc.stdout)
        self.assertIn("result", data)


# ---------------------------------------------------------------------------
# 2. Unknown tool exits 2 with a clear error
# ---------------------------------------------------------------------------

class TestToolUnknown(unittest.TestCase):
    """Unknown tool name exits 2 with a useful message."""

    def test_unknown_tool_exits_2(self):
        proc = _run(["tool", "no_such_tool"])
        self.assertEqual(proc.returncode, 2,
                         f"expected exit 2; got {proc.returncode}")

    def test_unknown_tool_stderr_mentions_name(self):
        proc = _run(["tool", "no_such_tool"])
        self.assertIn("no_such_tool", proc.stderr,
                      f"expected tool name in error; got:\n{proc.stderr}")

    def test_tool_missing_name_exits_2(self):
        """'tool' with no toolname argument exits 2."""
        proc = _run(["tool"])
        self.assertEqual(proc.returncode, 2,
                         f"expected exit 2 for missing toolname; got {proc.returncode}")


# ---------------------------------------------------------------------------
# 3. Path-traversal attempts are rejected with exit 2
# ---------------------------------------------------------------------------

class TestToolTraversalRejection(unittest.TestCase):
    """Unsafe tool names are rejected before any execution."""

    def test_traversal_dotdot_slash(self):
        proc = _run(["tool", "../setup"])
        self.assertEqual(proc.returncode, 2,
                         f"'../setup' should be rejected; got exit {proc.returncode}")
        self.assertTrue(proc.stderr, "expected an error message on stderr")

    def test_traversal_slash_in_name(self):
        proc = _run(["tool", "foo/bar"])
        self.assertEqual(proc.returncode, 2,
                         f"'foo/bar' should be rejected; got exit {proc.returncode}")

    def test_traversal_backslash_in_name(self):
        proc = _run(["tool", "foo\\bar"])
        self.assertEqual(proc.returncode, 2,
                         f"'foo\\bar' should be rejected; got exit {proc.returncode}")

    def test_traversal_absolute_path_unix_style(self):
        proc = _run(["tool", "/etc/passwd"])
        self.assertEqual(proc.returncode, 2,
                         f"absolute path should be rejected; got exit {proc.returncode}")

    def test_traversal_absolute_path_windows_style(self):
        proc = _run(["tool", "C:\\Windows\\System32\\cmd.exe"])
        self.assertEqual(proc.returncode, 2,
                         f"Windows absolute path should be rejected; got exit {proc.returncode}")

    def test_traversal_does_not_execute_setup(self):
        """Confirm ../setup cannot be invoked by checking setup.py is NOT run."""
        proc = _run(["tool", "../setup"])
        self.assertEqual(proc.returncode, 2)
        # setup.py prints install-related output; none should appear.
        self.assertNotIn("Installing", proc.stdout)
        self.assertNotIn("setup", proc.stdout)


# ---------------------------------------------------------------------------
# 4. Regression: existing --list and skill-dispatch paths are unchanged
# ---------------------------------------------------------------------------

class TestSkillDispatchRegression(unittest.TestCase):
    """'tool' mode must not break the existing skill or --list dispatch."""

    def test_list_flag_still_works(self):
        proc = _run(["--list"])
        self.assertEqual(proc.returncode, 0,
                         f"--list should still exit 0; stderr:\n{proc.stderr}")
        # Output is either skill names or the '(no skills...)' message.
        self.assertTrue(proc.stdout.strip(), "expected some output from --list")

    def test_help_flag_still_works(self):
        proc = _run(["--help"])
        self.assertEqual(proc.returncode, 0)
        self.assertIn("tool", proc.stdout.lower(),
                      "help output should mention 'tool' subcommand")

    def test_unknown_skill_still_exits_2(self):
        """A bare unknown skill name (not 'tool') must still exit 2."""
        proc = _run(["_no_such_skill_xyz"])
        self.assertEqual(proc.returncode, 2,
                         f"unknown skill should exit 2; got {proc.returncode}")

    def test_unknown_skill_stderr_unchanged(self):
        """Error path for missing skill still mentions the skill name."""
        proc = _run(["_no_such_skill_xyz"])
        self.assertIn("_no_such_skill_xyz", proc.stderr,
                      f"expected skill name in error; got:\n{proc.stderr}")


if __name__ == "__main__":
    unittest.main()

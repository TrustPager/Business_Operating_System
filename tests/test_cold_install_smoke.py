"""Cold-install smoke: proves clone -> setup -> signpost -> tool run from a foreign cwd.

This is the gate that verifies a fresh install actually works end to end:

  1. Stage the install: run tools/setup.py as a real subprocess with a temp
     HOME (HOME + USERPROFILE both redirected) and blank-key input piped in
     (keyless skip). Asserts that bos.json, bos-run.py, and the skill/command
     copies all land in <temphome>/.claude/.

  2. Invoke the signpost from a DIFFERENT temp dir (not the repo root) to
     prove that cwd-independence is real, not accidental:
     - Unknown-tool call verifies the signpost chain resolves (exit 2 = wired).
     - write_xlsx -> markitdown_convert round-trip (skipped when openpyxl or
       markitdown absent so a stripped env does not fail the whole suite).
     - finance_calc pmt (skipped when numpy_financial absent).

Why subprocess for the install stage instead of direct function calls:
  setup.py imports trustpager_api (which in turn reads CONFIG_PATH from
  Path.home() at module level). Running as a subprocess is the only way to
  truly redirect Path.home() for the import, giving us a hermetic install that
  matches what a real end-user runs. The subprocess also exercises the full
  --skip-deps + blank-key input path.

Offline, hermetic, never touches the real ~/.claude.

Run:
    BOS_OFFLINE=1 python -m unittest tests.test_cold_install_smoke
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from importlib import util as importutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SETUP_PY = REPO / "tools" / "setup.py"
RUN_PY = REPO / "tools" / "run.py"


# ---------------------------------------------------------------------------
# Library availability guards (mirror the pattern from test_run_tool_mode.py)
# ---------------------------------------------------------------------------

def _lib(name: str) -> bool:
    try:
        spec = importutil.find_spec(name)
        return spec is not None
    except (ImportError, ValueError):
        return False


HAS_OPENPYXL = _lib("openpyxl")
HAS_MARKITDOWN = _lib("markitdown")
HAS_NUMPY_FINANCIAL = _lib("numpy_financial")

_HAS_ROUND_TRIP_LIBS = HAS_OPENPYXL and HAS_MARKITDOWN


# ---------------------------------------------------------------------------
# Shared fixture: one install per test class, not per test method
# ---------------------------------------------------------------------------

def _build_env(temp_home: str) -> dict[str, str]:
    """Return an env dict with HOME and USERPROFILE pointing at temp_home."""
    env = os.environ.copy()
    env["HOME"] = temp_home
    env["USERPROFILE"] = temp_home
    return env


def _stage_install(temp_home: str) -> subprocess.CompletedProcess:
    """Run setup.py --skip-deps with blank key input into temp_home.

    --skip-deps skips the pip install so the test stays offline and fast.
    Blank input triggers the keyless skip path (_write_keyless).
    """
    env = _build_env(temp_home)
    proc = subprocess.run(
        [sys.executable, str(SETUP_PY), "--skip-deps"],
        input="\n",           # blank key -> keyless skip
        capture_output=True,
        text=True,
        env=env,
    )
    return proc


# ---------------------------------------------------------------------------
# Stage 1: install artifacts
# ---------------------------------------------------------------------------

class TestColdInstallArtifacts(unittest.TestCase):
    """setup.py writes bos.json, bos-run.py, and skill/command copies into
    a temporary home directory, proving the install stage is complete."""

    @classmethod
    def setUpClass(cls):
        cls._tmpdir = tempfile.TemporaryDirectory()
        cls.temp_home = cls._tmpdir.name
        cls.claude_dir = Path(cls.temp_home) / ".claude"
        cls.proc = _stage_install(cls.temp_home)

    @classmethod
    def tearDownClass(cls):
        cls._tmpdir.cleanup()

    def test_setup_exits_zero(self):
        """setup.py --skip-deps with blank key must exit 0."""
        self.assertEqual(
            self.proc.returncode, 0,
            f"setup.py exited {self.proc.returncode}; stderr:\n{self.proc.stderr}"
        )

    def test_bos_json_exists(self):
        """bos.json must land in <temphome>/.claude/ after setup."""
        bos_json = self.claude_dir / "bos.json"
        self.assertTrue(
            bos_json.exists(),
            f"bos.json not found at {bos_json}; stdout:\n{self.proc.stdout}"
        )

    def test_bos_json_has_bos_home(self):
        """bos.json must contain bos_home pointing at the real repo."""
        bos_json = self.claude_dir / "bos.json"
        if not bos_json.exists():
            self.skipTest("bos.json absent (covered by prior test)")
        cfg = json.loads(bos_json.read_text(encoding="utf-8"))
        self.assertIn("bos_home", cfg, "bos_home key missing from bos.json")
        # The bos_home must resolve to the repo (or a realpath equivalent).
        stored = Path(cfg["bos_home"]).resolve()
        expected = REPO.resolve()
        self.assertEqual(stored, expected,
                         f"bos_home mismatch: got {stored}, expected {expected}")

    def test_bos_json_no_api_key(self):
        """Keyless skip must NOT write an api_key."""
        bos_json = self.claude_dir / "bos.json"
        if not bos_json.exists():
            self.skipTest("bos.json absent")
        cfg = json.loads(bos_json.read_text(encoding="utf-8"))
        self.assertNotIn("api_key", cfg,
                         "api_key must not be written on keyless install")

    def test_signpost_shim_exists(self):
        """bos-run.py signpost must exist in <temphome>/.claude/."""
        shim = self.claude_dir / "bos-run.py"
        self.assertTrue(
            shim.exists(),
            f"bos-run.py not found at {shim}; stdout:\n{self.proc.stdout}"
        )

    def test_signpost_shim_references_bos_json(self):
        """Signpost content must read bos_home from bos.json (sanity check)."""
        shim = self.claude_dir / "bos-run.py"
        if not shim.exists():
            self.skipTest("bos-run.py absent")
        content = shim.read_text(encoding="utf-8")
        self.assertIn("bos.json", content, "shim must reference bos.json")

    def test_skills_directory_created(self):
        """<temphome>/.claude/skills/ must exist after setup."""
        skills_dir = self.claude_dir / "skills"
        self.assertTrue(
            skills_dir.is_dir(),
            f"skills/ directory not found at {skills_dir}"
        )

    def test_commands_directory_created(self):
        """<temphome>/.claude/commands/ must exist after setup."""
        commands_dir = self.claude_dir / "commands"
        self.assertTrue(
            commands_dir.is_dir(),
            f"commands/ directory not found at {commands_dir}"
        )

    def test_at_least_one_skill_installed(self):
        """At least one BOS skill must be copied into <temphome>/.claude/skills/."""
        skills_dir = self.claude_dir / "skills"
        if not skills_dir.is_dir():
            self.skipTest("skills/ absent")
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        self.assertGreater(
            len(skill_dirs), 0,
            "No skill directories found in ~/.claude/skills/"
        )

    def test_installed_skills_recorded_in_bos_json(self):
        """bos.json must record installed_skills after setup."""
        bos_json = self.claude_dir / "bos.json"
        if not bos_json.exists():
            self.skipTest("bos.json absent")
        cfg = json.loads(bos_json.read_text(encoding="utf-8"))
        self.assertIn("installed_skills", cfg,
                      "installed_skills key missing from bos.json")
        self.assertIsInstance(cfg["installed_skills"], list)


# ---------------------------------------------------------------------------
# Stage 2: signpost invocation from a foreign working directory
# ---------------------------------------------------------------------------

def _run_via_signpost(
    shim: Path,
    args: list[str],
    cwd: str,
    temp_home: str,
) -> subprocess.CompletedProcess:
    """Invoke the signpost shim from a foreign cwd with the temp HOME set."""
    env = _build_env(temp_home)
    return subprocess.run(
        [sys.executable, str(shim), *args],
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
    )


class TestSignpostChainResolution(unittest.TestCase):
    """The signpost resolves bos_home and dispatches tool calls regardless of cwd.

    An unknown-tool call through the signpost must exit 2 with a recognisable
    error from run.py (not a Python traceback from the shim itself). This proves
    the full chain -- shim reads bos.json, finds run.py, hands off -- without
    needing any optional libs.
    """

    @classmethod
    def setUpClass(cls):
        cls._tmpdir = tempfile.TemporaryDirectory()
        cls.temp_home = cls._tmpdir.name
        cls._foreign_dir = tempfile.TemporaryDirectory()
        cls.foreign_cwd = cls._foreign_dir.name
        proc = _stage_install(cls.temp_home)
        cls.install_ok = (proc.returncode == 0)
        cls.install_stderr = proc.stderr

    @classmethod
    def tearDownClass(cls):
        cls._tmpdir.cleanup()
        cls._foreign_dir.cleanup()

    def _shim(self) -> Path:
        return Path(self.temp_home) / ".claude" / "bos-run.py"

    def test_install_succeeded_before_chain_tests(self):
        """Install stage must succeed before chain tests can be meaningful."""
        self.assertTrue(
            self.install_ok,
            f"setup.py failed; cannot test signpost chain. stderr:\n{self.install_stderr}"
        )

    def test_unknown_tool_exits_2_via_signpost(self):
        """An unknown tool name through the signpost exits 2 (chain is wired)."""
        if not self.install_ok:
            self.skipTest("install stage failed")
        proc = _run_via_signpost(
            self._shim(),
            ["tool", "_bos_smoke_no_such_tool"],
            cwd=self.foreign_cwd,
            temp_home=self.temp_home,
        )
        self.assertEqual(
            proc.returncode, 2,
            f"Expected exit 2 for unknown tool; got {proc.returncode}. "
            f"stderr:\n{proc.stderr}"
        )

    def test_unknown_tool_stderr_mentions_tool_name(self):
        """run.py error message must name the unknown tool (not a raw traceback)."""
        if not self.install_ok:
            self.skipTest("install stage failed")
        proc = _run_via_signpost(
            self._shim(),
            ["tool", "_bos_smoke_no_such_tool"],
            cwd=self.foreign_cwd,
            temp_home=self.temp_home,
        )
        self.assertIn(
            "_bos_smoke_no_such_tool", proc.stderr,
            f"Tool name not in error; stderr:\n{proc.stderr}"
        )

    def test_cwd_is_foreign_not_repo(self):
        """Confirm the foreign cwd really is outside the repo (not a false pass)."""
        foreign = Path(self.foreign_cwd).resolve()
        repo = REPO.resolve()
        self.assertFalse(
            str(foreign).startswith(str(repo)),
            f"foreign_cwd {foreign} is inside the repo {repo}; test is not hermetic"
        )


class TestSignpostToolRoundTrip(unittest.TestCase):
    """write_xlsx -> markitdown_convert round-trip through the signpost shim.

    Skipped when openpyxl or markitdown is absent so a stripped env does not
    fail the whole suite. The chain-resolution test above covers that case.
    """

    @classmethod
    def setUpClass(cls):
        cls._tmpdir = tempfile.TemporaryDirectory()
        cls.temp_home = cls._tmpdir.name
        cls._foreign_dir = tempfile.TemporaryDirectory()
        cls.foreign_cwd = cls._foreign_dir.name
        proc = _stage_install(cls.temp_home)
        cls.install_ok = (proc.returncode == 0)
        cls.install_stderr = proc.stderr

    @classmethod
    def tearDownClass(cls):
        cls._tmpdir.cleanup()
        cls._foreign_dir.cleanup()

    def _shim(self) -> Path:
        return Path(self.temp_home) / ".claude" / "bos-run.py"

    @unittest.skipUnless(_HAS_ROUND_TRIP_LIBS, "openpyxl or markitdown not installed")
    def test_write_xlsx_exits_zero_via_signpost(self):
        """write_xlsx through the signpost exits 0 from a foreign cwd."""
        if not self.install_ok:
            self.skipTest("install stage failed")
        xlsx_path = os.path.join(self.foreign_cwd, "smoke.xlsx")
        proc = _run_via_signpost(
            self._shim(),
            ["tool", "write_xlsx",
             "--out", xlsx_path,
             "--rows", '[["A","B"],[1,2]]',
             "--header"],
            cwd=self.foreign_cwd,
            temp_home=self.temp_home,
        )
        self.assertEqual(
            proc.returncode, 0,
            f"write_xlsx via signpost exited {proc.returncode}; "
            f"stderr:\n{proc.stderr}"
        )

    @unittest.skipUnless(_HAS_ROUND_TRIP_LIBS, "openpyxl or markitdown not installed")
    def test_write_xlsx_creates_file_via_signpost(self):
        """write_xlsx through the signpost produces a real .xlsx file."""
        if not self.install_ok:
            self.skipTest("install stage failed")
        xlsx_path = os.path.join(self.foreign_cwd, "smoke_create.xlsx")
        _run_via_signpost(
            self._shim(),
            ["tool", "write_xlsx",
             "--out", xlsx_path,
             "--rows", '[["X","Y"],[10,20]]'],
            cwd=self.foreign_cwd,
            temp_home=self.temp_home,
        )
        self.assertTrue(
            os.path.isfile(xlsx_path),
            f"smoke_create.xlsx not created at {xlsx_path}"
        )

    @unittest.skipUnless(_HAS_ROUND_TRIP_LIBS, "openpyxl or markitdown not installed")
    def test_markitdown_reads_back_xlsx_via_signpost(self):
        """markitdown_convert through the signpost reads back the written .xlsx.

        This is the full round-trip: write_xlsx writes, markitdown_convert reads.
        Both calls go through the signpost from the foreign cwd.
        """
        if not self.install_ok:
            self.skipTest("install stage failed")

        xlsx_path = os.path.join(self.foreign_cwd, "smoke_rt.xlsx")
        marker = "BOSsmoke99"

        # Write
        w = _run_via_signpost(
            self._shim(),
            ["tool", "write_xlsx",
             "--out", xlsx_path,
             "--rows", f'[["{marker}", 42]]'],
            cwd=self.foreign_cwd,
            temp_home=self.temp_home,
        )
        self.assertEqual(
            w.returncode, 0,
            f"write_xlsx failed; stderr:\n{w.stderr}"
        )

        # Read back
        r = _run_via_signpost(
            self._shim(),
            ["tool", "markitdown_convert", xlsx_path],
            cwd=self.foreign_cwd,
            temp_home=self.temp_home,
        )
        self.assertEqual(
            r.returncode, 0,
            f"markitdown_convert failed; stderr:\n{r.stderr}"
        )
        self.assertIn(
            marker, r.stdout,
            f"Round-trip failed: marker {marker!r} not in markitdown output.\n"
            f"stdout:\n{r.stdout}"
        )


class TestSignpostFinanceCalc(unittest.TestCase):
    """finance_calc pmt through the signpost from a foreign cwd.

    Skipped when numpy_financial is absent.
    """

    @classmethod
    def setUpClass(cls):
        cls._tmpdir = tempfile.TemporaryDirectory()
        cls.temp_home = cls._tmpdir.name
        cls._foreign_dir = tempfile.TemporaryDirectory()
        cls.foreign_cwd = cls._foreign_dir.name
        proc = _stage_install(cls.temp_home)
        cls.install_ok = (proc.returncode == 0)
        cls.install_stderr = proc.stderr

    @classmethod
    def tearDownClass(cls):
        cls._tmpdir.cleanup()
        cls._foreign_dir.cleanup()

    def _shim(self) -> Path:
        return Path(self.temp_home) / ".claude" / "bos-run.py"

    @unittest.skipUnless(HAS_NUMPY_FINANCIAL, "numpy_financial not installed")
    def test_finance_calc_pmt_exits_zero_via_signpost(self):
        """finance_calc pmt through the signpost exits 0 from a foreign cwd."""
        if not self.install_ok:
            self.skipTest("install stage failed")
        proc = _run_via_signpost(
            self._shim(),
            ["tool", "finance_calc", "pmt",
             "--rate", "0.01", "--nper", "12", "--pv", "10000"],
            cwd=self.foreign_cwd,
            temp_home=self.temp_home,
        )
        self.assertEqual(
            proc.returncode, 0,
            f"finance_calc pmt via signpost exited {proc.returncode}; "
            f"stderr:\n{proc.stderr}"
        )

    @unittest.skipUnless(HAS_NUMPY_FINANCIAL, "numpy_financial not installed")
    def test_finance_calc_pmt_json_result_via_signpost(self):
        """finance_calc pmt returns valid JSON with the expected result field."""
        if not self.install_ok:
            self.skipTest("install stage failed")
        proc = _run_via_signpost(
            self._shim(),
            ["tool", "finance_calc", "pmt",
             "--rate", "0.01", "--nper", "12", "--pv", "10000"],
            cwd=self.foreign_cwd,
            temp_home=self.temp_home,
        )
        self.assertEqual(proc.returncode, 0, f"stderr:\n{proc.stderr}")
        import json
        data = json.loads(proc.stdout)
        self.assertIn("result", data)
        self.assertAlmostEqual(data["result"], 888.49, places=1)


if __name__ == "__main__":
    unittest.main()

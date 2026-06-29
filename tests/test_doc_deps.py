"""Tests for the D11 cold-install self-sufficiency wiring (Wave 1.5 Inc 1).

Two things are under test here, both offline/hermetic (no real pip, no network):

  1. Every doc tool emits the machine-readable ``BOS_MISSING_DEP: <spec>`` signal
     and exits NON-ZERO when its backing dependency is missing. We block the
     relevant import via a meta-path finder (mirroring tests/test_doc_lib_set.py)
     so the missing-dep branch fires deterministically even when the lib is
     installed in this environment. This is the signal the SKILL-layer offer loop
     keys off.

  2. tools/check-install.py serves the KEYLESS FLOOR first:
       - the write->read round-trip passes when the libs are present;
       - a blocked floor lib is reported with its BOS_MISSING_DEP spec and the
         doctor exits 1;
       - with NO CRM key configured the doctor still passes (it must not FAIL on a
         keyless install — the TrustPager probes sit behind a "key configured" branch).

Run:
    BOS_OFFLINE=1 python -m unittest tests.test_doc_deps
"""

import json
import os
import subprocess
import sys
import unittest
from importlib import util as importutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"


def _lib(name: str) -> bool:
    try:
        return importutil.find_spec(name) is not None
    except (ImportError, ValueError):
        return False


HAS_OPENPYXL = _lib("openpyxl")
HAS_DOCX = _lib("docx")
HAS_MARKITDOWN = _lib("markitdown")


def _key_configured() -> bool:
    """True if a TrustPager key is configured on this machine (env or bos.json).

    The keyless-floor tests assert the doctor's "no CRM key" branch, so they only
    apply when no key is configured. On a developer machine that HAS a key, we
    skip those (the connected tier would legitimately run)."""
    sys.path.insert(0, str(TOOLS))
    try:
        from trustpager_api import get_api_key, BOSError
        try:
            return bool((get_api_key() or "").strip())
        except BOSError:
            return False
    except Exception:  # noqa: BLE001
        return False


KEY_CONFIGURED = _key_configured()


def _run_blocked(script: str, args: list[str], block_import: str) -> subprocess.CompletedProcess:
    """Run a tools/ wrapper with ``block_import`` made un-importable.

    A meta-path finder raises ImportError for the blocked module (and its
    submodules), then we exec the real script — so the wrapper takes its
    missing-dependency branch deterministically.
    """
    preamble = (
        "import sys\n"
        f"_BLOCK = {block_import!r}\n"
        "class _Blocker:\n"
        "    def find_spec(self, name, path=None, target=None):\n"
        "        if name == _BLOCK or name.startswith(_BLOCK + '.'):\n"
        "            raise ImportError('blocked for test: ' + name)\n"
        "        return None\n"
        "sys.meta_path.insert(0, _Blocker())\n"
        f"sys.argv = [{str(TOOLS / script)!r}, *{args!r}]\n"
        f"exec(compile(open({str(TOOLS / script)!r}, encoding='utf-8').read(), "
        f"{str(TOOLS / script)!r}, 'exec'))\n"
    )
    return subprocess.run([sys.executable, "-c", preamble],
                          capture_output=True, text=True)


def _run_doctor(argv: list[str], *, block_import: str | None = None,
                env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    """Run tools/check-install.py, optionally with a blocked import, capturing output."""
    env = {**os.environ, "BOS_OFFLINE": "1"}
    if env_extra:
        env.update(env_extra)
    if block_import is None:
        return subprocess.run([sys.executable, str(TOOLS / "check-install.py"), *argv],
                              capture_output=True, text=True, env=env)
    preamble = (
        "import sys, runpy\n"
        f"_BLOCK = {block_import!r}\n"
        "class _Blocker:\n"
        "    def find_spec(self, name, path=None, target=None):\n"
        "        if name == _BLOCK or name.startswith(_BLOCK + '.'):\n"
        "            raise ImportError('blocked for test: ' + name)\n"
        "        return None\n"
        "sys.meta_path.insert(0, _Blocker())\n"
        f"sys.argv = [{str(TOOLS / 'check-install.py')!r}, *{argv!r}]\n"
        f"runpy.run_path({str(TOOLS / 'check-install.py')!r}, run_name='__main__')\n"
    )
    return subprocess.run([sys.executable, "-c", preamble],
                          capture_output=True, text=True, env=env)


# --- 1. Doc tools emit BOS_MISSING_DEP + exit non-zero --------------------


class TestMissingDepSignal(unittest.TestCase):
    """Every doc tool: a blocked import prints BOS_MISSING_DEP and exits non-zero."""

    def _assert_signal(self, proc: subprocess.CompletedProcess, spec: str) -> None:
        self.assertNotEqual(proc.returncode, 0, "tool must exit non-zero on missing dep")
        self.assertIn(f"BOS_MISSING_DEP: {spec}", proc.stderr,
                      f"expected the structured signal; got:\n{proc.stderr}")
        # The human line must recommend `python -m pip`, never a bare `pip`.
        self.assertIn("python -m pip install", proc.stderr)

    def test_write_xlsx_signal(self):
        proc = _run_blocked("write_xlsx.py", ["--out", "x.xlsx", "--rows", "[[1]]"], "openpyxl")
        self._assert_signal(proc, "openpyxl")

    def test_write_docx_signal(self):
        proc = _run_blocked("write_docx.py",
                            ["--out", "x.docx", "--blocks", '[{"type":"paragraph","text":"hi"}]'],
                            "docx")
        self._assert_signal(proc, "python-docx")

    def test_make_pdf_signal(self):
        proc = _run_blocked("make_pdf.py",
                            ["--out", "x.pdf", "--blocks", '[{"type":"paragraph","text":"hi"}]'],
                            "reportlab")
        self._assert_signal(proc, "reportlab")

    def test_pdf_tables_signal(self):
        proc = _run_blocked("pdf_tables.py", ["nonexistent.pdf"], "pdfplumber")
        self._assert_signal(proc, "pdfplumber")

    def test_no_bare_pip_recommendation(self):
        """None of the doc tools may recommend a BARE `pip install` (multi-Python trap)."""
        cases = [
            ("write_xlsx.py", ["--out", "x.xlsx", "--rows", "[[1]]"], "openpyxl"),
            ("write_docx.py", ["--out", "x.docx", "--blocks", '[{"type":"paragraph","text":"hi"}]'], "docx"),
            ("make_pdf.py", ["--out", "x.pdf", "--blocks", '[{"type":"paragraph","text":"hi"}]'], "reportlab"),
            ("pdf_tables.py", ["nope.pdf"], "pdfplumber"),
        ]
        for script, args, blk in cases:
            with self.subTest(script=script):
                proc = _run_blocked(script, args, blk)
                # The recommended command is always `python -m pip ...`; assert there is
                # no line that starts a recommendation with a bare `pip install`.
                for line in proc.stderr.splitlines():
                    stripped = line.strip()
                    self.assertFalse(stripped.startswith("pip install"),
                                     f"{script} recommended a bare pip: {line!r}")


@unittest.skipUnless(HAS_DOCX and HAS_MARKITDOWN,
                     "need python-docx + markitdown to build a .docx and exercise the read path")
class TestMarkitdownPerFormatMissingExtra(unittest.TestCase):
    """markitdown_convert.py must FAIL (not silently degrade) when the per-format
    reader extra is missing. We build a real .docx, then block `docx` so the docx
    reader extra is absent, and assert the wrapper names markitdown[docx] and exits
    non-zero rather than handing back a degraded fallback read."""

    def test_docx_read_missing_extra_signals_and_exits_nonzero(self):
        import tempfile
        import docx
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "probe.docx")
            doc = docx.Document()
            doc.add_paragraph("round trip body")
            doc.save(p)
            # Now block `docx` so markitdown's docx reader extra looks absent.
            proc = _run_blocked("markitdown_convert.py", [p], "docx")
            self.assertNotEqual(proc.returncode, 0,
                                f"expected non-zero on missing read extra; stderr:\n{proc.stderr}")
            self.assertIn("BOS_MISSING_DEP: markitdown[docx]", proc.stderr, proc.stderr)
            self.assertIn("python -m pip install markitdown[docx]", proc.stderr, proc.stderr)


class TestMarkitdownTotallyMissing(unittest.TestCase):
    """If markitdown itself is absent, the wrapper signals markitdown[all] + exits non-zero."""

    def test_markitdown_missing_signals_all(self):
        proc = _run_blocked("markitdown_convert.py", ["whatever.docx"], "markitdown")
        self.assertNotEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("BOS_MISSING_DEP: markitdown[all]", proc.stderr, proc.stderr)
        self.assertIn("python -m pip install markitdown[all]", proc.stderr, proc.stderr)


# --- 2. check-install.py keyless-floor mode -------------------------------


@unittest.skipIf(KEY_CONFIGURED,
                 "a TrustPager key is configured here — the connected tier runs; "
                 "the keyless-floor assertions only apply to a keyless install")
class TestCheckInstallKeylessFloor(unittest.TestCase):
    """The doctor serves the keyless floor first and never FAILs on a keyless install."""

    @unittest.skipUnless(HAS_DOCX and HAS_OPENPYXL and HAS_MARKITDOWN,
                         "round-trip needs python-docx, openpyxl, markitdown")
    def test_round_trip_passes_when_libs_present_and_no_key(self):
        proc = _run_doctor([])
        self.assertEqual(proc.returncode, 0,
                         f"keyless floor should pass; output:\n{proc.stdout}\n{proc.stderr}")
        self.assertIn("document round-trip works", proc.stdout)
        # Connected tier must be skipped, not failed, when no key is configured.
        self.assertIn("no CRM key configured", proc.stdout)
        self.assertNotIn("[FAIL]", proc.stdout)

    def test_blocked_floor_lib_reports_spec_and_exits_1(self):
        proc = _run_doctor([], block_import="openpyxl")
        self.assertEqual(proc.returncode, 1,
                         f"a missing floor lib must fail the doctor; output:\n{proc.stdout}")
        self.assertIn("BOS_MISSING_DEP: openpyxl", proc.stdout, proc.stdout)
        # Even with the floor failing, the connected tier must be skipped (no key), not errored.
        self.assertIn("no CRM key configured", proc.stdout)

    def test_fix_flag_no_op_when_present(self):
        """--fix is a real flag; with everything present it reports nothing to fix
        and the floor still passes. Hermetic: nothing is installed because nothing
        is missing (no real pip call)."""
        if not (HAS_DOCX and HAS_OPENPYXL and HAS_MARKITDOWN):
            self.skipTest("need the floor libs present to assert the no-op --fix path")
        proc = _run_doctor(["--fix"])
        self.assertEqual(proc.returncode, 0, f"{proc.stdout}\n{proc.stderr}")
        self.assertIn("Nothing to fix", proc.stdout)


if __name__ == "__main__":
    unittest.main()

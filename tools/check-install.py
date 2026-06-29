#!/usr/bin/env python3
"""Verify the Business Operating System install is healthy (doctor / healthcheck).

The keyless document floor comes FIRST. A brand-new owner with no account and no
key should still get a clean bill of health (the floor stands alone). So this
doctor verifies the keyless document stack with a real write -> read round-trip
by default, and only probes TrustPager when a CRM key is actually configured.

When to use:
- "Is my install working?"
- After running setup.py, to confirm the document tools are ready.
- "Reading/writing a document is failing. Is it a missing library?"
- (Connected tier) After connecting TrustPager or regenerating your API key.

What it checks (keyless floor, always):
- Python version >= 3.10
- The document WRITE tools produce a real .docx and .xlsx (python-docx, openpyxl)
- The document READ tool (markitdown) reads those files back (the round-trip)
- reportlab (PDF write) and pdfplumber (precise PDF read) import cleanly

What it checks (connected tier, only if a TrustPager key is configured):
- API key present and well-formed
- api.trustpager.com reachable + an authenticated read returns data
- Catalog fetch + local cache writable

Each missing document dependency is reported with its BOS_MISSING_DEP pip spec.
Run with --fix to install every missing dependency yourself, using the SAME
interpreter (sys.executable -m pip) so there's no multi-Python mismatch. This
is the openpyxl-interpreter-mismatch fix.

Output: green [OK] / orange [WARN] / red [FAIL] per check.
Exit code 0 if all REQUIRED checks pass; 1 if any fail.

Usage:
    python tools/check-install.py            # keyless floor first, CRM if configured
    python tools/check-install.py --fix      # install any missing document deps, then re-check
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from importlib import util as importutil
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent


def _ok(msg: str) -> None:
    print(f"  [OK]   {msg}")


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def _warn(msg: str) -> None:
    print(f"  [WARN] {msg}")


# --- The keyless document floor -------------------------------------------
#
# Each dep is (probe-module, pip-spec). The probe-module is what we import to
# tell if the dep is present; the pip-spec is exactly what we'd install. These
# are the BOS_MISSING_DEP specs the tools emit, so the doctor and the tools agree.
_FLOOR_DEPS: list[tuple[str, str]] = [
    ("docx", "python-docx"),      # write_docx.py
    ("openpyxl", "openpyxl"),     # write_xlsx.py
    ("reportlab", "reportlab"),   # make_pdf.py
    ("pdfplumber", "pdfplumber"), # pdf_tables.py
    ("markitdown", "markitdown[docx,pdf,xlsx,pptx]"),  # markitdown_convert.py (read)
]


def _present(module: str) -> bool:
    try:
        return importutil.find_spec(module) is not None
    except (ImportError, ValueError):
        return False


def _missing_floor_deps() -> list[tuple[str, str]]:
    """The (module, pip-spec) pairs from the floor stack that aren't importable."""
    return [(mod, spec) for (mod, spec) in _FLOOR_DEPS if not _present(mod)]


def _run_doc_round_trip() -> tuple[bool, str]:
    """Write a tiny .docx and .xlsx via the BOS write tools, then read them back
    via markitdown_convert.py. Returns (ok, detail). Pure local, no network."""
    import os
    with tempfile.TemporaryDirectory() as d:
        docx_path = os.path.join(d, "probe.docx")
        xlsx_path = os.path.join(d, "probe.xlsx")
        marker = "BOSroundtrip42"

        # 1. write .docx
        w = subprocess.run(
            [sys.executable, str(TOOLS / "write_docx.py"), "--out", docx_path,
             "--blocks", json.dumps([{"type": "paragraph", "text": marker}])],
            capture_output=True, text=True,
        )
        if w.returncode != 0 or not os.path.isfile(docx_path):
            return False, f"write_docx.py failed: {w.stderr.strip() or 'no file written'}"

        # 2. write .xlsx
        x = subprocess.run(
            [sys.executable, str(TOOLS / "write_xlsx.py"), "--out", xlsx_path,
             "--rows", json.dumps([[marker, 1]])],
            capture_output=True, text=True,
        )
        if x.returncode != 0 or not os.path.isfile(xlsx_path):
            return False, f"write_xlsx.py failed: {x.stderr.strip() or 'no file written'}"

        # 3. read each back via markitdown
        for path, label in ((docx_path, ".docx"), (xlsx_path, ".xlsx")):
            r = subprocess.run(
                [sys.executable, str(TOOLS / "markitdown_convert.py"), path],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                return False, f"reading the {label} back failed: {r.stderr.strip()}"
            if marker not in r.stdout:
                return False, (f"read the {label} but the content didn't round-trip "
                               f"(expected {marker!r})")
    return True, "wrote a .docx and .xlsx and read both back"


def _fix_missing(missing: list[tuple[str, str]]) -> int:
    """Install each missing pip-spec with this interpreter's pip. Returns the
    number that still fail to import afterward (0 == all healed)."""
    if not missing:
        return 0
    specs = [spec for (_mod, spec) in missing]
    print()
    print("Installing the missing document tools for you (one-time, same")
    print("interpreter so there's no version mismatch):")
    cmd = [sys.executable, "-m", "pip", "install", *specs]
    print(f"  {' '.join(cmd)}")
    try:
        subprocess.run(cmd)
    except OSError as e:
        print(f"  [warn] couldn't run pip ({e}).")
        return len(missing)
    # Re-probe (find_spec caches negative results within a process, so clear it).
    importutil.find_spec  # noqa: B018 (touch to keep import used)
    from importlib import invalidate_caches
    invalidate_caches()
    still = [(mod, spec) for (mod, spec) in missing if not _present(mod)]
    return len(still)


def check_floor() -> int:
    """The keyless document floor. Returns the number of failures."""
    failures = 0
    print("Keyless document floor:")

    missing = _missing_floor_deps()
    if not missing:
        _ok("all document libraries present "
            "(python-docx, openpyxl, reportlab, pdfplumber, markitdown)")
    else:
        for _mod, spec in missing:
            _fail(f"missing document dependency. BOS_MISSING_DEP: {spec}")
        print("       (re-run with --fix and I'll install these for you)")
        failures += len(missing)

    # The real proof: write -> read round-trip. Only attempt if the write+read
    # libs are present (otherwise the missing-dep failures above already explain it).
    needed_for_rt = {"docx", "openpyxl", "markitdown"}
    have_rt_libs = all(_present(m) for m in needed_for_rt)
    if have_rt_libs:
        ok, detail = _run_doc_round_trip()
        if ok:
            _ok(f"document round-trip works: {detail}")
        else:
            _fail(f"document round-trip failed: {detail}")
            failures += 1
    else:
        _warn("skipping the write->read round-trip until the libraries above are installed")
    return failures


def _configured_key() -> str | None:
    """Return a configured TrustPager key if one exists, else None, without
    raising. This is what decides whether to run the connected-tier probes."""
    sys.path.insert(0, str(TOOLS))
    try:
        from trustpager_api import get_api_key, BOSError  # noqa: E402
    except Exception:  # noqa: BLE001 (connected tier optional; never block the floor)
        return None
    try:
        key = (get_api_key() or "").strip()
        return key or None
    except BOSError:
        return None
    except Exception:  # noqa: BLE001
        return None


def check_connected(key: str) -> int:
    """The connected (TrustPager) tier. Only runs when a key is configured."""
    failures = 0
    sys.path.insert(0, str(TOOLS))
    from trustpager_api import (  # noqa: E402
        API_BASE, BOSError, CATALOG_CACHE_PATH, CATALOG_URL, get_catalog,
    )

    print()
    print("Connected tier, TrustPager (a key is configured):")

    if key.startswith("tp_live_"):
        _ok(f"API key configured (ends ...{key[-4:]})")
    else:
        _warn(f"API key set but doesn't start with 'tp_live_' (got '{key[:10]}...')")

    # API reach
    try:
        import urllib.request
        req = urllib.request.Request(
            API_BASE + "/", headers={"Authorization": f"Bearer {key}"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            _ok(f"Reached {API_BASE}/ ({resp.status})")
    except Exception as e:  # noqa: BLE001
        _fail(f"Could not reach {API_BASE}: {str(e).splitlines()[0]}")
        failures += 1

    # Catalog
    try:
        catalog = get_catalog()
        n_resources = len(catalog.get("resources", []))
        generated_at = catalog.get("generated_at", "?")
        _ok(f"Fetched catalog from {CATALOG_URL}: {n_resources} resources, "
            f"generated {generated_at}")
    except BOSError as e:
        _fail(str(e).splitlines()[0])
        failures += 1

    # Cache
    if CATALOG_CACHE_PATH.exists():
        _ok(f"Cache exists at {CATALOG_CACHE_PATH}")
    else:
        _warn(f"No cache yet at {CATALOG_CACHE_PATH} (created on first run)")
    try:
        CATALOG_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        probe = CATALOG_CACHE_PATH.parent / ".write-probe"
        probe.write_text("x", encoding="utf-8")
        probe.unlink()
        _ok(f"Cache directory writable: {CATALOG_CACHE_PATH.parent}")
    except OSError as e:
        _fail(f"Cache directory not writable: {e}")
        failures += 1

    # Authenticated read
    try:
        from trustpager_api import api_get
        r = api_get("opportunities", limit=1)
        n = len(r.get("data", []))
        _ok(f"GET /opportunities authenticated and responded ({n} row sample)")
    except BOSError as e:
        _fail(str(e).splitlines()[0])
        failures += 1
    return failures


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="BOS install healthcheck (keyless floor first).")
    ap.add_argument("--fix", action="store_true",
                    help="Install any missing document dependencies (same interpreter), then re-check.")
    args = ap.parse_args(argv)

    print("Business Operating System: install healthcheck")
    print()
    failures = 0

    # Python version
    py_ok = sys.version_info >= (3, 10)
    if py_ok:
        _ok(f"Python version: {sys.version.split()[0]}")
    else:
        _fail(f"Python version too old: {sys.version.split()[0]} (need 3.10+)")
        failures += 1
    print()

    # --fix: install the missing floor deps for the owner before checking.
    if args.fix:
        missing = _missing_floor_deps()
        if missing:
            still = _fix_missing(missing)
            if still:
                print(f"  [warn] {still} document dependency(ies) still missing after install.")
            print()
        else:
            print("Nothing to fix. The document tools are all present.")
            print()

    failures += check_floor()

    key = _configured_key()
    if key:
        failures += check_connected(key)
    else:
        print()
        print("Connected tier, TrustPager:")
        _ok("no CRM key configured, skipping (the keyless floor above is all you "
            "need to start). Connect TrustPager later to unlock the connected tier.")

    return _finish(failures, fixable=not args.fix)


def _finish(failures: int, *, fixable: bool) -> int:
    print()
    if failures == 0:
        print("All checks passed.")
        return 0
    print(f"{failures} check(s) failed. See above.")
    if fixable:
        print("Tip: many of these are missing document tools. Run "
              "`python tools/check-install.py --fix` to install them.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

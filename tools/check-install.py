#!/usr/bin/env python3
"""Verify the TrustPager skills install is healthy (doctor / healthcheck).

When to use:
- "Is my install working?"
- "Skill X is failing — is the problem auth, network, or the skill itself?"
- After running setup.py — confirm everything is connected.
- After regenerating your API key — confirm the new key works.

What it checks (7 probes, all required for skills to work):
- Python version >= 3.10
- TrustPager API key is configured
- Reachability of api.trustpager.com
- Catalog fetch from docs.trustpager.com
- Local catalog cache exists
- Cache directory is writable
- Authenticated read against /opportunities returns data

Output: green [OK] / orange [WARN] / red [FAIL] per check.
Exit code 0 if all checks pass; 1 if any fail.

Usage:
    python tools/check-install.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import (  # noqa: E402
    API_BASE, BOSError, CATALOG_CACHE_PATH, CATALOG_URL,
    get_api_key, get_catalog,
)


def _ok(msg: str) -> None:
    print(f"  [OK]   {msg}")


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def _warn(msg: str) -> None:
    print(f"  [WARN] {msg}")


def main() -> int:
    print("TrustPager — install healthcheck")
    print()
    failures = 0

    # Python version
    py_ok = sys.version_info >= (3, 10)
    if py_ok:
        _ok(f"Python version: {sys.version.split()[0]}")
    else:
        _fail(f"Python version too old: {sys.version.split()[0]} (need 3.10+)")
        failures += 1

    # API key
    print()
    print("Auth:")
    key = ""
    try:
        key = get_api_key()
        if key.startswith("tp_live_"):
            _ok(f"API key configured (ends ...{key[-4:]})")
        else:
            _warn(f"API key set but doesn't start with 'tp_live_' (got '{key[:10]}...')")
    except BOSError as e:
        _fail(str(e).splitlines()[0])
        failures += 1
        return _finish(failures)

    # API reach
    print()
    print("API reach:")
    try:
        import urllib.request
        req = urllib.request.Request(
            API_BASE + "/",
            headers={"Authorization": f"Bearer {key}"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            _ok(f"Reached {API_BASE}/ ({resp.status})")
    except Exception as e:  # noqa: BLE001
        msg = str(e).splitlines()[0]
        _fail(f"Could not reach {API_BASE}: {msg}")
        failures += 1

    # Catalog
    print()
    print("Catalog:")
    try:
        catalog = get_catalog()
        n_resources = len(catalog.get("resources", []))
        generated_at = catalog.get("generated_at", "?")
        _ok(f"Fetched from {CATALOG_URL} — {n_resources} resources, generated {generated_at}")
    except BOSError as e:
        _fail(str(e).splitlines()[0])
        failures += 1

    # Cache
    print()
    print("Cache:")
    if CATALOG_CACHE_PATH.exists():
        _ok(f"Cache exists at {CATALOG_CACHE_PATH}")
    else:
        _warn(f"No cache yet at {CATALOG_CACHE_PATH} (will be created on first run)")

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
    print()
    print("Authenticated read:")
    try:
        from trustpager_api import api_get
        r = api_get("opportunities", limit=1)
        n = len(r.get("data", []))
        _ok(f"GET /opportunities authenticated and responded ({n} row sample)")
    except BOSError as e:
        _fail(str(e).splitlines()[0])
        failures += 1

    return _finish(failures)


def _finish(failures: int) -> int:
    print()
    if failures == 0:
        print("All checks passed.")
        return 0
    print(f"{failures} check(s) failed. See above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

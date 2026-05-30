#!/usr/bin/env python3
"""Business Operating System — operator and skill-author CLI.

Subcommands:
    bos setup                       Interactive: prompt for API key, write ~/.claude/bos.json
    bos doctor                      Healthcheck: auth, catalog, cache, Python version
    bos catalog [resource]          Print catalog summary or per-resource detail
    bos inspect <resource> [method] [action] [--contains X]
                                    Print full schema (params, scopes, doc URL) for an endpoint
    bos lint <skill_dir>            Validate a skill's SKILL.md + fetch.py
    bos test <skill_name>           Run a skill's fetch.py against a fixture mock

This script is the entry point for everything except the slash commands. New
BOS installs should be able to run `bos setup` then `bos doctor` and either
get a clean bill of health or a clear list of what to fix.

Stdlib only. No `pip install` required. Tested on Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

# Resolve the shared lib regardless of where this script is invoked from.
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "skills" / "_shared"))

# These imports are deferred where possible so `bos setup` can run BEFORE
# the user has an API key configured.
from bos_lib import (  # noqa: E402
    API_BASE, BOSError, CATALOG_CACHE_PATH, CATALOG_URL, CONFIG_PATH,
    get_catalog, inspect_endpoint,
)


# =============================================================================
# bos setup — interactive auth bootstrap
# =============================================================================


def _find_key_in_mcp_config() -> str | None:
    """Look for an existing TrustPager API key in Claude Code's MCP config.

    Claude Code stores MCP connections in ~/.claude/.mcp.json (or similar).
    If the user has already run `claude mcp add trustpager`, the key is
    already on disk and we can offer to reuse it.
    """
    candidates = [
        Path.home() / ".claude" / ".mcp.json",
        Path.home() / ".claude" / "settings.json",
        Path.home() / ".claude.json",
    ]
    for path in candidates:
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        # Walk the structure looking for tp_live_* tokens
        found = _walk_for_key(data)
        if found:
            return found
    return None


def _walk_for_key(obj: Any) -> str | None:
    if isinstance(obj, str):
        if obj.startswith("tp_live_") and len(obj) > 20:
            return obj
        return None
    if isinstance(obj, dict):
        for v in obj.values():
            r = _walk_for_key(v)
            if r:
                return r
    if isinstance(obj, list):
        for v in obj:
            r = _walk_for_key(v)
            if r:
                return r
    return None


def cmd_setup(args: argparse.Namespace) -> int:
    print("Business Operating System — setup")
    print()
    print(f"This will write your TrustPager API key to: {CONFIG_PATH}")
    print()

    existing_key = None
    if CONFIG_PATH.exists() and not args.force:
        try:
            cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            existing_key = (cfg.get("api_key") or "").strip()
        except (json.JSONDecodeError, OSError):
            pass
        if existing_key:
            print(f"A key is already configured (ends ...{existing_key[-4:]}).")
            print("Re-run with --force to replace it, or skip setup entirely.")
            return 0

    # Try to detect from Claude Code's MCP config
    detected = _find_key_in_mcp_config()
    if detected:
        print(f"Detected an existing TrustPager API key in Claude Code config")
        print(f"  (ends ...{detected[-4:]}).")
        choice = input("Use this key for BOS too? [Y/n] ").strip().lower()
        if choice in ("", "y", "yes"):
            return _write_key(detected)

    print("Get your key from: https://app.trustpager.com/settings/api")
    print()
    key = input("Paste your tp_live_... key: ").strip()
    if not key:
        print("ERROR: empty key. Aborting.", file=sys.stderr)
        return 2
    if not key.startswith("tp_live_"):
        print(f"WARNING: key doesn't start with 'tp_live_'. Got '{key[:10]}...'", file=sys.stderr)
        confirm = input("Use it anyway? [y/N] ").strip().lower()
        if confirm not in ("y", "yes"):
            return 2
    return _write_key(key)


def _write_key(key: str) -> int:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps({"api_key": key}, indent=2), encoding="utf-8")
    print(f"Wrote {CONFIG_PATH}")
    print()
    print("Next: run `bos doctor` to verify everything works.")
    return 0


# =============================================================================
# bos doctor — healthcheck across every assumption a skill makes
# =============================================================================


def _ok(msg: str) -> None:
    print(f"  [OK]   {msg}")


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def _warn(msg: str) -> None:
    print(f"  [WARN] {msg}")


def cmd_doctor(args: argparse.Namespace) -> int:
    print("Business Operating System — doctor")
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
    try:
        from bos_lib import get_api_key
        key = get_api_key()
        if key.startswith("tp_live_"):
            _ok(f"API key configured (ends ...{key[-4:]})")
        else:
            _warn(f"API key set but doesn't start with 'tp_live_' (got '{key[:10]}...')")
    except BOSError as e:
        _fail(str(e).splitlines()[0])
        failures += 1
        return _doctor_finish(failures)

    # API reach — call the welcome endpoint at base URL (no auth needed to confirm hostname)
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

    # Cache dir
    print()
    print("Cache:")
    if CATALOG_CACHE_PATH.exists():
        _ok(f"Cache exists at {CATALOG_CACHE_PATH}")
    else:
        _warn(f"No cache yet at {CATALOG_CACHE_PATH} (will be created on first run)")

    # Try a write to the cache dir
    try:
        CATALOG_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        probe = CATALOG_CACHE_PATH.parent / ".write-probe"
        probe.write_text("x", encoding="utf-8")
        probe.unlink()
        _ok(f"Cache directory writable: {CATALOG_CACHE_PATH.parent}")
    except OSError as e:
        _fail(f"Cache directory not writable: {e}")
        failures += 1

    # Authenticated read — try a free endpoint
    print()
    print("Authenticated read:")
    try:
        from bos_lib import api_get
        r = api_get("opportunities", limit=1)
        n = len(r.get("data", []))
        _ok(f"GET /opportunities authenticated and responded ({n} row sample)")
    except BOSError as e:
        _fail(str(e).splitlines()[0])
        failures += 1

    return _doctor_finish(failures)


def _doctor_finish(failures: int) -> int:
    print()
    if failures == 0:
        print("All checks passed.")
        return 0
    print(f"{failures} check(s) failed. See above.")
    return 1


# =============================================================================
# bos catalog [resource] — print the catalog
# =============================================================================


def cmd_catalog(args: argparse.Namespace) -> int:
    try:
        catalog = get_catalog()
    except BOSError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if args.resource_id:
        resource = next((r for r in catalog["resources"]
                         if r["id"] == args.resource_id), None)
        if not resource:
            print(f"Resource not found: {args.resource_id}", file=sys.stderr)
            print(f"Available: {', '.join(r['id'] for r in catalog['resources'][:20])}...",
                  file=sys.stderr)
            return 1
        print(f"=== {resource['id']}  —  {resource['label']} ===")
        print(f"Doc: {resource.get('doc_url', '(none)')}")
        print(f"Description: {resource.get('description', '(none)')}")
        print()
        print(f"Endpoints ({len(resource['endpoints'])}):")
        for ep in resource["endpoints"]:
            mark = "W" if ep.get("is_write") else "R"
            scopes = " ".join(ep.get("scopes", []))
            print(f"  [{mark}] {ep['method']:6s} {ep['path']:50s}  scopes={scopes}")
        return 0

    # No resource — print summary
    print(f"Catalog from: {CATALOG_URL}")
    print(f"Generated:    {catalog.get('generated_at', '?')}")
    print(f"Base URL:     {catalog.get('base_url', '?')}")
    print(f"Auth:         {catalog.get('auth', {}).get('format', '?')}")
    print()
    print(f"{len(catalog['resources'])} resources:")
    for r in catalog["resources"]:
        n = len(r.get("endpoints", []))
        print(f"  {r['id']:30s} {n:3d} endpoints  {r.get('label', '')}")
    print()
    print("For details on one resource: bos catalog <resource_id>")
    return 0


# =============================================================================
# bos inspect <resource> [method] [action] — full endpoint schema
# =============================================================================


def cmd_inspect(args: argparse.Namespace) -> int:
    try:
        info = inspect_endpoint(
            args.resource_id, method=args.method, action=args.action,
            path_contains=args.path_contains,
        )
    except BOSError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"=== {info['method']} {info['path']} ===")
    print(f"Resource:    {info['resource_id']} — {info.get('resource_label', '')}")
    print(f"Write:       {'yes' if info['is_write'] else 'no'}")
    print(f"Scopes:      {' '.join(info['scopes']) if info['scopes'] else '(none)'}")
    print(f"Doc:         {info['doc_url']}")
    print()
    print(f"Description: {info['description']}")
    print()
    if info["params"]:
        print(f"Parameters ({len(info['params'])}):")
        for p in info["params"]:
            req = "required" if p.get("required") else "optional"
            print(f"  - {p.get('name', '?'):20s} {p.get('in', '?'):6s} {p.get('type', '?'):8s} {req}")
            desc = p.get("description", "")
            if desc:
                print(f"      {desc}")
    else:
        print("Parameters: (none)")
    return 0


# =============================================================================
# bos lint <skill_dir> — validate a skill's SKILL.md + fetch.py
# =============================================================================


REQUIRED_FRONTMATTER = {"name", "description", "triggers"}


def _parse_simple_frontmatter(text: str) -> dict[str, Any] | None:
    """Minimal YAML-frontmatter parser.

    We don't need a full YAML lib — just `---\\nkey: value\\n---\\n` with
    optional list values declared as bulleted lines. Returns None if the
    file doesn't start with frontmatter.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    block = text[4:end]
    out: dict[str, Any] = {}
    current_list_key: str | None = None
    for line in block.splitlines():
        if not line.strip():
            current_list_key = None
            continue
        if line.startswith("  - "):
            if current_list_key:
                out.setdefault(current_list_key, []).append(line[4:].strip())
            continue
        if ": " in line:
            k, v = line.split(": ", 1)
            k = k.strip()
            v = v.strip()
            if v:
                out[k] = v
                current_list_key = None
            else:
                # Empty value — could be the start of a list
                current_list_key = k
        elif line.endswith(":"):
            current_list_key = line[:-1].strip()
    return out


def cmd_lint(args: argparse.Namespace) -> int:
    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.is_dir():
        print(f"ERROR: not a directory: {skill_dir}", file=sys.stderr)
        return 2

    issues: list[tuple[str, str]] = []  # (severity, message)

    # Check SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        issues.append(("FAIL", f"missing {skill_md.name}"))
    else:
        text = skill_md.read_text(encoding="utf-8")
        fm = _parse_simple_frontmatter(text)
        if not fm:
            issues.append(("FAIL", "SKILL.md missing YAML frontmatter (--- ... ---)"))
        else:
            missing = REQUIRED_FRONTMATTER - set(fm)
            for k in missing:
                issues.append(("FAIL", f"SKILL.md frontmatter missing required field: {k}"))
            triggers = fm.get("triggers")
            if isinstance(triggers, list) and len(triggers) < 3:
                issues.append(("WARN", f"SKILL.md has only {len(triggers)} trigger phrases; aim for 5+"))

    # Check fetch.py if present
    fetch_py = skill_dir / "fetch.py"
    if fetch_py.exists():
        py_text = fetch_py.read_text(encoding="utf-8")
        if "from bos_lib import" not in py_text and "import bos_lib" not in py_text:
            issues.append(("WARN", "fetch.py doesn't import from bos_lib — likely missing shared helpers"))
        # Look for hardcoded API keys
        if re.search(r"tp_live_[A-Za-z0-9_]{20,}", py_text):
            issues.append(("FAIL", "fetch.py contains what looks like a hardcoded tp_live_* API key"))
        # Look for hardcoded base URL
        if "supabase.co" in py_text:
            issues.append(("WARN", "fetch.py references supabase.co directly — should use API_BASE from bos_lib"))
        # Look for hardcoded paths instead of resolve_path
        if "api_get(" in py_text and "resolve_path(" not in py_text:
            issues.append(("WARN", "fetch.py calls api_get() but doesn't use resolve_path() — paths may drift if the API renames endpoints"))

    # Report
    print(f"Linting {skill_dir.name}/...")
    if not issues:
        print("  OK — no issues found.")
        return 0
    for severity, msg in issues:
        marker = "[FAIL]" if severity == "FAIL" else "[WARN]"
        print(f"  {marker} {msg}")
    failures = sum(1 for s, _ in issues if s == "FAIL")
    return 2 if failures else 1


# =============================================================================
# bos test <skill_name> — run a skill's fetch.py against a fixture
# =============================================================================


def cmd_test(args: argparse.Namespace) -> int:
    skill_dir = REPO_ROOT / "skills" / args.skill_name
    fetch_py = skill_dir / "fetch.py"
    if not fetch_py.exists():
        print(f"ERROR: no fetch.py for skill '{args.skill_name}' at {fetch_py}", file=sys.stderr)
        return 2

    fixture_path = Path(args.fixture) if args.fixture else (skill_dir / "test-fixture.json")
    if not fixture_path.exists():
        print(f"ERROR: fixture not found: {fixture_path}", file=sys.stderr)
        print(f"Create one with this shape:", file=sys.stderr)
        print(json.dumps({
            "catalog": {"_use_live": True},
            "responses": {
                "opportunities": {"data": [{"id": "fake-1", "name": "Test deal", "status": "open"}]},
                "tasks": {"data": []},
            },
        }, indent=2), file=sys.stderr)
        return 2

    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    print(f"Testing {args.skill_name} against fixture {fixture_path.name}")
    print()

    # Monkey-patch bos_lib to return fixture responses
    import bos_lib

    real_api_get = bos_lib.api_get
    real_get_catalog = bos_lib.get_catalog

    def mock_api_get(path: str, **params: Any) -> dict[str, Any]:
        # Look up by exact path first, then by prefix
        responses = fixture.get("responses", {})
        if path in responses:
            return responses[path]
        for key, val in responses.items():
            if path.startswith(key):
                return val
        return {"data": [], "pagination": {"has_more": False}}

    def mock_get_catalog(force_refresh: bool = False) -> dict[str, Any]:
        cat = fixture.get("catalog", {})
        if cat.get("_use_live"):
            return real_get_catalog(force_refresh=force_refresh)
        return cat

    bos_lib.api_get = mock_api_get  # type: ignore[assignment]
    bos_lib.get_catalog = mock_get_catalog  # type: ignore[assignment]

    try:
        # Load and execute the fetch script as a module
        import importlib.util
        spec = importlib.util.spec_from_file_location("skill_fetch", fetch_py)
        if not spec or not spec.loader:
            print("ERROR: could not load fetch.py", file=sys.stderr)
            return 2
        mod = importlib.util.module_from_spec(spec)
        # Patch the bos_lib symbols the script imported BEFORE execution
        spec.loader.exec_module(mod)

        # Re-patch on the module's namespace too (Python caches imported names)
        if hasattr(mod, "api_get"):
            mod.api_get = mock_api_get
        if hasattr(mod, "get_catalog"):
            mod.get_catalog = mock_get_catalog

        # Run with sys.argv adjusted
        sys.argv = ["fetch.py", "--json-only"]
        if hasattr(mod, "main"):
            mod.main()
            print()
            print("OK — fetch.py ran without raising.")
            return 0
        print("ERROR: fetch.py has no main() function", file=sys.stderr)
        return 2
    except SystemExit as e:
        # main() called sys.exit() — check the code
        code = e.code if isinstance(e.code, int) else 1
        if code == 0:
            print()
            print("OK — fetch.py exited cleanly.")
            return 0
        print()
        print(f"FAIL — fetch.py exited with code {code}.")
        return code
    except Exception as e:  # noqa: BLE001
        print()
        print(f"FAIL — fetch.py raised: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        bos_lib.api_get = real_api_get
        bos_lib.get_catalog = real_get_catalog


# =============================================================================
# CLI dispatcher
# =============================================================================


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bos",
        description="Business Operating System — operator and skill-author CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_setup = sub.add_parser("setup", help="Interactive auth bootstrap")
    p_setup.add_argument("--force", action="store_true",
                         help="Overwrite an existing key without prompting")
    p_setup.set_defaults(func=cmd_setup)

    p_doctor = sub.add_parser("doctor", help="Healthcheck")
    p_doctor.set_defaults(func=cmd_doctor)

    p_catalog = sub.add_parser("catalog", help="Print catalog summary or one resource's detail")
    p_catalog.add_argument("resource_id", nargs="?", default=None,
                           help="Optional: a specific resource id to drill into")
    p_catalog.set_defaults(func=cmd_catalog)

    p_inspect = sub.add_parser("inspect", help="Print the full schema of one endpoint")
    p_inspect.add_argument("resource_id")
    p_inspect.add_argument("--method", default="GET")
    p_inspect.add_argument("--action", default="list",
                           choices=["list", "get", "create", "search"])
    p_inspect.add_argument("--path-contains", default=None,
                           help="Substring to disambiguate when a resource has multiple matches")
    p_inspect.set_defaults(func=cmd_inspect)

    p_lint = sub.add_parser("lint", help="Validate a skill's SKILL.md + fetch.py")
    p_lint.add_argument("skill_dir", help="Path to a skill directory (e.g. skills/sweep-my-day)")
    p_lint.set_defaults(func=cmd_lint)

    p_test = sub.add_parser("test", help="Run a skill's fetch.py against a JSON fixture")
    p_test.add_argument("skill_name", help="Name of the skill under skills/ (e.g. sweep-my-day)")
    p_test.add_argument("--fixture", default=None,
                        help="Path to fixture JSON (default: skills/<name>/test-fixture.json)")
    p_test.set_defaults(func=cmd_test)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

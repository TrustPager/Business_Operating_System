#!/usr/bin/env python3
"""Run a skill's fetch.py against a mock fixture (offline, no API calls).

When to use:
- Iterating on a skill — fast feedback without burning credits.
- Verifying a skill still works after refactoring trustpager_api.
- Running in CI — no API key needed.
- Demonstrating a skill's output shape to someone without a TrustPager workspace.

What it does:
- Loads skills/<name>/test-fixture.json (or a custom path with --fixture).
- Monkey-patches trustpager_api.api_get to return the fixture responses.
- Monkey-patches trustpager_api.get_catalog to use the fixture catalog
  (or the live catalog if the fixture sets {"_use_live": true}).
- Imports and runs the skill's fetch.py main(), capturing exit code.
- Prints OK/FAIL based on whether main() raised.

Fixture shape:
    {
      "catalog": {"_use_live": true},
      "responses": {
        "opportunities": {"data": [{"id": "...", "name": "..."}]},
        "tasks":         {"data": []}
      }
    }

Usage:
    python tools/test-skill.py sweep-my-day
    python tools/test-skill.py my-skill --fixture path/to/other-fixture.json

Related:
    python tools/lint-skill.py skills/<name>     # static validation
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("skill_name", help="Name of the skill under skills/ (e.g. sweep-my-day)")
    parser.add_argument("--fixture", default=None,
                        help="Path to fixture JSON (default: skills/<name>/test-fixture.json)")
    args = parser.parse_args()

    skill_dir = REPO_ROOT / "skills" / args.skill_name
    fetch_py = skill_dir / "fetch.py"
    if not fetch_py.exists():
        print(f"ERROR: no fetch.py for skill '{args.skill_name}' at {fetch_py}",
              file=sys.stderr)
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

    import trustpager_api

    real_api_get = trustpager_api.api_get
    real_get_catalog = trustpager_api.get_catalog

    def mock_api_get(path: str, **params: Any) -> dict[str, Any]:
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

    trustpager_api.api_get = mock_api_get  # type: ignore[assignment]
    trustpager_api.get_catalog = mock_get_catalog  # type: ignore[assignment]

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("skill_fetch", fetch_py)
        if not spec or not spec.loader:
            print("ERROR: could not load fetch.py", file=sys.stderr)
            return 2
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        if hasattr(mod, "api_get"):
            mod.api_get = mock_api_get
        if hasattr(mod, "get_catalog"):
            mod.get_catalog = mock_get_catalog

        sys.argv = ["fetch.py", "--json-only"]
        if hasattr(mod, "main"):
            mod.main()
            print()
            print("OK — fetch.py ran without raising.")
            return 0
        print("ERROR: fetch.py has no main() function", file=sys.stderr)
        return 2
    except SystemExit as e:
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
        trustpager_api.api_get = real_api_get
        trustpager_api.get_catalog = real_get_catalog


if __name__ == "__main__":
    sys.exit(main())

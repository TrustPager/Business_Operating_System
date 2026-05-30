#!/usr/bin/env python3
"""Set up TrustPager API access for Claude Code skills (first-run wizard).

When to use:
- Right after cloning this repo. This is the first thing a customer runs.
- After regenerating your TrustPager API key.
- After running config.py --clear to wipe an old key.

What it does:
- Looks for an existing tp_live_* key in Claude Code's MCP config
  (~/.claude/.mcp.json or ~/.claude/settings.json or ~/.claude.json).
- If found, offers to reuse it (no copy-paste needed).
- Otherwise, prompts you to paste your tp_live_... key.
- Writes the key to ~/.claude/bos.json so every skill can find it.

Usage:
    python tools/setup.py
    python tools/setup.py --force        # overwrite an existing key

Next step after this runs: python tools/check-install.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import CONFIG_PATH  # noqa: E402


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


def _find_key_in_mcp_config() -> str | None:
    """Look for an existing TrustPager API key in Claude Code's MCP config."""
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
        found = _walk_for_key(data)
        if found:
            return found
    return None


def _write_key(key: str) -> int:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps({"api_key": key}, indent=2), encoding="utf-8")
    print(f"Wrote {CONFIG_PATH}")
    print()
    print("Next: run `python tools/check-install.py` to verify everything works.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--force", action="store_true",
                        help="Overwrite an existing key without prompting")
    args = parser.parse_args()

    print("TrustPager — first-run setup for Claude Code skills")
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

    detected = _find_key_in_mcp_config()
    if detected:
        print(f"Detected an existing TrustPager API key in Claude Code config")
        print(f"  (ends ...{detected[-4:]}).")
        choice = input("Use this key for skill scripts too? [Y/n] ").strip().lower()
        if choice in ("", "y", "yes"):
            return _write_key(detected)

    print("Get your key from: https://app.trustpager.com/settings/api")
    print()
    key = input("Paste your tp_live_... key: ").strip()
    if not key:
        print("ERROR: empty key. Aborting.", file=sys.stderr)
        return 2
    if not key.startswith("tp_live_"):
        print(f"WARNING: key doesn't start with 'tp_live_'. Got '{key[:10]}...'",
              file=sys.stderr)
        confirm = input("Use it anyway? [y/N] ").strip().lower()
        if confirm not in ("y", "yes"):
            return 2
    return _write_key(key)


if __name__ == "__main__":
    sys.exit(main())

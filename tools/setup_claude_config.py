#!/usr/bin/env python3
"""setup_claude_config.py - additive, defensive helper to merge BOS settings into ~/.claude/.

Subcommands:

  merge-settings   Additively merge permissions from a JSON source into
                   ~/.claude/settings.json. Never removes user entries. Refuses
                   to touch the file if it is already present but invalid JSON.

  merge-claude-md  Insert or replace a delimited BOS block in ~/.claude/CLAUDE.md.
                   Never touches content outside the delimited block. Refuses if
                   the markers are unbalanced or the file cannot be decoded as UTF-8.

Usage:
  python tools/setup_claude_config.py [--home <dir>] merge-settings [--from <path>]
  python tools/setup_claude_config.py [--home <dir>] merge-claude-md [--from <path>]

The --home option (default: your real home directory) lets tests point at a
temporary directory without touching any real config.

Invoked through the signpost:
  python ~/.claude/bos-run.py tool setup_claude_config merge-settings
  python ~/.claude/bos-run.py tool setup_claude_config merge-claude-md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Block markers for CLAUDE.md
# ---------------------------------------------------------------------------

_BLOCK_START = "<!-- bos:best-practices:start -->"
_BLOCK_END = "<!-- bos:best-practices:end -->"

# ---------------------------------------------------------------------------
# Default source paths (resolved relative to this file's location, i.e. BOS_HOME)
# ---------------------------------------------------------------------------

_BOS_HOME = Path(__file__).resolve().parent.parent
_DEFAULT_SETTINGS_SRC = _BOS_HOME / "settings" / "recommended-settings.json"
_DEFAULT_MD_SRC = _BOS_HOME / "settings" / "recommended-global-claude.md"


# ---------------------------------------------------------------------------
# merge-settings
# ---------------------------------------------------------------------------

def _merge_settings(home: Path, from_path: Path) -> int:
    """Additively merge permissions from from_path into <home>/.claude/settings.json."""
    claude_dir = home / ".claude"
    settings_path = claude_dir / "settings.json"

    # Read the source file
    try:
        src_text = from_path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"[error] Cannot read source file: {from_path}", file=sys.stderr)
        print(f"        {e}", file=sys.stderr)
        return 1

    try:
        src_data = json.loads(src_text)
    except json.JSONDecodeError as e:
        print(f"[error] Source file is not valid JSON: {from_path}", file=sys.stderr)
        print(f"        {e}", file=sys.stderr)
        return 1

    src_perms = src_data.get("permissions", {})
    src_allow: list[str] = src_perms.get("allow", [])
    src_deny: list[str] = src_perms.get("deny", [])

    # Read or create the target settings.json
    existing: dict = {}
    if settings_path.exists():
        try:
            raw = settings_path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"[error] Cannot read {settings_path}", file=sys.stderr)
            print(f"        {e}", file=sys.stderr)
            return 1

        try:
            existing = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"[error] {settings_path} exists but is not valid JSON.", file=sys.stderr)
            print(f"        {e}", file=sys.stderr)
            print(f"        Fix or remove the file manually, then re-run.", file=sys.stderr)
            return 1

    # Merge permissions: union, de-duplicated, order-stable (existing first, then new)
    perms = existing.setdefault("permissions", {})

    existing_allow: list[str] = perms.get("allow", [])
    existing_deny: list[str] = perms.get("deny", [])

    seen_allow: set[str] = set(existing_allow)
    merged_allow = list(existing_allow)
    for entry in src_allow:
        if entry not in seen_allow:
            merged_allow.append(entry)
            seen_allow.add(entry)

    seen_deny: set[str] = set(existing_deny)
    merged_deny = list(existing_deny)
    for entry in src_deny:
        if entry not in seen_deny:
            merged_deny.append(entry)
            seen_deny.add(entry)

    if src_allow or existing_allow:
        perms["allow"] = merged_allow
    if src_deny or existing_deny:
        perms["deny"] = merged_deny

    # Write back
    claude_dir.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    print(f"[ok] Merged permissions into {settings_path}")
    return 0


# ---------------------------------------------------------------------------
# merge-claude-md
# ---------------------------------------------------------------------------

def _merge_claude_md(home: Path, from_path: Path) -> int:
    """Insert or replace the BOS block in <home>/.claude/CLAUDE.md."""
    claude_dir = home / ".claude"
    md_path = claude_dir / "CLAUDE.md"

    # Read the block content from the source file
    try:
        block_content = from_path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"[error] Cannot read source file: {from_path}", file=sys.stderr)
        print(f"        {e}", file=sys.stderr)
        return 1

    # Build the block to insert
    block = f"{_BLOCK_START}\n{block_content}{_BLOCK_END}"

    # If CLAUDE.md does not exist, create it with just the block
    if not md_path.exists():
        claude_dir.mkdir(parents=True, exist_ok=True)
        md_path.write_text(block + "\n", encoding="utf-8")
        print(f"[ok] Created {md_path} with BOS best-practices block.")
        return 0

    # Read the existing file
    try:
        existing_bytes = md_path.read_bytes()
    except OSError as e:
        print(f"[error] Cannot read {md_path}", file=sys.stderr)
        print(f"        {e}", file=sys.stderr)
        return 1

    try:
        existing = existing_bytes.decode("utf-8")
    except UnicodeDecodeError as e:
        print(f"[error] {md_path} is not valid UTF-8.", file=sys.stderr)
        print(f"        {e}", file=sys.stderr)
        print(f"        Fix encoding manually, then re-run.", file=sys.stderr)
        return 1

    # Count markers
    n_start = existing.count(_BLOCK_START)
    n_end = existing.count(_BLOCK_END)

    if n_start == 0 and n_end == 0:
        # No markers: append the block with a blank-line separator
        separator = "\n" if existing.endswith("\n") else "\n\n"
        new_content = existing + separator + block + "\n"
        md_path.write_text(new_content, encoding="utf-8")
        print(f"[ok] Appended BOS best-practices block to {md_path}")
        return 0

    if n_start == 1 and n_end == 1:
        # Validate ordering: start must come before end
        start_idx = existing.index(_BLOCK_START)
        end_idx = existing.index(_BLOCK_END)
        if start_idx >= end_idx:
            print(f"[error] {md_path} has an end marker before its start marker.", file=sys.stderr)
            print(f"        Remove or fix the markers manually, then re-run.", file=sys.stderr)
            return 1

        # Replace the content between (and including) the markers
        before = existing[:start_idx]
        after = existing[end_idx + len(_BLOCK_END):]
        new_content = before + block + after
        md_path.write_text(new_content, encoding="utf-8")
        print(f"[ok] Replaced BOS best-practices block in {md_path}")
        return 0

    # Anything else: unbalanced markers - refuse
    print(f"[error] {md_path} has unbalanced BOS markers "
          f"({n_start} start, {n_end} end).", file=sys.stderr)
    print(f"        Remove or fix the markers manually, then re-run.", file=sys.stderr)
    return 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Merge BOS settings and CLAUDE.md block into ~/.claude/ additively."
    )
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help="Home directory (default: real home). Use a temp path for testing.",
    )

    sub = parser.add_subparsers(dest="cmd")

    # merge-settings subcommand
    p_settings = sub.add_parser(
        "merge-settings",
        help="Additively merge permissions into ~/.claude/settings.json.",
    )
    p_settings.add_argument(
        "--from",
        dest="from_path",
        type=Path,
        default=_DEFAULT_SETTINGS_SRC,
        help="Source JSON file with a 'permissions' object (allow/deny lists).",
    )

    # merge-claude-md subcommand
    p_md = sub.add_parser(
        "merge-claude-md",
        help="Insert or replace the BOS block in ~/.claude/CLAUDE.md.",
    )
    p_md.add_argument(
        "--from",
        dest="from_path",
        type=Path,
        default=_DEFAULT_MD_SRC,
        help="Source markdown file whose contents become the BOS-managed block body.",
    )

    args = parser.parse_args(argv)

    if args.cmd == "merge-settings":
        return _merge_settings(args.home, args.from_path)
    if args.cmd == "merge-claude-md":
        return _merge_claude_md(args.home, args.from_path)

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

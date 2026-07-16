#!/usr/bin/env python3
"""CWD-independent launcher for skill data-fetchers and keyless tools.

Why this exists:
    Skills tell Claude to run a fetcher. Hardcoding `python skills/<name>/fetch.py`
    assumes the current working directory IS the BOS clone root -- which is false
    whenever Claude is running in the operator's own project folder, or when BOS
    is installed as a plugin (skills registered from ~/.claude/plugins/... while
    the Python lives in a separate clone). This launcher removes that assumption.

How it stays location-independent:
    This file lives at <BOS_HOME>/tools/run.py, so it locates BOS_HOME from its
    OWN path (`__file__`) -- never from the working directory. The fixed-location
    shim at ~/.claude/bos-run.py (written by tools/setup.py) is what bootstraps
    here from anywhere, so skills can always call:

        python ~/.claude/bos-run.py <skill-name> [args...]
        python ~/.claude/bos-run.py tool <toolname> [args...]

Usage (direct):
    python tools/run.py <skill-name> [args...]      # e.g. sweep-my-day
    python tools/run.py --list                      # show runnable skills
    python tools/run.py tool <toolname> [args...]   # e.g. tool finance_calc pmt --rate 0.01

Signpost form (from any directory):
    python ~/.claude/bos-run.py <skill-name> [args...]
    python ~/.claude/bos-run.py tool <toolname> [args...]

Extra args after <skill-name> or <toolname> are forwarded verbatim to the
skill's fetch.py or tool script.
(e.g. `draft-reply --hours 48`, `tool finance_calc pmt --rate 0.01 --nper 12 --pv 10000`)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

BOS_HOME = Path(__file__).resolve().parent.parent
SKILLS_DIR = BOS_HOME / "skills"
TOOLS_DIR = BOS_HOME / "tools"

# The tools a skill may invoke through the signpost `tool` mode. An allowlist
# (defence in depth): every file in tools/ is BOS's own code, but the launcher
# must only run the data/helper tools skills actually call, never the admin
# scripts (config.py can clear the key, setup.py re-runs the installer, run.py
# would recurse). To add a new signpost-invoked tool, add its bare name here.
# The test suite asserts every tool a skill invokes is listed here, so this set
# cannot silently drift out of sync.
_ALLOWED_TOOLS: frozenset[str] = frozenset({
    "audit-contacts",
    "audit-pipeline",
    "channel_breakdown",
    "check-install",
    "dump-crm-bundle",
    "finance_calc",
    "find-gaps",
    "lint-sequence",
    "markitdown_convert",
    "setup_claude_config",
    "sync-brand",
    "write_docx",
    "write_xlsx",
})


def _runnable() -> list[str]:
    if not SKILLS_DIR.is_dir():
        return []
    return sorted(d.name for d in SKILLS_DIR.iterdir() if (d / "fetch.py").is_file())


def _unsafe_toolname(toolname: str) -> bool:
    """Return True if the tool name contains path-traversal characters."""
    if "/" in toolname or "\\" in toolname or ".." in toolname:
        return True
    p = Path(toolname)
    if p.is_absolute():
        return True
    return False


def _dispatch_tool(argv: list[str]) -> int:
    """Handle the 'tool' subcommand: run a script from tools/ by name."""
    if not argv:
        print("[err] 'tool' requires a tool name.", file=sys.stderr)
        print("      usage: python tools/run.py tool <toolname> [args...]", file=sys.stderr)
        return 2

    toolname = argv[0]

    if _unsafe_toolname(toolname):
        print(f"[err] unsafe tool name '{toolname}': must be a bare filename with no path separators or '..'.",
              file=sys.stderr)
        return 2

    stem = toolname[:-3] if toolname.endswith(".py") else toolname
    if stem not in _ALLOWED_TOOLS:
        print(f"[err] '{stem}' is not a runnable BOS tool.", file=sys.stderr)
        print(f"      allowed: {', '.join(sorted(_ALLOWED_TOOLS))}", file=sys.stderr)
        return 2

    tool_file = TOOLS_DIR / (toolname if toolname.endswith(".py") else toolname + ".py")

    if not tool_file.is_file():
        print(f"[err] tool '{toolname}' not found.", file=sys.stderr)
        print(f"      looked in: {tool_file}", file=sys.stderr)
        return 2

    # Run in a child process and pass its exit code straight back.
    # subprocess (not os.execv) because execv on Windows mangles argv entries
    # that contain spaces -- same reasoning as the skill path above.
    proc = subprocess.run([sys.executable, str(tool_file), *argv[1:]])
    return proc.returncode


def _dispatch_journal_write(argv: list[str]) -> int:
    """Handle the 'journal-write' subcommand: append one write to the audit trail.

    A claude_mcp driver (e.g. meta-ads) has no Python transport, so its writes do
    not auto-journal through the kernel the way keyed-REST writes do. This branch
    lets the run-my-ads body record each confirmed create/update explicitly, so the
    Meta Ads write surface keeps the same append-only audit trail CRM writes land in
    (spec §8 Layer 2).

    This is NOT an _ALLOWED_TOOLS entry: it dispatches no file in tools/ (there is
    no tools/journal-write.py). It imports kernel.runtime.journal.record_write and
    calls it directly. --body is parsed as a JSON object.

    Usage:
        python tools/run.py journal-write \\
          --method mcp__meta-ads__ads_create_campaign \\
          --path meta-ads/act_<id>/campaigns \\
          --status ok --result-id <returned id> \\
          --body '{"objective":"...","status":"PAUSED"}'
    """
    parser = argparse.ArgumentParser(
        prog="run.py journal-write",
        description="Append one write to the append-only BOS audit trail.",
    )
    parser.add_argument("--method", required=True,
                        help="The write method (e.g. the mcp__meta-ads__* tool name).")
    parser.add_argument("--path", required=True,
                        help="A path/scope for the write (e.g. meta-ads/act_<id>/campaigns).")
    parser.add_argument("--status", default="ok",
                        help="Outcome status: ok | error | approval_pending (default: ok).")
    parser.add_argument("--result-id", dest="result_id", default=None,
                        help="The id the write returned (e.g. the created campaign id).")
    parser.add_argument("--body", default=None,
                        help="The write body as a JSON object string; summarised and redacted.")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse exits 2 on a usage error; pass it back
        return int(exc.code) if exc.code is not None else 2

    body: dict | None = None
    if args.body is not None:
        try:
            parsed = json.loads(args.body)
        except json.JSONDecodeError as exc:
            print(f"[err] --body must be valid JSON: {exc}", file=sys.stderr)
            return 2
        if not isinstance(parsed, dict):
            print("[err] --body must be a JSON object (e.g. '{\"status\":\"PAUSED\"}').",
                  file=sys.stderr)
            return 2
        body = parsed

    # Imported here (not at module top) so --list / tool dispatch never pay the
    # kernel import cost, and so a broken kernel path fails only this subcommand.
    # The kernel package is rooted at BOS_HOME, so put that on sys.path first —
    # run.py may be invoked from any working directory (see module docstring).
    if str(BOS_HOME) not in sys.path:
        sys.path.insert(0, str(BOS_HOME))
    try:
        from kernel.runtime.journal import record_write
    except ImportError as exc:
        print(f"[err] cannot import the journal ({exc}).", file=sys.stderr)
        print(f"      looked from: {BOS_HOME}", file=sys.stderr)
        return 2

    record_write(
        args.method,
        args.path,
        body,
        status=args.status,
        result_id=args.result_id,
    )
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    if argv[0] == "--list":
        names = _runnable()
        print("\n".join(names) if names else "(no skills with a fetch.py found)")
        return 0

    if argv[0] == "tool":
        return _dispatch_tool(argv[1:])

    if argv[0] == "journal-write":
        return _dispatch_journal_write(argv[1:])

    name = argv[0]
    fetch = SKILLS_DIR / name / "fetch.py"
    if not fetch.is_file():
        print(f"[err] no fetcher for skill '{name}'.", file=sys.stderr)
        print(f"      looked in: {fetch}", file=sys.stderr)
        runnable = _runnable()
        if runnable:
            print(f"      runnable skills: {', '.join(runnable)}", file=sys.stderr)
        return 2

    # Run the fetcher in a child process and pass its exit code straight back.
    # subprocess (not os.execv) because execv on Windows mangles argv entries
    # that contain spaces (e.g. an install path like "...\Final Piece\..."),
    # splitting the path at the space. The fetcher self-locates the shared lib
    # via its own __file__, so the child's working directory is irrelevant.
    proc = subprocess.run([sys.executable, str(fetch), *argv[1:]])
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""CWD-independent launcher for skill data-fetchers.

Why this exists:
    Skills tell Claude to run a fetcher. Hardcoding `python skills/<name>/fetch.py`
    assumes the current working directory IS the BOS clone root — which is false
    whenever Claude is running in the operator's own project folder, or when BOS
    is installed as a plugin (skills registered from ~/.claude/plugins/... while
    the Python lives in a separate clone). This launcher removes that assumption.

How it stays location-independent:
    This file lives at <BOS_HOME>/tools/run.py, so it locates BOS_HOME from its
    OWN path (`__file__`) — never from the working directory. The fixed-location
    shim at ~/.claude/bos-run.py (written by tools/setup.py) is what bootstraps
    here from anywhere, so skills can always call:

        python ~/.claude/bos-run.py <skill-name> [args...]

Usage (direct):
    python tools/run.py <skill-name> [args...]      # e.g. sweep-my-day
    python tools/run.py --list                      # show runnable skills

Extra args after <skill-name> are forwarded verbatim to the skill's fetch.py
(e.g. `draft-reply --hours 48`, `why-didnt-it-fire "<id>"`).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BOS_HOME = Path(__file__).resolve().parent.parent
SKILLS_DIR = BOS_HOME / "skills"


def _runnable() -> list[str]:
    if not SKILLS_DIR.is_dir():
        return []
    return sorted(d.name for d in SKILLS_DIR.iterdir() if (d / "fetch.py").is_file())


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    if argv[0] == "--list":
        names = _runnable()
        print("\n".join(names) if names else "(no skills with a fetch.py found)")
        return 0

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

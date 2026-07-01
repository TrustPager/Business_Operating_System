#!/usr/bin/env python3
"""Stage the CURRENT working tree into a throwaway profile for dogfooding.

Why: the feature branch is our staging environment. Before merging anything to
main, we want to use it as a brand-new owner would, without touching our real
~/.claude or polluting the repo. This installs the branch's BOS into an isolated
home directory and prints the one command to launch a clean-slate Claude Code
session against it. Delete the throwaway dir when done.

It runs the real tools/setup.py (so the dogfood matches a real install: skills +
commands discoverable, launcher shim, keyless path) but with the home directory
redirected to a throwaway location, the key prompt auto-skipped, and the heavy
document-stack pip skipped (pass --with-deps to include it).

Usage:
    python tools/dogfood.py                 # stage into <repo>/.dogfood
    python tools/dogfood.py --home DIR      # stage into a chosen dir
    python tools/dogfood.py --with-deps     # also install the document stack
    python tools/dogfood.py --reset         # delete the throwaway dir and exit

Notes:
- Connected steps (firecrawl web research, Gmail/Calendar) still need their own
  sign-in; a keyless dogfood exercises the challenge flow and the keyless apps.
- This never writes to your real home profile. It verifies the install landed in
  the throwaway dir and aborts if it did not.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_HOME = REPO / ".dogfood"


def _run_setup(home: Path, with_deps: bool) -> int:
    """Run tools/setup.py with the home redirected to `home`, prompts auto-skipped."""
    env = dict(os.environ)
    # Cover every platform's Path.home() resolution order:
    #   POSIX: HOME.  Windows: USERPROFILE, then HOMEDRIVE+HOMEPATH.
    env["HOME"] = str(home)
    env["USERPROFILE"] = str(home)
    env["HOMEDRIVE"] = home.drive or env.get("HOMEDRIVE", "")
    env["HOMEPATH"] = str(home)[len(home.drive):] if home.drive else str(home)

    cmd = [sys.executable, str(REPO / "tools" / "setup.py")]
    if not with_deps:
        cmd.append("--skip-deps")
    # Empty stdin lines skip the "paste your key" prompt into the keyless path.
    proc = subprocess.run(cmd, cwd=str(REPO), env=env, input="\n\n\n", text=True)
    return proc.returncode


def _verify_isolated(home: Path) -> bool:
    """Confirm the install landed in the throwaway home, never the real one."""
    staged = home / ".claude" / "skills" / "five-day-challenge"
    return staged.exists()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("--home", type=Path, default=DEFAULT_HOME,
                    help=f"Throwaway profile dir (default: {DEFAULT_HOME})")
    ap.add_argument("--with-deps", action="store_true",
                    help="Also install the document stack (slower)")
    ap.add_argument("--reset", action="store_true",
                    help="Delete the throwaway dir and exit")
    args = ap.parse_args()

    home = args.home.resolve()

    if args.reset:
        if home.exists():
            shutil.rmtree(home, ignore_errors=True)
            print(f"Removed {home}")
        else:
            print(f"Nothing to remove at {home}")
        return 0

    real_home = Path(os.path.expanduser("~")).resolve()
    if home == real_home:
        print("Refusing to dogfood into your real home directory.", file=sys.stderr)
        return 2

    project = home / "project"
    (home / ".claude").mkdir(parents=True, exist_ok=True)
    project.mkdir(parents=True, exist_ok=True)

    print(f"Staging the working tree into a throwaway profile: {home}\n")
    rc = _run_setup(home, args.with_deps)
    if rc != 0:
        print(f"\nsetup.py exited {rc}; check the output above.", file=sys.stderr)
    if not _verify_isolated(home):
        print("\n[abort] The install did not land in the throwaway profile "
              f"({home}\\.claude\\skills). Your real profile was not the target; "
              "nothing to clean up. This usually means Path.home() ignored the "
              "redirected env on this platform.", file=sys.stderr)
        return 1

    # Launch instructions, per shell.
    print("\n" + "=" * 68)
    print("Dogfood profile ready. Launch a clean-slate owner session:\n")
    print("  PowerShell:")
    print(f'    $env:USERPROFILE="{home}"; $env:HOME="{home}"; cd "{project}"; claude')
    print("\n  bash / zsh:")
    print(f'    HOME="{home}" USERPROFILE="{home}" bash -c \'cd "{project}" && claude\'')
    print("\nThen, as a brand-new owner, say:  start the 5 day challenge")
    print("\nThe project folder is empty, so start-here cold-starts like a real")
    print("first run. Connected steps (web research, Gmail/Calendar) still need")
    print("their own sign-in.")
    print(f"\nReset when done:  python tools/dogfood.py --reset")
    print("=" * 68)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

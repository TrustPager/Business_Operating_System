---
description: Update your Business Operating System to the latest version, safely. It finds your install, pulls the newest version from GitHub, refreshes your skills and commands, and protects your own brand and settings so nothing you set gets overwritten. Then it tells you what changed and reminds you to restart.
---

Run the **Update BOS** skill.

Invoke the skill at `skills/update-bos/SKILL.md` and follow it exactly.

Find the install from `~/.claude/bos.json` (`bos_home`), run everything from
there. Protect any local changes with `git stash` before `git pull`, then pop
them back. Their brand files are untracked by design, so their branding is never
touched. Re-run `python tools/setup.py --skip-deps` to refresh skills and
commands. Never hand the owner a raw command, you run it with permission. Report
what changed in plain, outcome language, and remind them to restart Claude Code so
new skills load. No em dashes in anything they read.

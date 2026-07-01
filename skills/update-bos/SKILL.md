---
name: Update BOS
description: Update your Business Operating System to the latest version, safely. Finds your install, pulls the newest version from GitHub, refreshes your skills and commands, and protects your own brand and settings so nothing you set gets overwritten. Tells you plainly what changed and reminds you to restart so the updates load.
triggers:
  - update my business operating system
  - update BOS
  - get the latest version
  - grab the new version
  - check for updates
  - pull the latest
  - update the operating system
function_slot: floor
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---

# Update BOS

Update the owner's Business Operating System to the latest version and make it
feel effortless and safe. They should never see a git error or be handed a
command to run. You do the whole thing, protect anything they have personalised,
and tell them what changed in plain language.

## Step 1: Find their install

Read `~/.claude/bos.json` and use its `bos_home` value as the BOS folder. If that
is missing, use the BOS repo directory (the folder that contains `tools/` and
`kernel/`). Run every git and setup command from there.

## Step 2: Protect their work, then pull

Their brand kit is already safe: those files (brand.json, logo, favicons) are
theirs and are not tracked, so an update never touches them. To be safe with
anything else they might have changed:

- Check for local changes (`git status`). If there are any, shelve them first
  (`git stash`) so the update cannot fail on them.
- Pull the latest (`git pull`).
- If you shelved changes, put them back (`git stash pop`). If that ever clashes,
  keep THEIR version and tell them in plain words which file you kept. Never drop
  their work silently.

If git says already up to date, tell them they are on the latest version and
stop. Nothing else to do.

## Step 3: Refresh the installed pieces

Run setup so the new skills and commands become available, and any new
blank-canvas brand defaults get seeded (it never overwrites a brand they set):

```bash
python tools/setup.py --skip-deps
```

setup is idempotent and safe to run every time. It refreshes the BOS skills and
commands in `~/.claude/`, and never touches their key or any skill they added
themselves.

## Step 4: Report, then restart

Tell them plainly what updated: the new or improved things they can now do, in
outcome language, not filenames. Reassure them their brand and settings are
untouched. Then remind them to restart Claude Code so the new skills load (skills
load at startup, not mid-session).

## Hard rules

- **Never hand them a raw git or pip command to run themselves.** You run it,
  with permission, and report back.
- **Never let their brand or their own added skills get overwritten.** Their brand
  files are untracked by design; protect any other local change with stash.
- **Never claim it updated if git said already up to date.**
- **Plain language and reassurance throughout.** No em dashes in anything they read.

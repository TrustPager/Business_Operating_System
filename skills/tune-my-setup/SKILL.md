---
name: Tune My Setup
description: Set up Claude Code with sensible working-style defaults and pre-approved safe reads, written into your global config so every project benefits. Two modes: apply the recommended defaults in one step, or walk through a short Q&A to build a personalised version. Additive and reversible at any time.
triggers:
  - tune my setup
  - set up my claude config
  - configure claude code
  - set up claude code best practices
  - improve my claude settings
  - add permissions to claude
  - set up global claude
  - configure my assistant settings
  - recommended claude settings
function_slot: floor
requires_driver: none
requires_credential: none
data_path: local
status: active
---

# Tune My Setup

This module writes your global Claude Code config at `~/.claude/`. It touches
two files: `~/.claude/CLAUDE.md` (a working-style guidance block) and
`~/.claude/settings.json` (a permissions block). Every change is additive and
clearly marked, so nothing existing is overwritten and you can edit or remove
the block whenever you like.

It does NOT touch your project's `CLAUDE.md`. Your project file stays exactly
as you left it.

---

## What gets added (the recommended defaults)

**Working-style block** (written into `~/.claude/CLAUDE.md`): a short set of
preferences that shape how Claude Code talks to you across every project:

- Plain language, no jargon
- One suggestion at a time
- Direct and confident
- Asks before anything customer-facing goes out
- Asks before anything hard to reverse

It also includes two optional content-style preferences (positive-only copy and
no em dashes) with clear labels so you can enable or remove them whenever you
want.

**Permissions block** (written into `~/.claude/settings.json`): a curated
allow/deny list so you are not prompted for every routine read:

- Pre-allowed (no prompt): safe reads from your workspace. All `get_*`,
  `list_*`, `search_*`, `describe_*`, and `preview_*` tools, plus `Read`,
  `Glob`, and `Grep`. These never change data.
- Still prompted (intentional): every write, send, create, update, delete,
  and bulk action. These touch real records, so a confirmation step stays.
- Explicitly denied: `delete_*` and `bulk_delete_*` permanently blocked.

---

## Pick your mode

**Mode A: Recommended** applies the above in one step. You see a preview first
and confirm before anything runs.

**Mode B: Guided** asks you a few short questions, explains the why behind each
one, builds a version tailored to your answers, and applies that.

Which would you prefer? Type A or B (or just say "recommended" or "guided"),
and we will go from there.

---

## Mode A: Recommended

Here is what will be written. Take a read, then say yes to apply.

**`~/.claude/CLAUDE.md` block** (inserted between BOS markers, never touching
anything outside them):

> Plain language, one suggestion at a time, direct and confident. Confirms
> before customer-facing output and before anything hard to reverse. Two
> optional content-style rules included but labelled, ready to switch on.

**`~/.claude/settings.json` permissions**:

- Allow: all TrustPager read tools, `Read`, `Glob`, `Grep`
- Deny: `delete_*`, `bulk_delete_*`
- Everything else: prompted each time

When you say yes, run these two commands in order:

```
python ~/.claude/bos-run.py tool setup_claude_config merge-claude-md
python ~/.claude/bos-run.py tool setup_claude_config merge-settings
```

Both default to the BOS bundled source files, so no `--from` flag is needed.
Each prints `[ok]` when it succeeds.

After they run, confirm the result:

- Open `~/.claude/CLAUDE.md` and look for the block between
  `<!-- bos:best-practices:start -->` and `<!-- bos:best-practices:end -->`.
- Open `~/.claude/settings.json` and look for the `allow` and `deny` arrays.

That is it. Changes take effect from the next Claude Code session.

---

## Mode B: Guided

Guided builds the same two files from your answers. Work through these
questions one at a time:

**Q1: How direct do you like your assistant?**
Some people prefer shorter, more confident replies. Others prefer more
explanation before a recommendation. (This shapes the working-style block.)

**Q2: Do you want the positive-only copy rule enabled?**
When drafting anything a customer or prospect will read, would you like Claude
to lead with outcomes and results rather than pain or frustration? (Recommended
for service businesses. You can change this any time by editing the block.)

**Q3: Do you want the no-em-dash rule enabled?**
Em dashes can make writing feel like it came from a template. Turning this off
means Claude uses commas, colons, or a new sentence instead. (Recommended if
you want output that sounds like a person, not a tool.)

**Q4: Do you use or plan to use TrustPager?**
If yes: the recommended permissions include pre-allowed safe reads for all
TrustPager `get_*`, `list_*`, `search_*`, `describe_*`, and `preview_*` tools,
so you are not prompted on every read. Writes still prompt. If no: those entries
are left out and the allow list contains only `Read`, `Glob`, and `Grep`.

**Q5: Keep all write tools prompting?**
Recommended: yes. This means any action that changes data (send, create, update,
delete) surfaces a confirmation step before it runs. The only exception is if
you explicitly trust a specific tool and add it yourself later.

Once you have answered all five, compose:

1. A CLAUDE.md block reflecting your working-style choices (Q1, Q2, Q3), write
   it to a temp file, and call:

   ```
   python ~/.claude/bos-run.py tool setup_claude_config merge-claude-md --from <temp-file>
   ```

2. A `settings.json` permissions object reflecting Q4 and Q5, write it to a
   temp file, and call:

   ```
   python ~/.claude/bos-run.py tool setup_claude_config merge-settings --from <temp-file>
   ```

Both commands are additive: they merge into what is already there rather than
replacing it. The `--from` flag points each tool at the file you built from
the guided answers.

---

## Project CLAUDE.md

This module sets up your global config only. If you do not yet have a
`CLAUDE.md` in your project folder, run `/start-here` to set up your business
profile. That is where your business context (name, services, voice, region)
lives so every skill knows who it is working for.

---

## Reversibility

Nothing applied here is permanent:

- To change or remove the working-style block: open `~/.claude/CLAUDE.md`,
  find the section between `<!-- bos:best-practices:start -->` and
  `<!-- bos:best-practices:end -->`, and edit or delete it freely.
- To change permissions: open `~/.claude/settings.json` and edit the `allow`
  and `deny` arrays directly. Plain JSON, no special tools needed.

Changes take effect from the next Claude Code session.

For a deeper read on why each setting works the way it does, see
`knowledge/claude-setup-method.md`.

---

**Note on the launcher:** The commands above use `~/.claude/bos-run.py` as
the signpost. If that file is missing, run `python tools/setup.py` once from
the BOS directory to create it, then re-run the command above.

---
description: Set up Claude Code with sensible working-style defaults and safe-read permissions, written into your global config so every project benefits. Two modes: apply the recommended defaults in one step, or answer a few short questions to build a personalised version. Additive and reversible at any time.
---

Run the **Tune My Setup** skill.

Invoke the skill at `skills/tune-my-setup/SKILL.md`. Follow it exactly:
present the two-line summary of what will be written (working-style block and
permissions), offer Mode A (recommended, one-step) or Mode B (guided, Q&A),
wait for the user to pick, then carry out the chosen mode.

Mode A: run `merge-claude-md` then `merge-settings` via the signpost (no
`--from` flag needed for the bundled defaults), confirm `[ok]` from each, and
tell the user exactly where to find the changes.

Mode B: ask the five questions one at a time, explain the why behind each,
compose the CLAUDE.md block and settings JSON from the answers, write each to a
temp file, and call the tool with `--from <temp-file>`.

End every mode by pointing to `/start-here` if no project `CLAUDE.md` exists,
and reassuring the user that every change is editable or removable at any time.

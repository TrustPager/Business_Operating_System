---
description: Check a nurture sequence against the house style — CTA above image, consistent sign-off, positive subjects, and set-wide consistency. Works on a live queue or local drafts.
---

Run the **Lint Nurture Sequence** skill.

Invoke the skill at `skills/lint-nurture-sequence/SKILL.md`. Follow it exactly:
read the sequence to lint — the live queue via `trustpager` MCP read tools
(`get_auto_queue` + its steps for a given queue id) or a local drafts file via
file tools — check it against the house style, then present the verdict — fails
first, then warnings, then the set-wide consistency findings — and route each
fix to `design-nurture-sequence` → `wire-nurture-sequence`. Never edit the queue
from this skill.

If the operator didn't say which queue or drafts, ask which one to lint.

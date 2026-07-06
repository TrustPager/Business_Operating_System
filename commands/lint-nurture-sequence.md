---
description: Check a follow-up sequence against your house style before it ships, and catch drift.
---

Run the **Lint Nurture Sequence** skill.

Invoke the skill at `skills/lint-nurture-sequence/SKILL.md`. Follow it exactly:
run `tools/lint-sequence.py` against the live queue (`--queue <id>`) or the
drafts file (`--drafts <file>`), then present the verdict: fails first, then
warnings, then the set-wide consistency findings, and route each fix to
`design-nurture-sequence` → `wire-nurture-sequence`. Never edit the queue from
this skill.

If the operator didn't say which queue or drafts, ask which one to lint.

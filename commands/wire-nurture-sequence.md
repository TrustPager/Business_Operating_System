---
description: Push an approved set of follow-up drafts live in the right order so the sequence runs on its own.
---

Run the **Wire Nurture Sequence** skill.

Invoke the skill at `skills/wire-nurture-sequence/SKILL.md`. Read the
live auto queue state first via `tools/dump-crm-bundle.py
--resources auto_queues`. Inventory the writes (UPDATE / ADD / CREATE)
and confirm with the operator before any MCP calls.

For inserting a new step at position 1 (or any middle position), use
the REVERSE-ORDER step_order shuffle described in the skill, never the
forward-order version.

If drafts haven't been approved yet, STOP and ask the operator to run
`/design-nurture-sequence` first.

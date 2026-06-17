---
description: Push approved nurture-sequence drafts into a live TrustPager auto queue — updates existing actions, adds new ones for silent stage-movers, inserts new queue steps with the reverse-order step_order shuffle.
---

Run the **Wire Nurture Sequence** skill.

Invoke the skill at `skills/wire-nurture-sequence/SKILL.md`. Read the
live auto queue state first via `trustpager` MCP read tools
(`list_auto_queues`, then `get_auto_queue` on the target queue and its
steps). Inventory the writes (UPDATE / ADD / CREATE) and confirm with
the operator before any MCP write calls.

For inserting a new step at position 1 (or any middle position), use
the REVERSE-ORDER step_order shuffle described in the skill — never the
forward-order version.

If drafts haven't been approved yet, STOP and ask the operator to run
`/design-nurture-sequence` first.

---
description: Design a multi-step email nurture sequence in the operator's voice: pick the help-center video per stage, draft each email anchored to a verbatim customer pain. Drafts only, no live writes.
---

Run the **Design Nurture Sequence** skill.

Invoke the skill at `skills/design-nurture-sequence/SKILL.md`. Confirm
which auto queue + audience + sequence shape with the operator first.
Map a help-center video to each stage, present the mapping for approval,
then draft each email following the canonical shape: forward-looking
subject, warm human opener, one core idea per paragraph, the video link
as the soft CTA, sign-off block.

This skill DRAFTS in chat. It does not write to the live auto queue.
When drafts are approved, run `/wire-nurture-sequence` to push them.

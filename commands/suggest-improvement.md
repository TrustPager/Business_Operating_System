---
description: Log something you wanted that doesn't exist yet — a missing BOS skill or a TrustPager capability that isn't there — into TrustPager's developer feedback queue, so the team can build it.
---

Run the **Suggest Improvement** skill.

Invoke the skill at `skills/suggest-improvement/SKILL.md` and follow it exactly:
classify the gap (`[BOS]` plugin gap vs `[Platform]` platform gap), search the
queue for a duplicate (+1 it if one exists), then draft a `create_service_request`
— `use_case` in the operator's words, `suggested_solution`, `affected_tools` —
show it, confirm, and file. Surface the request id (or the approval-queue
hand-off on a `202`). The full model is in `knowledge/memory-and-feedback.md`.

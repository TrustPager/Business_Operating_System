---
description: Show where every document you sent for signing stands, and who to follow up or chase, hottest first.
---

Run the **Signing Radar** skill.

Invoke the skill at `skills/signing-radar/SKILL.md`. Run
`python skills/signing-radar/fetch.py` (pass `--stale-days N` to tune the
unopened threshold), then present the report bucketed by follow-up urgency:
OPENED-NOT-SIGNED first (engaged, call them now), then SENT-UNOPENED-STALE
(chase or resend), then DECLINED, then the completed count. Offer the next
action per envelope (nudge/resend, draft a follow-up via `/draft-reply`, or
void a dead one), one at a time, with a yes. Never auto-resend or auto-void.

For "do this automatically every time someone opens a document", hand to
`/automate-this` on the `signature_opened` trigger.

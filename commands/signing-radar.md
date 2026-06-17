---
description: Show where every document you sent for signing stands — the sent → opened → signed funnel, who opened but hasn't signed (follow up now), who never opened and is going stale, and who declined. Hottest follow-ups first.
---

Run the **Signing Radar** skill.

Invoke the skill at `skills/signing-radar/SKILL.md`. It gathers signing envelopes
via `trustpager` MCP read tools (`list_signing_envelopes` + `get_signing_envelope`)
(the skill lets you tune the unopened-stale window in plain language, e.g. "use a
5-day stale window"), then presents the report bucketed by follow-up urgency:
OPENED-NOT-SIGNED first (engaged, call them now), then SENT-UNOPENED-STALE
(chase or resend), then DECLINED, then the completed count. Offer the next
action per envelope — nudge/resend, draft a follow-up via `/draft-reply`, or
void a dead one — one at a time, with a yes. Never auto-resend or auto-void.

For "do this automatically every time someone opens a document", hand to
`/automate-this` on the `signature_opened` trigger.

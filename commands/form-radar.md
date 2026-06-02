---
description: Show where every form you sent stands — the sent → opened → completed funnel, who started but didn't finish (nudge), who never opened it and is going stale (chase), and what completed this week. Hottest follow-ups first.
---

Run the **Form Radar** skill.

Invoke the skill at `skills/form-radar/SKILL.md`. Run
`python skills/form-radar/fetch.py` (`--stale-days N` to tune), then present the
report bucketed by follow-up urgency: STARTED-NOT-FINISHED first (a nudge closes
them), then SENT-UNOPENED-STALE (resend or call), then the completed count.
Offer the next action per submission — resend, draft a nudge via `/draft-reply`,
or void a dead one — one at a time, with a yes. Never auto-resend or auto-void.

For "nudge automatically whenever someone opens but doesn't finish", hand to
`/automate-this` on the `form_opened` trigger.

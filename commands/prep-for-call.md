---
description: Build the brief before a customer call: who they are, the deal, the history, and the outcome to drive.
---

Run the **Prep For Call** skill.

Invoke the skill at `skills/prep-for-call/SKILL.md`. Identify the call (today's
booking via `list_bookings`/`get_booking`, or a named person via
`search_opportunities`/`search_contacts`), then pull the picture around the
opportunity: `get_opportunity`, `get_opportunity_activities`, the last call's
transcript (`list_transcripts`, the most valuable input), `get_opportunity_tasks`,
`get_contact`, `get_opportunity_products`. Present the fixed brief (who they are /
where it's at / last time / open-owed / watch-for) ending in the single outcome
to drive. Read-only. Offer the follow-ons (`/draft-reply`, pull the proposal)
don't act unprompted. If there's no history, say "first conversation".

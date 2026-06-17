---
description: Build the brief before a customer call — who they are, the deal, the full history, what was said last time, what's open, and the one outcome to drive. Everything to walk in ready, in one read.
---

Run the **Prep For Call** skill.

Invoke the skill at `skills/prep-for-call/SKILL.md`. Identify the call (today's
booking via `list_bookings`/`get_booking`, or a named person via
`search_deals`/`search_contacts`), then pull the picture around the
opportunity: `get_deal`, `get_deal_activities`, the last call's
transcript (`list_transcripts` — the most valuable input), `get_deal_tasks`,
`get_contact`, `get_deal_products`. Present the fixed brief (who they are /
where it's at / last time / open-owed / watch-for) ending in the single outcome
to drive. Read-only — offer the follow-ons (`/draft-reply`, pull the proposal),
don't act unprompted. If there's no history, say "first conversation".

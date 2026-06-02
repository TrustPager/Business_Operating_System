---
description: Show the state of every job — count by status, which work orders have stalled in one status too long, and which completed recently (candidates for a completion update or review ask). Stalls first.
---

Run the **Work Order Radar** skill.

Invoke the skill at `skills/work-order-radar/SKILL.md`. Run
`python skills/work-order-radar/fetch.py` (`--stall-days N` to tune), then
present the report: STALLED first (sat too long in a non-terminal status), then
COMPLETED-THIS-WEEK (prompt: did the customer get the update + a review ask?),
then the by-status breakdown. Offer the next action per job — send a status
update (`send_work_status`, real recipients only, confirm first), move a status,
or draft a check-in via `/draft-reply` — one at a time, with a yes. Never
auto-send or auto-move.

For "ask for a review when a job completes" or portal-open alerts, hand to
`/automate-this`.

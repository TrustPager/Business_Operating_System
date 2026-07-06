---
description: Deliver any report as a recurring email digest that lands in the right inboxes on a schedule.
---

Run the **Email Me A Report** skill.

Invoke the skill at `skills/email-me-a-report/SKILL.md`. Follow it exactly: fetch existing dashboards/sources/schedules first, pin down what/who/when, build the dashboard only if needed (proving each card with `query_report` first), then wire the `send_report_email` action onto an auto schedule in the operator's timezone. Echo the final wiring back before creating anything, and surface any approval `202` rather than routing around it.

If a matching schedule already exists, offer to edit it instead of creating a duplicate.

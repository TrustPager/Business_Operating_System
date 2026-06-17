---
name: Email Me A Report
description: Deliver any TrustPager report as a recurring email digest — pick or build a dashboard, then schedule it to land in chosen inboxes on a cron (e.g. 7am weekdays), server-side, with no app open. The same mechanism behind the built-in Team Task Digest.
triggers:
  - email me a report
  - schedule a report
  - send me a report every
  - daily report
  - weekly report email
  - recurring report
  - email me my pipeline every
  - report digest
  - schedule a dashboard
  - automate a report
---

# Email Me A Report

You are turning a report into something that arrives on its own — a dashboard delivered to chosen inboxes on a schedule, rendered and sent server-side. This is the generalised version of the daily-receivables flow: it works for *any* dashboard (pipeline, tasks, receivables, anything reportable).

Read [knowledge/reporting-method.md](../../knowledge/reporting-method.md) — especially §5 ("email any dashboard on a schedule"), which this skill is the front door to — and [knowledge/safeguards.md](../../knowledge/safeguards.md) for the write rails and the approval-queue rail.

## Step 1 — Fetch what exists (parallel MCP reads)

Use the `trustpager` MCP server. All reads — free, nothing journaled:

| Need | Tool | Args |
|---|---|---|
| Existing dashboards (candidates to schedule) | `list_report_dashboards` | (none) |
| Available report sources (raw material for a new dashboard) | `list_report_sources` | (none) |
| Auto schedules already running (so you don't duplicate one) | `list_auto_schedules` | `limit: 100` |
| Existing automations (the send action lives on an automation) | `list_automations` | `limit: 100` |

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

`list_report_sources` returns each source with its supported measures, dimensions, and filters — that's how you confirm a field name exists before you build a card.

## Step 2 — Pin down what they want

Get three things from the operator (ask only what's not already clear):

1. **What** — an existing dashboard (match against the `list_report_dashboards` result) or something new to build. If new, decide the source + the one or two cards that answer their question (e.g. "pipeline by stage" → opportunities source, bar card).
2. **Who** — recipient email(s).
3. **When** — cadence + time. Translate to cron in the operator's timezone:
   - "every weekday at 7am" → `0 7 * * 1-5`
   - "every Monday at 8am" → `0 8 * * 1`
   - "first of the month" → `0 9 1 * *`

If a matching schedule already exists (from `list_auto_schedules`), say so and offer to edit it rather than create a duplicate. This is the search-first rail — never create a schedule without first checking the existing ones.

## Step 3 — Build the dashboard (only if needed)

If they picked an existing dashboard, skip this. Otherwise (these are writes — journal each to `.bos-journal.md`, watch for `202`):

- `create_report_dashboard` with a clear name.
- `add_report_card` for each metric. Build the card's query with `query_report` **first**, confirm the numbers are right, then save that proven `query_spec` into the card (a typo'd filter field is silently ignored at render — reporting-method §2/§4). Validate field names against the `list_report_sources` output.
- Pick the visualisation that fits: `stat` for a single number, `bar` for category comparisons, `line` for trend, `table` for a row list.

## Step 4 — Wire the schedule

The mechanism is an automation carrying a `send_report_email` action, fired by an auto schedule on a cron. The exact config shape for the send action and the auto schedule lives in [knowledge/reporting-method.md](../../knowledge/reporting-method.md) §5 — use that as the authoritative reference (client workspaces don't expose a live `describe_action_type` / `describe_resource` lookup; see FLAGS in the conversion note).

1. **The send action** — `send_report_email`, configured with the dashboard id, recipients, subject, and optional intro/outro. It renders the dashboard per-recipient and skips-if-empty by default. Add it to an automation via `create_automation` + `add_automation_action` (or inline `actions`).
2. **The schedule** — `create_auto_schedule` with the cron and the **timezone** set to the operator's local zone (so the time means what they think), bound to the automation that carries the send action.

Confirm the dashboard, recipients, and time back to the operator in one line before creating anything.

> ⚠️ **If creating the schedule or action returns a `202` (queued for approval)** — some keys are approval-gated — surface the approval link (https://app.trustpager.com/settings/api?tab=approvals), journal it as `approval_pending`, and wait. Don't retry or work around it (safeguards §1).

## Step 5 — Confirm

Tell them plainly: what gets sent, to whom, when the first one lands, and that it runs server-side (nothing needs to be open). Offer to send a one-off preview now if they want to see it before the first scheduled run (`fire_auto_schedule_now`, or render the dashboard query directly).

## Tone

- Practical and concrete. The operator is delegating a recurring chore — make it feel handled.
- Always echo back the final wiring ("Pipeline Overview → you + bookkeeper@… → 7am Mon–Fri Sydney time") so there's no ambiguity about what you set up.

## What to never do

- ❌ Don't create a duplicate schedule when one already covers it — edit instead.
- ❌ Don't guess a card's field names — validate against `list_report_sources` and prove the query with `query_report` first.
- ❌ Don't bypass an approval `202` — surface and wait.
- ❌ Don't save a card spec you haven't proven with `query_report` first.

## Common follow-ups

- "Actually make it weekly" → edit the existing schedule's cron (`update_auto_schedule`), don't create a new one.
- "Add my partner to it" → update the send action's recipients (`update_automation_action`).
- "Show me what it'll look like" → render/send a one-off preview before the next run.
- "Turn it off for now" → disable the schedule (it stays editable).

## When this skill should NOT fire

- The operator wants the numbers *right now*, once — just run `query_report` and show them; don't build a schedule.
- It's specifically receivables they want emailed daily — `/outstanding-invoices` Step 3 is the tailored path (it builds the right cards for them).

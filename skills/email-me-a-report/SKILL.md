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
function_slot: strategy
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__create_report_dashboard
  - mcp__add_report_card
  - mcp__query_report
  - mcp__describe_action_type
  - mcp__describe_resource
status: active
---

# Email Me A Report

You are turning a report into something that arrives on its own — a dashboard delivered to chosen inboxes on a schedule, rendered and sent server-side. This is the generalised version of the daily-receivables flow: it works for *any* dashboard (pipeline, tasks, receivables, anything reportable).

Read [knowledge/reporting-method.md](../../knowledge/reporting-method.md) — especially §5 ("email any dashboard on a schedule"), which this skill is the front door to — and [knowledge/safeguards.md](../../knowledge/safeguards.md) for the approval-queue rail.

## Step 1 — Fetch what exists

```bash
python ~/.claude/bos-run.py email-me-a-report
```

Returns existing `dashboards` (candidates to schedule), available `sources` (raw material for a new one), and `existing_schedules` (so you don't duplicate). Shape documented at the bottom of `fetch.py`.

## Step 2 — Pin down what they want

Get three things from the operator (ask only what's not already clear):

1. **What** — an existing dashboard (match against `dashboards`) or something new to build. If new, decide the source + the one or two cards that answer their question (e.g. "pipeline by stage" → opportunities source, bar card).
2. **Who** — recipient email(s).
3. **When** — cadence + time. Translate to cron in the operator's timezone:
   - "every weekday at 7am" → `0 7 * * 1-5`
   - "every Monday at 8am" → `0 8 * * 1`
   - "first of the month" → `0 9 1 * *`

If a matching schedule already exists in `existing_schedules`, say so and offer to edit it rather than create a duplicate.

When the ask is a generic "my weekly numbers" with no specific metrics named, default to the weekly scoreboard metric set (`business-method.md` §12.6; the card-to-source mapping lives in reporting-method §7): leads and conversations this week, close rate, cash collected, open/overdue follow-ups, plus one card for the metric the current diagnosis says matters most. Only build cards the workspace can honestly fill — a metric with no source becomes a "start measuring it" suggestion, not a chart.

## Step 3 — Build the dashboard (only if needed)

If they picked an existing dashboard, skip this. Otherwise:

- `create_report_dashboard` with a clear name.
- `add_report_card` for each metric. Build the card's query with `query_report` **first**, confirm the numbers are right, then save that proven `query_spec` into the card (a typo'd filter field is silently ignored at render — reporting-method §2/§4).
- Pick the visualisation that fits: `stat` for a single number, `bar` for category comparisons, `line` for trend, `table` for a row list.

## Step 4 — Wire the schedule

Two objects, both discovered live rather than guessed:

1. **The send action** — `describe_action_type('send_report_email')` for its exact config (dashboard id, recipients, subject, optional intro/outro). It renders the dashboard per-recipient and skips-if-empty by default.
2. **The schedule** — `describe_resource('auto_schedule')` for how to create the cron and bind it to the automation that carries the send action. Set the **timezone** to the operator's local zone so the time means what they think.

Confirm the dashboard, recipients, and time back to the operator in one line before creating anything.

> ⚠️ **If creating the schedule or action returns a `202` (queued for approval)** — some keys are approval-gated — surface the approval link (https://app.trustpager.com/settings/api?tab=approvals) and wait. Don't retry or work around it (safeguards §1).

## Step 5 — Confirm

Tell them plainly: what gets sent, to whom, when the first one lands, and that it runs server-side (nothing needs to be open). Offer to send a one-off preview now if they want to see it before the first scheduled run.

## Tone

- Practical and concrete. The operator is delegating a recurring chore — make it feel handled.
- Always echo back the final wiring ("Pipeline Overview → you + bookkeeper@… → 7am Mon–Fri Sydney time") so there's no ambiguity about what you set up.

## What to never do

- ❌ Don't create a duplicate schedule when one already covers it — edit instead.
- ❌ Don't guess the `send_report_email` config or the auto_schedule shape — `describe_*` them.
- ❌ Don't bypass an approval `202` — surface and wait.
- ❌ Don't save a card spec you haven't proven with `query_report` first.

## Common follow-ups

- "Actually make it weekly" → edit the existing schedule's cron, don't create a new one.
- "Add my partner to it" → update the send action's recipients.
- "Show me what it'll look like" → render/send a one-off preview before the next run.
- "Turn it off for now" → disable the schedule (it stays editable).

## When this skill should NOT fire

- The operator wants the numbers *right now*, once — just run `query_report` and show them; don't build a schedule.
- It's specifically receivables they want emailed daily — `/outstanding-invoices` Step 3 is the tailored path (it builds the right cards for them).

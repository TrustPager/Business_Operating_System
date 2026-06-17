---
name: Audit My Automations
description: Health-check every automation in the workspace — which are firing, which have gone stale, which are erroring, which are missing safety dials (dedup, daily caps), and which overlap with each other. Surfaces problems in priority order with a one-line fix for each.
triggers:
  - audit my automations
  - check my automations
  - are my automations working
  - automation health check
  - which automations are broken
  - review my automations
  - are my automations still firing
  - automation audit
---

# Audit My Automations

Operators set automations up and never look at them again — so they don't notice when one silently stops firing, starts erroring, or sends twice. This skill is the regular check-up.

**Read first:** [`knowledge/automation-method.md`](../../knowledge/automation-method.md) — especially §6 (safety dials) and §8 (reading the run log). The flags this skill raises map directly to those sections.

## Step 1 — Pull the data (parallel MCP calls)

Use the `trustpager` MCP server. All of these are reads — free, fast, nothing journaled.

| Need | Tool | Args |
|---|---|---|
| Every automation (flat list — no triggers/actions inline) | `list_automations` | `limit: 100` (page with `after` until exhausted) |
| Full structure per automation (triggers + actions + conditions inline) | `get_automation` | `automation_id: <id>` — one call per automation |
| Recent run health per **enabled** automation | `list_automation_runs` | `automation_id: <id>`, `limit: 10` |

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

Sequence:
1. `list_automations` (page through all of them with the `after` cursor) to get the id list.
2. For **every** automation, call `get_automation` to get its real structure. The flat list does NOT embed triggers/actions — `get_automation` does (returns name, `trigger_type`, conditions, and the action sequence inline). Fire these in parallel.
3. For **enabled automations only** (disabled ones can't fire, so stale/failure flags don't apply), call `list_automation_runs` with `limit: 10` to sample the last 10 runs. Keeps the call count down. Fire these in parallel too.

If a `get_automation` call fails, degrade to the flat list row for that automation rather than dropping it.

## Step 2 — Compute the per-automation flags

Everything below is computed against **now**. For each automation, read `enabled`, `trigger_type`, its triggers array (`automations_triggers`), its actions array (`automations_actions`), `dedup_enabled`, and `max_executions_per_day`. From its sampled runs, find the latest run time (`started_at` / `created_at`) and tally the status mix across `completed` / `skipped` / `failed` / other.

Raise these flags:

| Flag | Condition |
|---|---|
| `disabled` | `enabled` is false |
| `no_actions` | actions array is empty |
| `no_triggers` | triggers array is empty **AND** `trigger_type` is NOT one of `stage_changed` / `manual` / `api` / `event_queue_step` / `auto_queue` / `scheduled` (those fire without a trigger row, so zero triggers is normal for them — don't flag) |
| `never_run` | enabled but zero runs sampled |
| `stale_Nd` | enabled, has a last-run time, and it's **≥ 30 days** ago (N = days idle) |
| `recent_failures_N` | one or more sampled runs have status `failed` (N = failed count) |
| `mostly_skipped` | **≥ 3** runs sampled AND `skipped` runs are **≥ 80%** of those sampled (conditions may be too tight) |
| `sends_without_dedup` | enabled AND has a send action AND `dedup_enabled` is false |
| `webhook_without_daily_cap` | enabled AND has a webhook/feedback action AND `max_executions_per_day` is null |

**Send action types** (these reach a customer / cost credits, so they want dedup ON): `send_custom_email`, `send_gmail_email`, `send_sms`, `send_whatsapp`, `voice_outbound_call`, `send_form`, `send_for_signing`, `send_marketing_email`.

**Webhook/feedback action types** (these want a daily cap as a runaway seatbelt): `call_webhook`, `facebook_conversion`.

### Cross-automation: trigger overlaps

For **enabled** automations only, build a key for each trigger of the form `trigger_type:source_type:source_id` (use `any` for missing source_type, `*` for missing source_id). Any key shared by **2 or more** enabled automations is an **overlap** — list those automations together.

### Bucketing for the report

- **Needs attention:** any automation flagged `recent_failures_*`, `no_actions`, or `no_triggers`.
- **Worth a look:** any not already in "needs attention" that's flagged `stale_*`, `never_run`, `mostly_skipped`, `sends_without_dedup`, or `webhook_without_daily_cap`.
- **Healthy:** everything else that's enabled.
- **Disabled:** count separately — informational, not a problem.

## Step 3 — Present the report, worst first

Lead with what's broken, then what's risky, then a one-line "healthy" tally. Never dump all automations as a flat list.

```
🔧 NEEDS ATTENTION (N)
  → "Renewal reminder" — 3 failed runs this week. Last error: <error_message>. → check it
  → "Old intake" — has a trigger but no actions (does nothing). → add actions or delete

⚠️ WORTH A LOOK (N)
  → "Quote follow-up" — enabled but hasn't fired in 41 days. Trigger may be wrong, or just quiet.
  → "Welcome email" — sends email but dedup is OFF — a double-submit double-emails. → turn dedup on
  → "Lead → quoting API" — calls a webhook with no daily cap. → set max_executions_per_day as a seatbelt
  → "Win celebration" — 9 of last 10 runs SKIPPED. Conditions may be too tight to ever pass.

🔁 OVERLAPS (N)
  → "Tag new lead" and "Email new lead" both fire on form_completed (Intake form).
    Fine if intentional; consolidate into one automation with multiple actions if not.

✅ HEALTHY: 12 automations firing normally.
```

### What each flag means + the fix

| Flag | Meaning | Fix to offer |
|---|---|---|
| `recent_failures_N` | actions errored on recent runs | open it, read `error_message`; `/why-didnt-it-fire` for the detail |
| `no_actions` | trigger fires but nothing happens | add actions, or delete the automation |
| `no_triggers` | nothing can fire it (and not a stage automation) | add a trigger, or it's dead weight |
| `never_run` | enabled but never fired | trigger/source likely wrong, or genuinely no events yet |
| `stale_Nd` | enabled, no run in N days (≥30) | confirm the trigger still matches reality; not always a problem |
| `mostly_skipped` | ≥80% of recent runs `skipped` | conditions too tight — they rarely pass |
| `sends_without_dedup` | a send action, dedup OFF | turn dedup on so a double-event doesn't double-send |
| `webhook_without_daily_cap` | `call_webhook`/feedback action, no daily cap | set `max_executions_per_day` as a runaway-loop seatbelt |
| `disabled` | switched off | informational — list under a "staged/off" count, not as a problem |

## Step 4 — Offer fixes (with approval)

These are writes — they follow the rails in [`knowledge/safeguards.md`](../../knowledge/safeguards.md): show the change, get a yes, apply it **one at a time**, then journal each write as one line to `.bos-journal.md`. If a write returns a `202`/`approval_id`, surface the approvals link and stop — don't retry.

For the safe, mechanical fixes, offer to apply them — one at a time, with a yes:
- Turn on dedup → `update_automation(automation_id, dedup_enabled=true, dedup_window_minutes=60)`
- Set a daily cap → `update_automation(automation_id, max_executions_per_day=N)`
- Disable a redundant duplicate → `disable_automation(automation_id)`

Never delete an automation without explicit confirmation naming it. For "why is it failing / skipping" deep-dives, hand to `/why-didnt-it-fire`. For building a missing automation, `/automate-this`.

## What to never do

- ❌ Don't present automations alphabetically or as one flat list — rank by severity.
- ❌ Don't auto-apply fixes. Offer, get a yes, then apply — one at a time — and journal each.
- ❌ Don't flag `disabled` as broken — staged/off is a valid state. Count it, don't alarm about it.
- ❌ Don't treat `skipped` runs as failures — that's conditions working as designed. Only `mostly_skipped` is worth a mention.

## Output shape

Open with the headline tally ("18 automations: 12 healthy, 2 need attention, 4 worth a look"), then the prioritised sections, then the single most important fix to make first.

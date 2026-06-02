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

## Step 1 — Fetch the health digest

```bash
python skills/audit-my-automations/fetch.py
```

One call: lists every automation (with triggers + actions inline), samples each one's recent runs, and computes per-automation flags plus cross-automation trigger overlaps. The shape is documented at the bottom of `fetch.py`.

If the script can't run (auth/network), fall back to `mcp__trustpager__list_automations` + `mcp__trustpager__list_automation_runs` per automation — but that's many calls; prefer the script.

## Step 2 — Present the report, worst first

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

## Step 3 — Offer fixes (with approval)

For the safe, mechanical fixes, offer to apply them — **one at a time, with a yes**:
- Turn on dedup → `mcp__trustpager__update_automation(automation_id, dedup_enabled=true, dedup_window_minutes=60)`
- Set a daily cap → `update_automation(automation_id, max_executions_per_day=N)`
- Disable a redundant duplicate → `mcp__trustpager__disable_automation(automation_id)`

Never delete an automation without explicit confirmation naming it. For "why is it failing / skipping" deep-dives, hand to `/why-didnt-it-fire`. For building a missing automation, `/automate-this`.

## What to never do

- ❌ Don't present automations alphabetically or as one flat list — rank by severity.
- ❌ Don't auto-apply fixes. Offer, get a yes, then apply — one at a time.
- ❌ Don't flag `disabled` as broken — staged/off is a valid state. Count it, don't alarm about it.
- ❌ Don't treat `skipped` runs as failures — that's conditions working as designed. Only `mostly_skipped` is worth a mention.

## Output shape

Open with the headline tally ("18 automations: 12 healthy, 2 need attention, 4 worth a look"), then the prioritised sections, then the single most important fix to make first.

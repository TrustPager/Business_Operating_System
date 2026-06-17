---
name: Why Didn't It Fire
description: Diagnose why a specific automation didn't do what the operator expected — disabled, never matched, conditions skipped it, an action failed, or it actually ran fine and the surprise is in the outcome. Walks the run log and gives the one real reason plus the fix.
triggers:
  - why didn't my automation fire
  - why didn't it fire
  - my automation isn't working
  - the automation didn't run
  - why didn't the email send
  - automation didn't trigger
  - debug my automation
  - why did nothing happen
---

# Why Didn't It Fire

An operator expected an automation to do something and it didn't. Your job is to find the **one real reason** and tell them the fix — not a list of maybes. Almost every case is one of five things, and the run log tells you which.

**Read first:** [`knowledge/automation-method.md`](../../knowledge/automation-method.md) §8 (reading the run log) — this skill is that ladder, walked by hand.

## Step 1 — Identify which automation

Get the automation id or a distinctive bit of its name. If the operator is vague ("my lead automation"), run `/audit-my-automations` first to list them, or ask which one.

## Step 2 — Pull the diagnostic bundle (MCP calls)

Use the `trustpager` MCP server. These are reads — free, nothing journaled, no approval.

| You have | Tool | Args |
|---|---|---|
| The automation's UUID | `get_automation` | `id: "<uuid>"` — returns the structure (enabled, triggers, conditions, actions, dedup/cap) |
| Only a name fragment | `list_automations` | `limit: 100` — then filter to automations whose `name` contains the fragment |
| Either way, its run history | `list_automation_runs` | `automation_id: "<uuid>"`, `limit: 15` |

If a name fragment matches **more than one** automation, list the matches with their ids and ask the operator to re-run with the exact id — don't guess which one. Once you have the id, fetch its full structure with `get_automation` (so triggers/conditions/actions come back inline), then its runs with `list_automation_runs`. For a single run's detail, use `get_automation_run`.

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

## Step 3 — Walk the ladder (you compute the headline reason)

From the structure + run log, determine the **one** reason, top to bottom — the first rung that matches is the answer:

**1. `DISABLED`** — `enabled` is false. It's switched off, so it never runs. → "It's staged, not live. Want me to test it and switch it on?" (test first — never enable blind).

**2. `NO_TRIGGERS`** — no triggers configured (and `trigger_type` isn't `stage_changed`). Nothing is wired to fire it. → add a trigger.

**3. `NO_ACTIONS`** — it has triggers but no actions. It fires but does nothing visible. → add actions.

**4. `NO_RUNS`** — enabled, has triggers + actions, but **zero run rows**. The trigger doesn't match how the event actually arrives. The usual culprits:
   - **Website form mistaken for `form_completed`.** A form on the customer's own site posts in as a **webhook**, not `form_completed` (which is only for internal TrustPager forms sent via `send_form`). This is the single most common one. → switch the trigger to `webhook_received`, or add a webhook trigger.
   - **Wrong source** — bound to one specific form/agent/number when the events come from a different one (or should be "any").
   - **Genuinely no events yet** — nothing has happened to fire it. Confirm an event actually occurred in the window.
   Show the configured triggers from the bundle and ask: "is this how the event really comes in?"

**5. Latest run `SKIPPED`** — runs exist but the most recent is `skipped`. A condition didn't pass, so actions never ran (this is the system working as designed, not a bug). → show the `conditions` and walk through which field likely failed against the event data. Often the condition is stricter than the operator remembers, or references a field that's blank for that trigger.

**6. Latest run `FAILED`** — it fired but an action errored. Read `error_message` / `error_details` on the latest run and name the failing action. Common: a `{{variable}}` that doesn't exist for that trigger (renders blank / breaks), a missing integration, a bad recipient. → fix the action's config; re-test with `execute_automation_action`.

**7. Latest run `COMPLETED`** — the automation ran fine; the surprise is in the *outcome*. → the issue is what an action did: a blank variable in an email, the wrong recipient field, the wrong stage. Inspect the actions and the run's action counts (`actions_attempted` / `actions_completed` / `actions_failed`), not the trigger.

If none of the above resolves it cleanly, inspect the recent runs directly and explain what you see — don't fall back to a list of maybes.

## Step 4 — One reason, one fix

State it cleanly:

```
"Renewal reminder" didn't fire because it's NOT matching your website leads.

Here's why: it's triggered on `form_completed`, which only covers forms YOU send
from TrustPager. Your website's contact form arrives as a webhook, so the
automation never sees it — that's why there are zero runs.

Fix: add a `webhook_received` trigger pointing at your website webhook, alongside
the existing one. Then it fires from BOTH doorways. Want me to add it?
```

Then offer the concrete fix. Any write follows the rails in `knowledge/safeguards.md` — confirm before it lands, journal it to `.bos-journal.md`, search-first:
- Enable (after a test) → `/automate-this` rails, or `enable_automation`
- Add/fix a trigger → `add_automation_trigger` / point it at the right source
- Loosen a condition → `update_automation` with the revised `conditions`
- Fix an action → `update_automation_action` then `execute_automation_action` to re-test

## What to never do

- ❌ Don't give a list of five maybes — find the ONE reason from the run log and lead with it.
- ❌ Don't call `skipped` a failure — it's conditions doing their job. Explain it as "a condition blocked it", not "it broke".
- ❌ Don't re-enable or re-fire anything to "test" against a real customer — use `execute_automation_action` with sample data, or a test workspace.
- ❌ Don't guess at conditions/triggers — read them from the bundle and quote them back.

## Output shape

One sentence: which automation + the single reason. Then a short plain-English "here's why", then the concrete fix offered as a yes/no action.

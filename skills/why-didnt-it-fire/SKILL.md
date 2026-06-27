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
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__enable_automation
  - mcp__trustpager__add_automation_trigger
  - mcp__trustpager__update_automation
  - mcp__trustpager__update_automation_action
  - mcp__trustpager__execute_automation_action
status: active
---

# Why Didn't It Fire

An operator expected an automation to do something and it didn't. Your job is to find the **one real reason** and tell them the fix — not a list of maybes. Almost every case is one of five things, and the run log tells you which.

**Read first:** [`knowledge/automation-method.md`](../../knowledge/automation-method.md) §8 (reading the run log) — this skill is that ladder, automated.

## Step 1 — Identify which automation

Get the automation id or a distinctive bit of its name. If the operator is vague ("my lead automation"), run `/audit-my-automations` first to list them, or ask which one.

## Step 2 — Fetch the diagnostic bundle

```bash
python ~/.claude/bos-run.py why-didnt-it-fire "<automation id or name fragment>"
```

Returns the automation's structure (enabled, triggers, conditions, actions, dedup/cap), its recent runs with full status + error detail, and a computed `likely_reason`. If the name matches several automations it'll ask you to use the id.

## Step 3 — Walk the ladder (the script's `likely_reason` is your headline)

Confirm the reason against the data, then explain it plainly. The five rungs:

**1. `DISABLED`** — it's switched off. → "It's staged, not live. Want me to test it and switch it on?" (test first — never enable blind).

**2. `NO_RUNS` (trigger never matched)** — enabled but zero run rows. The trigger doesn't match how the event actually arrives. The usual culprits:
   - **Website form mistaken for `form_completed`.** A form on the customer's own site posts in as a **webhook**, not `form_completed` (which is only for internal TrustPager forms sent via `send_form`). This is the single most common one. → switch the trigger to `webhook_received`, or add a webhook trigger.
   - **Wrong source** — bound to one specific form/agent/number when the events come from a different one (or should be "any").
   - **Genuinely no events yet** — nothing has happened to fire it. Confirm an event actually occurred in the window.
   Show the configured triggers from the bundle and ask: "is this how the event really comes in?"

**3. `SKIPPED` (a condition blocked it)** — runs exist but the latest is `skipped`. A condition didn't pass, so actions never ran (this is the system working as designed, not a bug). → show the `conditions` and walk through which field likely failed against the event data. Often the condition is stricter than the operator remembers, or references a field that's blank for that trigger.

**4. `FAILED` (an action errored)** — read `error_message` / `error_details` on the latest run and name the failing action. Common: a `{{variable}}` that doesn't exist for that trigger (renders blank / breaks), a missing integration, a bad recipient. → fix the action's config; re-test with `execute_automation_action`.

**5. `COMPLETED` (it DID fire)** — the automation ran fine; the surprise is in the *outcome*. → the issue is what an action did: a blank variable in an email, the wrong recipient field, the wrong stage. Inspect the actions and the run's action counts, not the trigger.

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

Then offer the concrete fix:
- Enable (after a test) → `/automate-this` rails, or `enable_automation`
- Add/fix a trigger → `add_automation_trigger` / point it at the right source
- Loosen a condition → `update_automation(conditions=…)`
- Fix an action → `update_automation_action` then `execute_automation_action` to re-test

## What to never do

- ❌ Don't give a list of five maybes — find the ONE reason from the run log and lead with it.
- ❌ Don't call `skipped` a failure — it's conditions doing their job. Explain it as "a condition blocked it", not "it broke".
- ❌ Don't re-enable or re-fire anything to "test" against a real customer — use `execute_automation_action` with sample data, or a test workspace.
- ❌ Don't guess at conditions/triggers — read them from the bundle and quote them back.

## Output shape

One sentence: which automation + the single reason. Then a short plain-English "here's why", then the concrete fix offered as a yes/no action.

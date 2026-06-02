---
name: automate-this
description: Describe a repetitive task you'd like to stop doing manually. The skill builds the TrustPager automation that does it for you — trigger(s), conditions, actions, the lot. Handles multiple entry points (one automation, several triggers) and knows when something is really a multi-step sequence.
triggers:
  - automate this
  - automate that
  - I keep doing this manually
  - set up an automation
  - build an automation
  - every time X happens, do Y
  - I want an automation that
  - can you automate
  - what should I automate
---

# /automate-this

You shouldn't be doing the same thing twice. This skill turns "every time a lead comes in I tag them and email them within 5 minutes" into an actual TrustPager automation that does it forever.

**Read first:** [`knowledge/automation-method.md`](../../knowledge/automation-method.md) — the mental model (trigger → conditions → actions), multiple-triggers OR-match, the automation-vs-queue distinction, and the test-before-enable rails. This skill assumes it. If the operator asks "what *should* I automate?", pull from [`knowledge/automation-recipes.md`](../../knowledge/automation-recipes.md).

## Step 1 — Understand the rule

Get the operator to phrase it as **"WHEN X happens, DO Y"** — explicitly. Then break it down:

- **WHEN — the trigger(s).** What event starts it? A form submission, an opportunity reaching a stage, a new contact, an inbound SMS, a missed call, a paid invoice, a schedule?
  - **Ask about entry points:** *"Can this start more than one way — say a TrustPager form AND your website's form?"* If yes, that's **one automation with multiple triggers** (OR-match), not two automations. This is high-leverage and operators rarely know it exists. (Method §1.1.)
- **CONDITIONS — does it run every time, or only sometimes?** ("only quote requests", "only when value > $5k", "only for contacts with no existing opportunity"). All conditions must pass (AND); a failed condition makes the run `skipped`, not fired. (Method §2.)
- **DO — the actions, in order.** Tag, email, SMS, create task, move stage, create opportunity, call a webhook, notify someone. **Order matters** — "create opp" before "tag the opp". (Method §3.)

If they gave only "DO Y" with no "WHEN", ask: *"What should kick this off — a new lead arriving, a stage being reached, a schedule?"*

**Fork early — is this actually a sequence?** If the answer is "send a series of emails over several days" (Day 0 welcome, Day 3 value, Day 7 ask), that's an **auto queue**, not an automation. Hand off: *"That's a nurture sequence — `/design-nurture-sequence` is the right tool, want me to switch to that?"* (Method §4.) One-shot reaction = stay here.

## Step 2 — Map to the TrustPager primitives

Run the discovery bundle once:

```
python skills/automate-this/fetch.py
```

This returns `available_triggers`, `available_action_types`, and `existing_automations` in one call — replaces 3+ separate MCP discovery calls.

From the returned JSON:
- **Find the trigger(s)** matching each WHEN. For the chosen trigger's full payload + `{{variable}}` tokens, call `mcp__trustpager__get_trigger_schema(trigger_type)` — you need this to confirm any variable you'll use in an email/SMS body actually exists for that trigger.
- **Find the action types** matching the DO steps. For **each one**, call `mcp__trustpager__describe_action_type(action_type)` right before you write it — get the exact config schema, example, and warnings. Don't guess config shapes.
- **Check `existing_automations` for overlap.** If there's already an automation on the same trigger doing similar work, flag it before proceeding — and if it's the *same actions from a new entry point*, the right move may be **adding a trigger to the existing automation**, not building a new one.

If the operator wants something TrustPager can't do (no matching action):
> "TrustPager doesn't have an action for [X] yet. Closest options are [a] or [b]. Or I can file a feature request — `/make-it-happen file a feature request`."

Don't fake a missing action with a fragile `call_webhook` unless they explicitly want that.

## Step 3 — Build the spec for approval

Show a plain-English summary BEFORE creating anything. For multiple triggers, list them all under WHEN:

```
**New automation: "Inbound Lead Intake"**

WHEN (fires if ANY of these happen):
  • Form submission received — "Client Intake" form
  • Website webhook received — "Contact form" endpoint

ONLY IF:
  • Contact has no existing opportunity

THEN (in order):
  1. Create opportunity in "Inbound" pipeline, "New" stage
  2. Add tag "new-lead"
  3. Send email "Acknowledgement" within 2 minutes
  4. Create task "Qualify lead" due today

SAFETY: dedup ON (60 min) · disabled until we've tested it

Look right? Or anything to change?
```

WAIT for explicit go.

## Step 4 — Create the automation

Step-by-step, with progress. **Build it disabled, test, then enable.**

1. **`mcp__trustpager__create_automation`** — name, description, primary `trigger_type`, and (preferred) an inline `triggers: [...]` array for all triggers at once. Each trigger entry can carry its **own** `trigger_type` + `source_type`/`source_id` (that's what makes OR-match across different event classes work). Set `dedup_enabled` / `dedup_window_minutes` and, for anything with a `call_webhook` or a feedback path, `max_executions_per_day`. Leave `enabled` false.
2. **`mcp__trustpager__add_automation_action`** for each action — **in the order they should run**. (Or inline an `actions: [...]` array on create.)
3. **`mcp__trustpager__add_automation_trigger`** for any extra triggers not added inline — each with its own `trigger_type`/source.
4. **TEST IT.** `mcp__trustpager__execute_automation_action` against sample data for the key actions — confirm emails render with variables resolved, tags apply, webhooks post the right body. Never point a test send at a real customer; use the operator's own monitored inbox/number.
5. **If the test looks right:** `mcp__trustpager__enable_automation`. If not: report what was off and ask how to adjust — don't enable hopefully.

ALWAYS test before enabling. Disabled automations are safe; enabled ones run for real, send real messages, and spend credits.

## Step 5 — Confirm + provide controls

Tell the operator:
- Whether it's **live** or **staged** (not yet enabled).
- The URL: `https://app.trustpager.com/auto/automations/<id>`
- How to pause/edit it, and that each trigger can be edited (templates/agents in a modal, webhooks on the webhook page).
- Offer: *"Want me to check the first few runs tomorrow to confirm it's firing right?"* — and if anything misbehaves, `/why-didnt-it-fire` diagnoses it.

## Important behaviours

- **Test before enable.** ALWAYS.
- **One automation per invocation.** Don't bundle two unrelated rules into one chain.
- **Same actions, multiple entry points → ONE automation with multiple triggers.** Different actions per entry point → separate automations. If you'd copy-paste the action chain, you want multi-trigger. (Method §1.1.)
- **Don't silently reuse another automation's trigger.** If a new rule shares a trigger with an existing automation but does *different* work, it gets its own automation. Editing an existing automation's actions is `/make-it-happen edit automation X`.
- **Action ordering is load-bearing.** "Create opp" then "tag the opp" — never the reverse. Walk the order with the operator.
- **Variables.** Confirm `{{contact.first_name}}` etc. exist for the chosen trigger via `get_trigger_schema` before using them, or they render blank.
- **Set the safety dials.** Dedup on anything that sends; `max_executions_per_day` on anything with a webhook or feedback loop. (Method §6.)
- **Stage automations are different.** A `stage_changed` rule binds to a stage via `stage_id` — use `create_stage_automation` / the pipeline page, not a trigger row. (Method §1.2.)
- **A timed series is a queue.** Hand off to `/design-nurture-sequence`. (Method §4.)

## Output shape

"Created automation '{name}' (id: {id}) with {N} trigger(s). Currently {enabled/staged}. View at https://app.trustpager.com/auto/automations/{id}."

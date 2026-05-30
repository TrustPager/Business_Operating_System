---
name: automate-this
description: Describe a repetitive task you'd like to stop doing manually. The skill builds the TrustPager automation that does it for you — trigger, conditions, actions, the lot.
triggers:
  - automate this
  - automate that
  - I keep doing this manually
  - set up an automation
  - build an automation
  - every time X happens, do Y
  - I want an automation that
  - can you automate
---

# /automate-this

You shouldn't be doing the same thing twice. This skill turns "every time a lead comes in from the website I tag them and email them within 5 minutes" into an actual TrustPager automation that does it forever.

## Step 1 — Understand the rule

Ask the user to phrase it as "WHEN X happens, DO Y" — explicitly.

Then break it down:
- **WHEN (the trigger)** — what event starts the automation? (form submission, opportunity stage changed, contact created, scheduled time, etc.)
- **CONDITIONS** — does it run for ALL of those events, or only some? ("only when the form is 'Quote request'", "only when the value > $5k", "only for contacts with no existing opportunity")
- **DO (the actions)** — what should happen? (add tag, send email, create task, move stage, notify someone, create child opp, etc.)

If the user said only "DO Y" without "WHEN", ask:
> "What needs to happen for this to fire? A new lead arriving? A specific stage being reached? On a schedule?"

## Step 2 — Map to the TrustPager primitives

Before this step, run once:

```
python skills/automate-this/fetch.py
```

This returns `available_triggers`, `available_action_types`, and `existing_automations` in a single call — replaces 3+ separate MCP discovery calls.

From the returned JSON:
- Find the trigger matching WHEN. (For the chosen trigger's full payload + variables, you may still need `mcp__trustpager__get_trigger_schema(trigger_type)` if the bundle didn't include the variable tokens.)
- Find the action types matching the DO steps. For each, use `mcp__trustpager__describe_action_type(action_type)` to see its config schema before writing it.
- Check `existing_automations` for overlap — if the workspace already has an automation for the same trigger doing similar work, flag this to the user before proceeding.

If the user wants something TrustPager can't do (action doesn't exist):
> "TrustPager doesn't have an action for [X] yet. Closest options are [a] or [b]. Or I can file a feature request with the team — `/make-it-happen file a feature request`."

## Step 3 — Build the spec for approval

Show the user a plain-English summary BEFORE creating anything:

```
**New automation: "Hot Quote Requests"**

WHEN:
  Form submission received (form: "Quote request form")

ONLY IF:
  - Contact has no existing opportunity
  - Form field "loan_size" > 250000

THEN:
  1. Create opportunity in "Inbound" pipeline, "New leads" stage
  2. Add tag "hot-quote-request" to the contact
  3. Send email using template "Quote acknowledgement" within 2 minutes
  4. Notify @simon via internal note on the opp

Look right? Or anything to change?
```

WAIT for explicit go.

## Step 4 — Create the automation

Step-by-step, with progress:
1. `mcp__trustpager__create_automation` with the chosen trigger
2. `mcp__trustpager__add_automation_action` for each action — ORDER MATTERS, add in the order they should run
3. (Optional) `mcp__trustpager__add_automation_trigger` for additional triggers if the user wants multiple
4. Test it: `mcp__trustpager__execute_automation_action` against a sample event, see if it produces the expected output
5. If the test looks right: `mcp__trustpager__enable_automation`. If not: report and ask the user how to adjust.

ALWAYS test before enabling. Disabled automations are safe; enabled ones run for real.

## Step 5 — Confirm + provide controls

Tell the user:
- The automation is live (or staged, if not enabled yet)
- The URL to view it: `https://app.trustpager.com/auto/automations/<id>`
- How to pause or edit it
- That you'll show its first 3 runs when they happen (offer: "want me to check back in a day to confirm it's firing right?")

## Important behaviours

- **Test before enable.** ALWAYS.
- **One automation per /automate-this invocation.** Don't bundle two unrelated rules into one chain.
- **Don't reuse other automations' triggers.** If the user already has a "form submission → email" automation, the new "form submission → tag" automation gets its OWN trigger config. Editing existing automations is `/make-it-happen edit automation X`, not this skill.
- **Action ordering is load-bearing.** A "create opp" then "tag the new opp" is fine. A "tag the new opp" then "create opp" will fail. Walk through the order with the user.
- **Variables.** When using `{{contact.first_name}}` etc. in email/SMS actions, confirm with `get_trigger_schema` that the variable exists for the chosen trigger.

## Output shape

"Created automation '{name}' (id: {id}). Currently {enabled/staged}. View at https://app.trustpager.com/auto/automations/{id}."

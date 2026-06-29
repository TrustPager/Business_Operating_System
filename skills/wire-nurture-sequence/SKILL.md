---
name: Wire Nurture Sequence
description: Take an approved set of nurture-sequence drafts and push them into a live TrustPager auto queue — updating existing automation actions, adding new ones for stage-movers that are silent, and inserting new queue steps with the correct step_order shuffle.
triggers:
  - wire the nurture sequence
  - push the drafts into the auto queue
  - deploy the nurture emails
  - apply the nurture sequence
  - write the sequence to TrustPager
function_slot: comms
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__update_automation_action
  - mcp__trustpager__add_automation_action
  - mcp__trustpager__create_automation
  - mcp__trustpager__add_auto_queue_step
  - mcp__trustpager__update_auto_queue_step
status: active
---

# Wire Nurture Sequence

You're pushing approved nurture-sequence drafts into a live TrustPager
auto queue. The drafts came from `design-nurture-sequence` (or were
already approved another way). Your job is to wire them into TrustPager
without breaking anything.

The source of truth for the method is
[`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md)
— read its "Wiring the sequence into a TrustPager auto queue" section
before starting.

## Hard prerequisites

Before running ANY MCP write, you need:

1. **The auto queue ID** + its current state (steps, step_orders,
   delays, linked automation IDs). Run:
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/tools/dump-crm-bundle.py" --resources auto_queues
   ```
   Then read `auto_queues.json` for the target queue.

2. **For each step in the sequence**: the matching automation ID +
   action ID, OR the confirmation that no action exists yet (then
   you'll ADD instead of UPDATE).

3. **The canonical email config to copy verbatim** for every action:
   - `sender_mode: company`
   - `email_config_id: <operator's mail config id>`
   - `recipient_target: contact`
   - `bcc: ["<operator's email>"]`
   These come from an existing approved Day 0 / template email — DON'T
   guess. Read one live action first to copy the exact shape.

4. **Approved subject + body** for every step. Don't draft new copy in
   this skill — that's `design-nurture-sequence`'s job. If the operator
   asks you to write a body here, redirect.

## Step 1 — Inventory the current state

For each stage-mover automation in the queue, classify:

- **UPDATE** — automation already has a `send_gmail_email` action that
  needs to be rewritten. Use `update_automation_action`.
- **ADD** — automation has no email action yet (silent). Use
  `add_automation_action` to create a new one.
- **CREATE** — there's a missing step entirely (e.g. Day 0 in a queue
  that starts at Day 2). Use `create_automation` to build the automation,
  then `add_auto_queue_step` to wire it into the queue.

Present this inventory as a table:

| Day | Auto queue step ID | Automation ID | Action ID | UPDATE / ADD / CREATE |
|---|---|---|---|---|
| 0 | (none yet) | (will create) | — | CREATE |
| 2 | ... | ... | ... | UPDATE |
| ... | | | | |

Wait for the operator to confirm the inventory before any writes.

## Step 2 — Fire the writes

### Common settings template

Every `send_gmail_email` config you write or update uses the same shape
(only subject + body differ per step):

```json
{
  "bcc": ["operator@example.com"],
  "body": "<p>Hi {{contact.first_name}},</p>...",
  "subject": "...",
  "sender_mode": "company",
  "email_config_id": "c3e8f7d4-...",
  "recipient_target": "contact"
}
```

### UPDATE existing actions

```
mcp__trustpager__update_automation_action(
  automation_id, action_id, config={…above shape…}
)
```

Can be fired in parallel — different action_ids don't conflict.

### ADD new actions to silent stage-movers

```
mcp__trustpager__add_automation_action(
  automation_id,
  action_type="send_gmail_email",
  sequence=1,
  config={…above shape…}
)
```

Can be fired in parallel.

### CREATE a missing automation (e.g. inserting a Day 0)

```
mcp__trustpager__create_automation(
  name="Day 0-2 Welcome",
  description="Auto queue step 1 — Day 0 welcome email. Fires immediately on enrollment.",
  trigger_type="manual",
  enabled=true,
  actions=[{
    "action_type": "send_gmail_email",
    "config": {…above shape…}
  }]
)
```

Then add it as a queue step (see below).

### Adding the new step at position 1 — THE REVERSE-ORDER SHUFFLE

This is the critical-correctness section. Read carefully.

If the new step goes at the END (step_order = N+1 for a queue that
currently has N steps), it's trivial — just call `add_auto_queue_step`.

If the new step goes at the BEGINNING (step_order=1) or in the MIDDLE,
existing step_orders need to bump up. Do this in REVERSE ORDER so no
two steps ever share the same step_order during the operation:

```
For inserting at step_order=1 in a queue of N steps:
  1. Update step at step_order=N → step_order=N+1
  2. Update step at step_order=N-1 → step_order=N
  3. ... continue down to ...
  N. Update step at step_order=1 → step_order=2
  N+1. ADD the new step with step_order=1
```

All `update_auto_queue_step` calls in the bump phase can be fired in
parallel — they touch different rows. But the `add_auto_queue_step` for
the new entry must wait until ALL bumps are confirmed.

```
mcp__trustpager__add_auto_queue_step(
  queue_id,
  automation_id=<new>,
  step_order=1,
  delay_days=0,   delay_hours=0,   delay_minutes=0,
  description="Day 0 — Welcome email (fires immediately on enrollment)",
  is_active=true
)
```

### CRITICAL — `delay_days` is CUMULATIVE from enrolment (Day N), not "+N from the previous step"

The platform schedules every step as `enrolment_time + delay_days` — so the
value you store IS the absolute day number, not the gap since the last step.

| Intended cadence | CORRECT `delay_days` per step | WRONG (collapses) |
|---|---|---|
| Day 0, 2, 4, 6, 8, 10, 12 | `0, 2, 4, 6, 8, 10, 12` | `0, 2, 2, 2, 2, 2, 2` |
| Day 0, 7, 14, 21 | `0, 7, 14, 21` | `0, 7, 7, 7` |

If you store the per-step gap (the WRONG column above), every step after the
first resolves to the same fire time, and the contact gets the whole sequence
in one burst. **Two steps with the same total delay now hard-block enrolment** —
so a flat-delay queue silently stops enrolling anyone. Always store the running
total. Worked non-zero example (the Day-4 step of a 2-day-cadence drip):

```
mcp__trustpager__add_auto_queue_step(
  queue_id,
  automation_id=<step_3_automation>,
  step_order=3,
  delay_days=4,   delay_hours=0,   delay_minutes=0,   # Day 4 = cumulative, NOT 2
  description="Day 4 — Pipeline mastery",
  is_active=true
)
```

**Editing a delay does NOT reschedule already-enrolled contacts** — they keep
the schedule snapshotted at their enrolment. To fix in-flight enrollees you must
reschedule their `automation_timer_tasks` rows directly (or unenrol + re-enrol).

## Step 3 — Verify

After all writes:

```bash
python "${CLAUDE_PLUGIN_ROOT}/tools/dump-crm-bundle.py" --resources auto_queues
```

Read the new `auto_queues.json` and confirm:

1. **All steps are in step_order sequence** (1, 2, 3, ..., N with no
   gaps or duplicates).
2. **Each step points at the correct automation.**
3. **Each automation has exactly one `send_gmail_email` action with the
   approved subject + body.**

If any of these fail, REVERT before reporting success. The operator
needs to trust the wiring.

## Step 4 — Report

Present a clean summary table:

| # | Day | `delay_days` (cumulative) | Automation | Email subject |
|---|---|---|---|---|
| 1 | 0 | 0 (immediate) | ... | ... |
| 2 | 2 | 2 | ... | ... |
| 3 | 4 | 4 | ... | ... |
| ... | | | | |

The `delay_days` column must match the Day column exactly (cumulative), and must
strictly increase down the table. If two rows share a `delay_days` value, STOP —
the queue will burst / block on enrolment.

Plus a single line linking to the queue:
`https://app.trustpager.com/auto/queues/<queue_id>`

And a recommended next step:
*"Hit Send Test Email on each automation to verify the sender alias
and signature both work."*

## Hard rules

- **Read the live state first.** Never write based on an old snapshot.
- **Reverse-order step_order shuffles.** Forward-order risks transient
  step_order collisions.
- **One email action per automation.** If an automation already has a
  `send_gmail_email` action, UPDATE it — don't add a second one.
- **Don't write new copy in this skill.** Drafts come from
  `design-nurture-sequence`. If asked to write new copy, redirect.
- **Verify after every batch of writes.** Trust but verify.
- **If anything fails, REVERT.** A half-wired sequence is worse than
  no sequence.

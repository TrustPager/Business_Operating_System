---
name: Delegate This Work
description: Hand a piece of work to a specific team member so it doesn't fall through the cracks. Creates the task assigned to that person in TrustPager, notifies them with the link, sets a manager follow-up on the due date to verify it's done, and journals who-assigned-what-to-whom. Use whenever a manager wants to delegate a task, prep job, or follow-up to someone by name.
triggers:
  - delegate this
  - assign this to
  - hand this to
  - give this to sarah
  - delegate this work
  - assign the prep to
function_slot: people
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__create_task
status: active
---

# Delegate This Work

Team-run businesses live on delegation that lands and gets followed up. This
skill turns "Sarah should prep the Acme demo by Friday" into an assigned task,
a notification to Sarah, and a reminder to the manager to check it.

## Step 1 — Confirm the four things

You need: **what** (the work, one clear sentence), **who** (a person), **when**
(due date), **priority**. If any is missing from the operator's ask, get it in
one short question.

Resolve **who** against `templates/team-standards.md` section 5 (team members)
and the workspace's users. If the name is ambiguous or not on the team, ask which
person (don't guess an assignee). Confirm you have their user id / email.

## Step 2 — Check the operator may delegate to that person

Read the operator's role and the role table in `templates/team-standards.md`
section 3. A manager/owner/ops may delegate freely. If the operator's role
doesn't permit assigning work to others, say so and stop.

## Step 3 — Create the assigned task

Create the task in TrustPager assigned to that person, linked to the relevant
opportunity/contact if there is one:

- Use `create_task` with the title (the work), `assigned_to` = the person's user
  id, `due_date`, `priority`, and `opportunity_id`/`contact_id` if relevant.
- If a write returns HTTP 202 (queued for approval), surface the approval link
  and stop (see `knowledge/safeguards.md`); don't route around it.

## Step 4 — Notify the person + set a manager follow-up

- Notify the assignee: a short SMS or email (their choice of channel, or the
  team default) with the task and a link. Keep it in the team voice
  (`knowledge/communication-voice.md`): one line, what + when + the link. This is
  internal-to-team, so it can be brief, but it's still a real send — confirm
  before sending and respect approval gates.
- Create a **manager follow-up task** due on the same date: "Verify: <work> (assigned
  to <person>)", assigned to the manager. This is the bit that stops delegations
  vanishing.

## Step 5 — Journal + confirm

The write journal already records the task creation. Show the operator a tight
confirmation:

```
✓ Delegated: "Prep the Acme demo" → Sarah Lee, due Fri 20 Jun (high)
  • Task created + assigned (linked to opp "Acme 50k")
  • Sarah notified by SMS with the link
  • Your follow-up to verify is set for Fri 20 Jun
```

## Hard rules
- ❌ Don't guess an assignee — resolve to a real team member or ask.
- ❌ Don't skip the manager follow-up; it's the point of the skill.
- ❌ Don't route around an approval gate (202 = queued, surface it).
- ✅ Notify in the team voice; confirm before any send.
- ✅ Link the task to the opportunity/contact when there is one, so it shows on the record.

## Output shape
A 3-5 line confirmation: what was delegated, to whom, due/priority, that they
were notified, and that the manager follow-up is set. If anything queued for
approval, name what to approve instead.

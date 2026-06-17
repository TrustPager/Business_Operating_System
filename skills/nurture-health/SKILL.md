---
name: Nurture Health
description: Health-check the operator's live nurture sequences — for every auto queue, show the enrolment funnel (enrolled → active → completed → cancelled), which step is leaking the most people, per-step open/click rates where available, and whether the un-enrol side is firing. Closes the loop that design + wire leave open.
triggers:
  - nurture health
  - how is my sequence performing
  - how is the nurture sequence doing
  - is my drip working
  - which step is leaking
  - check my auto queue
  - auto queue health
  - sequence performance
  - is my reawakening campaign working
---

# Nurture Health

`design-nurture-sequence` drafts it, `wire-nurture-sequence` ships it — and then
nobody looks again. This skill is the part that was missing: it tells the
operator whether the sequence is actually working, which step is bleeding
people, and whether the machine's un-enrol side is firing so booked/dead leads
stop getting drip emails.

It pairs with the re-engagement machine in
[`knowledge/automation-recipes.md`](../../knowledge/automation-recipes.md) (R19/R20)
— that section explains what a healthy multi-channel queue looks like.

## Step 1 — Pull the data (MCP calls)

All reads, on the `trustpager` MCP server. Start with the queue list and an email-log sample in parallel, then drill into each queue:

| Need | Tool | Args |
|---|---|---|
| Every auto queue | `list_auto_queues` | `limit: 100` |
| Recent email logs (for engagement) | `list_email_logs` | `limit: 100` (sample a few hundred recent) |
| Each queue's steps + linked automation ids | `get_auto_queue` | `id: <queue_id>` |
| Each queue's enrolment funnel | `list_auto_queue_enrollments` | `queue_id: <queue_id>`, `limit: 100` (page, cap ~5 pages so a huge queue can't run away) |

Scope to a single queue if the operator names one. Everything here is read-only — nothing is journaled or needs approval.

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

**Best-effort by design:** enrolment and email-log endpoints vary in shape by workspace and API version. If a queue's enrolments aren't reachable, treat that queue as **step-only** (you still have the funnel structure) and tell the operator plainly what's measured vs unavailable. Don't bail on the whole health-check because one queue degrades.

## Step 2 — Compute the funnel and per-step drop-off

For each queue:

- **Steps** — read the ordered step list off the queue detail (sort by step order). Each step carries a `delay` (days/hours/minutes) and an `automation_id`. Build a day-label per step: use the step description if present, else `+Nd Nh Nm` from the delays (`0` delays = "immediate").
- **Enrolment funnel** — from the enrolment statuses, count: `enrolled` (total), `active`, `completed`, `cancelled` (count `cancelled` + `removed`). `completion_rate = completed / enrolled`.
- **Per-step reached counts** — for each enrolment, read how far it progressed (last completed / current step order). A step is "reached" by an enrolment if that enrolment's progress ≥ the step's order. Count reached enrolments per step.
- **Leak step** — walking steps in order, the drop after a step = `reached(prev) − reached(this)` when that's positive. The step with the **biggest single drop** is the queue's leak step.
- **Engagement per step** — bucket the sampled email logs by `automation_id` into `{sends, opens, clicks}` (an open = any `opened_at`/open count > 0; a click = any `clicked_at`/click count > 0). For each step, match its `automation_id` to a bucket → `open_rate = opens/sends`, `click_rate = clicks/sends`. If the email logs don't carry an `automation_id` in this workspace, engagement is **unavailable** — say so, don't fake rates.

**Headline across all queues:** total active, total completed, total cancelled, and the single biggest leak (queue + step + how many lost).

## Step 3 — Present, worst leak first

Lead with the single biggest leak across all queues, then go queue by queue.
Never dump raw step arrays — translate them into a funnel the operator reads in
ten seconds.

```
📉 BIGGEST LEAK: "Reawakening Sequence" loses 48 people at Day 7 (step 2).
   174 enrolled → 126 made it to Day 7. That's where to look first.

♻️ Reawakening Sequence  (active)
   Funnel: 174 enrolled → 120 active · 30 completed (17%) · 24 cancelled
   Steps:
     Day 0   174 reached   open 62%  click 18%
     Day 7   126 reached   open 41%  click 7%   ← 48 dropped here
     Day 14   118 reached   open 38%  click 6%
     ...
   ✅ Un-enrol firing: 24 cancelled means booked/dead leads are leaving the drip.

📨 Onboarding Sequence  (active)
   Funnel: 90 enrolled → 60 active · 22 completed (24%) · 8 cancelled
   ...

⚠️ Couldn't measure: open/click rates (email logs don't link to automations in
   this workspace) — funnel + drop-off are exact, engagement is unavailable.
```

### How to read each signal

| Signal | What it means | What to offer |
|---|---|---|
| Big drop at one step | that email is where people fall off | review that step's copy — hand to `/design-nurture-sequence`; lint it with `/lint-nurture-sequence` |
| `open_rate` low at a step | subject isn't landing (or deliverability) | rework the subject; check the sender/test-send |
| `click_rate` low but open ok | the body/CTA isn't pulling | the CTA-above-the-image / single-CTA rules — run the linter |
| `completion_rate` very low | sequence too long, or leak early | shorten, or fix the early leak first |
| `cancelled` is 0 on a campaign with a "Remove" stage | the **un-enrol automation isn't firing** — booked/dead leads still get drip | check stage automation B (R19); hand to `/why-didnt-it-fire` |
| `active` piling up, few completing | people stalled mid-sequence | check step delays + that later steps have email actions wired |

## Step 4 — Point at the fix, don't auto-fix

This is a read/diagnose skill. For the fixes it surfaces, hand off:
- Leaky/weak copy → `/design-nurture-sequence` (rewrite), then `/wire-nurture-sequence`.
- Style/consistency problems → `/lint-nurture-sequence`.
- Un-enrol not firing / a step never sends → `/why-didnt-it-fire`, then `/automate-this`.

Don't edit queue steps or automations from this skill.

## What to never do

- ❌ Don't present queues as a flat list — lead with the biggest leak, then per queue.
- ❌ Don't report open/click rates as exact when the email logs don't link to automations — say "estimated" or "unavailable".
- ❌ Don't call a queue "broken" because completion is low — low completion can be a long sequence working as designed. Flag the *leak step*, not the headline rate.
- ❌ Don't write to any queue or automation here.

## Output shape

Open with the single biggest leak (queue + step + how many lost). Then one
compact funnel block per queue. Then any "couldn't measure" line. Close with the
one step most worth fixing first and the skill to hand it to.

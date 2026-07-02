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
function_slot: comms
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__list_auto_queues
  - mcp__get_auto_queue
  - mcp__get_auto_queue_board
  - mcp__list_auto_queue_enrollments
  - mcp__list_email_logs
status: active
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

## Step 1 — Fetch the health digest

```bash
python ~/.claude/bos-run.py nurture-health
```

One run: lists every auto queue, pulls each one's steps + enrolment funnel +
per-step drop-off, and (where the email-log endpoint exposes `automation_id`)
open/click rates per step. Scope to one queue with `--queue <id>`.

This fetcher is **best-effort by design** — queue / enrolment / email-log
endpoints vary by workspace and API version. Anything it can't reach lands in
`warnings` and `_sources`, and it still returns everything else. Read those two
fields and tell the operator plainly what's measured vs estimated.

**Fallback if the script can't run at all** (auth/network): drive it by hand —
`list_auto_queues` → `get_auto_queue` (steps) → `get_auto_queue_board` (per-step
buckets) → `list_auto_queue_enrollments` (status mix) → `list_email_logs`
(engagement). That's many calls; prefer the script.

## Step 2 — Present, worst leak first

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
| Big `dropped_after` at one step | that email is where people fall off | review that step's copy — hand to `/design-nurture-sequence`; lint it with `/lint-nurture-sequence` |
| `open_rate` low at a step | subject isn't landing (or deliverability) | rework the subject; check the sender/test-send |
| `click_rate` low but open ok | the body/CTA isn't pulling | the CTA-above-the-image / single-CTA rules — run the linter |
| `completion_rate` very low | sequence too long, or leak early | shorten, or fix the early leak first |
| `cancelled` is 0 on a campaign with a "Remove" stage | the **un-enrol automation isn't firing** — booked/dead leads still get drip | check stage automation B (R19); hand to `/why-didnt-it-fire` |
| `active` piling up, few completing | people stalled mid-sequence | check step delays + that later steps have email actions wired |

### The verdict layer (what the numbers mean for the business)

Read each queue against the doctrine lens that fits its job: an
onboarding/enrolment queue against the activation lens (`business-method.md`
§11.3 — the % reaching the first win early IS next quarter's churn,
directional); a retention sequence against the ceiling equation (§11.1 —
churn caps the business's size regardless of marketing); a lead/reawakening
sequence against the engaged-lead math (§10.3 — fix the WORST stage, not the
top). The funnel says where the leak is; the lens says what it costs.

## Step 3 — Point at the fix, don't auto-fix

This is a read/diagnose skill. For the fixes it surfaces, hand off:
- Leaky/weak copy → `/design-nurture-sequence` (rewrite), then `/wire-nurture-sequence`.
- Style/consistency problems → `/lint-nurture-sequence`.
- Un-enrol not firing / a step never sends → `/why-didnt-it-fire`, then `/automate-this`.

Don't edit queue steps or automations from this skill.

## What to never do

- ❌ Don't present queues as a flat list — lead with the biggest leak, then per queue.
- ❌ Don't report open/click rates as exact when `_sources.engagement` isn't `ok` — say "estimated" or "unavailable".
- ❌ Don't call a queue "broken" because completion is low — low completion can be a long sequence working as designed. Flag the *leak step*, not the headline rate.
- ❌ Don't write to any queue or automation here.

## Output shape

Open with the single biggest leak (queue + step + how many lost). Then one
compact funnel block per queue. Then any "couldn't measure" line from
`warnings`/`_sources`. Close with the one step most worth fixing first and the
skill to hand it to.

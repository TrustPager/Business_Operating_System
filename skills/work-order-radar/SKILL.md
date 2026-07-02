---
name: Work Order Radar
description: Show the state of every job — the count by status, which work orders have stalled in one status too long, and which completed recently (candidates for a completion update or review ask). Stalls first.
triggers:
  - work order radar
  - check my work orders
  - which jobs are stalled
  - work order status
  - what's stuck in progress
  - how are my jobs tracking
  - which work orders need attention
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__list_work_orders
  - mcp__trustpager__send_work_status
status: active
---

# Work Order Radar

Owners raise work orders and then jobs quietly stall — stuck in *In progress*
for three weeks, or *Complete* but the customer was never told. This is the
check-up on the board.

**What matters:**
- **Stalled** — a non-terminal work order that's sat in one status too long.
  Something's blocked or forgotten.
- **Recently completed** — done, but did the customer get the completion update
  (and have you asked for the review)?

Source of truth: [`knowledge/work-order-method.md`](../../knowledge/work-order-method.md)
— §3 (the lifecycle you track) and §4 (automating it).

## Step 1 — Fetch the digest

```bash
python ~/.claude/bos-run.py work-order-radar
```

One call: lists every work order, counts by status, flags stalls (sat ≥N days in
a non-terminal status) and recent completions. `--stall-days N` tunes the stall
threshold (default 14).

Fallback if it can't run: `mcp__trustpager__list_work_orders` — raw list, no
stall flags; prefer the script.

## Step 2 — Present, stalls first

```
🔧 31 work orders — 18 complete, 9 in progress, 3 scheduled, 1 on hold

🛑 STALLED (4)  ← sitting too long, likely blocked
  → "Kitchen reno — Patel" — In progress 23d. → check in / update status
  → "Fit-out — Vertex" — On hold 19d, nobody's revisited. → unblock or close

✅ COMPLETED THIS WEEK (5)  ← did the customer get told?
  → "Service — Northside" — complete 2d ago. → send completion update + ask for a review

📊 By status: In progress 9 · Scheduled 3 · On hold 1 · Complete 18
```

## Step 3 — Offer the next actions (with approval)

One at a time, with a yes:
- **Send a status update** to the customer on a stalled or just-completed job →
  `mcp__trustpager__send_work_status(deal_id, recipient_email, recipient_name)`.
  Real recipients only; confirm first.
- **Move a stalled work order's status** (if the operator says it's actually
  progressed) → `update_work_order(work_order_id, ...)`.
- **Draft a customer check-in** for a stalled job → hand to `/draft-reply`.

When suggesting the review ask on a completed job, shape it per
`business-method.md` §10.5 tier 2: ask at the moment of demonstrated
satisfaction (the completion update, while the finished work is fresh), by the
person who did the work, with a direct link to leave the review.

For "ask for a review automatically when a job completes" or "ping me when the
customer opens their portal", hand to `/automate-this` (`work_order_opened` and
the completion path).

## What to never do

- ❌ Don't dump all work orders flat — lead with stalls.
- ❌ Don't auto-send status updates or auto-move statuses — offer, get a yes.
- ❌ Don't flag terminal/complete jobs as stalled — they're done.
- ❌ Don't send a status update to anyone but the confirmed customer contact.

## Output shape

Headline tally, then STALLED (worst first), then COMPLETED-THIS-WEEK (with the
"did they get told?" prompt), then the by-status breakdown — and the single most
valuable action to take first.

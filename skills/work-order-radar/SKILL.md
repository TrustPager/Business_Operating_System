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

## Step 1 — Pull the data (parallel MCP calls)

Fire these two reads in parallel in a single batch. Both reads — free, nothing journaled, no approval. Use the `trustpager` MCP server.

| Need | Tool | Args |
|---|---|---|
| Every work order | `list_work_orders` | `limit: 100` (page through until exhausted — up to ~20 pages) |
| The status labels for this workspace | `list_work_order_statuses` | — (so you know which statuses are terminal) |

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal". (Work orders carry a `deal_id` linking them to an opportunity.)

## Step 2 — Build the board + stall digest

For each work order, read its status label (it may arrive as `status`, `status_name`, `work_order_status`, or a nested object with `name`/`label` — normalise to a string) and compute **days in status** from `status_changed_at` (fall back to `updated_at`, then `created_at`).

A status is **terminal** if its label (lowercased, trimmed) is one of: `complete`, `completed`, `done`, `closed`, `cancelled`, `canceled`.

Then:
- **Count by status** — tally every work order under its status label.
- **Stalled** — a **non-terminal** work order whose days-in-status is **≥ the stall threshold (default 14 days**, adjustable if the operator asks). Capture id, name (`name` → `title` → `deal_name` → "(work order)"), linked opportunity (`deal_id`), status, days in status. **Sort stalled descending by days in status** (worst first).
- **Recently completed** — a **terminal** work order whose days-in-status is ≤ 7. These are the "did the customer get told?" candidates.

## Step 3 — Present, stalls first

```
🔧 31 work orders — 18 complete, 9 in progress, 3 scheduled, 1 on hold

🛑 STALLED (4)  ← sitting too long, likely blocked
  → "Kitchen reno — Patel" — In progress 23d. → check in / update status
  → "Fit-out — Vertex" — On hold 19d, nobody's revisited. → unblock or close

✅ COMPLETED THIS WEEK (5)  ← did the customer get told?
  → "Service — Northside" — complete 2d ago. → send completion update + ask for a review

📊 By status: In progress 9 · Scheduled 3 · On hold 1 · Complete 18
```

## Step 4 — Offer the next actions (with approval)

Anything that **writes** follows the rails in `knowledge/safeguards.md` — confirm before it lands, journal the write to `.bos-journal.md`, search-first so you don't duplicate. One at a time, with a yes:

- **Send a status update** to the customer on a stalled or just-completed job →
  `send_work_status` with `deal_id`, `recipient_email`, `recipient_name`.
  Real recipients only; confirm first. (A `202` / `approval_id` response means it's queued for human approval — surface the approval id + approvals URL, journal it as `approval_pending`, and stop; don't retry — safeguards §1.)
- **Move a stalled work order's status** (if the operator says it's actually
  progressed) → `update_work_order` with the `work_order_id` and new status.
- **Draft a customer check-in** for a stalled job → hand to `/draft-reply`.

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

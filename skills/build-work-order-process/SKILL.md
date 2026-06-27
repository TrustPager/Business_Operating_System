---
name: Build Work Order Process
description: Set up a work-order process in TrustPager — define the statuses jobs move through and the fields captured on each. Plans the board in chat for approval, then creates it via MCP. Raising individual work orders against deals comes after.
triggers:
  - set up work orders
  - build a work order process
  - define my job statuses
  - configure work order tracking
  - set up my fulfilment board
  - create work order fields
  - set up job tracking
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__list_work_order_statuses
  - mcp__trustpager__list_work_order_fields
  - mcp__trustpager__create_work_order_status
  - mcp__trustpager__reorder_work_order_statuses
  - mcp__trustpager__create_work_order_field
  - mcp__trustpager__describe_resource
  - mcp__trustpager__create_work_order
status: active
---

# Build Work Order Process

You're defining the **board** an owner's jobs move across — the statuses (Not
started → In progress → Complete) and the fields captured on each work order
(assigned tech, scheduled date, site address). Set this up once; individual work
orders then flow into it per job.

**This builds the process (statuses + fields). Raising work orders against
specific deals is a separate step** (offered at the end).

Source of truth: [`knowledge/work-order-method.md`](../../knowledge/work-order-method.md)
— read §1 (the two layers) and §5 (safety rails).

## Step 1 — Understand the workflow

Ask the operator:

1. **What stages does a job move through?** From raised to done. Keep it tight —
   4-6 statuses beats 12. (e.g. *Not started → Scheduled → In progress → On hold
   → Complete*.)
2. **What do you need to record on each job?** → custom fields (assigned person,
   scheduled date, site/address, notes, cost).
3. **Do customers see progress?** If yes, the portal + status updates matter —
   note it for the radar/automation hand-off.

## Step 2 — Read the current board + plan the changes

`mcp__trustpager__list_work_order_statuses` + `list_work_order_fields` to see
what already exists (don't duplicate). Present the planned board for approval:

```
Statuses (in order):  Not started → Scheduled → In progress → On hold → Complete
Fields:               Assigned tech (text) · Scheduled date (date) · Site address (text) · Notes (long text)
```

Wait for the operator's go.

## Step 3 — Create the statuses + fields

Once approved, build via MCP:

1. Statuses: `mcp__trustpager__create_work_order_status(...)` for each new one,
   then `reorder_work_order_statuses(...)` to set the order.
2. Fields: `create_work_order_field(...)` for each. Run `describe_resource("work_order")`
   first if unsure of a status/field payload shape — don't guess.

Narrate as you go; stop and show any error rather than pushing on.

## Step 4 — Read back + offer to raise the first work order

- `list_work_order_statuses` + `list_work_order_fields` and show the final board.
- A work order attaches to a **deal product** (§1). Offer: *"Board's set up. Want
  me to raise a work order against a job? I'll need the opportunity and which
  product line it's for (`create_work_order` attaches to a `deal_product_id`)."*
- Mention the customer side: *"Run `/work-order-radar` to track jobs and spot
  stalls. To ping yourself when a customer opens their work-order portal, that's
  `/automate-this` on the `work_order_opened` trigger."*

## Hard rules

- **Statuses + fields first; jobs second.** Define the board before raising work
  orders so they land in a meaningful shape.
- **Confirm the board before creating.**
- **Don't duplicate existing statuses/fields** — read the current board first.
- **A work order needs a deal product** to attach to (§5) — if the opportunity
  has no product line, that's added first.
- **Keep the status list tight.** 4-6 stages, not 12.

## Output shape

The current board, then the planned changes, then — after approval — a running
narration of the create calls, the read-back board, and the offer to raise the
first work order + the radar/automation hand-off.

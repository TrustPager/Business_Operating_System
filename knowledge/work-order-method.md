# Work Order Method

How to set up a work-order process in TrustPager and run it — define the
statuses + fields once, then raise work orders against a deal's products, move
them through the board, and keep the customer updated via the portal.

Source-of-truth method behind `build-work-order-process` and `work-order-radar`.

## The one-sentence model

A **work order** is a unit of work attached to a line item (a **deal product**)
on an opportunity; it moves through the **statuses** you define; the customer
can watch progress on a PIN-protected **portal**, and you push them **status
updates** along the way.

You define the statuses + fields once (the board). You raise work orders per job.

## 1. The two layers: the process, then the work orders

**Layer A — the process (set up once):**
- **Statuses** — the stages a work order moves through (e.g. *Not started →
  Scheduled → In progress → On hold → Complete*). Tools: `list_work_order_statuses`,
  `create_work_order_status`, `reorder_work_order_statuses`, `update`/`delete`.
- **Fields** — custom fields captured on each work order (e.g. *Assigned tech*,
  *Site address*, *Scheduled date*). Tools: `list_work_order_fields`,
  `create_work_order_field`, `reorder_work_order_fields`, `update`/`delete`.

**Layer B — the work orders themselves (per job):**
- **Create** — `create_work_order`, which attaches to a **`deal_product_id`** (a
  product line item on an opportunity). A work order doesn't float free; it's
  always against something the customer is buying/getting. `list_work_orders`,
  `get_work_order`, `update_work_order` (move status, set fields), `delete_work_order`.

## 2. The customer-facing portal

The customer views their work order(s) on a PIN-protected hosted page. The
moment they unlock it, `work_order_opened` fires — the same "they're engaged
right now" signal as document/form opens. `send_work_status` (needs `deal_id`,
`recipient_email`, `recipient_name`) pushes a status update to the customer.

This is what turns a back-office tracking board into a customer-experience
surface: they see the job move from *Scheduled* to *In progress* to *Complete*
without phoning to ask.

## 3. The lifecycle you track

`list_work_orders` (optionally by deal) is the board. Per work order, you watch:
- **Status** — where it is on the board. Stuck-in-one-status-too-long is the
  signal something's blocked.
- **Portal opened?** — `work_order_opened` tells you the customer is watching.
- **Status updates sent** — did the customer get told when it moved?

**Follow-up signals:** a work order sitting in *In progress* for weeks (stalled
job), a *Complete* work order whose customer was never sent the completion
update, an *On hold* nobody's revisited.

## 4. Automating it

Wire in `/automate-this`:
- `work_order_opened` — customer's looking at the portal; notify the owner, or
  trigger a "need anything?" touch.
- Status-change automations (via the opportunity/stage machinery) — e.g. when a
  work order completes, ask for a review or raise the invoice.

Tokens: `{{recipient_name}}`, `{{work_order_name}}`, `{{deal_id}}`, `{{opened_at}}`.

## 5. Safety rails

- **A work order needs a deal product to attach to.** If the opportunity has no
  product line item, there's nothing to raise a work order against — add the
  product first (or the create will have no `deal_product_id`).
- **Real recipients only** for `send_work_status` — never a test/`@example.com`
  address.
- **Don't delete a status that work orders are sitting in** — they'd be orphaned.
  Move them first, or pick a different status to retire.
- **Don't delete a work order** without naming it and getting a yes.

## 6. Discovery protocol

- `describe_resource("work_order")` — canonical tool surface + field hints.
- `list_work_order_statuses` / `list_work_order_fields` — read the current board
  shape before changing it.
- `get_trigger_schema("work_order_opened")` — exact trigger_data tokens.

## House rules

- **Define the board before raising jobs.** Statuses + fields first, then work
  orders flow into a shape that means something.
- **Work orders attach to deal products** — always against something concrete.
- **Use the portal + status updates** — the customer-facing side is the point;
  don't run it as a silent internal list.
- **Watch for stalls** — `work-order-radar` is the check-up; a job stuck in one
  status is the thing to surface.

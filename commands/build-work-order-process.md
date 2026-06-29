---
description: Set up a work-order process: define the statuses jobs move through and the fields captured on each. Plans the board in chat for approval, then creates it via MCP. Raising individual work orders comes after.
---

Run the **Build Work Order Process** skill.

Invoke the skill at `skills/build-work-order-process/SKILL.md`. Understand the
job workflow, read the current board (`list_work_order_statuses` +
`list_work_order_fields`) so you don't duplicate, plan the statuses + fields in
chat for approval, then create them via MCP (`create_work_order_status` +
`reorder_work_order_statuses`, `create_work_order_field`). Keep the status list
tight (4-6).

This builds the board. Raising a work order against a deal product
(`create_work_order`, needs a `deal_product_id`) is offered at the end. Hand off
to `/work-order-radar` and mention the `work_order_opened` automation.

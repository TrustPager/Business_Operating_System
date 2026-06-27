---
name: Add a Field
description: Add or change a custom field on the CRM records, and surface it where it's needed. Creates a text / number / date / dropdown field (e.g. broker name, settlement date, bank) in CRM settings, then optionally puts it on the opportunity card display and includes it in the relevant workspace spreadsheet — so the operator self-serves a field change end to end instead of filing a request and waiting.
triggers:
  - add a custom field
  - add a field
  - i need a new field for
  - add a dropdown for
  - add broker name as a field
  - put a field on the card
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
status: active
---

# Add a Field

Custom fields are how the CRM fits a specific business. This adds one and wires
it to where it's actually used, in one pass.

## Step 1 — Confirm the field

Get, in one short batch:
- **Name** (e.g. "Broker name", "Settlement date").
- **Type** — text, number, date, or **dropdown**. If dropdown, the **options**
  (e.g. the broker names). If a value set is small and stable, prefer a dropdown
  over free text so the data stays clean and filterable.
- **Which record** — opportunity, contact, or company.

## Step 2 — Create it in CRM settings

Add the custom field to that record's settings (CRM settings → additional
fields, via the platform's settings/custom-field tools). Use the exact name and
type confirmed. If a write returns 202 (queued for approval), surface it and stop
(`knowledge/safeguards.md`).

## Step 3 — Offer to surface it where it's used

A field nobody can see isn't much use. Offer (and do, on a yes):
- **On the opportunity card** — add it to the card display so it shows at a
  glance on the pipeline (`/settings/crm` card display).
- **In a spreadsheet** — if there's a workspace spreadsheet this field belongs in
  (e.g. settlement date → the monthly settlement sheet), add it as a column
  (hand off to `/build-spreadsheet`).

Tell the operator these two options explicitly; don't assume. A new field often
needs both to be useful.

## Step 4 — Confirm

```
✓ Added "Broker name" (dropdown: Dom, Sam, Priya) to opportunities.
  • Shown on the opportunity card ✓
  • Added to the "Monthly settlement" spreadsheet ✓
  Set it on a record and it'll flow through to both.
```

## Hard rules
- ❌ Don't guess the type or options — confirm them (a stable small set = dropdown, not text).
- ❌ Don't route around an approval gate.
- ✅ Always offer the card-display + spreadsheet surfacing; a hidden field is half-done.
- ✅ Use the exact field name everywhere so it matches across CRM, card, and spreadsheet.

## Output shape
A one-line confirmation naming the field + type (+ options), and which surfaces it
was added to (card / spreadsheet), or the offer to add it to those if the
operator hasn't said yet.

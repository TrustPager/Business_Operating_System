---
name: Wire Form
description: Wire a form template's fields to their CRM variables (so answers land on the right record) and connect the form to how it's used — sent to a contact, internal fill, or an intake automation. Makes a built form actually do something.
triggers:
  - wire my form
  - connect the form to the CRM
  - map form fields to contacts
  - hook up the intake form
  - make the form save to the right fields
  - send the form to a client
  - wire the form to an automation
function_slot: documents
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__get_form_template
  - mcp__trustpager__list_form_fields
  - mcp__trustpager__bulk_update_form_field_wiring
  - mcp__trustpager__send_form
  - mcp__trustpager__create_internal_form_submission
status: active
---

# Wire Form

A form with unwired fields is a survey — answers get captured on the submission
but never land on the contact or opportunity. This skill does the two things
that turn a built form into a working CRM process: **wire each field to a CRM
variable**, and **connect the form to how it's used**.

Source of truth: [`knowledge/form-method.md`](../../knowledge/form-method.md)
— §1 (wiring), §2 (the label rule), §3 (the three fill paths).

## Step 1 — Load the form + check the wiring

`mcp__trustpager__get_form_template(template_id)` + `list_form_fields(template_id)`.
For each field, note its current wiring target (if any). Build the mapping —
field → CRM variable — confirming with the operator where it's not obvious:

```
Field                 → wires to
Full name             → contact.full_name   ✓
Email                 → contact.email        ✓
Mobile                → contact.mobile       ✓
Business name          → company.name        ✓
What do you need?      → deal.description     ✓
Budget range           → (UNWIRED)            ← orphan — pick a home or mark display-only
```

Flag every orphan. The operator either gives it a CRM home or consciously marks
it display-only. Keep label = meaning = target (§2).

## Step 2 — Apply the wiring

Once the mapping's approved:

```
mcp__trustpager__bulk_update_form_field_wiring(template_id, wiring={ <field_id>: <crm_variable>, ... })
```

One call sets all of it. Read back with `list_form_fields` and confirm every
intended field now shows its target.

## Step 3 — Connect the form to how it's used

Pick the path the operator wants (§3):

- **Send to a named recipient** — `mcp__trustpager__send_form(template_id,
  recipient_email, recipient_name)`. Real recipients only; costs credits.
  Confirm the recipient out loud first. After sending, point at `/form-radar`.
- **Internal fill** — `create_internal_form_submission(template_id, deal_id)`
  for staff to enter the data themselves (no email).
- **Intake automation** — if inbound submissions should drive a workflow (notify,
  move stage, create task), hand to `/automate-this` on the `form_completed`
  (and/or `form_opened`) trigger. For a public *website* contact form, that's a
  `generic_webhook` trigger, NOT `form_completed` (§3) — say so.

## Step 4 — Hand off

End with: *"Wired and connected. Run `/lint-form` to confirm no field is an
orphan and the required ones are set, then `/form-radar` once submissions start
coming in."*

## Hard rules

- **No orphan fields ship silently.** Every data field is wired or consciously
  display-only.
- **Label = meaning = wiring target** (§2). Don't wire a "Summary" field to a
  precise CRM field, or vice versa.
- **Real recipients only** for `send_form`. Never a test/`@example.com` address.
- **Confirm the recipient** before any `send_form`.
- **Website forms use a webhook trigger**, not `form_completed`. Don't mis-wire.
- **If a send returns an approval gate, stop and tell the operator to approve it.**

## Output shape

The field→CRM mapping (orphans flagged) first, then — after approval — the
wiring call + read-back, then the chosen connect path, then the hand-off to
`/lint-form` + `/form-radar`.

---
name: Build Form
description: Design and create a form template in TrustPager — fields, types, and order. Plans the field list in chat for approval, then creates it via MCP. Wiring fields to CRM variables and connecting the form to an intake is the next step (wire-form).
triggers:
  - build a form
  - create a form template
  - set up an intake form
  - make an onboarding form
  - build a client questionnaire
  - turn this paper form into a TrustPager form
  - create a booking request form
---

# Build Form

You're building a reusable **form template** — an intake form, onboarding
questionnaire, consent form, booking request. You plan the fields with the
operator, then create the template.

**This builds the fields. It does NOT wire them to the CRM or send the form.**
Wiring + connecting to an intake is `wire-form`; sending is handled there too.

Source of truth: [`knowledge/form-method.md`](../../knowledge/form-method.md)
— read §1 (anatomy) and §2 (the label rule) before starting.

## Step 1 — Understand the form

Ask, unless already told:

1. **What's it for?** (new-client intake, onboarding, consent, booking…) and
   what happens to the answers.
2. **What does it need to capture?** Each piece of data → one field. Note which
   are required.
3. **Starting from a sample?** If they have a paper/PDF form or a paste, read it
   and reverse-engineer the field list rather than inventing one.
4. **Who fills it?** A client via an emailed link, or staff internally — this
   shapes tone and which fields are pre-known.

## Step 2 — Plan the field list in chat (for approval)

Present the planned fields BEFORE creating anything, and name the CRM home each
will later wire to (so `wire-form` is fast and the label rule holds — §2):

```
Form: "New Client Intake"

1. Full name        (text, required)    → contact.full_name
2. Email            (email, required)   → contact.email
3. Mobile           (phone, required)   → contact.mobile
4. Business name     (text)             → company.name
5. What do you need? (long text)        → deal.description
6. Budget range      (select)           → deal.value  (confirm: usually filled?)
```

For every field, confirm its label matches the data it captures and the record
it'll wire to. Flag any field that has no obvious CRM home — it may be an orphan
(§1). Wait for the operator's go.

## Step 3 — Create the template + fields

Once approved:

1. `mcp__trustpager__create_form_template(name=...)` → capture `template_id`.
2. For each field, `mcp__trustpager__add_form_field(template_id, type=..., label=...)`
   in order. Run `describe_resource("form")` first if unsure of a field `type`'s
   exact shape — don't guess field payloads.
3. `reorder_form_fields(template_id, field_ids=[...])` if needed.

Narrate as you add. If a field write fails, stop and show the error.

## Step 4 — Read it back + hand off to wiring

- `list_form_fields(template_id)` and show the operator the final field list.
- End with: *"Fields are built. Next, run `/wire-form` to map each field to its
  CRM variable (so the answers actually land on the record) and connect the form
  to how it's used — sent to a contact, internal fill, or an intake trigger. Then
  `/lint-form` before it ships."*

## Hard rules

- **Don't wire or send from this skill.** Building fields ≠ wiring ≠ sending.
  Redirect to `/wire-form`.
- **Confirm the field plan before creating.**
- **Label = meaning** (§2). A field's label must match the data it collects.
- **Flag orphan-prone fields** — anything with no clear CRM home — so wiring
  catches it.
- **Reuse over one-offs.** If it'll be filled more than once, it's a template.

## Output shape

The field plan first (with intended CRM homes), then — after approval — a
running narration of the create calls, then the read-back field list and the
hand-off to `/wire-form`.

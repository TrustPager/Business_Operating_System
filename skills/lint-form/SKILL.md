---
name: Lint Form
description: Pre-flight a form template before it ships — every data field wired to a CRM variable (no orphans), required fields set, labels match their wiring, no leftover placeholders. Read-only; fails first, then warnings.
triggers:
  - lint my form
  - check my form template
  - is this form ready to send
  - review my intake form
  - check the form before I send it
  - are my form fields wired
---

# Lint Form

Catch the silent form mistakes before a client fills it in and the answers
vanish: an unwired field whose answer never lands on the record, a label that
disagrees with its wiring, a missing required flag, leftover placeholder text.
Read-only — never edits; routes each fix to `/build-form` or `/wire-form`.

Source of truth: [`knowledge/form-method.md`](../../knowledge/form-method.md)
— checks map to §1 (orphans) and §2 (the label rule).

## Step 1 — Load the form

`mcp__trustpager__get_form_template(template_id)` + `list_form_fields(template_id)`.
If the operator named it by title, find it with `list_form_templates` first. If
they didn't say which, ask.

## Step 2 — Run the checks

**FAILS (fix before shipping):**
- **Orphan data field** — a field that collects real data (not a heading/display
  block) with no CRM wiring. The answer never lands on the record. → `/wire-form`
- **Label ↔ wiring mismatch** — a precise field ("Mobile") wired to the wrong
  target ("contact.email"), or a vague field ("Notes") wired to a precise CRM
  field. → fix label or wiring.
- **No fields** — empty template.
- **Broken option set** — a select/radio with zero options.

**WARNINGS (worth a look):**
- **Required not set** — a field the process clearly needs (email on an intake
  form) that isn't marked required.
- **Placeholder left in** — "Lorem ipsum", "TODO", "test field", "[label]".
- **Duplicate label** — two fields with the same label (confusing on the record
  and in the PDF).
- **File-upload with no purpose wired** — an upload field whose file isn't routed
  anywhere.

## Step 3 — Report, fails first

```
📋 "New Client Intake" — 2 fails, 1 warning

❌ FAILS (fix before shipping)
  → "Budget range" is unwired — the answer won't land on any record. → /wire-form
  → "Mobile" is wired to contact.email — label and target disagree. → /wire-form

⚠️ WORTH A LOOK
  → "Email" isn't marked required on an intake form — most should be. → /build-form
```

End with the single most important fix. If clean: *"Clean — every field's wired,
labels match, required fields set. Ready to send via `/wire-form`'s send step or
collect via intake."*

## Hard rules

- **Read-only.** Diagnose; route fixes to `/build-form` (fields) or `/wire-form`
  (wiring). Never edit here.
- **Fails before warnings.** Lead with what actually loses data.
- **An orphan data field is a FAIL** — that's the whole point of a form in a CRM.
- **Display-only fields aren't orphans** — a heading/instruction block needs no
  wiring; don't flag it.

## Output shape

Headline tally, then FAILS, then WARNINGS, then the one fix to make first — or a
clean bill of health.

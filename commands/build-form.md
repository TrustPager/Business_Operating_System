---
description: Design and create a form template — fields, types, and order. Plans the field list in chat for approval, then creates it via MCP. Wiring to CRM variables and connecting to an intake is the next step (wire-form).
---

Run the **Build Form** skill.

Invoke the skill at `skills/build-form/SKILL.md`. Understand what the form
captures and who fills it, plan the field list in chat (naming each field's
intended CRM home so the label rule holds), get approval, then create the
template via MCP (`create_form_template` → `add_form_field` ×N → read back).

This skill BUILDS the fields. It does not wire them to the CRM or send the form —
that's `/wire-form`. Offer `/lint-form` before it ships. If starting from a
paper/PDF form, read it and reverse-engineer the fields rather than inventing them.

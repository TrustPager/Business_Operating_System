---
description: Connect a form's fields to the right record so answers land where they should, then hook it in.
---

Run the **Wire Form** skill.

Invoke the skill at `skills/wire-form/SKILL.md`. Load the template
(`get_form_template` + `list_form_fields`), build the field → CRM-variable
mapping with the operator (flag every orphan), apply it with
`bulk_update_form_field_wiring`, then connect the form to its fill path: send to
a named recipient (`send_form`, real recipients only, confirm first), internal
fill (`create_internal_form_submission`), or an intake trigger via
`/automate-this` (`form_completed`/`form_opened`, NOT for public website forms,
which use a `generic_webhook` trigger).

Hand off to `/lint-form` then `/form-radar`.

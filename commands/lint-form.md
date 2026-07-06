---
description: Pre-flight a form before it ships: every field wired, required fields set, no leftover placeholders.
---

Run the **Lint Form** skill.

Invoke the skill at `skills/lint-form/SKILL.md`. Load the template
(`get_form_template` + `list_form_fields`), run the checks, and present the
verdict: FAILS first (orphan data field, label↔wiring mismatch, empty template,
broken option set), then WARNINGS (required not set, leftover placeholder,
duplicate label). Route field fixes to `/build-form` and wiring fixes to
`/wire-form`; never edit from this skill.

If the operator didn't say which form, ask which one to lint.

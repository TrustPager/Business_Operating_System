---
description: Turn an existing paper or PDF form or contract into a reusable digital template.
---

Run the **Template From Document** skill.

Invoke the skill at `skills/template-from-document/SKILL.md`. Follow it exactly:
convert the source with `tools/markitdown_convert.py`, work out whether it's a
form (becomes a form template) or an agreement (becomes a signing template),
propose the fields/sections it found, then hand off to `/build-form` or
`/build-document` to create it on confirmation. Built on
`knowledge/document-tools-method.md`.

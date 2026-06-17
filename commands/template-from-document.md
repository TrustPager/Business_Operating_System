---
description: Turn an existing paper or PDF form into a TrustPager form template, or an existing agreement/contract into a signing template. Reads the old document and builds the digital version so you stop working off paper.
---

Run the **Template From Document** skill.

Invoke the skill at `skills/template-from-document/SKILL.md`. Follow it exactly:
convert the source with `tools/markitdown_convert.py`, work out whether it's a
form (becomes a form template) or an agreement (becomes a signing template),
propose the fields/sections it found, then hand off to `/build-form` or
`/build-document` to create it on confirmation. Built on
`knowledge/document-tools-method.md`.

---
description: Pre-flight a signing template before it goes out: signatures, merge fields, nothing missing.
---

Run the **Lint Document** skill.

Invoke the skill at `skills/lint-document/SKILL.md`. Load the template
(`list_document_templates` to find it, `get_document_template` to read its
sections), run the checks, and present the verdict: FAILS first (signer with no
input, broken merge token, empty template), then WARNINGS (likely-blank merge
field, leftover placeholder, missing date next to a signature). Route every fix
to `/build-document`; never edit the template from this skill.

If the operator didn't say which template, ask which one to lint.

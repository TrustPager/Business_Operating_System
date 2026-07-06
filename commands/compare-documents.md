---
description: Compare two documents and show what actually changed, in plain language.
---

Run the **Compare Documents** skill.

Invoke the skill at `skills/compare-documents/SKILL.md`. Follow it exactly:
convert both files with `tools/markitdown_convert.py`, compare the Markdown, and
report the meaningful changes (added / removed / changed), grouped and in plain
language, with the figures and clauses that moved called out. Built on
`knowledge/document-tools-method.md`.

---
description: Compare two documents and show exactly what changed — contract v1 vs v2, a revised quote, updated terms. Converts both to Markdown and highlights the differences in plain language.
---

Run the **Compare Documents** skill.

Invoke the skill at `skills/compare-documents/SKILL.md`. Follow it exactly:
convert both files with `tools/markitdown_convert.py`, compare the Markdown, and
report the meaningful changes (added / removed / changed), grouped and in plain
language, with the figures and clauses that moved called out. Built on
`knowledge/document-tools-method.md`.

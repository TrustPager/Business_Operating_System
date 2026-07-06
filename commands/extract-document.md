---
description: Pull the data out of any file and use it: answer a question, summarise it, or map it to a record.
---

Run the **Extract Document** skill.

Invoke the skill at `skills/extract-document/SKILL.md`. Follow it exactly: convert
the file with `tools/markitdown_convert.py` (the standard MarkItDown path), then do
the specific extraction the operator asked for: pull named fields, summarise, or
map the data onto an opportunity/contact (confirming before any CRM write). Works
on PDF, Word, Excel, PowerPoint, images, HTML, and CSV.

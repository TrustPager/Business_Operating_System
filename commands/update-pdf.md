---
description: Fill a PDF with data from a record so you never retype it, then show you the filled copy to review.
---

Run the **Update PDF** skill.

Invoke the skill at `skills/update-pdf/SKILL.md`. Follow it exactly: read the blank
PDF (via `tools/markitdown_convert.py`) to learn its fields and labels, pull the
named record's data from the CRM, show the proposed field-by-field mapping for
confirmation, then write a filled copy to a new file (never overwrite the blank).
Flag any field the record can't fill rather than guessing.

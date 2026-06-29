---
description: Turn a messy source (a photo of a notebook, a phone-contacts export, a screenshot, a half-broken spreadsheet, or a pasted list) into one tidy customer list you can open and use. Reads it with MarkItDown, normalises it, and writes a clean .csv/.xlsx. Works with nothing connected.
---

Run the **import-from-anywhere** skill.

Invoke the skill at `skills/import-from-anywhere/SKILL.md`. Follow it exactly:
read the source with `tools/markitdown_convert.py` (the standard MarkItDown
path), work out the shape, normalise it into one clean table, show the preview,
then write the tidy list with `tools/write_xlsx.py` (or a plain .csv). Don't
skip the "Important behaviours" section: it encodes the safety rails (preview
before writing, never invent a value, no silent merging) that should never be
skipped.

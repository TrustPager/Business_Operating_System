---
description: Build a real spreadsheet you can open and start filling today (a job tracker, a simple cashflow, or a lead log) with columns designed for your trade and a working .xlsx saved locally. No account needed. Once your workspace is connected, the same tracker can live inside it and keep itself current as your work moves.
---

Run the **Build Spreadsheet** skill.

Invoke the skill at `skills/build-spreadsheet/SKILL.md`. Follow it exactly: work
out which slice the sheet is for (job tracker, simple cashflow, or lead log),
design the columns to fit how they run that part of the business, confirm the
header row, then write a real `.xlsx` with `tools/write_xlsx.py` (bold header, a
couple of clearly-labelled example rows). Hand the file over, then offer the
live, self-updating version once their workspace is connected, in plain words.

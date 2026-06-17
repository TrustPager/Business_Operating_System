---
description: Build either kind of TrustPager spreadsheet. A workspace sheet pulls live from your CRM (e.g. settled-this-month by broker, with monthly views, totals, and a rolling auto-create). A standalone sheet holds its own data (a calculator, a tracker, or an existing Excel imported in). The skill asks which, then builds it.
---

Run the **Build Spreadsheet** skill.

Invoke the skill at `skills/build-spreadsheet/SKILL.md`. Follow it exactly: first
work out whether they want a **workspace** spreadsheet (live from the CRM) or a
**standalone** one (its own data), then build it down the matching path — columns
+ period views + totals + rolling automation for workspace, or columns + data
(from scratch, a template, or an imported Excel/CSV via MarkItDown) + formulas for
standalone. Confirm before writing.

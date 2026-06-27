---
name: Build Spreadsheet
description: Build either kind of TrustPager spreadsheet. A WORKSPACE spreadsheet pulls live from the CRM (pick columns including custom fields, period views, running totals, a rolling auto-create) — for "track X by month" like monthly settlement reconciliation. A STANDALONE spreadsheet holds its own data (a calculator, a planner, a tracker, or an existing Excel/CSV imported in) and isn't bound to the CRM. This skill asks which, then builds it.
triggers:
  - build a spreadsheet
  - make a workspace spreadsheet
  - make a standalone spreadsheet
  - track settled this month
  - monthly reconciliation spreadsheet
  - total my X by month
  - import this excel into a spreadsheet
  - settlement spreadsheet
function_slot: accounting
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__create_spreadsheet
  - mcp__list_spreadsheet_templates
  - mcp__bulk_append_spreadsheet_rows
status: active
---

# Build Spreadsheet

TrustPager has two spreadsheet types, and they're for different jobs. Pick the
right one first, then build it.

## Step 1 — Which kind?

Ask (or infer from the request, then confirm):

- **Workspace spreadsheet** — pulls live from the CRM and stays current as
  records change. Use when the data IS your CRM: opportunities, values, custom
  fields, totalled by period (e.g. settled-this-month by broker and bank). → Path A.
- **Standalone spreadsheet** — its own data, not bound to the CRM. Use for a
  calculator, a planner, a commission model, an ad-hoc tracker, or bringing an
  existing Excel/CSV into TrustPager. → Path B.

If the request is "total my opportunities / settlements / pipeline by month" it's
workspace. If it's "a sheet to work out X" or "import my spreadsheet" it's
standalone.

---

## Path A — Workspace spreadsheet (live from the CRM)

### A1 — Confirm columns + period + totals
- **Columns** — opportunity fields + custom fields (e.g. opportunity name, value,
  settlement date, broker, bank). If a needed custom field doesn't exist, hand off
  to `/add-a-field` first (and ensure it's exposed to the spreadsheet system).
- **Period** — how it's grouped (usually by month, on a date field like settlement date).
- **Totals** — which column to sum (e.g. value).

### A2 — Create + add columns
Create a workspace spreadsheet (`create_spreadsheet`, sourced from opportunities)
and add the confirmed columns. Remove unwanted defaults. If a custom field can't
be added as a column, that's the known platform gap — tell the operator and offer
`/report-an-issue` rather than silently dropping it. Respect the approval queue.

### A3 — Period views + totals
A **view per period** (e.g. "June 2026") filtered on the date field to that month,
each with a **sum** on the totals column. Seed the last couple of periods + the
current one.

### A4 — Offer the rolling automation
Offer a **scheduled automation** that creates next period's view automatically
(hand off to `/automate-this`). Confirm before creating.

---

## Path B — Standalone spreadsheet (its own data)

### B1 — Where does the data come from?
- **From scratch** — the operator describes the columns and what it's for (e.g. a
  commission calculator: deal, loan amount, rate, commission). 
- **From a template** — if there's a fitting spreadsheet template, start from it
  (`list_spreadsheet_templates`).
- **From an existing file** — if they have an Excel/CSV, convert it with the
  standard tool first: `python tools/markitdown_convert.py "<file.xlsx>"`
  (`knowledge/document-tools-method.md`), then build the sheet from its columns
  and rows. Don't hand-parse the file.

### B2 — Create + set columns
Create a standalone spreadsheet (`create_spreadsheet` as a standalone sheet, not
CRM-sourced) with the confirmed columns and types. For an import, load the rows
(`bulk_append_spreadsheet_rows`); stream progress.

### B3 — Formulas / totals
Add the calculations the operator wants (sums, per-row formulas like
amount × rate). Confirm the formula logic in plain language before applying it,
so a wrong calc doesn't go unnoticed.

### B4 — Confirm it's standalone
Make clear it does NOT read from the CRM — it's a self-contained sheet. If they
later want it tied to CRM data, that's a workspace spreadsheet (Path A).

---

## Confirm (either path)

```
✓ Built "Monthly settlement" (workspace, live from opportunities):
  columns: opportunity, loan amount, settlement date, broker, bank
  views: Apr / May / June 2026, each summing loan amount
  → want next month's view auto-created each month?
```
or
```
✓ Built "Commission calculator" (standalone): 5 columns, commission = loan × rate.
  Self-contained — it doesn't read from your CRM.
```

## Hard rules
- ❌ Don't pick the type for the operator silently when it's ambiguous — confirm workspace vs standalone.
- ❌ Workspace: don't drop a needed custom-field column silently — create it (`/add-a-field`) or flag the gap.
- ❌ Standalone: don't hand-parse an Excel/CSV — convert via `tools/markitdown_convert.py`.
- ❌ Don't route around an approval gate (202 = queued).
- ✅ Workspace sheets source live from the CRM; standalone sheets hold their own data — don't blur the two.
- ✅ Confirm formula logic in plain language before applying it.

## Output shape
A one-line confirmation naming the spreadsheet, its type (workspace/standalone),
its columns, and either the period views + totals + auto-create offer (workspace)
or the formulas + "self-contained" note (standalone).

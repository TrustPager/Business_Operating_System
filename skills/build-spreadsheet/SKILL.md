---
name: Build Spreadsheet
description: Build a real spreadsheet you can open and start filling today — a job tracker, a simple cashflow, or a lead log — with the right columns designed for your trade and a working .xlsx saved locally. No account needed. Once your workspace is connected, the same tracker can live inside it and keep itself current as your work moves.
triggers:
  - build a spreadsheet
  - make me a job tracker
  - i need a cashflow spreadsheet
  - set up a lead log
  - track my jobs in a spreadsheet
  - spreadsheet to track money in and out
  - simple cashflow sheet
  - create an xlsx
function_slot: documents
requires_driver: doclib
requires_credential: none
data_path: local
status: active
---

# Build Spreadsheet

You hand the owner a real spreadsheet they can open in Excel or Google Sheets
and start filling the same minute. No account, no setup: pick the slice of the
business the sheet is for, design the columns so they actually fit the trade,
and write a real `.xlsx` to disk with `tools/write_xlsx.py`.

The keyless `.xlsx` is the win. A live workspace version that keeps itself
current is the deeper version you offer afterward, in plain words, once their
workspace is connected.

This is the keyless WRITE path built on the doc-lib-set driver
([`knowledge/document-tools-method.md`](../../knowledge/document-tools-method.md)).
The owner never has to think about any of that: they ask for a spreadsheet,
they get a spreadsheet.

## Step 1 — Which slice of the business?

Most owners who ask for "a spreadsheet" want one of these. Ask which fits, or
infer from what they said and confirm:

- **Job tracker** — every job in one place: who it's for, what it is, the
  stage it's at, what it's worth, when it's due. The default for a trade or
  service business that runs work job by job.
- **Simple cashflow** — money in and money out by date, with a running
  balance, so they can see where they stand this month at a glance.
- **Lead log** — every enquiry as it comes in: who, where from, what they
  want, what's been done about it, and whether it turned into work.
- **Weekly scoreboard** — one row a week with the numbers that show whether
  the business moved: enquiries in, conversations had, jobs won, cash
  collected, plus one slot for the number this quarter turns on (shape per
  `business-method.md` §12.6). Keep it exactly this simple — five or six
  columns an owner fills in ten minutes on a Monday.

If they describe something close to one of these, name it back and build that.
If it's genuinely a fourth thing (a quoting calculator, a stock list, a
planner), design columns for it the same way: a header row that matches how
they actually talk about the work, in a sensible order.

It's fine to ask one quick question about how they run that part of the
business, so the columns fit. Naming the messy part they want tidier is fine in
this conversation: the sheet itself stays plainly useful.

## Step 2 — Design the columns for that slice

Lay out the header row before writing anything, and shape it to their trade.
Starting points (adapt the wording to how *they* describe it):

- **Job tracker:** `Job` · `Customer` · `Stage` · `Value` · `Due date` ·
  `Notes`. Stage is their real stages (e.g. quoted, booked, in progress, done,
  invoiced) — ask, don't assume.
- **Simple cashflow:** `Date` · `Description` · `Money in` · `Money out` ·
  `Running balance`. One row per movement; the balance column is where the
  running total goes.
- **Lead log:** `Date` · `Name` · `Source` · `What they want` · `Status` ·
  `Next step`. Source is where the enquiry came from (referral, website, a call).
- **Weekly scoreboard:** `Week` · `Enquiries in` · `Conversations` ·
  `Jobs won` · `Cash collected` · one column named for the number this
  quarter turns on (ask what that is; if they don't have one, leave it as
  `This quarter's number`).

Show the planned header row in plain language and confirm it's right before you
generate the file. Columns are cheap to change now, annoying to redo once
they've typed real data in.

## Step 3 — Write the real .xlsx

Build the rows as a JSON array of arrays: the header row first, then a few
example rows so the sheet shows what good looks like (label them clearly as
examples the owner can type over, e.g. an `Example` in the first cell). Then
write it:

```bash
python ~/.claude/bos-run.py tool write_xlsx --out "job-tracker.xlsx" --rows '[["Job","Customer","Stage","Value","Due date","Notes"],["Example: fit-out at 14 Example St","A. Customer","Booked",4200,"2026-07-10","deposit paid"]]' --sheet "Jobs" --header
```

(The `~/.claude/bos-run.py` launcher resolves the install location for you. If it is missing, run `python tools/setup.py` once from the BOS directory to create it.)

- `--header` makes the first row bold so the columns read as headings.
- `--sheet` titles the tab for the slice ("Jobs", "Cashflow", "Leads").
- For a cashflow, put a sensible starting balance in the first example row's
  balance cell, and say in plain words how the running balance works (each row
  is the one above plus money in, minus money out) so they can keep it going.

If the wrapper reports the spreadsheet library isn't installed (a line starting
`BOS_MISSING_DEP:`), don't hand-build the file another way and don't hand the
owner a command. Offer the setup in plain language:

> To build that spreadsheet I need to add the document tool-kit, a quick free
> one-time setup on your machine. Want me to sort it?

On a yes, run `python ~/.claude/bos-run.py tool check-install --fix` (or
`python -m pip install openpyxl` for the one piece) yourself, confirm it worked,
then re-run the write command. Never tell the owner to run anything. The full
detect-offer-install-verify loop is the canonical one in
[`knowledge/document-tools-method.md`](../../knowledge/document-tools-method.md).

## Step 4 — Hand it over + offer the deeper version

Tell them what you built, where it saved, and how to keep it going:

```
✓ Built "job-tracker.xlsx" (saved here, opens in Excel or Google Sheets):
  columns: Job · Customer · Stage · Value · Due date · Notes
  one example row in there. Type over it and add your own.
```

Then offer the upgrade in plain language, without making it the price of
entry:

> This one's yours to fill in by hand, and it works today. Once your workspace
> is connected, I can set up the same tracker to live right inside it and keep
> itself current as your jobs move along, so you're not retyping anything. No
> rush though: this sheet stands on its own.

That live, self-updating version is a connected capability. Describe it the way
above and leave it there; the keyless file is the real deliverable here.

## Hard rules

- ❌ Don't make the owner connect anything to get a usable spreadsheet — the
  keyless `.xlsx` is the whole point, and it ships first.
- ❌ Don't invent columns that don't fit how they run the work — design to the
  slice and confirm the header row before writing.
- ❌ Don't hand-build the file some other way if the library's missing, and
  never hand the owner a command — offer the one-time setup in plain language
  and run the install yourself (see Step 3).
- ❌ Don't promise the live, self-updating version as if it's part of this
  keyless build — it's the deeper version, offered in words, after.
- ✅ Write a real `.xlsx` with `tools/write_xlsx.py`, header row bold, a couple
  of clearly-labelled example rows so the sheet teaches itself.
- ✅ Keep the sheet and every label plainly useful and forward-looking: it
  shows the owner where their work stands.

## Output shape

A confirmed header row for the chosen slice, then a one-line confirmation
naming the saved `.xlsx`, its columns, and the example row — followed by the
plain-language offer of the live, self-updating version once their workspace is
connected.

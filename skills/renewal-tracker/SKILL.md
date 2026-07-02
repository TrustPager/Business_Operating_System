---
name: Renewal Tracker
description: A live renewal tracker .xlsx the owner keeps and updates, where a days-until-renewal column is a live formula that recalculates every time the file is opened. Licenses, insurances, certifications, registrations, and memberships in, with each item's renewal date and an optional lead-time, and the owner walks away with a real spreadsheet sorted soonest-renewal-first, flags showing what is inside the lead window, and a clear view of what is coming up. Keyless, works from what the owner types in. Connecting a CRM or calendar is what turns these into reminders that actually fire.
triggers:
  - renewal tracker
  - track my renewals
  - license renewal
  - insurance renewal
  - certification renewal
  - registration renewal
  - membership renewal
  - renewals coming up
  - expiry tracker
  - don't let my license lapse
  - what's expiring soon
  - keep on top of renewals
  - renewal reminder
  - cert expiry
  - annual renewals
  - upcoming renewals
function_slot: documents
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---

# Renewal Tracker

An owner tells you what they need to renew each year (licenses, insurances,
certifications, registrations, memberships), gives you each item's renewal date
and optionally a lead-time (the number of days before renewal they want to act),
and walks away with a real `.xlsx` tracker where the days-until-renewal column
is a LIVE FORMULA. Every time the owner opens the file, Excel or Google Sheets
recalculates the column from today, so the numbers are always current. Rows are
sorted soonest-renewal-first so the most urgent item is always at the top.

This is the tracker partner to `cash-flow-forecast` and `profit-per-job`. Those
apps work on money; this one keeps the owner ahead of every compliance and
coverage date. It runs cold on day one, on typed inputs alone.

**The keyless win is the tracker file.** The owner gets a real, maintainable
`.xlsx` they can open any time and see exactly where each renewal sits right now.
What does NOT come from the keyless floor is reminders that actually fire on
their own: that requires connecting a CRM or calendar. That connection is the
deepener, described plainly at the close, never the price of the win today.

## Step 1: Take in the items

Ask the owner to list every renewable item they track. For each one gather:

- **Item name** (e.g. "Public liability insurance", "Electrical contractor
  licence", "Privacy Act registration", "Trade association membership").
- **Category** (e.g. Insurance, Licence, Certification, Registration,
  Membership). If it is obvious from the name, infer it and confirm in the
  read-back rather than asking.
- **Renewal date** (the date the item is next due). Required: if an item has no
  date, say so and leave it out rather than inventing one. Ask one plain question
  if the date is genuinely missing.
- **Lead-time (days)** (how many days before the renewal date the owner wants
  to act). Optional: if the owner does not give one, leave the cell blank or
  use a sensible stated default (e.g. 30 days) and flag you are using it.

If any renewal date is missing and the owner cannot supply it, exclude that item
from the tracker and say you have left it out, along with what you need to add
it later.

## Step 2: Read the items back before writing (one pass)

A wrong date here means the tracker shows the wrong urgency. Play the items back
in a compact list before writing anything:

> Here is what I have:
>
> 1. Public liability insurance (Insurance) renewal 2026-09-01, lead-time 30 days
> 2. Electrical contractor licence (Licence) renewal 2027-01-15, lead-time 60 days
> 3. Privacy Act registration (Registration) renewal 2026-10-31, lead-time 14 days
>
> That right? Anything to correct or add?

Take corrections, then confirm once more if needed. Only once confirmed do you
sort and write.

## Step 3: Sort soonest-first and build the row data

Order rows by renewal date ascending (nearest date at the top). If two items
share a renewal date, sort alphabetically by item name.

For each row compute:

- **Days until renewal (display):** the number of days from today to the renewal
  date (for showing in chat and for setting the row order). This display figure
  is for reference only; the live formula in the spreadsheet is the source of
  truth and always recalculates from the actual file-open date.
- **Status flag (display):** based on whether the item is inside its lead-time
  window. Inside the window: "Act now". Outside the window: "On track". No
  date: "Date needed". These are shown in chat but the live formula in the
  spreadsheet recalculates them from today every time.

State the sort order in one line so the owner knows what they are looking at.

## Step 4: Lay out the tracker in chat

Present a clean table the owner can act on immediately, even before the file is
built:

```
## Your renewal tracker (soonest first)

| Item | Category | Renewal date | Days until renewal | Lead-time (days) | Status |
|------|-----------|--------------|--------------------|------------------|--------|
| Privacy Act registration | Registration | 2026-10-31 | 124 | 14 | On track |
| Public liability insurance | Insurance | 2026-09-01 | 64 | 30 | Act now |
| Electrical contractor licence | Licence | 2027-01-15 | 200 | 60 | On track |

**Coming up first:** Privacy Act registration, due 2026-10-31 (124 days). Lead-time is 14 days, so the action window opens around 2026-10-17.

**Assumptions:**
- Days until renewal calculated from today (2026-06-29). The spreadsheet formula
  recalculates this automatically each time you open the file.
- Lead-time default of 30 days used for Public liability insurance (none given).
- [Any items excluded and why, if any.]
```

Frame it forward: this is the view that keeps the owner ahead of every deadline.

## Step 5: Build the live .xlsx tracker

The live spreadsheet IS the required deliverable for this app. Build it with
`tools/write_xlsx.py`. The days-until-renewal column MUST use a LIVE FORMULA
so it recalculates from TODAY() each time the file is opened.

**Column layout:**

| Col | Content |
|-----|---------|
| A   | Item name |
| B   | Category |
| C   | Renewal date (as a date string, e.g. "2026-09-01") |
| D   | Days until renewal (LIVE FORMULA referencing C and TODAY) |
| E   | Lead-time (days, numeric or blank) |
| F   | Status flag (LIVE FORMULA: Act now / On track / Date needed) |

Row 1 is the header (bold). Row 2 is the soonest-renewal item. Rows continue
in soonest-first order.

**Live formula pattern for days-until-renewal (column D).**

openpyxl writes cell strings that begin with `=` as live formula cells, not
text. The formula must reference the renewal-date cell in the same row and
subtract TODAY() so it recalculates on open.

For row 2 (first data row):

```
"=DATE(YEAR(C2),MONTH(C2),DAY(C2))-TODAY()"
```

But since the renewal date is stored as a plain string like "2026-09-01", the
safer pattern is to encode the date components directly so the formula does not
depend on C2 being parsed as a date by Excel. For a renewal date of 2026-09-01:

```
"=DATE(2026,9,1)-TODAY()"
```

Use the `=DATE(yyyy,m,d)-TODAY()` pattern for each row, substituting the year,
month, and day from the owner's data. This is robust across regional date
settings.

**Live formula pattern for status flag (column F).**

For row 2, where E2 is the lead-time (or blank), the flag formula reads:

```
"=IF(C2=\"\",\"Date needed\",IF(E2=\"\",IF(DATE(YEAR(C2),MONTH(C2),DAY(C2))-TODAY()<=0,\"Renew now\",\"On track\"),IF(DATE(YEAR(C2),MONTH(C2),DAY(C2))-TODAY()<=E2,\"Act now\",\"On track\")))"
```

Because Excel/openpyxl formulas that embed double-quotes require them escaped
as `\"` in the JSON string, and because this formula is complex enough to be
fragile in JSON escaping on some platforms, use the simpler D-column reference
approach once D is written:

```
"=IF(D2=\"\",\"Date needed\",IF(E2=\"\",IF(D2<=0,\"Renew now\",\"On track\"),IF(D2<=E2,\"Act now\",\"On track\")))"
```

For simplicity and reliability, use this D-column-reference version for every
data row (D2, D3, D4, ...).

**Exact write_xlsx command (4-item example, adjust for the owner's actual list):**

```bash
python ~/.claude/bos-run.py tool write_xlsx \
  --out "renewal-tracker.xlsx" \
  --sheet "Renewal Tracker" \
  --header \
  --rows '[
    ["Item","Category","Renewal date","Days until renewal","Lead-time (days)","Status"],
    ["Privacy Act registration","Registration","2026-10-31","=DATE(2026,10,31)-TODAY()",14,"=IF(D2<=0,\"Renew now\",IF(D2<=E2,\"Act now\",\"On track\"))"],
    ["Public liability insurance","Insurance","2026-09-01","=DATE(2026,9,1)-TODAY()",30,"=IF(D3<=0,\"Renew now\",IF(D3<=E3,\"Act now\",\"On track\"))"],
    ["Electrical contractor licence","Licence","2027-01-15","=DATE(2027,1,15)-TODAY()",60,"=IF(D4<=0,\"Renew now\",IF(D4<=E4,\"Act now\",\"On track\"))"]
  ]'
```

(The `~/.claude/bos-run.py` launcher resolves the install location for you. If it is missing, run `python tools/setup.py` once from the BOS directory to create it.)

Fill in the actual items, dates, and lead-times from the owner's data. Adjust
row numbers (D2/E2, D3/E3, ...) for each row. The `=DATE(yyyy,m,d)-TODAY()`
cells are written by openpyxl as live formula cells, so the value recalculates
each time the owner opens the file.

**If the JSON carries any non-ASCII characters** (accented names or characters
beyond standard ASCII), write the rows to a UTF-8 temp file and pipe on stdin:

```bash
python ~/.claude/bos-run.py tool write_xlsx --out "renewal-tracker.xlsx" --sheet "Renewal Tracker" --header < rows.json
```

**If openpyxl is missing.** The tool prints a line starting `BOS_MISSING_DEP:`
and exits. Do not hand-build the file another way. Offer it in plain language:

> To build that live tracker file I need to add the document tool-kit, a quick
> free one-time setup on your machine. Want me to sort it?

On a yes, run `python -m pip install openpyxl` yourself, confirm it worked,
then re-run the write command. Never tell the owner to run anything.

## Step 6: The connect-tier split (state it honestly)

After delivering the tracker, close with one honest line about what the keyless
floor provides versus what the connected tier adds:

> This tracker file stays current every time you open it, so you always know
> where each renewal sits. What it does not do on its own is fire a notification
> when a date is approaching: connecting your calendar or CRM is what turns
> this list into reminders that actually reach you on the day you need them.
> That is the natural next step when you are ready.

Never describe the keyless tracker as if it notifies anyone. Never oversell the
floor. The reminder-firing is the honest connect-time deepener.

## When the items are customer renewals (conditional)

Most runs track the owner's own compliance and coverage dates; for those,
nothing in this section applies. When some listed items are things customers
renew WITH the owner (client contracts, retainers, maintenance plans,
memberships), add this on top:

1. Say so in one line: for those rows the tracker is also a retention
   surface, not just a date list.
2. Each upcoming customer renewal inside its lead window is a re-sign
   conversation to schedule now, at the before-expiry moment (per
   `knowledge/business-method.md` §9.4 and §11.4).
3. A lapsed customer renewal gets the cancellation-save conversation within
   24 hours (§11.5). Offer to draft it: outcome-led, per §18.
4. Nothing else changes: same columns, same formulas, same connect-tier
   close.

## Step 7: Close the loop

After the tracker is built:

> "That is your renewal tracker, sorted with the nearest date at the top, and
> the days-until-renewal column updating every time you open the file. Add a row
> for anything new, and the whole thing stays current. Want to add more items,
> or build something else?"

## Hard rules

- **Never invent a renewal date.** Every date comes from the owner. If a date
  is missing, ask one plain question or leave the item out and say so.
- **The .xlsx is the required deliverable.** The live tracker file IS the win
  for this app. A chat table alone does not clear the bar. Build the file.
- **Days-until-renewal is a live formula.** The column MUST use `=DATE(yyyy,m,d)-TODAY()`
  (or equivalent), never a pre-computed number. A static value does not clear
  the bar.
- **Rows sorted soonest-first at write time.** Order by renewal date ascending
  before writing. The soonest item is always row 2.
- **State the connect-tier split honestly.** The keyless file is the tracker.
  The reminder-firing (CRM, calendar) is the connect-time deepener. Never
  imply the keyless file notifies anyone.
- **Customer-renewal rows are retention data, not just dates.** Route re-sign
  and save conversations per `knowledge/business-method.md` §9.4 and §11.5;
  never let a client renewal sit passive inside its lead window. Compliance
  renewals are untouched by this.
- **Customer-facing output is positive and outcome-led.** The tracker shows
  what is coming up so the owner stays ahead of it, never what they might miss
  or what could go wrong.
- **No em dashes in anything the owner reads.** Use commas, colons, or separate
  sentences.
- **No accounts, no files needed.** This runs on typed inputs alone.

## Output shape

The read-back of confirmed items (one compact list), then the chat tracker table
(sorted soonest-first, days-until shown from today, status flags), then the
coming-up-first callout and assumptions, then the live `.xlsx` built via
`tools/write_xlsx.py` with `=DATE(yyyy,m,d)-TODAY()` formula cells, then the
honest one-line connect-tier split, then the close.

---
name: import-from-anywhere
description: Take a messy source — a photo of a notebook, a phone-contacts export, a screenshot, a half-broken spreadsheet, a pasted list of names — and turn it into one tidy customer list you can open and use. Reads anything with the standard MarkItDown converter, normalises it, and writes a clean .csv/.xlsx. Works keylessly day one; once your CRM is connected, the same list can go straight in.
triggers:
  - import this list
  - import this CSV
  - tidy up this list
  - clean up these contacts
  - turn this list into a spreadsheet
  - photo of my customer list
  - here's a list of customers
  - my contacts are a mess
  - make one customer list
  - I have a spreadsheet that's a mess
function_slot: documents
requires_driver: markitdown
requires_credential: none
data_path: local
status: active
---

# /import-from-anywhere

Customer lists show up in twenty different shapes: a photo of a notebook page,
a contacts export off a phone, a screenshot of an old email, a spreadsheet
that's been hand-edited into a mess. This skill turns any of those into **one
clean customer list** you can open, sort, and send — a real `.csv`/`.xlsx`
file, built locally, no account needed.

The win is the tidy list itself. If you've connected your CRM, the very same
list can also go straight in for you (see the last section) — but that's a
bonus on top, never the price of getting your list sorted.

## Step 1 — Read the source with the standard converter

Whatever the source is — a photo, a PDF, a Word doc, an Excel file, an HTML
export, a screenshot/scan — run it through the one standard converter first.
Don't hand-parse raw bytes and don't ask the owner to re-type it:

```bash
python tools/markitdown_convert.py "<path-to-file>"
```

This is the standard read path (`knowledge/document-tools-method.md`). It
turns any file into clean Markdown that's easy to work on, and it OCRs photos
and scans. If the wrapper exits non-zero with a `BOS_MISSING_DEP: <spec>` line,
run the detect/offer/install-on-yes/verify loop in
`knowledge/document-tools-method.md` (offer to set it up, then run
`python -m pip install <spec>` yourself and retry). Never hand the owner a
command. If the conversion comes back empty (e.g. a blurry photo with no
readable text), say so plainly rather than inventing rows.

**Only skip Step 1 when the owner literally pastes the text** — then the paste
itself is your source and you go straight to Step 2.

## Step 2 — Work out the shape

Look at the converted text (or the paste) and read what kind of list it is:

- **Commas or tabs + a header row** → already a table; map the columns.
- **Names with emails / phones mixed in** → a contact list to split into fields.
- **Names with dollar amounts and dates** → looks like jobs or deals, not plain contacts. Flag it and ask.
- **Company names, ABNs, addresses** → businesses, not people.
- **Just phone numbers, no names** → a phone list; each number becomes a row.

If it's genuinely ambiguous, ASK one short question rather than guessing:

> I can see about 40 rows here. Should this come out as a people list (names,
> emails, phones) or a business list (company names and addresses)?

## Step 3 — Normalise into one tidy table

Decide a single clean column set and map every row onto it. A sensible default
for a people list:

```
First | Last | Email | Phone | Company | Notes
```

Then tidy as you go:
- **Split full names** into First / Last where it's clear; leave the whole name in First and flag it where it isn't.
- **Normalise Australian phone numbers** to a consistent format (`+61...`).
- **Trim stray punctuation, fix obvious casing** (ALL CAPS names → Title Case).
- **Flag likely OCR slips** from photos/scans (`O` vs `0`, `l` vs `1`) on the rows where they appear, rather than silently "correcting" them.
- **Keep the original line in Notes** when a row is messy, so nothing is lost and the owner can check it.

## Step 4 — Show the preview BEFORE writing the file

Build a preview of the first 5 cleaned rows plus a count and an issues list:

```
Tidied: 38 people
Preview:
  | First | Last | Email | Phone | Company |
  |---|---|---|---|---|
  | (first) | (last) | (email) | (phone) | (company) |
  ...

Worth a look:
  - 3 rows have no email (rows 4, 11, 27)
  - 1 phone couldn't be read (row 18: "see card")
  - 2 names look like the same person twice (rows 9 and 31)
```

ASK:

> Happy with this shape? I can drop the rows with gaps, merge the two that look
> like duplicates, or keep everything as-is. Your call.

## Step 5 — Write the clean list to a real file

After the go-ahead, write the tidy list locally with the standard writer:

```bash
python tools/write_xlsx.py --out customers.xlsx --header --rows '[["First","Last","Email","Phone","Company","Notes"], ... ]'
```

- Use `--header` so the column row is bold.
- For a plain `.csv` instead of `.xlsx`, write the same rows out as comma-separated lines.
- If the `.xlsx` path exits non-zero with `BOS_MISSING_DEP: openpyxl`, run the detect/offer/install-on-yes/verify loop in `knowledge/document-tools-method.md` (offer, then run `python -m pip install openpyxl` yourself and retry). Never hand the owner a command. Or fall back to writing a `.csv`, which needs nothing extra.

Tell the owner exactly where the file landed and what's in it.

## Step 6 — Report

End with a short, plain summary:

```
Built one tidy customer list: customers.xlsx
✅ 35 rows came through clean.
🔁 2 rows merged as the same person (kept the one with the email).
📝 1 phone left blank: couldn't read row 18 ("see card").
The original messy lines are saved in the Notes column so nothing's lost.
```

## Important behaviours

- **Always show the preview before writing the file.** Even for a handful of rows — it's the owner's data, and one quick look saves a re-do.
- **Never invent a value.** A blank cell with the original kept in Notes beats a guessed email or a "fixed" name that's now wrong.
- **No silent merging.** If two rows look like the same person, surface them and let the owner decide — don't quietly drop one.
- **Half a record isn't a record.** "Sarah from the markets" with nothing else is a Note to follow up, not a contact row — flag it.
- **The source stays traceable.** Keep the original line in Notes so the owner can always check the tidy version against what they started with.

## Edge cases

- **Photo / scan / screenshot** — convert it with `tools/markitdown_convert.py` (Step 1); MarkItDown OCRs it. Then flag any character that looks like an OCR slip and confirm those rows before they go in the file.
- **PDF / Word / Excel file** — same path: convert first, then tidy. Don't ask for a re-type.
- **A spreadsheet that's already mostly fine** — still run it through the converter so you're working on clean text, then just fix the few messy rows rather than rebuilding the whole thing.
- **A list of just emails, no names** — put the email in the Email column and the part before the `@` in First as a placeholder; ask the owner to confirm or supply real names.

## Once your CRM is connected (the bonus on-ramp)

The tidy list above is the whole win on its own. It's yours, it's a real file,
and it needed nothing connected to make.

When you've connected your CRM, there's a natural next step: instead of stopping
at the file, I can take that same clean list and seed it straight into your
customer database for you, each tidy row becoming a customer record ready to
work with. Same list, one step further. It's an upgrade you can take whenever
you're ready, and the file stands on its own until then.

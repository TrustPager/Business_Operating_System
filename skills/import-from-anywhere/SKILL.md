---
name: import-from-anywhere
description: Take a paste (CSV, screenshot text, PDF excerpt, email export, list of names) and import it as opportunities, contacts, or companies into TrustPager.
triggers:
  - import this list
  - import this CSV
  - import these contacts
  - turn this list into
  - bulk import
  - add these to the CRM
  - here's a list of
  - paste of contacts
  - paste of leads
  - I have a spreadsheet
---

# /import-from-anywhere

Customers paste data in 20 different shapes — CSV, screenshot OCR, copy-pasted email lists, PDF tables, "here's everyone I met at the conference, sorted by who looked at me weird." This skill turns any of those into clean TrustPager records.

## Step 1 — Detect what they pasted

After the user pastes, identify the shape:
- **Has commas or tabs + a header row** → CSV/TSV.
- **Has email-like patterns + name-like patterns interleaved** → free-text contact list.
- **Has dollar amounts + names + dates** → likely opportunities.
- **Has companies / ABNs / addresses** → companies, not contacts.
- **Has phone numbers, no emails** → contacts from a phone list.

If ambiguous, ASK:
> "I can see roughly 40 rows. Are these meant to land as contacts, opportunities, or companies?"

## Step 1.5 — Build the dedup baseline (in parallel with parsing)

While the user is reviewing the paste, run:

```
python skills/import-from-anywhere/fetch.py
```

This returns an index of every existing contact (by email + phone + name+company), every existing company (by name + domain), and every open opportunity (by name). Hold this in memory and check each parsed row against it during preview.

## Step 2 — Show what you parsed BEFORE writing anything

Build a preview table of the first 5 rows with the fields you've extracted. Show:

```
Detected: 38 contacts
Preview:
  | First | Last | Email | Phone | Company |
  |---|---|---|---|---|
  | (first) | (last) | (email) | (phone) | (company) |
  ...

Issues found:
  - 3 rows have no email (rows 4, 11, 27)
  - 1 row has an unparseable phone (row 18: "see card")
  - 2 rows look like duplicates of existing contacts
```

Run the duplicate detection by calling `python tools/audit-contacts.py --json` and matching against the parsed paste — show the user which rows are likely already in their workspace.

ASK:
> "OK to proceed? You can also tell me to skip the rows with issues, or to merge with existing rather than create new."

## Step 3 — Import in batches with progress

After explicit go:
- Use `mcp__trustpager__bulk_create_contacts` (or opportunities / companies) in batches of 50.
- Stream progress to the user: "Importing 38 contacts… 25/38 done… 38/38 done."
- If a batch fails: print the error and ask whether to continue with remaining batches or stop.

For opportunities: each one needs a pipeline + stage. Ask once up front:
> "Which pipeline should these land in? (current options: [list_pipelines]) — and which stage?"

## Step 4 — Report

End with:
```
Imported 38 contacts into TrustPager.
✅ 35 created cleanly.
⚠️  2 skipped as likely duplicates (you can review at /settings/...).
❌ 1 failed: row 18 had an unparseable phone number.
```

## Important behaviours

- **NEVER write without showing the preview first.** Even for 3 rows. Importing the wrong shape is hard to undo.
- **No silent dedup.** If a row matches an existing record, surface it — don't auto-merge.
- **Names are not contacts.** "Sarah from Acme" with no other detail = ask, don't import a half-record.
- **Phone normalization.** Aussie phones get normalized to E.164 (+61...) before writing.
- **The paste itself is data.** Save the original paste as a note on each created record so the source is traceable.
- **Spreadsheets are different.** If the user wants a SPREADSHEET row dump (not records), use `mcp__trustpager__bulk_append_spreadsheet_rows` instead and pick or create the target spreadsheet.

## Edge cases

- **PDF excerpt with broken whitespace** — ask the user to paste again into a code block (triple backticks) so multi-line entries are preserved.
- **Screenshot OCR with mis-recognized characters** — flag any name/email with non-ASCII chars from OCR mistakes ("O" vs "0", "l" vs "1") and ask for confirmation row-by-row.
- **List of just emails, no names** — import as contacts with first_name=email_local_part, ask the user to confirm or supply names.

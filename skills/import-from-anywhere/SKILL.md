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

## Step 1.5 — Build the dedup baseline (parallel MCP reads)

While the user reviews the paste, pull the existing records from the `trustpager` MCP server so you can flag duplicates BEFORE writing anything. All reads — free, nothing journaled:

| Need | Tool | Args |
|---|---|---|
| Existing contacts | `list_contacts` | `limit: 100` (page with `after` until exhausted, up to ~200) |
| Existing companies | `list_customers` | `limit: 100` (page with `after`, up to ~200) |
| Existing open opportunities | `list_deals` | `status: "open"`, `limit: 100` (page with `after`, up to ~200) |

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

Build an in-memory index from the results and hold it for the preview:
- **Contacts** keyed by: lowercased `email`; normalised `phone` (strip everything except digits and `+`, keep the last 12 chars); and a `first|last|companysuffix` key (lowercased first+last + the last 6 chars of `company_id`).
- **Companies** keyed by: lowercased `name`; and `website` **domain** (strip `https://` / `http://` / `www.`, take everything before the first `/` or `?`).
- **Open opportunities** keyed by: lowercased `name`.

This is the search-first rail ([`knowledge/safeguards.md`](../../knowledge/safeguards.md)) at bulk scale — one baseline fetch instead of N "is this a duplicate?" lookups per row.

## Step 2 — Show what you parsed BEFORE writing anything

Build a preview table of the first 5 rows with the fields you've extracted. Check each parsed row against the dedup index from Step 1.5 and surface matches. Show:

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
  - 2 rows look like duplicates of existing contacts (matched on email — rows 7, 22)
```

ASK:
> "OK to proceed? You can also tell me to skip the rows with issues, or to merge with existing rather than create new."

## Step 3 — Import in batches with progress

These are writes — they follow [`knowledge/safeguards.md`](../../knowledge/safeguards.md): no write before the preview is approved; journal each bulk write as one line to `.bos-journal.md`; if a call returns a `202`/`approval_id`, surface the approvals link and stop (don't retry).

After explicit go:
- Use `bulk_create_contacts` (or `bulk_create_deals` / `bulk_create_customers`) in batches of up to **100** records per call (the bulk tools cap at 100). Each returns `created[]` + `errors[]` for partial-success retry.
- **Set `skip_automations: true`** on historical imports so old records don't fire `*_created` automation emails — strongly recommended for any back-catalogue load.
- Stream progress to the user: "Importing 38 contacts… batch 1/1 done… 38/38."
- If a batch returns errors: print them and ask whether to continue with remaining batches or stop.

For opportunities: each one needs a pipeline + stage. Ask once up front:
> "Which pipeline should these land in? (I'll pull the options with `list_pipelines`) — and which stage?"

Pass the chosen `pipeline_id` / `stage_id` as the bulk-level default (each record can still override).

## Step 4 — Report

End with:
```
Imported 38 contacts into TrustPager.
✅ 35 created cleanly.
⚠️  2 skipped as likely duplicates (matched existing records — see preview).
❌ 1 failed: row 18 had an unparseable phone number.
```

## Important behaviours

- **NEVER write without showing the preview first.** Even for 3 rows. Importing the wrong shape is hard to undo.
- **No silent dedup.** If a row matches an existing record (per the Step 1.5 index), surface it — don't auto-merge.
- **Names are not contacts.** "Sarah from Acme" with no other detail = ask, don't import a half-record.
- **Phone normalization.** Aussie phones get normalized to E.164 (+61...) before writing.
- **The paste itself is data.** Save the original paste as a note on each created record (the `notes` field) so the source is traceable.
- **Spreadsheets are different.** If the user wants a SPREADSHEET row dump (not CRM records), append rows with `append_spreadsheet_row` — **one row per call** (there's no bulk row-append on the client tool surface; loop the rows and stream progress). Pick or create the target spreadsheet first; cells are keyed by column ID, not header name (get IDs from `get_spreadsheet`).

## Edge cases

- **PDF excerpt with broken whitespace** — ask the user to paste again into a code block (triple backticks) so multi-line entries are preserved.
- **Screenshot OCR with mis-recognized characters** — flag any name/email with non-ASCII chars from OCR mistakes ("O" vs "0", "l" vs "1") and ask for confirmation row-by-row.
- **List of just emails, no names** — import as contacts with first_name=email_local_part, ask the user to confirm or supply names.

---
name: Extract Document
description: Pull the data out of any document and use it. Converts the file (PDF, Word, Excel, PowerPoint, image/scan, HTML, CSV) to Markdown, then does what you asked: answer a question about it, summarise it, or map named fields onto a CRM opportunity or contact. The general "read a document and do something with it" skill; built on knowledge/document-tools-method.md.
triggers:
  - extract data from this pdf
  - extract document
  - read this document
  - pull the data out of this file
  - get the fields from this form
  - summarise this document
  - import this statement
function_slot: documents
requires_driver: markitdown
requires_credential: none
data_path: local
status: active
---

# Extract Document

Any "read a file and use what's in it" task goes through one path: convert to
Markdown with MarkItDown, then work on the Markdown. Don't try to parse raw PDF
or guess at a scan — convert first.

## Step 1 — Convert the file to Markdown

```bash
python ~/.claude/bos-run.py tool markitdown_convert "<path-to-file>"
```

(The `~/.claude/bos-run.py` launcher resolves the install location for you. If it is missing, run `python tools/setup.py` once from the BOS directory to create it.)

Handles PDF, Word, Excel, PowerPoint, images (OCR), HTML, CSV, JSON, ZIP. If the
wrapper reports MarkItDown isn't installed, relay its one-line install hint
(`pip install markitdown`) and stop until it's installed. If conversion fails or
comes back empty (e.g. a scan with no readable text), say so plainly rather than
inventing content.

## Step 2 — Do the specific extraction the operator asked for

Read the operator's goal and match it:

- **Answer a question / summarise** → work from the Markdown and answer. Quote
  the document where it matters; don't add facts that aren't in it.
- **Pull named fields** → return them as a clean list or table (e.g. applicant
  name, income, loan amount, property address). For anything the document
  doesn't contain, say "not in the document" — never guess a value.
- **Map onto a CRM record** → match each extracted field to its CRM field on the
  named opportunity/contact (use the real field names from the workspace). Show
  the proposed mapping and the values, then write only after the operator
  confirms. Respect the approval queue (a 202 is queued, surface it — see
  `knowledge/safeguards.md`).

## Step 3 — Show what you got + what you did

```
Read "ANZ-statement-March.pdf" (PDF → Markdown):
  • Applicant: Jane Smith   • Income: $142,000   • Loan: $640,000
  • Property: 14 Example St (not stated: deposit)
Mapped 3 fields onto opportunity "Smith refinance" (deposit left blank — confirm?).
```

## Hard rules
- ❌ Don't invent values not present in the document. "Not in the document" is a valid answer.
- ❌ Don't write to the CRM without showing the mapping and getting confirmation.
- ❌ Don't write bespoke per-format parsing — always go through `tools/markitdown_convert.py`.
- ✅ Quote the source for figures that matter; let the operator trust the extraction.
- ✅ Use the workspace's real field names when mapping.

## Output shape
A short summary of what was read and the fields pulled (with any "not in the
document" gaps named), then — if mapping to the CRM — the proposed mapping and
the ask, or a one-line confirmation of what was written.

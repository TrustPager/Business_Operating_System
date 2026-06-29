---
name: Update PDF
description: Populate a PDF with data from a CRM record so the operator doesn't retype it — a lender application, an agreement, an onboarding form filled from an opportunity or contact. Reads the blank form first (via MarkItDown) to learn its fields, maps them to the record, fills a copy, and shows it for review. The write side of the document tools (the read side is /extract-document); built on knowledge/document-tools-method.md.
triggers:
  - update this pdf
  - fill this pdf
  - populate this form
  - fill the application from this opportunity
  - put this client's data into the form
  - prefill this pdf
function_slot: documents
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
status: active
---

# Update PDF

This fills a PDF from a CRM record. It is the WRITE side of the document tools —
MarkItDown only reads, so here it's used to understand the blank form before a
PDF writer fills it.

## Step 1 — Understand the blank form

Read the blank PDF so you know what it's asking for:

```bash
python "${CLAUDE_PLUGIN_ROOT}/tools/markitdown_convert.py" "<path-to-blank-form.pdf>"
```

From the Markdown, list the fields the form wants (applicant name, income, ABN,
property address, signatures, etc.). Also detect whether the PDF has real
fillable form fields (an AcroForm) or is flat: 

```bash
python -c "import pypdf,sys; r=pypdf.PdfReader(sys.argv[1]); print(list((r.get_fields() or {}).keys()))" "<path>"
```

(If `pypdf` isn't installed, relay: `pip install pypdf`.)

## Step 2 — Pull the record + propose the mapping

Get the named opportunity/contact from the CRM (real field values). Build a
field-by-field mapping: each PDF field -> the CRM value that fills it. Show it to
the operator for confirmation before writing:

```
Filling "ANZ-home-loan-application.pdf" from opportunity "Smith refinance":
  Applicant name  ← Jane Smith
  Loan amount     ← $640,000
  Property        ← 14 Example St
  Income          ← (not on the record — leave blank? or enter now)
```

Never invent a value the record doesn't have — flag the gap and ask.

## Step 3 — Fill a COPY

After confirmation, write to a NEW file (e.g. `Smith-refinance-ANZ-filled.pdf`) —
never overwrite the blank template.

- **AcroForm (has fillable fields):** set the field values with `pypdf` and save.
- **Flat PDF (no fields):** don't guess coordinates blindly. Tell the operator the
  form has no fillable fields and offer the practical fallback: produce the
  answers as a clean field→value sheet they can paste in, or (if they have a
  field-position map) overlay the text. Don't silently produce a misaligned PDF.

## Step 4 — Show the result

```
✓ Filled 9 of 11 fields → Smith-refinance-ANZ-filled.pdf
  Left blank (not on record): income, deposit — add them and re-run if needed.
  Open it and check before sending.
```

The filled PDF is for the operator to review before it goes anywhere — it is not
verified until a human has looked at it (`knowledge/safeguards.md`).

## Hard rules
- ❌ Never overwrite the blank template — always write a new copy.
- ❌ Never invent a value the record doesn't have — flag it and leave it blank or ask.
- ❌ Don't blind-overlay text onto a flat PDF and pretend it's filled — say it has no fields and offer the fallback.
- ✅ Read the blank form first (MarkItDown) so the mapping matches the form's real labels.
- ✅ Show the mapping for confirmation before writing.

## Output shape
The proposed field→value mapping for confirmation, then after filling: a one-line
result naming the output file, how many fields were filled, and which were left
blank for the operator to complete.

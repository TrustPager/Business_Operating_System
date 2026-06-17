---
name: Template From Document
description: Turn existing paperwork into a TrustPager template. Reads a paper/PDF form (via MarkItDown) and builds a digital form template, or reads an existing agreement/contract and builds a signing template (sections + merge fields). The first-class "digitise this document" path; hands off to /build-form or /build-document to create it. Built on knowledge/document-tools-method.md.
triggers:
  - turn this form into a trustpager form
  - digitise this paper form
  - make a template from this document
  - build a form from this pdf
  - turn this contract into a signing template
---

# Template From Document

Businesses run on paperwork that should be digital. This reads the old document
and builds the TrustPager version, so the operator stops re-keying paper forms.

## Step 1 — Convert the source

```bash
python tools/markitdown_convert.py "<path-to-source>"
```

If it converts empty (image-only scan, no OCR text), say so and ask for a better
source rather than guessing the fields.

## Step 2 — Decide which template type

From the content:
- **A form to collect answers** (fields to fill: name, income, questions) → a
  **form template** (→ `/build-form`).
- **An agreement to be signed** (clauses + signature/date blocks) → a **signing
  template** (→ `/build-document`, with merge fields + signer inputs).

If it's genuinely both or unclear, ask the operator which they want.

## Step 3 — Propose the structure it found

Show what you extracted, for confirmation:

- **Form** → the list of fields with a sensible type each (text, number, date,
  dropdown with the options it lists, yes/no), in the document's order. Flag
  anything ambiguous ("'Status' — is this a dropdown? what options?").
- **Signing doc** → the sections/clauses, the merge fields (the blanks to fill
  per send, e.g. client name, amount), and the signer inputs (who signs/dates).

Don't invent fields the document doesn't have; don't drop ones it does.

## Step 4 — Hand off to build it

On confirmation, create it via the matching skill:
- Form → follow `skills/build-form/SKILL.md` with the proposed fields, then
  remind the operator to map it to the CRM (`/wire-form`) and test it safely
  (`/test-form`) before any customer sees it.
- Signing doc → follow `skills/build-document/SKILL.md` with the sections, merge
  fields, and signers, then `/lint-document` before use.

## Hard rules
- ❌ Don't build from an empty/garbled conversion — get a readable source first.
- ❌ Don't invent or omit fields/sections — mirror the source, flag the ambiguous bits.
- ❌ Don't skip the post-build steps (wire + test a form; lint a signing doc).
- ✅ Always convert through `tools/markitdown_convert.py`.
- ✅ Confirm the proposed structure before creating anything.

## Output shape
The detected template type + the proposed fields (form) or sections/merge-fields/
signers (signing doc) for confirmation, then a one-line "created — next: wire +
test" / "created — next: lint" handoff.

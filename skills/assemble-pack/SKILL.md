---
name: Assemble Pack
description: Combine a record's filled forms and uploaded files into one ordered PDF pack, ready to send onward (a lender bundle, an underwriter pack, a council submission). Lists what's on the opportunity, lets you pick the files and order, confirms, then produces one bundled PDF back on the record. The "gather it all into one document" step after /extract-document and /update-pdf.
triggers:
  - assemble the pack
  - build the lender pack
  - bundle these files
  - combine the documents into one
  - put the application pack together
  - make a submission pack
  - merge these files into one pdf
function_slot: documents
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__list_opportunity_files
  - mcp__trustpager__list_opportunity_documents
  - mcp__trustpager__describe_resource
  - mcp__trustpager__bundle_files
status: active
---

# Assemble Pack

The last step before something goes to a lender, insurer, underwriter, or
council: take everything collected on the opportunity — the forms you filled,
the documents the client uploaded — and combine it into ONE ordered PDF the
operator can send. This gathers; it does not send.

It pairs with the rest of the document tools: `/extract-document` reads, `/update-pdf`
fills, the portal collects uploads, and this assembles the result into one pack.

## Step 1 — Pick the opportunity

Ask which opportunity (or contact) the pack is for if it isn't already clear.
Pull it so you're working from the real record, not a name.

## Step 2 — List what's available to include

Gather the candidate files on that record:

- `list_opportunity_files(deal_id)` — uploaded documents and files on the opportunity (client uploads via the portal land here).
- `list_opportunity_documents(deal_id)` — completed forms auto-archive a PDF to the document library; signed envelopes land here too.

De-duplicate (the same file can appear in both) and present a single numbered
list with each file's name, type, and when it arrived:

```
On "Smith refinance" — 6 files available:
  1. Citywide homeline application (filled) — PDF, today
  2. Credit proposal disclosure (signed) — PDF, today
  3. Payslip 1 — PDF, uploaded 2d ago
  4. Payslip 2 — PDF, uploaded 2d ago
  5. Driver licence — image, uploaded 3d ago
  6. Rates notice — PDF, uploaded 3d ago
```

## Step 3 — Confirm the contents and the order

Let the operator choose which files go in the pack and in what order (lender
packs usually have a required order — cover/application first, then supporting
docs). Default to all, in the order shown, but always show the proposed pack and
get a yes before building:

```
Pack order (say "drop 5" or "move payslips after the licence" to change):
  1. Citywide homeline application (filled)
  2. Credit proposal disclosure (signed)
  3. Driver licence
  4. Payslip 1
  5. Payslip 2
  6. Rates notice
```

If a document you'd expect for this kind of pack is missing, say so here and
offer to run `/outstanding-documents` before building — don't silently ship an
incomplete pack.

## Step 4 — Build the bundle

Confirm the exact inputs the bundler wants first (file IDs, order, output name,
where it attaches) so you call it right the first time:

```
describe_resource("file")
```

Then call `bundle_files` with the chosen file IDs in the confirmed order, giving
the output a clear name (e.g. `Smith-refinance-lender-pack.pdf`). The combined
PDF saves back to the opportunity.

## Step 5 — Show the result

```
✓ Built "Smith-refinance-lender-pack.pdf" — 6 documents, in order, on the Smith refinance opportunity.
  Open it and check the order before it goes to the lender.
```

The pack is for the operator to review — it isn't verified until a human has
opened it (`knowledge/safeguards.md`). Then offer the next step: `/send-email`
to send it, or `/send-for-signing` if it needs signatures.

## Hard rules
- ❌ Never bundle without showing the file list and order for a yes.
- ❌ Never include a file the operator didn't pick.
- ❌ Never send the pack anywhere — assembling is not sending. Hand off to `/send-email` or `/send-for-signing` after.
- ❌ Don't silently ship a pack with an expected document missing — flag it, offer `/outstanding-documents`.
- ✅ Confirm `bundle_files`' real inputs via `describe_resource("file")` before calling it.
- ✅ Save the pack back to the opportunity so it lives with the record.

## Output shape
The numbered candidate list, then the proposed pack (contents + order) for
confirmation, then after building: a one-line result naming the output file, how
many documents it holds, and the reminder to check it before it's sent.

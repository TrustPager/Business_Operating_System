---
name: Outstanding Documents
description: Per client, what supporting documents you asked for versus what's actually arrived — so you chase exactly the right thing instead of "your form's incomplete". Reads the file-upload fields on the forms you sent plus the files on the record, builds a ✓ received / ✗ missing checklist per client, and ranks the chase by how overdue the missing docs are. Document-level (what each client still owes); /form-radar is form-level (which forms are unfinished).
triggers:
  - outstanding documents
  - what documents am I still waiting on
  - what's the client still owe me
  - which docs are missing
  - chase missing documents
  - who hasn't sent their documents
  - document checklist
function_slot: documents
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__list_form_submissions
  - mcp__get_form_submission
  - mcp__describe_resource
  - mcp__list_opportunity_files
  - mcp__list_opportunities
  - mcp__resend_form_submission
status: active
---

# Outstanding Documents

A broker (or anyone collecting supporting docs — insurance, legal, accounting)
loses deals to the two payslips that never arrived. This is the document-level
check-up: for each client, what did we ask for, what's in, and what's still
missing — so the chase names the exact document, not "your form's incomplete".

**How this differs from `/form-radar`:** form-radar tracks the form's submission
status (sent → opened → completed). This tracks the *documents themselves* — the
individual file-upload requests inside those forms plus what's been uploaded to
the record — so a "completed" form can still have a missing document, and a
client with no form can still owe docs.

## Step 1 — Scope it

One opportunity (ask which) or all active opportunities. For "all", keep it to
opportunities in stages where documents are being collected — don't scan won/lost.

## Step 2 — Work out requested vs received, per client

For each opportunity:

**Requested** — the documents we asked this client for:
- The file-upload fields on the forms we sent them. `list_form_submissions(?deal_id=)` to find their forms, then `get_form_submission(submission_id)` to read each field; a file-upload field with no file is a document still outstanding. Confirm the field shape with `describe_resource("form")` if unsure how an empty file field reads.
- Plus any document checklist the operator keeps on the record (a notepad, a custom field). If no requirement is recorded anywhere, say so for that client rather than guessing what they "should" have sent.

**Received** — what's actually arrived:
- `list_opportunity_files(deal_id)` — uploaded documents and files on the record (portal uploads land here).
- File-upload fields that now hold a file.

Match received against requested by what the document is (payslip, ID, rates
notice), not by exact filename.

## Step 3 — Present, chase-first

Per client, a tight checklist; clients with the most-overdue missing docs at the
top:

```
📄 Outstanding documents — 4 clients still owe you something

🔴 Smith refinance — asked 6d ago
   ✓ Driver licence   ✓ Rates notice
   ✗ Payslip (2 of 2)   ✗ Bank statements
   → chase: draft a reminder / resend the form

🟠 Nguyen purchase — asked 3d ago
   ✓ Application form
   ✗ Deposit evidence
   → chase

✅ Fully supplied this week: 3 (no action)
```

## Step 4 — Offer the chase (with approval)

One client at a time, with a yes:
- **Draft a reminder** naming the exact missing docs → hand to `/draft-reply`
  ("just chasing your last 2 payslips and bank statements to keep things moving").
- **Resend the form** if the request went via a form → `resend_form_submission(submission_id)`.
- For "remind clients automatically when a doc is still missing after N days",
  hand to `/automate-this`.

## Hard rules
- ❌ Never auto-send a chase — offer, get a yes, one client at a time.
- ❌ Don't guess a document is required when no requirement is recorded — say "no checklist on this one" and move on.
- ❌ Don't list clients who've supplied everything — count them, don't chase them.
- ❌ Don't confuse this with form completion — a completed form can still have a missing document.
- ✅ Name the exact missing documents in every chase, never "your form's incomplete".

## Output shape
A per-client ✓ received / ✗ missing checklist, ordered most-overdue first, then
the count of fully-supplied clients, and the single most valuable chase to make
first.

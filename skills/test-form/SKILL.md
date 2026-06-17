---
name: Test Form
description: Safely test a form or client portal before any real customer sees it. Checks the form's CRM field mapping, sends a test to the operator (or a test contact, never a real client), walks through submitting it, and confirms the answers wrote back onto the record correctly. Answers the question "how do I check this works without going to a customer?". The verify-before-a-customer discipline applied to forms.
triggers:
  - test this form
  - check this form works
  - test my form without a customer
  - does this form map correctly
  - test the client portal
  - send myself a test form
---

# Test Form

Before a form goes to real clients, confirm it actually captures and maps the
data. Never test on a real customer — use the operator or a test contact.

## Step 1 — Check the mapping first

Open the form and check its CRM field mapping. If fields are unmapped (the form
shows "N fields not mapped to a CRM variable"), the answers won't write back —
say so and offer to map them first (`/wire-form`, or Claude can map them). Show
which fields are unmapped before testing, so a green test doesn't hide a real gap.

## Step 2 — Pick a safe target

Send to **the operator's own email** or a dedicated **test contact** — never a
real client (`knowledge/safeguards.md`). If there's no test contact, create one
(e.g. "Test Applicant", the operator's email) so the test data doesn't pollute a
real record. Link it to a test opportunity, not a live deal.

## Step 3 — Send and submit the test

Send the form to that target (`send_form`), then walk the operator through
opening and submitting it with sample answers (give them the link). For a client
portal, send the portal and have them submit through the embedded form the same
way. Respect the approval queue (202 = queued, surface it).

## Step 4 — Confirm the answers landed

After submission, check the test record: did each answer write to the right CRM
field? Report it plainly:

```
Tested "Initial client discovery" → test contact (your email):
  ✓ 12 of 14 answers mapped onto the record correctly
  ⚠ "Co-applicant income" didn't land — it's not mapped to a CRM field
  ⚠ "Employment type" wrote to Notes instead of the Employment field
Fix the 2 mappings, then it's safe to send to clients.
```

## Step 5 — Clean up

Offer to remove the test submission / test record so it doesn't clutter the
workspace once the operator's seen the result.

## Hard rules
- ❌ Never test against a real customer or a live opportunity — operator/test contact only.
- ❌ Don't report "works" if fields are unmapped — an unmapped field silently drops data.
- ❌ Don't route around the approval queue.
- ✅ Check mapping before sending, and verify write-back after submitting — both halves.
- ✅ Offer to clean up the test data afterwards.

## Output shape
A pre-test mapping check (any unmapped fields named), then after submission a
field-by-field result of what mapped vs didn't, and a clear "safe to send / fix
these first" verdict.

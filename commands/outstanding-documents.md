---
description: Per client, what you asked for versus what has arrived, so you chase exactly the right thing.
---

Run the **Outstanding Documents** skill.

Invoke the skill at `skills/outstanding-documents/SKILL.md`. Follow it exactly:
for one opportunity or across all active ones, work out which documents were
requested (file-upload fields on the forms you sent, plus any checklist on the
record) versus which have been received (uploaded files + completed file
fields), and present a per-client ✓ received / ✗ missing checklist, most-overdue
first. Offer the chase per client (draft a reminder via `/draft-reply` or resend
the form via `resend_form_submission`), one at a time, with a yes. Never
auto-send. This is document-level (what each client still owes); `/form-radar` is
form-level (which forms are unfinished).

---
name: Form Radar
description: Show where every form you sent stands — the sent → opened → completed funnel, who started but didn't finish (nudge them), who never opened it and is going stale (chase), and what completed this week. Hottest follow-ups first.
triggers:
  - form radar
  - who hasn't filled in the form
  - check my forms
  - which forms are outstanding
  - who opened but didn't complete the form
  - chase incomplete forms
  - form submission status
---

# Form Radar

Owners send intake/onboarding forms and then don't notice the client who opened
it, started, and bailed — or the one who never opened it at all. This is the
check-up on every submission.

**The buckets that matter:**
- **Started but not completed** — opened or in-progress, never submitted. A
  short nudge usually finishes them.
- **Sent but never opened, going stale** — chase or resend.

Source of truth: [`knowledge/form-method.md`](../../knowledge/form-method.md)
— §4 (the submission lifecycle) and §5 (automating it).

## Step 1 — Fetch the digest

```bash
python skills/form-radar/fetch.py
```

One call: lists every submission, computes the funnel, buckets the follow-ups
(started-not-completed, sent-never-opened-stale, recently completed),
oldest-first. `--stale-days N` tunes the stale threshold (default 5).

Fallback if it can't run: `mcp__trustpager__list_form_submissions` — raw list,
no funnel; prefer the script.

## Step 2 — Present, follow-ups first

```
📋 22 forms out — 12 completed, 4 started (not finished), 5 sent (unopened), 1 expired

✏️  STARTED — NOT FINISHED (4)  ← a nudge usually closes these
  → "New Client Intake" — opened 3d ago, in progress. → nudge / draft a reminder
  → "Onboarding Questionnaire" — opened 6d ago, not submitted. → follow up

⏳ SENT — NEVER OPENED, going stale (5)
  → "Intake — Northside" — sent 8d ago, never opened. → resend or call

✅ Completed this week: 12  (PDFs auto-archived to their opportunities)
```

## Step 3 — Offer the follow-up actions (with approval)

One at a time, with a yes:
- **Resend** an unopened-stale submission → `mcp__trustpager__resend_form_submission(submission_id)`.
- **Draft a nudge** to a started-not-finished recipient → hand to `/draft-reply`
  ("saw you got started on the form — anything I can help with to finish it?").
- **Void** a dead/duplicate submission → `void_form_submission(submission_id)` —
  name it, get a yes.

For "nudge automatically whenever someone opens but doesn't finish", hand to
`/automate-this` on the `form_opened` trigger.

## What to never do

- ❌ Don't dump all submissions flat — bucket by follow-up urgency.
- ❌ Don't auto-resend or auto-void — offer, get a yes, one at a time.
- ❌ Don't chase `completed` ones — count them, move on.
- ❌ Don't chase a submission the operator voided on purpose.

## Output shape

Headline funnel tally, then STARTED-NOT-FINISHED, then SENT-UNOPENED-STALE, then
the completed count — and the single most valuable follow-up to make first.

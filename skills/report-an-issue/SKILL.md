---
name: Report an Issue
description: File a bug report or feature request to the TrustPager team without leaving Claude. Works out whether it's a bug or a feature, gathers the few details that make it actionable, and files a clean, well-structured service request via create_service_request so the team can investigate and fix fast. Use for "this is broken", "this isn't working", or "I wish it could do X".
triggers:
  - report an issue
  - report a bug
  - this is broken
  - this isn't working
  - request a feature
  - file a service request
  - tell the team about a problem
---

# Report an Issue

The team runs a service-request queue: a clear report gets fixed faster than a
vague one. This skill captures just enough to make the request actionable, files
it, and tells the operator plainly what happens next. The quality of the report
directly shapes how fast it's resolved, so get the few key details, but keep it
light.

## Step 1 — Bug or feature?

From what the operator said, decide:
- **Bug** — something that should work but doesn't / behaves wrong.
- **Feature request** — something the platform doesn't do yet that they want.
- **Not sure / question** — if it's really "how do I do X", hand off to
  `/show-me-how` instead of filing a request.

## Step 2 — Gather only what makes it actionable (one short batch)

**For a bug**, get (ask only for what's missing):
- **What you expected** to happen.
- **What actually happened** (the wrong behaviour, any error text).
- **Where** — the screen/feature, and the specific record if relevant (grab the
  URL or record name from the workspace where you can, rather than asking).
- **How to reproduce** — the steps that trigger it, if known.
- **How much it's hurting** — blocking work / annoying / minor — to set priority.

**For a feature request**, get:
- **The use case** — what they're trying to achieve and why.
- **The outcome** they want (what "done" would look like for them).

Don't over-interrogate. A few precise details beat a long form.

## Step 3 — File it

Call `create_service_request` with:
- **title** — one specific line ("Booking from a company record forces a manual
  opportunity link"), not "it's broken".
- **description** — the complete report in plain text: expected vs actual + where
  + repro for a bug, or use case + outcome for a feature. This is what the team's
  investigator reads first, so make it self-contained.
- **category** — `bug_report` or `feature_request`.
- **priority** — from how much it's hurting (high if it blocks work).
- Link the relevant record id if there is one.

If the call returns HTTP 202 (queued for approval), that's fine for a request —
surface it per `knowledge/safeguards.md`; don't retry.

## Step 4 — Confirm, plainly

Short and reassuring (`knowledge/communication-voice.md`), and set the right
expectation. The team fixes it, verifies it works, then tells you how to use it:

```
✓ Logged with the team: "Booking from a company record forces a manual link" (bug, high).
The team will investigate and fix it, confirm it's working, then let you know how
to use it. You don't need to chase anything.
```

Do not promise a timeframe you don't control.

## Hard rules
- ❌ Don't file a vague title/description — a clear report is the whole value. If
  a key detail is missing, ask one short question first.
- ❌ Don't turn a "how do I" into a service request — route to `/show-me-how`.
- ❌ Don't promise when it'll be fixed.
- ✅ Pull the record/URL from the workspace where you can instead of asking.
- ✅ Confirm in the team voice: what was logged + what happens next, then stop.

## Output shape
A one-line "logged with the team" confirmation naming the title, category, and
priority, plus one plain line on what happens next. If a detail was missing, the
one short question comes first.

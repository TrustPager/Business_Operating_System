---
name: Transcript Summary
description: Turn a recorded call or meeting into a usable document — a clean summary, the decisions, the action items, and the next step — logged to the opportunity timeline. Works on the latest transcript, a named contact's, or a specific one.
triggers:
  - transcript summary
  - summarise my last call
  - summarise that meeting
  - what did we agree on the call
  - turn the call into notes
  - write up the meeting
  - action items from the call
---

# Transcript Summary

The operator recorded a call or meeting and wants it turned into something
useful — a summary, the decisions, the action items, the next step — without
re-listening to 40 minutes of audio. This skill finds the transcript, summarises
it, and logs the result where the rest of the workspace can see it.

## Step 1 — Find the transcript

Ask which call if it's ambiguous, otherwise default to the most recent:

- **Latest / "my last call"** → `mcp__trustpager__list_transcripts(limit=5)`, take
  the most recent (or show the 5 and let them pick).
- **For a named person / deal** → `list_transcripts` filtered to that contact /
  opportunity, or find the opportunity first then its transcripts.
- **A specific one** → they give you the id.

Note: most plain phone calls aren't auto-transcribed — only Notetaker meetings
and voice-agent calls carry rich text. If there's no transcript body, say so
plainly (nothing to summarise) rather than inventing content.

For mining *many* transcripts at once (brand voice, positioning), that's
`/build-customer-voice` — this skill is for turning *one* conversation into a
document.

## Step 2 — Read + summarise

`mcp__trustpager__get_transcript(id)` for the full text. You can also use
`mcp__trustpager__ai_transcript_summary(id)` for a first-pass summary (costs
credits — say so), then tighten it. Produce, in the operator's plain language:

```
## <Contact / company> — <call type>, <date> (<duration>)

**Summary** — 2-3 sentences: what the call was about and where it landed.

**Decisions**
- …

**Action items**
- [ ] <who> — <what> — <by when, if said>

**Next step** — the one concrete thing that moves this forward.

**Notable quotes** (optional) — 1-2 verbatim lines if they capture a real concern.
```

Pull only what's actually in the transcript. Don't invent action items the
parties didn't agree to.

## Step 3 — Log it where it's useful (with approval)

Offer to put the write-up where the workspace can use it — confirm which:
- **On the opportunity/contact timeline** → `mcp__trustpager__add_note(...)` (or
  `log_meeting`) linked to the deal/contact, so it's there next time anyone opens
  the record. This is the usual default.
- **As a document** → if they want a shareable artefact, draft it and offer
  `/build-document` or save via the documents library.
- **As tasks** → offer to turn the action items into tasks
  (`create_task` per item) assigned + dated. One confirmation for the set.

End with the next step and the offer: *"Want me to log this to the deal timeline
and turn the action items into tasks?"*

## Hard rules

- **Only summarise what's in the transcript.** No invented decisions, no
  action items nobody agreed to.
- **Flag empty transcripts** — don't fabricate a summary for a call with no text.
- **Get approval before writing** notes/tasks to the workspace, and before any
  credit-costing AI summarise call (say it costs credits).
- **Use the operator's language**, not corporate meeting-minutes register.

## Output shape

The structured write-up first, then the offer to log it to the timeline + create
the action-item tasks.

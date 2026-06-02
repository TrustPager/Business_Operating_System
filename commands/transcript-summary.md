---
description: Turn a recorded call or meeting into a usable document — summary, decisions, action items, next step — logged to the opportunity timeline. Works on the latest transcript, a contact's, or a specific one.
---

Run the **Transcript Summary** skill.

Invoke the skill at `skills/transcript-summary/SKILL.md`. Find the transcript
(`list_transcripts`, default to most recent or let the operator pick), read it
(`get_transcript`, optionally `ai_transcript_summary` — say it costs credits),
and produce the structured write-up: summary, decisions, action items, next step.
Only summarise what's actually in the transcript; flag empty ones rather than
inventing content. Offer to log it to the deal/contact timeline (`add_note` /
`log_meeting`) and turn action items into tasks — with approval.

For mining many transcripts at once, that's `/build-customer-voice`, not this.

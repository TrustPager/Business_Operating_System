---
description: Mine ≥5min call + meeting transcripts into a verbatim customer-voice synthesis. Foundation for every marketing strategy artefact downstream.
---

Run the **Build Customer Voice** skill.

Invoke the skill at `skills/build-customer-voice/SKILL.md`. Follow its
instructions exactly: pull transcripts via the `trustpager` MCP
(`list_transcripts` to enumerate, `get_transcript` for each), read every
one end-to-end (filter out the host's voice), then write
`customer-voice-synthesis.md` with the 10 prescribed sections. Quote
verbatim with `[Speaker, transcript]` attribution. Report back
under 200 words.

If the operator hasn't said where to write the synthesis, default to
`transcripts/<UTC-date>/customer-voice-synthesis.md` alongside the
pulled transcripts.

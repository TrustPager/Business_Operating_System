---
description: Turn the words your customers use into a customer-voice doc that grounds all your marketing.
---

Run the **Build Customer Voice** skill.

Invoke the skill at `skills/build-customer-voice/SKILL.md` and follow it
exactly. Default to the keyless mode: gather the customer's actual words from
whatever the owner pastes (reviews, testimonials, support emails, call notes)
or from local files (convert each with `tools/markitdown_convert.py` first),
read every source end-to-end, keep the customer's voice and drop the owner's,
then write `customer-voice-synthesis.md` with the 10 prescribed sections.
Quote verbatim with source attribution. Report back under 200 words.

Do NOT demand recorded calls or a connected workspace. The richer
transcript-mined version is the deeper mode the skill offers only when the
workspace is connected, never the price of entry.

If the owner hasn't said where to write it, default to
`marketing-strategy/<BrandName>/customer-voice-synthesis.md` (or alongside the
source files they pointed you at).

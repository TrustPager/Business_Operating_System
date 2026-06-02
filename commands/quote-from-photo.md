---
description: Turn a site photo (plus a voice memo or a few notes) into a drafted proposal or quote — scope read off the image, line items, and a written proposal the operator reviews before it goes anywhere.
---

Run the **Quote From Photo** skill.

Invoke the skill at `skills/quote-from-photo/SKILL.md`. Read the attached site
photo(s) directly, layer in any voice-memo transcript / notes, and state clearly
what you can see vs what you're assuming (a photo can't measure). Draft the scope
+ line items + proposal in the operator's voice, pulling product names/prices
from their catalogue (`list_products`) — never invent prices; leave them blank
for the operator if there's no price list. Flag the unknowns (measurements,
access) loudly.

Draft only. When approved, offer the hand-off — turn it into a signing proposal
(`/build-document` → `/send-for-signing`), attach it to an opportunity, or send
as-is (`/send-email`). Don't create or send anything unprompted.

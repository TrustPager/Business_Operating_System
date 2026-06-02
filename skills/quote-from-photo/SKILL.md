---
name: Quote From Photo
description: Turn a site photo (plus a voice memo or a few notes) into a drafted proposal or quote in about a minute — scope read off the image, line items, and a written proposal the operator reviews before it goes anywhere.
triggers:
  - quote from photo
  - quote from this picture
  - draft a quote from this site photo
  - here's a photo of the job
  - turn this photo into a proposal
  - estimate from this image
---

# Quote From Photo

A trades / on-the-tools operator snaps a photo on site, mutters a voice memo, and
wants a proposal drafted before they've left the driveway. You read the image,
turn it into scope + line items, and draft the quote. The operator reviews before
anything is sent or saved — you're drafting, not committing.

## Step 1 — Read what you were given

The operator attaches one or more **site photos**, and usually a **voice memo
transcript or a few typed notes** (budget, timeline, the bit the photo doesn't
show). Work from all of it:

- **Read the photo(s) directly.** Describe back what you see that's quote-
  relevant — the space, materials, condition, scope signals, anything ambiguous.
- **Layer in the notes/voice memo** — they carry the things a photo can't
  (the client's budget, the deadline, "they also want the back fence done").
- **Surface your assumptions and the unknowns.** A photo can't tell you square
  meterage or what's behind a wall. List what you're assuming and what you'd need
  to confirm — don't silently invent a number.

## Step 2 — Draft the scope + line items

Pull from the operator's own products/services where they exist
(`mcp__trustpager__list_products`) so pricing and names match their catalogue —
don't invent product names or prices they don't use. Present:

```
## Quote — <job, from the photo> — <client, if known>

**Scope (read from the photo + your notes)**
- …

**Line items**
| Item | Qty | Unit | Notes |
|------|-----|------|-------|
| …    |     |      |       |

**Assumptions** — what I assumed from the image (confirm before sending).
**Need to confirm** — measurements / access / materials a photo can't show.

**Draft proposal**
<the written proposal in the operator's voice>
```

If you don't have their price list, draft the scope + line-item structure and
leave the prices for the operator to drop in — flag that clearly rather than
guessing rates.

## Step 3 — Hand off (with approval)

This skill DRAFTS. When the operator's happy with it, offer the next step —
don't do it unprompted:

- **Make it a real signing document** → `/build-document` (turn the proposal into
  a template/envelope) → `/send-for-signing`.
- **Attach to an opportunity** → create/find the deal, add the products
  (`add_opportunity_product`), save the proposal as a note or document.
- **Just send the text** → `/draft-reply` / `/send-email` with the proposal.

End with: *"That's the draft off the photo. Want me to turn it into a signing
proposal, attach it to a deal, or just send it as-is? Confirm the measurements
and prices first — I read scope off the image but I can't measure it."*

## Hard rules

- **Read the image; don't hallucinate scope.** State what you can see vs what
  you're assuming. A wrong assumption in a quote is a wrong quote.
- **Never invent prices or product names** the operator doesn't use — pull from
  their catalogue or leave prices blank for them to fill.
- **Draft only.** Don't create the deal, document, or send anything without the
  operator's go.
- **Flag the unknowns loudly** — measurements, access, what's behind the wall.

## Output shape

What you see in the photo, then the scope + line items + assumptions + need-to-
confirm, then the draft proposal, then the hand-off options. Fast and concrete —
the operator wants a usable draft in a minute, not a questionnaire.

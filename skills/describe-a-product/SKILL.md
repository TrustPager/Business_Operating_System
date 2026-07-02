---
name: Describe A Product
description: Turn one product (a photo, or a few notes) into an on-brand product description ready for an online store, a listing, or a catalogue, in the owner's voice, leading with what the buyer gets. Reads the brand voice if it has been set, falls back to the owner's words if not. Keyless, positive-only, outcome-led. One product per run.
triggers:
  - describe a product
  - write a product description
  - describe this product
  - write the listing for this
  - product description from this photo
  - write copy for this product
  - turn this product into a listing
  - description for my store
  - write the product blurb
  - product copy in my voice
function_slot: social
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---

# Describe A Product

You turn one product into the words that sell it: an on-brand product
description for an online store, a marketplace listing, or a printed
catalogue. The owner shows you the product (a photo, or a few notes about it)
and you write the description in their voice, leading with what the buyer
gets. This is the instant win for a product-seller or retail owner who has a
shelf of items and a blank "description" box waiting on each one.

This runs keylessly day one: no accounts, no files beyond the photo or notes
the owner gives you. The real, finished artifact is the publish-ready
description itself.

## Bounded: one product per run

One product per run. If the owner has a whole range to write up, do the first
one properly so they can see the shape and the voice, then offer the next as a
fresh run. A sharp description they can paste straight in beats a rushed batch.
(A whole catalogue at once is a different, heavier job; keep this one bounded.)

## Step 1 — Read the product

The owner arrives one of two ways, and either is fine:

| The owner has... | What you do |
|---|---|
| **A photo of the product** | Read the image directly. Describe back what you can see that's sales-relevant: the form, the materials, the colour, the finish, the size cues, the detail that makes it feel premium or handmade or sturdy. |
| **A few notes / a spec** | Take the notes as the brief: the name, what it's made of, the size, the price, what makes it different. |

Usually it's both, a photo plus a line or two. Work from all of it.

- **Surface what you can see versus what you're assuming.** A photo can't tell
  you the exact dimensions, the material, or the price. Name what you're
  reading off the image and what you'd need the owner to confirm. Never invent
  a measurement, a material, or a feature the product may not have.
- **Ask one sharpening question only if the product is genuinely thin** (a
  blurry photo, no name, no idea who it's for). One good answer beats a vague
  description built from nothing. For example: *"Lovely piece. Who's it for,
  and what's the one thing you'd want a buyer to notice first?"*

## Step 2 — Read the brand voice if it's there (graceful fallback if not)

Look for the owner's brand voice doc, usually at
`marketing-strategy/<BrandName>/voice.md` (built by `build-brand-strategy`, or
captured in their first brand brief). If it exists, read it and write to it:
the tone, the signature moves, the vocabulary their customers actually use,
and the register their voice avoids.

If there's no voice doc yet, that's fine. This still runs keyless. Fall back to
the owner's own words and how they describe the product, and say so plainly:
*"I don't have your brand voice on file yet, so I've written this from how you
described it. We can lock in your voice properly whenever you'd like."* Never
stall waiting for a voice doc. A real description in their words today beats a
perfect one that never ships.

The shared reference for how customer-facing copy should sound is
[`knowledge/communication-voice.md`](../../knowledge/communication-voice.md).

**When the "product" is a service package, a bundle, or a lead magnet:**
name it with 3-5 of the five naming parts (business-method.md §7.5), the
result part outcome-led (§18); a diagnostic magnet sells the gain (§10.4).
And when a listing stops pulling, rename before rebuilding — the refresh
order starts with the cheap changes (§7.5).

## Step 3 — Write the description

A product description earns the buyer's confidence and then their click. Shape
it so it works wherever it lands (a store page, a marketplace listing, a
catalogue line):

1. **Open with what the buyer gets.** Lead with the outcome or the feeling the
   product delivers, not a dry spec dump. The first line is the hook.
2. **Then the substance.** A short, vivid paragraph (or a few) on what it is,
   what it's made of, and what makes it worth choosing, in the owner's voice.
3. **The concrete details, where you have them.** Materials, size, what's
   included, care, the price if the owner gave it. Use only what the owner
   confirmed; flag anything you'd need them to fill (`[confirm: dimensions]`).
   Named inclusions with the benefit in the name out-persuade a bare list
   (business-method.md §7.3).
4. **A short, scannable spec / highlights list** when it helps a buyer decide
   (a few bullet-style lines of the key facts), so the page reads fast.
5. **One clear next step** if the channel wants one (add to cart, enquire,
   visit), stated plainly.

Match the length to the channel: a marketplace listing wants tight and
keyword-natural; a brand store page can breathe a little more. One product,
one description.

**Pre-flight — the value-equation check (internal, silent).** Before
handing over, check the draft against the value equation
(business-method.md §6). This is an internal checklist, NOT four new owner
questions:

- Does the copy name the **Arrival** — the destination, not the deliverable?
- Does it back the **Belief** with real, confirmed proof only?
- Does it shorten the felt **Wait** where true (in stock, ships today)?
- Does it cut the perceived **Work** (what's included, no assembly)?

Faster-and-easier is the higher-leverage half (§6).

## Step 4 — Before you output anything customer-facing: positive/outcome-led, and NO em dashes

The description is **customer-facing output**, so it obeys the content rule:

- **Positive-only, outcome-led, always.** Name what the buyer gets, what it
  lets them do, how it makes their day better. Describe the win, never the
  absence. Not "stop settling for flimsy ones", but "built to last the season
  and the one after it".
- **No invented proof.** Don't put a fake review, a made-up "bestseller" claim,
  a fabricated material, or a spec the owner didn't confirm into the copy.
  Anchor in what's real about the product.
- **NO em dashes anywhere in the copy.** Use a comma, a colon, parentheses, or
  two sentences. This holds for every word that ships. (A field test caught
  this being missed; check the output before handing it over.)

## Step 5 — Hand it over, ready to publish

Give the owner copy they can paste straight into the listing, plus a light
note on whose voice it's in and anything left to confirm:

```
Product description for "<product name>"

<the publish-ready description, with the highlights list>

Voice note: written from your brand voice on file (or, if none: from how you
described it). Left for you to confirm: <dimensions / price / material>.
Want me to write the next one?
```

Stay bounded: one product per run. A whole range is a sequence of fresh runs,
each a clean, finished description.

## Hard rules

- **Keyless and reasoning-only.** Needs no accounts and no files beyond the
  photo or notes the owner gives you. The finished description is the win.
- **One product per run.** Write the first one properly; offer the rest as
  fresh runs.
- **Read the product; don't hallucinate it.** State what you can see versus
  what you're assuming. Never invent a material, a measurement, a feature, or
  a price the owner didn't confirm. Flag gaps as `[confirm: …]` placeholders.
- **The owner's voice wins.** Write to the brand voice doc if it exists;
  otherwise reflect the owner's own phrasing.
- **Before you output anything customer-facing: positive-only, outcome-led,
  and NO em dashes** (use commas, colons, parentheses, or separate
  sentences). The copy names the win, never the absence; no invented proof.

## Output shape

The publish-ready product description for one product (hook, substance,
confirmed details, a short highlights list, one next step), then a one-line
note on whose voice it's in, any `[confirm: …]` placeholders left, and the
offer to write the next product as a fresh run.

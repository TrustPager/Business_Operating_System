---
name: Write Post Copy
description: Draft the publish-ready words for a social post in your own voice: the caption or body that goes out with the graphic, built from a planned content idea or a one-line brief. Reads your brand voice if set, falls back to your words if not. Optionally drafts the paid-ad primary text and a headline variant. Pairs with make-social-post, which makes the picture. Keyless.
triggers:
  - write post copy
  - draft a caption
  - write the caption for this post
  - draft the post body
  - write the words for this post
  - draft ad copy
  - write the primary text for an ad
  - caption in my voice
  - write a linkedin post
  - turn this content idea into a post
function_slot: social
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
produces_customer_facing_copy: true
---

# Write Post Copy

You write the words a post goes out with: the caption, the body, the line under
the picture. The graphic studio handles the on-image headline (that's the job of
`make-social-post`). This is the publish-ready text the owner copies straight
into the platform. One post per run, or a small matched set for a single
campaign idea. Always in the owner's own voice.

This pairs with `make-social-post`. That one makes the picture, this one writes
the words. They run happily together (a graphic plus its caption for the same
idea) or each on its own.

## Step 1: Find the source, a planned idea or a one-line brief

There are two ways the owner arrives, and either is fine:

| The owner has... | Where it comes from | What you do |
|---|---|---|
| A planned content idea: a row from their content plan (the platform, the angle, the date, a rough topic) | the `plan-my-content` app, or pasted in | Read the row, pull the angle and platform, then write the post that fills it |
| A standalone brief: "write me a post about the new same-day quotes thing" | straight from the owner | Take the brief as the idea and write from it |

If they hand you a planned row, honour what it already decided: the platform,
the angle, the rough hook. Don't re-litigate the plan, fill it. If they give you
a loose brief, that brief is the idea, so write from it.

When the idea is genuinely thin (a one-word topic, no angle, no audience), ask
ONE sharpening question before drafting, not five. For example: *"Happy to write
this. What's the one thing you'd want a reader to take away from it?"* One good
answer beats a vague post built from nothing.

## Step 2: Read the brand voice if it's there (graceful fallback if not)

Look for the owner's brand voice doc, usually at
`marketing-strategy/<BrandName>/voice.md` (built by `build-brand-strategy`, or
captured in their first brand brief). If it exists, read it and write to it:

- the tone adjectives and signature moves,
- the **vocabulary available**: phrases lifted from how their customers actually
  talk. Reach for one when it fits, and don't stuff every line with them.
- the **watch-out-for** register: the jargon and hype words their voice avoids,
- the words that are **fine** despite looking fancy: normal business English the
  owner genuinely uses, which you should not over-sanitise out.

If there's no voice doc yet, that's fine. This still runs keyless. Fall back to
the owner's own words from the brief and how they talk, and say so plainly:
*"I don't have your brand voice on file yet, so I've written this from how you
described it. We can lock in your voice properly whenever you'd like."* Never
stall waiting for a voice doc. A real post in their words today beats a perfect
one that never ships. The brand-voice path is the upgrade, not the entry fee.

The shared reference for how customer-facing messages should sound is
[`knowledge/communication-voice.md`](../../knowledge/communication-voice.md).
The strategy artifacts this reads slot into the pipeline described in
[`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md).
(That method's CRM and auto-queue layers are connected-tier deepeners, not
something this app needs. This writes copy from reasoning alone.)

## Step 3: Write the post for its platform

A caption is not a billboard (that's the on-image headline). It's the few lines
that earn the scroll-stop and point at the next step. Match the shape to where
it's going:

| Platform | Shape that lands |
|---|---|
| Instagram | A warm hook line, two or three short lines of substance, one clear next step, then a small set of relevant hashtags |
| LinkedIn | A strong first line (it's the only line shown before "see more"), short punchy paragraphs, a human close, one ask |
| X (Twitter) | One tight thought that stands alone; trim every word that isn't load-bearing |
| Facebook | Conversational, a touch longer is OK, one clear call to action |

Across all of them:

1. **Open with a strong hook, not a wind-up.** The first line has to earn the
   scroll-stop. No "So I wanted to share something..." preamble. Reach for the
   angle that fits the owner's brand and their audience; ad callouts that name
   the person land well ("Brunswick landlords: ...").
2. **One idea per post.** If two ideas are fighting, that's two posts. Pick the
   stronger one for this run.
3. **One clear next step.** Book, reply, read, visit: one ask, stated plainly,
   with a raw link as its own visible text when there's a link (never "click
   here", never breadcrumb navigation).
4. **Sound like a person.** Short sentences. Their words. No jargon, no
   system-internals, no hype register.

**The craft under the hook** — the contrast word that creates the curiosity gap
(*most people think X, but…*), naming an idea so it sticks (term branding), and
condensing the point so a reader can retell it in one line (atomic sharability) —
lives in [`knowledge/storytelling-method.md`](../../knowledge/storytelling-method.md).
Reach for it when a post reads flat or the first line won't earn the scroll-stop.
Framing stays the owner's choice; the file supplies the mechanics, not the register.

## Step 4: Optional, the ad variant (only if they ask)

If the owner wants this as a paid ad too, add a second block. Don't replace the
organic caption, sit it alongside:

- **Primary text**: the body that runs above the creative. Tighter and more
  direct than the organic caption. Lead with your strongest line first (assume
  it gets truncated), make the value plain fast, one call to action. Structure
  it per the ad anatomy (business-method.md §10.6): call out the person, make
  the value vivid, one CTA with a real reason to act now.
- **Headline variant**: a single short line (think 5 to 7 words) for the ad's
  headline field that complements the on-image headline rather than repeating
  it word for word.

Label the two clearly so the owner knows which is the organic caption and which
is the paid version.

## Step 5: Hand it over, ready to publish

Give the owner copy they can paste straight in, plus a couple of light choices.
Never a pile of homework:

```
Post copy for Instagram (your "same-day quotes" idea)

Caption:
Your quote, same day, every time.
We turned the bit that used to take a week into something that lands while
the kettle's still warm. You get a clear number fast, they get to say yes
fast, and the job's moving before the day's out.
Want yours that quick? Book a 15-min look: https://example.com/book
#localtrades #smallbusiness #samedayservice

Voice note: written from your brand voice on file (lifted "while the kettle's
still warm", that's yours). Want a paid-ad version of this too?
```

If you wrote a small matched set for one campaign idea (say the same message for
Instagram and LinkedIn), show each clearly labelled: same core message, shaped
for its platform. Stay bounded: one idea per run, not a month's calendar.

## Hard rules

- **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and the marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`.
- **Regulated shapes have extra limits (check the business shape first).** Read
  the profile's business shape: prefer an explicit `Business shape:` line in
  `## How the business is running` (start-here records it, with any regulated
  override spelled out) and fall back to inferring it from the `## My business`
  context in the workspace `CLAUDE.md`. For a clinic / appointment or finance shape (and insurance /
  legal), run every draft through the regulated compliance row: sell the
  logistics and the care, never treatment or result outcomes; no outcome
  testimonials, no before/after result claims, no result guarantees (service-level
  only), and no urgency or price pressure on clinical or advice decisions. The
  per-shape overrides are in `content-rules.md` §4, which points to
  `industry-notes.md` and `business-method.md` §7.2 / §15.
- **Keyless and reasoning-only.** This needs no accounts and no files beyond
  what the owner gives you. The real, finished artifact is the publish-ready
  copy itself.
- **The owner's voice wins.** When a brand voice doc exists, write to it. When
  the owner's actual phrasing differs from any guideline, the owner's phrasing
  wins. Reflect their words back so it reads as *"that's exactly how I'd say it."*
- **One idea per post, one clear next step.** If it needs two asks or two ideas,
  it's two posts. Write the stronger one.
- **When the post's next step points at an offer or lead magnet**, use its
  five-part name (business-method.md §7.5).
- **Bounded scope.** One post, or one small matched set for a single campaign
  idea, per run. A whole content calendar is a different job (that's the
  `plan-my-content` app).

## Output shape

The publish-ready post copy, labelled by platform, ready to paste, plus a
one-line note on whose voice it's written from (brand doc on file, or the
owner's own words) and any single open choice left for them. If an ad variant
was asked for, the primary text and headline variant sit alongside, clearly
labelled.

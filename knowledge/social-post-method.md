# Social Post Method

The canonical knowledge for designing branded social posts using the bundled
studio at `studio/social/`. This is the operator-facing summary; the full
rules live inline in the studio's source (deliberately co-located with the
code so corrections don't drift):

- [`studio/social/CLAUDE.md`](../studio/social/CLAUDE.md)
  — post anatomy, the four formats, the questions to ask, samples.json fields
- [`studio/social/src/templates/SocialPost.jsx`](../studio/social/src/templates/SocialPost.jsx)
  (JSDoc header) — canonical layout, the `FORMATS` scale table, full data shape

When in doubt, the inline rules win. This file is the executive summary.

---

## A post is a billboard, not a paragraph

Someone scrolls past it in under a second. One message, big, legible at
thumbnail scale. If you need two sentences to land the idea, it's two posts.

- ✅ *"Run your whole business from one place"*
- ❌ *"TrustPager brings your leads, quotes, follow-ups, scheduling and
  invoicing into a single workspace so nothing slips"*

---

## The four formats

| Format | Size | Layout | Use it for |
|---|---|---|---|
| Instagram · Square | 1080 × 1080 | portrait | the IG feed default |
| Instagram · Portrait | 1080 × 1350 | portrait | more feed real estate / reach |
| LinkedIn | 1200 × 627 | landscape | a LinkedIn post or link image |
| X (Twitter) | 1600 × 900 | landscape | an X post (16:9) |

Same component, same copy — one `samples.json` entry per format. Portrait
formats stack the visual under the headline; landscape formats put it to the
right. Write the message once, render the sizes you need.

---

## Headline rules

**Lead with the reader's outcome, not your feature's mechanics.**
- ✅ *"Your back office, finally on autopilot"*
- ❌ *"Our automation engine processes your workflow triggers"*

**Exactly one gradient accent word (`accentWord`).** It picks up the brand
gradient fill (teal → mint → blue). One — give the eye a single place to land.

**At most one serif emphasis word (`emphasisWord`).** Optional. Adds a human,
editorial beat — *whole*, *finally*, *yours*, *real*. Skip it if the headline
is already tight.

**Short beats clever.** 3–8 words. Use `\n` to control the line break so the
shape reads well.

**Open a curiosity gap where you can.** The strongest headlines carry a contrast —
the distance between what the reader expects and what you say is true. The craft for
this (contrast words, naming an idea so it sticks) is in
[`storytelling-method.md`](storytelling-method.md). It's the mechanic; the framing
below is the house choice.

**Positive framing only.** State the outcome, not the failure you're avoiding.
- ✅ *"Every lead followed up, automatically"*
- ❌ *"Stop letting leads slip away"*

---

## Choosing the visual (optional)

Pick at most one. A clean headline-only post is great for announcements.

| Visual | Shape | Use it for |
|---|---|---|
| `card` | a product-ish list (label/value rows + status pill) | "look inside the product" — a pipeline, a week's numbers |
| `stats` | a 1–3 metric strip (big number + sub) | proof — *"9x faster"*, *"+34% MoM"*, *"11 hrs saved"* |
| `quote` | a testimonial with an initials monogram (or a photo via `quote.avatar`) | social proof — a customer's words |

The card chrome stays on the brand palette (teal / green / blue / slate).
Don't reach for red / orange / purple to "make a number pop" — the gradient
accent and one tone tag are enough.

---

## Banned framings

- **Negative / fear** — "Stop losing leads", "Don't let jobs slip". Flip to
  the positive outcome.
- **Surveillance vibes** — "Track everything your team does". Reframe as
  empowerment.
- **Third-party vendor names** — anywhere a follower would see them. Your
  brand only.
- **Markup / pricing math** — never expose cost formulas in a post.
- **Wall of text** — if the headline needs a comma-spliced second clause to
  make sense, cut it.

---

## Common mistakes (don't re-walk)

| Mistake | Fix |
|---|---|
| Two ideas in one post | Split into two posts, one idea each |
| Two gradient accent words | One. Pick the outcome word |
| Headline clipped on LinkedIn (627px is short) | Shorten the headline or drop the visual — landscape has the least vertical room |
| A visual card with red/orange/purple to "pop" | Brand palette only; the gradient accent already carries the eye |
| Vendor name visible to followers | Scrub it — your brand only |
| Declared done from the browser preview | Render the PNG (`npm run shoot`) and read it — the gradient word only renders correctly in real Chrome |
| Same copy reformatted by hand for each platform | One entry per format with a different `template`; the studio resizes the same design |

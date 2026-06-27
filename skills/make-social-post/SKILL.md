---
name: Make Social Post
description: Design and render branded social posts (Instagram square/portrait, LinkedIn, X) for your brand using the bundled Social Studio. Headline-first billboard layout with optional product card, stat strip, or testimonial. Browser preview → puppeteer-rendered PNG → optional one-command publish to your Files folder (when connected).
triggers:
  - make a social post
  - design an instagram post
  - create a social graphic
  - new social post
  - linkedin post image
  - twitter post image
  - publish social post
  - render social post
  - shoot social post
function_slot: social
requires_driver: render
requires_credential: none
data_path: local
status: active
---

# Make Social Post

You're helping the operator design and render a social post for their own
brand using the bundled studio at `studio/social/`. It's a Vite + React +
Puppeteer pipeline producing PNGs in four formats that can stay local or be
uploaded to the operator's workspace (when connected).

The design rules + the post anatomy + the data shape live in **two**
canonical files inside the studio (read them BEFORE designing, not after):

| File | What's in it |
|---|---|
| `studio/social/CLAUDE.md` | Post anatomy, the four formats, the questions to ask, brand + content rules, samples.json field table |
| `studio/social/src/templates/SocialPost.jsx` (JSDoc header) | Canonical layout, the `FORMATS` scale table, the full data shape, brand rules in compact form |

The methodology is summarised at
[`knowledge/social-post-method.md`](../../knowledge/social-post-method.md).

## Step 1 — Confirm the brief

Ask the operator:

1. **Which format(s)?** Instagram Square (1080×1080), Instagram Portrait
   (1080×1350), LinkedIn (1200×627), or X (1600×900). A campaign often wants
   the same message in 2–3 formats — that's one samples.json entry per
   format, same copy.
2. **What's the one message?** A post is a billboard — 3–8 word headline, one
   idea. If it won't fit in 8 words, it's two posts.
3. **Accent + emphasis** — which one word gets the brand gradient
   (`accentWord`), and is there a single serif emphasis word
   (`emphasisWord`, optional)?
4. **A visual?** Optional, pick at most one:
   - `card` — a product-ish list (label/value rows), the "look inside the
     product" feel
   - `stats` — a 1–3 metric strip ("9x faster", "+34% MoM")
   - `quote` — a testimonial (initials monogram by default; `quote.avatar` URL for a real photo)
   - none — a clean headline-only announcement

## Step 2 — Add the design to samples.json

Edit `studio/social/src/data/samples.json`. Minimum shape:

```json
"launch-square": {
  "template": "social-square",
  "data": {
    "eyebrow": "Now live",
    "headline": "Run your whole business from one place",
    "accentWord": "one place",
    "emphasisWord": "whole",
    "subhead": "Leads, quotes and follow-ups stop slipping through the cracks.",
    "handle": "@yourbusiness",
    "cta": "Book a demo"
  }
}
```

`template` is one of `social-square` / `social-portrait` / `social-linkedin`
/ `social-x`. For a multi-format campaign, duplicate the entry with a
different `template` (and key suffix) and the same copy.

## Step 3 — Iterate in the browser

```bash
cd studio/social
npm install        # first run only
npm run dev        # http://localhost:3216
```

The sidebar groups designs into one folder per format. Click the new design;
the right pane renders it at native pixel size. Tweak samples.json or
`SocialPost.jsx` — Vite hot-reloads.

**Quality checks before shipping:**

1. **Headline** — 3–8 words, positive framing, exactly one `accentWord` that
   appears verbatim, at most one `emphasisWord`.
2. **Palette** — any visual card chrome stays on the brand palette (teal /
   green / blue / slate). No red / orange / purple.
3. **No vendor names** anywhere a follower would see them.
4. **Fits the frame** — nothing clipped at the edges (especially LinkedIn's
   short 627px height).

## Step 4 — Render to PNG

```bash
npm run shoot <key>
```

Puppeteer + real Chrome writes the PNG to `studio/social/output/` and opens
it. Inspect at 100% — the gradient accent word uses `background-clip:text`,
which ONLY renders correctly in real Chrome, not in-browser rasterisers.

## Step 5 — Publish (optional, when connected)

The keyless deliverable is the rendered PNG. If the operator has a connected
workspace, you can also one-command publish it straight to their Files folder:

```bash
npm run publish <key>            # one design
npm run publish -- --all         # every design (skip existing)
npm run publish <key> --replace  # overwrite
```

Uploads to the operator's `Files > Images > Social Posts` folder. Idempotent:
skip-if-exists by default, `--replace` to overwrite.

## Hard rules

- **Don't invent design rules.** The two canonical files in the studio
  (CLAUDE.md + the SocialPost.jsx JSDoc) are the source of truth. Read them.
- **The operator owns the copy.** Draft headlines if asked, but don't ship
  without their nod.
- **Render before declaring done.** A design that looks right in the dev
  server can misrender in puppeteer. Run `npm run shoot` and read the PNG.
- **Publish is optional.** If they'd rather post by hand, the PNG in
  `studio/social/output/` is the deliverable.

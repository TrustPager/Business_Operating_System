# Social Studio

**Code-driven social posts for your TrustPager brand.** Browser editor →
puppeteer-rendered PNG → optional one-command publish to your Files folder.

Part of the [Business Operating System](../../README.md). Same shape as the
[thumbnail](../thumbnails/) and [CTA](../cta/) studios — only the templates
and canvas sizes differ.

---

## Four formats, one design language

| Format | Size | Where it goes |
|---|---|---|
| Instagram · Square | 1080 × 1080 | IG feed (square) |
| Instagram · Portrait | 1080 × 1350 | IG feed (portrait — more reach) |
| LinkedIn | 1200 × 627 | LinkedIn post / link image |
| X (Twitter) | 1600 × 900 | X post (16:9) |

Every format is the same component (`src/templates/SocialPost.jsx`) at a
different size. Write the message once; render it in whichever formats you
need.

---

## Quick start

```bash
npm install
npm run dev          # http://localhost:3216
```

The left sidebar lists your designs, grouped into one folder per format.
Click one — the right pane renders it at native pixel size. Edit
`src/data/samples.json` and Vite hot-reloads.

To export:

```bash
npm run shoot <key>           # render a PNG locally + open it
npm run publish <key>         # render + upload to your TrustPager Files > Social Posts
```

`publish` resolves your API key from `$TRUSTPAGER_API_KEY`, uploads to a
**Social Posts** folder, and is idempotent (skip-if-exists; `--replace` to
overwrite).

---

## The composition

```
+--------------------------------------------------+
| [logo]                              [eyebrow]    |
|                                                  |
|   Big Headline With                              |
|   one //gradient// word + one *serif* word       |
|   Short supporting subhead line.                 |
|                                  [ visual card ] |
| @yourhandle                       [ CTA pill ]   |
+--------------------------------------------------+
```

- **Headline** — 3–8 words, one idea. One `accentWord` gets the brand
  gradient fill; an optional `emphasisWord` gets serif italic for a human beat.
- **Visual** (optional) — one of: a product-ish **`card`** (list of
  label/value rows), a **`stats`** strip (1–3 metrics), or a **`quote`**
  (testimonial with a real avatar). Portrait formats stack it under the
  headline; landscape formats put it on the right.
- **Footer** — your handle on the left, a CTA pill on the right, over a thin
  brand gradient line.

A headline-only post (no visual) is completely valid — great for
announcements.

---

## Brand

Everything visual flows from [`BOS/brand/brand.json`](../../brand/brand.json)
via `src/brand.js`. There are no hex literals in the template. Edit
brand.json (or run `/brand-my-workspace`), then re-run `/brand-my-workspace`
to refresh the logo + favicons, and every post reskins to your brand.

---

## Adding a design

Add an entry to `src/data/samples.json` (see the shape in
[CLAUDE.md](./CLAUDE.md) §5 or the JSDoc header in
[`src/templates/SocialPost.jsx`](src/templates/SocialPost.jsx)), then
`npm run shoot <key>`. For a campaign across formats, add one entry per
format with the same copy and a different `template`.

The easiest path: just ask Claude — **`/make-social-post`**.

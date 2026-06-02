# Social Studio — Instructions for AI Assistants

You're working in the TrustPager Social Studio. Before doing anything in
this directory, follow the protocol below.

---

## 1. What this is

A Vite + React + Puppeteer pipeline that turns a small JSON entry into a
branded social post PNG, in four formats:

| Template id | Size | Platform |
|---|---|---|
| `social-square`   | 1080 × 1080 | Instagram square / feed |
| `social-portrait` | 1080 × 1350 | Instagram portrait / feed |
| `social-linkedin` | 1200 × 627  | LinkedIn link/feed image |
| `social-x`        | 1600 × 900  | X (Twitter) 16:9 |

All four are the SAME component (`src/templates/SocialPost.jsx`)
specialised by a `format` prop. One design language, four canvas sizes.

Browser editor: `npm run dev` → http://localhost:3216
Canonical export: `npm run shoot <key>` (puppeteer + real Chrome).

---

## 2. The post anatomy

Every post is the same composition (portrait formats stack the visual under
the headline; landscape formats put it to the right):

```
+--------------------------------------------------+
| [logo]                              [eyebrow]    |   top bar
|                                                  |
|   Big Headline With                              |
|   one //gradient// word + one *serif* word       |   headline block
|   Short supporting subhead line.                 |
|                                  [ visual card ] |   optional visual
| @yourhandle                       [ CTA pill ]   |   footer bar
+--------------------------------------------------+
```

Spatial + type scale per format lives in the `FORMATS` table at the top of
`SocialPost.jsx`. Change sizing there — never hard-code positions inline.

---

## 3. The questions to ask before making a post

1. **Which format(s)?** Square + Portrait are the Instagram feed pair;
   LinkedIn is landscape; X is 16:9. A campaign often wants the same message
   in 2–3 formats — make one entry per format, same copy.
2. **What's the one message?** A post is a billboard. 3–8 word headline,
   one idea. If you can't say it in 8 words, it's two posts.
3. **Which word gets the gradient accent (`accentWord`)?** Usually the
   noun being transformed or the outcome word. Exactly one.
4. **Any serif emphasis word (`emphasisWord`)?** Optional. At most one —
   it adds a human, editorial beat (e.g. *whole*, *finally*, *yours*).
5. **Is there a visual?** Optional. One of: `card` (a product-ish list),
   `stats` (a 1–3 metric strip), or `quote` (a testimonial with avatar).
   A headline-only post is completely valid for announcements.

---

## 4. Commands

```bash
npm run dev                      # studio at http://localhost:3216 — live reload
npm run shoot <key>              # render one PNG + auto-open (iteration loop)
npm run shoot                    # render every design in samples.json
npm run shoot -- --no-open       # render without auto-opening
npm run publish <key>            # render + upload to your TrustPager > Files > Social Posts
npm run publish -- --all         # publish every design (skip existing)
npm run publish <key> --replace  # delete existing then re-upload
```

**Rule:** `shoot` is for iteration, `publish` is finalize. Don't publish
until the user has approved the rendered PNG. Always **read the PNG** before
declaring a render done — the studio preview can differ from puppeteer's
output (the gradient accent word uses `background-clip:text`, which only
renders correctly in real Chrome).

---

## 5. Each samples.json entry

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
    "cta": "Book a demo",
    "card": {
      "title": "This week",
      "status": "Live",
      "rows": [
        { "label": "Leads booked", "value": "12", "tag": "+34%", "tone": "success" }
      ]
    }
  }
}
```

| Field | Purpose |
|---|---|
| `template` | **Mandatory.** One of the four ids in the table above — drives canvas size + portrait/landscape layout. |
| `headline` | The billboard line. 3–8 words. `\n` forces a line break. |
| `accentWord` | The one word/phrase that gets the brand gradient fill. Matches case-insensitively, appears verbatim in the headline. |
| `emphasisWord` | Optional. One word that gets serif italic. |
| `subhead` | One supporting line. |
| `eyebrow` | Small top-right pill (e.g. `New`, `Customer story`). |
| `handle` | Footer-left text (e.g. `@yourbusiness`). |
| `cta` | Footer-right pill label. |
| `card` / `stats` / `quote` | At most one — the optional visual. See SocialPost.jsx data-shape header. |

The filename on disk is `<platform>-<key>.png` (e.g. `ig-square-launch-square.png`)
so every format of a campaign sorts together.

---

## 6. Brand + content rules (carried from the thumbnail studio)

- **All colour flows from `BOS/brand/brand.json`** via `src/brand.js`. NO hex
  literals in `SocialPost.jsx`. Editing brand.json (or running
  `/brand-my-workspace`) reskins every post. After editing brand.json, run
  `python tools/sync-brand.py` from the BOS root to refresh the logo.
- **Stay on the brand palette** in any visual card chrome — teal / green /
  blue / light teal / slate. No red / orange / purple.
- **Exactly one gradient accent word, at most one serif emphasis word.** More
  than one of each and the eye has nowhere to land.
- **Positive framing only in the headline.** No "Stop", "Don't", "Never",
  no surveillance vibes ("Track Every…"). State the outcome.
- **No third-party vendor names** anywhere a follower would see them.
- **Quote avatars are self-contained.** A quote post renders a brand-tinted
  initials monogram from `quote.name` by default — no external image
  dependency. To use a real customer photo, pass `quote.avatar` (a URL).

---

## 7. File map

```
social/
├── CLAUDE.md                       ← this file
├── README.md                       ← human design guide
├── package.json                    ← npm scripts (dev / shoot / publish / render)
├── vite.config.js                  ← dev server on port 3216
├── index.html
├── src/
│   ├── main.jsx                    ← React entry
│   ├── App.jsx                     ← studio UI (sidebar + preview)
│   ├── brand.js                    ← brand tokens from BOS/brand/brand.json
│   ├── templates/
│   │   ├── index.js                ← registry (4 format ids → wrappers)
│   │   └── SocialPost.jsx          ← THE template + JSDoc rules + FORMATS table
│   └── data/
│       └── samples.json            ← all designs — edit to add new
├── scripts/
│   ├── shoot.js                    ← npm run shoot
│   ├── publish.js                  ← npm run publish (→ Files > Social Posts)
│   ├── render.js                   ← puppeteer renderer (shared by shoot + publish)
│   └── _filename.js                ← <platform>-<key>.png naming
├── public/                         ← brand logo + favicons (synced by tools/sync-brand.py)
└── output/                         ← rendered PNGs (gitignored)
```

---

## 8. Behaviour expected of you

- Keep the headline short and positive; one accent word.
- One samples.json entry per format when a campaign needs multiple sizes.
- Verify renders by reading the PNG, not just the browser preview.
- Stay on the brand palette; never introduce hex literals in the template.
- If you hit something not covered here, ask before guessing.

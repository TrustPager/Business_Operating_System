# OG Image Studio

**Code-driven Open Graph images for your brand.** Browser editor →
puppeteer-rendered 1200×630 PNG → drop into your site's `<meta og:image>`
or one-command publish to your TrustPager Files folder.

Part of the [Business Operating System](../../README.md). Same shape as the
[social](../social/) and [thumbnail](../thumbnails/) studios — only the
template (one: `og-image`, 1200×630) and canvas size differ.

---

## What's an OG image?

The picture that unfurls when one of your links is shared on Slack, LinkedIn,
X, Facebook, or iMessage. It's set per-page via two meta tags:

```html
<meta property="og:image" content="https://yoursite.com/og/home.png" />
<meta name="twitter:image" content="https://yoursite.com/og/home.png" />
```

Without it, a shared link unfurls with whatever the crawler can scrape — usually
your favicon or nothing. A bespoke per-page image turns every shared link into a
branded marketing surface. **1200×630** is the universal size (1.91:1) all the
platforms crop to.

---

## Quick start

```bash
npm install
npm run dev        # editor at http://localhost:3217
```

Then in another terminal:

```bash
npm run shoot docs-home      # render one design → output/docs-home.png
npm run shoot                # render every design in samples.json
```

Read the PNG in `output/`. When it looks right, ship it (see **Deploy** below).

---

## Design language

Every OG image is the same composition (`src/templates/OgImage.jsx`):

- **Left:** your logo (top-left) + a punchy headline with ONE accent word in
  the brand gradient.
- **Right:** a product "hero" — a miniature of a real product surface (a
  pipeline, a contact list, a permissions grid, your AI team…) that bleeds off
  the bottom edge.
- **Chrome:** soft brand-colour halos behind the hero + a thin diagonal accent
  strip near the bottom.

All colours flow from `BOS/brand/brand.json` — edit it once (or run
`/brand-my-workspace`) and every image reskins.

---

## The 4 rules before you make one

1. **The page leads the image, not the other way around.** Read the page you're
   making the image for. Pick a headline that echoes it and a hero that mirrors
   its strongest visual.
2. **Real content, no fabricated data.** If the page says "5 minutes", the image
   says "5 minutes" — not "10". People compare in the first 3 seconds.
3. **One accent word.** The headline gets exactly one gradient word — the one
   that carries the meaning. `accentWord` in the sample picks it.
4. **Pick the hero that matches.** Browse the hero list below. A docs page about
   AI → `agent-hub` or `claude-pipeline`. An auth page → `permissions`. A
   pricing page → `pricing-tiers`. If nothing fits, the closest product surface
   still beats a generic one.

---

## Samples schema

`src/data/samples.json` — one entry per page/route you want an image for:

```json
{
  "docs-home": {
    "template": "og-image",
    "filename": "docs-home.png",
    "data": {
      "headline": "Docs Built for AI Agents",
      "accentWord": "AI Agents",
      "hero": "claude-pipeline"
    }
  }
}
```

| Field | What |
|---|---|
| `template` | always `"og-image"` |
| `filename` | output PNG name — usually matches the route it previews (e.g. `docs-home.png` → the `<meta og:image>` on your home page). Falls back to `<key>.png`. |
| `data.headline` | the big left-side text, 4–7 words |
| `data.accentWord` | the ONE word/phrase that gets the brand gradient |
| `data.hero` | a hero key from the list below |
| `data.gradient` | optional — `default` (full brand wash, the default), `hero` (teal→blue), or `warm` (teal→green) |

---

## Heroes

The right-side product miniatures. Keys for `data.hero`:

`agent-hub` · `claude-pipeline` · `pipeline` · `contacts` · `permissions` ·
`platform-overview` · `automations` · `approvals` · `reports` · `scheduling` ·
`forms` · `fill-with-ai` · `tasks` · `sms` · `send-emails` · `stage-emails` ·
`email-campaigns` · `event-queues` · `esigning` · `proposals` ·
`needs-analysis` · `notepads` · `crm-templates` · `service-request` ·
`google-calendar` · `help-center` · `website-builder` · `pricing-tiers` ·
`image-gallery`

Open the editor (`npm run dev`) and click through the samples to see each one.

---

## Deploy

Two ways to ship a rendered image:

**A. Into your website repo (most common).** Copy the PNG from `output/` into
your site's `public/og/` folder, then add the meta tags to that page's
`<head>`:

```html
<meta property="og:image" content="https://yoursite.com/og/docs-home.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://yoursite.com/og/docs-home.png" />
```

Static-site crawlers don't run JS — make sure the tags land in the static HTML
the server returns, not just client-side.

**B. To your TrustPager workspace.**

```bash
npm run publish docs-home          # render + upload to Files > "OG Images"
npm run publish -- --all           # every design
npm run publish docs-home --replace  # overwrite an existing one
```

The API returns a hosted URL you can paste straight into an `og:image` tag.
Auth resolves from `$TRUSTPAGER_API_KEY` or `~/.claude/bos.json` (run
`python tools/setup.py` from the BOS root if you haven't installed a key).

---

## File map

```
og/
├── README.md                       ← you are here
├── CLAUDE.md                       AI-assistant entry point
├── package.json
├── vite.config.js                  dev server on port 3217
├── index.html
├── src/
│   ├── App.jsx                     studio editor UI
│   ├── brand.js                    loads BOS/brand/brand.json (single brand)
│   ├── profiles.jsx                avatar pool (points at public/agents/)
│   ├── theme.js                    neutral design tokens
│   ├── templates/
│   │   ├── OgImage.jsx             ← the 1200×630 template
│   │   ├── index.js                template registry
│   │   └── heroes/                 29 product heroes + registry
│   └── data/
│       └── samples.json            every OG image you've defined
├── scripts/
│   ├── shoot.js                    npm run shoot  (render + open)
│   ├── render.js                   puppeteer renderer
│   ├── publish.js                  npm run publish (render + upload)
│   └── _filename.js                sample → output filename
├── public/
│   ├── logo.png                    your brand logo (synced by sync-brand.py)
│   ├── agents/                     AI-team portraits (agent-hub + avatar pool)
│   └── favicon*                    studio favicons
└── output/                         rendered PNGs (gitignored)
```

---

## Common mistakes

- **Fabricating numbers/copy.** Read the real page. Match its claims exactly.
- **More than one accent word.** Exactly one. The gradient loses its punch if
  half the headline is coloured.
- **Rendering then committing without looking.** Always open the PNG in
  `output/` first — the editor preview can differ from the puppeteer render.
- **Forgetting crawlers don't run JS.** The og:image tags must be in the static
  HTML the server returns.
- **Hardcoding hex.** All colours come from `brand.json`. Add or change colours
  there, never inline in a template or hero.

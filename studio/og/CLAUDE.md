# OG Image Studio — Instructions for AI Assistants

You're in `studio/og/` inside the Business Operating System. This studio
produces 1200×630 Open Graph images — the previews that unfurl when a link is
shared on Slack, LinkedIn, X, Facebook, iMessage.

**Read [README.md](README.md) first.** It has the design language, samples
schema, hero list, and deploy steps. This file is the short AI-facing version.

## Before generating an OG image — ask 4 questions

1. **What page is this for, and what does it actually say?** Read the page (or
   ask for its content). The image must echo the page — its headline, its real
   numbers, its strongest visual.
2. **What's the one accent word?** The headline gets exactly one gradient word —
   the word that carries the meaning. Set it as `accentWord`.
3. **Which hero matches the page?** Pick from the hero list in the README. The
   hero is a miniature of a real product surface; choose the one a person would
   screenshot to summarise the page. Don't default to a generic hero.
4. **What filename?** Usually matches the route it previews (`docs-home.png` →
   the home page's `<meta og:image>`).

## The workflow

```
1. Add an entry to src/data/samples.json   (template: "og-image")
2. npm run dev          (if not already running — port 3217)
3. npm run shoot <key>  → writes output/<filename>.png
4. READ the rendered PNG before claiming it's done. The editor preview can
   differ from the puppeteer output — only the PNG in output/ is truth.
5. Deploy: copy output/<filename>.png into the site's public/og/ AND add the
   og:image + twitter:image meta tags to that page's <head> (must be in the
   static HTML — crawlers don't run JS). Or `npm run publish <key>` to upload
   to the workspace's Files > "OG Images" folder for a hosted URL.
```

## Brand

Every colour, font, and the logo come from `BOS/brand/brand.json` via
`src/brand.js`. `OgImage.jsx` injects them as `--brand-*` CSS variables on the
canvas root; every hero reads `var(--brand-*)`. So editing `brand.json` (or
running `/brand-my-workspace`) reskins every image. **Never hardcode hex** in a
template or hero — add it to `brand.json`.

## Rules (do / don't)

- **DO** read the target page before picking a headline + hero. Real content,
  real numbers.
- **DO** keep the headline to 4–7 words with exactly one `accentWord`.
- **DO** read the PNG in `output/` before saying it's done.
- **DON'T** fabricate pricing, counts, or copy that isn't on the page.
- **DON'T** colour more than one accent word.
- **DON'T** hardcode brand colours — they live in `brand.json`.
- **DON'T** edit a page's meta tags without ensuring they land in the static
  HTML (client-side `<head>` injection is invisible to crawlers).
- **DON'T** add a new external asset dependency. The avatar pool
  (`profiles.jsx`) and agent portraits already point at committed files under
  `public/agents/` — keep new assets local so renders work offline.

## File map

See README.md § File map. The two files you'll touch most:
`src/data/samples.json` (define images) and occasionally
`src/templates/heroes/` (add a hero — copy the closest existing one, keep it
on `var(--brand-*)`, register it in `heroes/index.js`).

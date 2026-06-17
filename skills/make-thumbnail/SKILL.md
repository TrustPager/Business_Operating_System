---
name: Make Thumbnail
description: Design and render a 1280×720 YouTube thumbnail for a tutorial video using the bundled TrustPager Thumbnail Studio. Headline-first layout with hero UI on the right, distilled from 22+ iterations of design corrections.
triggers:
  - make a thumbnail
  - design a youtube thumbnail
  - build a tutorial thumbnail
  - new thumbnail
  - publish thumbnail
  - render thumbnail
  - shoot thumbnail
---

# Make Thumbnail

You're helping the operator design and render a YouTube thumbnail for one
of their tutorial videos using the bundled studio at
`studio/thumbnails/`. The studio is a Vite + React + Puppeteer pipeline
producing 1280×720 PNGs that can either stay local or be uploaded to the
operator's TrustPager workspace.

The design rules + title patterns + banned framings live in **three**
canonical files inside the studio (read them BEFORE designing anything,
not after):

| File | What's in the header |
|---|---|
| `studio/thumbnails/YOUTUBE_TITLES.md` | YouTube title patterns + description template + banned word table + lint rules |
| `studio/thumbnails/src/templates/YouTubeThumbnail.jsx` (JSDoc lines 1-250) | Canonical layout, full brand palette, headline writing guide, hero UI master rule, common mistakes |
| `studio/thumbnails/src/templates/heroes/index.js` (header comment) | The 6 hero family patterns, step-by-step "add a hero" instructions, anti-patterns |

The methodology distilled from those three is also summarised at
[`knowledge/youtube-thumbnail-method.md`](../../knowledge/youtube-thumbnail-method.md).

## Step 1 — Confirm the brief

Ask the operator for:

1. **What's the video about?** One-sentence outcome the viewer gets.
2. **Already-shipped help center article or YouTube title?** If yes,
   reuse the title for SEO consistency. If no, you'll generate one
   following the YOUTUBE_TITLES.md patterns.
3. **Hero family** — what's the visual centrepiece going to be? Six
   options in the registry: card stack, event row, field stack, roster,
   checklist, document, flow. Pick the one whose shape matches what the
   feature actually looks like in the product.

## Step 2 — Add the design to samples.json

Run the interactive helper:

```bash
cd studio/thumbnails
npm run make
```

It asks for a key (lowercase, kebab-case), headline (4-7 words), accent
word (which word in the headline gets the brand gradient fill), and the
hero registry key. Writes a new entry to `src/data/samples.json`.

**If the helper isn't available** (the operator interrupted it / running
non-interactively), edit `src/data/samples.json` directly. The minimum
shape is:

```json
"my-tutorial-key": {
  "composition": null,
  "template": "youtube-thumbnail",
  "data": {
    "headline": "Forms That Auto-Fill Your CRM",
    "accentWord": "Auto-Fill",
    "hero": "field-stack",
    "title": "How to Build & Send Forms in TrustPager"
  }
}
```

## Step 3 — Iterate in the browser

Make sure the dev server is running:

```bash
npm run dev    # opens at http://localhost:3210
```

The left sidebar shows the new design. Click it. The right pane renders
the live preview at actual pixel dimensions. Tweak `samples.json` or the
hero / template files — Vite hot-reloads.

**Quality checks before declaring it shipped:**

1. **Title check** — is the YouTube title 4-7 words, present-tense active
   verb, lead with the viewer's outcome (not the AI's action)? Read
   YOUTUBE_TITLES.md if unsure.
2. **Headline check** — does the on-thumbnail headline have one accent
   word that appears VERBATIM in the title? Read the JSDoc in
   YouTubeThumbnail.jsx.
3. **Hero check** — does the hero look like real product UI (not a
   configurator)? Read the heroes/index.js header.
4. **Banned framings** — no surveillance ("Track Every Promise"), no
   passive vibes ("Nothing Falls Through the Cracks"), no negative
   "Stop X" framing, no third-party vendor names visible in the
   thumbnail.

## Step 4 — Render to PNG

```bash
npm run shoot <design-key>
```

That runs puppeteer + real Chrome and writes the PNG to
`studio/thumbnails/output/`. Opens it automatically when done. Inspect
it at 100% — there are CSS features (background-clip:text, backdrop-
filter) that ONLY render correctly via real Chrome, not via in-browser
rasterisation libraries.

If something looks off in the rendered PNG that looked fine in the
browser, the JSDoc has a "Common mistakes" section worth reading.

## Step 5 — Publish (optional)

To upload the PNG to the operator's own TrustPager workspace's
`Files > Images > Tutorial Thumbnails` folder:

```bash
npm run publish <design-key>
```

Auth comes from the `TRUSTPAGER_API_KEY` environment variable. The script handles
idempotency — re-running publish with the same design key skips if the
file's unchanged, renames if the title shifted, replaces only on
`--replace`.

To publish every design in one shot:

```bash
npm run publish -- --all              # skip existing
npm run publish -- --all --replace    # wipe + re-upload
```

## Hard rules

- **Don't invent design rules.** The three canonical files in the studio
  (README, YOUTUBE_TITLES.md, the templates JSDoc) are the source of
  truth — they distil real corrections from 22+ iterations. Read them.
- **The operator owns the title.** Generate a draft if asked, but don't
  ship without their nod.
- **Render before declaring done.** A design that looks right in the
  Vite dev server can still misrender in puppeteer if it uses unusual
  CSS features. Run `npm run shoot` and look at the actual PNG.
- **Examples ≠ inspiration to copy.** The 6 PNGs in
  `studio/thumbnails/examples/` are FinalPiece's own thumbnails. They
  show the design DNA but are not templates to clone verbatim.
- **Publish is optional.** If the operator wants the PNG to stay local
  (post manually to YouTube studio), skip publish. The shoot output in
  `studio/thumbnails/output/` is the deliverable.

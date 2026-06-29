---
name: Brand My Workspace
description: Point this at the user's website. Detect their brand colours, fonts, name, and logo. Write `brand/brand.json` + drop `brand/logo.png`. Run `tools/sync-brand.py` so every studio is rebranded in one shot. This is the single touchpoint for theming every BOS studio (thumbnails, CTAs, future studios).
triggers:
  - brand my workspace
  - rebrand my pack
  - rebrand the studios
  - skin BOS to my brand
  - import brand from my website
  - update brand kit
function_slot: creative
requires_driver: none
requires_credential: none
data_path: local
status: active
---

# Brand My Workspace

You're rebranding every BOS studio in one shot. The user points at their website (or hands you their colours directly). You write `brand/brand.json` + drop `brand/logo.png`, then run `tools/sync-brand.py` so every studio's `public/` folder picks up the new assets.

After this skill finishes, every thumbnail and every CTA the user renders will be on their brand. They don't have to touch any other file.

## What you're producing

```
BOS/brand/
├── brand.json    ← colours, fonts, name, tagline
├── logo.png      ← wordmark, transparent PNG ideally
├── icon.png      ← optional, square; source for favicons
├── favicon.ico
├── favicon-16x16.png
├── favicon-32x32.png
├── favicon-192x192.png
└── favicon-512x512.png
```

Anything you can't determine confidently, leave the existing default in place — don't guess.

## Step 1 — Get the URL

If the user gave you a URL, use it. Otherwise ask:

> "What's the URL of the website I should pull your brand from?"

Accept things like `acmeplumbing.com.au`, `https://acmeplumbing.com.au`, `www.acmeplumbing.com.au`. Normalise to `https://<host>`.

## Step 2 — Fetch the homepage

Use the `WebFetch` tool to grab the homepage. Ask it to extract:

- The page `<title>` and `<meta name="description">`
- All `<link rel="icon">`, `<link rel="apple-touch-icon">`, `<link rel="shortcut icon">` URLs (resolve relative paths to absolute)
- Any `<meta name="theme-color">` value
- The `<header>` contents (likely contains the logo + nav)
- Visible H1 / hero copy (often signals tagline)
- All inline `style="..."` attributes and any `<style>` blocks (for brand colour signals)

Save the raw response to `_staging/brand-fetch-<host>.html` for your own reference.

## Step 3 — Find the logo

In order of preference:
1. The `<img>` inside `<header>` / `<nav>` with `alt` containing the company name
2. The largest `apple-touch-icon` link
3. The first `<link rel="icon">` that isn't the default 16×16 favicon
4. `<meta property="og:image">`

Once you have the URL, download the image with `curl` (or `WebFetch`) to `_staging/logo-fetch.<ext>`. Quick sanity check: should be > 5kb, should not be a 404 or HTML error page. If it's an SVG, use it as-is. If it's a small raster favicon, prefer larger versions found elsewhere.

Convert / save to `brand/logo.png`. If only an SVG is available, leave the SVG at `brand/logo.svg` AND keep the existing `brand/logo.png` — flag this to the user as something to address manually.

## Step 4 — Detect colours

You have three signals, in order of trustworthiness:

1. **`<meta name="theme-color">`** — explicit primary, trust as `primary`.
2. **CSS custom properties** — look for `--primary`, `--brand`, `--accent`, `--color-primary` in `<style>` blocks or linked stylesheets. If you can WebFetch the linked CSS, do.
3. **Inline styles + class names on hero elements** — most common signal. Look at the button background colour, the `<header>` background, link colours, the visible accent under the H1.

For each colour, normalise to a 6-character lowercase hex string (`#29c6c6`, never `rgb(...)`).

You're filling in this shape (current values are TrustPager defaults that you're replacing):

```json
{
  "primary":     "#29c6c6",    // main brand colour — buttons, accent text, brand gradient anchor
  "primaryDeep": "#1ea5a5",    // darker variant for hover/depth — usually `primary` desaturated 10%
  "primaryTint": "#e6f7f7",    // pale tinted background — usually `primary` at ~10% opacity flattened on white
  "primaryTintDeep": "#cbeded",
  "accent":      "#47a3d9",    // secondary colour — often blue
  "deepBlue":    "#2e7fb0",    // darker accent
  "midMint":     "#5ed4d4",    // gradient midpoint
  "light":       "#7dd3d3",
  "slate":       "#94a3b8",
  "success":     "#2db87d",    // success/green — usually safe to keep
  "warning":     "#facc15"     // warning/yellow — usually safe to keep
}
```

**Required to confidently set: `primary`.** Everything else can be derived:
- `primaryDeep` = primary darkened 10-15% (drop lightness)
- `primaryTint` = primary mixed 90% with white
- `primaryTintDeep` = primary mixed 75% with white
- `accent` — if you can't find a clear secondary in the brand, fall back to a complement of primary (or leave the TrustPager default and flag for the user)
- `midMint` / `light` / `deepBlue` — gradient stops. If only one brand colour exists, derive these from primary at different lightness levels.

For `success` and `warning`: keep the defaults. They're universal greens/yellows, not brand colours.

## Step 5 — Detect business name + tagline

- `name`: from the `<title>` (drop trailing " | Tagline" or " - Subtitle" parts), or from `<meta property="og:site_name">`. Sentence-case.
- `tagline`: from `<meta name="description">` (trim to first sentence), or from the hero H1. Keep under 80 characters.

## Step 6 — Detect fonts

Look at:
- `<link rel="stylesheet">` to Google Fonts URLs (extract `family=` params)
- Inline `font-family:` declarations in `<style>` blocks
- The hero H1's computed font (if visible in inline styles)

Output:
```json
{
  "fonts": {
    "primary": "\"Inter\", -apple-system, BlinkMacSystemFont, system-ui, sans-serif",
    "serif":   "\"Playfair Display\", Georgia, serif",
    "mono":    "\"JetBrains Mono\", \"Fira Code\", monospace"
  },
  "googleFontsHref": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
}
```

If you can't find their fonts, KEEP the existing defaults (Plus Jakarta Sans). Most brand colour swaps work fine on the default font.

## Step 7 — Compose the gradient strings

```json
{
  "gradient":     "linear-gradient(110deg, ${primaryDeep} 0%, ${primary} 35%, ${midMint} 50%, ${accent} 70%, ${deepBlue} 100%)",
  "heroGradient": "linear-gradient(135deg, ${primary} 0%, ${accent} 100%)",
  "warmGradient": "linear-gradient(135deg, ${primary} 0%, ${success} 100%)"
}
```

(With the actual hex values inlined, not the `${}` placeholders — `brand.json` is plain JSON.)

## Step 8 — Write `brand/brand.json`

Read the current file at `brand/brand.json`. Update ONLY the keys you've changed. Preserve any keys you didn't touch — don't drop fields the studios expect to exist.

Pretty-print with 2-space indent.

## Step 9 — Generate favicons from logo (best-effort)

If the user has Python + Pillow available, you can resize `logo.png` (or `icon.png` if they provided one) to all favicon sizes. If not, leave the existing favicons in place and flag to the user.

Quick path with Pillow:

```python
from PIL import Image
src = Image.open("brand/icon.png")
for size in [16, 32, 192, 512]:
    src.resize((size, size), Image.LANCZOS).save(f"brand/favicon-{size}x{size}.png")
src.resize((180, 180), Image.LANCZOS).save("brand/apple-touch-icon-source.png")  # for reference
src.resize((32, 32), Image.LANCZOS).save("brand/favicon.ico", format="ICO", sizes=[(16,16),(32,32)])
```

Skip this step if you only have a wide wordmark (not a square icon). Tell the user to drop a square `icon.png` into `brand/` if they want regenerated favicons.

## Step 10 — Run sync-brand.py

```bash
python ~/.claude/bos-run.py tool sync-brand
```

(The `~/.claude/bos-run.py` launcher resolves the install location for you. If it is missing, run `python tools/setup.py` once from the BOS directory to create it.)

This copies the new `brand/logo.png` + favicon set into every studio's `public/`.

## Step 11 — Tell the user what changed

Hand back a summary:

- Brand name: <name>
- Tagline: <tagline> (or "kept default")
- Primary colour: <hex>
- Accent colour: <hex>
- Logo: <path or "kept default">
- Studios synced: thumbnails, cta (+ any others under `studio/`)

Then tell them:

> "Hard-refresh your studio tabs (Ctrl+Shift+R) to see the new brand. If a tab was already open, the favicon may stay cached — closing and reopening fixes it."

## What you don't do

- Don't edit any template `.jsx` files. The brand kit alone is enough — templates read from it.
- Don't try to set per-design content (headlines, captions) — that's `samples.json` in each studio, not `brand.json`.
- Don't touch the studio editor UI (sidebar, zoom, command chips). Those are intentionally hardcoded.

If the user's brand differs from yours in a way the brand kit can't express (e.g. a completely different card layout, a different aspect ratio), tell them which `.jsx` template to edit and STOP. Don't try to redesign the template via JSON.

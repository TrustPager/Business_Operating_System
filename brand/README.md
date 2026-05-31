# Brand kit

This folder is the **single source of truth for your brand** across every BOS studio. Edit `brand.json`, drop your logo in, run one sync command — every studio you build picks it up automatically.

## Files

| File | What it is | Required |
|---|---|---|
| `brand.json` | Colours, fonts, business name, tagline | yes |
| `logo.png` | Wordmark logo. Used in studio outputs (top-left of thumbnails, CTAs, etc). | yes |
| `icon.png` | Square icon, ≥512×512. Source for favicons. | for favicons |
| `favicon.ico` | Browser tab icon | yes (auto from icon.png) |
| `favicon-16x16.png` | 16×16 PNG favicon | yes |
| `favicon-32x32.png` | 32×32 PNG favicon | yes |
| `favicon-192x192.png` | Android Chrome icon | yes |
| `favicon-512x512.png` | Android Chrome large icon | yes |

## How to rebrand

### Option 1 — let Claude do it

```
/brand-my-workspace https://yourwebsite.com
```

Claude scrapes your site, picks up your colours, finds your logo, writes `brand.json` + drops the logo in. Done in 30 seconds.

### Option 2 — edit by hand

1. Open `brand.json`. Swap colours under `colors:`. Plain hex codes.
2. Replace `logo.png` with yours (ideally a wide wordmark; 400-1200px wide; transparent PNG).
3. Run the sync:
   ```bash
   python tools/sync-brand.py
   ```
   This copies `logo.png` + the favicon set into each studio's `public/` folder so dev servers serve them at `/logo.png`, `/favicon.ico`, etc.
4. Restart any running studio dev servers.

That's it. Every studio in `studio/` is now on your brand.

## How studios read this

Each studio has `src/brand.js` — a thin loader that imports `../../../brand/brand.json` and re-exports typed tokens (`COLORS`, `GRADIENT`, `FONT_BODY`, `LOGO_URL`, etc.). Studio templates import from there, never from inline hex literals.

To add a new studio that uses this brand kit, copy any existing studio's `src/brand.js` into your new studio's `src/` — that's the only wiring needed.

## What stays under your control

`brand.json` only controls the brand IDENTITY (colours, fonts, logo, name). It does NOT control:

- Layout or composition of each design
- Per-design content (headlines, captions, feature lists) — those live in each studio's `src/data/samples.json`
- The editor UI in each studio — that's intentionally fixed so the dev tool stays predictable

If you want to change how a thumbnail or CTA looks beyond the colours, edit the template `.jsx` file directly. The brand kit just makes the COLOURS portable.

# Motion Studio — human design guide

Module one of the **Content Creation Studio** hub. It turns a `<slug>.scenes.json`
visual plan into a branded, motion-graphics video (MP4) on your own brand, read
from the root `brand/brand.json`. It runs on your machine, with no accounts and no
API keys.

Where the four still studios (thumbnails, og, social, cta) render one branded PNG,
and the video studio renders text-on-screen from a script, this studio is the
**Remotion engine**: real React motion — spring physics, staggered entrances,
diagram/before-after/flow/stat devices — composed into one MP4.

---

## What it is

One parametrised Remotion project. A plan (`<slug>.scenes.json`) names, per beat,
a **style** and a **visual device**; the engine looks each up in a registry and
plays them in order. Change the plan, get a new video — no per-video code.

- Studio preview (live reload): `npm run studio`
- Render a plan: `npm run render -- Video output/<slug>.mp4 --props=data/<slug>.scenes.json`
- Check your setup once: `npm run preflight`

The organising idea shared with the whole content factory: **the plan is the
spec.** `script-my-video` writes the words, `design-my-scenes` writes the visual
plan, this studio renders it, and `package-my-video` collates it — all reading the
same `<slug>` files.

---

## The vocabulary

**Three styles**, each a full aesthetic (structure + motion):

- `clean_editorial` — big type, generous negative space, restrained springs.
- `blueprint` — schematic technical-drawing register; thin strokes that draw in.
- `bold_pop` — high-energy, high-contrast, overshoot motion.

**Four devices**, each built in every style, so any beat renders its *meaning*:

- `typographic_statement` — one emphatic line, staggered in.
- `before_after` — the same thing transformed, no sentence needed.
- `process_flow` — a few steps, nodes then connectors.
- `big_stat` — one number, counted up, made the whole frame.

The style owns colour-free **structure and motion**; your `brand.json` owns
**colour and type**. Every render is on your palette and your fonts.

---

## How a render works

`Video` is the one composition you render. It takes the whole plan as Remotion
input props and derives its own length, aspect, and frame rate from the plan
(`calculateMetadata` → `computeFacelessMeta`). `scripts/render.js` reads the plan
file for you and hands it in, then writes a `<slug>.timing.json` sidecar the
packaging step reads for chapters.

You never type a render flag, edit a `<Sequence>`, or pick a pixel format — the
guided `make-my-video` skill drives all of it. This studio is the engine; the
skill is the steering wheel.

---

## Brand and content

All colour and type flow from `BOS/brand/brand.json` (via `src/brand.js` →
`src/tokens.ts`). Edit the brand once — or run `/brand-my-workspace` — and every
studio, this one included, reskins. On-screen labels are short, in your brand
voice, with positive framing and no em dashes.

For the full craft, the props-render contract, and the render-survival reality
(software-render times, the swangle default, the "blank canvas → check the
browser console" rule), read [`CLAUDE.md`](./CLAUDE.md) in this folder.

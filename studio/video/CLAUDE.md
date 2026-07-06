# Video Studio — Instructions for AI Assistants

You're working in the BOS Video Studio, the fifth render studio. It turns a
beat-structured video script into a branded, text-on-screen motion-graphic video
on the owner's own brand, read from the root `brand/brand.json`. Before doing
anything in this directory, follow the protocol below.

---

## 1. What this is

A Vite + React + Puppeteer pipeline — the same stack as the four still studios
(thumbnails, og, social, cta) — that renders a `<slug>.script.json` (written by
`script-my-video`) as a branded text-on-screen video. It is the **motion
generalisation** of the still studios: instead of one PNG, it captures the same
brand.json-driven React composition at every frame across a timeline and stitches
the frames into an MP4.

The organising principle of the whole YouTube factory: **the script is the
spec.** One `<slug>.script.json` drives this video, the thumbnail concept in
`make-thumbnail`, and the publish folder in `package-my-video`.

- Browser preview + frame scrubber: `npm run dev` → http://localhost:3218
- Canonical render: `npm run shoot <slug>` (Puppeteer + real Chromium + ffmpeg)

---

## 2. The frame-drive interface (read before touching render.js or the template)

This is the load-bearing contract, and the spec owns it (Decision 4 +
§5 Task 1.4 of `docs/architecture/2026-07-05-youtube-studio-design.md`):

- **The template reads its frame from `?frame=N`.** `VideoBeats.jsx` takes a
  `frame` prop; `App.jsx` reads `?frame=N` (and `?slug=`) from the URL so the
  browser preview and the headless renderer share exact frame semantics.
- **`render.js` steps `?frame=0..duration*fps` deterministically** and
  screenshots the `.video-canvas` element each step. It is **frame-capture,
  never realtime capture** — the same frame always paints identically, so renders
  are reproducible. This is the same "resolve animations at a frame" idea as
  `studio/thumbnails/src/remotion-shim.jsx`.
- **`fps` is a studio constant (30), not a script field.** It lives in
  `src/timing.js`, the one place that owns all timeline math.

Do NOT add Remotion here. The workspace hard-rule reserves the Remotion render
engine for the separate `Remotion-VideoStudio` repo; this studio uses the same
lightweight Puppeteer frame-capture as its four siblings (Decision 4/8).

---

## 3. The timing sidecar (`<slug>.timing.json`)

After the frame loop, `render.js` writes `<slug>.timing.json` beside the MP4 with
the ACTUAL rendered per-beat times. Shape (spec §3 / Pin 1 — the owner):

```json
{
  "slug": "quote-a-job-in-under-a-minute",
  "fps": 30,
  "beats": [
    { "id": "hook",    "start_s": 0.0, "end_s": 4.4 },
    { "id": "promise", "start_s": 4.4, "end_s": 11.6 }
  ]
}
```

Keyed by beat `id`, seconds as floats, array in render order. `package-my-video`
reads this exact shape for chapter timestamps, falling back to the script's
planned `duration_s` when no render has happened. Never change this shape without
updating spec §3 and `package-my-video`.

---

## 4. Audio: a silent stereo track (on purpose)

The floor MP4 carries a **silent stereo audio track** (ffmpeg `anullsrc`, 2
channels). This keeps the floor keyless and silent while making the Phase-2 voice
rung a track replacement/remux, not a container change (Decision 4). Do not strip
it.

---

## 5. ffmpeg (keyless, three-arm resolution)

The shipped arm is **`ffmpeg-static`** (an npm devDependency — verified to install
and stitch cleanly, and it lives in gitignored `node_modules`, so no binary is
ever committed). `render.js` resolves ffmpeg in three arms, in order:

1. `ffmpeg-static` (preferred, keyless, self-contained).
2. a system `ffmpeg` on PATH (fallback).
3. neither → the render **never hard-fails silently**: it keeps the frame PNGs
   and `<slug>.timing.json` and prints a one-line positive install pointer.

Keep this contract. `node_modules/` and `output/` stay gitignored.

---

## 6. Commands

```bash
npm install                      # deps (Chromium via puppeteer, ffmpeg via ffmpeg-static)
npm run dev                      # studio at http://localhost:3218 — live reload + scrubber
npm run shoot <slug>             # render data/<slug>.script.json → MP4 + GIF + timing.json
npm run shoot <slug> --no-open   # render without auto-opening the MP4
npm run render -- <slug>         # the raw renderer (shoot wraps it + checks the dev server)
npm run render -- --script <path>  # render an explicit script file
```

**Rule:** `shoot` needs the dev server running (`npm run dev` in another
terminal). Always **read/play the MP4** before declaring a render done — the
browser preview can differ from Chromium's headless output.

---

## 7. Each data/<slug>.script.json

The studio renders the exact shape `script-my-video` emits (spec §3 beat schema):
top-level `slug`, `working_title`, `packaging`, `meta` (`duration_target_s`,
`aspect`, `hook_window_s`), and `beats[]`. Each beat carries `id`, `role`
(`hook | promise | point | reset | proof | cta`), `spoken`, `on_screen`,
optional `b_roll`, optional `evidence_ref`, optional `duration_s`. The studio
renders each beat's **`on_screen`** line; `spoken` drives the later voice rung,
not the floor. `meta.aspect` picks the canvas (16:9 → 1920×1080, 9:16 →
1080×1920).

Commit fixtures under `data/`. The smoke-render fixture is
`data/quote-a-job-in-under-a-minute.script.json` (a copy of
`skills/script-my-video/sample.script.json`).

---

## 8. Brand + content rules

- **All colour flows from `BOS/brand/brand.json`** via `src/brand.js` (import
  identical to every other studio). NO hex literals in `VideoBeats.jsx`. Edit
  `brand.json` (or run `/brand-my-workspace`), then `python tools/sync-brand.py`
  from the BOS root to refresh the logo, and every studio reskins.
- **The copy is the script's, the palette is the owner's.** On-screen lines come
  from the beats' `on_screen` fields verbatim. **No third-party vendor names**
  anywhere a viewer would see them.
- **Positive framing, no em dashes** in any on-screen line — enforced upstream by
  `script-my-video`; the studio renders what the script gives it.

---

## 9. File map

```
video/
├── CLAUDE.md                       ← this file
├── README.md                       ← human design guide
├── package.json                    ← npm scripts (dev / shoot / render)
├── vite.config.js                  ← dev server on port 3218
├── index.html
├── src/
│   ├── main.jsx                    ← React entry
│   ├── App.jsx                     ← studio UI (sidebar + frame preview + scrubber)
│   ├── brand.js                    ← brand tokens from BOS/brand/brand.json (identical to social)
│   ├── timing.js                   ← the ONE timeline/timing math (planned→frames→sidecar)
│   └── templates/
│       ├── index.js                ← template registry
│       └── VideoBeats.jsx          ← THE template: reads ?frame=N, paints the active beat
├── scripts/
│   ├── shoot.js                    ← npm run shoot (wraps render.js)
│   ├── render.js                   ← NET-NEW: frame loop + ffmpeg stitch + silent track + timing.json
│   └── _filename.js                ← output naming helper
├── data/
│   └── <slug>.script.json          ← committed fixture(s)
└── output/                         ← rendered MP4/GIF/frames/timing.json (gitignored)
```

---

## 10. Behaviour expected of you

- Read the frame-drive interface (§2) and the timing contract (§3) before
  changing `render.js`, `timing.js`, or the template.
- Verify a render by reading/playing the MP4 and reading the `timing.json`, not
  just the browser preview.
- Keep all colour on `brand.json`; never introduce hex literals in the template.
- Keep the silent stereo track and the three-arm ffmpeg fallback intact.
- If you hit something not covered here, ask before guessing.
```

# Video Studio — human design guide

> **Status: not the engine of record, but a supported path with one job.**
> `studio/motion` (Remotion) is the engine of record and where new video work goes:
> faceless motion graphics, talking-head overlay, the product-demo add-on, voiceover,
> local captions, the scene library. Every video-making skill drives it.
>
> **This studio's one job is the owner who does not want a licence obligation.**
> Remotion is free for an individual or a small team and a company of four or more
> needs to buy its own licence (`studio/motion/CLAUDE.md` §1: BOS mentions that once
> and never enforces it). This studio has no licence obligation at all, so it is the
> honest answer when an owner asks whether they have to pay. `make-my-video` Step 1
> offers it for exactly that reason, and `package-my-video` accepts its output.
>
> **Be straight about the trade.** It renders branded text-on-screen video from a
> `<slug>.script.json`, plus a preview GIF and the timing sidecar. It does NOT do
> voiceover, talking-head overlay, local captions, the product-demo add-on, or the
> scene library. An owner choosing this path gets a plainer video, and should be told
> so rather than discovering it.
>
> Kept deliberately narrow: it is maintained for that one job, not extended with new
> features. Anything the script schema grows (a new beat role, say) must degrade
> gracefully here rather than needing a matching change, which is why the beat-role
> label is derived rather than hardcoded.

The fifth studio in the BOS family. It turns a beat-structured video script
(`<slug>.script.json`, written by `script-my-video`) into a branded,
text-on-screen motion-graphic video (MP4 + preview GIF), plus a timing sidecar
the packaging step reads. Same Vite + React + Puppeteer stack as the four still
studios (thumbnails, og, social, cta), one root brand, no accounts.

---

## What it is

The four still studios render one branded PNG from a JSON entry. This studio is
the **motion generalisation** of that: it renders the *same* kind of
brand.json-driven React composition, but captured at every frame across a
timeline, then stitched into a video. The organising idea is the same one the
whole YouTube factory runs on: **the script is the spec.** One
`<slug>.script.json` drives the video here, the thumbnail in `make-thumbnail`,
and the publish folder in `package-my-video`.

- Browser preview + frame scrubber: `npm run dev` then http://localhost:3218
- Canonical render: `npm run shoot <slug>` (Puppeteer + real Chromium + ffmpeg)

---

## The frame-drive interface

This is what makes the render reproducible, and it is the contract between the
template and the renderer:

1. The template (`src/templates/VideoBeats.jsx`) reads the current frame from a
   URL query param: **`?frame=N`**. Given a frame, it shows the beat that frame
   falls in and paints the beat's `on_screen` line, with a deterministic
   fade/slide-in based on how far into the beat the frame is.
2. `scripts/render.js` steps **`?frame=0`, `?frame=1`, … up to
   `duration*fps`** deterministically, screenshotting the `.video-canvas`
   element each step. It is **frame-capture, never realtime capture** — the same
   frame always paints identically, so two renders of one script are byte-stable.
3. The frames are stitched to an MP4 (H.264) and a preview GIF.

`fps` is a studio constant (30), not a script field — it is a render property.
The timeline math lives in one place, `src/timing.js`, so the browser preview,
the frame loop, and the timing sidecar can never disagree.

---

## The timing contract (planned vs actual)

The timing contract has two halves, and this studio owns the *actual* half
(spec §3 of `docs/architecture/2026-07-05-youtube-studio-design.md` is the owner
of the contract itself):

- **Planned** — `script-my-video` fills each beat's optional `duration_s` from
  its spoken word count at 150 words per minute.
- **Actual** — after the frame loop, `render.js` writes **`<slug>.timing.json`**
  with the actual rendered per-beat start/end times, keyed by beat `id`, seconds
  as floats, in render order:

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

`package-my-video` prefers this file for chapter timestamps and falls back to the
script's planned `duration_s` when no render has happened yet. Because the render
is deterministic on the frame grid, the actual times equal the planned windows
quantised to whole frames.

---

## Audio: a silent stereo track

The floor MP4 carries a **silent stereo audio track** (generated with ffmpeg's
`anullsrc`, 2 channels, 48kHz). This is on purpose: the Phase-2 voice rung drops
the owner's voiceover onto the timeline as a **track replacement/remux**, not a
container change. The floor stays keyless and silent; adding voice later never
reshapes the file.

---

## ffmpeg (keyless, with a fallback)

The stitch step needs ffmpeg. It resolves in three arms, in order:

1. **`ffmpeg-static`** (preferred) — an npm devDependency that ships a static
   ffmpeg binary. `npm install` brings it in, no account and no system install
   needed. The studio stays fully self-contained and keyless.
2. **System `ffmpeg`** (fallback) — if `ffmpeg-static` is not resolvable,
   `render.js` shells an `ffmpeg` on your PATH.
3. **Neither available** — the render **never hard-fails silently.** It keeps the
   captured frame PNGs and the `<slug>.timing.json`, and prints a one-line,
   positive install pointer (`npm install`, or ffmpeg.org) so you are never
   blocked. Re-run the render once ffmpeg is present and it stitches the video.

`node_modules/` and `output/` are gitignored, so the binary is never committed.

---

## Commands

```bash
npm install                      # deps (Chromium via puppeteer, ffmpeg via ffmpeg-static)
npm run dev                      # studio at http://localhost:3218 — live reload + scrubber
npm run shoot <slug>             # render data/<slug>.script.json to an MP4 + GIF + timing.json
npm run shoot <slug> --no-open   # render without auto-opening the MP4
npm run render -- <slug>         # the raw renderer (shoot wraps this)
npm run render -- --script path/to/my.script.json   # render an explicit script file
```

`shoot` needs the dev server running (start `npm run dev` in another terminal).
Always **read/play the MP4** before declaring a render done — the browser preview
can differ from Chromium's headless output.

**Port override.** The dev server defaults to port 3218. If that port is already
in use (a concurrent session or a leftover dev server), set `BOS_VIDEO_PORT` to a
free port. The dev server (`vite.config.js`) and both render scripts read the
same variable, so one setting keeps them together:

```bash
BOS_VIDEO_PORT=3219 npm run dev            # dev server on 3219
BOS_VIDEO_PORT=3219 npm run shoot <slug>   # render against 3219
```

If `shoot` says the dev server is unreachable, this is the first thing to try.

---

## File map

```
video/
├── CLAUDE.md                       ← AI-assistant protocol for this studio
├── README.md                       ← this file
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
│   └── <slug>.script.json          ← committed fixture(s) for the smoke render
└── output/                         ← rendered MP4/GIF/frames/timing.json (gitignored)
```

---

## Brand + content rules

- **All colour flows from `BOS/brand/brand.json`** via `src/brand.js` (the import
  is identical to every other studio). No hex literals in `VideoBeats.jsx`. Edit
  `brand.json` (or run `/brand-my-workspace`), then `python tools/sync-brand.py`
  from the BOS root to refresh the logo, and every studio reskins.
- **The copy is the script's, the palette is the owner's.** No third-party vendor
  names anywhere a viewer would see them. On-screen lines come from the beats'
  `on_screen` fields verbatim.
- **Positive framing, no em dashes** in any on-screen line (that is enforced
  upstream by `script-my-video`; the studio renders what the script gives it).
```

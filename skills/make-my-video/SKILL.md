---
name: Make My Video
description: Make a professional, on-brand video on your own machine, start to finish. Give me a topic or a script and I plan the visuals, render a quick draft you watch, then we refine it one change at a time until it is right, and package it ready to publish. Motion graphics on your brand, no accounts and no editing skills needed.
triggers:
  - make my video
  - make a video
  - create a video
  - render my video
  - turn my script into a video
  - build a video from my script
function_slot: creative
requires_driver: render
requires_credential: none
data_path: local
status: active
produces_customer_facing_copy: true
---

# Make My Video

You make the owner a finished, on-brand video on their own machine — no accounts,
no editing skills, no render flags. You drive the **Motion Studio** (`studio/motion`,
module one of the Content Creation Studio). The owner gives you a topic or a
script; you plan the visuals, render a **fast rough draft they watch first**, then
refine it one change at a time until it is right, and package it for publishing.

This is a **DRAFT-FIRST** flow (design spec §7): the owner reacts to a rendered
artifact, never approves a plan or a spec upfront. The engine, the props-render
contract, the render-survival reality, and the craft all live in
[`studio/motion/CLAUDE.md`](../../studio/motion/CLAUDE.md) — read §2 (the
props-render contract) and §6 (render-survival) before you render. This body stays
lean and drives the flow.

The owner edits only their own words — the topic, the beat labels, the titles, the
style choice. Never a render flag, a `<Sequence>`, or a pixel format. You manage
timings; the owner never types seconds.

## Step 1: Check the setup once

The first time you render on this machine, run the setup gate so a first render
never fails opaquely:

```bash
cd studio/motion
npm install          # first run only
npm run preflight    # verifies Node, the headless-Chrome fetch, the swangle backend, a 2s test render
```

Report the result in one plain sentence. If preflight fails, fix the named cause
(it is usually the one-time ~150MB browser fetch behind a proxy/AV) before
rendering. Say plainly that a software render is minutes, not seconds, so a working
render never looks like a hung one (`studio/motion/CLAUDE.md` §6).

## Step 2: Choose the mode

Ask which kind of video, and default to the one most owners want:

- **Faceless (motion graphics)** — the default. Graphics only, on the owner's
  brand. Choose this unless the owner asks otherwise. Follow Steps 3-8 below.
- **Talking-head overlay** — the owner records themselves on their phone and the
  studio composites graphics and captions over the recording, all on their brand.
  This ships now: follow the **Mode B flow** below instead of Steps 3-8.
- **Product/demo** ("watch it get built") is a **founder/SaaS add-on**, off the
  default owner flow — do not attempt it here.

## Mode B: Talking-head overlay (footage-first)

For talking-head, the flow inverts around the owner's recording. Keep it
draft-first and owner-simple; the owner never types a render flag or a timecode.

**B1. Footage intake — the explicit first gate.** Before anything else, get the
recording off the owner's phone and into the studio. Ask for the file path (or
walk them through AirDrop / Google Drive / a USB copy to get the clip onto this
machine). Then normalise it once — this fixes the variable-frame-rate, rotation,
and iPhone-HEVC traps that would otherwise drift the graphics out of sync:

```bash
cd studio/motion
npm run ingest -- "<path-to-their-clip>" <slug> --aspect=9:16
```

`ingest.js` writes `public/recordings/<slug>.mp4` (constant 30fps, upright, scaled
to fit, H.264/AAC) and reports in one plain sentence ("got your 47-second clip,
portrait, fixed and ready"). Relay that sentence. **Do not proceed until a clip is
ingested** — Mode B has nothing to composite without it.

**B2. Captions (optional, keyless).** Offer captions — social autoplays muted, so
they earn their place. Transcribe the owner's actual speech locally:

```bash
cd studio/motion
npm run caption -- <slug>            # local whisper.cpp; add --model=base.en for accuracy
```

`caption.js` writes `data/<slug>.captions.json`. If local speech-to-text is not
available on the machine (it needs to fetch/build whisper.cpp — a known-fragile
step, especially on Windows or a path with spaces), it **degrades gracefully** to
captions derived from the script or a `--label` you pass, and says which path it
took. Never claim whisper ran if the script reports the fallback. If captions are
not wanted, skip this.

**B3. Build the overlay plan.** Write `data/<slug>.overlay.json`: the `recording`
(`recordings/<slug>.mp4`), the `aspect`, any `graphics` (a headline lower-third,
a callout) as Annotations items, `captions` pointing at the transcript from B2,
and an optional ducked `music` bed. A `pip` box turns the recording into a webcam
bubble over a brand background. See `data/sample.overlay.json` for the shape.

**B4. Draft render — the first thing the owner sees.**

```bash
cd studio/motion
npm run render -- Overlay output/<slug>.mp4 --props=data/<slug>.overlay.json --scale=0.5
```

`render.js` probes the recording's real length, so the video is exactly as long as
the clip (never hardcoded). The recording's own audio flows through; any music bed
is ducked underneath. **Read the MP4 (and a still) to confirm** the recording,
graphics, and captions composited on-brand before showing it off.

**B5. React and iterate — one change at a time.** Same as faceless: translate each
plain request into a single edit to `data/<slug>.overlay.json` (move a headline,
retime a caption, add a webcam bubble) and re-render. Then render once at
`--scale=1` for the final and hand off to `package-my-video` (Step 8).

## Step 3: Get or write the script

The video needs a `<slug>.script.json` (the words + beats):

- **If one exists**, read it and confirm the slug.
- **If none exists**, hand off to `script-my-video` to write one from the topic
  (it fits the hook to its window and sets one call to action). Come back with the
  script.
- For a very short faceless clip where the owner does not want a full script, a
  tight beat list you hold is enough — but a real script makes the later voiceover
  and packaging cleaner, so prefer it.

## Step 4: Auto-plan the scenes (draft, not a gate)

Call `design-my-scenes` to turn the script (or topic) into
`studio/motion/data/<slug>.scenes.json`. It **auto-assigns** a style and one visual
device per beat — you do not stop to ask the owner about art direction here. This
is the plan behind the draft they are about to watch.

## Step 5: Render a fast rough draft — the first thing the owner sees

Render the draft with a low scale so it comes back fast:

```bash
cd studio/motion
npm run render -- Video output/<slug>.mp4 --props=data/<slug>.scenes.json --scale=0.5
```

`scripts/render.js` reads the plan, hands it to the studio as input props (the
studio derives length/aspect/fps from the plan), and writes
`output/<slug>.timing.json` beside the MP4. `--gl=swangle` and a conservative
concurrency are the config defaults, so you never pass a GL backend or a pixel
format.

**Then verify the draft yourself before you show it off:** read the MP4 (and read a
still frame or two from it) to confirm it rendered on-brand and coherent — the
Studio preview can differ from the headless output (`studio/motion/CLAUDE.md` §9).
Give the owner the output path and a one-line description of what they will see.

## Step 6: React and iterate — one change at a time

Now the owner reacts to the actual video. Translate each plain request into a
single edit and re-render:

- "Make this bit longer" / "hold on that line" → bump that scene's `duration_s`.
- "That number should be bigger" / "wrong word on screen" → edit that scene's
  `visual` props or `on_screen_label` (keep it 1–4 words).
- "Try a flow here instead" → change that scene's `visual_device`.

Change **one thing, re-render, read the result, confirm it with the owner**, then
move to the next. You manage the timings; the owner never types seconds. Keep the
draft scale until the content is locked, then render once at full scale
(`--scale=1`) for the final.

## Step 7: Offer a style switch from the pre-rendered samples (optional)

If the owner wants a different look, do not describe styles in words — show them.
The studio ships fixed style samples (`Faceless` = clean editorial,
`FacelessBlueprint` = blueprint, `FacelessPop` = bold pop). Render a short branded
sample of each on the owner's brand once and cache it:

```bash
cd studio/motion
npm run render -- Faceless          output/sample-editorial.mp4  --scale=0.5
npm run render -- FacelessBlueprint output/sample-blueprint.mp4  --scale=0.5
npm run render -- FacelessPop       output/sample-pop.mp4        --scale=0.5
```

Let the owner pick the look they *see*. Then set that `direction.style` in their
`<slug>.scenes.json` and re-render their video. Style-lock and a beat-table review
are opt-in, never mandatory gates.

## Step 8: Render the final and package it

Once the content and look are locked, render once at full quality:

```bash
cd studio/motion
npm run render -- Video output/<slug>.mp4 --props=data/<slug>.scenes.json --scale=1
```

Read the final MP4 to confirm it. Then hand off to `package-my-video` to collate
the video, the thumbnail (from `make-thumbnail`), title options, and a description
with chapters (from `<slug>.timing.json`) into one publish-ready folder. Manual
upload is the honest ending — the owner uploads it themselves.

## Hard rules

- ✅ **Keyless and local.** Everything runs on the owner's machine with no accounts
  connected. The only tool is the local render (`requires_driver: render`); no
  `mcp__` tools, no network, no upload.
- ✅ **Draft-first.** The owner reacts to a rendered draft, never approves a plan or
  a spec upfront. Render before you discuss.
- ✅ **One change at a time.** Edit one thing, re-render, read it, confirm it. You
  manage timings; the owner never types a render flag or a Sequence.
- ✅ **Verify by watching.** Read the MP4 (and a still) before declaring any render
  done — the Studio preview can differ from the headless output.
- ✅ **Faceless and talking-head both ship.** Faceless is the default (Steps 3-8);
  talking-head is the footage-first Mode B flow (ingest → optional captions →
  Overlay render). Product-demo is a founder/SaaS add-on — do not attempt it here.
- ✅ **Content guardrails.** On-screen copy uses no em dashes, invents no facts or
  numbers, and names no third-party vendor. Brand voice, from
  `marketing-strategy/<BrandName>/voice.md` when it exists (identity from
  `brand.json`, which carries no voice)
  ([`knowledge/content-rules.md`](../../knowledge/content-rules.md)).

## Output shape

A finished `studio/motion/output/<slug>.mp4` on the owner's brand, its
`<slug>.timing.json` sidecar, and — after `package-my-video` — one publish-ready
folder holding the video, thumbnail, titles, and a chaptered description. The owner
watched it come together draft-first and refined it in their own words, never
touching a render flag.

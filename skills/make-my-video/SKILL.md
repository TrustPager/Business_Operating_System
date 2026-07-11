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

Ask which kind of video, and default to the one that ships:

- **Faceless (motion graphics)** — the default and what ships today. Graphics only,
  on the owner's brand. Choose this unless the owner asks otherwise.
- **Talking-head overlay** and **product/demo** are **later phases** — name them as
  coming, do not attempt them here. If the owner wants to record themselves, say
  talking-head is on the way and offer a faceless version now.

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
- ✅ **Faceless ships; other modes are later phases.** Name talking-head and
  product-demo as coming; do not attempt them here.
- ✅ **Content guardrails.** On-screen copy uses no em dashes, invents no facts or
  numbers, and names no third-party vendor. Brand voice, from `brand.json`
  ([`knowledge/content-rules.md`](../../knowledge/content-rules.md)).

## Output shape

A finished `studio/motion/output/<slug>.mp4` on the owner's brand, its
`<slug>.timing.json` sidecar, and — after `package-my-video` — one publish-ready
folder holding the video, thumbnail, titles, and a chaptered description. The owner
watched it come together draft-first and refined it in their own words, never
touching a render flag.

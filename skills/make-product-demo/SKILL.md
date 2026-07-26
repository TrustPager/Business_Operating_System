---
name: Make Product Demo
description: FOUNDER / SAAS ADD-ON. Make a "watch it get built" product demo, a fake-assistant chat driving a cursor, clicks, and a build sequence over your OWN product screenshots, with a task panel ticking off. For a founder or software business demoing their product. Not part of the everyday video flow; a service business has no software to demo. Keyless, renders on your machine.
triggers:
  - make a product demo
  - watch it get built video
  - product demo video
  - demo my product
  - show my product being used
  - build a saas demo video
function_slot: creative
requires_driver: render
requires_credential: none
data_path: local
status: active
produces_customer_facing_copy: true
---

# Make Product Demo (Founder / SaaS add-on)

**This is a labelled FOUNDER / SaaS add-on, off the default owner flow.** A
service-business owner has no software to demo, so `make-my-video` does not offer
this. Use it only when the owner is a founder or a software business who wants
their own product shown in motion: a fake-assistant chat surface driving a
cursor, clicks, and a build sequence over the owner's OWN product screenshots,
with a task panel ticking off as it goes. The reusable value is the interaction +
storytelling layer, never any product UI of ours.

You drive the **Motion Studio** (`studio/motion`) `ProductDemo` composition. Read
`studio/motion/CLAUDE.md` §2 (the props-render contract) and §6 (render-survival)
before you render. Keyless and local — the only tool is the render
(`requires_driver: render`); no accounts, no network, no upload.

## Step 1: Check the setup once

The first time you render on this machine, run the setup gate:

```bash
cd studio/motion
npm install          # first run only
npm run preflight    # Node, headless-Chrome fetch, swangle backend, a 2s test render
```

Report the result in one plain sentence. A software render is minutes, not
seconds, so a working render never looks like a hung one.

## Step 2: Collect the owner's own screenshots

The demo composites over the OWNER'S screens, never a mock of ours. Ask the owner
for a handful of screenshots (or full-resolution screen grabs) of the moments the
demo will show, and copy them into `studio/motion/public/screens/`. Name them
plainly (`dashboard.png`, `pipeline.png`). Note, for each screen, the proportional
(0-1) position of the element the cursor should land on — never guess pixel
coordinates; measure the box on the real screenshot.

## Step 3: Write the demo plan

Write a `ProductDemo` plan (see `studio/motion/data/sample.product-demo.json` for
the shape). It is a list of timed **beats**:

- A **`chat` beat** renders the assistant chat surface with a message list that is
  revealed in order over the beat. This is where the story is told.
- A **`screen` beat** renders one of the owner's screenshots, with an optional
  cursor/click (`clicks`, each an element box the ring lands on) and an optional
  `composerOverlay` that types a prompt over the screen.
- A **`progress`** block ticks tasks off across the whole clip.

**The one hard rule — never cut from "submit" straight to "done".** A beat flagged
`"build": true` must show the working sequence — a thinking row and at least one
tool row — BEFORE the final answer. The engine checks this and renders a loud
warning frame if a build beat skips it, so the rule holds even if the plan slips.

## Step 4: Draft render — the first thing the owner sees

```bash
cd studio/motion
npm run render -- ProductDemo output/<slug>.mp4 --props=data/<slug>.product-demo.json --scale=0.5
```

`render.js` derives length/fps/dimensions from the plan and writes
`output/<slug>.timing.json`. **Read the MP4 (and a still) to confirm** the chat,
the screenshots, the cursor/click, and the progress panel composited on-brand
before showing it off. Then iterate one change at a time, same as any video.

## Step 5 (optional): Transparent export for a video editor

Only if the owner wants to hand the graphics to their own editor, use the
advanced alpha door (design spec §5.4). It is never on the default path:

```bash
cd studio/motion
# ProRes 4444 (.mov) for an editor:
npm run render -- ProductDemo output/<slug>.mov --props=data/<slug>.product-demo.json --alpha
# or WebM VP9 (.webm) for the web:
npm run render -- ProductDemo output/<slug>.webm --props=data/<slug>.product-demo.json --alpha=vp9
```

`--alpha` marks the plan `transparent` (so no solid background kills the alpha)
and switches to an alpha-carrying codec. The output is a transparent overlay the
owner drops onto their own footage. Everyday demos stay on the default MP4 path.

## Hard rules

- Labelled **founder / SaaS add-on**, off the default owner flow. `make-my-video`
  must never route here.
- **Keyless and local.** Everything runs on the owner's machine; no accounts, no
  network, no upload.
- **The owner's own screenshots.** Composite over the owner's real product, never
  a mock of ours or a third-party product's UI.
- **Never eyeball a click.** Wrap the real element box (proportional coords
  measured on the screenshot); never guess an x/y.
- **Never cut from submit to done.** Build beats show thinking then tool rows then
  the result — the engine enforces it.
- **Verify by watching.** Read the MP4 (and a still) before declaring a render
  done — the Studio preview can differ from the headless output.
- **Content guardrails.** On-screen copy invents no facts or numbers and names no
  third-party vendor. Brand voice, from
  `marketing-strategy/<BrandName>/voice.md` when it exists (identity from
  `brand.json`, which carries no voice)
  ([`knowledge/content-rules.md`](../../knowledge/content-rules.md)).

## Output shape

A finished `studio/motion/output/<slug>.mp4` on the owner's brand — the
fake-assistant chat surface driving a build over the owner's own screenshots,
cursor and clicks landing on real elements, the task panel ticking off — plus its
`<slug>.timing.json` sidecar. Optionally, a transparent `.mov`/`.webm` overlay for
a video editor.

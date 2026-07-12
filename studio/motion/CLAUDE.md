# Motion Studio — Instructions for AI Assistants

You are working in the **Motion Studio**, module one of the Content Creation
Studio hub. It is a Remotion (React → MP4) engine that renders a
`<slug>.scenes.json` visual plan into a branded, motion-graphics video on the
owner's own brand, read from the root `brand/brand.json`. Nothing here needs an
account or an API key.

Read this file before touching anything in this directory. The guided owner flow
lives in the `make-my-video` skill; the scene-planning logic lives in
`design-my-scenes`. This file is the craft + the render-survival reality those
skills lean on.

---

## 1. What this is

One parametrised Remotion project, one render command, one MP4. A
`<slug>.scenes.json` plan (written by `design-my-scenes`) names, per beat, a
**style** and a **visual device**; the engine looks each up in the scene registry
and plays them in order through a `TransitionSeries`. Swap the JSON, get a new
video in a new style — no per-video component code.

- Studio preview: `npm run studio` (the Remotion Studio, live reload)
- Faceless render: `npm run render -- Video output/<slug>.mp4 --props=data/<slug>.scenes.json`
- Faceless voiceover (BYO key): `npm run voice -- <slug>` (ElevenLabs/OpenAI, degrades to silent)
- Talking-head ingest: `npm run ingest -- "<clip>" <slug> --aspect=9:16`
- Talking-head captions: `npm run caption -- <slug>` (local whisper.cpp, degrades gracefully)
- Talking-head render: `npm run render -- Overlay output/<slug>.mp4 --props=data/<slug>.overlay.json`
- Setup check: `npm run preflight`

Three modes (spec §5): **Mode A faceless** (shipping — the scenes.json registry),
**Mode B talking-head overlay** (shipping — the `Overlay` composition composites an
ingested recording with graphics + captions; see §2b), and **Mode C product/demo**
(shipping as a LABELLED FOUNDER/SAAS ADD-ON, off the default owner flow — the
`ProductDemo` composition; see §2d). `make-my-video` never routes to Mode C; the
separate `make-product-demo` skill drives it. Build only what a mode needs.

---

## 2. The props-render contract (read before touching Root.tsx or render.js)

This is the load-bearing seam that makes the studio data-driven.

- **`Video` is the one owner-facing composition.** It renders an ARBITRARY plan
  handed in as Remotion **input props**. Its `calculateMetadata` derives fps,
  dimensions, and duration from that plan (via `computeFacelessMeta`), so the
  timeline and the render can never disagree. With no props it falls back to
  `defaultProps` (the bundled sample) so the Studio always shows something.
- **`calculateMetadata` runs in a headless browser, not Node.** It cannot read a
  file off disk. So the plan must arrive *inline* as input props.
- **`scripts/render.js` does the disk read.** `npm run render` points at it. It
  resolves the plan from `--props` (a `scenesPath`, a plan-file path, or an inline
  plan), writes the resolved plan to a temp file, and hands that to
  `remotion render --props=<file>` so the plan arrives inline. Every other flag
  (`--gl`, `--scale`, `--concurrency`) is forwarded untouched.
- **The four `Faceless*` comps are fixed style samples** (static plan imports),
  kept so the owner can compare styles from pre-rendered cuts. They do not take
  props. Do not route owner renders through them; route through `Video`.
- After a successful render, `render.js` writes `<slug>.timing.json` beside the
  MP4 (§3).

The one metadata owner is `computeFacelessMeta(plan)` in
`src/compositions/facelessFactory.tsx`. Never compute fps/duration/dims a second
way.

---

## 2b. Talking-head (Mode B) — the Overlay compositing contract

`Overlay` is the second owner-facing composition (`src/compositions/Overlay.tsx`).
It is props-driven exactly like `Video`: an **overlay plan** arrives as input props
and `computeOverlayMeta(plan)` owns its fps/dimensions/duration. The plan carries a
`recording` (path under `public/`, loaded via `staticFile`), a `graphics` list
(Annotations items), a `captions` array, an optional ducked `music` bed, and an
optional `pip` box (webcam-bubble mode). See `data/sample.overlay.json`.

The load-bearing rules:

- **The recording is normalised on the way in.** Raw phone/OBS footage is often
  VFR, rotated, or HEVC — all of which drift out of sync. `scripts/ingest.js`
  re-encodes every recording to constant 30fps, upright, scaled-to-fit,
  H.264/AAC → `public/recordings/<slug>.mp4` before it is ever composited. Never
  point a plan at a raw, un-ingested file.
- **The recording renders through `<Video>` from `@remotion/media`** (frame-perfect,
  carries its own audio). Graphics layer over it by AbsoluteFill DOM/paint order;
  `PictureInPicture` gives the webcam bubble.
- **Duration comes from the recording, never hardcoded.** `calculateMetadata` runs
  in a headless browser and cannot read the file, so `scripts/render.js` probes the
  recording's real length in Node (via the shared ffmpeg resolver) and injects
  `durationInFrames` into the plan before handing it to Remotion.
- **Audio:** the recording's track flows through `<Video>`; a `music` bed is ducked
  under it via a per-frame `volume` callback (a low constant bed with short fades).
- **Captions are keyless and degrade.** `scripts/caption.js` transcribes the real
  speech with local whisper.cpp (verified working). The whole step runs from a
  SPACE-FREE working dir: `installWhisperCpp` downloads its binary zip to CWD and
  extracts it with an unquoted `Expand-Archive`, so a path with a space (this studio
  is under "Final Piece Docs"; or a Windows username with a space) would break it.
  `spaceFreeBase()` picks `tmpdir` when clean, else the Windows 8.3 short path, else
  the drive root; `BOS_WHISPER_DIR` overrides. If whisper is still unavailable it
  degrades to script/label-derived captions and says which path it took. Never claim
  whisper ran if the fallback fired.

`render.js` routes on the plan shape: a `scenes[]` plan is faceless, a `recording`
plan is Overlay. Both write the same `<slug>.timing.json`.

---

## 2c. Faceless voiceover (the VOICE rung) — the `voice` contract

Faceless videos are **silent by default** (on-strategy for muted social autoplay).
An optional synthetic voiceover is the one keyed subsystem in the whole studio; the
guided rung is the `voice-my-video` skill. The load-bearing rules:

- **`scripts/voice.js` is the connected step.** It reads the per-beat spoken text
  from `data/<slug>.script.json` (falling back to the scenes' `on_screen_label` /
  `intent`), generates **one MP3 per beat, never concatenated** at
  `public/audio/<slug>/beat<N>.mp3`, and writes `data/<slug>.voice.json` (per-beat
  file + start + duration + word/char timings). Primary provider: **ElevenLabs**
  (`ELEVENLABS_API_KEY`, `/with-timestamps` — char-level alignment, captions
  self-sync). Secondary: **OpenAI** (`OPENAI_API_KEY`, audio only; caption timing
  via the local whisper path in `caption.js`).
- **No key => graceful degrade, exit 0.** With no provider key set, voice.js prints
  a plain note that the video stays silent + captions and exits cleanly. A missing
  key is never a failure. Keys are read from the environment, never handled in files
  (`public/audio/` + `data/*.voice.json` are gitignored).
- **A plan opts into voice with `"voice": "audio/<slug>"`.** `render.js` reads
  `data/<slug>.voice.json` in Node and inlines it as `{ dir, beats }` on the plan
  (the composition runs headless and cannot read a file). `facelessFactory` layers
  each beat's `<Audio>` INSIDE that beat's scene Sequence, so it starts at the
  scene's start on the existing timeline and is clipped to the scene (no bleed).
  **`computeFacelessMeta`'s visual duration is unchanged;** voice.js warns when a
  beat's VO overruns its scene so the scene's `duration_s` can be lengthened.

---

## 2d. Product-demo (Mode C) — the `ProductDemo` contract (FOUNDER/SAAS ADD-ON)

`ProductDemo` (`src/compositions/ProductDemo.tsx`) is a **labelled founder/SaaS
add-on, off the default owner flow**. `make-my-video` never routes here; the
separate `make-product-demo` skill drives it. A service-business owner has no
software to demo — this serves a founder or SaaS client showing their own product.

It is props-driven exactly like `Video`/`Overlay`: a product-demo plan (`beats[]`)
arrives as input props and `computeProductDemoMeta(plan)` owns its fps/dimensions/
duration. The plan is a list of timed **beats** over the owner's OWN screenshots:

- **`chat` beat** — the ported chat kit (`ClaudeShell` + `ActiveChatScreen`), with
  messages revealed IN ORDER over the beat. The chat kit lives in `src/components/`
  and is brand-neutral (every colour flows from `tokens.ts`; no vendor logo or
  model name ships). Message roles are `user` / `assistant` / `assistant-thinking`
  / `assistant-tool`.
- **`screen` beat** — one of the owner's screenshots (`staticFile` under
  `public/screens/`, gitignored), with optional cursor/click (`clicks`, each a
  proportional element box wrapped in `ClickTarget` so the ring lands on the real
  element, never a guessed x/y) and an optional `ComposerOverlay` typing a prompt
  over the screen.
- **`progress`** — a `PersistentProgressPanel` ticking tasks across the whole clip.

**The baked hard rule — "never cut from submit straight to done."** A beat flagged
`build: true` is validated to show a thinking row AND at least one tool row before
the RESULT (its last assistant answer); an early acknowledgement is fine. A build
beat that skips the working sequence renders a loud in-studio warning frame rather
than a misleading cut — the rule is enforced in the engine, not left to the plan.

**Alpha / transparent export (advanced door, spec §5.4).** `npm run render --
ProductDemo output/<slug>.mov --props=... --alpha` marks the plan `transparent`
(so no solid background kills the alpha) and switches to ProRes 4444
(`yuva444p*`); `--alpha=vp9` writes WebM VP9 instead. This is the "hand it to my
video editor" escape hatch — never on the default MP4 path. `render.js` sets
`BOS_ALPHA_EXPORT` so `remotion.config.ts` skips the h264-only CRF (ProRes rejects
it). `render.js` routes on plan shape: `scenes[]` → faceless, `recording` →
Overlay, `beats[]` → ProductDemo; all three write the same `<slug>.timing.json`.

## 3. The timing sidecar (`<slug>.timing.json`)

After a render, `render.js` writes `<slug>.timing.json` beside the MP4 with
per-beat times. Shape (spec §3, identical to studio/video):

```json
{
  "slug": "quote-in-60-seconds",
  "fps": 30,
  "beats": [
    { "id": "hook", "start_s": 0.0, "end_s": 3.0 },
    { "id": "problem-to-win", "start_s": 3.0, "end_s": 7.0 }
  ]
}
```

Keyed by each scene's `beat_ref` (the script beat it realises), falling back to
the scene `id`. `package-my-video` reads this exact shape for YouTube chapters,
falling back to the script's planned `duration_s` when no render has happened.
Never change this shape without updating spec §3 and `package-my-video`.

---

## 4. The scenes.json plan (what `design-my-scenes` writes)

The plan is the spec for the video. Its schema is owned by design spec §5.2
(`docs/architecture/2026-07-09-content-creation-studio-design.md`). Top level:
`slug`, `mode`, `aspect` (16:9 / 9:16 / 1:1), `fps`, `direction` (`style` +
palette/type sources + motion/texture/mood), `rules`, `transition`, and
`scenes[]`. Each scene carries `id`, `beat_ref`, `role`, `intent`,
`visual_device`, `on_screen_label`, `motion`, `duration_s`, and a structured
`visual` object read by the device primitive.

**The shipping vocabulary** (the registry, `src/scenes/library/registry.ts`):

- **Styles:** `clean_editorial`, `blueprint`, `bold_pop`.
- **Devices** (each implemented in every style): `typographic_statement`,
  `before_after`, `process_flow`, `big_stat`.

The style owns **structure + motion**; `brand.json` owns **colour + type**.
Never hardcode either into a style. One device per scene; on-screen labels are
1–4 words. If a scene reads as "centred text on a background," it is wrong —
that is the single failure mode to design against.

---

## 5. The craft (storyboard is the spec)

Port these into every video you plan and render:

- **A beat is one idea:** one spoken line + one caption + one shot + one artifact.
  Time each beat to its narration; beats do not overlap.
- **Visualise the point, do not transcribe it.** The on-screen label is 1–4 words;
  the *device* carries the meaning (a before/after, a flow, a single big number),
  never a paragraph of subtitle.
- **Show the outcome before the steps.** Lead with the win, then how it happens.
- **One action per video.** Map the emotional arc; both entry and exit states are
  framed positively.
- **Author for the least tech-savvy viewer.** Introduce no term before it appears
  on screen; ground every spoken instruction in something visible.
- **Captions are data.** Size them for a phone — roughly 110–150px on a 1920-wide
  composition — and treat legibility as a hard requirement.
- **Never eyeball a click coordinate.** Wrap the real element; do not guess x/y.
- **Never end on black.** Hold a closing frame.
- **When you narrate a build, never cut from "submit" straight to "done"** — show
  the thinking, the steps, then the result.
- **Reuse-first.** Thin orchestrators; keep any one composition well under ~500
  lines. Evolve a component in place — never ship `Foo2.tsx` / `FooV3.tsx`.
- **Fictional data comes from one shared file** (`src/data/starter-cast.json`);
  never invent a real person, quote, or statistic.
- **A music bed is ducked under the voice** (the voice rung); it never competes.
- **Verify your source material before scripting.** Do not script a claim you have
  not grounded.
- **Review incrementally:** make one change, render a still or a short draft,
  read it, confirm it, then move on. Copy each cut the owner will judge onto the
  device they will watch it on (their phone).
- **Run every narration line through brand voice + positive-only + no-em-dash**
  before any audio is generated (the voice rung), not after.
- **Title and thumbnail are a pair.** `make-thumbnail` and `package-my-video`
  read the same `<slug>.script.json`; keep them in step.

For a premium hero (an AI-generated character or product image), layer custom
animation over it — float, glow, parallax, one canonical character across a
video — rather than dropping a flat still onto the canvas.

---

## 6. Render-survival (generic Remotion reality — read before you render)

This is not optional folklore; it is how a software render survives on a normal
laptop.

- **`npm run …`, never `npx …`** for the studio scripts. Use the package scripts.
- **Write every source file as UTF-8 with no BOM.** A BOM breaks the bundler.
- **`registerRoot(...)` is called exactly once** (`src/index.ts`). If it is
  missing or doubled, the Studio shows a black "waiting for registerRoot" screen.
- **A blank canvas means: check the BROWSER console, not the terminal.** Remotion
  renders React in a headless browser; a component error surfaces in the browser
  devtools/console, not in the Node output. This is the first place to look when a
  frame comes up empty.
- **`--gl=swangle` is a hard default** (set in `remotion.config.ts`): a
  software backend that renders identically on any machine with no GPU driver
  dependency. `--gl=angle` is an OPT-IN speed lever, and only on a machine with a
  verified working GPU. Never make the owner choose a GL backend.
- **Cap `--concurrency` well below the core count** (the config defaults to 2). A
  modest 8–16GB laptop must not thrash. Bump it per-render only on capable
  hardware.
- **Do a guarded first-render smoke test before any full render:** confirm the
  composition list loads, render a single still, then a short draft, then the full
  clip. `npm run preflight` does the machine-level version of this.
- **Software rendering is minutes, not seconds.** A 60-second 1080p clip is a
  few minutes of render on a normal laptop, not instant. Tell the owner that up
  front so a working render never looks like a hung one.
- **Owner note, plain language:** if the screen glitches or the machine reboots
  during a render, stop and check the graphics driver — that is a GPU issue, not
  a bug in the video.

---

## 7. Brand + content rules

- **All colour and type flow from `BOS/brand/brand.json`** via `src/brand.js` →
  `src/tokens.ts` (the brand bridge) and `src/fonts.ts`. NO hex literals in
  components. Edit `brand.json` (or run `/brand-my-workspace`), then
  `python tools/sync-brand.py` from the BOS root to refresh the logo/favicons, and
  every studio reskins.
- **The copy is the owner's, the palette is the owner's.** On-screen labels are
  short and in the owner's brand voice. **No third-party vendor names** anywhere a
  viewer would see them.
- **Positive framing, no em dashes** in any on-screen line — the content rules
  live in [`knowledge/content-rules.md`](../../knowledge/content-rules.md).

---

## 8. File map

```
motion/
├── CLAUDE.md                 ← this file
├── README.md                 ← human design guide
├── package.json              ← npm scripts (studio / render / still / preflight)
├── remotion.config.ts        ← render defaults: swangle, concurrency 2, h264/CRF
├── scripts/
│   ├── ffmpeg.js             ← shared 3-arm ffmpeg resolver + duration/dimension probe
│   ├── ingest.js             ← normalise a recording → public/recordings/<slug>.mp4 (CFR/H.264/AAC)
│   ├── caption.js            ← local whisper.cpp captions → data/<slug>.captions.json (degrades)
│   ├── voice.js              ← BYO-key TTS: per-beat MP3s → public/audio/<slug>/ + data/<slug>.voice.json (degrades to silent)
│   ├── render.js             ← the props seam: faceless OR overlay plan → remotion render → timing.json
│   └── preflight.js          ← "check my setup" gate
├── src/
│   ├── index.ts              ← registerRoot(RemotionRoot) — called ONCE
│   ├── Root.tsx              ← registers Video + Overlay (props-driven) + the style samples
│   ├── brand.js              ← brand tokens from BOS/brand/brand.json
│   ├── tokens.ts             ← THE brand bridge (one source of token values)
│   ├── fonts.ts              ← render-time font resolution
│   ├── compositions/
│   │   ├── facelessFactory.tsx  ← the faceless engine + computeFacelessMeta (metadata owner)
│   │   ├── Overlay.tsx          ← the talking-head compositor + computeOverlayMeta (Mode B)
│   │   ├── ProductDemo.tsx      ← the "watch it get built" add-on + computeProductDemoMeta (Mode C)
│   │   ├── Faceless*.tsx        ← fixed style samples (static plan imports)
│   │   └── Scaffold/Showcase.tsx ← engine demos on the owner's brand
│   ├── components/           ← ported brand-neutral chat kit (Mode C add-on): ClaudeShell, Sidebar,
│   │                            Composer, NewChatScreen, ActiveChatScreen, ClaudeMessage, ClaudeThinking,
│   │                            UserMessageBubble, ClaudeMcpToolUse, ApprovalPrompt, ProgressPanel,
│   │                            chat-primitives, chat-icons (neutral; AssistantMark spark)
│   ├── scenes/library/       ← the scene vocabulary (registry + per-style devices)
│   ├── overlays/             ← Annotations (graphics engine) + CaptionTrack + PersistentProgressPanel
│   ├── compositor/ primitives/ ui/  ← ported motion + UI primitives (PictureInPicture = webcam bubble;
│   │                            ComposerOverlay = prompt-over-screen, Mode C)
│   └── data/                 ← neutral starter-cast.json
├── data/
│   ├── <slug>.scenes.json    ← faceless visual plans (committed samples + owner videos)
│   ├── sample.overlay.json   ← talking-head plan shape (schema example)
│   ├── sample.product-demo.json ← product-demo (Mode C) plan shape (schema example)
│   └── <slug>.captions.json  ← per-recording caption tracks (gitignored, owner-specific)
├── public/recordings/        ← ingested owner footage (gitignored)
├── public/screens/           ← owner product screenshots for Mode C (gitignored)
└── output/                   ← rendered MP4 + timing.json (gitignored)
```

---

## 9. Behaviour expected of you

- Read the props-render contract (§2), the timing contract (§3), and the scenes
  schema (§4) before changing `Root.tsx`, `facelessFactory.tsx`, or `render.js`.
- **Verify a render by reading the MP4 (and a still from it), not just the
  Studio preview** — the browser preview can differ from the headless output.
- Keep all colour on `brand.json`; never introduce a hex literal in a component.
- Keep `computeFacelessMeta` the single owner of fps/duration/dimensions.
- If you hit something this file does not cover, ask before guessing.
```


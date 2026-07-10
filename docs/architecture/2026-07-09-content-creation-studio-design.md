# Content Creation Studio — Design Spec

**Status:** Design approved by founder 2026-07-09. Ready for implementation planning.
**Supersedes/extends:** realizes founder-decisions **D13** (genericised Remotion studio as a library module); revises one line of [`2026-07-05-youtube-studio-design.md`](2026-07-05-youtube-studio-design.md) Decision 8 (labelled). One home for the ruling: founder-decisions.md **D14**.
**Origin:** Packaging the TrustPager-coupled `Remotion-VideoStudio` (RVS) repo as a brand-agnostic, keyless, guided BOS add-on. Design produced by a 15-agent mapping + feasibility pass and three adversarial reviews (keyless integrity, decoupling completeness, guided-process realism); this spec folds in every review fix.

---

## Founder decisions (locked 2026-07-09)

1. **Reverse Decision 8** ("no Remotion in the BOS") as an **explicit, labelled, scoped exception**. The keyless `studio/video` Puppeteer floor stays untouched. The Remotion engine gets exactly one contained home inside the BOS. This must be logged in [`founder-decisions.md`](founder-decisions.md) and cross-referenced from the youtube-studio spec's Decision 8 as a labelled override (per the one-rule-one-home / label-divergence doctrine).
2. **Lead with faceless + talking-head** as the core client product. The product-demo "watch it get built" kit (Claude-chat UI + build sequence) becomes a **separate, clearly-labelled founder/SaaS add-on**, off the default owner flow. A service-business owner has no software to demo.
3. **Local, keyless captions for talking-head** via `@remotion/install-whisper-cpp` (whisper.cpp), so casual off-script recording captions itself with no API key.
4. **"Content Creation Studio" is an umbrella hub.** The Remotion video engine is module one, in its own folder (working internal name `studio/motion/`) so it does not collide with the existing `studio/{og,social,cta,thumbnails,video}` set. Voiceover, audio, and future add-ons attach under the hub later. Build lean now (video engine only); lay out the hub structure so it grows.

---

## 1. Positioning and scope

**Promise:** "High-quality video is no longer outside your purview." Any BOS owner produces professional video on their own brand, keyless day one.

**Umbrella:** *Content Creation Studio* — a hub that will grow to hold multiple content-production modules. Module one is the Remotion video engine (`studio/motion/`). Future modules (voiceover, audio, others) attach under the same hub brand.

**Three video modes** (one parametrised Remotion project, one render command, one MP4):
- **Mode A — Faceless synthetic** (core, default, keyless). Motion-graphics-only, the founder's own style.
- **Mode B — Talking-head overlay** (core, keyless). The owner records themselves; the studio composites graphics over/around the recording, all in Remotion.
- **Mode C — Product / demo** ("watch it get built"). **Founder/SaaS add-on, not in the default owner flow.** Uses the ported Claude-chat + cursor/build kit over the owner's own product screenshots.

**ICP:** Australian service businesses (owner-operated; the owner is the one in the Claude Code session). Modes A and B are what they make. Mode C serves the founder and SaaS clients.

---

## 2. The gating ruling (Decision 8 reversal)

The prior ruling built `studio/video` on Puppeteer frame-capture specifically to avoid a Remotion dependency, and reserved Remotion for the separate RVS repo. The founder's product is **not achievable** on frame-capture: Puppeteer-screenshot-per-frame cannot composite a user's recording with its own audio into one mixed MP4, cannot export ProRes 4444 alpha, and cannot run `spring()`/`@remotion/media`. This is a capability gap, not a preference.

**Ruling (logged as D14):** Remotion is permitted inside the BOS in **one** contained module (`studio/motion/`) under the Content Creation Studio hub. This is not a wholesale reversal: it **realizes founder-decisions D13** (the genericised Remotion studio was already blessed as a future library module) and **revises one line of Decision 8** (labelled) that had reserved the heavyweight engine to RVS only. It accepts one render-engine "duplication" (frame-capture floor + Remotion premium) because the two are different rungs on the floor/shelf ladder, not a reskin of each other. The keyless `studio/video` floor is unchanged and remains the YouTube factory.

---

## 3. Architecture

### 3.1 Hub + module placement

```
studio/
  video/              # UNCHANGED keyless Puppeteer floor (the existing 5th studio)
  motion/             # NEW: Remotion video engine, module one of the Content Creation Studio hub
  ...                 # og, social, cta, thumbnails unchanged
docs/content-creation-studio/
  hub.md              # the umbrella: what the hub is, which modules exist, how a module is added
```

The hub is, for now, a documented brand + a thin registry convention (`hub.md` lists modules). We do **not** over-build an umbrella framework before there is a second module (YAGNI). The structure simply reserves the shape: modules live under the hub brand and share the BOS brand system + the `.script.json`/`.timing.json` contract.

### 3.2 `studio/motion/` folder layout

```
studio/motion/
  package.json          # remotion, @remotion/media, @remotion/captions, @remotion/transitions,
                        # @remotion/shapes, @remotion/paths, @remotion/noise, @remotion/motion-blur,
                        # @remotion/install-whisper-cpp, ffmpeg-static, @remotion/google-fonts
  remotion.config.ts    # DEFAULT --gl=swangle (machine-independent); conservative concurrency;
                        # h264/CRF; alpha profiles documented as opt-in only
  tsconfig.json
  src/
    index.ts            # registerRoot(RemotionRoot) — MUST exist or black screen
    Root.tsx            # registers ONLY Faceless / Overlay (+ ProductDemo when the add-on is installed).
                        # Must import NO existing TrustPager composition.
    brand.js            # import brand from '../../../brand/brand.json' — byte-identical loader to studio/social
    theme.ts            # THE brand bridge: maps brand.js tokens -> the token shape every ported component reads
    tokens.ts           # colour + type tokens (the sweep target; see §4)
    compositor/         # PORTED motion primitives (cursor/click/build/connector/callout/PiP/progress)
    components/         # PORTED Claude chat kit (ships only with the product-demo add-on)
    overlays/           # PORTED Annotations (caption/headline engine) + PersistentProgressPanel
    scenes/
      shared/           # PORTED ClickIndicator (ClickTarget + TutorialCaption)
      library/          # NEW brand-neutral scene vocabulary (diagram/metaphor/before-after/flow/data-viz/typographic)
    compositions/
      Faceless.tsx
      Overlay.tsx
      ProductDemo.tsx   # add-on only
    data/
      starter-cast.json # NEW neutral fictional roster (replaces the TrustPager roster)
  scripts/
    ingest.js           # NEW: normalise an owner recording (CFR H.264/AAC) — reuses studio/video's ffmpeg-static resolver
    caption.js          # NEW: local whisper.cpp transcription -> Caption[] for talking-head
    render.js           # wraps npx remotion render; emits <slug>.timing.json
    preflight.js        # NEW: node/ffmpeg/browser-fetch/backend check + 2s test render, plain-English pass/fail
  public/
    logo.png, favicon-* # pushed by tools/sync-brand.py (auto-discovered)
    recordings/         # owner's ingested talking-head footage
    audio/<slug>/       # per-beat MP3s (voice rung only); music-bed.mp3
  CLAUDE.md             # scrubbed operating manual (§8)
  README.md
  output/  node_modules/  # gitignored
```

### 3.3 Brand bridge (corrected — this is a real sweep, not one file)

The design's original "no component reads a hex literal, one `theme.ts`, LOW effort" claim was **false** (decoupling review). Reality:
- ~50 hardcoded colour literals in `compositor/`, ~48 in the chat kit. TrustPager **clay `#c96442` / `hsl(15,63%,50%)`** and **teal `#29c6c6` / `hsl(174,64%,47%)`** are baked as **default values, not props**, in components otherwise fit to keep (`CursorClick`, `ClickPulseRing`, `ComposerOverlay`, `ConnectorLine`, `CrossHighlight`, `PipelineRewireGlow`, `ClaudeMcpToolUse`, `scenes/shared/ClickIndicator`). The Claude `theme.ts` does **not** feed the compositor.
- Two font sources (`Claude-src/fonts.ts`, `TrustPager-src/fonts.ts`) plus hardcoded `Plus Jakarta Sans` literals.
- `ClickPulseRing` bakes the string `'trustpager'` into its exported **type** and colour-convention comments (semantic coupling, not a colour value).

**Bridge design (single owner):** `tokens.ts` is the ONE source of token values, mapping `brand/brand.json`'s existing semantic keys (verified schema: `colors.{primary, primaryDeep, primaryTint, accent, deepBlue, text, textMuted, panel, border, pageBg, canvasBg, success, warning, ...}`, `gradient`/`heroGradient`/`warmGradient`, `fonts.{primary, serif, mono}` as CSS stacks, `googleFontsHref`) onto the token names the ported RVS components expect. `theme.ts` is at most a thin adapter re-exposing `tokens.ts` in the legacy `theme` shape, not a second brand source. Every ported component's **default** reads a token, never a baked clay/teal fallback. The colour-role vocabulary is renamed brand-neutral (`primary`/`accent` or `app`/`assistant`, never `trustpager`/`claude`).

**Fonts (mechanism — was missing):** the neutral default `brand.json` uses system-font CSS stacks (`-apple-system, ...`), so the default render needs no font loading at all. When an owner sets a real brand font, load it for the render: `@remotion/google-fonts` for a Google family, or `loadFont()` from a self-hosted file (`staticFile`) for a non-Google face; fall back to the CSS stack in `brand.fonts.primary` when neither resolves. `googleFontsHref` (a `<link>` the still-studios use) does NOT load a font into a Remotion render, so it is treated as a hint, not the mechanism. The exact family map is a Phase 1 deliverable.

`sync-brand.py` auto-discovers `studio/motion/` (direct child of `studio/` with a `public/`) and pushes logo + favicons on dev-server restart, no code change. Owner brand survives `update-bos` because `brand.json` + logo + favicons are git-untracked.

**Effort re-rating:** the decoupling is **MEDIUM**, not LOW. Pervasive but mechanical: a ~100-literal sweep across two component trees + a font consolidation + a type/convention rename fan-out. Not a single-file swap.

### 3.4 Engine-swappable contract (the payoff)

`studio/motion` reads the **same** `<slug>.script.json` and emits the **same** `<slug>.timing.json` shape as `studio/video`. So `script-my-video`, `make-thumbnail`, and `package-my-video` drive either studio unchanged. A new `<slug>.scenes.json` sidecar (keyed to beat ids, never rewriting the script) carries the visual plan.

---

## 4. KEEP / STRIP / ADAPT manifest (corrected & completed)

"Crown jewel" = reusable storytelling infrastructure. This section is now **exhaustive over `src/`** (the decoupling review flagged three whole trees the first pass missed).

### 4.1 `src/compositor/` — reusable motion engine
KEEP (brand via token default): `CursorHover`, `CursorPath`, `AutomationBuildSequence`, `NoAutomationsCard`, `PictureInPicture` (core to the talking-head bubble), `Callout`, `DebugOverlay`, `animations.ts`, `ActOffsetWrapper`.
**ADAPT (colour-literal sweep — re-rated from KEEP):** `CursorClick`, `ClickPulseRing` (+ `'trustpager'` type/convention rename), `ComposerOverlay`, `ConnectorLine`, `CrossHighlight`, `PipelineRewireGlow`, `AutomationLightningStrike`, `AutomationPreviewCard` (When/Then copy), `StageAutomationBadges` (font+shadow), `composition-helpers.tsx` (rename the "TrustPager API" comment), `compositor/index.ts` (drop `trustpager-positions` re-exports; fix header mojibake).
STRIP: `trustpager-positions.ts` (only the `StagePosition` interface shape survives).

### 4.2 `src/Claude-src/components/` — the "watch it get built" surface (ships with the Mode C add-on only)
KEEP (token swap): `ClaudeShell` (make `tp-favicon.png` a prop), `Sidebar`, `Composer`, `NewChatScreen` (fix teal CSV-chip), `ActiveChatScreen` (strip disclaimer + hardcoded model default), `ClaudeMessage`, `ClaudeThinking`, `UserMessageBubble`, `ClaudeMcpToolUse` (parameterise clay spinner), `ApprovalPrompt`, `ProgressPanel`, `index.ts` (prune settings-replica exports if unused).
STRIP: `ChatBubble` (`@deprecated`, unexported).
ADAPT: `theme.ts` (folds into `tokens.ts`).
Settings-replica screens (`ClaudeProfileMenu`, `ClaudeSettingsPage`, `CustomizeClaudePage`, `CustomizeConnectorsPage`, `AddCustomConnectorDialog`) — **ship only inside the Mode C add-on** (pixel-matched claude.ai settings screens, useful only for connect-a-tool demos); otherwise STRIP. Not in the default studio.
**Phasing note:** the entire chat-kit colour sweep (~48 literals) is **Phase 5 (Mode C add-on) work**, not Phase 1. Phase 1's ~50-literal sweep covers the compositor + overlays only (see §10).

### 4.3 `src/TrustPager-src/` (path alias `@tp/* → TrustPager-src/*`) — 60 files, `@tp/*` imported 236×
Verified `@tp/*` surface and per-area verdicts (grepped from source):
- `@tp/components/ui/*` (`card`, `badge`, `avatar`, `date-badge`, `clean-button`, `input`, `premium-textarea`, `select`, `dialog`, `switch`, `category-tag`, `PageHeader`, `DataTable`, `stat-card`, `gradient-tabs`) — **ADAPT**: extract as brand-neutral shadcn-style primitives, tokenise, and bring their internal `lib`/`cn()` helper with them.
- `@tp/theme` — **STRIP** (folds into `tokens.ts`).
- `@tp/icons/*` — **ADAPT**: replace with a generic icon set (`src/icons.tsx`, e.g. `lucide-react`) so no ported file imports `@tp/icons`.
- `@tp/components/{navigation,documents,notepads,crm}/*`, `@tp/document-builder/*`, `fonts.ts`, the page mocks — **STRIP** (product-specific).
- **tsconfig remap:** `studio/motion/tsconfig.json` drops the `@tp/*` alias; extracted primitives get a new local alias (e.g. `@ui/*`) or relative imports. No `@tp/*` alias survives.
- **Port-order dependency (verified):** the KEEP `primitives/` (`Avatar`/`Button`/`Tag`/`DateBadge`) and some KEEP scenes (`scenes/shared/TutorialUI`) import `@tp/components/ui/*` **and** `@tp/components/navigation/{UserProfileMenu,ServiceRequestButton}`. So `ui/*` + `icons.tsx` must land **before** `primitives/`, and the navigation imports inside `primitives/` are dropped (product chrome, not needed for a brand-agnostic primitive).

### 4.4 `src/compositions/` — 15 assemblies + `acts/` + `ai-bos/` + `_template/` (unclassified in the first pass)
**STRIP:** all product assemblies incl. `HybridCompositions.tsx` (**Hybrid-LeadsPipeline-Build**), `FeatureCompositions`, `WhyClaudeTrustPager`, `ClaudeVideo1`, `TutorialConnectClaudeV3`, `TutorialMigrateData`, `acts/`, `ai-bos/` (its own `tokens.ts`, `HeroFigure`). These consume `TRUSTPAGER_STAGES`; the new `Root.tsx` imports none of them.
**ADAPT (optional):** a genericised `_template/HybridVideoTemplate.tsx` if useful as a starting scaffold (strip its `TRUSTPAGER_STAGES` import).

### 4.5 `src/scenes/features/` — TrustPager product UI
STRIP: `PipelineView`, `StageColumn`, `PipelineCard`, `PipelineToolbar`, `PipelineDragOverlay`, `ConnectedPipelinesPanel`, and the ~107 CRM page mocks (these ARE the product being demoed; the owner's own screenshots replace them in Mode C).
ADAPT (only if a client demos a CRM-like product): collapse the 5 `*Layout.tsx` app-shell scaffolds into one generic shell.

### 4.6 Remaining `src/` dirs (swept per review)
KEEP: `scenes/shared/ClickIndicator.tsx` (crown-jewel click primitive, referenced 74×, `resolvePalette()` already colour-agnostic — rename `'teal'` role), `primitives/` (`Avatar`/`Button`/`DateBadge`/`Tag`, generic), `overlays/PersistentProgressPanel`.
ADAPT: **canonical annotation source = `overlays/Annotations`** (strip teal→blue gradient + `Plus Jakarta Sans`); reconcile `Claude-src/overlays/Annotations` (keep only its renderers; `ELEMENT_POSITIONS` is per-screen) and the top-level `annotations/` file into it, then delete the duplicates. **Canonical animation source = `compositor/animations.ts`**; fold any unique helpers from top-level `animations/` and `Claude-src/animations` into it, then delete the duplicates.
STRIP / neutral-seed: `promo/`, `stills/FocusedStills.tsx` (imports `professional-services.json`), `data/professional-services.json`, `data/reporting-demo.json`, `data/permission-scopes.ts`, the TrustPager fictional roster (Coastal Consulting, Evie, Sarah Chen). Ship a fresh neutral `starter-cast.json`. `hooks/` — **KEEP by default** (frame/timing utilities); Phase 1 confirms per-file that none import `@tp`/brand.

### 4.7 Thumbnails
Confirm no TrustPager-branded thumbnail template ships. `make-thumbnail` is reused unchanged **only if** its templates carry no baked colour/logo/wordmark; otherwise route them through `brand.json` like everything else.

---

## 5. The three modes (all-in-Remotion)

All feasibility claims below verified **feasible, keyless** in the research pass.

### 5.1 Mode A — Faceless synthetic (default, keyless)
Graphics-only composition: ported compositor primitives + the new `scenes/library/` vocabulary, sequenced with `<Series>`/`<Sequence>`, entrances via `spring()`. Driven by `<slug>.scenes.json` so each beat renders its **meaning** as a device (diagram/metaphor/before-after), not a paragraph of caption text. Audio: silent enforced stereo track by default; per-beat VO on the voice rung. `@remotion/effects` is **not needed** — effects are custom CSS/SVG + the installed `motion-blur/noise/paths/shapes/transitions` packages, all local. Quality is motion discipline (spring physics, staggered timing, negative space), not effects.

### 5.2 Mode B — Talking-head overlay (keyless)
The owner's recording is one layer, rendered with `<Video>` from `@remotion/media` (frame-perfect, carries its own audio). Graphics layer via DOM order in `<AbsoluteFill>`; `PictureInPicture` gives the webcam-bubble look. Duration comes from the recording via `calculateMetadata()`, never hardcoded. Remotion sums the recording's audio + any music/VO into one AAC track; music ducks under voice via a per-frame `volume` callback.
- **Component choice (verified, no contradiction):** use `<Video>` from `@remotion/media` (Remotion's recommended path for new projects); it renders through `<OffthreadVideo>` under the hood, which is what provides HEVC support and the `transparent` frame-extraction used for alpha (§5.4). Embedding a user recording + mixing its audio is **net-new** for this codebase (RVS today uses only `<Audio>`, never `<Video>`/`<OffthreadVideo>`), so this path gets its own smoke test before Mode B ships.

**Two hard operational rules** (feasibility + review): (1) **normalise every upload to CFR H.264/AAC on ingest** (`scripts/ingest.js`) or VFR phone/OBS recordings drift out of sync — the #1 trap; (2) iPhone HEVC hits the slow `<OffthreadVideo>` fallback, so transcode to H.264 on ingest. `ingest.js` **reuses `studio/video/scripts/render.js`'s ffmpeg resolver** (bundled `ffmpeg-static` preferred → system ffmpeg → graceful message, never hard-fail), and `ffmpeg-static` is a package dep so it works after a plain `npm install`.

**Captions (keyless, corrected):** talking-head captions come from **local whisper.cpp** (`@remotion/install-whisper-cpp`) transcribing the owner's actual speech → `Caption[]`. This makes casual off-script recording caption itself with no key. One-time model download (~150MB–1GB). Faceless captions can still be script-derived (see §6).

### 5.3 Mode C — Product / demo (founder/SaaS add-on, off the default flow)
The reusable value is the **interaction + storytelling layer** (cursor/click/build/progress/annotation over the owner's own screenshots or screen-recording), not any product UI. The Claude-chat kit is only relevant to owners whose product has an AI/chat surface, so it ships **inside this add-on**, never in the default owner mode gate. The "never cut from submit straight to done" rule is baked in (thinking → tool rows → result). TrustPager CRM mocks are stripped; the owner supplies their own screens.

### 5.4 Alpha / transparent-overlay export (advanced, hidden)
Feasible, keyless, but **behind an "advanced / hand this to my video editor" door** — never a codec or pixel-format choice on the default path. When invoked: ProRes 4444 `.mov` (`--codec=prores --prores-profile=4444 --pixel-format=yuva444p10le --image-format=png`) for editors; WebM VP9 for web. Gotcha handled by shipping a transparent-canvas composition variant (any solid `background-color` kills alpha; embedded footage must use `<OffthreadVideo transparent>`).

---

## 6. Keyless voice and captions

**Only one subsystem is keyed: synthetic VO generation.** Render, captions, and effects are 100% local.

**Default rung (keyless):**
- Silent enforced stereo track (`--enforce-audio-track`) — social autoplays muted, so caption-only is on-strategy.
- **Faceless captions** are built from `<slug>.script.json` (ground-truth text already in hand; per-word timing estimated ~2.5–3 w/s). State plainly that estimated timing suits short faceless beats and muted-autoplay social; owners can nudge per-beat timing conversationally.
- **Talking-head captions** use local whisper.cpp (§5.2) — accurate over real speech, keyless. `@remotion/install-whisper-cpp` provides the whole chain (`installWhisperCpp`, `downloadWhisperModel`, `transcribe`, `toCaptions`), so no extra caption-conversion dependency is needed. It compiles whisper.cpp locally and downloads a model (~150MB–1GB) — gated in preflight (§9), with fallback to script-derived captions if the compile fails.
- `@remotion/captions` mirrors the existing custom `Caption` renderer's type; whitespace is significant (leading space per token, `whiteSpace:'pre'`).

**Upgrade rung (bring-your-own-key synthetic voice):**
- **ElevenLabs primary** — `/text-to-speech/{voice}/with-timestamps` returns audio + char-level alignment in one call, so captions auto-sync. Remotion ships an ElevenLabs adapter.
- **OpenAI TTS secondary** (cheaper, audio-only) — captioned via a Whisper pass; may drift from script. Owner-facing line: "ElevenLabs voices caption themselves; OpenAI voices get captioned by transcribing them back."
- **Explicitly NOT** TrustPager `ai_generate_speech`; the "Jimbo" voice is locked in TrustPager's account and not portable. Dropped.
- Wire as a **plan/run seam** (reuse the Meta-Ads connected-driver pattern): keyless "thinking" writes the VO script (green under `BOS_OFFLINE`); connected "doing" calls the keyed TTS; missing/invalid key **degrades gracefully** to silent + captions. One MP3 per beat, never concatenated.

---

## 7. Skill cluster and the guided flow (DRAFT-FIRST)

Author every skill as **numbered gates before defaults**, keyless-floor unless it needs a credential, **dogfooded on Sonnet** as the merge gate.

| Skill | New/Extend | Does |
|---|---|---|
| `script-my-video` | Extend | Already emits `<slug>.script.json`. Add mode-awareness only; do not fork the schema. |
| `design-my-scenes` | NEW (keyless) | Emits `<slug>.scenes.json` sidecar keyed to beat ids. Enforces: translate meaning to one visual device (≤4-word labels, one device per scene) and a machine-checkable lint (or Sonnet drifts back to subtitle paragraphs). **Defaults everything** — it does not gate the owner on art-director choices upfront. |
| `make-my-video` | NEW (`requires_driver: render`, keyless local render like `design-my-site`) | Drives `studio/motion`. Chooses mode, runs footage intake, generates compositions, renders a **fast rough draft first**, then iterates. |
| `voice-my-video` | NEW (connected rung) | Keyless "thinking" writes VO script; connected "doing" calls ElevenLabs/OpenAI; degrades to silent+captions. |
| `make-thumbnail` / `package-my-video` | Reuse | Unchanged; engine-agnostic via `.script.json`/`.timing.json`. |

### 7.1 The guided flow (inverted per the realism review — react to an artifact, never approve a spec)

1. **Choose mode** — faceless / talking-head (Mode C hidden unless the add-on is installed).
2. **Footage intake FIRST (talking-head)** — the explicit first gate. Accept a file path or walk the owner through getting the clip off their phone; copy/rename it into `recordings/` for them; auto-correct orientation and resolution/aspect mismatch; report in one plain sentence ("got your 47-second clip, portrait, iPhone HEVC, fixed and ready"). **Mode B does not ship until this is tested against a genuine unedited phone MP4.**
3. **Script** — hand to `script-my-video` if none exists, else read the existing one.
4. **Draft** — `design-my-scenes` **auto-assigns** a default style + visual devices; the studio renders a fast rough cut. **This is the first thing the owner sees.**
5. **React & iterate** — one change at a time; the assistant translates plain requests ("make this bit longer", "hold on that line") into `scenes.json`/timing edits and re-renders only changed scenes. **Timings are assistant-managed; the owner never types seconds.**
6. **Style (optional, from samples)** — if the owner wants a different look, show **pre-rendered 3–5s branded samples** of each shipping style (rendered once on their `brand.json`, cached) and let them pick what they see, not a token name. Beat-table approval and explicit style-lock are opt-in controls, not mandatory gates.
7. **Compose** — layers assemble to one MP4 (alpha export only via the advanced door).
8. **Package** — `package-my-video` collates the upload folder; chapters from `.timing.json`.

The owner edits only an author-editable block (prompt, beat labels, titles, style choice). Never a render flag, a `<Sequence>`, or a pixel format.

### 7.2 `<slug>.scenes.json` schema (engine-independent sidecar)
Keyed to beat ids; carries `mode`, `aspect`, a defaulted `direction` (style/motion/texture/mood; `palette_source`/`type_source` = `brand/brand.json`), `rules` (`on_screen_max_words:4`, `visualize_not_transcribe:true`, `one_device_per_scene:true`), and per-scene `{id, beat_ref, role, intent, visual_device, visual, on_screen_label, motion, duration_s}`. The style token owns **structure + motion**; `brand.json` owns **colour + type**. Never hardcode either into a style.

---

## 8. Scrubbed operating manual (`studio/motion/CLAUDE.md`)

**PORT (the craft):** storyboard-is-the-spec; beat = one VO line + one caption + one shot + one artifact; time each beat to its VO, no overlap; per-beat VO never concatenated; run every narration line through brand/voice + positive-only + no-em-dash **before** generating audio; map the emotional arc, one action per video; **visualise the point, don't transcribe** (1–4 word labels); show outcome before steps; ground every spoken instruction visually; introduce no term before it appears; author for the least tech-savvy viewer; captions are data; size captions for a phone (~110–150px on a 1920 comp); never eyeball click coords (wrap the real element); mandatory cheap still-check at every click/legibility frame; "watch it get built" (never cut submit→done); reuse-first thin orchestrators, compositions well under ~500 lines; never version component files (evolve in place); fictional data from one shared file; never end on black; music bed ducked under VO; verify source material before scripting; incremental review (one change, still, verify, confirm, copy each cut to the owner's phone); a premium-asset hero pipeline (stills → identity-preserving edits → transparent PNG composites → float/glow/parallax, one canonical character across a video); title+thumbnail as a pair, publish the ToS-safe way.

**PORT (genericised — the review's most important catch):** the Windows/Remotion **render-survival** knowledge is *generic Remotion reality, not TrustPager scar tissue*. Include, names scrubbed: `npm run` not `npx`; write files as UTF-8 **no BOM**; `registerRoot` called exactly once, and **"blank canvas = check the BROWSER console, not the terminal"**; `--gl=swangle` a **hard default**, `angle` an opt-in speed lever needing a working GPU; **cap `--concurrency` well below core count**; a **guarded first-render smoke test** (compositions → single still → short draft) before any full render; a plain-language owner note: "if your screen glitches or the machine reboots during a render, stop and check your graphics driver"; and realistic render-time expectations for software rendering (a 60s 1080p clip is minutes, not seconds).

**DROP (scar tissue):** the angle-vs-swangle NVIDIA saga and "verified clean on THIS machine"; `content-pipeline/remotion is dead` warnings; the 2026-05-27 cleanup punch list and V2/V3 prune diaries; absolute local paths, Dropbox folder, ports 3210/3310; all TrustPager brand/product specifics and `TRUSTPAGER_STAGES`/Hybrid comp; the TrustPager roster; all TrustPager API/infra plumbing (`ai_generate_speech/image/music`, `TRUSTPAGER_API_KEY`, Jimbo/Jessica voice ids, edge-function timeout, help-center webhook); named real-person data (keep the fictional-only rule, drop the names); PowerShell 5.1 authoring gotchas; stale live counts; AI-BOS project state; two-repo/`/help-publish` plumbing; onboarding-program specifics.

---

## 9. Environment and hardware reality (keyless ≠ frictionless)

`make-my-video` opens with a one-time **`preflight.js`** "check my setup" gate: verify Node, run `npm install`, explicitly trigger Remotion's first-render **headless-Chrome fetch (~150MB)** with a clear progress/failure message (fails opaquely behind corporate proxy/AV), **validate the `swangle` backend works** (offer `angle` only as an opt-in speed lever, never a choice the owner must make), do a 2-second test render, and report pass/fail in plain English. For talking-head (Phase 3) a second gate installs/compiles whisper.cpp and downloads the model (~150MB–1GB) with progress; the whisper.cpp compile needs a C/C++ build toolchain, the fragile step on a stock Windows laptop, so it degrades to script-derived captions on failure rather than blocking. Document a minimum-RAM floor and expected render duration so a non-dev isn't staring at a hung-looking terminal. Default concurrency conservatively.

**Remotion licence gate:** no API key, but a **4+ person for-profit company legally needs a paid Remotion Company Licence** — the modal Aussie service firm, not an edge case. First-run, plain-English, one-time acknowledgement recorded in the owner profile before the first render ("Remotion is free for teams up to 3; 4+ people need a paid Company Licence before publishing commercially"). Pass `licenseKey:'free-license'` at render for the small-team path (verified: `renderMedia()`/`renderStill()` accept it; it is telemetry and honor-based, never blocks a render, so the recorded acknowledgement is the real business gate). Marketing copy says **"no API keys," never "free."**

---

## 10. Phased build plan

- **Phase 0 — Log the ruling (no code).** Record the Decision 8 reversal in `founder-decisions.md`; add a labelled override note to the youtube-studio spec's Decision 8.
- **Phase 1 — Extract the brand-agnostic engine.** Port compositor + overlays + ClickIndicator + primitives into `studio/motion/src`; run the colour-literal sweep for **the compositor + overlays only** (the chat-kit sweep is Phase 5) into `tokens.ts` ← `brand.js` ← `brand.json`; extract the generic `@tp/components/ui/*` primitives + a generic `icons.tsx` and remap the tsconfig alias, dropping the navigation imports `primitives/` pulls in; rename the `'trustpager'` colour role; wire the font loader (§3.3); drop `trustpager-positions` re-exports; strip `ChatBubble`, the `compositions/` product tree, and the scenes/CRM mocks; ship neutral `starter-cast.json`; wire `sync-brand.py` auto-discovery; add `preflight.js`. **Deliverable:** a Remotion studio rendering a **hardcoded scaffold composition** on the owner's brand with zero TrustPager tokens, proving the token + font bridge. The `.scenes.json`-driven pipeline is Phase 2, not this. **Risk:** verify no hex/font leaks survive the sweep (CSV-chip teal, tool-use spinner clay, annotation gradient, `Plus Jakarta Sans`), and that the `@tp/components/ui` extraction + `icons.tsx` land **before** `primitives/` so imports do not break.
- **Phase 2 — Faceless mode (FIRST SHIPPABLE).** `design-my-scenes` (schema + lint) + the `scenes/library/` vocabulary; `make-my-video` faceless gates with the **draft-first** flow and style-from-samples; silent+captions keyless default. **Risk (make-or-break):** the scene library must have genuine diagram/metaphor primitives, not styled text, or "visualise the point" degrades to "animated captions."
- **Phase 3 — Talking-head mode.** `ingest.js` (CFR normalise, orientation/resolution fix, ffmpeg-static resolver), **footage-intake gate**, `caption.js` (local whisper.cpp), `Overlay.tsx`, `calculateMetadata` duration, `PictureInPicture` bubble, audio mixing/ducking. **Risk:** VFR/HEVC drift — the ingest pre-pass must run on every upload; test against a real unedited phone MP4 before shipping. A whisper.cpp readiness gate (install/compile + model download) must precede the first caption, degrading gracefully to script-derived captions if the Windows compile fails.
- **Phase 4 — BYO-key voice rung.** `voice-my-video` plan/run seam: ElevenLabs primary (single-call timestamps), OpenAI+Whisper secondary, graceful degrade to silent+captions.
- **Phase 5 — Product-demo add-on (founder/SaaS).** `ProductDemo.tsx` + the Claude-chat kit + build-sequence + progress, over the owner's own screenshots; alpha export behind the advanced door. **Includes the chat-kit colour-literal sweep (~48 literals) deferred from Phase 1**, plus the settings-replica screens if a connect-a-tool demo is in scope. Packaged and labelled as a separate add-on, off the default owner flow.
- **Phase 6 — Full generalisation + Sonnet dogfood gate.** Registry regen, hub `hub.md`, `docs/CAPABILITIES.md`, starter-projects/connectors entries, `check-connectors.py`/`check-onboarding-binding.py` green, the scrubbed `CLAUDE.md`, and a **Sonnet dogfood of both core modes** as the merge gate — scoped honestly to "skill logic + one-machine render completes," paired with `preflight.js` + conservative defaults as the actual owner-hardware protection.

---

## 11. Remaining open questions (minor; do not block Phase 0–1)

1. **Which 2–3 scene styles ship first?** Recommend 2–3 solid brand-neutral languages at launch rather than over-promising a big library. Founder to name the founding aesthetics. **Must be resolved before Phase 2:** each launch style needs at least one worked scene primitive per `visual_device` as Phase 2's definition-of-done (not just a category name), so "visualise the meaning" has a concrete acceptance test.
2. **Confirm ElevenLabs as the default paid voice provider** (recommended) with OpenAI secondary.
3. **Licence presentation** — acknowledgement wording/placement (drafted in §9; founder to approve copy).

---

## 12. Honest risk summary

The decoupling is mechanical but **MEDIUM** (a ~100-literal sweep + an unclassified UI-kit tree + a compositions strip + a type rename), not the trivial one-file swap the first pass claimed. The render/captions/effects pipeline is genuinely keyless and local; the only keyed dependency is synthetic VO, handled by the rung. The two real risks are not decoupling: (1) **scene-library craft** (Phase 2) — making "visualise the meaning" repeatable enough that a non-dev on Sonnet gets directed video, not animated captions; and (2) **owner-hardware fragility** (Phases 3, 9) — Remotion's heavy footprint, first-render browser fetch, VFR/HEVC drift, and software-render time on a modest laptop. Both are mitigated above (scene primitives + lint; preflight + conservative defaults + graceful degradation), not hand-waved. The Remotion 4+ person licence is a real cost obligation for a meaningful slice of the ICP and is surfaced in-flow, not buried.

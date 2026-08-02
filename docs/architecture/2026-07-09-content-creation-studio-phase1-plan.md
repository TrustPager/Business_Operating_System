# Content Creation Studio — Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (fresh subagent per task + review) or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax. Load `remotion-best-practices` before writing/editing any Remotion code.

**Goal:** Stand up `studio/motion/` — a keyless, brand-agnostic Remotion studio that renders a hardcoded scaffold composition on the owner's `brand/brand.json`, with **zero TrustPager tokens, strings, or imports**. This proves the engine + brand bridge; the `.scenes.json`-driven pipeline and the three modes are Phases 2+.

**Architecture:** Port the reusable RVS engine (compositor primitives, overlays, ClickIndicator, primitives, extracted `@tp/components/ui`) into `studio/motion/src`, behind a single `tokens.ts` brand bridge fed by `brand.js` ← `brand/brand.json`. Sweep every baked clay/teal colour literal and the `'trustpager'` colour-role name out. Strip the TrustPager product trees entirely. Source repo (`Remotion-VideoStudio`, "RVS") is READ-ONLY — we copy + transform into BOS, never modify RVS.

**Tech Stack:** Remotion + `@remotion/media` + `@remotion/transitions/shapes/paths/noise/motion-blur`, `lucide-react` (icons), Vite/Remotion Studio, TypeScript. `--gl=swangle` default. Node on Windows.

**Source paths:** RVS = `../Remotion-VideoStudio` (sibling repo). BOS = this repo root.

**Spec:** [2026-07-09-content-creation-studio-design.md](2026-07-09-content-creation-studio-design.md) (§3 architecture, §4 manifest, §8 operating manual). Ruling: founder-decisions.md **D14**.

**Leak-check grep (the Phase-1 definition of done)** — run from `studio/motion/src`, must return zero hits:
```
rg -n -i "c96442|29c6c6|47a3d9|rgba?\(\s*201[,\s]|rgba?\(\s*41,\s*198|rgba?\(\s*71,\s*163|hsl\(\s*15[,\s]\s*63|hsl\(\s*174[,\s]\s*64|trustpager|@tp/|@claude/|TRUSTPAGER_STAGES|professional-services|Plus Jakarta Sans|Coastal Consulting|Sarah Chen|\bEvie\b|Jessica|Jimbo|ai_generate_speech" .
```

---

### Task 0: Governance — log the ruling (DONE 2026-07-09)

- [x] `founder-decisions.md` D14 added; `2026-07-05-youtube-studio-design.md` Decision 8 labelled-revised; spec §2 reframed. No code.

---

### Task 1: Scaffold `studio/motion` and prove a render on this machine (environment de-risk)

**Files:**
- Create: `studio/motion/package.json`, `remotion.config.ts`, `tsconfig.json`, `src/index.ts`, `src/Root.tsx`, `src/brand.js`, `src/compositions/Scaffold.tsx`, `.gitignore`
- Reference: `studio/social/src/brand.js` (the loader to copy), `studio/video/CLAUDE.md` §5 (ffmpeg resolver pattern)

- [ ] **Step 1: Write `package.json`** with `remotion`, `@remotion/cli`, `@remotion/media`, `@remotion/transitions`, `@remotion/shapes`, `@remotion/paths`, `@remotion/noise`, `@remotion/motion-blur`, `@remotion/install-whisper-cpp`, `ffmpeg-static`, `lucide-react`, `react`, `react-dom`, `typescript`. Scripts: `studio` (`remotion studio src/index.ts`), `render`, `still`. `node_modules/` + `output/` gitignored.
- [ ] **Step 2: Write `remotion.config.ts`** — `Config.setChromiumOpenGlRenderer('swangle')`, `Config.setConcurrency(2)` (conservative for owner laptops), H.264 default. Comment: `angle` is an opt-in speed lever only.
- [ ] **Step 3: Write `src/index.ts`** — `registerRoot(RemotionRoot)`. (Absence = black screen.)
- [ ] **Step 4: Write `src/brand.js`** — copy `studio/social/src/brand.js` verbatim (`import brand from '../../../brand/brand.json'`), re-export tokens.
- [ ] **Step 5: Write `src/compositions/Scaffold.tsx`** — a trivial composition (brand-coloured `<AbsoluteFill>` + centered brand `NAME`, one `spring()` fade) reading `brand.js`. `src/Root.tsx` registers ONLY `Scaffold` (1920×1080, 30fps, 90 frames).
- [ ] **Step 6: Install + first render (the real gate).** Run `cd studio/motion && npm install` (expect Remotion to fetch headless Chrome ~150MB on first render). Then `npx remotion still src/index.ts Scaffold output/scaffold.png --gl=swangle`. **Expected:** a PNG in `output/` showing the neutral slate brand colour + business name. READ the PNG. If the machine glitches/reboots (documented GPU risk), stop and check the graphics driver.
- [ ] **Step 7: Commit.** `git add studio/motion` (excluding gitignored) → `git commit -m "feat(motion-studio): scaffold Remotion studio + first brand-driven render"`.

---

### Task 2: `tokens.ts` brand bridge + font loader

**Files:**
- Create: `studio/motion/src/tokens.ts`, `src/fonts.ts`
- Modify: `src/compositions/Scaffold.tsx` (read from `tokens.ts`)

- [ ] **Step 1: Write `tokens.ts`** — import from `brand.js`; export the token names the RVS components will need, mapped from `brand.colors.*` (e.g. `primary`, `accent`, `text`, `panel`, `border`, `bg`, plus role aliases `app`/`assistant` → `primary`/`accent`). **Also export `colors`, `fonts`, and `shadows` objects matching the shape RVS's `@claude/theme` exposes** — 5 KEEP compositor files import `{colors, fonts, shadows}` from it, so the Task 4 rewire becomes a one-line import swap. No hex literals; every value traces to `brand.json`.
- [ ] **Step 2: Write `fonts.ts`** — resolve the render font: if `brand.fonts.primary` is a system stack (default), use it as a CSS `fontFamily` (no load needed); if a Google family is named, `loadFont()` via `@remotion/google-fonts`; else fall back to the CSS stack. Export `FONT_BODY`, `FONT_SERIF`, `FONT_MONO`. Document the family map inline.
- [ ] **Step 3: Point `Scaffold.tsx` at `tokens.ts` + `fonts.ts`** (no inline hex/font).
- [ ] **Step 4: Verify.** Re-render the still; confirm identical output on the neutral brand. Temporarily edit `brand/brand.json` `colors.primary` to `#7c3aed`, re-render, confirm the scaffold recolours, then revert `brand.json`.
- [ ] **Step 5: Commit** — `feat(motion-studio): brand + font bridge (tokens.ts) driven by brand.json`.

---

### Task 3: Extract the generic `@tp/components/ui/*` primitives into a local kit

**Files:**
- Create: `studio/motion/src/ui/*` (the extracted shadcn-style primitives + their internal `cn()`/`lib` helper), `src/icons.tsx`
- Modify: `tsconfig.json` (add `@ui/*` path, no `@tp/*`)

- [ ] **Step 1: Enumerate** the `@tp/components/ui/*` set actually needed downstream (from spec §4.3: `card`, `badge`, `avatar`, `date-badge`, `clean-button`, `input`, `select`, `dialog`, `switch`, `category-tag`, `PageHeader`, `DataTable`, `stat-card`, `gradient-tabs`) by grepping which KEEP files import them. Copy only those + their internal `cn()` util from RVS `TrustPager-src/`.
- [ ] **Step 2: Tokenise** — replace any hardcoded colour in the copied `ui/*` with `tokens.ts` values; remove `@tp/theme` imports.
- [ ] **Step 3: Write `icons.tsx`** — re-export the icons used (map former `@tp/icons` names to `lucide-react`). No `@tp/icons` anywhere.
- [ ] **Step 4: tsconfig** — add `"@ui/*": ["ui/*"]`; confirm NO `@tp/*` alias exists.
- [ ] **Step 5: Verify** — `npx tsc --noEmit` builds; `rg "@tp/" src` returns zero.
- [ ] **Step 6: Commit** — `feat(motion-studio): extract brand-neutral ui kit + lucide icons`.

---

### Task 4: Port the compositor primitives (the motion engine) + colour sweep

**Files:**
- Create: `studio/motion/src/compositor/*` (CursorClick, ClickPulseRing, CursorHover, CursorPath, AutomationBuildSequence, AutomationLightningStrike, ConnectorLine, CrossHighlight, PictureInPicture, Callout, PipelineRewireGlow, NoAutomationsCard, DebugOverlay, animations.ts, composition-helpers.tsx, ActOffsetWrapper, index.ts). **EXCLUDE `ComposerOverlay`** — it imports the Phase-5 `@claude` Composer; defer to Phase 5.

- [ ] **Step 1: Copy** the compositor files from RVS; DROP `trustpager-positions.ts` and its re-exports from `index.ts`.
- [ ] **Step 2: Colour sweep** — replace every baked `#c96442`/clay and `#29c6c6`/teal default with a `tokens.ts` value; make colour a prop where it already is, defaulting to a token.
- [ ] **Step 3: Semantic rename** — `ClickPulseRing`'s `ClickPulseColor` type and `CLICK_COLORS` map: rename `'trustpager'`/`'claude'` roles to `'primary'`/`'assistant'` (or `app`/`assistant`); rewrite the convention comment. Fan out the rename to callers as they are ported.
- [ ] **Step 4: Verify** — `npx tsc --noEmit`; run the leak-check grep over `src/compositor` (zero hits); render a still of `Scaffold` extended to drop in a `CursorClick` + `ConnectorLine` on the brand accent; READ the PNG (ring/line render in brand colour).
- [ ] **Step 5: Commit** — `feat(motion-studio): port compositor primitives, sweep TrustPager colours`.

---

### Task 5: Port overlays (canonical Annotations) + PersistentProgressPanel

**Files:**
- Create: `studio/motion/src/overlays/Annotations.tsx` (canonical), `src/overlays/PersistentProgressPanel.tsx`

- [ ] **Step 1: Port** `overlays/Annotations` as the canonical annotation source; strip its teal→blue gradient + `Plus Jakarta Sans`, drive colour/type from `tokens.ts`/`fonts.ts`. Fold any unique renderers from `Claude-src/overlays/Annotations` + top-level `annotations/`; do not port their per-screen `ELEMENT_POSITIONS`.
- [ ] **Step 2: Port** `PersistentProgressPanel` (inherits accent token).
- [ ] **Step 3: Verify** — tsc builds; leak grep clean over `src/overlays`; render a still with a headline annotation on brand.
- [ ] **Step 4: Commit** — `feat(motion-studio): port annotation + progress overlays, brand-driven`.

---

### Task 6: Port ClickIndicator + primitives (drop product-nav imports)

**Files:**
- Create: `studio/motion/src/scenes/shared/ClickIndicator.tsx`, `src/primitives/*`

- [ ] **Step 1: Port** `scenes/shared/ClickIndicator.tsx` (`ClickTarget` + `TutorialCaption`); rename its `'teal'` role; confirm `resolvePalette()` reads tokens.
- [ ] **Step 2: Port** `primitives/` (Avatar, Button, Tag, DateBadge) pointing at the local `@ui/*` (Task 3), and **drop** the `@tp/components/navigation/{UserProfileMenu,ServiceRequestButton}` imports (product chrome, not needed).
- [ ] **Step 3: Verify** — tsc builds; `rg "@tp/|navigation/UserProfileMenu" src` zero; leak grep clean.
- [ ] **Step 4: Commit** — `feat(motion-studio): port ClickIndicator + brand-neutral primitives`.

---

### Task 7: Hardcoded scaffold composition + full leak audit (Phase-1 DoD)

**Files:**
- Modify: `src/compositions/Scaffold.tsx` (upgrade to exercise the ported kit), `src/Root.tsx`
- Create: `src/data/starter-cast.json` (neutral fictional roster)

- [ ] **Step 1: Build a hardcoded scaffold** that uses a handful of ported pieces (a title annotation, a `ConnectorLine`, a `CursorClick`, a `PersistentProgressPanel` ticking two tasks) on the owner's brand — NOT `.scenes.json`-driven (that is Phase 2). Ship `starter-cast.json` (neutral names) for any component needing a person.
- [ ] **Step 2: Render** a 1080p still at 3 frames + a short draft MP4 (`npx remotion render ... --gl=swangle`). READ the outputs.
- [ ] **Step 3: FULL leak audit** — run the leak-check grep over ALL of `studio/motion/src` and over `public/`. **Zero hits is the definition of done.** Also `rg "@claude/" src` (should be gone or aliased).
- [ ] **Step 4: Recolour proof** — flip `brand/brand.json` to a vivid test palette, re-render, confirm the whole scaffold reskins; revert.
- [ ] **Step 5: Commit** — `feat(motion-studio): brand-driven scaffold composition + zero-leak audit`.

---

### Task 8: `sync-brand.py` discovery + `preflight.js` (owner-hardware gate)

**Files:**
- Create: `studio/motion/scripts/preflight.js`
- Verify: `tools/sync-brand.py` auto-discovers `studio/motion/public/`

- [ ] **Step 1: Confirm** `tools/sync-brand.py` pushes `logo.png` + favicons into `studio/motion/public/` (it auto-discovers `studio/*/public`; if not, note the one-line include — do NOT rewrite it).
- [ ] **Step 2: Write `preflight.js`** — verify Node, `npm install` state, trigger Remotion's browser fetch with progress, validate `swangle` works, do a 2-second test render, report pass/fail in plain English + expected render-time note. (Whisper gate is Phase 3.)
- [ ] **Step 3: Verify** — run `node scripts/preflight.js` on this machine; expect a clear pass.
- [ ] **Step 4: Commit** — `feat(motion-studio): preflight env check + brand-sync discovery`.

---

### Task 9: Scrubbed operating manual + README

**Files:**
- Create: `studio/motion/CLAUDE.md`, `studio/motion/README.md`, `docs/content-creation-studio/hub.md`

- [ ] **Step 1: Write `studio/motion/CLAUDE.md`** from spec §8 PORT list (storyboard-is-spec, per-beat VO, visualise-don't-transcribe, captions-are-data, never-eyeball-clicks, watch-it-get-built, reuse-first, the genericised Windows/GPU render-survival section, `--gl=swangle` default). Include NONE of the §8 DROP scar tissue.
- [ ] **Step 2: Write `README.md`** (human design guide, sibling-studio pattern) and `docs/content-creation-studio/hub.md` (the umbrella: what the hub is, that video is module one, how a module is added).
- [ ] **Step 3: Verify** — grep the CLAUDE.md for scar-tissue terms (NVIDIA, `C:\\Users`, TrustPager, ports 3210/3310) → zero; confirm the swangle + browser-console-check rules are present.
- [ ] **Step 4: Commit** — `docs(motion-studio): scrubbed operating manual + hub doc`.

---

### Task 10: Review + Phase-1 close

- [ ] **Step 1: Self-review** the full `studio/motion` diff for leftover leaks, hardcoded hex, and spec drift.
- [ ] **Step 2: Run** superpowers:requesting-code-review (code-reviewer agent) against this plan + the spec.
- [ ] **Step 3: Fix** anything flagged; re-run the leak audit.
- [ ] **Step 4: Report** Phase-1 status to the founder: what renders, the zero-leak proof, and readiness for Phase 2 (which needs the founding scene styles — an open founder call).

---

## Execution notes
- **Sequential, with checkpoints.** Tasks 1→7 build on each other (little parallelism); do NOT batch untested changes (founder working-style rule). One task, render/grep verify, commit, next.
- **Task 1 is the environment gate** — it front-loads the documented Remotion-on-Windows GPU/first-render risk. If it cannot render cleanly here, stop and resolve before porting.
- **RVS is read-only.** Every file is copied into BOS and transformed; RVS is never edited.
- **Deferred to later phases:** the Claude-chat kit + its ~48-literal sweep (Phase 5), `design-my-scenes`/`.scenes.json` + the scene library (Phase 2), `ingest.js`/whisper/`Overlay.tsx` (Phase 3), the voice rung (Phase 4).

# YouTube Studio Phase 1 (Keyless Floor) Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the keyless YouTube factory floor — four new skills (`research-my-channel`, `plan-my-youtube`, `script-my-video`, `package-my-video`), a genericised `make-thumbnail`, a fifth render studio (`studio/video`), two knowledge files, and an optional `yt-dlp` local-driver blueprint — so an owner with zero accounts goes research → plan → script → branded text-on-screen video → thumbnail → publish-ready folder, entirely keyless and green under `BOS_OFFLINE`.

**Architecture:** The script is the spec. `script-my-video` writes one machine-renderable `<slug>.script.json` (beat-structured), and every downstream surface reads it: `studio/video` renders the beats' `on_screen` text as branded motion graphics (frame-capture, the motion generalisation of the four still studios), `make-thumbnail` reads the packaging concept, `package-my-video` reads packaging + timing for the publish folder. Nothing here connects an account; the later connected rungs (Phases 2-4, out of scope) re-render the same script at higher fidelity.

**Tech Stack:** Python (skill frontmatter/manifest/registry tooling, unittest offline suite), Node/Vite + React + Puppeteer + `ffmpeg-static` (the `studio/video` render surface, copying the `studio/social` pattern exactly), root `brand/brand.json` (identity), Firecrawl via delegation to the research skills (channel research), optional `yt-dlp` local CLI (transcript/comment deepener).

**Spec:** docs/architecture/2026-07-05-youtube-studio-design.md (approved 2026-07-05)

---

## Source-of-truth note on altitude

The spec (§2, §3, §5) and the two new method files (Task 1.7) own the *content* — the beat schema, the timing contract, the packaging/script craft. This plan owns the *mechanics* — exact files, frontmatter blocks, commands, tests, gates. Where a task says "author per the method file," the executor writes the prose/components against the spec + method file, not against inlined-here copy. Where a task reproduces a contract (the beat schema, the `<slug>.timing.json` shape, the frame-drive interface), that reproduction is load-bearing and complete so an implementer never needs the spec open to avoid drift — the spec §3 remains the one owner, cited at each site.

## Validation doctrine (from the codebase)

Reasoning-heavy skills (`research-my-channel`, `plan-my-youtube`, `script-my-video`, `package-my-video`, genericised `make-thumbnail`) are validated by a scripted **Sonnet dogfood** (the pass bar), exactly as `get-found-online` and `design-my-site` were — plus per-task offline fixture checks where a schema or an artifact can be asserted. The one code artifact (`studio/video`) gets a real offline smoke render. Every task ends by running its stated gate; Task 1.8 runs the full CI-order block.

## CI-order gates (run after Task 1.8; all must pass)

```bash
BOS_OFFLINE=1 python tools/check-no-secrets.py
BOS_OFFLINE=1 python tools/check-kernel-clean.py
BOS_OFFLINE=1 python tools/check-doctrine-voice.py
BOS_OFFLINE=1 python tools/check-connectors.py            # yt-dlp (kind: local) resolves; no activation paths
BOS_OFFLINE=1 python tools/check-onboarding-binding.py    # floor skills are keyless-clean, not needs_connection
BOS_OFFLINE=1 python tools/check-surface-budget.py        # every description <= 400 chars
BOS_OFFLINE=1 python tools/registry-generator.py --check
BOS_OFFLINE=1 python tools/export-capabilities.py --check
for d in skills/research-my-channel skills/plan-my-youtube skills/script-my-video skills/package-my-video skills/make-thumbnail; do python tools/lint-skill.py "$d"; done
BOS_OFFLINE=1 python -m unittest discover -s tests -v
```

(Invocation note, settled in code: `tools/manifest.py` takes exactly one PATH argument — its `__main__` block exits 2 with usage when run bare. CI never calls it directly; manifests are validated tree-wide via `registry-generator.py --check`, `export-capabilities.py --check`, and `lint-skill.py`, all of which import the shared `validate_manifest`. Per-task, check a single skill with `python tools/manifest.py skills/<name>/SKILL.md`.)

---

## File map (lock decomposition before tasks)

**New skills (`skills/`):**
- `skills/script-my-video/SKILL.md` — the load-bearing beat-script skill; emits `<slug>.script.json` (§3 schema) + `<slug>.script.md`. Owns the beat contract's *author* half. (Task 1.1)
- `skills/research-my-channel/SKILL.md` — Firecrawl-delegated channel/competitor/comment research → `youtube-research.md`; names the optional `yt-dlp` deepener. (Task 1.2)
- `skills/plan-my-youtube/SKILL.md` — composes `build-social-strategy` + `plan-my-content`; channel strategy + video pipeline with the four packaging fields per video. (Task 1.3)
- `skills/package-my-video/SKILL.md` — extends `assemble-content-pack`; one publish-ready folder; consumes `<slug>.timing.json` (or planned `duration_s` fallback) for chapters. (Task 1.6)

**New studio (`studio/video/`):** (Task 1.4)
- `studio/video/package.json` — `dev`/`shoot`/`render` scripts, `puppeteer` + `ffmpeg-static` deps (mirrors `studio/social/package.json`).
- `studio/video/vite.config.js` — dev server on **port 3218** (thumbnails 3210, cta 3213, social 3216, og 3217 are taken; site-starter uses 3220).
- `studio/video/index.html` — Vite entry.
- `studio/video/src/main.jsx` — React entry.
- `studio/video/src/brand.js` — identical single-root `../../../brand/brand.json` import (clone of `studio/social/src/brand.js`).
- `studio/video/src/App.jsx` — studio preview UI (sidebar + frame scrubber).
- `studio/video/src/templates/index.js` — template registry.
- `studio/video/src/templates/VideoBeats.jsx` — THE template: renders a `<slug>.script.json`'s beats as branded text-on-screen motion graphics, reading `?frame=N`.
- `studio/video/src/data/` — a committed fixture `<slug>.script.json` for the smoke render.
- `studio/video/scripts/render.js` — Puppeteer frame-capture (`0..duration*fps`) + `ffmpeg-static` stitch to MP4/GIF; writes `<slug>.timing.json`; adds a silent stereo audio track.
- `studio/video/scripts/shoot.js` — `npm run shoot` wrapper (clone of `studio/social/scripts/shoot.js`).
- `studio/video/scripts/_filename.js` — output naming helper.
- `studio/video/.gitignore` — `output/`, `node_modules/`.
- `studio/video/CLAUDE.md` + `studio/video/README.md` — the four-studios doc pattern.
- `studio/video/output/` — rendered MP4/GIF (gitignored).

**New knowledge files (`knowledge/`):** (Task 1.7)
- `knowledge/youtube-packaging-method.md` — outlier analysis, angle/title/thumbnail differentiation, franchise thinking.
- `knowledge/youtube-script-method.md` — hook patterns, retention structure, per-beat discipline, the wpm default rationale.

**New driver blueprint (`drivers/`):** (Task 1.2)
- `drivers/yt-dlp/__init__.py` — documentation-only `local`-kind `DRIVER` dict (no transport, no `never_call`/`never_set`). See the yt-dlp scope note below.
- `drivers/yt-dlp/README.md` — what it is, the honest Firecrawl-vs-yt-dlp boundary, how the skill offers it.

**Existing files modified:**
- `skills/make-thumbnail/SKILL.md` — genericised to the owner's brand + non-tutorial titles (Decision 9). (Task 1.5)
- `studio/thumbnails/*` — the TrustPager-tutorial framing flipped to owner-brand (Task 1.5): `studio/thumbnails/YOUTUBE_TITLES.md`, `studio/thumbnails/src/templates/YouTubeThumbnail.jsx` (JSDoc), `studio/thumbnails/CLAUDE.md`. Flip only the TrustPager-specific hard-rules and the tutorial-hero assumption; keep the distilled craft.
- `kernel/registry.json` — regenerated by `tools/registry-generator.py` (never hand-edited). (Task 1.8)
- `docs/CAPABILITIES.md` — regenerated by `tools/export-capabilities.py`. (Task 1.8)
- `knowledge/starter-projects.md` — new 🎨 market-group rows for the keyless factory; Phase-2+ rungs are `needs_connection` doorways only, NOT added to the cold pool. (Task 1.8)

**New artifacts the add-on produces (owner's working dir — never committed):** `youtube-research.md`, `<slug>.script.json`, `<slug>.script.md`, `<slug>.timing.json`, the rendered MP4/GIF, the thumbnail PNG, the `package-my-video` folder.

**Do NOT touch:** `skills/whats-possible/SKILL.md` (runtime registry reader), `kernel/*` (Phase 1 adds skills + one studio + knowledge only — no kernel edit, per spec §7), `kernel/registry.json` by hand, the `Remotion-VideoStudio` repo (the workspace hard-rule reserves the Remotion render engine for it; `studio/video` uses Puppeteer frame-capture, not Remotion — spec Decision 4/8).

---

## The two review pins (the spec reviewer left these to the plan)

**Pin 1 — the exact `<slug>.timing.json` shape.** Task 1.4's `render.js` writes it; Task 1.6's `package-my-video` reads it. Both tasks cite this exact shape (spec §3 timing contract is the owner):

```json
{
  "slug": "quote-in-60-seconds",
  "fps": 30,
  "beats": [
    { "id": "hook",    "start_s": 0.0,  "end_s": 5.2 },
    { "id": "promise", "start_s": 5.2,  "end_s": 11.0 },
    { "id": "point-1", "start_s": 11.0, "end_s": 28.4 },
    { "id": "cta",     "start_s": 68.0, "end_s": 75.0 }
  ]
}
```

Keyed by beat `id`; `start_s`/`end_s` are seconds as floats; `beats` is an array in render order. These are the *actual* rendered per-beat times (not the script's planned `duration_s`). `package-my-video` maps `start_s` → chapter timestamps when this file is present, and falls back to the script's per-beat `duration_s` cumulative sum otherwise.

**Pin 2 — yt-dlp ships neither `connect.md` nor a `connectors.md` card.** Spec §8's "each with `connect.md` + `connectors.md` card" applies to **Phase 2+ connected drivers only** (voice/music/image/avatar `keyed_cli`, `youtube` `claude_mcp`). `yt-dlp` is `kind: local`, keyless, no account — so it ships **only** `drivers/yt-dlp/__init__.py` (the `DRIVER` dict) + `drivers/yt-dlp/README.md`, and **no `connect.md`, no `connectors.md` card**. `tools/check-connectors.py` requires those two only for `CONNECTED_KINDS = {claude_mcp, keyed_cli}` (confirmed at `tools/check-connectors.py` lines 130, 370-392); a `local`-kind driver passes conformance with a valid `kind` + a resolving `requires_driver`, nothing more. Task 1.2 states this explicitly so no implementer adds a spurious connect card.

---

## Dependency graph + parallelization

```
1.1  script-my-video (the beat schema — LOAD-BEARING, lands first)
        │
        ├──────────────┬───────────────┬─────────────────┐
        ▼              ▼               ▼                 ▼
1.2 research-my-    1.3 plan-my-    1.4 studio/video  1.5 make-thumbnail
    channel(+yt-dlp)    youtube        (reads schema)     (genericise)
        │              │               │                 │
        └──────────────┴───────┬───────┴─────────────────┘
                               ▼
                        1.6 package-my-video (reads timing.json from 1.4 + packaging)
                               │
                        1.7 knowledge files (siblings; can start any time, needed by 1.2/1.3/1.5/1.6 as link targets)
                               ▼
                        1.8 wiring / registry / surfaces / gates (needs ALL skills present)
                               ▼
                        1.9 Sonnet dogfood (THE MERGE GATE — everything green first)
```

- **Sequential-first:** Task 1.1 lands the beat schema before anything reads it. Task 1.8 needs every skill present. Task 1.9 is last.
- **Safe to run in PARALLEL worktrees after 1.1:** 1.2, 1.3, 1.4, 1.5, and 1.7 touch disjoint file sets (four separate skill folders, one studio folder, `studio/thumbnails/*`, two knowledge files) with no shared edits. **1.7 (knowledge files) is fully independent** and can start immediately, but 1.2/1.3/1.5/1.6 link to it, so land 1.7 before their link-checks run (or land 1.7 first).
- **1.6 depends on 1.4** (it reads `<slug>.timing.json` shape) and on the packaging fields from 1.3 — run it after both.
- **1.8 is a merge/regen step** — run it once all skill folders and the studio exist, in a single worktree (it regenerates `kernel/registry.json` + `docs/CAPABILITIES.md`, which cannot be merged in parallel).

---

## Description-writing rule for the four new skills

Every new skill `description` is warm, plain, outcome-led, carries trigger vocabulary (the phrases an owner would say), has **no em dashes**, and is **≤400 chars** (aim well under — `tools/check-surface-budget.py` fails over 400). Positive-only framing. State what it does and when to use it; cut benefit-marketing prose. The frontmatter blocks below are copy-ready.

---

## Task 1.1 — The script schema + `script-my-video` skill (LOAD-BEARING, first)

**Files:**
- Create: `skills/script-my-video/SKILL.md`
- Test: an offline fixture check (Step 4) — no committed test file needed unless a schema-validator helper is written; if one is, add `tests/test_script_schema.py`.

**The beat schema this skill emits** (spec §3 is the owner — reproduced here so the implementer never drifts). `<slug>.script.json`:

```jsonc
{
  "slug": "quote-in-60-seconds",
  "working_title": "How I Quote a Job in Under a Minute",
  "packaging": { "title_options": [ "..." ], "thumbnail_concept": "...", "angle": "..." },
  "meta": { "duration_target_s": 75, "aspect": "16:9", "hook_window_s": 5 },
  "beats": [
    {
      "id": "hook",
      "role": "hook",          // one of: hook | promise | point | reset | proof | cta
      "spoken": "…",           // the owner's-voice line (drives VO on Phase 2)
      "on_screen": "…",        // the text/graphic callout (drives studio/video)
      "b_roll": "…",           // visual note (owner's own footage / stock guidance)
      "evidence_ref": "…",     // optional: a customer-voice quote id the claim rests on
      "duration_s": 6          // optional: PLANNED duration, estimated from spoken
                               // word-count at a stated words-per-minute default
    }
    // …promise, retention resets, points, proof, CTA
  ]
}
```

The timing contract's *author half* lives here: `script-my-video` fills each beat's optional `duration_s` from spoken-word count × a stated wpm default (the skill body states the wpm it used). `studio/video` writes the *actual* `<slug>.timing.json` after render (Task 1.4, Pin 1); `package-my-video` prefers actual, falls back to planned (Task 1.6). Cite spec §3.

**Frontmatter (copy exactly — spec §5 Task 1.1):**
```yaml
---
name: Script My Video
description: Turn a topic into a beat-by-beat video script in your own voice, written so it can be filmed and rendered straight away. Covers the hook, the promise, the points, and a clear call to action. Every claim rests on real evidence, never invented. Writes a script file your studio and thumbnail both read. No accounts needed.
triggers:
  - script my video
  - write a video script
  - script a youtube video
  - write my youtube script
  - turn this into a video script
function_slot: creative
requires_driver: none
requires_credential: none
data_path: local
status: active
---
```
(Well under the 400 cap. No em dashes.)

- [ ] **Step 1: Write the gate-led body** (numbered gates before defaults, for Sonnet — see memory `bos-target-model-is-sonnet`), against spec §5 Task 1.1 and referencing `knowledge/youtube-script-method.md` (Task 1.7) throughout so the body stays lean:
  - *Read silently:* Source A `brand/brand.json` (name, voice, tagline); Source B `./CLAUDE.md` (business shape, offer, region only if a `Region:` line is explicitly set). Consume `youtube-research.md` + the `plan-my-youtube` pipeline row **if present**.
  - *Interview (the video-specific bucket only):* topic, the one action the video drives, target length, aspect.
  - *Emit* `<slug>.script.json` (the schema above) + a human-readable `<slug>.script.md` (teleprompter/shot-list view).
  - *Fill* each beat's `duration_s` from spoken word-count at a stated wpm default; state the wpm in the body.
  - *Anchor* claims in customer-voice evidence via `evidence_ref` where a `build-customer-voice` synthesis exists; never fabricate quotes, numbers, or testimonials.
  - **Hard rules block:** keyless (no `mcp__*` token anywhere in the body), positive-only + no em dashes in owner-facing copy (script CTAs, titles), hook inside the target window, never fabricate evidence.
- [ ] **Step 2: Lint.**
  ```bash
  python tools/lint-skill.py skills/script-my-video
  ```
  Expected: exit 0 (no `[FAIL]`; a triggers-count WARN is acceptable — 5 triggers).
- [ ] **Step 3: Validate frontmatter.**
  ```bash
  python tools/manifest.py skills/script-my-video/SKILL.md
  ```
  Expected: OK; the new manifest validates (`function_slot: creative`, `requires_credential: none`, `data_path: local`).
- [ ] **Step 4: Offline schema fixture check.** Feed the skill a saved topic payload (a small committed fixture, e.g. `skills/script-my-video/test-fixture.json`) and confirm the produced JSON conforms: all required beat roles reachable (`hook`, `promise`, `point`, `cta` at minimum), `meta.hook_window_s` respected, `beats` a non-empty array, each beat carrying `id`/`role`/`spoken`/`on_screen`. No network. If a validator helper is written, add `tests/test_script_schema.py` (TDD: failing test → run → implement → run → commit).
- [ ] **Step 5: Commit.**
  ```bash
  git add skills/script-my-video/SKILL.md
  git commit -m "feat(youtube-studio): script-my-video skill + the load-bearing beat schema (script is the spec)"
  ```

**Merge gate (spec §5 Task 1.1 DoD):** a topic + brand → a valid `<slug>.script.json` conforming to the schema, positive-only, no em dashes in owner-facing copy, hook inside the target window. Test gate: offline fixture (topic → schema-valid JSON, all required beat roles present); `lint-skill.py` clean; no network.

---

## Task 1.2 — `research-my-channel` skill (+ the `yt-dlp` local-driver blueprint)

Runs in parallel with 1.3/1.4/1.5 after 1.1.

**Files:**
- Create: `skills/research-my-channel/SKILL.md`
- Create: `drivers/yt-dlp/__init__.py`
- Create: `drivers/yt-dlp/README.md`

**The yt-dlp driver scope note (Pin 2 — read before writing the driver):** `yt-dlp` is `kind: local`, keyless, no account. It ships **only** the `DRIVER` dict + `README.md`. It ships **NO `connect.md` and NO `connectors.md` card** — those are required by `check-connectors.py` for connected kinds (`claude_mcp`, `keyed_cli`) only, and a `local` driver passes conformance with a valid `kind` and a resolving `requires_driver` alone. Do not add a connect card. (Phase 2+ connected drivers get connect.md + a card; those are out of scope here.)

**The `DRIVER` dict (copy exactly — documentation-only, `local` kind, no transport, no `never_call`/`never_set`):**
```python
# drivers/yt-dlp/__init__.py
"""yt-dlp driver — an OPTIONAL keyless local-CLI deepener for research-my-channel.

DOCUMENTATION ONLY. No BOS mechanism imports or reads this module; there is no
driver-metadata loader. The load-bearing artifacts are the DRIVER dict (so
check-connectors.py validates the kind) and this file + README.md documenting the
honest Firecrawl-vs-yt-dlp boundary. It is NOT a connected driver: kind is
``local`` (a local binary, no account, keyless), so it ships neither connect.md nor
a connectors.md card, and it carries no ``never_call``/``never_set`` (a read-only
scrape has no irreversible/live action). It stays on the keyless floor.
"""

DRIVER = {
    "id": "yt-dlp",
    "kind": "local",                 # keyed_rest | keyed_cli | keyless_mcp | local | data_pack | claude_mcp
    "display_name": "yt-dlp",
    "cli": "yt-dlp",                 # the local CLI invoked via Bash; keyless, no account
    "connect_doc": None,             # local driver: no connect flow, no connect.md
    "credential": "none",            # keyless local binary
    "read_only_scope_first": True,   # read-only scrape; never a write
}
```
(Note: `local` kind is not in `CONNECTED_KINDS`, so `check-connectors.py` does not require `connect.md`/card; `research-my-channel` carries `requires_driver: none`, so its manifest is not mechanically linked to this driver — the driver blueprint exists as an offered deepener the skill body names, not a hard dependency. This keeps the manifest keyless-clean.)

**Frontmatter for the skill (copy exactly — spec §5 Task 1.2):**
```yaml
---
name: Research My Channel
description: Study your niche on YouTube and come back with video ideas that will actually land: what the top channels cover, what viewers keep asking for in the comments, and the angles nobody is taking yet. Every idea backed by what real viewers said, in their own words. No accounts needed.
triggers:
  - research my channel
  - research my youtube niche
  - what videos should i make
  - find video ideas
  - what is my competition doing on youtube
function_slot: research
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---
```
(`research` is a confirmed valid `FUNCTION_SLOTS` value in `tools/manifest.py`. Description well under the 400 cap; no em dashes.)

- [ ] **Step 1: Write the driver blueprint** `drivers/yt-dlp/__init__.py` (the dict above) + `drivers/yt-dlp/README.md` carrying the honest boundary from spec Decision 5: Firecrawl alone suffices for channel/video *surface* facts (titles, descriptions, view counts, cadence, visible top comments — the packaging signal); `yt-dlp` is worth its local-binary install only for deep transcript analysis or exhaustive comment mining. Default to Firecrawl; offer `yt-dlp` as "want me to go deeper?", never a prerequisite.
- [ ] **Step 2: Write the skill body** against spec §5 Task 1.2, referencing `knowledge/youtube-packaging-method.md` (Task 1.7). Firecrawl-powered by default, **delegating** to the research skills / keyless hosted Firecrawl read, scope-clamped per `knowledge/research-method.md` (no crawl/map/agent/extract). Do NOT name an `mcp__*` / firecrawl tool in the body (keeps the manifest clean). Three outputs into `youtube-research.md`: (a) competitor content scan (topics, formats, cadence, outliers vs the channel baseline); (b) comment mining (questions, "nobody explains X" gaps, each an idea WITH verbatim audience evidence); (c) novel-packaging gap-and-angle map (identically-packaged topics, untaken angles, standout title/thumbnail/franchise concepts). Name the `yt-dlp` deepener as an optional "go deeper?" offer.
  - **Hard rules block:** keyless (no `mcp__*`, no direct firecrawl call), every mined idea carries a verbatim-evidence line, the packaging map cites real observed outliers never invented ones, positive-only + no em dashes.
- [ ] **Step 3: Lint + validate + connector gate.**
  ```bash
  python tools/lint-skill.py skills/research-my-channel
  python tools/manifest.py skills/research-my-channel/SKILL.md
  BOS_OFFLINE=1 python tools/check-connectors.py
  ```
  Expected: lint exit 0; manifest OK; `check-connectors.py` OK (the new `yt-dlp` `DRIVER` dict declares a canonical `kind: local`, requires neither connect.md nor a card, and every `requires_driver` still resolves).
- [ ] **Step 4: Offline research fixture check** (spec §5 Task 1.2 test gate). Feed a saved competitor-page payload; confirm a correct `youtube-research.md` with all three sections, each mined idea carrying verbatim evidence. No live fetch; `BOS_OFFLINE` green.
- [ ] **Step 5: Commit.**
  ```bash
  git add skills/research-my-channel/SKILL.md drivers/yt-dlp/__init__.py drivers/yt-dlp/README.md
  git commit -m "feat(youtube-studio): research-my-channel (Firecrawl floor) + optional yt-dlp local-driver blueprint"
  ```

**Merge gate (spec §5 Task 1.2 DoD):** a niche + channel URL → a `youtube-research.md` with all three sections, every mined idea carrying a verbatim-evidence line, the packaging map citing real observed outliers. Test gate: offline fixture, no live fetch, `BOS_OFFLINE` green, `check-connectors.py` green with `yt-dlp` validated.

---

## Task 1.3 — `plan-my-youtube` skill (composition, no forking)

Runs in parallel with 1.2/1.4/1.5 after 1.1.

**Files:**
- Create: `skills/plan-my-youtube/SKILL.md`

**Frontmatter (copy exactly — spec §5 Task 1.3):**
```yaml
---
name: Plan My YouTube
description: Turn your channel research into a real plan: a clear channel strategy and a pipeline of videos, each with an idea, an angle, a working title, and a thumbnail concept ready to script. Builds on your social strategy and content plan so it all fits together. No accounts needed.
triggers:
  - plan my youtube
  - plan my channel
  - plan my youtube videos
  - build my youtube strategy
  - what should my channel be about
function_slot: strategy
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---
```
(`strategy` is a valid `FUNCTION_SLOTS` value. Description well under the 400 cap; no em dashes. If the executor prefers `creative` to match the family, either is valid; `strategy` fits "channel strategy" best.)

- [ ] **Step 1: Write the skill body** against spec §5 Task 1.3. It **COMPOSES** `build-social-strategy` + `plan-my-content` — delegates to them by reference, never copies or forks their bodies — consuming `youtube-research.md`. Produces channel strategy + a video pipeline: per video an idea → angle → working title → thumbnail concept (the four packaging fields that `script-my-video`'s `packaging` block and `make-thumbnail` both read).
  - **Hard rules block:** keyless, delegation is by-reference (no duplicated strategy logic), positive-only + no em dashes.
- [ ] **Step 2: Lint + validate.**
  ```bash
  python tools/lint-skill.py skills/plan-my-youtube
  python tools/manifest.py skills/plan-my-youtube/SKILL.md
  ```
  Expected: lint exit 0; manifest OK.
- [ ] **Step 3: Composition check** (spec §5 Task 1.3 test gate). Confirm the body **references** (does not restate) `build-social-strategy` + `plan-my-content` — a grep for the two skill ids in the body, and a read confirming no strategy prose is copied wholesale.
  ```bash
  grep -n "build-social-strategy\|plan-my-content" skills/plan-my-youtube/SKILL.md
  ```
- [ ] **Step 4: Commit.**
  ```bash
  git add skills/plan-my-youtube/SKILL.md
  git commit -m "feat(youtube-studio): plan-my-youtube skill (composes build-social-strategy + plan-my-content, no fork)"
  ```

**Merge gate (spec §5 Task 1.3 DoD):** research artifact → a channel strategy + a dated/ordered video pipeline of N videos, each with the four packaging fields; delegation by-reference, no duplicated strategy logic. Test gate: offline; lint clean; the reference check passes.

---

## Task 1.4 — `studio/video` (the fifth studio)

Runs in parallel with 1.2/1.3/1.5 after 1.1. This is the one code artifact; it gets a real offline smoke render.

**Files:** the `studio/video/` tree in the file map above. The SCAFFOLD mirrors `studio/social/` (package.json scripts, `vite.config.js`, `src/brand.js` identical single-root import, `src/main.jsx`, `src/App.jsx`, a template, `scripts/shoot.js` + `scripts/_filename.js`, `.gitignore`, `CLAUDE.md`, `README.md`, a `data/` fixture, `output/` gitignored) — but `scripts/render.js` is **net-new**: social's `render.js` is a still-PNG screenshotter with no motion pipeline to copy, while this one implements the frame loop (`?frame=N`, deterministic `0..duration*fps` stepping per the frame-drive interface below), the `ffmpeg-static` stitch to MP4/GIF, the silent stereo audio track, and the `<slug>.timing.json` writer.

**The frame-drive interface (concrete — spec §5 Task 1.4 + Decision 4 is the owner; reproduced so the implementer never drifts):**
- The video template (`src/templates/VideoBeats.jsx`) reads its frame from a **URL query param `?frame=N`**.
- `render.js` iterates **`0..duration*fps`** (where `duration` = sum of the script's per-beat planned `duration_s`, or `meta.duration_target_s`; `fps` is a studio constant, e.g. 30), loading/setting each frame and capturing it. **Deterministic stepping, never realtime capture** — this is the motion generalisation of the still studios, reusing `studio/thumbnails/src/remotion-shim.jsx`'s "resolve animations at a frame" idea.
- Stitch the captured frames to MP4/GIF with the npm-bundled **`ffmpeg-static`**.
- The floor MP4 carries a **silent stereo audio track** (so the Phase-2 voice rung is a track replacement/remux, not a container change).

**The timing sidecar `<slug>.timing.json` (Pin 1 — the exact shape, cite spec §3):** after render, `render.js` writes the actual rendered per-beat start/end times:
```json
{
  "slug": "quote-in-60-seconds",
  "fps": 30,
  "beats": [
    { "id": "hook",    "start_s": 0.0,  "end_s": 5.2 },
    { "id": "promise", "start_s": 5.2,  "end_s": 11.0 },
    { "id": "cta",     "start_s": 68.0, "end_s": 75.0 }
  ]
}
```
Keyed by beat `id`, seconds as floats, array in render order. `package-my-video` (Task 1.6) reads this exact shape.

**The ffmpeg sub-decision (spec Decision 4 leaves this to implementation — state the decision procedure + fallback contract, not a premature answer):**
- **Decision procedure:** first try committing `ffmpeg-static` as a `studio/video` devDependency and run the repo-hygiene / kernel-clean / no-secrets gates against the new studio folder. If `ffmpeg-static` clears those gates (no tracked binary in `git ls-files`, `node_modules` gitignored, no secret false-positive), keep it — the studio stays fully self-contained and keyless.
- **Fallback contract (required either way):** if `ffmpeg-static` cannot ship (a gate fails, or a binary-in-repo concern), the stitch step shells a **system `ffmpeg`** via Bash, and the studio README + `render.js` MUST carry a **keyless-fallback note**: detect `ffmpeg` on PATH; if absent, emit a clear, positive install pointer and still produce the frame PNGs + `<slug>.timing.json` so the owner is never blocked. The contract is: the render never hard-fails silently, and the keyless path is always documented. Resolve which arm applies at this task's Step 3 gate, mirroring how the site-builder deferred `templates/site-starter` placement to a planning check.

- [ ] **Step 1: Scaffold the tree** by cloning `studio/social/` and adapting: set the dev port to **3218** in `vite.config.js`; `src/brand.js` is an identical copy (the `../../../brand/brand.json` import is unchanged — spec Decision 4 requires it be identical to `studio/social/src/brand.js`); write `VideoBeats.jsx` (reads `?frame=N`, renders the active beat's `on_screen` text on the brand palette, no TrustPager literals); write `render.js` (frame-capture `0..duration*fps` + `ffmpeg-static` stitch + silent stereo track + `<slug>.timing.json` writer); commit a `data/` fixture `<slug>.script.json`. Author `CLAUDE.md` + `README.md` in the four-studios pattern (what it is, the beat-drive interface, the ffmpeg fallback note).
- [ ] **Step 2: Smoke render on the fixture.**
  ```bash
  cd studio/video && npm install && npm run dev &   # dev server on 3218 (background)
  npm run shoot <fixture-slug>
  ```
  Expected: a branded MP4 (silent stereo track present) whose on-screen text matches the fixture beats, colours from `brand/brand.json`, no TrustPager literals, PLUS a `<slug>.timing.json` sidecar with the Pin-1 shape. Runs on the npm-bundled Chromium with no account.
- [ ] **Step 3: Hygiene + gates for the new folder** (resolve the ffmpeg sub-decision here).
  ```bash
  git ls-files | grep 'studio/video/node_modules/' || echo "clean: node_modules not tracked"
  git ls-files | grep 'studio/video/output/'        || echo "clean: output not tracked"
  BOS_OFFLINE=1 python tools/check-no-secrets.py
  BOS_OFFLINE=1 python tools/check-kernel-clean.py
  ```
  Expected: `node_modules`/`output` not tracked; no-secrets passes (no example tokens in tracked files); kernel-clean passes (it scans only `kernel/**/*.py`, so it never inspects `studio/`, but run it to confirm the whole suite stays green). Confirm the ffmpeg arm chosen and that the fallback note is present in the README + `render.js`.
- [ ] **Step 4: Commit** (source only, not `node_modules`/`output`).
  ```bash
  git add studio/video/package.json studio/video/vite.config.js studio/video/index.html studio/video/src studio/video/scripts studio/video/data studio/video/.gitignore studio/video/CLAUDE.md studio/video/README.md
  git commit -m "feat(youtube-studio): studio/video — the fifth studio (frame-capture motion graphics from the beat script)"
  ```

**Merge gate (spec §5 Task 1.4 DoD):** `npm install && npm run shoot <slug>` on a fixture script produces a branded MP4 (silent stereo track) whose on-screen text matches the beats, colours from `brand.json`, no TrustPager literals, plus the `<slug>.timing.json` sidecar; runs on npm-bundled Chromium with no account. Test gate: the studio's own smoke render on the committed fixture; repo-hygiene / kernel-clean gates pass for the new folder (ffmpeg-static sub-decision resolved); `node_modules` + `output` gitignored.

---

## Task 1.5 — genericise `make-thumbnail` (Decision 9)

Runs in parallel with 1.2/1.3/1.4 after 1.1. LABELLED supersession (spec Decision 9) — flag exactly what flips.

**Files:**
- Modify: `skills/make-thumbnail/SKILL.md`
- Modify: `studio/thumbnails/YOUTUBE_TITLES.md`, `studio/thumbnails/src/templates/YouTubeThumbnail.jsx` (JSDoc), `studio/thumbnails/CLAUDE.md` (the TrustPager-tutorial framing sites).

- [ ] **Step 1: Flip the framing** to the owner's brand + non-tutorial titles, taking the packaging concept from `plan-my-youtube`:
  - `skills/make-thumbnail/SKILL.md`: description + body genericised — titles carry the *owner's* brand (from `brand.json`), packaging comes from `plan-my-youtube`'s concept. The vendor-name hard-rule changes from "must say TrustPager, no third-party vendor names" to "the owner's brand, no unintended third-party names" (retain the vendor-name safeguard in generic form). Remove the tutorial-only assumption; keep the "read the three canonical studio files before designing" discipline and the distilled craft.
  - `studio/thumbnails/YOUTUBE_TITLES.md` + `YouTubeThumbnail.jsx` JSDoc + `studio/thumbnails/CLAUDE.md`: flip the TrustPager hard-rules and the tutorial-hero assumption only. Keep `knowledge/youtube-thumbnail-method.md` wholesale (the craft's one home).
  - The `make-thumbnail` frontmatter stays `function_slot: creative`, `requires_driver: render`, `requires_credential: none`, `data_path: local`, `status: active` (unchanged — it is already studio-class keyless). Update only the `description` (keep ≤400 chars, no em dashes, drop the "tutorial" narrowing).
- [ ] **Step 2: Lint + validate + no-new-TrustPager grep** (spec §5 Task 1.5 test gate).
  ```bash
  python tools/lint-skill.py skills/make-thumbnail
  python tools/manifest.py skills/make-thumbnail/SKILL.md
  BOS_OFFLINE=1 python tools/check-doctrine-voice.py
  git diff studio/thumbnails skills/make-thumbnail | grep -i "trustpager" || echo "clean: no new TrustPager literals introduced"
  ```
  Expected: lint exit 0; manifest OK; doctrine-voice clean; the diff shows framing being *removed*, not added (any TrustPager hits in the diff are deletions with a leading `-`).
- [ ] **Step 3: Offline render on an owner-brand fixture.** Confirm a thumbnail for a non-tutorial owner-brand video renders on the owner's palette with no "must say TrustPager" constraint and no unintended third-party vendor names.
- [ ] **Step 4: Commit.**
  ```bash
  git add skills/make-thumbnail/SKILL.md studio/thumbnails/YOUTUBE_TITLES.md studio/thumbnails/src/templates/YouTubeThumbnail.jsx studio/thumbnails/CLAUDE.md
  git commit -m "refine(youtube-studio): genericise make-thumbnail to owner brand + non-tutorial titles (LABELLED, supersedes TrustPager framing)"
  ```

**Merge gate (spec §5 Task 1.5 DoD):** a thumbnail for a non-tutorial owner-brand video renders on the owner's palette with no "must say TrustPager" constraint and no unintended third-party vendor names; the vendor-name safeguard retained in generic form. Test gate: lint clean; an offline render on the owner-brand fixture; a grep showing no new TrustPager literals introduced.

---

## Task 1.6 — `package-my-video` skill

Depends on 1.4 (the `<slug>.timing.json` shape) and the packaging fields from 1.3. Run after both.

**Files:**
- Create: `skills/package-my-video/SKILL.md`

**The timing contract this skill consumes (Pin 1 — cite spec §3):** chapter timestamps follow the timing contract. Consume `<slug>.timing.json` when present (the exact shape from Task 1.4 / Pin 1 — keyed by beat `id`, `start_s`/`end_s` floats, array in render order; map each beat's `start_s` to a chapter timestamp). Fall back to the script's planned per-beat `duration_s` (cumulative sum) otherwise.

**Frontmatter (copy exactly — spec §5 Task 1.6):**
```yaml
---
name: Package My Video
description: Turn your rendered video into one publish-ready folder (the video, the thumbnail, title options, a full description with chapters, tags, and a short upload checklist), so all you do is upload it to YouTube yourself. Everything gathered in one place, ready to go. No accounts needed.
triggers:
  - package my video
  - get my video ready to publish
  - prepare my video for youtube
  - make my youtube description
  - bundle my video for upload
function_slot: creative
requires_driver: none
requires_credential: none
data_path: local
status: active
---
```
(Description well under the 400 cap; no em dashes.)

- [ ] **Step 1: Write the skill body** against spec §5 Task 1.6, extending the `assemble-content-pack` pattern (reference it, do not fork it). Collate one named publish-ready folder: the rendered video, the thumbnail, title options (from `packaging.title_options`), a description with chapters (timing contract above), tags, and a short publish checklist + readme. Manual upload is the honest floor ending (spec: Phase 4 automates it — out of scope here).
  - **Hard rules block:** keyless (`data_path: local`), every owner-facing line positive-only, no em dashes, never fabricate.
- [ ] **Step 2: Lint + validate.**
  ```bash
  python tools/lint-skill.py skills/package-my-video
  python tools/manifest.py skills/package-my-video/SKILL.md
  ```
  Expected: lint exit 0; manifest OK.
- [ ] **Step 3: Offline assembly fixture check** (spec §5 Task 1.6 test gate). From local fixtures (a script + a rendered video + a thumbnail + a `<slug>.timing.json`), confirm the folder assembles with all six artifacts + a short readme, chapters read from `timing.json`, every owner-facing line positive-only with no em dashes. Then confirm the fallback: with `timing.json` absent, chapters derive from planned `duration_s`.
- [ ] **Step 4: Commit.**
  ```bash
  git add skills/package-my-video/SKILL.md
  git commit -m "feat(youtube-studio): package-my-video skill (publish-ready folder, timing-contract chapters)"
  ```

**Merge gate (spec §5 Task 1.6 DoD):** a script + rendered video + thumbnail → one named folder with all six artifacts + a short readme; every owner-facing line positive-only, no em dashes. Test gate: offline; lint clean; the folder assembles from local fixtures.

---

## Task 1.7 — knowledge files (fully independent; land early)

No dependency; can start immediately. 1.2/1.3/1.5/1.6 link to these, so land them before those tasks' link-checks (or first).

**Files:**
- Create: `knowledge/youtube-packaging-method.md`
- Create: `knowledge/youtube-script-method.md`

- [ ] **Step 1: Author both** as self-contained craft docs, siblings of `knowledge/youtube-thumbnail-method.md`:
  - `youtube-packaging-method.md`: outlier analysis, angle/title/thumbnail differentiation, franchise thinking (the packaging craft `research-my-channel` + `plan-my-youtube` reference).
  - `youtube-script-method.md`: hook patterns, retention structure, per-beat discipline, and the words-per-minute default rationale (the craft `script-my-video` references). End each with the positive-only + no-em-dash output rule (as `seo-method.md` does — note: em dashes are fine in the *dev-facing* method prose per memory `em-dash-scope`; the rule these files STATE is the one skills apply to owner-facing output).
- [ ] **Step 2: Voice check + link-check.**
  ```bash
  BOS_OFFLINE=1 python tools/check-doctrine-voice.py
  ```
  Expected: clean. Manually confirm the skills that reference these files point at the right paths (a link-check the referencing tasks also run).
- [ ] **Step 3: Commit.**
  ```bash
  git add knowledge/youtube-packaging-method.md knowledge/youtube-script-method.md
  git commit -m "docs(youtube-studio): youtube-packaging-method + youtube-script-method knowledge files"
  ```

**Merge gate (spec §5 Task 1.7 DoD):** each method file is a self-contained craft doc; the skills link to them rather than restating. Test gate: n/a (docs); a link-check that the skills point at them.

---

## Task 1.8 — wiring, registry, surfaces, compliance

Needs every skill folder + the studio present. Single worktree (regenerates `kernel/registry.json` + `docs/CAPABILITIES.md` — not parallel-mergeable).

**Files:**
- Modify: `knowledge/starter-projects.md`
- Regenerate: `kernel/registry.json`, `docs/CAPABILITIES.md`

- [ ] **Step 1: Add starter-projects rows.** Under the **🎨 market group** of `knowledge/starter-projects.md`, add the research/plan/script/package factory as keyless first-build / deeper wins (outcome-led pitch, skill-id in backticks, tagged keyless — NOT `better_with_crm`/`needs_crm`). The Phase-2+ rungs (voice/avatar/publish) are `needs_connection` doorways only — do **NOT** add them to the cold pool until their drivers ship. Promote the Planned-section relationship per spec Decision 8 (the YouTube floor is live-keyless; `make-brand-video` stays Planned/separate — do not conflate them).
- [ ] **Step 2: Regenerate registry + capabilities.**
  ```bash
  BOS_OFFLINE=1 python tools/registry-generator.py
  BOS_OFFLINE=1 python tools/export-capabilities.py
  grep -n "research-my-channel\|plan-my-youtube\|script-my-video\|package-my-video" kernel/registry.json
  ```
  Expected: all four new skills present with `requires_credential: none` and the frontmatter slots from their tasks. (A manifest that fails `tools/manifest.py` validation is silently skipped by the generator — so if a skill is missing here, its frontmatter failed validation; fix it first.)
- [ ] **Step 3: Run every guard script** (spec §5 Task 1.8 test gate).
  ```bash
  BOS_OFFLINE=1 python tools/check-onboarding-binding.py  # floor skills keyless-clean, not needs_connection
  BOS_OFFLINE=1 python tools/check-connectors.py          # yt-dlp kind:local validated; no activation paths
  BOS_OFFLINE=1 python tools/check-surface-budget.py      # every description <= 400 chars
  BOS_OFFLINE=1 python tools/registry-generator.py --check
  BOS_OFFLINE=1 python tools/export-capabilities.py --check
  for d in skills/research-my-channel skills/plan-my-youtube skills/script-my-video skills/package-my-video skills/make-thumbnail; do python tools/lint-skill.py "$d"; done
  ```
  Expected: all exit 0. (Tree-wide manifest validation happens through the `registry-generator.py --check` + `export-capabilities.py --check` + `lint-skill.py` trio, which all import the shared `validate_manifest` — there is no bare tree-wide `manifest.py` call; per-skill checks used its one-PATH form in earlier tasks.) `registry-generator.py --check` reports not STALE. `check-surface-budget.py` confirms all four new descriptions (and the updated `make-thumbnail`) are within the 400-char cap. No new command shims exist (Decision 6 — the four new skills get **no `commands/*` shim**; verify none were added).
- [ ] **Step 4: Full offline suite.**
  ```bash
  BOS_OFFLINE=1 python -m unittest discover -s tests -v
  BOS_OFFLINE=1 python tools/check-no-secrets.py
  BOS_OFFLINE=1 python tools/check-kernel-clean.py
  BOS_OFFLINE=1 python tools/check-doctrine-voice.py
  ```
  Expected: all green.
- [ ] **Step 5: Commit.**
  ```bash
  git add knowledge/starter-projects.md kernel/registry.json docs/CAPABILITIES.md
  git commit -m "feat(youtube-studio): register + onboard the keyless factory (starter-projects rows, registry, capabilities)"
  ```

**Merge gate (spec §5 Task 1.8 DoD):** registry regenerates clean, all guard scripts green, CAPABILITIES current. Test gate: full offline suite green; `registry-generator.py --check` not STALE.

---

## Task 1.9 — Sonnet dogfood (THE MERGE GATE)

Everything above green first. Dogfood on **Sonnet** (the client run-tier — memory `bos-target-model-is-sonnet`).

- [ ] **Step 1: Run the scenario** — a local tradie who wants a channel. Walk the full floor: `research-my-channel` → `plan-my-youtube` → `script-my-video` → `studio/video` → `make-thumbnail` → `package-my-video`.
- [ ] **Step 2: Pass bar (spec §5 Task 1.9):**
  - `research-my-channel` returns evidence-anchored ideas (no invented comments);
  - `plan-my-youtube` composes a real pipeline without re-deriving strategy;
  - `script-my-video` emits a schema-valid beat script with the hook in-window;
  - `studio/video` renders a branded text-on-screen MP4 (silent stereo track, colours from `brand.json`, no TrustPager literals) + the `<slug>.timing.json` sidecar;
  - `make-thumbnail` is on the owner's brand (no TrustPager framing);
  - `package-my-video` assembles the folder with chapters from `timing.json`;
  - every customer-facing line is positive-only with no em dashes.
- [ ] **Step 3: Fold fixes + re-run gates.** Record the result in the spec's status line (mirroring how the SEO/site specs record their dogfood). Do not declare Phase 1 done until this passes.

---

## Definition of Done (the whole Phase 1 floor)

- **Every spec §5 gate met** — Tasks 1.1-1.8 each pass their stated DoD + test gate (listed per task above).
- **Full suite green** — the CI-order gate block at the top of this plan all exits 0:
  - `check-no-secrets`, `check-kernel-clean`, `check-doctrine-voice`, `check-connectors` (yt-dlp `kind: local` resolves, no activation paths), `check-onboarding-binding` (the four floor skills are keyless-clean, not `needs_connection`), `check-surface-budget` (all descriptions ≤400), `registry-generator --check` (not STALE), `export-capabilities --check`, `lint-skill` on all five skills, `unittest discover -s tests`. (Manifest validation rides in the generator/lint trio, which import the shared `validate_manifest`.)
  - **No `mcp__*` token** in any of the four floor skill bodies or the genericised `make-thumbnail` (spec §7).
  - **No new command shims** (Decision 6).
  - **No `kernel/*` edit** (spec §7 — Phase 1 adds skills + one studio + knowledge + one `local` driver blueprint only).
- **The keyless walk works** — an owner with zero accounts goes research → plan → script → branded text-on-screen video → thumbnail → publish-ready folder, entirely keyless and green under `BOS_OFFLINE`.
- **Sonnet dogfood passes** (Task 1.9 pass bar) — the merge gate. Only then is Phase 1 done.

Finish the branch per `superpowers:finishing-a-development-branch` (the BOS repo push is Vic's to run — memory `push-means-bos-repo`).

---

## Non-goals (carried from spec §9)

Phases 2-4 (faceless voice, AI twin, publish) and their drivers; Shorts/vertical auto-cutting; the TrustPager `ai_generate_*` route; the `make-brand-video` RVS bridge; any hosted/multi-tenant video service, in-app editor, or auto-captioning. No re-implementation of research / social strategy / content planning / brand strategy — `research-my-channel` delegates to Firecrawl, `plan-my-youtube` composes the two existing skills, brand comes from `brand.json`.

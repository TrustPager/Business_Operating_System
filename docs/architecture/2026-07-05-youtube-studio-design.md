# YouTube Studio — the ladder: keyless script-driven video floor, then connected fidelity rungs

**Status:** Phase 1 (keyless floor) IMPLEMENTED and Sonnet-dogfood GREEN on branch `feat/youtube-studio` (all 7 pass-bar criteria passed on a fresh plumber walk, 2026-07-06). Merged within that branch, not yet pushed (the push is the founder's). Connected rungs (Phases 2-4) are not built yet. Founder-approved as Approach A, 2026-07-05. This is the build
spec for the `youtube-studio` Tier-1 add-on: a keyless floor that takes an owner
from channel research to a publish-ready, branded, text-on-screen video, plus three
later connected rungs (faceless voice, AI twin, publish) that RE-RENDER the same
artifacts at higher fidelity rather than adding side paths. Founder-approved as
Approach A, "the ladder". The organizing principle throughout: **the script is the
spec** — one beat-structured script artifact drives on-screen graphics, voiceover
(when keys arrive), thumbnail concept, and metadata.

The floor is the sibling of the site-builder floor
([2026-07-03-site-builder-design.md](2026-07-03-site-builder-design.md)) and the ads
floor ([2026-07-03-meta-ads-addon-design.md](2026-07-03-meta-ads-addon-design.md)):
keep the *method* wholesale, ship the *keyless slice* bounded and studio-class, mark
the *paid / connected* steps as later rungs. The connected rungs are built to the
[Tier-1 Connected Add-on Kit](tier-1-addon-kit.md) and its Connection Scoping
Doctrine; this spec links to that doctrine and never restates it.

---

## 1. Why

Owners want a channel that earns them attention, not a video-editing degree. Three
capabilities are all wanted (founder-ruled): the full factory (research → plan →
script → render → package), a faceless mode (fully voiced video with no camera), and
an AI-twin mode (an avatar that presents). The ladder order is approved: ship the
keyless factory floor first, then add fidelity in rungs, each rung re-rendering the
*same* script artifact rather than forking a new path.

The BOS already proved the load-bearing half of this. The four render studios
(`studio/thumbnails`, `og`, `social`, `cta`) render `brand.json`-driven,
beat-structured specs to branded PNGs through Vite + React + Puppeteer, and
`studio/thumbnails/src/remotion-shim.jsx` already renders Remotion components as
stills in plain React. The YouTube thumbnail craft is already distilled
([knowledge/youtube-thumbnail-method.md](../../knowledge/youtube-thumbnail-method.md)).
What is missing is the *video* surface and the *script discipline* that makes a video
machine-renderable. This add-on supplies both, keyless, and leaves every fidelity
upgrade to a later rung the owner unlocks with a best-in-class key.

**The value is the ladder, not any one rung.** A keyless owner gets a real,
publish-ready, branded video from their own words on day one (text-on-screen,
manual upload). When they are ready for more, the *same script* comes back fully
voiced, then presented by an avatar, then published and measured — no rework, no
second tool.

---

## 2. The shape — one floor of six surfaces, then four rungs

### Floor (Phase 1, all keyless, green under `BOS_OFFLINE`)

| Surface | Kind | Job |
|---|---|---|
| **`research-my-channel`** (new skill) | Floor, keyless (Firecrawl) | Competitor content scan + comment mining + novel-packaging gap-and-angle map → `youtube-research.md`. Optional keyless `yt-dlp` local-driver deepener for transcripts + full comment threads. |
| **`plan-my-youtube`** (new skill) | Floor, keyless, composes | Channel strategy + a video pipeline (idea → angle → working title → thumbnail concept per video), COMPOSING `build-social-strategy` + `plan-my-content`, consuming the research artifact. |
| **`script-my-video`** (new skill) | Floor, keyless, load-bearing | The beat-structured script: per beat the spoken line (owner's voice), on-screen text/graphic callout, b-roll/visual note. Hook, promise, retention resets, CTA. Deliberately machine-renderable. Writes `<slug>.script.json` + a human-readable `<slug>.script.md`. |
| **`studio/video`** (new studio) | Floor, keyless, studio-class | The fifth render studio, same Vite/React + Puppeteer/npm+Chromium pattern as the four existing studios, driven by root `brand/brand.json`. Renders script beats as branded text-on-screen motion-graphics video. |
| **`make-thumbnail`** (exists, genericised) | Floor, keyless, studio-class | Freed from TrustPager-tutorial framing (owner's brand, non-tutorial titles), taking the packaging concept from `plan-my-youtube`. |
| **`package-my-video`** (new skill) | Floor, keyless | One publish-ready folder: video, thumbnail, title options, description with chapters, tags, publish checklist. Manual upload is the honest floor ending. Extends the `assemble-content-pack` pattern. |

**Knowledge files (floor), siblings of `youtube-thumbnail-method.md`:**
`knowledge/youtube-packaging-method.md` (novel packaging craft) and
`knowledge/youtube-script-method.md` (hook patterns, retention structure, per-beat
discipline).

### Connected rungs (later phases, spec'd at decision level only)

| Rung | Phase | Kind | What it re-renders |
|---|---|---|---|
| **Faceless voice** | 2 | Best-in-class `keyed_cli` drivers (voice first; music/image optional) | The same scripts, fully voiced. Provider selected at build time (named candidates §6). |
| **AI twin** | 3 | Avatar provider `keyed_cli` driver (HeyGen-class) | The same scripts, presented by an avatar. |
| **Publish** | 4 | `youtube` driver (upload + analytics) | Uploads the packaged video; analytics feeds back into `research-my-channel`. OAuth → the one genuinely MCP-shaped candidate (`claude_mcp`, local scope). |

Every rung consumes the Phase-1 `<slug>.script.json` unchanged. The script is the
spine; the rungs raise fidelity on the same spine.

---

## 3. The organizing principle — the script is the spec

`script-my-video` writes one machine-renderable artifact, `<slug>.script.json`, that
every downstream surface reads. This is the same discipline the render studios
already run on (`samples.json` beats → branded stills); the video studio is the
motion generalisation of it, and it is why the connected rungs need no rework.

**The beat schema (the contract between every surface):**

```jsonc
{
  "slug": "quote-in-60-seconds",
  "working_title": "How I Quote a Job in Under a Minute",
  "packaging": { "title_options": [ ... ], "thumbnail_concept": "...", "angle": "..." },
  "meta": { "duration_target_s": 75, "aspect": "16:9", "hook_window_s": 5 },
  "beats": [
    {
      "id": "hook",
      "role": "hook",                 // hook | promise | point | reset | proof | cta
      "spoken": "…",                  // the owner's-voice line (drives VO on Phase 2)
      "on_screen": "…",               // the text/graphic callout (drives studio/video)
      "b_roll": "…",                  // visual note (drives owner's own footage / stock guidance)
      "evidence_ref": "…",            // optional: a customer-voice quote id the claim rests on
      "duration_s": 6                 // optional: planned duration, estimated by script-my-video
                                      // from spoken-word count at a stated words-per-minute
                                      // default (the skill states the wpm it used)
    }
    // …promise, retention resets, points, proof, CTA
  ]
}
```

**The timing contract (planned vs actual — one explicit contract, two halves):**
(a) `script-my-video` writes the optional per-beat `duration_s` above (the *planned*
timing, word-count × a stated words-per-minute default). (b) `studio/video` writes a
`<slug>.timing.json` sidecar after render with the *actual* rendered per-beat
start/end times. `package-my-video` consumes `<slug>.timing.json` when present (real
chapter timestamps) and falls back to the planned per-beat `duration_s` otherwise.
This contract is referenced from Tasks 1.1, 1.4, and 1.6 so three different
implementers cannot drift on it.

- **`on_screen`** drives `studio/video` (branded text-on-screen motion graphics) on
  the floor, keyless.
- **`spoken`** drives the Phase-2 voice driver (best-in-class TTS) when a key
  arrives, and the Phase-3 avatar driver after that. On the floor it is the owner's
  own recording guide.
- **`packaging.thumbnail_concept`** drives `make-thumbnail`.
- **`packaging` + `meta`** drive `package-my-video`'s title/description/tags.
- A companion `<slug>.script.md` is the human-readable teleprompter/shot-list view.

**Claims are anchored in customer-voice evidence where available** (`evidence_ref`
into a `build-customer-voice` synthesis), never fabricated — the same safeguard the
site-builder and ads floors carry.

---

## 4. Decisions (founder-ruled 2026-07-05)

Numbered like [founder-decisions.md](founder-decisions.md); each carries its
rationale. Decisions 8–10 LABEL where this spec supersedes or refines earlier video
rulings, per the one-rule-one-home policy.

**1. Ladder order — floor factory first, then fidelity rungs (approved).** Ship the
keyless factory (research → plan → script → text-on-screen render → thumbnail →
package → manual upload) as Phase 1. Faceless voice (Phase 2), AI twin (Phase 3),
publish (Phase 4) follow, each re-rendering the *same* `<slug>.script.json` at higher
fidelity. Rationale: a keyless owner gets a real, complete win on day one, and no
rung throws away prior work — the exact floor/deepener shape the whole system runs
on. Full factory + faceless + AI-twin are all wanted; the ladder sequences them.

**2. Best-in-class keys, explicitly NOT TrustPager-first.** Voice, music, and image
generation route through best-in-class third-party APIs (ElevenLabs-class for voice;
named candidates in §6), never the TrustPager `ai_generate_*` route. Rationale: the
quality bar for a public YouTube channel is set by the category leaders, and the
owner already pays them or will; wiring their own key beats a lowest-common-
denominator platform call. This is the founder ruling; the TrustPager route is the
rejected-for-now alternative (§9).

**3. Connection kind per the Connection Scoping Doctrine.** Every driver this spec
proposes states its kind and scope per the doctrine in
[tier-1-addon-kit.md](tier-1-addon-kit.md) (linked, never restated):

| Driver | Kind | Scope | Why (per the doctrine — see it for the rule) |
|---|---|---|---|
| `yt-dlp` (optional floor deepener) | `local` | n/a (local CLI, no account) | Keyless local binary, stateless. |
| voice / music / image (Phase 2) | `keyed_cli` | n/a (keyed CLI, no registered server) | Stateless key-in / JSON-out services → the doctrine's CLI-first shape. |
| avatar (Phase 3) | `keyed_cli` | n/a | Same: stateless render-job API, key-in / file-out. |
| `youtube` (Phase 4) | `claude_mcp` | **local (this-folder) scope** | OAuth sign-in + persistent connection → the one genuinely MCP-shaped candidate; scope per the doctrine's scoped-connections rule. |

Rationale: the kind and scope assignments above follow directly from the Connection
Scoping Doctrine in [tier-1-addon-kit.md](tier-1-addon-kit.md); that section owns the
reasoning, and this spec only applies it. Voice/music/image/avatar are stateless →
`keyed_cli`. Only YouTube's OAuth + upload session justifies a `claude_mcp` server,
and it takes local scope.

**4. Render mechanism — Puppeteer frame-capture inside `studio/video`, NOT a
Remotion dependency in the studio folder.** `studio/video` is the fifth studio in the
existing family and copies its proven stack exactly: Vite + React, `brand.json` via
an `src/brand.js` identical to `studio/social/src/brand.js`, Puppeteer + the
npm-bundled Chromium, `npm run shoot`/`dev`/`render` scripts. It renders motion by
frame-capturing a React timeline (the template reads its frame from a `?frame=N`
URL query param; the renderer iterates `0..duration*fps` deterministically, never
realtime capture; stitch to MP4/GIF with the npm-bundled `ffmpeg-static`) — the
motion generalisation of the still studios, reusing `remotion-shim.jsx`'s "resolve
animations at a frame" idea. The floor MP4 carries a **silent stereo audio track**,
so the Phase-2 voice rung is a track replacement/remux, not a container change. Rationale considered and rejected: adding Remotion
*inside* `studio/video` would (a) duplicate the render engine the workspace hard-rule
reserves for the separate `Remotion-VideoStudio` repo, and (b) break the "five
studios, one pattern" symmetry a builder relies on. Keeping frame-capture keeps the
studio keyless (`requires_driver: render`), self-contained, and consistent with its
four siblings. **Open sub-decision left to implementation** (labelled): whether
`ffmpeg-static` clears the repo-hygiene / kernel-clean gates as a studio dependency,
or whether the stitch step shells a system `ffmpeg` with a keyless-fallback note —
resolve at Task 1.4, mirroring how the site-builder deferred `templates/site-starter`
vs `studio/site-starter` placement to a planning check.

**5. `yt-dlp` optional local driver — spec'd, honest about when Firecrawl suffices.**
`research-my-channel` is Firecrawl-powered by default (Firecrawl is already
user-scope keyless on every install). An optional keyless `yt-dlp` `local`-kind
driver blueprint deepens it: full competitor transcripts + complete comment threads
that Firecrawl's page-scrape cannot reach. Rationale + honest boundary (carried in
the skill body and the driver README): Firecrawl alone suffices for channel/video
*surface* facts (titles, descriptions, view counts, upload cadence, visible top
comments) — the packaging signal. `yt-dlp` is only worth its local-binary install
when the owner wants deep transcript analysis or exhaustive comment mining. Default
to Firecrawl; offer `yt-dlp` as a "want me to go deeper?" deepener, never a
prerequisite. It is a `local` driver (no account, keyless), so it stays on the floor.

**6. Shim policy — no new command shims for the new skills (labelled decision).** The
new floor skills (`research-my-channel`, `plan-my-youtube`, `script-my-video`,
`package-my-video`) get **no `commands/*` slash-command shim**. Rationale: the
8 most recent skills shipped without shims, and the floor-completion-plan §5
anti-bloat ruling flags the 1:1 command↔skill wrappers as rot at scale; skills
trigger via their frontmatter `triggers`, and `whats-possible` reads the registry.
This decision makes the new-skill practice explicit: no new shims, consistent with
recent practice. (`make-thumbnail` keeps whatever surface it already has; this
decision governs only the net-new skills.)

**7. `studio/video` is a studio, not a Remotion bridge.** The video capability ships
as an in-repo keyless studio (Decision 4), rendering text-on-screen motion graphics
from `brand.json` + the script. It is **not** a bridge to the separate
`Remotion-VideoStudio` repo. See Decision 8 for how this relates to the prior
Remotion-bridge ruling.

**8. SUPERSEDES floor-completion-plan §4 + founder-decisions D6's "Remotion bridge"
for the YouTube case (LABELLED).** Prior rulings
([floor-completion-plan.md](floor-completion-plan.md) §4;
[founder-decisions.md](founder-decisions.md) D6, lines 69–71) said the BOS video
capability is a **bridge** to `Remotion-VideoStudio` (a `tools/video-bridge.py` +
genericised RVS promo primitives), pin-on, with `make-brand-video` as the floor app.
**This spec supersedes that for the YouTube-studio scope:** the floor video surface is
the in-repo `studio/video` (frame-capture, Decision 4), NOT a bridge to RVS. Why the
change: (a) the five-studios-one-pattern symmetry is simpler to build and dogfood than
a cross-repo bridge; (b) it keeps the workspace hard-rule intact — the heavyweight
Remotion render engine stays *only* in `Remotion-VideoStudio`, and `studio/video`
uses the same lightweight Puppeteer frame-capture the other four studios already use,
so no video render engine is duplicated. The RVS repo and its hard rule are untouched;
this spec simply does not route through it. `make-brand-video` (the RVS-bridge floor
app named in the Planned section of
[starter-projects.md](../../knowledge/starter-projects.md)) is **out of scope here**
and left as-is — if it ships later it is a *different* capability (a generic brand
promo via RVS), not the YouTube factory. This supersession is labelled so the two
video designs do not silently diverge; the one home for the YouTube video render
decision is this doc.

> **[REVISED 2026-07-09, Content Creation Studio — LABELLED]** Point (b) above said
> "the heavyweight Remotion render engine stays *only* in `Remotion-VideoStudio`." That
> line is now revised: a *genericised* Remotion engine also lives in-repo at
> `studio/motion` (the premium Content Creation Studio, realizing founder-decisions D13).
> This does NOT change Decision 8 for `studio/video` — the floor stays keyless Puppeteer
> frame-capture, untouched. BOS now knowingly carries two render engines (keyless floor +
> Remotion premium module); they are different rungs. One home for this call:
> founder-decisions.md D14 and
> [2026-07-09-content-creation-studio-design.md](2026-07-09-content-creation-studio-design.md).

**9. SUPERSEDES `make-thumbnail`'s TrustPager-tutorial framing (LABELLED).**
`make-thumbnail` and its studio
([studio/thumbnails](../../studio/thumbnails/CLAUDE.md)) are today steeped in
TrustPager-tutorial framing: the YouTube title hard-rule "must say TrustPager, no
third-party vendor names", the tutorial-thumbnail hero library, the
`publish → TrustPager Files` step. **This spec refines `make-thumbnail` to the
owner's brand and non-tutorial titles:** titles carry the *owner's* brand (from
`brand.json`), packaging comes from `plan-my-youtube`'s concept, and the vendor-name
hard-rule becomes "the owner's brand, no unintended third-party names". The
distilled craft in
[youtube-thumbnail-method.md](../../knowledge/youtube-thumbnail-method.md) is kept
wholesale; only the TrustPager-specific framing is genericised. This is a labelled
supersession of the current framing, flagged so a reviewer sees exactly what flips
and why. (Consistent with the floor-completion-plan's own note that `make-thumbnail`
was TrustPager-tutorial-steeped; here it is genericised rather than demoted.)

**10. REFINES founder-decisions D6's floor voiceover ruling (LABELLED).**
[floor-completion-plan.md](floor-completion-plan.md) §4 ruled floor video is
"voiceover OFF by default (text-on-screen only) to stay keyless; VO via
`ai_generate_speech` is a connected-tier upgrade (TrustPager MCP — NOT floor)."
**This spec keeps floor video text-on-screen-only and keyless (agreeing on the
floor), but refines the *upgrade path*:** the connected voice upgrade routes through a
best-in-class `keyed_cli` voice driver (Decision 2), NOT the TrustPager
`ai_generate_speech` route. Labelled so the divergence reads as policy: the "floor is
silent, keyless text-on-screen" rule stands; the "how voice arrives later" rule is
updated to best-in-class keys per Decision 2.

---

## 5. Phase 1 (floor) — implementation outline, task-sliceable

Every task is keyless and must stay green under `BOS_OFFLINE`. An implementation
planner consumes this section; each task carries its own definition-of-done and test
gate. Slices are ordered by dependency (the script schema is load-bearing, so it
lands before the surfaces that read it).

### Task 1.1 — The script schema + `script-my-video` skill
- **Build:** `skills/script-my-video/SKILL.md` (keyless, gate-led for Sonnet). Reads
  `brand/brand.json` (A) and `./CLAUDE.md` (B) silently; the interview is the video-
  specific bucket (topic, the one action the video drives, target length, aspect).
  Consumes `youtube-research.md` + the `plan-my-youtube` pipeline row if present.
  Emits `<slug>.script.json` (the §3 schema) + `<slug>.script.md`. Fills each beat's
  optional `duration_s` (planned timing) from spoken-word count at a stated
  words-per-minute default, per the §3 timing contract. Anchors claims in
  customer-voice evidence where a synthesis exists; never fabricates quotes, numbers,
  or testimonials.
- **Frontmatter:** `function_slot: creative`, `requires_driver: none`,
  `requires_credential: none`, `data_path: local`, `status: active`. No `mcp__*` token
  anywhere in the body.
- **DoD:** a topic + brand → a valid `<slug>.script.json` conforming to the schema,
  positive-only, no em dashes in owner-facing copy, hook inside the target window.
- **Test gate:** offline fixture (topic payload → schema-valid JSON with all required
  beat roles present); `tools/lint-skill.py` clean; no network.

### Task 1.2 — `research-my-channel` skill (+ optional `yt-dlp` local-driver blueprint)
- **Build:** `skills/research-my-channel/SKILL.md`. Firecrawl-powered (delegates to
  the keyless hosted Firecrawl read, scope-clamped per
  [research-method.md](../../knowledge/research-method.md): no crawl/map/agent/extract).
  Three outputs into `youtube-research.md`: (a) competitor content scan — topics,
  formats, cadence, outliers vs the channel baseline; (b) comment mining — questions,
  complaints, "nobody explains X" gaps, each an idea WITH evidence in the audience's
  own words; (c) novel-packaging gap-and-angle map — topics packaged identically,
  angles nobody takes, title/thumbnail/franchise concepts that stand out. Optional
  deepener: the `drivers/yt-dlp/` `local`-kind blueprint (Decision 5) for transcripts
  + full comment threads, offered as "want me to go deeper?", never required.
- **Frontmatter:** `function_slot: research` (a confirmed valid `FUNCTION_SLOTS`
  value in `tools/manifest.py`),
  `requires_driver: none`, `requires_credential: none`, `data_path: fetch_rest`
  (it reads the live web, same as the sibling research skills; not `reasoning_only`).
  Firecrawl is reached by delegating to the research skills / keyless hosted MCP, not
  by naming an `mcp__*` tool in the body.
- **DoD:** a niche + channel URL → a `youtube-research.md` with all three sections,
  every mined idea carrying a verbatim-evidence line; the packaging map cites real
  observed outliers, never invented ones.
- **Test gate:** offline fixture (a saved competitor-page payload → a correct
  research artifact); no live fetch; `BOS_OFFLINE` green.

### Task 1.3 — `plan-my-youtube` skill (composition, no forking)
- **Build:** `skills/plan-my-youtube/SKILL.md`. COMPOSES `build-social-strategy` +
  `plan-my-content` (delegates to them, never copies or forks their bodies), consuming
  `youtube-research.md`. Produces channel strategy + a video pipeline: per video an
  idea → angle → working title → thumbnail concept (the packaging seed
  `script-my-video` and `make-thumbnail` both read).
- **Frontmatter:** keyless floor (`requires_driver: none`, `requires_credential:
  none`, `data_path: reasoning_only`).
- **DoD:** research artifact → a channel strategy + a dated/ordered video pipeline of
  N videos, each with the four packaging fields; delegation to the two existing skills
  is by-reference, no duplicated strategy logic.
- **Test gate:** offline; lint clean; a check that it references (not restates)
  `build-social-strategy` + `plan-my-content`.

### Task 1.4 — `studio/video` (the fifth studio)
- **Build:** `studio/video/` mirroring `studio/social/` exactly: `package.json`
  (`dev`/`shoot`/`render` scripts), `vite.config.js`, `src/brand.js` (identical
  single-root `brand/brand.json` import), `src/main.jsx`, `src/App.jsx` (studio
  preview), a template that renders a `<slug>.script.json`'s beats as branded
  text-on-screen motion graphics, a Puppeteer frame-capture `render.js` +
  `ffmpeg-static` stitch to MP4/GIF (Decision 4). Plus `studio/video/CLAUDE.md` +
  `README.md` in the four-studios documentation pattern.
- **Frame-drive interface (concrete):** the video template reads its frame from a URL
  query param (`?frame=N`); `render.js` iterates `0..duration*fps`, loading/setting
  each frame and capturing it — deterministic stepping, never realtime capture.
- **Timing sidecar (§3 timing contract):** after render, `render.js` writes
  `<slug>.timing.json` with the actual rendered per-beat start/end times, which
  `package-my-video` consumes for chapter timestamps.
- **Audio track:** the floor MP4 carries a silent stereo audio track, so the Phase-2
  voice rung is a track replacement/remux, not a container change (Decision 4).
- **DoD:** `npm install && npm run shoot <slug>` on a fixture script produces a
  branded MP4 (silent stereo track present) whose on-screen text matches the beats,
  colours from `brand.json`, no TrustPager literals, plus the `<slug>.timing.json`
  sidecar; runs on the npm-bundled Chromium with no account.
- **Test gate:** the studio's own smoke render on a committed fixture script; the
  repo-hygiene / kernel-clean gates pass for the new studio folder (resolve the
  `ffmpeg-static` sub-decision here, Decision 4); `node_modules` gitignored.

### Task 1.5 — genericise `make-thumbnail` (Decision 9)
- **Build:** refine `skills/make-thumbnail/SKILL.md` + the `studio/thumbnails` framing
  to the owner's brand + non-tutorial titles; take the packaging concept from
  `plan-my-youtube`. Keep the distilled craft in `youtube-thumbnail-method.md`; flip
  only the TrustPager-specific hard-rules and the tutorial-hero assumption.
- **DoD:** a thumbnail for a non-tutorial owner-brand video renders on the owner's
  palette with no "must say TrustPager" constraint and no unintended third-party
  vendor names; the vendor-name safeguard is retained in generic form.
- **Test gate:** lint clean; an offline render on the owner-brand fixture; a grep
  showing no new TrustPager literals introduced.

### Task 1.6 — `package-my-video` skill
- **Build:** `skills/package-my-video/SKILL.md`, extending the `assemble-content-pack`
  pattern. Collates one publish-ready folder: the rendered video, the thumbnail, title
  options (from packaging), a description with chapters, tags, and a publish
  checklist. Chapter timestamps follow the §3 timing contract: consume
  `<slug>.timing.json` when present (actual rendered per-beat start/end), fall back
  to the script's planned per-beat `duration_s` otherwise. Manual upload is the
  honest floor ending (Phase 4 automates it).
- **Frontmatter:** keyless floor (`data_path: local`).
- **DoD:** a script + rendered video + thumbnail → one named folder with all six
  artifacts + a short readme; every owner-facing line positive-only, no em dashes.
- **Test gate:** offline; lint clean; the folder assembles from local fixtures.

### Task 1.7 — knowledge files
- **Build:** `knowledge/youtube-packaging-method.md` (outlier analysis, angle/title/
  thumbnail differentiation, franchise thinking) and `knowledge/youtube-script-method.md`
  (hook patterns, retention structure, per-beat discipline), siblings of
  `youtube-thumbnail-method.md`. The skills reference these; the method's one home is
  the knowledge file.
- **DoD:** each method file is self-contained craft doc; the skills link to them
  rather than restating.
- **Test gate:** n/a (docs); a link-check that the skills point at them.

### Task 1.8 — wiring, registry, surfaces, compliance
- **Register** the four new skills in `kernel/registry.json` via
  `python tools/registry-generator.py`; commit `kernel/registry.json`. A manifest that
  fails `tools/manifest.py` validation is silently skipped, so all frontmatter must
  pass validation first.
- **Regenerate CAPABILITIES:** `python tools/export-capabilities.py`, commit
  `docs/CAPABILITIES.md`.
- **Starter-projects rows:** add rows under the 🎨 market group of
  [starter-projects.md](../../knowledge/starter-projects.md) — the research/plan/script/
  package factory as keyless first-build/deeper wins. The Phase-2+ rungs are
  `needs_connection` doorways, not cold pitches; do NOT add them to the cold pool until
  their drivers ship. Promote the Planned-section relationship per Decision 8 (the
  YouTube floor is live-keyless; `make-brand-video` stays Planned/separate).
- **Guard scripts green:** `tools/manifest.py` (no `mcp__*` in any keyless body),
  `tools/check-onboarding-binding.py` (no credential-coupling tokens in the
  `credential:none` bodies; the floor skills are keyless, not `needs_connection`),
  `tools/lint-skill.py` clean. `tools/check-connectors.py` passes with the `yt-dlp`
  driver validated (`kind: local`) — `drivers/yt-dlp/` ships its docs + `DRIVER` dict
  (no transport) in Phase 1, so the gate validates it from day one.
- **Descriptions within the surface budget** (skill description ≤400 chars, well
  under). **No new command shims** (Decision 6).
- **DoD:** registry regenerates clean, all guard scripts green, CAPABILITIES current.
- **Test gate:** full offline suite green; `registry-generator.py --check` not STALE.

### Task 1.9 — Sonnet dogfood (the merge gate)
- **Dogfood on Sonnet** (the client run-tier): a local tradie who wants a channel.
  Pass bar: `research-my-channel` returns evidence-anchored ideas (no invented
  comments), `plan-my-youtube` composes a real pipeline without re-deriving strategy,
  `script-my-video` emits a schema-valid beat script with the hook in-window,
  `studio/video` renders a branded text-on-screen MP4, `make-thumbnail` is on the
  owner's brand (no TrustPager framing), `package-my-video` assembles the folder, and
  every customer-facing line is positive-only with no em dashes. Don't declare Phase 1
  done until this passes.

**Phase 1 definition-of-done (the whole floor):** an owner with zero accounts goes
research → plan → script → branded text-on-screen video → thumbnail → publish-ready
folder, entirely keyless and green under `BOS_OFFLINE`, dogfooded on Sonnet.

---

## 6. Phases 2–4 (connected rungs) — decision-level only

Spec'd at decision level; each becomes its own design doc + Tier-1 kit build when
scheduled. All build to [tier-1-addon-kit.md](tier-1-addon-kit.md).

### Phase 2 — Faceless (best-in-class voice; music/image optional)
- **Drivers:** `keyed_cli` (Decision 2/3), zero standing token cost. **Named
  candidates, provider chosen at build time:** voice — ElevenLabs (category leader),
  with Cartesia / PlayHT as alternates; music (optional) — Suno / Udio; image
  (optional) — the leading text-to-image API of the day. Voice ships first; music and
  image are optional sub-rungs.
- **What it re-renders:** the same `<slug>.script.json` — each beat's `spoken` line is
  voiced by the chosen TTS, dropped onto the `studio/video` timeline, producing a fully
  voiced faceless video. No script rework.
- **Build shape:** a floor voice-plan skill is unnecessary (the script IS the plan);
  the connected skill is a `voice-my-video` doing-skill that reads the script + the
  driver profile. Follows the kit: `connect.md`, `connectors.md` card,
  `starter-projects.md` `needs_connection` row, Source A/B/C/D intake, profile as DATA
  at `~/.claude/bos-cache/youtube-voice-profile.json`.
- **DoD (when built):** the same script comes back fully voiced; `check-connectors.py`
  green for the voice driver; positive-only.

### Phase 3 — AI twin (avatar)
- **Driver:** avatar provider `keyed_cli`, HeyGen-class evaluated at build time
  (HeyGen / Synthesia / D-ID as candidates). Stateless render-job API → `keyed_cli`.
- **What it re-renders:** the same script, presented by an avatar reading the `spoken`
  lines; on-screen callouts from `studio/video` composited over or beside the avatar.
- **DoD (when built):** the same script presented by an avatar; kit-conformant.

### Phase 4 — Publish + analytics
- **Driver:** `youtube` — the one genuinely MCP-shaped candidate (OAuth + upload
  session + persistent connection), `claude_mcp` kind, **local scope** (Decision 3).
- **What it does:** uploads the `package-my-video` folder (video + thumbnail + title +
  description + tags) and reads back analytics. **Analytics feeds back into
  `research-my-channel`** — the loop closes: real performance sharpens the next
  packaging pass.
- **Safety:** publishing is a public, effectively-irreversible act → carries the kit's
  write-safety stack (confirm-before-publish, journal, `never_call` on any
  delete/irreversible tool), same shape as the ads floor's paused-by-construction and
  the site floor's preview-before-prod.
- **DoD (when built):** confirmed upload + analytics read; `check-connectors.py` green;
  local scope verified.

---

## 7. Compliance (stated here, enforced at build)

- **Floor skills:** `requires_driver: none`, `requires_credential: none`,
  `data_path: reasoning_only|local`; **no `mcp__*` token in any floor body**
  (`research-my-channel`, `plan-my-youtube`, `script-my-video`, `package-my-video`,
  and genericised `make-thumbnail` all stay keyless-clean). `studio/video` is
  `requires_driver: render` studio-class, matching `make-thumbnail`.
- **Connected rungs:** per the kit — `keyed_cli` / `claude_mcp` kinds and scopes per
  Decision 3, exhaustive `uses_tools` with any irreversible tool omitted, `connect.md`
  one-home, `connectors.md` card, `needs_connection` row, Source A/B/C/D intake,
  profile as DATA, `OPERATING-CONTEXT.md` fold-in with the skill's own no-clobber
  merge (never `learn-my-business`).
- **Kernel unchanged:** Phase 1 adds skills + one studio + knowledge files only; no
  `kernel/*` edit. The connected rungs add `requires_driver` strings + folderless
  driver docs, no kernel change (same as the ads/site floors).
- **Surfaces:** starter-projects rows; `kernel/registry.json` regeneration via the
  generator; `docs/CAPABILITIES.md` regeneration; connectors cards when drivers land.
- **Shims:** none for the new skills (Decision 6).
- **Language:** positive-only in all owner-facing text (script CTAs, thumbnail/title
  copy, package readme, connect stories); no em dashes in shipped copy. Method craft
  attributed in the knowledge files.
- **Model + gate:** author skills as numbered gates before defaults (target model
  Sonnet); Sonnet dogfood before merge (Task 1.9).

---

## 8. Artifact inventory

**New skills (`skills/`):** `research-my-channel/SKILL.md`, `plan-my-youtube/SKILL.md`,
`script-my-video/SKILL.md`, `package-my-video/SKILL.md`.

**New studio (`studio/`):** `studio/video/` — `package.json`, `vite.config.js`,
`src/brand.js`, `src/main.jsx`, `src/App.jsx`, template(s) for beat rendering,
`scripts/render.js` (+ `shoot.js`/`dev`), `CLAUDE.md`, `README.md`, `data/` fixture
script, `output/` (gitignored).

**New knowledge files (`knowledge/`):** `youtube-packaging-method.md`,
`youtube-script-method.md`.

**New driver blueprints (`drivers/`, Phase 1 optional + later phases):**
`drivers/yt-dlp/` (local, optional floor deepener — docs + `DRIVER` dict, no
transport); Phase 2+ `drivers/<voice>/`, `drivers/<music>/`, `drivers/<image>/`,
`drivers/<avatar>/` (`keyed_cli`, docs-only), `drivers/youtube/` (`claude_mcp`,
folderless docs) — each with `connect.md` + `connectors.md` card when it ships.

**New per-owner profiles (`~/.claude/bos-cache/`, outside the repo):**
`youtube-voice-profile.json` and later rung profiles — DATA, never forked skill files.

**New artifacts the add-on produces (owner's working dir):** `youtube-research.md`,
`<slug>.script.json`, `<slug>.script.md`, `<slug>.timing.json` (the actual per-beat
render timing sidecar, §3 timing contract), the rendered video (MP4/GIF), the
thumbnail PNG, the `package-my-video` publish-ready folder.

**Existing files touched:** `skills/make-thumbnail/SKILL.md` +
`studio/thumbnails/*` (genericised, Decision 9); `kernel/registry.json` (regenerated);
`docs/CAPABILITIES.md` (regenerated); `knowledge/starter-projects.md` (new market
rows + Planned-section relationship per Decision 8); `knowledge/connectors.md` +
`skills/connect-a-tool/SKILL.md` (only when Phase 2+ drivers land, with labelled
exceptions if an add-mechanism differs).

---

## 9. Out of scope (YAGNI)

- **Shorts / vertical repurposing and FFmpeg-based clip cutting** — a later rung; the
  `studio/video` timeline already parameterises aspect (`meta.aspect`), so a
  9:16 Shorts render is a small future extension, but auto-cutting a long video into
  Shorts (scene detection, reframing) is deferred.
- **TrustPager `ai_generate_*` route (rejected-for-now alternative).** The founder
  ruled voice/music/image go through best-in-class third-party keys (Decision 2), NOT
  `ai_generate_speech` / `ai_generate_music` / `ai_generate_image` on the TrustPager
  MCP. Recorded here as the considered-and-rejected path so it does not resurface as
  drift; if the platform's generation ever reaches category-leader quality, revisit.
- **The `make-brand-video` RVS bridge** — a *different* capability (generic brand
  promo via `Remotion-VideoStudio`), left in the Planned section as-is (Decision 8).
  This spec does not build or replace it; it simply does not route the YouTube factory
  through RVS.
- **No hosted/multi-tenant video service, no in-app video editor, no auto-captioning
  translation, no music-licensing management this round.**
- **No re-implementation of research, social strategy, content planning, or brand
  strategy** — `research-my-channel` delegates to Firecrawl/research skills;
  `plan-my-youtube` composes `build-social-strategy` + `plan-my-content`; brand comes
  from `brand.json`. No logic duplicated.

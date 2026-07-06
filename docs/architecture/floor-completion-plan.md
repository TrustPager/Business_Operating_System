I have full grounding on every load-bearing fact and disagreement. The lenses' two big factual claims are confirmed: transcript-summary is 100% TrustPager-coupled despite being listed as floor (a correctness gap), and the marketing method stops at content-pillars.yaml with no content-calendar layer. I now have everything to write the consolidated plan.

# BOS Floor-Completion Plan — Lead Architect's Consolidation

This is the decisive, deduped synthesis of five expert lenses against the locked docs (`founder-decisions.md` D6, `bos-rearchitecture-review.md` §2/§5/P2#12, `skill-extraction-audit.md` §2/§4/§6/§7) and the live `studio/` + `brand/` pattern. Where lenses disagreed I have ruled; where they piled onto the same item I have collapsed it to one.

**Three rulings up front that shape everything below:**

1. **`grill-me-on-this-decision`, the four Firecrawl research apps, and the Remotion bridge are DECIDED-BUT-UNBUILT** (verified: no `skills/grill*`, no `skills/research-*`, no video skill exist). They are net-new builds, not promotions. Three lenses flagged this independently — it is the single biggest gap between the locked decisions and the repo.
2. **`transcript-summary` is listed as floor but is 100% TrustPager-coupled** (confirmed: `SKILL.md` Steps 1-3 read only via `mcp__trustpager__list_transcripts/get_transcript` and log via `add_note`). As written it does NOT satisfy "works with zero accounts." This is a correctness bug, not a feature request, and must be fixed for the floor claim to be literally true.
3. **Curation discipline is the whole point.** The floor grows by *completing a job-cluster's story*, never by adding a tool because it could be on. I am net-roughly-flat on default-on count: I add a curated set and complete clusters, but I demote `make-thumbnail` to pinnable and refuse every borderline extractable.

---

## 1. The completed floor at a glance

The default-on floor after additions, grouped by the four job-clusters that make it read as ONE product. `[current]` = ships today; `[fix]` = exists but needs a standalone path; `[new]` = net-new build; `[promote]` = move from the extractable bucket to default-on.

**KNOW — outbound intelligence (keyless, Firecrawl)**
- `research-a-competitor` `[new]`
- `research-before-call` `[new]`
- (`scan-the-market`, `enrich-this-lead` stay pinnable — see §5)

**MAKE — the creative engine (one `brand.json` reskins all)**
- `build-brand-strategy` `[current]` · `build-customer-voice` `[promote]` · `brand-my-workspace` `[current]` — the brand spine
- `make-social-post` `[current]`
- `plan-my-content` `[new]` · `write-post-copy` `[new]` — the missing plan→words hinge
- `make-brand-video` (+ GIF/ad siblings) `[new, pin-on]` — the Remotion bridge
- `assemble-content-pack` `[new]` — the publish-ready terminus
- (`make-thumbnail` `[demoted to pinnable]`; `og`/`cta` studios stay pinnable extensions of this cluster)

**HANDLE PAPERWORK & DATA — zero-credential**
- `extract-document` `[current]` · `compare-documents` `[current]`
- `quote-from-photo` `[current]` (now with a driver-less pricing fallback — see §2)
- `price-my-work` `[new]` · `write-a-proposal` `[new]` — the missing sales-math loop
- `transcript-summary` `[fix]` — add a paste/local-file path
- `import-from-anywhere` `[promote]` · `build-spreadsheet` `[promote]` — get-it-in → structure-it

**THINK & RUN THE TEAM — pure reasoning**
- `write-prompt` `[current]`
- `grill-me-on-this-decision` `[new]` — the one visible reasoning anchor (D6)
- `onboard-team-member` `[current]` · `sync-team-standards` `[current]`
- `write-a-job-ad` `[new, should]` · `write-a-policy` `[new, should]` — round out hiring/SOP
- (`learn-my-business` is the invisible onboarding spine that runs first and feeds every cluster)

**The story it tells.** Today's 11-app floor is inbound/document/brand-heavy and sales/money/intelligence-light — an owner can brand a workspace and summarize a doc, but cannot *know* their market, *price and propose* the work, *plan and produce* a content drop, or *stress-test a decision* with nothing connected. The completed floor closes all four: a 2-10 person owner lands and can research a competitor, turn a brain-dump into positioning and voice, plan a fortnight of content and produce it (stills, captions, video, GIFs, a publish-ready pack), price a job and send a branded proposal, get their data in and structured, and be grilled on a hire — before connecting a single account. Every addition is `data_path: reasoning_only` (or keyless Firecrawl/local render) and *deepens* on connect (feeding `build-document`, `build-knowledge-base-from-docs`, `wire-nurture-sequence`, the live workspace sheet), so nothing is throwaway — which is the platform thesis itself (audit §1).

---

## 2. New floor apps to build — ranked

Effort: S = reasoning-only, reuses existing brand/voice docs; M = new artifact/orchestration; L = cross-repo integration.

### MUST

| App | One-line why | Effort | Standalone data source |
|---|---|---|---|
| **`grill-me-on-this-decision`** | Locked floor app (D6) with no `skills/` home today — the only visible reasoning anchor; closes a decision↔code gap at near-zero cost. | S | The decision the owner describes + their business profile. Pure reasoning, no tools. |
| **`price-my-work`** | The single highest-relief uncovered job for trades/consulting; also the driver-less pricing fallback `quote-from-photo` needs (it currently leans on `mcp__trustpager__list_products`). | S | Costs/hours/rates the owner types. `reasoning_only`. |
| **`write-a-proposal`** | The artifact that actually wins the job; closes price→proposal→(later e-sign). `build-document` only does the *live* signing template — no driver-less "just write me the proposal" exists. | M | Scope/line items (from `price-my-work`/`quote-from-photo`/paste) + the brand voice docs. Becomes the live signing template when TrustPager connects. |
| **`research-a-competitor`** + **`research-before-call`** | Two of the four Firecrawl apps D6 already decided; give the floor its missing outbound-intelligence dimension. Keyless hosted Firecrawl is already active in `.mcp.json`. | M | Keyless Firecrawl scrape/search. |
| **`plan-my-content`** | THE missing hinge: nothing turns `content-pillars.yaml` into a dated multi-channel plan (confirmed — `marketing-strategy-method.md` stops at pillars). Without it every creative app is an island. | M | `content-pillars.yaml` + `voice.md`. `reasoning_only`. |
| **`write-post-copy`** | The studios only render the on-image headline (3-8 words); nothing drafts the caption/body or paid-ad primary-text+headline+variants that publish *with* the creative. | S | Topic/brief or a `plan-my-content` row + `voice.md`. Must enforce the positive-only language rule. |
| **`make-brand-video`** (+ GIF, ad siblings) | D6's named **priority**; the floor is stills-only without it. See §4 for the full bridge design. | L | `brand.json` + voice + a plan row; local Remotion render, no account. **Pin-on.** |

### SHOULD

| App | One-line why | Effort | Standalone data source |
|---|---|---|---|
| **`assemble-content-pack`** | Collates one plan item's brief + copy + rendered asset into a publish-ready folder; the clean handoff to a channel driver. Reuses the `assemble-pack` local-folder pattern. | S | Local output files. |
| **`write-a-policy`** | Owners constantly need a cancellation/deposit/privacy policy or FAQ and have nowhere driver-less to get one; pre-feeds the planned `build-knowledge-base-from-docs`. | S | The owner describes how they do the thing + voice docs. |
| **`write-a-job-ad`** | Floor has post-hire (`onboard-team-member`) but nothing for the before-hire "write the ad + screening questions"; rounds out the team cluster. | S | Role description or business profile + voice docs. |

### COULD

| App | One-line why | Effort | Standalone data source |
|---|---|---|---|
| **`make-qr-code`** | Pure-local `qrcode` lib, renders through `brand.json`; tangible minute-one artifact (van/flyer/counter QR). | S | The link/vCard/wifi the owner gives. |
| **`make-calendar-invite`** (ICS) | Plain-text `.ics`, the most honestly-keyless "calendar" possible; lets the partner "book the next step" before any calendar OAuth. | S | Event details typed in. |

**Promotions (not builds) — covered in §3:** `build-customer-voice` (must), `import-from-anywhere`, `build-spreadsheet`, `design-nurture-sequence` (should).

**Disagreement resolved — `write-a-job-ad`/`write-a-policy` vs the JTBD lens's larger list.** Both earn their place on coverage-per-effort, but only at `should` — the coherence-critic lens is right that the floor must not balloon. They complete existing clusters (team, document-feeder) rather than opening new ones, which is the test for inclusion.

---

## 3. Keyless floor drivers

The floor's power comes from naming capabilities that already exist in the repo as *drivers*, with explicit `requires_credential: none` so the registry can truthfully answer "what can I do right now?" (the architecture panel's named optimization + P2 #12).

| Driver | Status | Unlocks |
|---|---|---|
| **Firecrawl** (keyless hosted MCP) | Decided (D6), active in `.mcp.json` | `research-a-competitor`, `research-before-call` (default-on); `scan-the-market`, `enrich-this-lead` (pinnable). All net-new builds. |
| **MarkItDown** (`tools/markitdown_convert.py`) | Exists, unnamed as a driver — **promote to first-class** | The "throw me any file" read side: PDF/Word/Excel/PPT/HTML/CSV/JSON/ZIP + image OCR, keyless local `pip`. It is the swapped data source the audit §4 says extractables need — turns `import-from-anywhere`, `build-knowledge-base-from-docs`, `template-from-document`, and the `transcript-summary` paste-path into genuine floor apps. **This is the highest-leverage keyless promotion.** |
| **Creative render** (the four studios + Remotion bridge under ONE driver) | Exists as four loose folders — **unify** | The MAKE cluster. Vite+React+Puppeteer (Chromium bundled on npm install = keyless), `brand.json`-driven, headless PNG; Remotion is the motion extension (the `remotion-shim.jsx` already renders Remotion comps as stills in plain React — confirmed). Frame as one "make branded visuals & video" capability, not five render scripts. |
| **Local doc generation** (anthropic-skills `docx`/`pptx`/`xlsx`/`pdf`, `pypdf`) | Exists — **name as the "write side"** | Finished-file artifacts offline: filled PDF, proposal `.docx`, tracker `.xlsx`. Closes the loop (read any file AND produce any file) that makes the floor feel like a product, not read-only tricks. Powers `write-a-proposal`'s output and `build-spreadsheet` standalone. |

**Honesty calibration (ruled, against the scout lens — I agree and adopt its cuts):** genuinely keyless = local `pip`/`npm` lib or keyless hosted MCP. **NOT keyless, kept out of the floor:** AI image generation (needs a key or multi-GB model), live calendar (OAuth), cloud transcription (key). Local Whisper is keyless-but-heavy → pin-on with a "downloads a model first" warning, never default. ICS file generation is the floor-appropriate calendar substitute; `make-qr-code` is keyless, QR/barcode *reading* is not worth the weight.

---

## 4. Remotion creative-engine packaging (priority)

> **Superseded on YouTube scope (labelled, 2026-07-05):** YouTube-scope video is
> superseded by
> [2026-07-05-youtube-studio-design.md](2026-07-05-youtube-studio-design.md)
> (in-repo `studio/video` frame-capture, not an RVS bridge); the `make-brand-video`
> RVS bridge below is unaffected.

This is the founder's named priority. The two creative lenses converged on the same design; I adopt it and sequence it.

### The bridge — what BOS ships vs. what it calls

**BOS ships (in-repo, DATA + one tools script):**
- **`studio/video/`** — a brand-aware spec layer mirroring the proven studio pattern: a `samples.json`-style spec file + `src/brand.js` importing the one root `brand/brand.json` (identical to `studio/social/src/brand.js`, confirmed line 7).
- **`tools/video-bridge.py`** — sibling of `tools/sync-brand.py`. Locates-or-clones `Remotion-VideoStudio` under a known path, runs `npm install`, syncs `brand.json` into it, writes the owner's spec to `scripts/<id>.json`, and shells `npx remotion render … output/<name>.{mp4|gif}` (GIF via `--codec=gif`) / `npx remotion still`.

**BOS calls (separate repo, never edited from BOS):** the existing `ScriptSpecRenderer.tsx` (already JSON-spec-driven) + the brand-generic `src/promo/` primitives (HeroLoop, FeatureSpotlight, TextReveal, ReelSlide, etc.). All `.tsx` render code stays in RVS — honouring the hard rule (founder-decisions L60-62, workspace CLAUDE.md). The bridge calls ONLY the brand-generic promo surface, **never** the TrustPager demo comps.

This fits the architecture ruling cleanly: `kernel/` + `drivers/` are DATA-only, triggerable behaviour lives in `skills/`, so the bridge is a `tools/` script + a skill, never kernel code. Its "driver" is a CLI bridge to a local repo (closest to `type=cli`), not a credential.

### Precondition — brand-genericise the RVS promo layer FIRST

Today the RVS promo primitives bind to `@tp/theme` + hardcoded TrustPager UI. Before any video floor app, add a `brand.js`-equivalent in RVS that the bridge populates from the synced `brand.json`, and confirm the primitives consume those tokens. Without this, "make a brand video" renders TrustPager teal for an unrelated plumber — breaking the platform-agnostic north star. This is the same one-`brand.json`-reskins-everything contract the still studios already prove.

### Floor apps it exposes

- **`make-brand-video`** (must) — 15-30s branded promo from `brand.json` + voice + a plan row. **Voiceover OFF by default** (text-on-screen only) to stay keyless; VO via `ai_generate_speech` is a connected-tier upgrade (it routes through the TrustPager MCP — NOT floor).
- **`make-a-gif`** (should) — looping branded GIF via `--codec=gif`; highest organic-content ROI for a small owner.
- **`make-an-ad`** (should) — hook-led video/GIF in 9:16 / 1:1 / 16:9, parameterising the spec's dimensions exactly as `studio/social` specialises one template across four formats.
- **`branded-post-set`** (should) — the headline "one brief → full kit" moment: orchestrates the still studios + a GIF for one campaign from one `brand.json`. Pure orchestration over existing apps.
- **`video-from-template`** (could) — 3-5 pre-wired templates, answer 2-3 questions, render; the friendliest first-video on-ramp (mirrors `npm run make` in `studio/thumbnails`).

### How it composes with the brand profile

`build-brand-strategy`/`brand-my-workspace` write `brand.json`; `sync-brand.py` (and the new `video-bridge.py`) propagate it; every render — still or motion — is on-brand by default with zero template edits. One brand, every surface. That IS the "develop a brand and plug it into your marketing" outcome the founder wants.

### Floor-now vs. deferred

- **Floor now:** local keyless MP4/GIF/still renders from genericised promo primitives, text-on-screen, multi-aspect. **Pin-on** per D6 (heavy first install: clone + `npm install` + multi-minute render), with a D4 warn-and-proceed heads-up; preflight remediates by cloning, never dead-ends.
- **Deferred:** per-beat AI voiceover (connected-tier, TrustPager MCP); the TrustPager UI-mockup comp library (`TrustPager-src/`, `Claude-src/` — product demos, meaningless to an agnostic owner); pixel-perfect cursor/measure-still tutorial tooling; ad-platform publishing (floor stops at the rendered asset in `output/`, exactly as the still studios stop at the PNG); the studios' `npm run publish` TrustPager-Files step (the lone TrustPager coupling — stays behind the connected section); and the dead `content-pipeline/remotion/` graveyard (target the live RVS repo, never resurrect it).

**Sequencing ruling:** do the genericise-promo + bridge as ONE foundational L-effort piece (the spine), then `make-brand-video` + `make-a-gif` ride on it cheaply. **If scope must be cut for first ship, cut `og`/`cta` surfacing and the spreadsheet/import promotions before cutting the Remotion bridge or the grill app — those two are locked decisions, not nice-to-haves.**

---

## 5. Cut / defer to the pinnable catalog

The default set is defined as much by what it excludes. These stay catalog-pinnable (discoverable via `/whats-possible`, OUT of the always-loaded trigger surface — P2 #12), with rationale.

- **`make-thumbnail` → demote to pinnable.** A YouTube tutorial thumbnail is a near-zero-relief day-one job for the named ICP (trades/broking/allied-health/consulting); the studio examples are all TrustPager tutorial thumbnails and the skill is steeped in TrustPager-tutorial framing. `make-social-post` covers the universal "branded graphic to post" need. Pin-on for the content-creator subset. *(JTBD + coherence lenses agree; I rule for demotion.)*
- **`og` / `cta` studios → pinnable extensions** of the MAKE cluster, not default-on apps. Narrower/more technical than social; folding them under the one creative slot keeps the default creative set to social + video.
- **All 22 remaining extractables stay catalog-pinnable** except the four promotions named in §1/§3. The audit's extractable bucket is its own *optimistic, unverified read* (§1, §6 — the adversarial verify pass did not run on ~21). Default-on'ing them would ship apps that quietly need a swapped data source.
- **Hard cuts (broken-promise apps):**
  - **`send-email`** — a "send" verb with no send capability; standalone it is just "draft an email" which `draft-reply` covers (audit §6). Catalog-only, lights up when a comms driver connects.
  - **`build-form` / `template-from-document`** — standalone they produce a *spec*, not a working form with a response host (audit §6). They are the lead "here's what connecting unlocks" demo, not floor.
  - **`outstanding-invoices` / `outstanding-documents` / `follow-up-radar`** — "gone quiet" needs `last_activity_at` an export may lack (audit §6); fragile minute-one promise. Catalog-only.
  - **`delegate-this-work`** — thin without a task system. Catalog-only.
- **Heavier deferrals:** generic AI image generation (no honestly-keyless path); a website/landing one-pager (heavier than a reasoning app, and TrustPager owns `create_website` natively — revisit as a 5th studio after `price-my-work`/`write-a-proposal` ship); a real calendar driver, video editor, analytics/performance reporting, media-buying strategy, full-campaign-in-one-shot generation (`plan-my-content` defaults to a reviewable 1-2 week horizon, not a 90-day firehose).
- **Never surface as toggles** (locked, D6): Superpowers and the grill-me *technique* are invisible infrastructure. The ONLY visible grill surface is the `grill-me-on-this-decision` app. Do not propose a "methodical mode" switch.
- **Anti-bloat on commands:** do NOT ship a 1:1 slash-command stub per new floor app (the review flags the 58 command↔skill wrappers as rot at scale). Keep a small curated command set; let the rest trigger via skill frontmatter or generate from manifests.

---

## 6. Definition of done — the bar before implementation

The floor's initial development stage is complete when ALL of the following hold:

- [ ] **Every default-on app carries `requires_driver: none` / `data_path: reasoning_only|fetch_rest|mcp_tools` as a first-class manifest enum**, so the registry can answer "what can you do right now with nothing connected?" as a *queryable set* (architecture optimization), not an inferred one.
- [ ] **The curated default-on set, and ONLY it, is in the always-loaded trigger surface.** All extractables + TrustPager-native apps live in the pinnable catalog reachable via `/whats-possible`, grouped by `function_slot` (KNOW / MAKE / PAPERWORK & DATA / THINK & TEAM) in plain language — never "kernel/driver/app/MCP/studio/Remotion" (P2 #12 + the plain-language partner rule + D3).
- [ ] **The two locked-but-unbuilt D6 commitments exist as real skills:** `grill-me-on-this-decision` and the Remotion bridge (`make-brand-video` + `tools/video-bridge.py` + genericised RVS promo layer).
- [ ] **The four Firecrawl research apps exist** (2 default-on, 2 pinnable) wired to the keyless hosted Firecrawl MCP.
- [ ] **`transcript-summary` has a keyless standalone path** (paste / local-file via MarkItDown → summary + decisions + action items), offering the CRM log only when connected. The floor's "works with zero accounts" claim is now literally true for all 11+ default apps.
- [ ] **MarkItDown and the creative-render pipeline are named first-class keyless drivers** with `requires_credential: none`; the four extractables MarkItDown unblocks are promotable.
- [ ] **The brand→content→produce loop is end-to-end with nothing connected:** `build-customer-voice` → `build-brand-strategy` → `plan-my-content` → `write-post-copy` + `make-social-post`/`make-brand-video` → `assemble-content-pack`. `build-customer-voice` is promoted to default-on (it is the documented prerequisite of the already-floor `build-brand-strategy` — shipping the dependent without the dependency is a broken minute-one path).
- [ ] **The sales-math loop is end-to-end:** `price-my-work` → `write-a-proposal`, and `quote-from-photo` has `price-my-work` as its driver-less pricing fallback.
- [ ] **Every new floor app ships vendor-neutral copy from the start** (the de-branding debt — ~125 files carry TrustPager literals; do not add to it) and **every customer-facing-copy app** (`write-post-copy`, `plan-my-content`, `write-a-proposal`, `write-a-job-ad`, `write-a-policy`) **enforces the positive-only language rule.**
- [ ] **Every default-on app runs green in the offline harness** (`BOS_OFFLINE` + `tools/test-skill.py`) with zero key/network — that is the operational definition of zero-credential (TESTING.md).

---

**Files cited (all under `C:\Users\USER\Desktop\Final Piece Docs\Business_Operating_System\` unless noted):** `docs/architecture/founder-decisions.md` (D3/D4/D6, floor drivers L56-69); `docs/architecture/bos-rearchitecture-review.md` (§2 kernel/driver/app contract + driver-type taxonomy, §5 data-path ruling + `requires_credential` enum, P2 #12 catalog gating, plugin-reality 1:1-command rot); `docs/architecture/skill-extraction-audit.md` (§2 buckets, §4 extraction specs, §6 borderline/verify caveat, §7 minute-one set); `skills/transcript-summary/SKILL.md` (confirmed CRM-only — the correctness gap); `skills/quote-from-photo/SKILL.md` (`list_products` pricing dependency); `knowledge/marketing-strategy-method.md` (Layers 1-4, stops at `content-pillars.yaml`); `brand/brand.json` + `brand/README.md` + `tools/sync-brand.py` + `skills/brand-my-workspace/SKILL.md` (the one-`brand.json`-reskin spine); `studio/social/src/brand.js` (line 7 — single root import) + `studio/social/CLAUDE.md` + `studio/{og,cta,thumbnails}/` (the proven shoot/publish render pattern; `publish.js` = the lone TrustPager coupling); `studio/thumbnails/src/remotion-shim.jsx` (Remotion-as-stills proof); `tools/markitdown_convert.py` + `knowledge/document-tools-method.md` (the keyless read driver); and in the sibling repo `C:\Users\USER\Desktop\Final Piece Docs\Remotion-VideoStudio\` — `CLAUDE.md`, `NEW-VIDEO.md`, `src/promo/`, `src/compositions/ScriptSpecRenderer.tsx` (the brand-generic JSON-spec render surface the bridge must call).
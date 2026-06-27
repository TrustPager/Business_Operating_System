# Floor Wave 1 — Build Out the Wins Library Implementation Plan

> **For agentic workers:** Execute via superpowers:subagent-driven-development (fresh subagent per task + spec review + quality review). Run in the `floor-wave1` worktree. **Every task's gate:** `python tools/check-onboarding-binding.py` exits 0, the relevant skill lints clean + manifest valid, `python tools/registry-generator.py --check` is fresh, and `BOS_OFFLINE=1 python -m unittest discover -s tests` is green. The binding guardrail (Wave 0) keeps the surface honest the whole way.

**Goal:** Build out **every component the first-win roster needs** ([`floor-roster.md`](../floor-roster.md)) so each roster win becomes a real, keyless, offered capability — in dependency order. Drivers first, then the apps that ride on them.

**Architecture:** Drivers are thin `tools/` wrappers + a registry-recognised `requires_driver` id (mirror `tools/markitdown_convert.py`). Apps are Markdown skills carrying manifests. Keyless = `requires_credential: none` + `requires_driver` in the keyless set. The wins library is "in order of logic": a component is only built after the things it depends on exist.

**Tech stack:** Python stdlib (kernel/tools) + vendored doc libs (openpyxl/python-docx/pdfplumber/reportlab, install-on-first-use like MarkItDown), Markdown skills, the keyless hosted Firecrawl MCP (already in `.mcp.json`), the offline harness.

**Cross-cutting rules (apply to every task):**
- **Positive-only language** on every customer-facing OUTPUT the app produces (pain-naming OK in the app's own discovery prompts). **No em dashes** in content.
- **Keyless + offline:** reasoning_only/local apps must be `BOS_OFFLINE`-green. Firecrawl apps are network (`fetch_rest`) — their offline tests MOCK/SKIP the fetch; flag the network dependency in the skill.
- **Wire each built win into onboarding:** after a win is real + keyless, promote it in `knowledge/starter-projects.md` (Planned → live keyless offer) and add it to `skills/start-here` routing where it fits a signal. The binding check then passes *because* it's now real. This is the payoff step — the library becomes real AND offered.
- **MIT-clean:** any vendored lib must be MIT/BSD/MPL (no AGPL/GPL). Document the boundary.
- After any manifest/skill change, **regenerate `kernel/registry.json`** in the same commit (the drift guard fails otherwise).
- **Update `floor-roster.md` statuses** (🆕/🔁 → ✅) as wins land.

---

## Increment 1 — Foundation drivers (build first; ~9 wins ride on these)

> Sequential — these touch `tools/`, `drivers/`, the manifest/binding contracts, and `registry.json`. Each is its own task + review.

### Task 1.1 — doc-lib-set driver (the keyless WRITE side) — unlocks 5
**Files:** create `tools/doc_write.py` (or a small set: `tools/write_xlsx.py`, `tools/write_docx.py`, `tools/fill_pdf.py`, `tools/pdf_tables.py` — mirror `markitdown_convert.py`'s shape: argparse CLI, `INSTALL_HINT`, clean exit codes); update `tools/check-onboarding-binding.py` `_KEYLESS_DRIVERS` to include the new driver id (e.g. `doclib`); document in `knowledge/document-tools-method.md`.
**Build:** thin wrappers over `openpyxl` (write .xlsx), `python-docx` (write .docx), `reportlab` (generate PDF), `pdfplumber` (precise table/text extraction beyond MarkItDown). `OCRmyPDF` gated behind a one-time install preflight; `python-pptx` on-demand only. Each wrapper: if the lib isn't installed, print a one-line `pip install` hint and exit 2 (like MarkItDown). No network at runtime → `local` / `BOS_OFFLINE`-green once installed.
**Driver id:** pick one canonical id (`doclib`) used in `requires_driver`. Add it to the binding check's keyless-driver set AND note it in the manifest contract docs.
**Tests:** mirror the MarkItDown wrapper tests — round-trip a tiny .xlsx/.docx, extract a table from a fixture PDF, assert the install-hint path. License check: record that all four libs are MIT/BSD/MPL.
**Acceptance:** wrappers run; missing-lib path is graceful; `doclib` is a recognised keyless driver; lint/binding/registry/offline green.

### Task 1.2 — markitdown promoted to first-class keyless driver — unlocks 4
**Files:** `knowledge/document-tools-method.md` (name MarkItDown the canonical keyless READ driver); confirm `markitdown` is in the binding-check keyless set (it is). Light task — `tools/markitdown_convert.py` already exists and skills already declare `requires_driver: markitdown`.
**Build:** make the convention explicit/documented so downstream tasks (transcript-summary fix, import-from-anywhere) have a clean keyless read path to lean on. No behavioural change unless a gap is found.
**Acceptance:** documented; nothing regresses; binding/offline green.

### Task 1.3 — firecrawl-keyless driver (the KNOW/web side) — unlocks 2
**Files:** `knowledge/research-method.md` (new — the keyless web-research method doc); resolve the manifest convention in `tools/manifest.py` / `tools/check-onboarding-binding.py` if needed.
**Build + the design call to make:** the hosted Firecrawl MCP is keyless (no key for `scrape`/`search`/`interact`), but the manifest rule forbids `mcp__…` in a `requires_credential: none` skill's `uses_tools`. Resolve cleanly: a firecrawl app is `requires_credential: none`, `requires_driver: firecrawl`, `data_path: fetch_rest`, and **does NOT list `mcp__firecrawl__…` in `uses_tools`** (it calls them in the body — the binding check's C assertion only forbids *TrustPager* coupling, not firecrawl, so the body is fine). Document this convention in `research-method.md`. Scope-clamp hard: `scrape`/`search`/`interact` ONLY — `crawl`/`map`/`agent`/`extract` need a key and are OUT of floor scope.
**Offline:** firecrawl apps are network → their unit tests mock/skip the fetch and test the synthesis/shape logic. Document the `BOS_OFFLINE` accommodation.
**Acceptance:** the convention is documented + enforced consistently; a firecrawl app can be declared keyless and pass the binding check + manifest rule; offline suite green (network mocked).

---

## Increment 2 — Reasoning-only apps (parallelisable; no driver deps)

> Each is a new (or decoupled) skill: `skills/<name>/SKILL.md` with manifest `function_slot: <slot>`, `requires_driver: none`, `requires_credential: none`, `data_path: reasoning_only` (or `local` if it writes a file via doclib once 1.1 lands). Mirror an existing keyless skill (e.g. `build-brand-strategy`, `extract-document`) for shape. Positive-only on outputs. After building, **promote in starter-projects + start-here** and regenerate the registry.

### Task 2.1 — price-my-work (slot: money) — unlocks 3
The defensible-price win: owner types costs/hours/materials/desired-margin → a clear priced breakdown with margin shown and the assumptions stated. Optional clean `.xlsx` pricing sheet via doclib (1.1). The keyless pricing fallback `quote-from-photo` + `write-a-proposal` both lean on. **Acceptance:** delivers a priced quote from typed inputs with zero accounts; positive-only; gates green.

### Task 2.2 — grill-me-on-this-decision (slot: strategy) — unlocks 1
Locked floor app (D6). The owner describes a decision (hire / price rise / drop a service) → a structured grilling that surfaces the holes, assumptions, and the strongest case each way, ending in a clear recommendation to weigh. Pure reasoning over the decision + the business profile. Pairs with `write-prompt`. **Acceptance:** real pressure-test, not cheerleading; gates green. **Then route it from start-here Step 6 (decision signal) — it becomes a real instant-win again.**

### Task 2.3 — plan-my-content (slot: social) — unlocks 1
THE missing hinge. Reads the brand's `content-pillars.yaml` + `voice.md` (from build-brand-strategy) → a dated 1-2 week multi-channel content plan (what to post, when, where). Horizon clamped (never a 90-day firehose). **Acceptance:** a reviewable dated plan from the pillars; positive-only; gates green.

### Task 2.4 — write-post-copy (slot: social) — unlocks 3
The studios render only the on-image headline; this drafts the caption/body (+ optional ad primary-text/headline) in the owner's voice from a plan row or a standalone brief. Pairs with `make-social-post`. **Acceptance:** publish-ready caption in voice; positive-only; gates green.

### Task 2.5 — write-a-job-ad (slot: people) — unlocks 1
Role description + voice docs → a job ad + screening questions in the owner's voice. Completes the team cluster's before-hire gap (post-hire `onboard-team-member` exists). **Acceptance:** ready-to-post ad + screening Qs; positive-only; gates green.

### Task 2.6 — write-a-policy (slot: people or documents) — unlocks 1
Owner describes how they handle a thing (deposits / cancellations / privacy / funding) + voice docs → clean policy/FAQ text. Pre-feeds `build-knowledge-base-from-docs` on connect. Allied-health funding wording: confirm specifics first, never invent compliance claims. **Acceptance:** clean policy text; positive-only; gates green.

### Task 2.7 — build-customer-voice DECOUPLE to keyless (slot: strategy) — unlocks 3
Currently `mcp`/`trustpager` (pulls live transcripts). Add a keyless path: accept owner-pasted notes / reviews / testimonials (and MarkItDown-read local files once 1.2 is confirmed) instead of `mcp list_transcripts`. The TrustPager transcript auto-pull becomes the connected deepener. It is the documented prerequisite of floor `build-brand-strategy`'s full mode. Reclassify the keyless mode's manifest to `requires_credential: none`, `requires_driver: none` (or `markitdown` if it reads files), `data_path: reasoning_only`/`local`. **Acceptance:** runs keyless from pasted/owner-provided voice; the connected pull still works; gates green; binding check sees it keyless.

---

## Increment 3 — Driver-dependent apps + decouples

### Task 3.1 — write-a-proposal (slot: strategy) — unlocks 1
Consumes `price-my-work` (2.1) output + brand voice (build-brand-strategy) → an on-brand proposal/SOW, emitted as `.docx` via doclib (1.1). Becomes the live signing template on connect. **Hard order:** after 2.1 + 1.1. Positive-only. **Acceptance:** a real .docx proposal keyless; gates green.

### Task 3.2 — build-spreadsheet DECOUPLE (slot: documents) — unlocks 2
Currently `mcp`/`trustpager` (`create_spreadsheet`). Add a keyless standalone path: emit a real local `.xlsx` via doclib (1.1); the live workspace sheet is the connected deepener. **Acceptance:** keyless .xlsx output; CRM path still works on connect; gates green.

### Task 3.3 — import-from-anywhere DECOUPLE (slot: documents) — unlocks 1
Currently `mcp`/`trustpager` (`bulk_create_contacts`). Keyless path: MarkItDown read (1.2) → normalized local `.xlsx`/`.csv` via doclib (1.1); CRM seed only on connect. The natural connect on-ramp. **Acceptance:** clean normalized local list keyless; gates green.

### Task 3.4 — transcript-summary FIX to keyless (slot: comms/documents) — unlocks 1
Currently 100% `trustpager`-coupled. Add a keyless paste/local-file path: MarkItDown-read a transcript/recording file (or pasted text) → summary + decisions + action list; the CRM log is offered only on connect. Closes the floor's "works at zero accounts" gap. **Acceptance:** keyless summary from pasted/local transcript; gates green. **Then route from start-here Step 6 (call→notes signal).**

### Task 3.5 — assemble-content-pack (slot: social/creative) — unlocks 1
Pure local orchestration (reuse the `assemble-pack` pattern): collate an already-produced brief + caption + rendered asset into a clean, named, publish-ready folder. No generation. **Acceptance:** a publish-ready folder from existing files; gates green.

### Task 3.6 — research-a-competitor (slot: research) — unlocks 2
Firecrawl (1.3): one rival URL → a one-page sharp-operator read (positioning, apparent pricing, gaps). `scrape`/`search` only. Network → offline test mocks the fetch. **Acceptance:** a one-page competitor read keyless; gates green (network mocked). **Then route from start-here Step 6 (competitor signal).**

### Task 3.7 — research-before-call (slot: research) — unlocks 1
Firecrawl (1.3), builds on 3.6: a name/company → a one-page pre-meeting brief + 3 sharp questions. Network → mocked offline. **Acceptance:** a pre-call brief keyless; gates green.

---

## Increment 4 — deferred to P6 (named for completeness)
- **make-brand-video + creative-render-driver** — the Remotion bridge. Large, **cross-repo** (`Remotion-VideoStudio`), pin-on (heavy clone+install), requires brand-genericising the RVS promo layer first. This is **P6**, its own phase — NOT built in Wave 1. Tracked in the roster as the one 🆕 that stays planned here.

---

## Definition of done (Wave 1)
- [ ] Increment 1 drivers exist + recognised keyless (`doclib` added to the binding keyless set; firecrawl convention documented + enforced; MarkItDown first-class).
- [ ] Every Increment 2 + 3 app is built/decoupled, genuinely keyless, lints clean, and is OFFERED in onboarding (promoted from Planned in starter-projects; routed from start-here where it fits).
- [ ] `floor-roster.md` statuses updated to ✅ for every shipped win; only make-brand-video remains 🆕 (→ P6).
- [ ] `check-onboarding-binding.py` exits 0; registry fresh; every skill lints clean; secrets + kernel-clean green; `BOS_OFFLINE` suite green (firecrawl fetches mocked).
- [ ] No TrustPager coupling re-enters the floor (the guardrail enforces this every commit).

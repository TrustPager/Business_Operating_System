# Business Operating System — Implementation Roadmap

> **For agentic workers:** This is the PROGRAM plan. Each phase is an independent subsystem with its own detailed bite-sized plan in `docs/architecture/plans/`. Execute one phase at a time via **superpowers:subagent-driven-development** (or executing-plans), each in its own git worktree. Per-phase plans use checkbox (`- [ ]`) steps.

**Goal:** Re-architect BOS from a TrustPager onboarding tool into a platform-agnostic business operating system that thrives with **zero TrustPager** — a thin kernel + swappable drivers + plain-language apps, fronted by a powerful keyless floor.

**Architecture:** A thin vendor-neutral **kernel** (profile/progress schema, generated registry, journal, safety/preflight, transport-neutral `request()`), **drivers** as data + adapters (TrustPager is the deepest, never required), and **apps** = skills carrying manifest frontmatter. Claude's native skill-triggering is the router; the kernel only adds self-awareness (registry) + a connect-on-demand preflight. (`bos-rearchitecture-review.md` §2.)

**Tech stack:** Python stdlib (kernel + tools), Markdown skills + frontmatter manifests, Vite/React/Puppeteer + Remotion (creative, via a bridge to the sibling `Remotion-VideoStudio` repo), the offline test harness (`BOS_OFFLINE`, `lint-skill.py`, `test-skill.py`, `check-no-secrets.py`).

**Source specs (all in `docs/architecture/`, locked):** `founder-decisions.md` · `bos-rearchitecture-review.md` · `skill-extraction-audit.md` · `floor-completion-plan.md` · `native-and-ecosystem-scan.md` · `floor-tool-stress-test.md`.

**Non-negotiables (the gates every phase is measured against):**
- The kernel does NOT change when a driver/app is added.
- The floor works at zero accounts and zero TrustPager.
- Plain-language partner — owners never see "kernel/driver/app/MCP".
- Every default-on app is green under `BOS_OFFLINE` (zero key, zero network).
- MIT-clean: no AGPL/GPL/proprietary code vendored (service/blueprint boundaries documented).
- **Token-frugal per turn:** the connected tier must never flood context. A brand-new owner on a Pro plan must not have their usage burned by tool-loading overhead in the first few turns. The floor loads zero MCP tools by construction; connected-driver loading must be designed (native tool-deferral + OAuth scoping + REST path; gateway/proxy as the planned multi-driver path). See [D10](founder-decisions.md).

---

## Phase overview

| Phase | Subsystem | Depends on | Done-when gate |
|---|---|---|---|
| **P0** | Foundation — split the engine into kernel + TrustPager driver | — | A no-op 2nd driver journals through the kernel without importing TrustPager; all 22 `fetch.py` still run green |
| **P1** | The contract — manifests + generated registry + hardened lint | P0 | `registry.json` generates in CI; lint FAILs on bad manifest/undeclared tool/vendor-literal-in-kernel |
| **P2** | Safety truth — fix the journal, rule the data path, write-approval gate | P0 | Every write (key + MCP) is journaled; stored key is `chmod 0600`; expensive writes gated |
| **P3** | Kernel behavior — onboarding + catalog + connect-on-demand | P1, P2 | `start-here` runs info-dump→win→deepen at zero tools; `whats-possible` reads the registry; preflight remediates, never dead-ends |
| **P4** | The floor — fix, adopt, build | P1, P3 | All default-on floor apps green under `BOS_OFFLINE`; the two adopted libs (firecrawl-keyless, doc-lib-set) wired |
| **P5** | MONEY + people-ops floor | P4 | AU finance + people-ops apps run keyless off a versioned ATO/Fair-Work constants file |
| **P6** | Creative engine — Remotion bridge | P4 | A brand-genericised RVS renders an on-brand MP4/GIF for a non-TrustPager business; `make-brand-video` works pin-on |
| **P7** | TrustPager re-slot + de-brand | P1–P4 | TrustPager lives behind the "unlock" section; user-facing prose vendor-neutral; Xero proves driver #2 |
| **P8** | Install + migration + ship | all | One-command conversational plugin install; existing installs migrate without breakage |

**Status (updated 2026-06-27): P0 ✅, P1 ✅, and P3 (onboarding + catalog) ✅ shipped to `main`.** (P0 = kernel/driver split, 49 tests; P1 = manifest + registry contract, 97 tests; P3 = keyless `start-here` onboarding + `whats-possible` registry catalog + keyless `build-brand-strategy` first-win + `learn-my-business` reframed as the connected deepener + state-gated TrustPager, 60 skills registered, 97 tests.) **P3 remainder deferred:** `connect-a-tool` + `tools/preflight.py` (connect-on-demand) ride on P2's safety work and land with the plumbing phases — the shipped P3 increment is onboarding + the registry-driven catalog.

**Floor-first re-sequence (founder directive — make the day-zero floor the star, not TrustPager).** The P0–P8 numbering stands, but the BUILD ORDER after P1 is re-prioritized to foreground the floor:
1. **P0 ✅ → P1 ✅** — done (the foundation + the data-driven contract that surfaces the floor).
2. **Floor build leads next** — P3 (conversational onboarding) + the floor portions of P4/P5/P6: the keyless day-zero apps (research via Firecrawl, the document tools, brand/content, the location-agnostic MONEY cluster, `grill-me`, `price-my-work`→`write-a-proposal`, the Remotion creative engine) **plus re-pointing the ~37 `floorable` skills toward keyless** (the P1 backfill identified them). This is where the product's value for "anyone" lives.
3. **Then the plumbing** — P2 (safety hardening), P7 (TrustPager re-slot), P8 (install) — *after* the floor is robust.

**P1 follow-ups (inert today; harden before a 2nd connected driver lands):** normalize `review-team-draft`'s bare `uses_tools` names to the `mcp__…` form; tighten the lint MCP-tool regex (hyphenated-UUID server segments) and swap `_driver_owns_tool`'s substring match for an exact `mcp__<driver>__` segment match.

The original spine note still holds mechanically: P0→P3 are sequential; P4/P5/P6 parallelize after P3; P7/P8 close out — the re-sequence just moves the floor ahead of P2/P7 in priority.

---

## P0 — Foundation: split the engine
**Goal:** Separate the vendor-neutral kernel from TrustPager specifics so a second driver is possible without core rot.
**Builds:** `kernel/runtime/` (offline guard, `request()` seam, `journal()`, `ApprovalPending`/202, redaction, profile/progress contracts) + `drivers/trustpager/` (`API_BASE`, `CATALOG_URL`, `tp_live_` resolver, `PATH_OVERRIDES`, cross-catalog bridge, `resolve_path`). `tools/trustpager_api.py` becomes a thin re-export shim. A no-op second driver as the boundary proof.
**Implements:** review P0 #1, migration Steps 0–1. Adopt `CLAUDE_PLUGIN_ROOT`; freeze/retire `PATH_OVERRIDES` + cross-catalog bridge; tag a pre-refactor release.
**Depends on:** — (must come first).
**Done when:** the no-op driver journals a write through the kernel with zero TrustPager imports; all 22 `fetch.py` + `bos-run.py` run unchanged; full offline suite green.
**Detailed plan:** [`plans/2026-06-25-p0-kernel-driver-split.md`](plans/2026-06-25-p0-kernel-driver-split.md)

## P1 — The contract: manifests + registry + lint
**Goal:** Make capability data-driven so growth is additive (drop in a folder), never a kernel edit.
**Builds:** manifest frontmatter on every skill (`function_slot`, `requires_driver`, `requires_credential`, `data_path`, `uses_tools`, `unlocks`, `status`, `reads_for_profile`); `tools/registry-generator.py` → `kernel/registry.json` (CI diff-checked, shipped like a lockfile); `lint-skill.py` promoted WARN→FAIL (resolve_path, unknown manifest keys, undeclared `uses_tools`, vendor literals banned in `kernel/`, key-path writes untagged).
**Implements:** review P0 #2 (partial), P1 #6/#7/#11, founder D6 (pinning = registry activation).
**Depends on:** P0.
**Done when:** registry regenerates deterministically in CI; lint fails the build on any contract violation; a real YAML parse (or unit-tested flat schema) reads manifests.

## P2 — Safety truth: journal + data path + approval gate
**Goal:** Make the "everything is logged / nothing reaches a customer unverified" promise literally true.
**Builds:** `journal_mcp_write()` wired into the 14 MCP-write skills; per-app `data_path` (`reasoning_only`/`fetch_rest`/`mcp_tools`); read-only-vs-tight-lockdown key handling (`chmod 0600` on `bos.json`, rotation note) in `SECURITY.md`; a kernel write-approval gate on expensive/customer-facing actions (warn-and-proceed, dismissible — founder D4).
**Implements:** review P0 #3, P1 #9, founder D2/D4.
**Depends on:** P0.
**Done when:** every write path (key + MCP) appears in the journal; `SECURITY.md` is the single home for key hygiene; expensive actions surface a credit heads-up.

## P3 — Kernel behavior: onboarding + catalog + connect-on-demand
**Goal:** The self-actualizing partner — value before completeness, deepening over time.
**Builds:** `skills/start-here/` (conversation-first onboarding: 60-sec info-dump → instant floor win → rewarded deepening, binge-or-sip, resumable); `skills/whats-possible/` (reads `registry.json` → grouped plain-language catalog + pinning); `skills/connect-a-tool/` + `tools/preflight.py` (driver check → connect tutorial: MCP › CLI › `.env`). Demote `learn-my-business` to a step `start-here` invokes; collapse the four "front door" claims to one.
**Implements:** review P0 #4/#5, P1 #10, founder D6, onboarding decisions (Q3).
**Depends on:** P1, P2.
**Done when:** a brand-new owner with nothing connected completes onboarding and gets a floor win; capability surfacing + connect-on-demand are registry-driven; the kernel is unchanged by adding a driver.

## P4 — The floor: fix, adopt, build
**Goal:** A complete, powerful default-on floor that stands at zero accounts.
**Now roster-defined (founder [D9](founder-decisions.md), 2026-06-27):** the floor is defined by the first-win roster in [`floor-roster.md`](floor-roster.md) and built in its unlock-priority order. **Wave 0 (guardrail + onboarding repair) is the prerequisite to all further floor work** — it binds onboarding to the registry so the surface can never again advertise unbuilt/non-keyless apps (plan: [`plans/2026-06-27-floor-guardrail-and-repair.md`](plans/2026-06-27-floor-guardrail-and-repair.md)). The build list below is the menu the roster draws from.
**Builds:**
- **Fix:** `transcript-summary` gets a keyless paste/local-file path.
- **Adopt (the only two survivors):** wire `firecrawl-keyless` (`scrape`/`search`/`interact` only) as the KNOW driver; vendor the **doc-lib-set** (`openpyxl`, `python-docx`, `pdfplumber`, `reportlab` core; `OCRmyPDF` gated behind one-time install preflight; `python-pptx` on-demand) as `tools/` Bash wrappers; name MarkItDown + the render engine as first-class keyless drivers.
- **Build MUST apps:** `grill-me-on-this-decision`, `price-my-work`, `write-a-proposal`, `research-a-competitor`, `research-before-call`, `plan-my-content`, `write-post-copy`.
- **Promote:** `build-customer-voice` (prerequisite of the floor `build-brand-strategy`), `import-from-anywhere`, `build-spreadsheet`.
- **Demote:** `make-thumbnail` → pinnable.
**Implements:** floor-completion-plan §1–§3/§5, stress-test survivors + cuts, skill-audit floor.
**Depends on:** P1, P3.
**Done when:** every default-on floor app is green under `BOS_OFFLINE`; the brand→content and price→proposal loops run end-to-end with nothing connected.

## P5 — MONEY + people-ops floor
**Goal:** Close the department gaps the org-chart review surfaced, keylessly — **location-agnostic core, regional specificity opt-in** (founder D7).
**Builds:**
- **Location-agnostic core (universal business math):** `cash-flow-forecast`, `profit-per-job`, `expense-sense`, budgeting/margin. Work for any business, any country, with no region set.
- **Regional pack (a swappable data module selected at onboarding; AU ships first + complete):** `estimate-my-bas` (Simpler-BAS G1/1A/1B), GST/super/PAYG off a versioned **ATO/Fair-Work constants** file. Region-specific apps only surface once a region is set in the profile — *same activation model as a driver* (region = swappable module, AU = default-shipped, others stub in on demand). **Prepare figures, never lodge.**
- **People-ops:** `write-a-job-ad`, `write-a-policy`, `renewal-tracker` (license/insurance/cert expiry).
- Positive-only-language enforced on every customer-facing-copy app; regional framing comes from the locale module, never hardcoded.
**Implements:** department-gap analysis, floor-completion §2, stress-test (au-gov-data → constants file, not a live driver).
**Depends on:** P4.
**Done when:** AU finance + people-ops apps run keyless and green; constants file is FY-versioned with an update note.

## P6 — Creative engine: Remotion bridge
**Goal:** Brand video + GIFs + ads for paid & organic, on-brand by default, keyless-local.
**Builds:** **first** brand-genericise the RVS promo layer (a `brand.js` the bridge populates — without this it renders TrustPager teal for a plumber); then `tools/video-bridge.py` (locate/clone RVS, sync `brand.json`, write spec, shell `npx remotion render`), `studio/video/` spec layer, and apps `make-brand-video`/`make-a-gif`/`make-an-ad`/`branded-post-set`/`video-from-template`; plus a Bash+FFmpeg post-production skill (blueprinted from the cut `mcp-video`). All `.tsx` stays in RVS (hard rule).
**Implements:** floor-completion §4 (founder priority), stress-test (FFmpeg as blueprint not dependency).
**Depends on:** P4. **Touches the sibling `Remotion-VideoStudio` repo** — coordinate the genericise change there.
**Done when:** a non-TrustPager business renders an on-brand MP4 + GIF; `make-brand-video` works pin-on with a clone+install preflight.

## P7 — TrustPager re-slot + de-brand
**Goal:** TrustPager becomes the deepest optional driver, not the center; the product reads as platform-agnostic.
**Builds:** move TrustPager behind the "connect this — here's what it unlocks" section; de-brand user-facing prose (README/INSTALL/onboarding); move `templates/CLAUDE.md` "About TrustPager" → `drivers/trustpager/about.md`; wire **Xero as exemplar driver #2** (the cross-driver proof — if the model can't express `sync-from-xero` cleanly, the model is wrong). Infra strings stay byte-identical (frozen).
**Implements:** review migration Steps 5–6, founder D3.
**Depends on:** P1–P4.
**Done when:** the floor + catalog never name TrustPager unprompted; Xero slots in as a driver with no kernel change.

## P8 — Install + migration + ship
**Goal:** Brain-dead-simple, one-command conversational install; existing clients migrate cleanly.
**Builds:** plugin-only install (owner tells Claude → fetch public repo → install → initialize → walkthrough); adopt `CLAUDE_PLUGIN_ROOT`; retire the `bos.json`/`bos-run.py`/launcher dual-install seam; `tools/migrate-install.py` (idempotent on first pull); recommend existing clients redownload.
**Implements:** founder D1/D5, review open-decision 1.
**Depends on:** all.
**Done when:** a non-technical owner installs in one conversational step and reaches a floor win; existing installs upgrade without manual fixes.

---

## Execution model
- **One worktree per phase** (superpowers:using-git-worktrees), each producing working, testable software before merge.
- **Plan-review before execute:** each per-phase plan goes through a plan-document-reviewer pass before coding.
- **Subagent-driven execution:** fresh subagent per task + two-stage review (superpowers:subagent-driven-development).
- **The Remotion phase (P6) spans two repos** — the genericise change lands in `Remotion-VideoStudio`; BOS only ships the bridge.
- **Every phase ends green in the offline harness** — that IS the definition of "zero-credential floor."

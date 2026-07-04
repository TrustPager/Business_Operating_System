# Site Builder Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking. Run this in a dedicated git worktree.

**Goal:** Ship `design-my-site` (keyless floor skill that builds a bespoke, high-converting, findable page/site locally by steering Claude Design) and `launch-my-site` (Tier-1 shelf skill that deploys it to Vercel), reusing `get-found-online` for SEO.

**Architecture:** BOS is the conversion + uniqueness engine that drives Claude Design. A committed lean Next.js starter (`templates/site-starter/`) carries the wireframe skeleton + a design-system layer; the floor skill derives a unique design system from the owner's taste + reference sites, inlines it into an instantiated copy of the starter, and steers Claude Design (design-system-first) to build off its house style; the shelf skill deploys via the Vercel CLI. Method IP lives in one knowledge file. Full design spec: [../2026-07-03-site-builder-design.md](../2026-07-03-site-builder-design.md).

**Tech Stack:** Python (manifest/driver/registry tooling, unittest offline suite), Next.js + Tailwind (the starter), Claude Design (`/design-sync`, web-capture, Handoff to Claude Code), Vercel CLI, Firecrawl (via delegation to `research-a-competitor` / `get-found-online`).

**Source-of-truth note on altitude:** the spec (§3, §5, §6) and the method file (Task 1.1) own the *content* (the seven-section skeleton, the steering playbook, the copy rules). This plan owns the *mechanics* (exact files, frontmatter, commands, tests, gates). Where a task says "author per the method file," the executor writes the prose/components against the spec + method file rather than inlined-here copy; where a task shows code (manifest edit, driver, frontmatter, the inlining helper, tests), it is complete.

**Validation doctrine (from the codebase):** reasoning-heavy skills are validated by a scripted **Sonnet dogfood** (the pass bar), not by unit tests, exactly as `get-found-online` was (5/5). Code artifacts (the manifest change, the `vercel` driver, the starter build, any Python/Node helper) get real offline tests run with `BOS_OFFLINE=1`. Every phase ends by running the CI-order gates.

**CI-order gates (run after each phase; all must pass):**
```bash
BOS_OFFLINE=1 python tools/check-no-secrets.py
BOS_OFFLINE=1 python tools/check-kernel-clean.py
BOS_OFFLINE=1 python tools/check-doctrine-voice.py
BOS_OFFLINE=1 python tools/check-connectors.py           # connected-add-on gate (Phase 2: launch-my-site + drivers/vercel)
BOS_OFFLINE=1 python tools/registry-generator.py --check
BOS_OFFLINE=1 python tools/export-capabilities.py --check
BOS_OFFLINE=1 python tools/check-onboarding-binding.py
for d in skills/design-my-site skills/launch-my-site; do python tools/lint-skill.py "$d"; done
BOS_OFFLINE=1 python -m unittest discover -s tests -v
```

---

> **Execution status (2026-07-04): IMPLEMENTED.** Built on `feat/site-builder-reconcile` (`74146c6..1912136`), all tasks done, all gates green (379 tests, 0 failures), design-my-site dogfood 6/6, final review ready-to-merge. Residual live validations (owner/account needed): a multi-page dogfood + a live Vercel deploy dogfood. History of the hold below.
>
> **Execution status (2026-07-04): HOLD LIFTED, reconciliation folded.** The 2026-07-03 hold (waiting on a forthcoming Meta-ads skill so the two would share one intake pattern) is resolved. That skill shipped as the **Tier-1 Connected Add-on Kit** ([`../tier-1-addon-kit.md`](../tier-1-addon-kit.md)), with `plan-my-ads` + `run-my-ads` as its reference and the guided **Source A/B/C/D intake** as its fill-out. This plan has been reconciled with the shipped kit: `design-my-site` adopts the Source A/B/C/D intake (Task 1.4), and `launch-my-site` conforms to the kit (`keyed_cli` docs-only driver, one-home `connect.md` + `connectors.md` card + labelled `connect-a-tool` exception, OPERATING-CONTEXT fold-in, Hard-rules-first deploy safety with no CI grep). Execution may proceed.

## File Structure

**New files:**
- `knowledge/web-design-method.md` — the whole method: conversion skeleton, site IA, on-page SEO wiring, Claude Design steering playbook. Links out to `seo-method.md`, `business-method.md` §10.5, `marketing-strategy-method.md`, `communication-voice.md`.
- `templates/site-starter/` — committed lean Next.js app (see Task 1.2 for its internal tree).
- `skills/design-my-site/SKILL.md` — the floor skill (gate-led body).
- `skills/design-my-site/inline_design_system.py` — scaffold helper: reads `brand/brand.json` + the derived token overrides (from `~/.claude/bos-cache/site-builder-profile.json`), writes a self-contained `tokens.css` + `design-system.json` into an instantiated project copy (so it does not depend on the in-repo `../../../brand` path once copied out). Unit-tested.
- `skills/launch-my-site/SKILL.md` — the shelf skill (deploy).
- `drivers/vercel/__init__.py` — **documentation-only `keyed_cli` driver**, mirroring `drivers/meta-ads/__init__.py`: a top-level `DRIVER` dict + a "DOCUMENTATION ONLY" docstring, NOT a `DriverConfig`. No `auth.py`, no `catalog.py`, no key resolver, no import of `kernel.runtime.*`. The `DRIVER` dict: `{"id":"vercel", "kind":"keyed_cli", "display_name":"Vercel", "cli":"vercel", "connect_doc":"connect.md", "credential":"key", "secret_pattern":"<vercel token regex>"}`. No `never_call`/`never_set` (a CLI deploy has no quiet live-switch; the one explicit switch is guarded by the skill's Hard rules, see Task 2.4). This is the reference `keyed_cli` driver the kit's taxonomy names.
- `drivers/vercel/connect.md` — the single home for the Vercel connect steps (meta-ads `connect.md` shape). See Task 2.3b.
- `drivers/vercel/OPERATING-CONTEXT.md` — the operating context the skill folds into `./CLAUDE.md` on connect (meta-ads `OPERATING-CONTEXT.md` shape). See Task 2.4.
- `tests/test_inline_design_system.py` — offline unit tests for the inlining helper.
- `tests/test_vercel_driver.py` — offline test: `drivers.vercel` imports clean, exposes a `DRIVER` dict with `kind=='keyed_cli'` and `credential=='key'`, and importing it pulls in no other vendor.

**Modified files:**
- `tools/manifest.py` — add `deploy` to `FUNCTION_SLOTS`.
- `docs/architecture/manifest-schema.md` — mirror the new `deploy` slot (not CI-checked; manual sync).
- `knowledge/connectors.md` — add a `## Vercel (put your site live)` card (meta-ads card schema). Required for `check-connectors.py` conformance (the gate prefix-matches the driver's `display_name` to a card heading). See Task 2.5.
- `skills/connect-a-tool/SKILL.md` — add a labelled "Exception, Vercel" in Step 3 and the Hard rules, parallel to the existing "Exception, Meta Ads", pointing at `drivers/vercel/connect.md` as the single home for the steps. See Task 2.3b.
- `knowledge/starter-projects.md` — add `design-my-site` as a `[live]` + keyless row (market/win-work group); add `launch-my-site` as a connected doorway row tagged `needs_connection` (NOT keyless, NOT a CRM tag).
- `knowledge/business-method.md` (or `knowledge/connectors.md`) — add the one-home statement of the reusable connect-doorway articulation ("Here is X you can do keyless; it becomes enhanced by Y, which you unlock with Z"). Decide the single home during Task 2.5.
- `kernel/registry.json` — regenerated (never hand-edited).
- `docs/CAPABILITIES.md` — regenerated by `export-capabilities.py`.
- `.gitignore` — ensure `templates/site-starter/node_modules/` and `.next/` are ignored (root ignores of `node_modules/` likely already cover it; verify).

**Do NOT touch:** `skills/whats-possible/SKILL.md` (runtime registry reader), `kernel/registry.json` by hand.

---

## Phase 1 — `design-my-site` (the keyless floor win, shippable on its own)

Phase 1 delivers a complete win with zero dependency on Phase 2: the owner gets a bespoke page running on localhost. It requires no schema change and no Vercel.

### Task 1.1: The method file `knowledge/web-design-method.md`

**Files:**
- Create: `knowledge/web-design-method.md`

- [ ] **Step 1: Author the file** against spec §3 and §7, in four parts, each linking out rather than restating:
  - *Conversion skeleton* (spec §3a): the seven sections (Hero, Trust bar, Benefits, How-it-works, Social proof, FAQ, Final CTA), each with its job, why it converts, positive-only copy guidance, and its on-page SEO role. Plus the nine ordering principles.
  - *Site layer / IA* (spec §3b): the page set (Home, Services hub, Service pages, Service-Area pages, About, Reviews, Contact, optional Blog), nav/footer/internal-linking rules, and the per-page rule (treat every page as a landing page; Core Web Vitals + speed-to-lead constraints).
  - *On-page SEO wiring* (spec §7): link to `knowledge/seo-method.md` for the checklist and `business-method.md` §10.5 for the local gravity-stack gate. State the "one artifact, both outcomes" rule and the local-first discipline. Do not duplicate the SEO checklist.
  - *Claude Design steering playbook* (spec §3c): the design-system-first levers (attach a real design system; literal hex/typeface/radius tokens; verify the font `@import` loads; named design-movement anchor; density on the first prompt; negative-prompt each default paired with its replacement; component-level rules; reference web-captures with the layer-override; refine via Tweaks sliders + fresh sessions), the ten-part art-direction brief structure, and the anti-patterns list.
  - End with the positive-only + no-em-dash output rule (as `seo-method.md` does).
- [ ] **Step 2: Verify voice + links.** Run:
  ```bash
  BOS_OFFLINE=1 python tools/check-doctrine-voice.py
  ```
  Expected: `OK: doctrine voice clean (tracked files).` Manually confirm every cross-reference path resolves (`seo-method.md`, `business-method.md`, `marketing-strategy-method.md`, `communication-voice.md`).
- [ ] **Step 3: Commit.**
  ```bash
  git add knowledge/web-design-method.md
  git commit -m "feat(site-builder): web-design-method — conversion + IA + SEO + Claude Design steering"
  ```

### Task 1.2: The committed lean Next.js starter `templates/site-starter/`

**Files (create the tree):**
- `templates/site-starter/package.json` — pinned Next.js + Tailwind + React; scripts `dev` (port 3220 to avoid the studio ports 3210/3213/3216/3217), `build`, `start`, `lint`.
- `templates/site-starter/next.config.js`, `tailwind.config.js`, `postcss.config.js`, `tsconfig.json` (or `jsconfig.json`).
- `templates/site-starter/app/layout.tsx` — root layout: metadata API defaults, font `<link>` wiring (Task-1.1 rule: the font must actually load), the design-system `tokens.css` import, shared Nav + Footer for the site case.
- `templates/site-starter/app/page.tsx` — the landing page composed of the section components in skeleton order.
- `templates/site-starter/components/sections/` — the seven section components (`Hero`, `TrustBar`, `Benefits`, `HowItWorks`, `SocialProof`, `Faq`, `FinalCta`) + `Nav`, `Footer`. Each is a real, buildable component reading design tokens as CSS variables, and each carries a first-line `{/* @dsCard group="sections" */}` marker so Claude Design's Design System pane indexes it into `_ds_manifest.json`. (The spec §6 shows this marker as an HTML comment `<!-- @dsCard ... -->`; inside a `.tsx` component use the JSX comment form shown here, never a raw HTML comment.)
- `templates/site-starter/components/seo/` — JSON-LD components (`LocalBusinessJsonLd`, `ServiceJsonLd`, `FaqJsonLd`, `ReviewJsonLd`).
- `templates/site-starter/styles/tokens.css` — the design-system tokens as CSS variables (the in-repo default reads from `brand/brand.json` via a generated file; see Task 1.4 helper). Ships with sensible neutral defaults so the app builds standalone.
- `templates/site-starter/.gitignore` — `node_modules/`, `.next/`, `out/`.
- `templates/site-starter/README.md` + `templates/site-starter/CLAUDE.md` — mirror the studio docs pattern (what it is, how the skill instantiates it, how `/design-sync` attaches to it).

- [ ] **Step 1: Scaffold the tree** with the files above. Keep it lean: only our components + a thin app shell. Pin exact dependency versions in `package.json`.
- [ ] **Step 2: Verify it builds offline.** Run:
  ```bash
  cd templates/site-starter && npm install && npm run build
  ```
  Expected: a clean production build, no network beyond the npm install. Then `npm run dev` and confirm the page renders the seven sections at `http://localhost:3220`.
- [ ] **Step 3: Verify hygiene.** Run `git status` in the repo root; confirm `templates/site-starter/node_modules/` and `.next/` are ignored (add to root or local `.gitignore` if they appear). Run:
  ```bash
  git ls-files | grep 'templates/site-starter/node_modules/' || echo "clean: node_modules not tracked"
  BOS_OFFLINE=1 python tools/check-no-secrets.py
  ```
  Expected: node_modules not tracked; no-secrets passes. Note: `check-kernel-clean.py` scans only `kernel/**/*.py`, so it never inspects `templates/` and is not the relevant guard here. The real guard is `check-no-secrets.py`, which rglobs the repo (skipping `node_modules`): confirm the starter ships no example tokens/keys in tracked files (no placeholder `VERCEL_TOKEN=...` in a committed `.env`, use `.env.example` with empty values if needed).
- [ ] **Step 4: Commit** (source only, not `node_modules`/`.next`).
  ```bash
  git add templates/site-starter/package.json templates/site-starter/*.js templates/site-starter/*.json templates/site-starter/app templates/site-starter/components templates/site-starter/styles templates/site-starter/.gitignore templates/site-starter/README.md templates/site-starter/CLAUDE.md
  git commit -m "feat(site-builder): committed lean Next.js starter (wireframe skeleton + design-system layer)"
  ```

### Task 1.3: The scaffold helper `inline_design_system.py` (TDD)

This is the piece that makes the starter self-contained once copied into the owner's workspace: it reads `brand/brand.json` + the skill's derived token overrides (which the skill persists to `~/.claude/bos-cache/site-builder-profile.json`, the intake profile from Task 1.4) and writes a standalone `styles/tokens.css` + `design-system.json` into the instantiated project, so nothing depends on the in-repo `../../../brand` path after copy-out. The helper stays a pure function taking `brand` + `overrides` as args (see the test); the skill body is what reads them from the profile before calling it.

**Files:**
- Create: `skills/design-my-site/inline_design_system.py`
- Test: `tests/test_inline_design_system.py`

- [ ] **Step 1: Write the failing test.**
```python
"""Offline-safe: no network, no key. Run: BOS_OFFLINE=1 python -m unittest tests.test_inline_design_system"""
import json, sys, tempfile, unittest
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "skills" / "design-my-site"))
import inline_design_system as ids

class TestInline(unittest.TestCase):
    def test_writes_self_contained_tokens(self):
        with tempfile.TemporaryDirectory() as d:
            proj = Path(d)
            (proj / "styles").mkdir()
            brand = {"colors": {"primary": "#1A2B6D", "accent": "#E84545", "pageBg": "#F8F8F6", "text": "#111111"},
                     "fonts": {"primary": "DM Sans", "serif": "Syne"}}
            overrides = {"radius": {"sm": "2px", "md": "4px", "full": "0px"}, "colors": {"accent": "#0EA5A0"}}
            ds = ids.inline(proj, brand=brand, overrides=overrides)
            css = (proj / "styles" / "tokens.css").read_text()
            self.assertIn("--color-primary: #1A2B6D", css)          # brand token carried through
            self.assertIn("--color-accent: #0EA5A0", css)           # override wins over brand
            self.assertIn("--radius-full: 0px", css)                # radius pinned (anti-sameness)
            self.assertNotIn("../../../brand", css)                 # self-contained, no repo path
            self.assertEqual(ds["colors"]["accent"], "#0EA5A0")     # returns the merged system
            self.assertTrue((proj / "design-system.json").exists()) # machine copy for /design-sync
```
- [ ] **Step 2: Run it, verify it fails.**
  ```bash
  BOS_OFFLINE=1 python -m unittest tests.test_inline_design_system -v
  ```
  Expected: FAIL (module or `inline` not defined).
- [ ] **Step 3: Implement `inline_design_system.py`** — a pure function `inline(project_dir, brand, overrides)` that deep-merges `overrides` over `brand`, writes `styles/tokens.css` (CSS variables for colours, fonts, and the full radius scale) and `design-system.json` into `project_dir`, and returns the merged design system dict. No network, no key reads.
- [ ] **Step 4: Run the test, verify it passes.**
  ```bash
  BOS_OFFLINE=1 python -m unittest tests.test_inline_design_system -v
  ```
  Expected: PASS.
- [ ] **Step 5: Commit.**
  ```bash
  git add skills/design-my-site/inline_design_system.py tests/test_inline_design_system.py
  git commit -m "feat(site-builder): inline_design_system helper — self-contained tokens on instantiate"
  ```

### Task 1.4: The `design-my-site` skill body

**Files:**
- Create: `skills/design-my-site/SKILL.md`

- [ ] **Step 1: Write the frontmatter** (studio-class keyless, matches `make-thumbnail`):
```yaml
---
name: Design My Site
description: A bespoke, high-converting landing page or website built from the sites you admire and your own taste, running on your machine in a sitting. On-brand, findable, and unmistakably yours, not a template. No accounts needed to build it.
triggers:
  - design my site
  - build my website
  - build a landing page
  - make a website
  - i want a website like
  - design a page that converts
function_slot: creative
requires_driver: render
requires_credential: none
data_path: local
status: active
---
```
- [ ] **Step 2: Write the gate-led body** against spec §5a, referencing `knowledge/web-design-method.md` throughout so the body stays lean. Steps 1-2 adopt the shipped **Source A/B/C/D intake** (kit §6, worked example `run-my-ads` Step 1), so this skill and the ads add-on share one intake shape:
  1. *Make it yours — the Source A/B/C/D intake.* Read the profile first (`~/.claude/bos-cache/site-builder-profile.json`); if it exists, load it and skip ahead. If absent, run the intake once:
     - **Source A — read `brand/brand.json` silently:** business name, colours, logo, voice, tagline. Read, never copied into the profile (brand's one home is `brand/brand.json`).
     - **Source B — read `./CLAUDE.md` silently:** business shape, offer, region (only if a `Region:` line is explicitly set, never inferred), diagnosed constraint, goal.
     - **Source C — ask only the small site-specific bucket (the ONLY interview):** landing page vs multi-page site and the one action each page drives; 2-5 reference sites they admire and what they like about each; taste and anti-taste.
     - **Source D — no live account read (this add-on is keyless).** Source D here is the delegated reference-site research in Step 2.3-below: it auto-fills the profile to CONFIRM in words, never a fifth question set.
     - **Write the profile** to `~/.claude/bos-cache/site-builder-profile.json` (outside the repo, so updates never touch it; no `.gitignore` entry needed). Brand fields are read from `brand/brand.json`, never copied in.
  2. *Source D — research the references (delegate, keyless).* Delegate the reference read to `research-a-competitor` and the target-term winnability read to `get-found-online`'s SERP spot-check. Auto-fill the profile from what comes back and confirm it in words. Do NOT call `mcp__`/firecrawl tools directly (keeps the manifest clean).
  3. *Derive:* a unique design system (tokens + radius pinned + type pairing + section treatments) + the ten-part art-direction brief + the real, positive-only, on-page-SEO-correct copy for the seven-section skeleton (site: IA first, then home/primary page fully, rest iterative). Persist the derived design overrides into the profile JSON.
  4. *Scaffold:* copy `templates/site-starter/` into the owner's workspace; run `inline_design_system.py`, which reads the derived overrides from the profile JSON, to write self-contained `tokens.css` + `design-system.json`.
  5. *Steer Claude Design:* hand the owner the brief to paste, which sites to web-capture (+ the layer-override), and `/design-sync` to attach the inlined design system.
  6. *Land + view:* Handoff to Claude Code into the copied project; `cd` there, `npm install` + `npm run dev` (port 3220), open `http://localhost:3220` for the owner. Install/run the studio for them; never ask them to.
  7. *Close:* name `launch-my-site` (deploy) and `get-found-online` (live audit) as the next doors, reactive and outcome-only.
  - Include a **Hard rules** section: keyless (no `mcp__`, no direct firecrawl), positive-only + no em dashes in emitted copy, never fabricate testimonials/numbers, bounded first win (one page live locally, not a whole site in one sitting), and **personalization is DATA, never a forked skill file** (kit §6): per-owner detail lives in the profile JSON; never template or copy this skill file per owner.
- [ ] **Step 3: Lint.**
  ```bash
  python tools/lint-skill.py skills/design-my-site
  ```
  Expected: exit 0 (no `[FAIL]`; a triggers-count WARN is acceptable but we have 6).
- [ ] **Step 4: Commit.**
  ```bash
  git add skills/design-my-site/SKILL.md
  git commit -m "feat(site-builder): design-my-site skill (keyless, studio-class, steers Claude Design)"
  ```

### Task 1.5: Register + onboard `design-my-site`

**Files:**
- Modify: `knowledge/starter-projects.md`
- Regenerate: `kernel/registry.json`, `docs/CAPABILITIES.md`

- [ ] **Step 1: Add the onboarding row** to `knowledge/starter-projects.md` under the market / win-work group: a `[live]` + `keyless` row with an outcome-led pitch, skill-id in backticks. Do NOT tag it `better_with_crm`/`needs_crm` (it is genuinely keyless).
- [ ] **Step 2: Regenerate the registry + capabilities.**
  ```bash
  BOS_OFFLINE=1 python tools/registry-generator.py
  BOS_OFFLINE=1 python tools/export-capabilities.py
  grep -n "design-my-site" kernel/registry.json
  ```
  Expected: `design-my-site` present with `requires_credential: none`, `requires_driver: render`, `function_slot: creative`.
- [ ] **Step 3: Run the onboarding-binding + freshness gates.**
  ```bash
  BOS_OFFLINE=1 python tools/check-onboarding-binding.py
  BOS_OFFLINE=1 python tools/registry-generator.py --check
  BOS_OFFLINE=1 python tools/export-capabilities.py --check
  ```
  Expected: all exit 0 (assertion B passes because the skill is keyless-marked).
- [ ] **Step 4: Commit.**
  ```bash
  git add knowledge/starter-projects.md kernel/registry.json docs/CAPABILITIES.md
  git commit -m "feat(site-builder): register + onboard design-my-site (keyless win)"
  ```

### Task 1.6: Phase-1 gates + Sonnet dogfood

- [ ] **Step 1: Run the full CI-order gate block** (see header). All exit 0.
- [ ] **Step 2: Dogfood on Sonnet** (the pass bar, mirroring `get-found-online`). Scenario: a local tradie who names two admired sites and wants a landing page. Pass bar:
  - the brief yields a *distinct* art direction (radius pinned, real font import, negative-prompts paired with replacements, not the Claude beige/serif house look);
  - the copy is positive-only, no em dashes, and on-page-SEO-correct (single H1 as the benefit-keyword, FAQ block, JSON-LD);
  - the local gravity-stack discipline holds (answer speed + reviews are not traded for keywords);
  - the starter is instantiated with self-contained tokens and the local host view runs at `localhost:3220`;
  - no deploy logic leaks into this skill.
  - Then a second dogfood on the multi-page path (home + one service page + IA). Record results in the spec's validation note, fold any fixes, re-run gates.

---

## Phase 2 — `launch-my-site` (Tier-1 shelf deploy) + the schema/driver foundations it needs

Phase 2 is only reached once Phase 1 is green. Its foundations (the `deploy` slot, the `vercel` driver) exist solely for this skill, which is why they live here, not before Phase 1.

### Task 2.1: Vercel connection mechanism (settled — record the rationale)

- [ ] **Step 1: Record the settled choice** (founder-settled, reconciled with the kit 2026-07-04): the **Vercel CLI** invoked via Bash (`vercel deploy`, `vercel deploy --prod`), with account auth via `vercel login` / a `VERCEL_TOKEN` → `requires_credential: key`, `data_path: local`, driver kind `keyed_cli`. The rationale, mirroring the kit's two connected kinds: **meta-ads = `mcp` because it is a hosted-OAuth MCP (the `claude_mcp` kind); vercel = `key` because it is a keyed local CLI (the `keyed_cli` kind) — the `claude_mcp` pattern does NOT apply, and vercel is the reference `keyed_cli` driver the taxonomy names.** No Vercel MCP. The rest of Phase 2 builds to CLI + `key` + `keyed_cli`.

### Task 2.2: Add the `deploy` function_slot (TDD)

**Files:**
- Modify: `tools/manifest.py` (the `FUNCTION_SLOTS` frozenset)
- Modify: `docs/architecture/manifest-schema.md`
- Test: `tests/test_manifest_deploy_slot.py`

- [ ] **Step 1: Write the failing test.**
```python
"""Offline-safe: no network, no key. Run: BOS_OFFLINE=1 python -m unittest tests.test_manifest_deploy_slot"""
import sys, unittest
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import manifest

class TestDeploySlot(unittest.TestCase):
    def test_deploy_is_a_valid_function_slot(self):
        self.assertIn("deploy", manifest.FUNCTION_SLOTS)
    def test_deploy_manifest_validates(self):
        meta = {"function_slot": "deploy", "requires_driver": "vercel",
                "requires_credential": "key", "data_path": "local", "status": "active"}
        errors = manifest.validate_manifest(meta)
        self.assertEqual(errors, [])
```
- [ ] **Step 2: Run it, verify it fails.** `BOS_OFFLINE=1 python -m unittest tests.test_manifest_deploy_slot -v` → FAIL.
- [ ] **Step 3: Add `"deploy"`** to the `FUNCTION_SLOTS` frozenset in `tools/manifest.py`, and add a `deploy` row to the `function_slot` table in `docs/architecture/manifest-schema.md` (the doc is a manual mirror; code wins but keep them synced).
- [ ] **Step 4: Run it, verify it passes.** Expected: PASS.
- [ ] **Step 5: Commit.**
  ```bash
  git add tools/manifest.py docs/architecture/manifest-schema.md tests/test_manifest_deploy_slot.py
  git commit -m "feat(site-builder): add 'deploy' function_slot (manifest.py + schema doc + test)"
  ```

### Task 2.3: The `vercel` driver — documentation-only `keyed_cli` (TDD)

Mirror `drivers/meta-ads/__init__.py`'s declarative style, NOT a keyed-REST `DriverConfig`. Nothing in BOS imports or reads this module; the load-bearing artifacts are the `requires_driver: vercel` string on `launch-my-site`, `connect.md`, and the `connectors.md` card (kit §3). Clone the shape from `drivers/_template/__init__.py` (the `keyed_cli` branch: keep `cli`, drop `server_url`, add `secret_pattern`).

**Files:**
- Create: `drivers/vercel/__init__.py`
- Test: `tests/test_vercel_driver.py`

- [ ] **Step 1: Write the failing test.**
```python
"""Offline-safe: no network, no key. Run: BOS_OFFLINE=1 python -m unittest tests.test_vercel_driver"""
import importlib, sys, unittest
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

class TestVercelDriver(unittest.TestCase):
    def test_exposes_keyed_cli_driver_dict(self):
        mod = importlib.import_module("drivers.vercel")
        self.assertTrue(hasattr(mod, "DRIVER"))
        self.assertEqual(mod.DRIVER["kind"], "keyed_cli")
        self.assertEqual(mod.DRIVER["credential"], "key")
    def test_pulls_in_no_other_vendor(self):
        for m in [m for m in list(sys.modules) if m.startswith("drivers.")]:
            del sys.modules[m]
        importlib.import_module("drivers.vercel")
        self.assertNotIn("drivers.trustpager", sys.modules)  # boundary: no cross-vendor import
```
- [ ] **Step 2: Run it, verify it fails.** → FAIL (module not found).
- [ ] **Step 3: Implement `drivers/vercel/__init__.py`** — a documentation-only driver mirroring `drivers/meta-ads/__init__.py`: a top-level `DRIVER` dict and a "DOCUMENTATION ONLY" docstring stating plainly that nothing reads this module. The dict:
  ```python
  DRIVER = {
      "id": "vercel",
      "kind": "keyed_cli",
      "display_name": "Vercel",
      "cli": "vercel",                 # the local CLI invoked via Bash (NOT a server_url)
      "tool_prefix": "mcp__vercel__",  # unused (the skill shells the CLI); kept for shape parity
      "connect_doc": "connect.md",
      "credential": "key",
      "read_only_scope_first": True,
      "secret_pattern": r"<vercel token regex>",  # for redaction; a Vercel token is ~24 alnum chars
  }
  ```
  **No `DriverConfig`, no `auth.py`, no `catalog.py`, no key resolver, no import of `kernel.runtime.*`** (that transport shape is for keyed-REST drivers like `trustpager`). **No `never_call`/`never_set`** — a CLI deploy has no quiet live-switch; the single explicit `vercel --prod` switch is guarded by the skill's Hard rules (Task 2.4), so the connector gate's safety scan is a no-op for this driver by construction.
- [ ] **Step 4: Run it, verify it passes.** Also run the existing boundary test to be safe: `BOS_OFFLINE=1 python -m unittest tests.test_driver_boundary tests.test_vercel_driver -v` → PASS.
- [ ] **Step 5: Commit.**
  ```bash
  git add drivers/vercel/__init__.py tests/test_vercel_driver.py
  git commit -m "feat(site-builder): documentation-only keyed_cli vercel driver (DRIVER dict + secret_pattern)"
  ```

### Task 2.3b: `drivers/vercel/connect.md` + the labelled connect-a-tool exception

The connect steps have exactly one home: `drivers/vercel/connect.md` (kit §4). Every other surface points at it, never restates it.

**Files:**
- Create: `drivers/vercel/connect.md`
- Modify: `skills/connect-a-tool/SKILL.md`

- [ ] **Step 1: Author `drivers/vercel/connect.md`** in the meta-ads `connect.md` shape (clone `drivers/_template/connect.md`, `keyed_cli` branch):
  - **What this unlocks** — your site on a real, shareable URL.
  - **The honest boundary** — one browser sign-in only the owner can do; the system does everything else; never asks for a password or code.
  - **Step 1: add the Vercel CLI + `vercel login` (permission first)** — the system installs the CLI and runs `vercel login` for the owner on their machine.
  - **Step 2: the owner signs in** — the browser opens Vercel's sign-in; the owner approves.
  - **Step 3: verify** — one lightweight read, `vercel whoami`, proves it is live.
  - **Step 4: deploy a preview** — `vercel` (preview) first; production only on approval (points at `launch-my-site`).
- [ ] **Step 2: Add the labelled "Exception, Vercel"** to `skills/connect-a-tool/SKILL.md` in Step 3 and the Hard rules, parallel to the existing "Exception, Meta Ads": label it "this overrides the usual in-app `/mcp` flow because Vercel is a keyed CLI the system installs and runs `vercel login` for," and point at `drivers/vercel/connect.md` as the single home for the steps (do not repeat them).
- [ ] **Step 3: Voice check + commit.**
  ```bash
  BOS_OFFLINE=1 python tools/check-doctrine-voice.py
  git add drivers/vercel/connect.md skills/connect-a-tool/SKILL.md
  git commit -m "feat(site-builder): vercel connect.md (single home) + labelled connect-a-tool exception"
  ```

### Task 2.4: The `launch-my-site` skill body + `drivers/vercel/OPERATING-CONTEXT.md`

**Files:**
- Create: `skills/launch-my-site/SKILL.md`
- Create: `drivers/vercel/OPERATING-CONTEXT.md`

- [ ] **Step 1: Write the frontmatter.** `uses_tools` is deliberately omitted (the skill shells the Vercel CLI; the connector gate allows an empty/absent `uses_tools` for a `keyed_cli` add-on).
```yaml
---
name: Launch My Site
description: Take the site you built with design-my-site live on the internet. Connect a Vercel account once, and every future update ships with a word. Your page, on a real URL, ready to share.
triggers:
  - launch my site
  - publish my site
  - put my site live
  - deploy my website
  - ship my site to the internet
  - go live with my site
function_slot: deploy
requires_driver: vercel
requires_credential: key
data_path: local
status: active
---
```
- [ ] **Step 2: Author `drivers/vercel/OPERATING-CONTEXT.md`** in the meta-ads `OPERATING-CONTEXT.md` shape (clone `drivers/_template/OPERATING-CONTEXT.md`): how the Vercel connection works (keyed CLI, `vercel whoami` verify, preview-first), what lives in the account (projects, deployments, domains), and the write-safety lines in plain language (preview first; production only on an explicit yes; report the real outcome). This is the source text Step 1 of the body folds into `./CLAUDE.md`.
- [ ] **Step 3: Write the gate-led body** against spec §5b, **Hard-rules-first** (mirroring `run-my-ads`). Open the body with a "Hard rules (read first — these override everything below)" block:
  1. Never deploy to production without an explicit yes.
  2. Preview first; production only on the owner's approval.
  3. Report the real CLI outcome, including failures; never claim the site is live until `vercel` confirms the URL.
  Then the steps:
  1. *Step 1 init — fold the operating context (kit §6, mirrors `run-my-ads` Step 1).* Fold `drivers/vercel/OPERATING-CONTEXT.md` into the owner's `./CLAUDE.md` with the skill's OWN no-clobber merge: read the source, read `./CLAUDE.md`, show the section or the diff, append or merge, never clobber hand-tuned content. Do **not** call `learn-my-business` (CRM-gated, never runs for an add-on-only owner).
  2. Confirm the local project builds (`npm run build` in the instantiated project).
  3. The connect-story (the worked example of the reusable doorway, see Task 2.5): explain the owner needs two things, a Vercel account and the Vercel CLI, and exactly how to get both (point at `drivers/vercel/connect.md`).
  4. Deploy a preview with the Vercel CLI; report the preview URL for review.
  5. On an explicit go, deploy to production (`vercel --prod`); report the URL. Never deploy without the go; never announce it live until `vercel` confirms it (Hard rules).
  6. Offer the post-launch loop: `get-found-online` live audit + the connected rank-tracking / AI-visibility doorway.
  - **Explicitly do NOT add a `check-*-safety.py` grep.** The Meta spend-scan in `check-connectors.py` exists to catch a *quiet* live switch (a status field flipped via an update tool). A CLI deploy has no such dual-path activation risk: `vercel --prod` is the single explicit switch, already guarded by Hard rule 1. A grep here would cargo-cult the Meta pattern onto a surface that does not need it — and the `vercel` driver ships no `never_call`/`never_set`, so the gate's safety scan is a no-op for it by construction.
- [ ] **Step 4: Lint.** `python tools/lint-skill.py skills/launch-my-site` → exit 0.
- [ ] **Step 5: Commit.**
  ```bash
  git add skills/launch-my-site/SKILL.md drivers/vercel/OPERATING-CONTEXT.md
  git commit -m "feat(site-builder): launch-my-site skill (Hard-rules-first Vercel CLI deploy) + operating context"
  ```

### Task 2.5: The `## Vercel` connectors card + the reusable connect-doorway doctrine

**Files:**
- Modify: `knowledge/connectors.md` (the `## Vercel` card — required for gate conformance)
- Modify: `knowledge/business-method.md` OR `knowledge/connectors.md` (the connect-doorway doctrine — pick one home)

- [ ] **Step 1: Add a `## Vercel (put your site live)` card** to `knowledge/connectors.md`, following the meta-ads card schema at the top of that file. This is **required for `check-connectors.py` conformance** (the gate prefix-matches the driver's `display_name` "Vercel" to a card heading). Fields:
  - **What it is** — the owner's Vercel account, so the system can put their built site on a real URL.
  - **Fits businesses that** — have built a site with `design-my-site` and want it live and shareable.
  - **Unlocks** — `launch-my-site`.
  - **Connect it** — a pointer to `drivers/vercel/connect.md` (not restated), plus the labelled `connect-a-tool` exception note (the keyed-CLI path).
  - **Keep it lean** — connect it when ready to go live, not "just in case."
  - **Heads-up** — Vercel's free tier is generous; the honest cost note said out loud first.
  - **Verify** — `vercel whoami` proves it is live.
- [ ] **Step 2: Decide the doctrine home** (lean `connectors.md` if it owns connect-tier framing; else a labelled section in `business-method.md`).
- [ ] **Step 3: Author the one-home statement:** the reusable articulation "Here is X you can do keyless; it becomes enhanced by Y, which you unlock with Z," with `design-my-site` → `launch-my-site` as the worked example. Have `launch-my-site` and `get-found-online`'s connected doorway reference this rather than restating it.
- [ ] **Step 4: Voice check + commit.**
  ```bash
  BOS_OFFLINE=1 python tools/check-doctrine-voice.py
  git add knowledge/business-method.md knowledge/connectors.md
  git commit -m "docs(site-builder): ## Vercel connectors card + one-home connect-doorway articulation (X keyless, enhanced by Y via Z)"
  ```

### Task 2.6: Register + onboard `launch-my-site`

**Files:**
- Modify: `knowledge/starter-projects.md`
- Regenerate: `kernel/registry.json`, `docs/CAPABILITIES.md`

- [ ] **Step 1: Add a connected-doorway row** to `knowledge/starter-projects.md` for `launch-my-site`, tagged **`needs_connection`** — the vendor-neutral connected-tier tag that already lives in `_CONNECTED_TIER_TAGS` in `tools/check-onboarding-binding.py` (it landed with the meta-ads work). This exempts the row from assertion B's keyless-honesty check honestly. Because it is `requires_credential: key`, it must NOT be tagged `[live]`+keyless; and it is NOT the CRM, so do NOT reach for `better_with_crm`/`needs_crm` (both are CRM-specific and would misdescribe a Vercel deploy). A row that follows `design-my-site` tagged `needs_connection` passes assertions A and B cleanly.
- [ ] **Step 2: Regenerate + verify.**
  ```bash
  BOS_OFFLINE=1 python tools/registry-generator.py
  BOS_OFFLINE=1 python tools/export-capabilities.py
  grep -n "launch-my-site" kernel/registry.json
  ```
  Expected: present with `function_slot: deploy`, `requires_driver: vercel`, `requires_credential: key`.
- [ ] **Step 3: Gates.**
  ```bash
  BOS_OFFLINE=1 python tools/check-onboarding-binding.py
  BOS_OFFLINE=1 python tools/check-connectors.py
  BOS_OFFLINE=1 python tools/registry-generator.py --check
  BOS_OFFLINE=1 python tools/export-capabilities.py --check
  ```
  Expected: all exit 0. `check-connectors.py` is the connected-add-on conformance gate: it proves `drivers/vercel` declares a valid `keyed_cli` kind, `requires_driver: vercel` resolves, `connect.md` + the `## Vercel` card are present, and `launch-my-site` honours the connected frontmatter contract.
- [ ] **Step 4: Commit.**
  ```bash
  git add knowledge/starter-projects.md kernel/registry.json docs/CAPABILITIES.md
  git commit -m "feat(site-builder): register + onboard launch-my-site (connected doorway, needs_connection)"
  ```

### Task 2.7: Phase-2 gates + deploy dogfood

- [ ] **Step 1: Run the full CI-order gate block** (including `tools/check-connectors.py`). All exit 0. The gate-conformance acceptance criterion (spec §10.1) is met when `launch-my-site` + `drivers/vercel` pass `check-connectors.py`.
- [ ] **Step 2: Deploy dogfood** (live, with a real Vercel account, done by Vic or with explicit go): take a Phase-1 built page, run `launch-my-site`, confirm a preview URL then a production URL, and confirm the skill never deployed without the go and reported the real outcome. Fold any fixes; re-run gates.

---

## Phase 3 — Final integration pass

- [ ] **Step 1: Full gate sweep** in CI order (secret scan → kernel-clean → doctrine-voice → registry `--check` → capabilities `--check` → onboarding-binding → lint each skill → `unittest discover`). All green.
- [ ] **Step 2: Update the spec status** in `docs/architecture/2026-07-03-site-builder-design.md` to "Implemented" with the commit range, and note the two dogfood results (as the SEO spec records its 5/5).
- [ ] **Step 3: Finish the branch** using superpowers:finishing-a-development-branch (merge to `main`; the BOS repo push is Vic's to run, per the workspace rule).

---

## Non-goals (carried from the spec §9)

- No deploy logic inside `design-my-site`; no Claude Design MCP-server dependency on the floor; no hosted/multi-tenant builder, CMS, or e-commerce checkout; no re-implementation of SEO / competitor research / brand strategy (delegate); no new `studio/` render surface (the site is the owner's project, not a shared render studio).

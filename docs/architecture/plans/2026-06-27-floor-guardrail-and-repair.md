# Floor Wave 0 — Guardrail + Onboarding Repair Implementation Plan

> **For agentic workers:** Execute via superpowers:subagent-driven-development (fresh subagent per task + spec review + quality review). Run in the `floor-guardrail-repair` worktree. Gate per task: relevant tests/lint green + faithful to this plan + full offline suite green.

**Goal:** Stop the shipped onboarding from advertising apps that don't exist or aren't keyless, and install the structural guardrail that prevents the drift from ever recurring — binding the onboarding surface to `kernel/registry.json` as the single source of truth.

**Architecture:** A new offline binding check + a manifest rule make "onboarding only ever offers real, keyless wins" a checked CI invariant; `start-here` is constrained at runtime to route only to registry-keyless apps; the curated `starter-projects.md` library is kept for vertical tailoring but its references are bound. No new floor apps are built in this wave — those follow in unlock-priority order per [`floor-roster.md`](../floor-roster.md).

**Tech stack:** Python stdlib (the check), Markdown skills + manifest frontmatter, the offline harness (`BOS_OFFLINE`, `lint-skill.py`, `registry-generator.py --check`).

**Source of truth for what is/isn't keyless:** `kernel/registry.json` (generated from manifests). Keyless = `requires_credential: none` AND `requires_driver` in {`none`, `markitdown`, `render`, `firecrawl`}.

---

## Task 1: The onboarding-binding check + manifest rule (TDD)

**Files:**
- Create: `tools/check-onboarding-binding.py`
- Create: `tests/test_onboarding_binding.py`
- Modify: `tools/manifest.py` (or `tools/lint-skill.py`) — add the `credential:none` ⇒ no `mcp__` in `uses_tools` rule
- Modify: the CI/test wiring so the check runs in the suite (mirror how `registry-generator --check` is invoked)

**Build:** A stdlib checker that loads `kernel/registry.json` and scans the onboarding surface — `skills/start-here/SKILL.md`, `skills/whats-possible/SKILL.md`, `knowledge/starter-projects.md` — extracting referenced app-ids (skill folder names / command names; the backticked `Builds on` cells and routing tokens). It asserts:
- **A (exists):** every referenced app-id is a key in the registry with `status: active`. Phantom apps (no registry entry) FAIL.
- **B (keyless honesty):** any app the surface offers as a keyless win / tags `[live]` / routes as a cold instant-win is `requires_credential: none` AND a keyless driver. A `[live]`/keyless-offered app that the registry marks `mcp`/`trustpager` FAILS. (Apps explicitly tagged `better_with_crm` / `needs_crm` / placed in a non-routable "Planned" block are EXEMPT from B — they are honestly flagged as connected-tier/unbuilt.)
- **C (no hidden coupling):** no `requires_credential: none` skill body contains a TrustPager tool token (`mcp__trustpager__*`), a `dump-crm-bundle`/`dump-transcripts` script call, or an `api.trustpager.com` curl. (This is what catches `design-nurture-sequence`.)

**Manifest rule:** a `requires_credential: none` skill may not list any `mcp__…` entry in `uses_tools`. Add to the manifest validator / lint so it FAILs (this catches `quote-from-photo`).

**TDD order:** write failing tests first using fixtures — (1) a phantom reference fails A; (2) a `[live]`-tagged `mcp` app fails B; (3) a keyless skill body with a `mcp__trustpager__` token fails C; (4) a `credential:none` manifest with an `mcp__` `uses_tools` entry fails the manifest rule; (5) a clean surface passes. Then implement to green.

**Acceptance:** all five tests pass; the check is wired into the suite; running it against the CURRENT (unrepaired) tree FAILS loudly on the known drift (the 10 phantoms + the mislabels + design-nurture-sequence + quote-from-photo). Capture that failing output in the task report (it is the proof the guardrail works). Do NOT fix the drift in this task — Task 2 does.

## Task 2: Repair the onboarding surface + decouple the mislabels + regenerate

**Files (modify):** `skills/start-here/SKILL.md`, `knowledge/starter-projects.md`, `skills/quote-from-photo/SKILL.md`, `skills/design-nurture-sequence/SKILL.md`, `knowledge/industry-notes.md`, `knowledge/communication-voice.md`, `skills/make-social-post/SKILL.md`, `skills/make-thumbnail/SKILL.md`, `skills/onboard-team-member/SKILL.md`, `templates/CLAUDE.md` (only if a TP-coupled tool list lingers); then regenerate `kernel/registry.json`.

**Build — make every onboarding offer real + keyless:**
1. **start-here Step 6 + Step 7:** remove routes to apps that aren't keyless-and-built. Keep only the genuinely keyless instant-wins that ship today: `build-brand-strategy` (Mode A), `quote-from-photo`, `extract-document`, `make-social-post`, `compare-documents`, `template-from-document`, `write-prompt`. Drop the `grill-me-on-this-decision`, `research-a-competitor`, and uncaveated `transcript-summary` routes (these return in later waves as they're built). Add an explicit instruction that start-here may only route to apps present in `kernel/registry.json` with `requires_credential: none` — the registry is the routing allow-list; the library proposes, the registry gates.
2. **starter-projects.md:** move every `[floor-new]` (unbuilt) row into a clearly-labelled, **non-routable "Planned / coming soon"** section (so the curation/vision is preserved but start-here cannot offer them as buildable now). Delete the header clause that says projects may map to "a decided-but-unbuilt floor app." Retag the mislabels honestly: `build-customer-voice`, `build-spreadsheet`, `audit-my-data`, `import-from-anywhere` → `better_with_crm` / `needs_crm` (they are connected-tier today). Keep slot-1/slot-2 cold offers keyless; TrustPager stays reactive-only.
3. **quote-from-photo:** drop `mcp__trustpager__list_products` from `uses_tools` (it's a `none/none` skill); reword Step 2 so the catalogue pull is explicitly "if your workspace is connected" optional enrichment over the keyless default (price-my-work will be the keyless pricing fallback once it lands; for now the keyless fallback is "draft the scope + line-item structure, leave prices for the owner").
4. **design-nurture-sequence:** reclassify the manifest to `requires_credential: mcp`, `requires_driver: trustpager`, `data_path: mcp_tools` (it hard-requires the CRM — `dump-crm-bundle`, the help-center curl, the synthesis-file STOP). It is a connected-tier comms skill, not floor. (A keyless draft-only mode is a later-wave option, not this wave.)
5. **Cosmetic leaks:** `industry-notes.md` — genericise "TrustPager" in the data-ownership gotchas to "your CRM / system of record." `communication-voice.md` — swap the hardcoded `app.trustpager.com` example URL for a neutral placeholder. `make-social-post`/`make-thumbnail` — soften "your TrustPager brand/workspace" → "your brand / your workspace (when connected)"; leave the optional publish step. `onboard-team-member` — make the TP connect step conditional and copy the owner's actual business-context block rather than hardcoding an "About TrustPager" heading.
6. **Regenerate** `kernel/registry.json` (`python tools/registry-generator.py`) so the design-nurture-sequence reclassification + any frontmatter edits land; confirm `--check` passes.

**Acceptance:** `tools/check-onboarding-binding.py` now PASSES (the proof the repair closed the drift); the manifest rule passes; `registry-generator --check` clean; every skill lints clean; `check-no-secrets` + `check-kernel-clean` green; full `BOS_OFFLINE` suite green. The floor entry path (start-here / whats-possible / build-brand-strategy Mode A) remains TP-reactive-only.

---

## Definition of done
- [ ] The binding check + manifest rule exist, are wired into the suite, and FAIL on the pre-repair tree (captured) then PASS post-repair.
- [ ] start-here routes only to registry-keyless apps; starter-projects `[floor-new]` rows are in a non-routable Planned block; mislabels retagged; quote-from-photo + design-nurture-sequence corrected; cosmetic leaks fixed.
- [ ] Registry regenerated; lint + manifest + registry-fresh + secrets + kernel-clean + full offline suite all green.
- [ ] No new floor apps built (those follow per floor-roster.md unlock-priority order).

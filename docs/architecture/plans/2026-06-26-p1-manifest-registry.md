# P1 — Manifest + Generated Registry Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (fresh subagent per task + two-stage review). The bulk backfill (Task 4) is a Workflow fan-out. Steps use checkbox (`- [ ]`) syntax. Run in a dedicated worktree.

**Goal:** Make BOS capability data-driven — every skill carries a manifest, a generated `registry.json` is the single source of truth for "what can you do / what's connected," and lint enforces the contract — so growth is additive (drop in a folder), never a kernel edit.

**Architecture:** Markdown-frontmatter-first. Each skill's `SKILL.md` gains a manifest block. A generator reads all manifests → `kernel/registry.json` (shipped like a lockfile, CI diff-checked). `lint-skill.py` validates the contract and FAILs CI on violations. No new runtime deps (stdlib-only; flat-frontmatter parser, not external YAML).

**Tech Stack:** Python 3 stdlib · `unittest` · the offline harness (`BOS_OFFLINE`, `lint-skill.py`, `check-kernel-clean.py`, `check-no-secrets.py`).

**Source specs:** `docs/architecture/founder-decisions.md` (D6 floor/catalog, **D8 MCP-first data path**), `bos-rearchitecture-review.md` (§2 contract, P0 #2, P1 #6/#7/#11, P2 #12), `skill-extraction-audit.md` (the bucket per skill).

**The manifest schema (the contract):** frontmatter keys, flat values + simple string lists only:
| Key | Required | Values |
|---|---|---|
| `function_slot` | ✓ | one of: `crm`, `accounting`, `ads`, `social`, `creative`, `comms`, `documents`, `money`, `people`, `strategy`, `research`, `floor` |
| `requires_driver` | ✓ | a driver id (e.g. `trustpager`) or `none` |
| `requires_credential` | ✓ | `none` \| `mcp` \| `key` (D8: TrustPager apps = `mcp`; floor = `none`) |
| `data_path` | ✓ | `reasoning_only` \| `mcp_tools` \| `fetch_rest` (D8: TrustPager default `mcp_tools`; floor `reasoning_only`; keyed turbo `fetch_rest`) |
| `uses_tools` | optional | list of `mcp__*` tool names the skill body calls |
| `unlocks` | optional | list of capabilities this app's driver enables |
| `reads_for_profile` | optional | list of profile fields this app can enrich |
| `status` | optional (default `active`) | `active` \| `deprecated` \| `removed` |

**Non-negotiables:** kernel stays vendor-neutral (check-kernel-clean green); no new runtime deps; every existing test stays green; the registry is *generated*, never hand-edited.

---

## Task 1: Manifest schema + validator + two exemplars

**Files:**
- Create: `tools/manifest.py` (importable `parse_frontmatter(text)` + `validate_manifest(meta) -> list[str]` errors)
- Create: `docs/architecture/manifest-schema.md` (the human contract — the table above + examples)
- Modify: `skills/write-prompt/SKILL.md` (exemplar: floor), `skills/sweep-my-day/SKILL.md` (exemplar: TrustPager/MCP)
- Test: `tests/test_manifest.py`

- [ ] **Step 1: Write failing tests** in `tests/test_manifest.py`: a valid floor manifest passes; missing a required key fails; a bad enum (`data_path: nope`) fails; an unknown key fails; `requires_driver: none` + `requires_credential: none` + `data_path: reasoning_only` is the canonical floor combo.
- [ ] **Step 2: Run → FAIL** (`BOS_OFFLINE=1 python -m unittest tests.test_manifest -v`).
- [ ] **Step 3: Implement `tools/manifest.py`** — `parse_frontmatter` (reuse/extract the flat-frontmatter logic; flat scalars + `- ` list items only) and `validate_manifest` (required keys present, enum membership, closed key set, list-typed fields are lists).
- [ ] **Step 4: Run → PASS.**
- [ ] **Step 5: Add manifest frontmatter to the two exemplars** — `write-prompt` (`function_slot: floor`, `requires_driver: none`, `requires_credential: none`, `data_path: reasoning_only`) and `sweep-my-day` (`function_slot: crm`, `requires_driver: trustpager`, `requires_credential: mcp`, `data_path: mcp_tools`, `uses_tools: [...]`). Validate both with `validate_manifest`.
- [ ] **Step 6: Write `docs/architecture/manifest-schema.md`** (the contract table + the two exemplars).
- [ ] **Step 7: Full offline suite + secret scan + kernel-clean green. Commit.** `feat(p1): manifest schema + validator + exemplar manifests`

## Task 2: Registry generator

**Files:** Create `tools/registry-generator.py`; Test `tests/test_registry_generator.py`

- [ ] **Step 1: Failing test** — given a temp tree of 2-3 fake `skills/*/SKILL.md` with manifests, `generate_registry(skills_dir)` returns a dict with one entry per skill carrying the manifest fields, sorted by skill name; running it twice yields byte-identical JSON (determinism).
- [ ] **Step 2: Run → FAIL.**
- [ ] **Step 3: Implement `tools/registry-generator.py`** — walk `skills/*/SKILL.md`, parse+validate each manifest (skip with a logged warning if a manifest is malformed; never crash the whole registry — review P1 #8), emit `kernel/registry.json` (sorted keys, `indent=2`, trailing newline). Importable `generate_registry()` + `__main__` that writes the file.
- [ ] **Step 4: Run → PASS.**
- [ ] **Step 5: Generate against the two real exemplars + assert determinism. Commit.** `feat(p1): registry generator -> kernel/registry.json`

## Task 3: Lint hardening

**Files:** Modify `tools/lint-skill.py`; Test extend `tests/` (or `tests/test_lint_manifest.py`)

- [ ] **Step 1: Failing tests** — lint FAILs a skill with: a missing/invalid manifest; an `mcp__*` tool referenced in the body but absent from `uses_tools`; a `resolve_path` violation (promote the existing WARN→FAIL). Lint PASSes a clean skill. **Labelled exception:** a `requires_driver: trustpager` app MAY name `mcp__*trustpager*`/TrustPager tools freely (per D6 + anti-drift) — encode that exception explicitly.
- [ ] **Step 2: Run → FAIL.**
- [ ] **Step 3: Implement** — wire `validate_manifest` into `lint-skill.py`; add the undeclared-`uses_tools` check (with the TrustPager-native exception); flip `resolve_path` WARN→FAIL.
- [ ] **Step 4: Run → PASS** (and confirm the two exemplars lint clean; other skills will warn-not-fail until they get manifests in Task 4 — gate the new manifest checks so they only FAIL once a manifest exists, to avoid breaking the suite mid-rollout, OR run lint only on manifested skills until Task 4 completes; document the choice).
- [ ] **Step 5: Commit.** `feat(p1): lint enforces the manifest contract`

## Task 4: Bulk backfill — manifests on all skills (WORKFLOW fan-out)

This task is executed by a **Workflow** (one agent per skill), not a single implementer — it's a per-item classification across ~58 skills.

- [ ] **Step 1:** Run a Workflow that, per skill: reads `SKILL.md` + its bucket from `skill-extraction-audit.md`, derives the manifest (floor → `reasoning_only`/`none`; TrustPager-native → `mcp_tools`/`mcp`/`requires_driver: trustpager`; extractable → its standalone `data_path`), and writes the frontmatter block. Each agent validates with `tools/manifest.py`.
- [ ] **Step 2:** Regenerate `kernel/registry.json`; run `lint-skill.py` across ALL skills → every skill now passes the manifest contract.
- [ ] **Step 3:** Full offline suite + fixtures green. Commit. `feat(p1): backfill manifests across all skills + regenerate registry`

## Task 5: Robust flat-frontmatter parse + round-trip tests

**Files:** Modify `tools/manifest.py`; Test `tests/test_manifest.py`

- [ ] **Step 1: Failing round-trip tests** — every field type round-trips through `parse_frontmatter`: scalar string, quoted string with special chars, a `- ` list, an empty list, booleans/ints as strings. A nested/indented value is rejected with a clear error (we do NOT support nested YAML — flat only). (Review P1 #11: since stdlib has no YAML, we constrain to flat + test exhaustively rather than add a dep.)
- [ ] **Step 2: Run → FAIL** for any unhandled case; **Step 3: harden the parser** to handle/reject each precisely; **Step 4: PASS.**
- [ ] **Step 5: Commit.** `test(p1): exhaustive flat-frontmatter round-trip coverage`

## Task 6: CI — registry drift guard

**Files:** Modify `.github/workflows/test.yml`; Test `tests/test_registry_fresh.py`

- [ ] **Step 1: Failing test** — `tests/test_registry_fresh.py`: generating the registry in-memory equals the committed `kernel/registry.json` (fails if someone edits a manifest without regenerating).
- [ ] **Step 2: Run → it passes if registry is fresh; prove teeth by editing a manifest without regenerating → test FAILs; regenerate → passes.**
- [ ] **Step 3: Wire CI** — add a step to `.github/workflows/test.yml` (after kernel-clean): `python tools/registry-generator.py --check` (generates to a temp + diffs against committed; non-zero on drift).
- [ ] **Step 4: Full local CI sequence green. Commit.** `ci(p1): fail on registry drift`

---

## Definition of done
- [ ] Every skill carries a valid manifest; `lint-skill.py` FAILs the build on any contract violation (missing/invalid manifest, undeclared `uses_tools`, resolve_path violation).
- [ ] `kernel/registry.json` is generated, committed, and CI-diff-checked (drift fails the build).
- [ ] Manifest enums encode D8 (TrustPager apps `mcp_tools`/`mcp`; floor `reasoning_only`/`none`).
- [ ] No new runtime dependency; kernel stays vendor-neutral; all prior tests still green.
- [ ] A malformed single manifest degrades gracefully (logged, skipped) at runtime; fails loudly in CI.

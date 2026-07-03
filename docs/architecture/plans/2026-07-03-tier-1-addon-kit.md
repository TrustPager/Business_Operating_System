# Tier-1 Connected Add-on Kit Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking. Run this on the `feat/tier1-addon-kit` branch (already created, stacked off `feat/meta-ads-addon`).

**Goal:** Turn the shipped Meta Ads add-on into a reusable system: one CI gate (`tools/check-connectors.py`) that reads each connected driver's own `DRIVER` dict for both safety and structural conformance, a recipe doc, a driver-kind taxonomy, and docs-only templates, so every future connected add-on is near-mechanical and cannot ship half-wired or unsafe.

**Architecture:** Generalize `check-ads-safety.py` into `check-connectors.py`: it discovers `drivers/*/__init__.py` (skipping `_`-prefixed template dirs), `ast`-parses each top-level `DRIVER` dict statically (no import), and drives both a safety scan (`never_call`/`never_set`, now single-sourced from the dict) and a structural conformance scan (valid `kind`, `requires_driver` resolves, `connect.md` + connectors card for connected kinds, the connected frontmatter contract). Only drivers that ship a `DRIVER` dict are in scope, which grandfathers every legacy driver automatically. Full spec: [../2026-07-03-tier-1-addon-kit-design.md](../2026-07-03-tier-1-addon-kit-design.md).

**Tech Stack:** Python stdlib only (the gate stays import-free so it runs anywhere), `ast` for static dict reads, unittest offline suite (`BOS_OFFLINE=1`), Markdown (recipe + templates), GitHub Actions (one CI step repointed).

**Validation doctrine:** code artifacts (the gate) get real offline unittests. The retrofit must preserve **parity** with the shipped `check-ads-safety.py` (the same meta-ads violations still caught). Docs (recipe, taxonomy, templates) pass `check-doctrine-voice.py`. Every phase ends by running the CI-order gates.

**CI-order gates (run after each phase; all must pass):**
```bash
BOS_OFFLINE=1 python tools/check-no-secrets.py
BOS_OFFLINE=1 python tools/check-kernel-clean.py
BOS_OFFLINE=1 python tools/check-doctrine-voice.py
BOS_OFFLINE=1 python tools/registry-generator.py --check
BOS_OFFLINE=1 python tools/export-capabilities.py --check
BOS_OFFLINE=1 python tools/check-onboarding-binding.py
BOS_OFFLINE=1 python tools/check-connectors.py       # the new gate (Phase 1)
for d in skills/*/; do python tools/lint-skill.py "$d"; done
BOS_OFFLINE=1 python -m unittest discover -s tests -v
```

---

## File Structure

**New files:**
- `tools/check-connectors.py` — the generalized gate (renamed from `check-ads-safety.py` via `git mv`, then extended). Safety + conformance, driver-dict-driven.
- `tests/test_check_connectors.py` — offline unittests: parity (meta-ads violations still caught), plus one failing-fixture per conformance rule.
- `tests/fixtures/connectors/` — fixture drivers/skills/cards: a good `claude_mcp` add-on, a good `keyed_cli` add-on, and broken ones (bad kind, unresolved `requires_driver`, missing `connect.md`, missing card, `never_call` tool in a body, `never_set` field live).
- `docs/architecture/tier-1-addon-kit.md` — the recipe (the one home; checklist + taxonomy + the two frontmatter contracts + the connectors-card snippet).
- `drivers/_template/__init__.py`, `drivers/_template/connect.md`, `drivers/_template/OPERATING-CONTEXT.md`, `drivers/_template/README.md` — docs-only skeleton (`_`-prefixed so the gate skips it).

**Modified files:**
- `.github/workflows/test.yml` — repoint the existing "Ads spend-safety" step's `run:` to `check-connectors.py` and rename the step.
- `drivers/meta-ads/__init__.py` — add `keyed_cli` to the `kind` comment's enum (the DRIVER dict is already the safety single-source; no value change).

**Deleted:**
- `tools/check-ads-safety.py` — via `git mv` to `check-connectors.py` (history preserved).

**Do NOT touch:** the legacy drivers (`trustpager`, `regional`, `_noop`, folderless `firecrawl`/`render`/`markitdown`), `kernel/*`, `manifest.py`, `registry-generator.py`.

---

## Phase 1 — The gate

### Task 1: Rename + generalize the safety half (parity-preserving)

**Files:**
- Rename: `tools/check-ads-safety.py` → `tools/check-connectors.py`
- Modify: `drivers/meta-ads/__init__.py` (kind comment only)
- Test: `tests/test_check_connectors.py`

- [ ] **Step 1: `git mv` the file, update the module docstring** to describe the generalized gate (reads every connected driver's `DRIVER` dict; safety + conformance). Keep the existing `_skill_bodies()`, `_active_field_pattern()`, `SKIP_DIRS`, `MAX_BYTES` helpers.

- [ ] **Step 2: Write the failing parity test.**
```python
"""Offline-safe: no network, no key. Run: BOS_OFFLINE=1 python -m unittest tests.test_check_connectors"""
import subprocess, sys, unittest
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent

class TestSafetyParity(unittest.TestCase):
    def test_gate_passes_clean_on_real_tree(self):
        r = subprocess.run([sys.executable, "tools/check-connectors.py"], cwd=REPO,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_reads_never_call_from_driver_dict(self):
        sys.path.insert(0, str(REPO / "tools"))
        import importlib, check_connectors as cc
        importlib.reload(cc)
        drivers = cc._load_driver_dicts()
        self.assertIn("meta-ads", drivers)
        self.assertNotIn("_template", drivers)          # underscore dirs skipped
        self.assertNotIn("trustpager", drivers)         # no DRIVER dict → grandfathered
        self.assertIn("mcp__meta-ads__ads_activate_entity", drivers["meta-ads"]["never_call"])
```

- [ ] **Step 3: Run it, verify it fails.** `BOS_OFFLINE=1 python -m unittest tests.test_check_connectors -v` → FAIL (`_load_driver_dicts` not defined).

- [ ] **Step 4: Implement `_load_driver_dicts()`** (static `ast`, no import, skips `_`-prefixed dirs):
```python
import ast

def _load_driver_dicts() -> dict[str, dict]:
    """{driver_id: DRIVER dict} for every drivers/<id>/__init__.py declaring a
    top-level DRIVER dict. Skips underscore-prefixed dirs (templates/scaffolding).
    Static ast.literal_eval — never imports driver code."""
    out: dict[str, dict] = {}
    ddir = REPO_ROOT / "drivers"
    if not ddir.is_dir():
        return out
    for init in sorted(ddir.glob("*/__init__.py")):
        drv_id = init.parent.name
        if drv_id.startswith("_"):
            continue
        try:
            tree = ast.parse(init.read_text(encoding="utf-8", errors="ignore"))
        except (OSError, SyntaxError):
            continue
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "DRIVER" for t in node.targets
            ):
                try:
                    out[drv_id] = ast.literal_eval(node.value)
                except (ValueError, SyntaxError):
                    pass
    return out
```

- [ ] **Step 5: Replace the hard-coded `NEVER_CALL_TOOLS`/`NEVER_SET_ACTIVE`** with values aggregated from the loaded dicts, matching **both** name forms to preserve parity:
```python
def _name_forms(tool: str, driver_id: str) -> set[str]:
    forms = {tool}
    prefix = f"mcp__{driver_id}__"
    if tool.startswith(prefix):
        forms.add(tool[len(prefix):])          # bare name, preserves current breadth
    return forms
```
Build `never_call` as `(form, driver_id)` pairs and `never_set` as `{form: (fields...)}` from every driver's dict, then run the existing per-line (Path 1) and whole-text DOTALL (Path 2) scans unchanged. Delete the module-level `NEVER_CALL_TOOLS`/`NEVER_SET_ACTIVE` literals.

- [ ] **Step 6: Add `keyed_cli` to the meta-ads kind comment** in `drivers/meta-ads/__init__.py` (`# keyed_rest | keyed_cli | keyless_mcp | local | data_pack | claude_mcp`). No value change.

- [ ] **Step 7: Run the parity tests, verify PASS.** `BOS_OFFLINE=1 python -m unittest tests.test_check_connectors -v` → PASS, and `python tools/check-connectors.py` still prints OK on the real tree.

- [ ] **Step 8: Repoint CI.** In `.github/workflows/test.yml`, rename the step to `Connector safety + conformance` and change its `run:` to `python tools/check-connectors.py`.

- [ ] **Step 9: Commit.**
```bash
git mv tools/check-ads-safety.py tools/check-connectors.py   # if not already done in Step 1
git add tools/check-connectors.py drivers/meta-ads/__init__.py .github/workflows/test.yml tests/test_check_connectors.py
git commit -m "feat(addon-kit): generalize the safety gate to read each driver's DRIVER dict (parity-preserving)"
```

### Task 2: Add the conformance checks

**Files:**
- Modify: `tools/check-connectors.py`
- Test: `tests/test_check_connectors.py`, `tests/fixtures/connectors/`

- [ ] **Step 1: Write failing conformance fixtures + tests.** Under `tests/fixtures/connectors/` create a good `claude_mcp` add-on, a good `keyed_cli` add-on, and broken ones (bad kind; `requires_driver` typo; missing `connect.md`; card heading not matching `display_name` prefix; connected frontmatter violating credential/data_path/uses_tools). Because the real gate scans the repo, make the checker accept a `--root <dir>` argument so tests can point it at a fixture tree; assert exit 0 on the good fixtures and exit 2 (with the specific message) on each broken one.
```python
def _run(root):
    return subprocess.run([sys.executable, "tools/check-connectors.py", "--root", str(root)],
                          cwd=REPO, capture_output=True, text=True)
class TestConformance(unittest.TestCase):
    def test_good_claude_mcp_passes(self):
        self.assertEqual(_run(REPO/"tests/fixtures/connectors/good-claude-mcp").returncode, 0)
    def test_good_keyed_cli_passes(self):
        self.assertEqual(_run(REPO/"tests/fixtures/connectors/good-keyed-cli").returncode, 0)
    def test_bad_kind_fails(self):
        r = _run(REPO/"tests/fixtures/connectors/bad-kind"); self.assertEqual(r.returncode, 2); self.assertIn("kind", r.stdout)
    def test_unresolved_requires_driver_fails(self):
        r = _run(REPO/"tests/fixtures/connectors/bad-driver-id"); self.assertEqual(r.returncode, 2); self.assertIn("requires_driver", r.stdout)
    # ... missing_connect_md, missing_card, bad_frontmatter
```

- [ ] **Step 2: Run, verify fail.** → FAIL (`--root` unsupported; conformance not implemented).

- [ ] **Step 3: Implement conformance in `check-connectors.py`:**
  - Add a `--root` arg (defaults to `REPO_ROOT`) so `_skill_bodies()`, `_load_driver_dicts()`, and the connectors-card/connect.md reads all resolve under it (enables fixture testing).
  - `CANONICAL_KINDS = {"claude_mcp","keyed_cli","keyed_rest","keyless_mcp","local","data_pack"}`; for each loaded `DRIVER` dict, FAIL if `kind` absent or not in the set.
  - **`requires_driver` resolution** across every skill manifest: valid if `none`, OR in `_KEYLESS_DRIVERS` (reuse the exact set from `check-onboarding-binding.py`: `{none, markitdown, render, firecrawl, doclib}` — import it or mirror with a one-line comment pointing at the source), OR `drivers/<id>/` exists. Else FAIL naming the skill.
  - For each loaded dict whose `kind` is connected (`claude_mcp`, `keyed_cli`): FAIL if `drivers/<id>/connect.md` missing, or if no heading in `knowledge/connectors.md` **begins with** `display_name` (prefix match, per spec §6).
  - **Connected frontmatter contract:** for each skill whose `requires_driver` is a loaded-dict driver id, FAIL if `requires_credential` not in `{mcp,key}`, or `data_path` not in `{mcp_tools,local}`, or any `uses_tools` entry is not driver-owned (does not contain the driver id). Parse the skill frontmatter with the existing `manifest.py` `parse_frontmatter` (import it — this is a checker, importing the parser is fine; the stdlib-only constraint is about not importing driver/vendor code, and manifest.py is stdlib).
  - Merge conformance findings into the same `findings` list as the safety scan; one exit code, one report.

- [ ] **Step 4: Run tests, verify PASS** (good fixtures exit 0, each broken one exits 2 with its message), and `python tools/check-connectors.py` still OK on the real tree.

- [ ] **Step 5: Commit.**
```bash
git add tools/check-connectors.py tests/test_check_connectors.py tests/fixtures/connectors/
git commit -m "feat(addon-kit): conformance checks (kind, requires_driver resolves, connect.md + card, connected frontmatter)"
```

## Phase 2 — Recipe, taxonomy, templates

### Task 3: The recipe doc + taxonomy

**Files:**
- Create: `docs/architecture/tier-1-addon-kit.md`

- [ ] **Step 1: Author the recipe** per spec §3-§4: the mechanical build checklist (plan/run seam; the two frontmatter contracts with the deliberate-omission trick; the folderless documentation-only driver; `connect.md` single-home; the connectors-card schema; the labelled `connect-a-tool` override; the `needs_connection` onboarding tag as done; the Source A/B/C/D intake + `~/.claude/bos-cache/<addon>-profile.json`; personalization-is-DATA; layered write-safety only for money/irreversible surfaces). Include the canonical six-`kind` taxonomy table and point at `meta-ads` as the worked example. Cross-link `trustpager-to-floor-extraction.md` (adjacent: floor-extraction vs connected-add-on authoring).
- [ ] **Step 2: Voice check + commit.**
```bash
BOS_OFFLINE=1 python tools/check-doctrine-voice.py
git add docs/architecture/tier-1-addon-kit.md
git commit -m "docs(addon-kit): the recipe — how to build a connected add-on"
```

### Task 4: The docs-only driver template

**Files:**
- Create: `drivers/_template/__init__.py`, `drivers/_template/connect.md`, `drivers/_template/OPERATING-CONTEXT.md`, `drivers/_template/README.md`

- [ ] **Step 1: Author the skeleton** mirroring `drivers/meta-ads/` shapes: `__init__.py` with a `DOCUMENTATION ONLY` docstring and a fully-commented `DRIVER` dict (every field explained, `kind` showing the canonical set, and a `never_set` example carrying **all** interchangeable status fields per spec §8, not a one-field simplification). `connect.md`/`OPERATING-CONTEXT.md`/`README.md` stubs following the meta-ads shapes with `<placeholder>` markers.
- [ ] **Step 2: Confirm the gate skips it.** Run `python tools/check-connectors.py` — the `_`-prefix skip (Task 1) means `_template` is not validated, so placeholder values do not fail CI. Verify OK.
- [ ] **Step 3: Voice check + commit.**
```bash
BOS_OFFLINE=1 python tools/check-doctrine-voice.py
git add drivers/_template/
git commit -m "docs(addon-kit): drivers/_template docs-only skeleton for the next connected driver"
```

## Phase 3 — Validation + finish

### Task 5: Full sweep, dogfood, finish

- [ ] **Step 1: Run the full CI-order gate block** (see header). All exit 0, including the new `check-connectors.py`.
- [ ] **Step 2: Dogfood the gate.** Confirm `check-connectors.py` passes clean against the real `meta-ads` add-on, and that a deliberately-broken copy of meta-ads (e.g. an `ads_activate_entity` call added to a scratch skill body under the fixture root) is caught with a clear `file:line` message. Confirm parity: the same violations `check-ads-safety.py` caught pre-rename are still caught.
- [ ] **Step 3: Update the spec status** in `docs/architecture/2026-07-03-tier-1-addon-kit-design.md` to "Implemented" with the commit range.
- [ ] **Step 4: Finish the branch** with superpowers:finishing-a-development-branch. `feat/tier1-addon-kit` stacks off `feat/meta-ads-addon`, so the merge order is meta-ads first, then this. The BOS repo push is Vic's to run.

---

## Non-goals (carried from spec §10)

No full sweep of legacy drivers into the taxonomy; no scaffolding/codegen script; not the D13 library subsystem; not the D10 token investigation; no change to `kernel/*`, `manifest.py`, or `registry-generator.py` (the gate does `requires_driver` resolution externally).

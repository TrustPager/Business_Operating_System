# Public-Release Readiness Implementation Plan

> **For agentic workers:** Execute via superpowers:subagent-driven-development (fresh subagent per task + spec review + quality review). Run in a `public-release` worktree. Steps use checkbox (`- [ ]`) syntax. **Every task's gate:** `BOS_OFFLINE=1 python -m unittest discover -s tests` green; `python tools/check-no-secrets.py` OK; and for any manifest/registry/capabilities change, `python tools/registry-generator.py --check` + `python tools/export-capabilities.py --check` both report up to date in the same commit.

**Goal:** Make the BOS repo honest, coherent, and genuinely installable as a public GitHub project: a stranger with no TrustPager account installs and reaches a real keyless first win, while the TrustPager tier reads as a powerful optional upgrade.

**Architecture:** Three workstreams. (1) Install actually works: a shared `tools/_paths.py` root resolver + `CLAUDE_PLUGIN_ROOT`-resolved tool invocation in keyless skills (clone/dev fallback), a `setup.py` key-skip, and a cold-install smoke that runs from outside the repo so it cannot false-green. (2) Public prose: audit `CAPABILITIES.md` classification, then reposition README / INSTALL / plugin manifests / `commands/` descriptions keyless-first with TrustPager as the positive optional upgrade. (3) OSS community scaffolding. The install workstream lands first so the prose and the release gate verify against a working install.

**Tech stack:** Python stdlib (tools), Markdown (skills, docs, community files), JSON (plugin manifests, registry), the offline harness (`BOS_OFFLINE`, `check-install.py`, `check-no-secrets.py`, `registry-generator.py`, `export-capabilities.py`).

**Source spec (locked, approved):** [`docs/architecture/2026-06-29-public-release-readiness-design.md`](../2026-06-29-public-release-readiness-design.md).

**Cross-cutting rules (apply to every task):**
- **Shipped content carries ZERO em dashes** (README, INSTALL, all OSS files, plugin/marketplace descriptions, `commands/*.md` descriptions, any SKILL prose touched). Grep each file you author/edit for the em-dash character before committing. Use commas, colons, periods, or parentheses.
- **No document may claim TrustPager is required to start.** TrustPager is the positive optional upgrade in its own section; Claude may speak factually about what it unlocks.
- **Positive-only, outcome-led** customer-facing copy.
- **Preserve, do not rewrite-from-scratch.** Where existing prose is already correct (README opening, `/start-here` block, "Going deeper"), keep it and fix only the stale parts.
- Repo identity is unchanged: `TrustPager/Business_Operating_System`, owner `trustpager`, LICENSE copyright `TrustPager`.

---

## Increment 1 — Install actually works (foundation; build first)

> The riskiest workstream and the one the release gate verifies against. Sequential.

### Task 1.1 — reuse + extend the EXISTING root resolver (`kernel/runtime/paths.py`)
**Do NOT create a new resolver.** `kernel/runtime/paths.py` already implements `plugin_root()` (the `CLAUDE_PLUGIN_ROOT` → walk-upward → fallback chain) with tests at `tests/test_paths.py`. Creating a second `tools/_paths.py` would be a competing system (anti-drift violation). This task audits and extends the existing one.
**Files:** modify `kernel/runtime/paths.py` (only if helpers are missing); extend `tests/test_paths.py`.
**Build:** read `kernel/runtime/paths.py` and confirm `plugin_root()` returns: `CLAUDE_PLUGIN_ROOT` if set and non-empty, else the repo root derived from the file location, cwd-independently. Add `tool_path(name)` and `data_path(*parts)` convenience helpers ONLY if not already present, built on `plugin_root()`. If the existing fallback already satisfies cwd-independence, this task is mostly verification + (maybe) the two helpers.
**Import note for tools:** a standalone `tools/foo.py` shelled directly cannot `import kernel.runtime.paths` without the repo root on `sys.path`. The convention (used by Task 1.2): the tool resolves its own location and inserts the repo root onto `sys.path` before importing, e.g. `import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent)); from kernel.runtime.paths import plugin_root`. Document this one-line bootstrap in the resolver's docstring so every tool uses the same idiom.
**Tests (extend `tests/test_paths.py`):** `plugin_root()` honors `CLAUDE_PLUGIN_ROOT` when set (monkeypatch); falls back to the real repo root when unset, regardless of `os.getcwd()` (chdir to a temp dir to prove cwd-independence); any new helper resolves under `plugin_root()`.
**Acceptance:** ONE resolver (the kernel one), cwd-independent and env-aware; the tool bootstrap idiom is documented; tests green; suite green; no em dashes in code comments.

### Task 1.2 — route repo-relative tool data reads through `_paths`
**Files:** modify the tools that read repo-relative data — at minimum `tools/regional.py` (the AU constants dir), and audit `tools/registry-generator.py`, `tools/export-capabilities.py`, `tools/check-install.py`, `tools/markitdown_convert.py`, `tools/write_xlsx.py`, `tools/finance_calc.py` for any path that assumes cwd. Most already resolve from `__file__`; convert any that assume cwd to `_paths`. Test: `tests/test_paths_resolver.py` (extend) or `tests/test_regional_au.py`.
**Build:** replace ad-hoc `Path(__file__)...` data-root logic with `from _paths import bos_root, data_path` where it clarifies, and ensure each tool can be invoked from a cwd outside the repo and still find its data. Do NOT change tool behavior or output, only path resolution.
**Tests:** a test that imports/invokes `load_au_constants("AU")` (and any other data-reading tool touched) after `os.chdir(tempdir)` and asserts it still loads. Add a regression that `registry-generator`/`export-capabilities --check` still pass from a foreign cwd.
**Acceptance:** every data-reading tool works from any cwd; outputs byte-identical to before; suite + `--check`s green.

### Task 1.3 — `CLAUDE_PLUGIN_ROOT`-resolved tool invocation in skills + commands
**Files:** grep-driven scope, NOT a hardcoded list. Run `grep -rl "python tools/" skills/ commands/` to get the exact set (repo verification at plan time: ~23 `skills/**/SKILL.md` plus at least `commands/audit-my-data.md`; include `build-customer-voice` and `build-knowledge-base-from-docs`, which do shell tools). Do not assume `assemble-pack`/`quote-from-photo` are in scope (they shell nothing); trust the grep.
**Build:** change every bare `python tools/foo.py ...` to the official Claude Code plugin form (confirmed against the plugins reference: Claude Code substitutes `${CLAUDE_PLUGIN_ROOT}` and the plugin's `tools/` is materialized on disk under it):
```
python "${CLAUDE_PLUGIN_ROOT}/tools/foo.py" ...
```
Double-quote the path (spaces); forward slashes are fine on Windows for `python`. **Do NOT use a Bash `${VAR:-default}` fallback** (it breaks in PowerShell/cmd, the primary platform). Dev/clone runs set `CLAUDE_PLUGIN_ROOT` to the checkout root (documented in CONTRIBUTING and set by the harness/smoke), so the same single form works in dev and in a plugin install. Update any prose that says "run from the repo root."
**Open verification (resolved in Task 1.5):** the docs confirm `${CLAUDE_PLUGIN_ROOT}` substitution for hooks/MCP/monitors but do not formally confirm it inside SKILL bodies, nor the Windows shell. Task 1.5 empirically verifies this form on Windows in a real plugin-cache layout. **Fallback if verification fails:** a launcher in `bin/` (auto-added to PATH when the plugin is active, per the plugins reference) that resolves the root internally, so skills call `bos-tool foo ...` with no path/var in the command. If 1.5 shows the token form does not expand in skill bodies on Windows, switch this task to the `bin/` launcher form before proceeding.
**Tests:** a `tests/` assertion (or check-install sub-check) that no in-scope skill/command still uses a bare `python tools/` without the `${CLAUDE_PLUGIN_ROOT}` form. Lint each touched skill clean; manifests unchanged so registry stays fresh.
**Acceptance:** every in-scope skill/command uses the resolved form (or the `bin/` launcher if 1.5 dictates); lint + binding + registry + suite green; em-dash scan clean on touched files.

### Task 1.4 — `setup.py` clean key-skip (keyless success)
**Files:** modify `tools/setup.py`; test `tests/test_setup_keyskip.py` (create) or extend an existing setup test.
**Build:** the key-collection step must allow a clean skip: blank input proceeds (no `ERROR: empty key. Aborting.` / exit 2), prints a friendly "no key set, the keyless floor is ready, connect TrustPager later" line, and `setup.py` exits 0 having installed the doc stack. Keep the detect-and-reuse path (existing MCP key) and the explicit-paste path intact. Doc-stack bundling (D11) unchanged.
**Tests:** simulate blank key input → exit 0, doc stack install attempted, no key written; simulate a pasted `tp_live_...` → key stored as before. Keep offline (mock the pip call + input).
**Acceptance:** keyless `setup.py` finishes successfully with no key; keyed path unchanged; suite green.

### Task 1.5 — cold-install smoke (no false-green) + check-install keyless mode
**Files:** modify `tools/check-install.py` (confirm/extend its keyless-floor mode); create `tests/test_cold_install_smoke.py` or a documented script `tools/cold-install-smoke.py`.
**Build:** a smoke that sets `CLAUDE_PLUGIN_ROOT` to the repo, runs from a cwd OUTSIDE the repo, and exercises the keyless floor end-to-end with zero key: a doc write to read round-trip (`write_xlsx` then `markitdown_convert`), a `finance_calc` run, and the `regional` loader for `AU`. It must FAIL if any tool cannot resolve its path. `check-install.py --keyless` (or equivalent) runs the same checks and prints green/red.
**Windows verification of the Task 1.3 invocation form (resolves the open question):** in addition to the Python-level smoke, verify the actual `${CLAUDE_PLUGIN_ROOT}` skill-invocation form on Windows by staging a real plugin-cache-style layout (copy the repo to a temp dir, set `CLAUDE_PLUGIN_ROOT` to it) and running the exact `python "${CLAUDE_PLUGIN_ROOT}/tools/foo.py"` command a skill would emit, through the session shell (PowerShell). Confirm it resolves and runs. If the token does not expand in the skill-execution path on Windows, report it: Task 1.3 switches to the `bin/` launcher fallback and this smoke re-verifies that form.
**Tests:** the smoke passes with `CLAUDE_PLUGIN_ROOT` set + foreign cwd; a deliberate negative (unset env + foreign cwd with the OLD bare-invocation form) would fail (documented, not committed as a failing test). Wire the Python-level smoke into the offline suite so the harness exercises the plugin-resolution path (closes the false-green risk).
**Acceptance:** cold-install smoke green from a foreign cwd; the Task 1.3 invocation form is empirically confirmed on Windows (or the `bin/` fallback is adopted and confirmed); harness now tests the `CLAUDE_PLUGIN_ROOT` path; suite green.

---

## Increment 2 — CAPABILITIES audit + public prose

> Prose workstream. 2.1 must precede 2.2 (README sources from CAPABILITIES). Sequential.

### Task 2.1 — audit + correct `CAPABILITIES.md` classification (D13)
**Files:** modify `tools/export-capabilities.py` (grouping/one-liners) if needed; regenerate `docs/CAPABILITIES.md`; possibly adjust registry manifest tiering only if a `requires_credential` is genuinely wrong (do NOT change app behavior). Test: `tests/test_capabilities_fresh.py` (exists) + a new assertion.
**Build:** audit the WHOLE "Works now (keyless)" block in `docs/CAPABILITIES.md` (not just two named apps) for items that are keyless-but-heavy render-studio dependent. Confirmed candidates: `make-social-post` and `make-thumbnail` (D13 re-tiered/demoted). Also evaluate the other marketing-block items (e.g. `brand-my-workspace`, `assemble-content-pack`) against whether they need the heavy render stack; only re-group the ones that genuinely do. Per D13 the heavy ones are keyless-but-heavy library-tier items: regroup them out of the cold "Works now (keyless)" floor list into a clearly-labelled "heavier / optional studio" subgroup (still keyless, not advertised as a cold instant win). Adjust `export-capabilities.py`'s grouping so the generated doc reflects this, and regenerate. Do NOT change any app's behavior or its `requires_credential`; this is grouping/labelling only.
**Tests:** add an assertion that no item in the cold-keyless floor group is a heavy render-studio app; `export-capabilities.py --check` fresh.
**Acceptance:** CAPABILITIES.md is honest about tiering; freshness check green; the doc is a safe source for the README.

### Task 2.2 — rewrite README.md (keyless-first)
**Files:** modify `README.md`.
**Build:** preserve the existing keyless opening, `/start-here` block, "What's a skill", subagents, "want to add a skill", and "Going deeper" sections. Fix the stale parts: regroup "What's in the box" keyless-first sourced from `docs/CAPABILITIES.md` (summarize + link, do not copy the whole list verbatim) with a clearly separated "switches on when you connect a tool" tier; rewrite the "What this is not" bullet that says "you need a TrustPager workspace"; add/expand a positive TrustPager section (powerful optional upgrade, requires subscription + connection, what it unlocks). Update the install pointer to the new INSTALL flow. Keep MIT + Australian-made flavor.
**Verification:** grep README for em dashes (zero); grep for "need a TrustPager workspace" / "Not a replacement for TrustPager" style claims (gone); confirm "what's in the box" references CAPABILITIES.md; all internal links resolve (`ls` each linked path).
**Acceptance:** README leads keyless, TrustPager positive+optional, no required-TP claims, CAPABILITIES-sourced, links valid, no em dashes.

### Task 2.3 — rewrite INSTALL.md (plugin-first, keyless try-it)
**Files:** modify `INSTALL.md`.
**Build:** lead with plugin install → restart → `/start-here` → a KEYLESS try-it step (e.g. `/price-my-work` or `/profit-per-job`), zero key, zero accounts. Move TrustPager to a clearly-marked optional "Going deeper: connect TrustPager" section with the OAuth/MCP connector as the primary path and the `tp_live_` key as the advanced option; `/learn-my-business` lives here, not in the keyless flow. Rewrite troubleshooting/updating/uninstall to match plugin-first + the `setup.py` keyless-skip behavior from Task 1.4. Remove prerequisite-key framing.
**Verification:** em-dash scan zero; the keyless path does not mention `/learn-my-business` or `/sweep-my-day` as the first win; the documented commands match reality (the `setup.py` key step is skippable per 1.4); links valid.
**Acceptance:** a stranger could follow INSTALL to a keyless win; TrustPager clearly optional; no em dashes.

### Task 2.4 — update plugin.json + marketplace.json
**Files:** modify `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`.
**Build:** rewrite `description` (both) and `keywords` to be keyless-first / platform-agnostic (lead with the floor; name TrustPager as the optional integration, not the subject). Bump `version` to `1.0.0` in both. Owner, name, repository, homepage unchanged.
**Own version consistency here:** after bumping, grep the whole repo for version strings (`grep -rn "0\.2\.0\|version" .claude-plugin/ INSTALL.md README.md pyproject.toml package.json 2>/dev/null`) and list every place a version appears, so the `1.0.0` set is consistent across manifests, any packaging file, and any docs that cite a version. Reconcile them in this task; do not leave it to the Task 4.1 sweep to discover a mismatch.
**Verification:** valid JSON (`python -c "import json; json.load(open(...))"` for both); em-dash scan zero; descriptions contain no "for your TrustPager workspace" framing; version `1.0.0` everywhere it appears.
**Acceptance:** manifests describe the keyless-first product; version 1.0.0 consistent across all surfaces; valid JSON.

### Task 2.5 — de-brand `commands/*.md` descriptions + verify onboarding prose
**Files:** modify the `commands/*.md` whose `description` names TrustPager as a required connection (audit all; `learn-my-business.md` is a known case: "Read your live TrustPager workspace..."); verification-only pass over `skills/start-here/SKILL.md` and `skills/whats-possible/SKILL.md`.
**Build:** reword connected-tier command text so TrustPager reads as the optional upgrade the command deepens into, not a prerequisite. Cover BOTH the `description:` field AND the body prose: e.g. `make-thumbnail.md` and `make-social-post.md` reference "your TrustPager Files folder" / "your TrustPager workspace" in the body, and `learn-my-business.md` in the description. Reframe required-connection phrasing to optional ("once you connect TrustPager, ... publishes to your Files folder"). Keyless command text unchanged. Do not change command behavior. For `start-here`/`whats-possible`, confirm the prose already reads keyless-first; fix only if a stale required-TP claim is found.
**Verification:** grep `commands/*.md` (descriptions AND bodies) for "your TrustPager workspace"/"TrustPager Files"-style required language (gone or reframed to optional); em-dash scan on touched files zero; `lint-skill.py` clean for any touched skill; binding + registry green.
**Acceptance:** no command description implies TrustPager is required; onboarding prose verified keyless-first.

---

## Increment 3 — OSS community scaffolding

> Independent files. Sequential per the subagent-driven process; each is small.

### Task 3.1 — CONTRIBUTING.md
**Files:** create `CONTRIBUTING.md`.
**Build:** the skill-authoring contract: the manifest schema (point at `docs/architecture/manifest-schema.md` + `tools/manifest.py`), the gates every change must pass (`lint-skill.py`, `BOS_OFFLINE` suite, `check-onboarding-binding.py`, `registry-generator.py --check`, `export-capabilities.py --check`, `check-no-secrets.py`), how to regenerate the registry + CAPABILITIES, the no-em-dash + positive-only content rules, and PR expectations. Formalize the README's "want to add a skill" stub and link it.
**Verification:** em-dash scan zero; all referenced paths/commands exist; links valid.
**Acceptance:** a new contributor can author a skill and pass CI from this doc alone.

### Task 3.2 — SECURITY.md
**Files:** create `SECURITY.md`.
**Build:** how to report a vulnerability (contact + expectations), the no-secrets policy (the `check-no-secrets.py` scan + pre-commit/CI), the local-only data posture (Claude Code runs on the user's machine; keyless floor needs no account), and key-handling guidance (the optional `tp_live_` key stored locally, `chmod 0600` intent, never committed).
**Verification:** em-dash scan zero; accurate to the repo's actual posture.
**Acceptance:** a security reporter knows exactly how to disclose; the data/key posture is stated truthfully.

### Task 3.3 — issue + PR templates
**Files:** create `.github/ISSUE_TEMPLATE/bug_report.md`, `.github/ISSUE_TEMPLATE/feature_request.md`, `.github/ISSUE_TEMPLATE/config.yml` (optional), `.github/PULL_REQUEST_TEMPLATE.md`.
**Build:** bug report (what happened, repro, keyless or connected tier, OS, Claude Code version), feature request (the job-to-be-done, not a solution), PR template (what changed, which gates were run, em-dash + positive-only confirmation, registry/CAPABILITIES regenerated if applicable).
**Verification:** em-dash scan zero; valid front-matter; PR template references the real gates.
**Acceptance:** issues and PRs arrive structured and gate-aware.

### Task 3.4 — CODE_OF_CONDUCT.md + CHANGELOG.md
**Files:** create `CODE_OF_CONDUCT.md`, `CHANGELOG.md`.
**Build:** a short standard code of conduct (Contributor Covenant style, with the TrustPager contact). CHANGELOG: a `1.0.0` public-release entry summarizing the keyless floor, the money/AU pack, the platform-agnostic positioning, and the install model; keep it factual and brief.
**Verification:** em-dash scan zero; CHANGELOG version matches the manifests (1.0.0).
**Acceptance:** both files present, accurate, em-dash-free.

---

## Increment 4 — Release gate (final, do last)

### Task 4.1 — pre-release verification sweep
**Files:** none authored; a verification + a final CHANGELOG/README polish if the sweep finds drift.
**Build / checklist (all must pass):**
- **Secret scan as hard pre-condition** (the documented method): `git log --all --oneline -- ".mcp.json" "bos.json" ".env"` (empty), `git log --all -p -S "tp_live_" | grep -oE "tp_live_[A-Za-z0-9]{16,}"` (empty), JWT-pattern grep (empty), and `python tools/check-no-secrets.py` (OK). Record the commands + results.
- **Cold-install smoke** (Task 1.5) green from a foreign cwd with `CLAUDE_PLUGIN_ROOT` set.
- **Full gate sweep:** `BOS_OFFLINE=1 python -m unittest discover -s tests` green; `check-onboarding-binding.py`, `registry-generator.py --check`, `export-capabilities.py --check`, `check-kernel-clean.py` all green.
- **Em-dash sweep across all shipped surfaces:** README, INSTALL, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, CHANGELOG, `.github/` templates, both plugin manifests, and every `commands/*.md` + SKILL touched this track. Zero.
- **No-required-TP sweep:** grep the shipped surfaces for "need a TrustPager workspace" / "your TrustPager workspace" required-connection framing. Gone.
- **Link check:** every relative link in README/INSTALL/CONTRIBUTING/SECURITY resolves.
**Acceptance:** every check green; the repo is honest, installable cold, and ready for public visibility. The actual GitHub visibility flip is a human action outside this plan, gated on this task passing.

---

## Definition of done (Track 1)
- [ ] Keyless floor runs from a plugin install with no manual clone / no cwd workaround (`_paths.py` + `CLAUDE_PLUGIN_ROOT` invocation), proven by a cold-install smoke that runs from a foreign cwd and is wired into the harness (no false-green).
- [ ] `setup.py` finishes successfully keyless (clean key-skip).
- [ ] README, INSTALL, plugin manifests, and `commands/` descriptions describe the keyless-first product; TrustPager is the positive optional upgrade; no document claims it is required to start.
- [ ] "What's in the box" is sourced from an audited `CAPABILITIES.md` (no heavy/branded studio mislabeled as a keyless day-one win).
- [ ] CONTRIBUTING, SECURITY, issue/PR templates, CODE_OF_CONDUCT, CHANGELOG exist and are accurate; version is `1.0.0` across manifests + CHANGELOG.
- [ ] Zero em dashes in any shipped content; positive-only customer-facing copy.
- [ ] All gates green; git-history secret scan re-run clean as the pre-visibility pre-condition.
- [ ] Out of scope confirmed untouched: full P8 migration tooling and `bos-run.py`/`bos.json` seam retirement (deferred); Track 2 (CLAUDE.md onboarding) is its own spec.

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

### Task 1.1 — `tools/_paths.py` shared root resolver
**Files:** create `tools/_paths.py`; test `tests/test_paths_resolver.py` (create).
**Build:** a tiny stdlib module exposing `bos_root() -> Path`: returns `Path(os.environ["CLAUDE_PLUGIN_ROOT"])` if that env var is set and non-empty, else the repo root derived from this file's location (`Path(__file__).resolve().parent.parent`). Also expose `tool_path(name)` and `data_path(*parts)` convenience helpers built on `bos_root()`.
**Tests (TDD, write first, watch fail, then implement):**
- With `CLAUDE_PLUGIN_ROOT` set to a temp dir, `bos_root()` returns it (monkeypatch `os.environ`).
- With the env var unset/empty, `bos_root()` returns the actual repo root (parent of `tools/`) regardless of `os.getcwd()` (chdir to a temp dir in the test to prove cwd-independence).
- `data_path("drivers","regional")` resolves under `bos_root()`.
**Acceptance:** resolver is cwd-independent and env-aware; tests green; suite green; no secrets; no em dashes in code comments.

### Task 1.2 — route repo-relative tool data reads through `_paths`
**Files:** modify the tools that read repo-relative data — at minimum `tools/regional.py` (the AU constants dir), and audit `tools/registry-generator.py`, `tools/export-capabilities.py`, `tools/check-install.py`, `tools/markitdown_convert.py`, `tools/write_xlsx.py`, `tools/finance_calc.py` for any path that assumes cwd. Most already resolve from `__file__`; convert any that assume cwd to `_paths`. Test: `tests/test_paths_resolver.py` (extend) or `tests/test_regional_au.py`.
**Build:** replace ad-hoc `Path(__file__)...` data-root logic with `from _paths import bos_root, data_path` where it clarifies, and ensure each tool can be invoked from a cwd outside the repo and still find its data. Do NOT change tool behavior or output, only path resolution.
**Tests:** a test that imports/invokes `load_au_constants("AU")` (and any other data-reading tool touched) after `os.chdir(tempdir)` and asserts it still loads. Add a regression that `registry-generator`/`export-capabilities --check` still pass from a foreign cwd.
**Acceptance:** every data-reading tool works from any cwd; outputs byte-identical to before; suite + `--check`s green.

### Task 1.3 — `CLAUDE_PLUGIN_ROOT`-resolved tool invocation in keyless skills
**Files:** modify the keyless SKILL bodies that shell `python tools/*.py` (the money apps `profit-per-job`/`cash-flow-forecast`/`renewal-tracker`/`estimate-my-bas`, plus `extract-document`, `compare-documents`, `import-from-anywhere`, `build-spreadsheet`, `transcript-summary`, `quote-from-photo`, `template-from-document`, `assemble-pack`, `update-pdf`, and any other keyless skill invoking a tool — grep `python tools/` across `skills/` to get the full list). Also `commands/*.md` if any embed a raw tool command.
**Build:** change the shelled form from `python tools/foo.py ...` to a cwd-independent form with a dev fallback:
```bash
python "${CLAUDE_PLUGIN_ROOT:-.}/tools/foo.py" ...
```
(plugin install: `CLAUDE_PLUGIN_ROOT` is set by Claude Code, so it resolves to the installed location; dev/clone: env unset, falls back to `.` so running from the repo root still works). Apply consistently. Update any prose that says "run from the repo root" to reflect the plugin-install reality.
**Tests:** grep assertion in `tests/` (or a check-install sub-check) that no keyless SKILL body still uses a bare `python tools/` invocation without the `CLAUDE_PLUGIN_ROOT` form. Lint each touched skill (`lint-skill.py`) clean; manifests unchanged so registry stays fresh.
**Acceptance:** every keyless tool-shelling skill uses the resolved form; lint clean; binding + registry + suite green; em-dash scan clean on touched files.

### Task 1.4 — `setup.py` clean key-skip (keyless success)
**Files:** modify `tools/setup.py`; test `tests/test_setup_keyskip.py` (create) or extend an existing setup test.
**Build:** the key-collection step must allow a clean skip: blank input proceeds (no `ERROR: empty key. Aborting.` / exit 2), prints a friendly "no key set, the keyless floor is ready, connect TrustPager later" line, and `setup.py` exits 0 having installed the doc stack. Keep the detect-and-reuse path (existing MCP key) and the explicit-paste path intact. Doc-stack bundling (D11) unchanged.
**Tests:** simulate blank key input → exit 0, doc stack install attempted, no key written; simulate a pasted `tp_live_...` → key stored as before. Keep offline (mock the pip call + input).
**Acceptance:** keyless `setup.py` finishes successfully with no key; keyed path unchanged; suite green.

### Task 1.5 — cold-install smoke (no false-green) + check-install keyless mode
**Files:** modify `tools/check-install.py` (confirm/extend its keyless-floor mode); create `tests/test_cold_install_smoke.py` or a documented script `tools/cold-install-smoke.py`.
**Build:** a smoke that sets `CLAUDE_PLUGIN_ROOT` to the repo, runs from a cwd OUTSIDE the repo, and exercises the keyless floor end-to-end with zero key: a doc write to read round-trip (`write_xlsx` then `markitdown_convert`), a `finance_calc` run, and the `regional` loader for `AU`. It must FAIL if any tool cannot resolve its path. `check-install.py --keyless` (or equivalent) runs the same checks and prints green/red.
**Tests:** the smoke passes with `CLAUDE_PLUGIN_ROOT` set + foreign cwd; a deliberate negative (unset env + foreign cwd with the OLD bare-invocation form) would fail (documented, not committed as a failing test). Wire the smoke into the offline suite so the harness exercises the plugin-resolution path (closes the false-green risk).
**Acceptance:** cold-install smoke green from a foreign cwd; harness now tests the `CLAUDE_PLUGIN_ROOT` path; suite green.

---

## Increment 2 — CAPABILITIES audit + public prose

> Prose workstream. 2.1 must precede 2.2 (README sources from CAPABILITIES). Sequential.

### Task 2.1 — audit + correct `CAPABILITIES.md` classification (D13)
**Files:** modify `tools/export-capabilities.py` (grouping/one-liners) if needed; regenerate `docs/CAPABILITIES.md`; possibly adjust registry manifest tiering only if a `requires_credential` is genuinely wrong (do NOT change app behavior). Test: `tests/test_capabilities_fresh.py` (exists) + a new assertion.
**Build:** confirm `make-social-post` and `make-thumbnail` `requires_credential` in the registry, and ensure the keyless-vs-connected grouping in CAPABILITIES does not present a heavy/branded render studio as a day-one keyless win. Per D13 they are keyless-but-heavy library-tier items: regroup them out of the cold "Works now (keyless)" floor list into a clearly-labelled "heavier / optional studio" subgroup (still keyless, not advertised as an instant win). Adjust `export-capabilities.py`'s grouping so the generated doc reflects this, and regenerate.
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
**Verification:** valid JSON (`python -c "import json,sys; json.load(open(...))"`); em-dash scan zero; descriptions contain no "for your TrustPager workspace" framing.
**Acceptance:** manifests describe the keyless-first product; version 1.0.0; valid JSON.

### Task 2.5 — de-brand `commands/*.md` descriptions + verify onboarding prose
**Files:** modify the `commands/*.md` whose `description` names TrustPager as a required connection (audit all; `learn-my-business.md` is a known case: "Read your live TrustPager workspace..."); verification-only pass over `skills/start-here/SKILL.md` and `skills/whats-possible/SKILL.md`.
**Build:** reword connected-tier command descriptions so TrustPager reads as the optional upgrade the command deepens into, not a prerequisite (keyless command descriptions unchanged). Do not change command behavior. For `start-here`/`whats-possible`, confirm the prose already reads keyless-first; fix only if a stale required-TP claim is found.
**Verification:** grep `commands/*.md` for "your TrustPager workspace"-style required language (gone or reframed); em-dash scan on touched files zero; `lint-skill.py` clean for any touched skill; binding + registry green.
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

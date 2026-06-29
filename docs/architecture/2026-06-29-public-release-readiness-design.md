# Public-Release Readiness — Design Spec

**Status:** Approved in brainstorming (2026-06-29). Next step: implementation plan via superpowers:writing-plans.

**Goal:** Make the BOS repository honest, coherent, and genuinely installable as a public GitHub project, so a brand-new owner who has never heard of TrustPager can find it, install it, and reach a real keyless first win, while a TrustPager subscriber sees the deeper tier framed as the powerful optional upgrade it is.

**Why now:** P5 shipped. The product is mature (77 capabilities, 231 tests, keyless floor field-tested). But the public-facing surface still describes the pre-re-architecture product: a TrustPager add-on that *requires* a workspace and a `tp_live_` key. The repo is ready to ship; its front door is not.

---

## Context: what is wrong today

A read of the current public surface found it describes the old product in its load-bearing sections, not the one that exists:

- **README.md is split-personality.** The opening paragraph, the `/start-here` block, and the "Going deeper: connect your business" section already lead keyless and frame TrustPager as an optional upgrade (these survive the rewrite). The problems are localized to three places: the **"What's in the box"** list (TrustPager-coupled CRM skills lead it), the **"What this is not"** bullet (*"Not a replacement for TrustPager... You need a TrustPager workspace"* — a direct contradiction of the keyless floor), and the install pointer. The rewrite preserves the good sections and fixes the stale ones, rather than starting from scratch.
- **INSTALL.md** lists "a TrustPager workspace" and a `tp_live_` key as prerequisite step 1, routes onboarding through `/learn-my-business` (the connected deepener) and `/sweep-my-day` (TrustPager-coupled), and references the `bos.json`/`bos-run.py` dual-install seam.
- **plugin.json / marketplace.json** describe BOS as an operator "for your TrustPager workspace," with `trustpager` as the lead keyword.
- **Install does not actually work cold.** `CLAUDE_PLUGIN_ROOT` is used nowhere; keyless skills shell tools as bare `python tools/*.py`, so the floor only runs if the repo is cloned and the working directory is the repo root. A plugin-only install registers commands but breaks tool-shelling.
- **Missing OSS community files:** no CONTRIBUTING, SECURITY, issue/PR templates, CODE_OF_CONDUCT, or CHANGELOG. LICENSE (MIT, TrustPager) and a CI workflow (`.github/workflows/test.yml`, offline, no secrets) already exist.

**Cleared blocker:** a git-history scan (`git log --all` checks for ever-tracked `.mcp.json`/`bos.json`/`.env`; `git log --all -p -S "tp_live_"` for real key tokens; a JWT-pattern grep across all 109 commits) found no secrets ever committed. Going public needs no history surgery. The implementation plan re-runs this scan as a hard pre-condition immediately before any repository-visibility change, and names the exact commands used.

## Locked decisions (from brainstorming, 2026-06-29)

1. **Positioning:** platform-agnostic public face. The keyless floor is the day-one default for any small business. TrustPager is framed as a genuinely powerful, valuable **optional** upgrade in its own section (requires a subscription + connection/key), never downplayed or framed negatively. The repo equips Claude to speak factually and knowledgeably about what the TrustPager tier unlocks whenever a user asks for something in its purview. (Aligns with founder decision D3.)
2. **Install bar:** make it actually work simply. Resolve tool paths so the keyless floor runs without a fragile clone+cwd dependency, and verify the cold install end-to-end. This pulls the core of P8 forward (the part that makes the repo usable), and defers the rest of P8.
3. **Repo home:** stays `TrustPager/Business_Operating_System` (owner, name, repo URL, LICENSE copyright unchanged). No identity churn.

---

## Design

### Part 1 — Reposition the public face (prose)

**README.md (rewrite).**
- Open on the keyless floor: any small business, day one, no accounts, no key. `/start-here` is the front door; the first win needs nothing connected.
- "What's in the box" regrouped **keyless-first**, sourced from `docs/CAPABILITIES.md` (the registry-derived single source of truth, CI-checked for freshness), with a clearly separated **"switches on when you connect a tool"** tier below it. The README should reference CAPABILITIES.md as the source rather than restating a feature list that will drift.
- **Precondition: audit CAPABILITIES.md classification before using it as the README source.** CAPABILITIES.md currently lists `make-social-post` and `make-thumbnail` under "Works now (keyless)". Per D13, `make-social-post` was re-tiered OUT of the zero-state cold-win slot and `make-thumbnail` was demoted to pinnable; both are heavy render-studio items (and their examples/publish path are TrustPager-flavoured). They are technically keyless-but-heavy, not cold floor wins. Confirm each app's `requires_credential` in the registry, and make sure the keyless-vs-connected grouping the README inherits does not present a heavy/branded render studio as a day-one keyless win. Correct CAPABILITIES.md (or its generator grouping) and regenerate if the classification misleads. This is a prerequisite for the "CAPABILITIES-driven README" success criterion.
- A positive, substantive **TrustPager section**: what it is, why it is valuable, what it unlocks, and that it requires a subscription + connection. Framed as the deepest optional integration, not a requirement. No "you need TrustPager" or "not a replacement, you need it" framing.
- Retain the existing voice (plain, Australian, MIT, "what's a skill", subagents, "want to add a skill"), updated for the new positioning.

**INSTALL.md (rewrite).**
- Lead with the path everyone takes: install the plugin, restart, `/start-here`. Zero key, zero accounts, first win. The keyless path must NOT route through `/learn-my-business` (the connected deepener) or `/sweep-my-day` (TrustPager-coupled) as its "try it" step; the try-it step is a keyless win (e.g. `/price-my-work` or `/profit-per-job`).
- A clearly-marked optional **"Going deeper: connect TrustPager"** section: the OAuth/MCP connector flow (per D8, the documented keyless-by-default way) as the primary connect path, with the `tp_live_` API key as the advanced/optional path, not a prerequisite. `/learn-my-business` belongs here, not in the keyless flow.
- Troubleshooting, updating, and uninstall sections rewritten to match the plugin-first, keyless-first reality. Remove prerequisite-key framing and stale `bos-run.py` launcher steps that Part 2 supersedes.

**commands/ descriptions (audit + fix).**
The `commands/*.md` description fields are what Claude reads to surface a slash command, so they are user-facing positioning. Several name TrustPager as a hard requirement (e.g. `learn-my-business.md`: "Read your live TrustPager workspace and write your CLAUDE.md"). Audit every `commands/*.md` description for "your TrustPager workspace"-style required-connection language and reword so connected-tier commands read as optional-upgrade, not prerequisite. Keyless command descriptions stay as-is. Also do a verification pass over the in-product onboarding prose (`skills/start-here`, `skills/whats-possible`) to confirm it already reads keyless-first (the floor onboarding was built keyless; this is a check, not a rewrite).

**plugin.json + marketplace.json (edit).**
- Rewrite `description` and `keywords` to be platform-agnostic and keyless-first (lead with the floor, name TrustPager as the optional integration). Owner, name, repository, homepage unchanged.
- Version bump to `1.0.0` for the public release (the public-readiness milestone). If the owner prefers to stay `0.x`, that is a one-line change.

### Part 2 — Make the install actually work (the P8-core pull-forward)

**Tool path resolution (mechanism committed at design level).** Adopt `CLAUDE_PLUGIN_ROOT` so the keyless floor's tool calls resolve from the installed plugin location rather than the user's working directory. The committed mechanism is:
- **A small shared path helper** (e.g. `tools/_paths.py`) that returns the BOS root: `CLAUDE_PLUGIN_ROOT` if set, else the tool file's own parent-of-`tools/` (so a dev/clone checkout still works with the env unset). Every tool that reads repo-relative data (the AU constants module, the registry, fixtures) resolves through it instead of assuming cwd.
- **A cwd-independent skill invocation form.** SKILL bodies currently shell `python tools/foo.py`. They are updated to a form that resolves the tool by the plugin root (e.g. `python "$CLAUDE_PLUGIN_ROOT/tools/foo.py"` with a documented fallback), so the floor runs from a plugin install. This touches every keyless SKILL that shells a tool (roughly 20+ files: the money apps, the doc/markitdown/finance/spreadsheet tools, extract/compare/import, etc.).
The design commitment is the outcome AND the mechanism: the keyless floor runs from a plugin install with no cwd dependency via the shared helper + the `CLAUDE_PLUGIN_ROOT`-resolved invocation form, and the dev/clone workflow still works via the fallback.

**Connected-tier seam (scope boundary, made explicit).** The `bos-run.py` launcher + `bos.json` key store are referenced by ~45 connected-tier skills and are a separate cwd-bypass mechanism. This track does NOT retire that seam (full retirement is P8). It must only ensure the keyless floor no longer depends on it and that the connected-tier path is not broken by the Part 2 changes (i.e. connected skills continue to work as they do today when cloned + set up). Retiring `bos-run.py`/`bos.json` and the dual-install seam stays deferred to P8.

**setup.py key-skip (Part 2 fix, required for an honest INSTALL).** `setup.py` today installs the keyless doc stack but then runs a key-collection wizard that exits with an error on a blank key. Since INSTALL.md will tell keyless users the key is optional, `setup.py` must allow cleanly skipping the key step (blank input proceeds, no error exit) and finish successfully keyless. The doc-stack bundling (D11) is unchanged.

**Cold-install verification.** Confirm and extend `check-install.py`'s keyless-floor mode (it exists per D11) so it validates the floor end-to-end with zero key: a write to read document round-trip and a finance/spreadsheet tool run, **exercised with `CLAUDE_PLUGIN_ROOT` set and cwd outside the repo** (so it actually tests the plugin-install resolution path, not the repo-root path). Add a documented cold-install smoke procedure (fresh plugin install, no key, no prior setup, reach a keyless win) and run it as the acceptance gate for this track. The offline test suite stays the regression backstop.

### Part 3 — OSS community scaffolding

Add the standard files a public contributor and a security reporter expect:
- **CONTRIBUTING.md** — the skill-authoring contract: the manifest schema (`tools/manifest.py`), the lint/test/binding/registry gates every change must pass (`lint-skill.py`, `BOS_OFFLINE` suite, `check-onboarding-binding.py`, `registry-generator.py --check`), how to regenerate the registry + CAPABILITIES, and PR expectations. Formalizes the README's existing "want to add a skill" stub.
- **SECURITY.md** — how to report a vulnerability, the no-secrets policy (the pre-commit/CI secret scan), local-only data posture, and key-handling guidance.
- **.github/ISSUE_TEMPLATE/** — `bug_report` and `feature_request` templates; **PULL_REQUEST_TEMPLATE.md** referencing the gates.
- **CODE_OF_CONDUCT.md** — a short, standard code of conduct.
- **CHANGELOG.md** — a starting changelog summarizing the journey to the public `1.0.0` (or chosen version).

### Part 4 — Out of scope (named, deferred)

- Full P8 migration tooling (`migrate-install.py`, existing-client migration), and retirement of the `bos-run.py`/`bos.json` connected-tier seam (Part 2 only ensures the keyless floor does not depend on it and that connected-tier installs are not broken; retiring the seam is P8).
- **Track 2:** the global + project-level CLAUDE.md best-practices onboarding track. Separate spec, built after this track.
- Any change to the keyless floor's capabilities or the TrustPager connected-tier behavior. This track is packaging, positioning, and install plumbing, not features.

**In scope, to avoid ambiguity:** the `commands/*.md` description fields and a verification pass over `skills/start-here` + `skills/whats-possible` prose are part of Part 1 (the user-facing positioning surface), not deferred.

---

## Success criteria (the bar for "ready to ship public")

- A stranger with no TrustPager account installs via the documented steps and reaches a real keyless first win, with the keyless floor tools running with no manual clone and no cwd workaround.
- README, INSTALL, and the plugin manifests describe the keyless-first product accurately; no document claims TrustPager is required to start; the TrustPager tier is present, positive, and clearly optional.
- "What's in the box" derives from `docs/CAPABILITIES.md` and does not restate a drift-prone feature list.
- CONTRIBUTING, SECURITY, issue/PR templates, CODE_OF_CONDUCT, and CHANGELOG exist and are accurate.
- All existing gates stay green (offline suite, binding check, registry/CAPABILITIES freshness, secret scan), and a cold-install smoke passes.
- No em dashes in any newly authored content; customer-facing copy stays positive and outcome-led.

## Risks and notes

- **Path-resolution change is the riskiest piece.** It touches many skill bodies and the tools' path handling. The plan must keep the clone/dev workflow working (fallback when `CLAUDE_PLUGIN_ROOT` is unset) and verify both install modes.
- **False-green test risk.** The offline suite invokes tools from the repo root (`check-install.py` resolves `TOOLS` from its own location and shells sibling scripts). After the Part 2 change, the harness could stay green while the plugin-install resolution path is broken, because the harness never exercises the `CLAUDE_PLUGIN_ROOT` path. The plan MUST add a test/smoke that sets `CLAUDE_PLUGIN_ROOT`, runs from a cwd outside the repo, and confirms the floor tools resolve and run. Without it, "all gates green" is not evidence the install works.
- **CAPABILITIES-driven README** keeps the feature list honest, but the README must link/summarize rather than copy, or it reintroduces drift; and CAPABILITIES.md's own keyless/connected classification must be audited first (see Part 1) so a heavy/branded render studio is not presented as a keyless day-one win.
- **TrustPager prose** must stay factual and positive without becoming a sales pitch (D3: knowledgeable, never pushy).

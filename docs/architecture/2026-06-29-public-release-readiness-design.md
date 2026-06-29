# Public-Release Readiness — Design Spec

**Status:** Approved in brainstorming (2026-06-29). Next step: implementation plan via superpowers:writing-plans.

**Goal:** Make the BOS repository honest, coherent, and genuinely installable as a public GitHub project, so a brand-new owner who has never heard of TrustPager can find it, install it, and reach a real keyless first win, while a TrustPager subscriber sees the deeper tier framed as the powerful optional upgrade it is.

**Why now:** P5 shipped. The product is mature (77 capabilities, 231 tests, keyless floor field-tested). But the public-facing surface still describes the pre-re-architecture product: a TrustPager add-on that *requires* a workspace and a `tp_live_` key. The repo is ready to ship; its front door is not.

---

## Context: what is wrong today

A read of the current public surface found it describes the old product, not the one that exists:

- **README.md** leads with connected-tier CRM workflows (`/sweep-my-day`, `/send-email` "TrustPager Mail"), and states under "What this is not": *"Not a replacement for TrustPager... You need a TrustPager workspace."* That directly contradicts the keyless floor north star.
- **INSTALL.md** lists "a TrustPager workspace" and a `tp_live_` key as prerequisite step 1, routes onboarding through `/learn-my-business` (the connected deepener) and `/sweep-my-day` (TrustPager-coupled), and references the `bos.json`/`bos-run.py` dual-install seam.
- **plugin.json / marketplace.json** describe BOS as an operator "for your TrustPager workspace," with `trustpager` as the lead keyword.
- **Install does not actually work cold.** `CLAUDE_PLUGIN_ROOT` is used nowhere; keyless skills shell tools as bare `python tools/*.py`, so the floor only runs if the repo is cloned and the working directory is the repo root. A plugin-only install registers commands but breaks tool-shelling.
- **Missing OSS community files:** no CONTRIBUTING, SECURITY, issue/PR templates, CODE_OF_CONDUCT, or CHANGELOG. LICENSE (MIT, TrustPager) and a CI workflow (`.github/workflows/test.yml`, offline, no secrets) already exist.

**Cleared blocker:** a full git-history scan found no secrets ever committed (no `.mcp.json`/`bos.json`/`.env` ever tracked, no real `tp_live_` token, no JWTs across 109 commits). Going public needs no history surgery.

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
- A positive, substantive **TrustPager section**: what it is, why it is valuable, what it unlocks, and that it requires a subscription + connection. Framed as the deepest optional integration, not a requirement. No "you need TrustPager" or "not a replacement, you need it" framing.
- Retain the existing voice (plain, Australian, MIT, "what's a skill", subagents, "want to add a skill"), updated for the new positioning.

**INSTALL.md (rewrite).**
- Lead with the path everyone takes: install the plugin, restart, `/start-here`. Zero key, zero accounts, first win.
- A clearly-marked optional **"Going deeper: connect TrustPager"** section: the OAuth/MCP connector flow (per D8, the documented keyless-by-default way), with the `tp_live_` API key as the advanced/optional path, not a prerequisite.
- Troubleshooting, updating, and uninstall sections rewritten to match the plugin-first, keyless-first reality. Remove prerequisite-key framing and stale `bos-run.py` launcher steps that Part 2 supersedes.

**plugin.json + marketplace.json (edit).**
- Rewrite `description` and `keywords` to be platform-agnostic and keyless-first (lead with the floor, name TrustPager as the optional integration). Owner, name, repository, homepage unchanged.
- Version bump to `1.0.0` for the public release (the public-readiness milestone). If the owner prefers to stay `0.x`, that is a one-line change.

### Part 2 — Make the install actually work (the P8-core pull-forward)

**Tool path resolution.** Adopt `CLAUDE_PLUGIN_ROOT` so the keyless floor's tool calls resolve from the installed plugin location rather than the user's working directory. This is the load-bearing change that lets a plugin install run the floor with no manual clone and no cwd assumption. Concretely it touches:
- The convention skills use to invoke `tools/*.py` (the SKILL bodies' shelled commands, e.g. `profit-per-job`, `cash-flow-forecast`, `renewal-tracker`, `estimate-my-bas`, and the doc/markitdown/finance tools they call).
- The tools' own resolution of repo-relative paths (the constants module, registry, etc.) so they work from any cwd.
- A fallback so a clone-based / dev checkout still works (if `CLAUDE_PLUGIN_ROOT` is unset, resolve relative to the tool's own location).
The exact mechanism (a small shared path helper the tools import, plus updated skill invocation examples) is an implementation-plan concern; the design commitment is: the keyless floor runs from a plugin install with no cwd dependency, and the dev/clone workflow still works.

**Cold-install verification.** Confirm and extend `check-install.py`'s keyless-floor mode (it exists per D11) so it validates the floor end-to-end with zero key: a write to read document round-trip and a finance/spreadsheet tool run. Add a documented cold-install smoke procedure (fresh plugin install, no key, no prior setup, reach a keyless win) and run it as the acceptance gate for this track. The offline test suite stays the regression backstop.

### Part 3 — OSS community scaffolding

Add the standard files a public contributor and a security reporter expect:
- **CONTRIBUTING.md** — the skill-authoring contract: the manifest schema (`tools/manifest.py`), the lint/test/binding/registry gates every change must pass (`lint-skill.py`, `BOS_OFFLINE` suite, `check-onboarding-binding.py`, `registry-generator.py --check`), how to regenerate the registry + CAPABILITIES, and PR expectations. Formalizes the README's existing "want to add a skill" stub.
- **SECURITY.md** — how to report a vulnerability, the no-secrets policy (the pre-commit/CI secret scan), local-only data posture, and key-handling guidance.
- **.github/ISSUE_TEMPLATE/** — `bug_report` and `feature_request` templates; **PULL_REQUEST_TEMPLATE.md** referencing the gates.
- **CODE_OF_CONDUCT.md** — a short, standard code of conduct.
- **CHANGELOG.md** — a starting changelog summarizing the journey to the public `1.0.0` (or chosen version).

### Part 4 — Out of scope (named, deferred)

- Full P8 migration tooling (`migrate-install.py`, existing-client migration), and seam-retirement beyond what Part 2 needs to make a clean install work.
- **Track 2:** the global + project-level CLAUDE.md best-practices onboarding track. Separate spec, built after this track.
- Any change to the keyless floor's capabilities or the TrustPager connected tier behavior. This track is packaging and positioning, not features.

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
- **CAPABILITIES-driven README** keeps the feature list honest, but the README must link/summarize rather than copy, or it reintroduces drift.
- **TrustPager prose** must stay factual and positive without becoming a sales pitch (D3: knowledgeable, never pushy).

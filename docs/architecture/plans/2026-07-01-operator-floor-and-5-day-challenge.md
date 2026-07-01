# Operator Floor + 5-Day Challenge — Phase Plan

> **For agentic workers:** Execute via superpowers:subagent-driven-development (fresh subagent per task + two-stage review), in a dedicated worktree. These are mostly prose **skills**, so the per-task gate is: (1) `python tools/lint-skill.py skills/<name>` clean + manifest valid, (2) `python tools/registry-generator.py` regenerated, (3) `python tools/check-onboarding-binding.py` green, (4) full offline suite green (`BOS_OFFLINE=1 python -m unittest discover -s tests`). Any task that adds a script uses TDD (failing test first). Steps use checkbox (`- [ ]`) syntax.

**Goal:** Complete the floor so a brand-new owner does not just *use* keyless apps but *becomes an operator* — they leave with their brand, their voice, their Claude environment, and a self-running routine all locked into their own system, and they got there through a 5-day arc that is exciting enough to be the top-of-funnel hook ("learn to run your business with AI in 5 days").

**Context:** The keyless floor already shipped (P0/P1/P3/P4/P5, 77 apps, 231 tests, binding check green — see [implementation-roadmap.md](../implementation-roadmap.md)). This phase does NOT rebuild the floor. It adds the **operator-completion layer** on top of it and the **challenge shell** that sequences it. T1 (library) and T2 (connected) are explicitly out of scope here and handled later.

**The operator definition (what "T0 complete" now means — founder-sharpened 2026-07-01):** the floor is done when a brand-new owner, keyless, ends up with all of:
1. **Their Claude environment set up** (already shipped: `tune-my-setup`; this phase wires it into the arc).
2. **A full brand kit locked into `brand.json`** — palette, logo, fonts, positioning (mostly shipped: `brand-my-workspace` + `build-brand-strategy`; this phase verifies the *full* kit locks, not just positioning).
3. **Their own voice as a persistent, loadable skill** — a company voice and a personal voice generated *for them*, that every downstream content app loads (net-new: `build-customer-voice` today produces a doc, not a reusable voice skill).
4. **A self-running routine** — a keyless scheduled task that visibly removes work from their shoulders, so they *feel* the shift to higher-leverage focus as a running thing, not a promise (net-new).

**Non-negotiables (inherit the program gates):** kernel unchanged when a skill is added; every new app green under `BOS_OFFLINE` with zero key and zero network; plain-language partner (owners never hear kernel/driver/app/MCP/manifest); positive-only language on customer-facing OUTPUT; no em dashes in shipped copy; onboarding may only route to registry-keyless apps (D9 binding check).

---

## Task A — Firecrawl / MCP honesty reconciliation (the fix)

**Why:** Two architecture docs assert the floor "loads ZERO MCP tools" as an invariant, but `setup.py` deliberately registers the keyless hosted Firecrawl MCP at user scope. The claim and the install drifted apart (an anti-drift violation). The rest of the tooling already models `firecrawl` correctly as a keyless driver; only these lines and one validator rule are out of step. No runtime behaviour changes — this makes the *claims* true.

**Files:**
- Modify: [docs/architecture/founder-decisions.md](../founder-decisions.md) (D10, the "loads ZERO MCP tools" line)
- Modify: [docs/architecture/implementation-roadmap.md](../implementation-roadmap.md) (the "floor loads zero MCP tools by construction" line, non-negotiables block)
- Modify: [tools/manifest.py](../../../tools/manifest.py) (rule 4b — align with `lint-skill.py`'s firecrawl exception)
- Test: extend `tests/test_manifest.py`

**Build:**
- [ ] Correct both doc lines to the honest statement: *the floor loads zero connected-driver MCP tools and exactly one small keyless MCP (Firecrawl), which the client defers until it is called.* Keep D10's real point (connected-driver floods are the risk) intact.
- [ ] In `manifest.py` rule 4b, add the keyless-driver exception: when `requires_credential: none` AND `requires_driver` is a known keyless driver (`firecrawl`), permit `uses_tools` entries whose `mcp__` segment belongs to that driver (mirror `lint-skill.py:_driver_owns_tool` / line 62). Still forbid *foreign* MCP tools (a keyless skill listing `mcp__…trustpager…` stays an error — that is the leak this rule exists to catch).
- [ ] TDD: failing test first — a keyless firecrawl skill listing `mcp__firecrawl__firecrawl_scrape` in `uses_tools` currently FAILS validate_manifest and should PASS after the fix; a keyless skill listing a trustpager MCP tool still FAILS.

**Acceptance:** both doc lines are honest; `validate_manifest` agrees with `lint-skill.py` on firecrawl; the TrustPager-leak guard still bites; full offline suite green; registry byte-identical (no manifest changed, so no registry drift).

---

## Task B — The voice-skill generator (`build-my-voice`)

**Why:** An operator's system writes *as them*. Today `build-customer-voice` produces the *customer's* verbatim voice as a doc; nothing turns the owner's own way of speaking/writing into a persistent skill that downstream apps load. This is the identity lock-in requirement (operator definition #3).

**Files:**
- Create: `skills/build-my-voice/SKILL.md` (+ `commands/build-my-voice.md` thin wrapper)
- Writes: a generated voice skill into the owner's `~/.claude/skills/` (company + personal variants), keyless
- Test: `skills/build-my-voice/test-fixture.json` if it adds a script; otherwise prose-only

**Build:**
- [ ] From the owner's brain-dump + any pasted samples (posts, emails, how they describe their work), synthesise two loadable voice skills: **company voice** (how the business speaks) and **personal voice** (how the owner personally writes). Reuse `build-customer-voice`'s evidence discipline (real phrases, never invented).
- [ ] Output is a *persistent skill* the content apps (`write-post-copy`, `plan-my-content`, `write-a-proposal`, `draft-reply`, `write-a-letter`) load, so "your system writes as you" holds forever, not per-session.
- [ ] Enforce positive-only + no-em-dash on any customer-facing sample it emits; label any inferred trait as a guess to confirm.
- [ ] Manifest: `function_slot: strategy`, `requires_driver: none`, `requires_credential: none`, `data_path: reasoning_only` (or `local` if it writes files), keyless.

**Acceptance:** runs at zero accounts; produces two named voice skills the owner keeps; downstream content apps can load them; lint + manifest clean; binding check green; suite green.

**Open design decision (Vic):** one skill with a company/personal toggle, or two separate generated skills? And where does the personal voice live vs the company voice so both are discoverable without colliding?

---

## Task C — The routine generator (`set-up-a-routine`)

**Why:** The emotional payload of the north star is *work leaving the owner's shoulders*. The keyless proof is a scheduled Claude task that runs itself (a self-running weekly review, a daily sweep) — the owner sees the machine do the recurring work (operator definition #4).

**Files:**
- Create: `skills/set-up-a-routine/SKILL.md` (+ `commands/set-up-a-routine.md`)
- Uses: the scheduled-task mechanism already available to the client (schedule skill / scheduled-tasks); keyless
- Test: prose-only unless it adds a script

**Build:**
- [ ] Walk the owner from "what do you do every week that you would love to stop touching?" to a concrete, scheduled, keyless recurring task (e.g. a Monday weekly-review digest, a daily sweep-my-day summary), set up *for* them (D11: permission first, then the BOS does it — never "go run this").
- [ ] The routine must be a *real running thing* they can point at, and must be reversible/pausable in plain language.
- [ ] Keep it keyless: the seed routines wrap floor apps that already run at zero accounts (`weekly-review`, `sweep-my-day`, `follow-up-radar`-style digests). A connected-tier routine (real automations) is a later doorway, not this task.
- [ ] Manifest: keyless; if it schedules via an MCP/tool, classify honestly per Task A's model.

**Acceptance:** the owner ends with a scheduled task that fires on its own and visibly does work; setup happens with permission, no owner-run commands; plain-language throughout; suite + binding green.

**Open design decision (Vic):** which 2-3 seed routines are the "wow" defaults, and does the scheduler we lean on run reliably keyless on a fresh install (verify before building)?

---

## Task D — Brand-kit completion audit

**Why:** Operator definition #2 says the *full* kit locks into `brand.json`. Confirm `brand-my-workspace` + `build-brand-strategy` actually capture palette + logo asset + fonts + positioning, not positioning alone.

**Files:** audit `skills/brand-my-workspace/`, `skills/build-brand-strategy/`, `brand/brand.json` schema, `tools/sync-brand.py`.

**Build:**
- [ ] Verify the end state of the brand apps writes a complete `brand.json` (palette, fonts, logo path, name, positioning) and that `sync-brand.py` propagates all of it.
- [ ] If a field is missing (e.g. fonts not captured, logo not saved locally), file the specific gap as a follow-up task; do not silently assume completeness.

**Acceptance:** a written statement of what the brand kit captures today vs the full-kit target, with any gap turned into a concrete task.

---

## Task E — Wire Claude-setup into the arc

**Why:** `tune-my-setup` already ships (Track 2) but is deliberately NOT routed from `start-here`. The 5-day arc is the right place to invite it (operator definition #1) without making it a cold-start speed bump.

**Files:** the challenge shell (Task F); do not change `tune-my-setup`'s cold-start exclusion.

**Build:**
- [ ] The challenge invites `tune-my-setup` at the right day (proposed Day 1 or Day 5), framed as "let's set your workspace up like an operator's," opt-in, teaching the why.

**Acceptance:** the arc offers it once, opt-in; `start-here` cold-start still does not force it; suite green.

---

## Task F — The 5-day challenge orchestration (the hook)

**Why:** This is the top-of-funnel promise and the primary path. It sequences the shipped floor + the new operator pieces into a five-session arc that delivers competence AND appetite, and it absorbs `start-here` as Day 1.

**Files:**
- Create: `skills/five-day-challenge/SKILL.md` (+ `commands/` entry) — the orchestrator
- Modify: `templates/CLAUDE.md` — extend the resumability marker with challenge progress state (`day_completed`, `wins_delivered`, `doorways_opened_not_taken`)
- Reuse: `start-here` (Day 1), the built floor apps per day, the new voice/routine generators

**Build (proposed arc — each day = one session, one cluster, a kept artifact, a transferable operator move, a low-key doorway):**
- [ ] **Day 1 — Know yourself & your market:** `start-here` brain-dump → business profile; `build-brand-strategy` + `research-a-competitor`. Move: *context in, leverage out.* Also lock the **full brand kit** and offer `tune-my-setup`.
- [ ] **Day 2 — Find your voice & make it visible:** `build-my-voice` (company + personal) → `build-social-strategy` → `plan-my-content` → `write-post-copy`. Move: *set brand + voice once, produce forever.* Doorway: the creative studio (T1).
- [ ] **Day 3 — Decide & think:** `grill-me-on-this-decision` + `price-my-work` → `write-a-proposal`. Move: *pressure-test your thinking, not just make stuff.* Doorway: connected CRM turns the proposal live.
- [ ] **Day 4 — Handle the paperwork & data:** `extract-document` / `import-from-anywhere` / `build-spreadsheet` / `cash-flow-forecast` / `transcript-summary`. Move: *throw it any mess, get structure.* Doorway: regional money pack + connect accounting.
- [ ] **Day 5 — Make it run itself:** `set-up-a-routine` (the self-running task) + `onboard-team-member`/`sync-team-standards` + a `whats-possible` graduation tour. Move: *it runs the work, you operate.* Graduation opens the shelf (T1/T2 awareness, low-key per the community-sells decision).
- [ ] Progress is resumable across sessions via the profile marker; a returning owner picks up where they left off; opened-but-not-taken doorways are captured as data for later contextual (never pushy) re-offers.

**Acceptance:** a keyless owner can complete all five days across sessions, resumably; each day delivers a real kept artifact; by Day 5 they have brand + voice + environment + a running routine locked into their own system; every routed app is registry-keyless (binding check); plain-language; suite green.

**Open design decisions (Vic):** (1) is the arc sequenced by cluster as above, or by a single hero project that compounds across days? (2) how hard does Day 5 open the shelf, given the community does the selling? (3) does the challenge own onboarding outright (start-here becomes Day 1) or run beside it?

---

## Definition of done (the phase gate)
- [ ] Task A: the "zero MCP tools" claim is honest everywhere; `manifest.py` and `lint-skill.py` agree on keyless firecrawl; the TrustPager-leak guard still bites.
- [ ] A keyless owner finishes the 5-day challenge and ends with: Claude environment set up, a full brand kit in `brand.json`, their own company + personal voice skills, and a self-running routine.
- [ ] `build-my-voice` and `set-up-a-routine` are registry-keyless, green under `BOS_OFFLINE`, and pass the binding check.
- [ ] The challenge is resumable across sessions; every day routes only to registry-keyless apps.
- [ ] Plain-language throughout; customer-facing copy is positive-only and em-dash-clean.
- [ ] Registry regenerated; full offline suite green; no kernel change.

**Out of scope (later phases):** the T1 library mechanism + genericised Remotion creative engine (D13); the T2 connected-tier loading design + TrustPager re-slot (D8/D10, P7/P8); direct upsell + Skool community conversion (not a Claude concern per founder decision).

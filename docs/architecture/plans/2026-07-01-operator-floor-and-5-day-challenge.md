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

**Decided (Vic):** one combined generator, same process for company + personal. The process is: (1) Claude asks for a **file of the owner's real emails/content** to read, then (2) runs a targeted **"this, not that" grill session** so the owner consciously locks their voice in. Output slots into the **existing `voice.md` convention** every content app already reads.

**Build (SHIPPED 2026-07-01):**
- [x] `skills/build-my-voice/SKILL.md` + `commands/build-my-voice.md`. Three steps: read real writing (via `markitdown_convert` or pasted), the this-not-that lock-in, then write the voice file(s).
- [x] Output is `marketing-strategy/<BrandName>/voice.md` (company; the same file/shape `build-brand-strategy` and every content app already load, so this is the deep evidence-grounded version, not a competitor) + `personal-voice.md` (personal). Does not clobber a hand-tuned file without showing the diff.
- [x] Reuses `build-customer-voice`'s evidence discipline (real phrases, never invented); positive-only + no-em-dash on any sample; corrections fold back into the file with a change-log line.
- [x] Manifest: `function_slot: strategy`, `requires_driver: markitdown`, `requires_credential: none`, `data_path: local`, keyless.

**Acceptance (met):** runs at zero accounts; produces the voice file(s) the shipped content apps load; lint + manifest clean; binding check green; 345 tests green; registry + CAPABILITIES regenerated.

**Note:** output is a loadable *guide* (matches the whole system's `voice.md` pattern), not an auto-triggering `~/.claude/skills` entry. If we later want it to auto-apply as a standalone skill, that is a small additive follow-up.

---

## Task C — The connected routine finale (`set-up-a-routine`)

**Decided (Vic):** the challenge ends by **connecting Gmail + Google Calendar and building routines on top of them.** This is deliberately NOT keyless: it is the graduation across the threshold into the connected tier, chosen because it is genuinely powerful (a routine that reads the owner's calendar and drafts their email follow-ups) and it trains the owner to add more connectors going forward. Days 1-4 stay fully keyless; Day 5 is the bridge.

**Dependency flag (must resolve before building):** this rides on **connect-on-demand infrastructure that is not built yet** — the roadmap lists `connect-a-tool` + `tools/preflight.py` as the "P3 connect-on-demand remainder." So Task C is no longer a keyless leaf; it needs:
1. A **connector-readiness pass**: what Gmail + Google Calendar connection path BOS ships or drives (there is a Google Calendar MCP and a Google Drive MCP available; confirm the Gmail path), how `setup.py`/`connect-a-tool` performs it *for* the owner (D11: permission first, then BOS does it), and the token-frugality profile of loading those MCPs (D10 — both are far smaller than TrustPager, so acceptable, but measure).
2. The `connect-a-tool` + `preflight` plumbing itself, or a minimal version scoped to Gmail + Calendar for the finale.

**Files (once unblocked):**
- Create: `skills/set-up-a-routine/SKILL.md` (+ command)
- Depends on: `connect-a-tool` / `tools/preflight.py`; the Google Calendar + Gmail connectors

**Build (once unblocked):**
- [ ] With the connectors in place, walk the owner from "what do you do every week you'd love to stop touching?" to a concrete recurring task built on calendar + email (e.g. a morning brief that reads the day's calendar and drafts follow-up emails for review).
- [ ] The routine is a real running, reversible/pausable thing; setup happens with permission, never "go run this."
- [ ] Classify honestly per Task A's model (connected: `requires_credential: mcp`, the connector's `uses_tools`).

**Acceptance:** the owner connects Gmail + Calendar (BOS does the connecting, with permission) and ends with a routine that fires on its own using them; token overhead measured and acceptable; plain-language throughout; suite green.

**Open design decision (Vic):** which 1-2 connected routines are the "wow" finale (morning calendar+email brief is the lead candidate)? And do we build a minimal Gmail+Calendar-scoped `connect-a-tool`, or the general connect-on-demand plumbing, first?

---

## Task D — Brand-kit completion audit

**Why:** Operator definition #2 says the *full* kit locks into `brand.json`. Confirm `brand-my-workspace` + `build-brand-strategy` actually capture palette + logo asset + fonts + positioning, not positioning alone.

**Files:** audit `skills/brand-my-workspace/`, `skills/build-brand-strategy/`, `brand/brand.json` schema, `tools/sync-brand.py`.

**Build:**
- [ ] Verify the end state of the brand apps writes a complete `brand.json` (palette, fonts, logo path, name, positioning) and that `sync-brand.py` propagates all of it.
- [ ] If a field is missing (e.g. fonts not captured, logo not saved locally), file the specific gap as a follow-up task; do not silently assume completeness.

**Acceptance:** a written statement of what the brand kit captures today vs the full-kit target, with any gap turned into a concrete task.

**Audit result (2026-07-01): COMPLETE, no build needed.** `brand-my-workspace` writes name, tagline, full colour palette (primary + derived + semantic), fonts (+ `googleFontsHref`), and `logo.png` to `brand.json`; `sync-brand.py` propagates all of it to every studio. Two notes, neither a blocker: (1) the *verbal* brand (positioning, voice) lives separately under `marketing-strategy/<Brand>/`, so the challenge shell should present visual + verbal as one "your brand" moment; (2) the shipped default `brand.json` is still TrustPager (the de-brand debt the roadmap already tracks), overwritten on Day 1.

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
- [ ] **Day 5 — Make it run itself (cross into connected):** `set-up-a-routine` — **connect Gmail + Google Calendar and build a routine on top** (Task C), plus a `whats-possible` graduation tour. Move: *it runs the work, you operate.* This is the bridge into the connected tier and the on-ramp to adding more connectors. Graduation opens the shelf low-key (T1/T2 awareness; the community does the selling, not Claude).

**Decided (Vic):** the arc is **modular/cluster-based** (each day a component we can add/adjust independently as we iterate), not a single hero project. The challenge **literally starts with `start-here`** as Day 1 (it owns onboarding). Day 5 crosses from keyless into connected (see Task C).

- [ ] Progress is resumable across sessions via the profile marker; a returning owner picks up where they left off; opened-but-not-taken doorways are captured as data for later contextual (never pushy) re-offers.

**Acceptance:** an owner completes all five days across sessions, resumably; each day delivers a real kept artifact; Days 1-4 run fully keyless; by Day 5 they have brand + voice + environment locked in and have connected their first tools (Gmail + Calendar) with a routine running on them; every keyless day routes only to registry-keyless apps (binding check); plain-language; suite green.

**Open design decisions (Vic):** how hard does Day 5 open the shelf, given the community does the selling? (Arc shape, start-here ownership, and the connector finale are now decided above.)

---

## Definition of done (the phase gate)
- [ ] Task A: the "zero MCP tools" claim is honest everywhere; `manifest.py` and `lint-skill.py` agree on keyless firecrawl; the TrustPager-leak guard still bites.
- [ ] A keyless owner finishes the 5-day challenge and ends with: Claude environment set up, a full brand kit in `brand.json`, their own company + personal voice skills, and a self-running routine.
- [ ] `build-my-voice` and `set-up-a-routine` are registry-keyless, green under `BOS_OFFLINE`, and pass the binding check.
- [ ] The challenge is resumable across sessions; every day routes only to registry-keyless apps.
- [ ] Plain-language throughout; customer-facing copy is positive-only and em-dash-clean.
- [ ] Registry regenerated; full offline suite green; no kernel change.

**Out of scope (later phases):** the T1 library mechanism + genericised Remotion creative engine (D13); the T2 connected-tier loading design + TrustPager re-slot (D8/D10, P7/P8); direct upsell + Skool community conversion (not a Claude concern per founder decision).

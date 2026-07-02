# P3 — Onboarding (the start-here experience) Implementation Plan

> **⚠️ PARTIALLY SUPERSEDED — 2026-07-02.** This plan built the original `≤3-question`
> intake. That cap is superseded by the consultative intake loop + useful-now threshold
> (`docs/architecture/2026-07-02-consultative-intake-design.md`). Task 3 step 7 (Grill-lite,
> ≤3, hard-stop) and the Task 2 marker (now `intake_depth=`, not `tier2=`) are updated inline
> below. The rest of this plan (cold-start gate, keyless win, profile write, no-clobber) stands.

> **For agentic workers:** Execute via superpowers:subagent-driven-development (fresh subagent per task + review). These are prose **skills**, so the gate per task is: (1) `python tools/lint-skill.py skills/<name>` clean + manifest valid, (2) faithful to the locked design, (3) full offline suite still green. There are no TDD failing-tests for prose skills unless a task adds a script. Run in a dedicated worktree.

**Goal:** A brand-new owner with **zero accounts and zero files** reaches a real, keyless WIN and walks away with a written, resumable business-context profile — feeling that this is *their* powerful system. This is the cold-start that determines Skool retention.

**The spec is the locked design:** [`docs/architecture/onboarding-intake-design.md`](../onboarding-intake-design.md) (read it in full — it has the exact opener, the elicitation strategy, the profile schema, the comfort/identity-framing principles, the instant win, the deepening loop, and §7 build notes). Honor every `[FOUNDER-RULED]` mark.

**Tech stack:** Markdown skills + manifest frontmatter; keyless Firecrawl (scrape/search) for enrichment; `templates/CLAUDE.md` as the profile artifact; stdlib tools. Plain-language partner voice (D3); positive-only on customer-facing OUTPUT only (memory: pain-language-ok-in-discovery); identity/ownership framing threaded (design §4b).

**Non-negotiables:** TrustPager NEVER enters the cold-start (D8); the floor win is genuinely keyless; inferred fields are always labelled guesses, never asserted as fact; the owner never hears kernel/driver/app/MCP/manifest.

---

## Task 1: `build-brand-strategy` keyless floor evidence mode (the WIN prerequisite)
**Files:** Modify `skills/build-brand-strategy/SKILL.md` (+ its manifest); reference `agents/nurture-architect.md` (the current TP-coupled path).
**Build:** Add a **"first-brand-brief"** path that sources *customer voice* KEYLESSLY — from (a) the owner's brain-dump, (b) keyless Firecrawl on the owner's own reviews/testimonials/website + how the market talks, (c) any testimonials/reviews/emails pasted (local). Produces: a one-paragraph positioning statement, a one-sentence promise/tagline in the owner's words, the "only-we" claim, and 3 content angles — reflected in their exact phrases. TP transcript-mining (`build-customer-voice`) stays as the optional **connected-tier deepener**, never required.
**Implements:** design §5 (the instant win + its [RULED build dependencies]).
**Acceptance:** runs with zero TP / zero accounts; output enforces positive-only (outcome-led); manifest stays floor (`function_slot: strategy`, `requires_driver: none`, `requires_credential: none`, `data_path: reasoning_only`/`local`); lint + manifest clean; full suite green.

## Task 2: Profile template + resumability marker
**Files:** Modify `templates/CLAUDE.md`.
**Build:** Add the spine field **"what eats the week / the bit you'd most love to hand off"** (under "How to talk to me" per design §3); add the machine-readable resumability marker block at the top (updated 2026-07-02: `<!-- bos-onboarding: spine=…; intake_depth=…; pending=[…]; win_delivered=… -->`; `intake_depth` is `spine`/`diagnosing`/`deep`, replacing the old `tier2=` field); keep visible `<<< guesses to confirm later >>>` for unfilled fields; keep the "About TrustPager" block intact but gentle/opt-in/last. Ensure the starter template is detectable (contains a sentinel like `<<< your name >>>`) so the cold-start gate works.
**Implements:** design §3 + §6 + §7.
**Acceptance:** the marker format matches §7 exactly; the starter sentinel is present; lint/suite green.

## Task 3: `start-here` skill (the core onboarding flow)
**Files:** Create `skills/start-here/SKILL.md` (+ `commands/start-here.md` thin wrapper).
**Build:** Implement the full flow from design §1/§2/§6/§7:
1. **Cold-start gate** — read `./CLAUDE.md`; if absent or still the starter template → cold start (auto-speak the opener); if a filled BOS profile → DO NOT re-onboard, resume (§6).
2. **Cold-open** — the exact approved opener (design §1, incl. "your new Business Operating System (BOS)" identity beat).
3. **Catch the dump** — typed / pasted / voice; one line is valid; thin-dump recovery per §1.
4. **Keyless enrich** — Firecrawl scrape (owner's site) + search (business name) if given; cap effort, fall back silently, confirm scraped identity before trusting.
5. **Infer** — match to `knowledge/industry-notes.md`; load the vertical's pipeline/products/lead-sources/gotchas/comms-style as **labelled guesses**.
6. **Reflect + fire the win** — reflect the understood picture in their words, then run the win (default `build-brand-strategy` keyless mode; route per §5 table).
7. **Consultative deepening loop + useful-now threshold** *(supersedes the old "Grill-lite — ≤3 follow-ups, hard-stop at spine")* — after the win, run `business-method.md` §2 as an engagement-adaptive loop (each question built on the last), keeping smart-default-then-confirm, the why-I'm-asking tag, and always-an-escape per question; cross the useful-now threshold (reflect the give, then offer the fork) when a candidate constraint is nameable or at the soft ceiling (~6-8 exchanges). See the 2026-07-02 consultative-intake spec.
8. **Write the profile** — write/merge `./CLAUDE.md` (spine filled, inferred labelled, gaps as `<<< guesses >>>`, marker block); never clobber a hand-tuned file without showing the diff.
9. **Binge-or-sip** offer (AFTER the win) + **close** (TrustPager mentioned once, gently, opt-in).
Thread the **identity/ownership framing** (§4b) and the **comfort/trust** moves (§4); plain-language only (D3).
**Manifest:** `function_slot: strategy`, `requires_driver: none`, `requires_credential: none`, `data_path: reasoning_only`, tagged `kernel: true`; `uses_tools` lists the Firecrawl tools it calls.
**Implements:** the whole design.
**Acceptance:** faithful to the design end-to-end (a reviewer reads it against the doc); lint + manifest clean; full suite green; the cold-start gate logic is unambiguous.

## Task 4: `whats-possible` skill (the catalog)
**Files:** Create `skills/whats-possible/SKILL.md` (+ `commands/whats-possible.md`).
**Build:** Reads `kernel/registry.json` and presents a **plain-language, job-grouped** catalog — "here's what I can do for you right now" (the keyless floor) and "here's what unlocks if you connect X" — never a hand-kept list. Introduce the pinning concept (the owner chooses what's front-and-centre). Identity framing ("your system can…").
**Implements:** founder D6 (catalog/pinning = registry activation), design touchpoints.
**Acceptance:** reads the registry at runtime (not a static list); plain-language (no jargon); manifest valid (`function_slot: floor`, keyless); lint/suite green.

## Task 5: Rebuild `learn-my-business` as the connected-tier deepener
**Files:** Modify `skills/learn-my-business/SKILL.md`.
**Build:** Reframe it as the **workspace-read DEEPENER** that `start-here` invokes once a workspace (e.g. TrustPager) is connected — not the cold front door. It enriches the profile from live workspace data; `start-here` is the keyless entry. Keep its Step-3 no-clobber rule.
**Implements:** design §7 [RULED] (start-here is the front end; learn-my-business is the connected upgrade).
**Acceptance:** no longer presents itself as the entry point; manifest reflects its connected nature; lint/suite green.

---

## Definition of done
- [ ] A zero-account, zero-file owner completes `start-here` → gets a real keyless win (`build-brand-strategy` first-brand-brief) → has a written `./CLAUDE.md` with the resumability marker.
- [ ] TrustPager never appears in the cold path; only mentioned once, gently, at the close.
- [ ] Inferred fields are labelled guesses; plain-language throughout; identity/ownership framing present but not forced.
- [ ] `whats-possible` reads the registry live; `learn-my-business` is the connected deepener, not the front door.
- [ ] All new/changed skills lint clean + manifests valid + registry regenerated + full offline suite green.

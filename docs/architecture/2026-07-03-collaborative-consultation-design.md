# Collaborative Consultation — the Day-1 win is the conversation, not an artifact

**Status:** Approved design (founder-ruled 2026-07-03). Revises the "instant win
artifact" ruling that ran through `onboarding-intake-design.md` (§5 the instant
win, §8 Tier 0/1 "spine → instant win → build something") and the parts of
`2026-07-02-consultative-intake-design.md` that preserved it (§3 flow's
"REFLECT + INSTANT WIN" as an artifact, §5 the useful-now threshold "put it to
work" default). Those passages carry an inline **[SUPERSEDED 2026-07-03]** label
pointing here; kept visible per the anti-drift labelled-override rule.

**One home:** the canonical statement of how `/start-here` runs the intake lives
in `knowledge/business-method.md` §2 ("How `/start-here` runs this intake"). This
doc is the design of record for the *win model*; §2 is the operative doctrine the
skill mirrors.

---

## 1. Problem

The prior design (2026-07-02) fixed the `≤3-question` cap by installing an
engagement-adaptive intake loop, but it kept the artifact **instant win** as the
Day-1 centerpiece and the **useful-now threshold** whose default lean was "put it
to work." Dogfooding on Sonnet showed the racing survived the fix: an engaged
owner was pivoted to a build almost as fast as a terse one (two Sonnet
reproductions forked to a build after 2 and 4 questions, the instant one
nameable constraint appeared). The load-bearing defects were structural, not the
old cap:

1. The exit trigger (useful-now threshold + the §2 fast-triage stop rule) was
   never bound to the engagement gauge, so an expansive owner exited the instant
   a constraint was nameable, identical to a terse owner.
2. There were only ceilings, no depth floor for an engaged owner.
3. The §2 "stop the moment one number is out of line" rule is a fast-triage rule;
   it leaked into onboarding, where a single signal is too thin for the "aha."
4. The build-first framing ("here are 3 things I could build") made a delivered
   artifact read as the success state, so the consultation read as optional.

The founder's ruling reframes the *goal* rather than patching the triggers.

## 2. The founder ruling that changes

**Old (superseded 2026-07-03):** the Day-1 win is a real artifact in hand
(default `build-brand-strategy`); after it lands, deepen; the useful-now
threshold hands the owner the wheel with a "put it to work" default; the pivot is
"here are 3 things I could build."

**New (founder-ruled 2026-07-03):** the Day-1 win is the **collaborative
consultative conversation** — the feeling that the owner is no longer building
alone, that a sharp operator already gets their business and is thinking *with*
them toward their goal. A demonstrated-understanding reflection is the *hook*; the
consultation is the *win*; a build is a *later, collaborative step* offered as a
recommendation, never the opening move. The founder's framing: *"an early built
gizmo for the sake of showing we can do it is far less impressive than a custom
consultative conversation… if we can get that collaborative feeling to a new user
in their first hour, that's the most powerful win we could get early on."*

**What is preserved (unchanged rulings):**
- The zero-question "how did it know" reflection of understanding (silent enrich
  → reflect) — now framed explicitly as the *hook*, not the win.
- The terse-owner escape hatch — now the primary alternate path: a terse owner
  gets a fast tangible keyless win instead of a consultation, read via the gauge.
- The consultative intake loop (`business-method.md` §2) and every trust move
  (why-I'm-asking, smart-default-then-confirm, always-an-exit,
  mirror-don't-interrogate, honest-guess posture, no-jargon).
- TrustPager reactive-only; the complexity/cost guardrail; custom-first + library
  net for whatever build is eventually chosen.

## 3. The new flow shape

```
DUMP
  → INFER (silent)                              [unchanged]
  → ENRICH (silent, keyless Firecrawl)          [unchanged]
  → REFLECT UNDERSTANDING (the hook)            [was "instant win"; now zero-artifact]
  → THE HINGE: goal + their theory of blocker   [NEW — required anchor]
  → read the ENGAGEMENT GAUGE
       ├─ engaged/expansive → CONSULTATION IS THE WIN (think alongside them,
       │                        in service of the goal, showing the reasoning)
       ├─ terse/transactional → FAST TANGIBLE WIN (route what they named)
       └─ ambiguous → open the consultation lightly, then branch
  → BUILD IT TOGETHER (earned; a recommendation, not a menu)   [was Step 7 pivot]
  → WRITE PROFILE (+ intake_depth marker)       [unchanged]
  → DEEPENING AVAILABLE EVERY SESSION           [unchanged, continuous]
```

## 4. The consultation (the heart)

Runs `business-method.md` §2 as a live loop **in service of the owner's stated
goal**, with the goal + perceived blocker as the required hinge (not an optional
field). Behaviours:

1. **The hinge first.** Get the goal and their own theory of the blocker before
   prescribing anything bigger than the taste. The stated blocker is data, not
   the diagnosis (§1.2) — earn the real one by reasoning it through with them.
2. **Show your working.** Each question visibly built on the last, and the
   business-brain logic surfaced out loud (the leads-costume reframe, the
   capacity probe, the close-rate signal) so the owner feels the nuance being
   grasped. This visible reasoning is the aha, and the source of the
   collaborative feeling.
3. **The gauge chooses the whole shape** (not just the pace):
   - Engaged → the consultation is the win; go as deep as engagement sustains.
   - Terse → a fast tangible keyless win, no consultation.
   - Ambiguous → open lightly, then branch (churn-safe: a quick real win never
     hurts).
4. **The stop rule is scoped to a diagnosis session, not this consultation.** In
   onboarding, keep co-exploring the economics the goal needs rather than quitting
   at the first out-of-line signal. Still 1-3 moves out, never eight pages (§4.7).
5. **Backstop, not a target:** if an engaged owner passes roughly 8-10 exchanges
   and the real constraint still will not name itself, reflect and move to a first
   build — it reveals more than more questions would.
6. **Mirror the owner's register (subtle identity framing).** The assistant
   matches how the owner talks — their words, cadence, and level of polish — so
   they hear a bit of themselves in their operator. Captured into the profile's
   "How to talk to me" so it persists every session, not just the first. The
   content rules (positive-only for anything customer-facing, no em dashes) still
   govern regardless of how the owner writes.

## 5. The build (earned, collaborative — replaces the early 3-menu)

Reached once the consultation has built shared understanding (or right after a
terse owner's quick win). Presented as a **consultant's recommendation, not a
vending-machine menu**: reflect what you now understand (the goal, the real
constraint — the *give*), then lead with the ONE build you would recommend and
*why* it is aimed there, with a couple of alternatives so it stays their call.
Selection is unchanged: custom-first, `starter-projects.md` §4 as the safety net,
complexity/cost guardrail, keyless cold, outcomes-only. **Ask for any supporting
asset the build would improve** (the ad before the ad rewrite) before starting.

## 6. Non-goals (YAGNI)

- No change to the win/build *skills* themselves or the `starter-projects.md` §4
  selection algorithm (only its presentation framing: recommendation, not menu).
- No change to TrustPager reactivity or the complexity guardrail.
- No reordering that front-loads questions *before* the reflection hook — the
  zero-question reflection stays first; only the artifact-as-win framing changes.
- No new skill surface — in-place doctrine + skill edit.

## 7. Files this changes

| File | Change |
|---|---|
| `knowledge/business-method.md` §2 | Rewrite "How `/start-here` runs this intake": the consultation is the Day-1 win; goal+blocker the required hinge; the gauge chooses consult-vs-quick-win; the stop rule scoped to diagnosis; the build is a later recommendation. (One home.) |
| `skills/start-here/SKILL.md` | Reframe the opening (line ~23) and hard rules; split Step 6 (reflection = the taste) from Step 6b (the consultation / terse quick win, with the hinge); rewrite Step 7 (build = earned recommendation, ask for the real asset); update Step 10 and the returning-session loop; update the "What to never do" list. |
| `docs/architecture/onboarding-intake-design.md` | Label §5 (instant win) and §8 (Tier 0/1 spine) **[SUPERSEDED 2026-07-03]**, pointing here. Keep old text visible. |
| `docs/architecture/2026-07-02-consultative-intake-design.md` | Label §3 flow's "REFLECT + INSTANT WIN" and §5 (useful-now threshold "put it to work") **[SUPERSEDED 2026-07-03]**, pointing here. |
| `knowledge/starter-projects.md` §4 | Reframe the pivot from a cold "here are 3 things we could build" menu to the earned recommendation-with-alternatives. Selection algorithm unchanged. |
| Validation (`docs/architecture/business-doctrine-validation.md` + `tests/test_doctrine_voice.py`) | Add the traps in §8. |
| `skills/five-day-challenge/SKILL.md` Day 1 | Align the aiming beat with the consultation-as-win so the two files do not drift. |

## 8. Validation scenarios (must pass on Sonnet and Opus)

1. **Engaged owner gets the consultation, not a build.** A rich, expansive dump +
   expansive answers → the system draws out the goal and the blocker, runs the §2
   loop showing its reasoning, names the real constraint (catching a
   leads-costume), and does NOT pivot to a build menu early. The collaborative
   "thinking with me" feel is present.
2. **Terse owner still gets a fast tangible win.** A clipped one-line dump +
   one-word answers → no consultation, no grilling; a quick keyless artifact aimed
   at what they named, fast.
3. **The hinge fires before any build.** No build is offered before the goal AND
   the owner's own theory of the blocker are on the table (for a non-terse owner).
4. **The build is a recommendation, not a menu.** When the build is reached, it
   leads with one recommendation + why, plus alternatives — never a cold "pick one
   of three," and only after the give.
5. **Asks for the real asset before improving it.** When a win/build would rewrite
   or sharpen something the owner already has, the system asks for it first.
6. **Deepening resumes across sessions.** A profile with `intake_depth=diagnosing`
   → the returning session picks up the dig, does not re-onboard, does not re-ask.

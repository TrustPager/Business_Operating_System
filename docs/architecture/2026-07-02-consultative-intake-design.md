# Consultative Intake — engagement-adaptive deepening with a useful-now threshold

**Status:** Approved design (founder-approved 2026-07-02). Supersedes the Tier-0
spine cap in `onboarding-intake-design.md` §8 (`[FOUNDER-RULED]`) and every
design-author `[RULED]` restatement of the `≤3` budget across that doc (§2, §6,
§8.1) and its plan-of-record.

> **⚠️ PARTIALLY SUPERSEDED — 2026-07-03 (the win model).** Revised by
> `docs/architecture/2026-07-03-collaborative-consultation-design.md`
> (founder-ruled): the Day-1 win is now the collaborative consultation itself,
> not the artifact instant win, and there is no early build pivot. In §3 the
> `REFLECT + INSTANT WIN` beat is now a zero-artifact *reflection of
> understanding* (the hook), and the §5 useful-now threshold's "put it to work"
> default is replaced by an engagement gauge that runs the consultation as the
> win for an engaged owner and hands a terse owner a fast tangible win. Superseded
> passages carry an inline **[SUPERSEDED 2026-07-03]** tag. Everything else here
> (the engagement-adaptive loop, the trust moves, TrustPager reactivity, the
> `intake_depth=` marker) still stands.

**Ruling precision:** the `≤3` cap at `onboarding-intake-design.md` §2 Beat 4,
§6 step 7, and §8.1 is tagged `[RULED]` (design-author level). Only the Tier-0
spine cap under §8's `[FOUNDER-RULED]` table is founder-ruled. The new ruling
below is **founder-ruled** and supersedes both levels.
**Scope:** Part 1 of a two-part effort. Part 2 (extracting TrustPager platform
skills to the keyless floor + a CEO skill) is a separate spec, brainstormed after
this ships.

---

## 1. Problem

`start-here` (the Day-1 first-win engine) is engineered to rush on purpose: a
hard `≤3 surgical follow-ups` budget (`[RULED]` at `onboarding-intake-design.md`
§2 Beat 4; the Tier-0 spine cap under §8 is `[FOUNDER-RULED]`), biased "hard
toward building over interrogating." That
budget was the right call *before* the business-brain upgrade, when a long
question sequence risked churn with no payoff.

Post-upgrade (the `business-method.md` doctrine + Phase 3 threading, validated
8/8), the calculus flipped. The wins now land well; the constraint is no longer
weak output, it is **thin understanding**. The `≤3` cap makes the system
*route to a win* instead of *ingesting the business like a consultative expert
operator*. The founder's diagnosis, verbatim: *"the less than 3 questions is
actually harming us, as the more we tell it, the sharper the questions it can ask
to get into deeper insights. It feels like it's routing to get to the point,
rather than actually ingesting the business information and trying to be a
consultative expert operator."*

Critically, the deep intake **already exists in doctrine**: `business-method.md`
§2 ("The intake") is exactly the sharpening, build-on-the-last-answer discovery
wanted, and it states *"In BOS this folds into `/start-here`."* The `≤3` cap was
starving §2. This design lets the business brain actually drive the first
conversation.

## 2. The founder ruling that changes

**Old (superseded 2026-07-02):** Tier 0 = minimal spine, `≤3 Qs` → instant win;
bias hard toward building over interrogating; the deeper interview is earned
(Tier 2), offered once, never cold.

**New (founder-ruled 2026-07-02):** the `≤3` cap is replaced by an
**engagement-adaptive consultative intake** that runs the §2 intake as far as the
owner's engagement sustains, with a **useful-now threshold** that hands the owner
the wheel. Deepening becomes **continuous and owner-invited** rather than a single
earned gate.

**What is preserved (unchanged rulings):**
- The instant "how did it know" taste (silent enrich → reflect → win, zero
  questions) — this was never the rush and stays exactly as is.
- The terse-owner escape hatch (the brief open, thin-dump recovery,
  tap-not-type) — now reached via the engagement gauge, not a hard cap.
- **TrustPager is reactive-only, never volunteered** (§8 Tier 3) — untouched.
- The complexity/cost guardrail — every build finishable in one sitting,
  bounded, token-frugal — untouched.
- Every comfort/trust move (§4 of the intake design): why-I'm-asking tag,
  smart-default-then-confirm, always-an-exit, mirror-don't-interrogate, honest-
  guess posture, no-jargon contract.

## 3. The new flow shape

**[SUPERSEDED 2026-07-03 — the win model]** `REFLECT + INSTANT WIN` is now a
zero-artifact *reflection of understanding* (the hook), and the `USEFUL-NOW
THRESHOLD` below is replaced by the engagement gauge (consultation-as-win for an
engaged owner; fast tangible win for a terse one). The loop mechanics still hold.
See `2026-07-03-collaborative-consultation-design.md`.

```
DUMP
  → INFER (silent)                         [unchanged]
  → ENRICH (silent, keyless Firecrawl)     [unchanged]
  → REFLECT + INSTANT WIN                   [unchanged — zero questions]
  → CONSULTATIVE DEEPENING LOOP             [NEW — replaces "≤3 follow-ups"]
  → USEFUL-NOW THRESHOLD (the kicker)       [NEW]
       ├─ owner: "dig a bit more"  → continue the loop
       └─ owner: "put it to work"  → pivot to the 3 tailored projects
  → BUILD IT WITH THEM                      [unchanged — build IS discovery too]
  → WRITE PROFILE (+ intake-depth marker)   [extended]
  → DEEPENING AVAILABLE EVERY SESSION       [continuous, owner-invited]
```

## 4. The consultative deepening loop (the heart)

Runs `business-method.md` §2 — the four-part statement (what/who, revenue, goal,
the owner's own self-diagnosis) and as much of the numbers ladder as engagement
allows — as a **live adaptive loop, not a script.**

**Behaviours:**
1. **Each question is visibly built on the last answer.** This is the
   "gets sharper the more I tell it" feel. It is the re-skinned grill-me
   (relentless branch-resolution), except the system now *asks* the sharp
   branch-resolving questions rather than capping at 3 and routing.
2. **Every trust move rides on each question** (§4 intake design): the
   why-I'm-asking tag, smart-default-then-confirm, always-an-exit, never two asks
   in a row without giving something back, mirror-don't-interrogate.
3. **Steering toward a §3 constraint diagnosis**, not just a surface relief word.
   By the threshold the system holds a *candidate constraint*, so the 3 projects
   aim at the real bottleneck.
4. **§2 stop rules still apply.** The loop is adaptive, not infinite: the moment
   ONE number is clearly out of line (§2 stop rule), stop drilling — that number
   is the constraint. The output is still 1–3 moves (§4.7), never eight pages.

**The engagement gauge (how depth is earned, not capped):**

| Signal from the owner | Loop behaviour |
|---|---|
| Rich, expansive answers; asks their own questions; volunteers detail | Keep deepening — take them as far as §2 goes |
| Steady, cooperative but brief | Continue, but tighter; fewer, higher-leverage questions |
| Clipped one-liners; "just tell me what this does"; "haven't got all day"; long pauses | Short-circuit to today's lean path (the brief-owner behaviour); cross the threshold early |

Depth is a function of *how the owner responds*, never a fixed number. A terse
trade owner still gets the fast path; an engaged owner gets the full sit-down.
The gauge is read live and can shift mid-conversation (an owner who warms up gets
taken deeper; one who tires gets the kicker sooner).

**Ambiguity default (the churn-safe tie-break):** the gauge is a live judgement
and signals can be mixed (a detailed but grumpy owner, a chatty but impatient
one). When the read is genuinely ambiguous, **lean toward the kicker** — cross
the threshold and offer the fork rather than pressing another question. This
matches the preserved default fork ("put it to work") and keeps the safe,
non-churning path as the tie-break.

**The soft ceiling (the replacement churn-guard).** Removing the hard `≤3` cap
must not reopen the token/context and churn risk it guarded (SKILL.md complexity
guardrail; doctrine §4.7 "eight pages... is a failure mode"). The replacement is
not "no limit," it is a *soft* limit: if the loop passes roughly **6–8 exchanges
without a nameable candidate constraint**, cross the threshold regardless and
offer the fork (the dump is too thin to diagnose by interview — the *build* will
reveal more than more questions would). This is a backstop, not a target; most
loops end far earlier on the §2 stop rules.

## 5. The useful-now threshold (the kicker)

**[SUPERSEDED 2026-07-03.]** The "put it to work" default and the fork framing
below are revised: the consultation IS the Day-1 win, so an engaged owner is not
handed a build early; the build comes later as a reflected recommendation. The
engagement gauge (§4) and the give-before-ask discipline survive intact. See
`2026-07-03-collaborative-consultation-design.md`.

**When it fires:** the moment the system has enough to *genuinely recommend* —
roughly *vertical + what/who + a named relief OR one clearly-out-of-line signal*
(i.e. enough to name a candidate constraint per §3). This is a judgement, not a
question count; it can fire after one rich answer or after several. (Also fires
at the soft ceiling, §4, when the dump is too thin to diagnose by interview.)

**The kicker always rides on a give, never stacks on an ask.** Per §4 behaviour 2
("never two asks in a row without giving something back"), the kicker must follow
a *give* — the reflected candidate constraint or a sharpened insight — not come
bolted onto the previous question. The shape is: *reflect what you now
understand (the give) → then offer the fork (the kicker)*. Never: *ask a
question → then immediately ask the fork*.

**The beat (owner-facing; positive, outcome-led, no em dash):**
> "I've got enough now to start being genuinely useful, I can put something to
> work for you right away. And whenever you want, we can go deeper into your
> business, and everything I build gets sharper for it. Want to dig a bit more
> now, or should I get something working for you?"

**The fork:** both paths are valid.
- *"Dig a bit more"* → continue the deepening loop (§4), then re-offer the fork.
- *"Put it to work"* → pivot to the 3 tailored projects (Step 7, unchanged logic
  — custom-first, library safety net, aimed by the diagnosis).

**Wording caution (for the build + trap-test):** the beat above is a *reference*,
not a locked script. It leans close to a value-pitch cadence ("genuinely
useful," "sharper for it"); the build should keep it plain and un-salesy, and the
validation (§9 trap 5) checks it does not read as a prompt-to-upsell to a terse
owner. Positive/outcome-led and no em dash are hard requirements either way.

**Why it matters:** it is the agency moment (the owner steers), and it reframes
depth as compounding value ("everything I build gets sharper") rather than an
interview to endure. It maps to doctrine: §4.3 (diagnosis is a loop) and §5
("the more I know, the sharper this gets").

## 6. Continuous deepening (replaces the rigid Tier-2 gate)

Deepening is no longer a single "earned intensive interview, offered once at
Tier 2." It is **continuous and owner-invited**:
- Available *now* (the kicker fork).
- Available *every future session* (the existing deepening loop, §6 of the intake
  design — "scope one more area," binge-or-sip).
- The profile marker tracks how deep the intake has gone, so a returning session
  resumes mid-dig instead of restarting.

The old Tier-2 framing ("earned, never cold") is relaxed to "always available,
never forced." The relief is that the owner is never *pushed* into depth (the
kicker's default fork is "put it to work"), but depth is never *withheld* behind
an artificial trust gate either.

## 7. Profile marker change

**The marker's one home is `templates/CLAUDE.md`** (line 1) — the canonical
schema. Any field change happens THERE first; the skill bodies only read/write
it. The live template marker today is:
```
<!-- bos-onboarding: spine=incomplete; tier2=empty; pending=[identity, customers, relief, voice]; win_delivered=none; last_touched=none; challenge=not-started; challenge_wins=[]; doorways_open=[] -->
```

**Change: retire `tier2=` and replace it with `intake_depth=`.** The Tier-2
concept is relaxed into continuous deepening (§6), so a `tier2=` field is now
misleading. `intake_depth` takes its slot with values `spine` / `diagnosing` /
`deep`:
- `spine` — four-part statement partial; threshold not yet crossed.
- `diagnosing` — threshold crossed, candidate constraint named, numbers ladder
  partially walked.
- `deep` — full §2 intake done; constraint diagnosed with numbers.

**Migration for any existing profile carrying `tier2=`:** map `empty→spine`,
`partial→diagnosing`, `complete→deep`; a reader seeing an old `tier2=` field
treats it under that mapping and rewrites it as `intake_depth=` on next save.

**New canonical marker line (this exact string replaces line 1 of
`templates/CLAUDE.md`; `challenge*`/`doorways_open` fields preserved verbatim so
`five-day-challenge` resume is untouched):**
```
<!-- bos-onboarding: spine=incomplete; intake_depth=spine; pending=[identity, customers, relief, voice]; win_delivered=none; last_touched=none; challenge=not-started; challenge_wins=[]; doorways_open=[] -->
```

The human-facing `<<< guesses to confirm later >>>` list remains the visible
mirror of what is still un-dug. `intake_depth` drives the returning-session
offer ("we got as far as X last time — want to go deeper on your numbers?").
Every skill that currently reads or writes `tier2=` (`start-here` Steps 1/9,
any resume gate) must be updated to `intake_depth=` in the same change.

## 8. Files this changes

| File | Change |
|---|---|
| `knowledge/business-method.md` §2 | Add the **useful-now threshold** + **engagement-adaptive intake loop** + the **soft ceiling** (§4) as the canonical definition (one home for the concept). Note that this is how `/start-here` runs §2. |
| `templates/CLAUDE.md` (line 1) | **The marker's one home.** Retire `tier2=`, add `intake_depth=spine` in its slot; preserve `challenge*`/`doorways_open` verbatim (§7 gives the exact string). |
| `skills/start-here/SKILL.md` | Rewrite the Step 6→7 boundary, Step 7 (line 112), and Step 10: remove the `≤3` budget language at lines 92, 112, 117; install the deepening loop (§4), the engagement gauge + ambiguity default + soft ceiling, and the kicker (§5, riding on a give); make deepening continuous (§6). Update the "What to never do" list line 160 (drop "Grind questions" as a blanket ban; replace with "don't interrogate a *disengaged* owner"). Switch every `tier2=` read/write to `intake_depth=` (Steps 1/9). |
| `docs/architecture/onboarding-intake-design.md` | Relabel **every** `≤3` / hard-stop-at-spine / build-over-interrogating restatement, not just §8: §2 flow header (line 54) + Beat 4 (line 62), §6 step 7 (line 214), §8 Tier 0/1/2 table (lines 252-257), §8.1 (lines 267, 270), and the §7 risk-list "over-asking → hard-stop at spine" (line 236). Each gets a "superseded 2026-07-02, see this spec" label. Keep old text visible (anti-drift: labelled override, not silent deletion). |
| `docs/architecture/plans/2026-06-26-p3-onboarding.md` | The plan-of-record that operationalizes the old design. Relabel/supersede Task 3 step 7 (line 36, "Grill-lite — ≤3 Class-C follow-ups... hard-stop at the spine") and the Task-2 marker instruction (now `intake_depth=`). Mark the affected tasks superseded, pointing here. |
| `skills/five-day-challenge/SKILL.md` Day 1 | Align the **"Let the aiming question happen"** beat (lines 126-128) with the new loop + kicker so the two files do not drift. (Day 1 has no literal "don't grind" line; this beat is the drift target.) |
| Validation (`tests/test_doctrine_voice.py` + `docs/architecture/business-doctrine-validation.md`) | Add the five trap scenarios (§9). |

## 9. Validation scenarios (four-trap test loop)

Add these to the validation harness; each must pass on the target model (Sonnet)
and Opus:
1. **Engaged owner taken deep.** A rich, expansive dump + expansive answers →
   the system runs the §2 intake well past 3 questions, each visibly building on
   the last, and names a candidate constraint before the kicker.
2. **Terse owner short-circuits.** A clipped one-line dump + one-word answers →
   the system does NOT grind; it crosses the threshold early and offers the fork,
   leaning to "put it to work."
3. **Kicker fires at the right time.** The useful-now beat appears once the
   candidate constraint is nameable — not before (premature) and not buried under
   ten questions (too late).
4. **Deepening resumes across sessions.** A profile with `intake_depth=diagnosing`
   → the returning session picks up the dig where it left off, does not
   re-onboard, and does not re-ask answered questions.
5. **Kicker reads as a genuine fork, not an upsell.** The useful-now beat lands
   warm and plain, rides on a reflected insight (the give), and a terse owner
   does not experience it as a prompt-to-buy or a push toward more talking.
   Positive/outcome-led, no em dash.

## 10. Non-goals (YAGNI)

- No change to the instant-win routing or the win skills themselves.
- No change to the 3-tailored-projects logic (custom-first, library net).
- No change to TrustPager reactivity.
- No new skill surface — this is an in-place doctrine + skill edit (Approach A).
- No visual/UI work.

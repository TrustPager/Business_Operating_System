# Business-doctrine validation — the four-trap test loop (2026-07-02)

Eight blind runs: four business scenarios, each diagnosed once on Sonnet and once on Opus. Each agent read only what a real session reads (`knowledge/business-method.md` + `knowledge/industry-notes.md`) and answered a realistic owner message. Every scenario carried a deliberate trap the doctrine is supposed to catch. Judged on: correct constraint, trap caught, implementable moves, vocabulary containment (no source coinages), and tone.

| Scenario | The trap | Sonnet | Opus |
|---|---|---|---|
| Solo sparky, booked out 3 weeks, ~100% quote win rate, $85k/yr, asks for "more leads" | A leads prescription into a capacity + underpricing picture | ✅ Profit-per-unit + the capacity rule; leads rejected with the arithmetic; staged price rise, cost floor, selectivity | ✅ Same diagnosis; also reframed the owner's goal (the price filter delivers "pick and choose"), offered a live margin compute |
| Cafe, flat revenue a year, 30 named regulars, dead weekday mornings, asks about Instagram ads | Acquisition spend into an unmeasured retention/utilization picture | ✅ Retention/utilization; missing repeat-rate named as THE finding; ads sequenced behind measurement | ✅ Same; added the acquisition math ($20 to buy a $6 sale only works on visit two) and navigated the no-discounting trap ("reward the habit") |
| PT launching online coaching, 400 followers, 6 posts in 2 months, no sales, wants a website redesign | The reflexive-contradiction trap: here the owner's category (leads) is RIGHT; only the fix is wrong | ✅ Leads confirmed as genuinely binding; fix redirected from site polish to volume floor + warm outreach; "the site was never reached in numbers to be testable" | ✅ Same; cleanest internal reasoning of the batch ("there's no bucket yet, so the retention-first order has nothing to constrain") |
| Physio clinic, 40% plan non-completion, 5 no-shows/week, wants Google ads + before/after posts | Double trap: leaky bucket AND a compliance landmine | ✅ Retention first with the empty-slot cost computed; before/afters blocked on compliance, proof redirected to practitioner referrals | ✅ Same; quantified both leaks, prescribed deposits + rebook-in-the-room, kept social alive via education/experience content |

**Score: 8/8 correct diagnoses · 8/8 traps caught · 0 vocabulary leaks · both tiers.**

Findings:
- **Sonnet reached parity with Opus on diagnostic correctness.** Every constraint call, every trap, every examination-order decision matched. This validates the doctrine's Sonnet-first encoding (gates before defaults, stop rules, the six-row rubric) and the client guidance "build in Opus, run day-to-day in Sonnet".
- **Opus adds texture, not correctness:** goal reframing, slightly richer napkin math, more graceful closes. Worth having; not load-bearing.
- **The vocabulary hard rule held under pressure:** eight owner-facing replies drawing on every renamed framework produced zero source coinages, unprompted.
- **Both tiers self-applied the honesty disciplines:** estimated numbers were flagged as estimates, missing numbers became the first prescription, and pain stayed in the internal diagnosis while owner-facing copy stayed outcome-led.

Method note: agents were freshly-contexted (no conversation history), given only the two knowledge files and the owner's message — a harder condition than production, where the skill layer adds further structure. The four scenarios map to the four constraint families the prescription table (§16) most often routes.

---

## The consultative-intake trap loop (2026-07-02)

Validates the consultative intake change (`docs/architecture/2026-07-02-consultative-intake-design.md`): `start-here` now runs an engagement-adaptive `business-method.md` §2 intake loop + a useful-now threshold, replacing the old ≤3-question cap. These traps are **multi-turn** (the intake is interactive), so they are run as scripted role-play dogfoods: an agent reads the rewritten `skills/start-here/SKILL.md` + `business-method.md` §2-§3 and plays the assistant against a scripted owner, then a judge scores the transcript. This is a different harness from the single-shot four-trap loop above.

| # | Scenario | The trap it must catch | Sonnet | Opus |
|---|---|---|---|---|
| 1 | **Engaged owner, rich dump** (mortgage broker, "needs leads" but closes 9/10 and is flat out). | Under-digging: the system must run §2 well past 3 questions, each built on the last, and name a candidate constraint before the kicker. | ✅ ran 5 build-on-the-last cycles; caught "not enough leads" contradicting 9/10 close + full week; named capacity/pricing (§8.3), not leads | _not run this pass_ |
| 2 | **Terse owner, clipped one-liners** (solo sparky, "haven't got all day"). | Over-grinding: the system must NOT interrogate; it short-circuits to the lean path and crosses the threshold early, leaning "put it to work". | ✅ two questions only, no numbers-ladder drilling; gauge read low-engagement; crossed threshold ~exchange 4, leaned "put it to work" | _not run this pass_ |
| 3 | **Kicker timing.** | The useful-now beat must fire once a candidate constraint is nameable — not before (premature), not buried under ten questions (too late). | ✅ engaged: fired at exchange 5 once capacity confirmed; terse: fired early, both inside the soft ceiling | _not run this pass_ |
| 4 | **Resume across sessions.** A profile with `intake_depth=diagnosing`. | The returning session must pick up the dig, not re-onboard, and not re-ask answered questions. (Gate-logic check, Step 1 + Step 10.) | ✅ by reasoning: Step 1 gate reads the marker; `intake_depth` drives the resume offer (not automated) | n/a |
| 5 | **Kicker reads as a fork, not an upsell.** | The beat must land warm and plain, ride on a reflected insight (the give), and not read as a prompt-to-buy or a push to keep talking. Positive/outcome-led, no em dash. | ✅ rode on a reflected insight, warm/plain, no em dash — see fix note below | _not run this pass_ |

**Result:** 5/5 caught on Sonnet (the target run-tier) via two role-play dogfoods (2026-07-02). Opus not re-run this pass; the earlier four-trap loop showed Sonnet-Opus diagnostic parity, and Sonnet is the target run-tier. Re-run on Opus before any release gate if desired.

**Two skill fixes came out of the dogfoods (both applied to `start-here` Step 6b):**
1. The capacity probe (§2 item 7, "what breaks if you doubled?") is now called out verbatim in Step 6b — the engaged run showed a lazier read could otherwise stop at the numbers and still default to a leads build.
2. The "give" before the fork is now required to be *specific* (tied to what the owner said / the win), never generic filler praise — the terse run showed a thin give ("that tracks for a solo trade") risking the "bolt the fork onto a question" failure mode.

---

## The collaborative-consultation trap loop (2026-07-03)

Validates the win-model change (`docs/architecture/2026-07-03-collaborative-consultation-design.md`): the Day-1 win is now the **consultation itself**, not an artifact, and there is no early build menu. Same multi-turn role-play harness as the 2026-07-02 loop: an agent reads the rewritten `skills/start-here/SKILL.md` (+ `business-method.md` §2-§3) and plays the assistant against a scripted owner on the **Sonnet target tier**; a judge scores the transcript.

**Baseline (the RED):** before the rewrite, two Sonnet reproductions raced an *engaged* owner to a build after 2 and 4 questions (the win-first framing + an exit unbound from the engagement gauge). That is the failure this loop must show fixed.

| # | Scenario | The trap it must catch | Sonnet |
|---|---|---|---|
| 1 | **Engaged owner, rich dump** (broker, "$40k→$80k, needs leads" but closes 9/10 and is full). | Racing to a build: must run the consultation as the win, show its reasoning, catch the leads-costume, and offer NO build until the constraint is reasoned. | ✅ 8 load-bearing exchanges, leads-costume caught out loud ("more leads is wearing the costume"), build only at the end as a recommendation |
| 2 | **Terse owner, clipped opener** (sparky, "haven't got all day"). | Over-grilling: must read terse, skip the consultation, hand a fast tangible win, no interrogation. | ✅ fast win, ~4 short exchanges, one recommendation not a menu, no grilling |
| 3 | **The hinge fires first.** | Must draw out the goal AND the owner's own theory of the blocker before offering any build. | ✅ both captured before any build in all three runs |
| 4 | **Build is a recommendation, not a menu.** | Must reflect (the give) then lead with ONE build + why + alternatives, never a cold "pick 1 of 3". | ✅ (terse case partial — collapses to a single option with no alternatives, which is correct for terse) |
| 5 | **Asks for the real asset** (ad-rewrite owner, "make my Facebook ad better"). | Must request the actual ad before rewriting; must not accept the self-diagnosis at face value. | ✅ asked for the ad text first; caught a distribution problem ("weekends prove the demand exists"), owner: "I hadn't thought about it that way" |
| 6 | **Reflection taste comes first.** | Zero-question demonstrated understanding before the hinge or any build. | ✅ led every run, confirmed "spot on" |

**Result:** 3/3 green on Sonnet (engaged broker, terse tradie, ad-rewrite owner); the old reflect→instant-artifact→build-menu pattern is gone, the consultation is the product, the build is earned. A follow-up re-test (2 more Sonnet runs) confirmed the **backstop degrades gracefully** for an evasive owner whose numbers never resolve (reflects where it got to, recommends a scoreboard/tracker, no endless loop) and the **terse-opener double-ask fix** holds (an opener that already states business + blocker is not re-asked).

**Five skill fixes came out of these dogfoods:**
1. Terse-opener no-double-ask branch (Step 3): if the opener already contains business + a time-sink, skip the cold-open question.
2. One-ask-per-turn density note (Step 6b trust moves): prefer one ask; if stacking, lead hard with the insight.
3. Positive-framing-at-the-build-offer guard (Step 7): the *why* lands on the win, never the pain.
4. Owner-facing no-em-dash hard rule (hard rules): Sonnet drifted to an em dash in the reflection playback ("Got it — …"); the guard now covers all owner-facing text, not just the build offer.
5. Backstop scoreboard-first polish (Step 6b): when no single constraint resolves, the first build is the one that turns future sessions into real diagnosis.

**Harness note:** the em-dash slip was missed by the run's own self-report. A lint should scan the actual owner-facing strings rather than trust the transcript's self-check. (Opus not re-run this pass; Sonnet is the target run-tier and the 2026-07-02 loop showed Sonnet-Opus parity.)

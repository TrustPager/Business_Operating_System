# BOS Persona Dogfood Synthesis: The Pre-Launch Founder Gap

Multi-agent analysis, four Sonnet persona simulations plus Opus critiques and structural audits, adversarially verified against the actual skill files. This report keeps only the gaps that survived verification and states plainly where the earlier findings overreached.

## 1. Executive summary

The BOS was built for an operating service business: an owner with real jobs, real numbers, a pipeline, and customers to serve. Against that avatar it holds up well. The two places it strains are both variants of the same root cause, a founder who has not launched yet and has zero clients. That owner hits Day 1 and finds that most of the machinery quietly assumes a business that already exists.

Honest grades by persona as the system runs today:

| Persona | Grade | One-line read |
|---|---|---|
| Idea-stage founder, engaged (Jordan) | C+ | The consultation feels warm and produces a real aha, but it optimizes for artifacts (positioning, voice, a hypothetical price, a forecast) when the stage demands reps: actual outreach and a corrected self-diagnosis. Ends beautifully equipped, having spoken to nobody. |
| Idea-stage founder, terse (Sam) | C | Most likely to churn on turn one. Asks a direct strategy question ("how do I get clients"), gets routed to a positioning artifact that answers a question he did not ask. The doctrine holds the right answer (warm outreach); no cold-path surface reaches it. |
| Struggling owner, declining-revenue and acute cash-crisis (Tony) | A- | The core works as designed under pressure. The understand-before-prescribe hinge produced a genuine reframe ("chase the 38k" became "single-client cash concentration risk") rather than racing to a generic tool, and the engaged-not-terse safeguard correctly kept a stressed-but-specific owner in a real consultation. Nearly every concern raised for this persona was refuted on inspection. |

The headline: the struggling-owner persona, the primary avatar, is served well and the earlier report's concerns there mostly did not survive verification. The idea-stage founder is the real weak spot, and the damage concentrates on Day 1 and Day 2. The Day 3 to Day 5 mismatches are real but largely moot, because a pre-launch founder who gets a wrong answer on turn one does not stay to reach them.

A correction worth stating up front: the doctrine is not missing a pre-launch playbook. business-method §5 (sell before building, warm outreach first), §7.0 (the market gate), §9.1 (build order), §10.1 (warm outreach until roughly 10 paying customers), and §16 row 1 (new business, no pipeline, warm outreach as drafts in chat) together form a complete stage-0 path. The defect is routing and exposure, not a gap in the method. The coaching brain holds the right answer; the onboarding surfaces cannot reach it.

## 2. What already works and must not be broken

These behaviors were verified as strengths across the runs. Any change made for the pre-launch founder must leave them intact.

- **The understand-before-prescribe hinge (start-here Step 6b, business-method §2.1).** It forces an explicit goal and blocker rather than an inferred one, and reasons from the stated blocker to a sharper real one before offering to build. For Tony it produced a true diagnostic reframe under time pressure. This is the single best thing the system does.
- **The terse gauge and its "short is not the same as terse" safeguard.** It correctly read impatience markers for Sam, and correctly kept Tony in the engaged path once his short replies carried real specifics. Do not weaken the gauge itself; the fix below is about what the terse path is allowed to do, not about re-classifying owners.
- **The build-ready fork (Step 7a) as words-only, no stapled artifact.** Verified to follow the hard rule.
- **The staged build (rough pass, guesses flagged, sharpened together).** Suits a stressed owner who will not accept a polished output on faith.
- **Keyless engines that run cold from typed-in numbers.** cash-flow-forecast was an unexpectedly strong organic fit for a founder's runway concern, and price-my-work, profit-per-job, and cash-flow-forecast all run on day one without a completed job.
- **build-my-voice already degrades gracefully** when there is almost nothing to read (it builds from how the owner describes themselves). The Brand and Voice leg needs no new logic, just a pointer to this existing fallback.
- **The standing guardrails held:** plain-language (no jargon leaked), complexity and cost bounding, TrustPager staying reactive-only, and the Wins-post beat firing only after a real win landed.

## 3. Prioritized recommendations

Three tiers. Severity is weighted by where the churn actually happens, so the Day-1 routing gaps rank above the later-day content gaps even though all four were confirmed HIGH.

### Tier 1: Must-fix (Day 1, the make-or-break turn)

**1. Add a "wants clients / no pipeline yet" entry to the terse signal list.**
- Owning file: `skills/start-here/SKILL.md`, Step 6b signal list (line 121).
- Change: Insert a leads entry before the `build-brand-strategy` default. For a pre-launch or early (roughly $0 to 10k) owner, answer the strategy question directly in chat with a concrete first-client warm-outreach action set (the §10.1 pattern: acknowledge something specific, a genuine compliment, one small clear ask, prefer "who do you know who…?"), drafted inline the same way the chase-my-quotes entry drafts its three-touch set. For an owner already trading, route the same ask to plan-my-content or build-social-strategy. Keep build-brand-strategy as the default only for genuine "why pick me" positioning asks.
- Serves: idea-stage terse (Sam) primarily, idea-stage engaged secondarily.
- Why it is first: a terse founder asking "how do I get clients" currently lands on a positioning artifact that answers a question he did not ask, violating §2.1's own rule that the terse fast win be aimed at what the owner named. This is the most likely single churn point in the whole system.

**2. Add a keyless warm-outreach option to the cold "finding leads" relief map.**
- Owning file: `knowledge/starter-projects.md`, §4 finding-leads relief map (line 282).
- Change: Gate a warm-outreach-drafting option to the no-pipeline, zero-customer case: draft 10 to 20 personalised messages to the owner's named contacts using the §10.1 pattern, executed via drafts-in-chat, offered before referrals and get-found-online (which assume existing customers or a live site). Mirror it as the same signal-list entry described in recommendation 1.
- Serves: idea-stage engaged and terse.
- Note on the earlier proposal: do not route the pre-launch founder to get-found-online, set-up-referrals, or research-a-competitor. Every one of those assumes an existing site, existing customers, or a live-market competitor, so they still misroute a zero-client founder. The executor ("drafts in chat") and the §16 row already exist; this is a coverage add to the cold menu, not a new skill.

**3. Give the reframe a pre-launch anchor so it stops reasoning toward pricing.**
- Owning file: `knowledge/business-method.md` (the rule), with a one-line inline anchor in `skills/start-here/SKILL.md` Step 6b.
- Change: Add a short pre-launch rule (natural home: §2 after the numbers ladder, or §5 as a pre-$0 row) stating that at zero paying customers the numbers ladder and all of §8 pricing doctrine are moot because no close rate exists to read, so the binding constraint is offer validation. Run the §7.0 market gate (real pain, purchasing power, findability) and the §2 item-1 "I sell WHAT to WHO" test before any leads or pricing prescription. Then anchor it inline at Step 6b: if the owner has zero clients, the reframe is structural ("at zero clients, pricing is not your constraint yet, getting in front of buyers is") and the assistant pressure-tests the offer via §7.0 rather than reasoning toward pricing.
- Serves: idea-stage engaged and terse.
- Note: do not add a separate "do not invent psychological reads" line. §1.2 and §12.7 already forbid an unsignalled character reframe; the run that invented "avoidance of real conversations" was a model slip against existing rules, not a missing rule.

### Tier 2: Should-fix (Day 3, real but only reached if Day 1 lands)

**4. Add a pre-launch branch to the Day 3 floor clusters.**
- Owning file: `skills/five-day-challenge/SKILL.md`, Day 3 clusters.
- Change: Add one short pre-launch branch, parallel to the existing referral-only branch, triggered off Day 1 or Day 2 discovery showing no customers or jobs yet. (a) Win the Work: reframe "on a real job" to "on the standard job or package you are about to offer," price it with §8.6 launch-cheap-then-ratchet, and swap write-a-proposal's customer proposal for an outreach one-pager (named offer, top three worries, price). (b) Money and Paperwork: reframe "real messy file / real cash" to projected cash via cash-flow-forecast and a planned profit-per-job on the intended offer; skip extract-document when there is no file yet. (c) Brand and Voice: no new logic, just point to build-my-voice's existing "almost nothing to read" fallback.
- Serves: idea-stage engaged and terse.
- Why Tier 2 not Tier 1: verified narrower than filed. The keyless engines already run cold and build-my-voice already degrades, so the gap is the prescriptive "real job / real messy file" wording that can make the coach gate on material the founder lacks and stall. Real, but the owner only reaches Day 3 if turn one succeeded, so Tier 1 must land first.

### Tier 3: Nice-to-have

**5. Add a pre-revenue candidate routine to Day 5.**
- Owning file: `skills/five-day-challenge/SKILL.md`, Day 5 Beat 1.
- Change: Add "tracking outreach and pipeline stage for your first clients" (outreach sent, conversations booked, clients closed) as an explicit candidate routine alongside the existing operating-business examples.
- Serves: idea-stage engaged.
- LOW confidence, single source, and the existing weekly-scoreboard fallback already adapts reasonably. Do only if touching Day 5 for another reason.

## 4. Suggested standing dogfood scenarios

Add these to the test suite so the pre-launch coverage does not regress, and so the struggling-owner strengths stay verified. Each names the persona opener and the specific behavior to check.

1. **Idea-stage, terse, direct leads ask.** Opener: "got an idea for an AI agency. how do I get clients. keep it quick." Pass condition: the terse path answers the question with a concrete warm-outreach action set in chat, not a positioning artifact. This is the recommendation 1 regression guard.

2. **Idea-stage, engaged, pre-revenue with savings runway.** Opener: a brand-new founder, no locked name, no clients, "3 clients in 90 days," "6 months of savings," "don't know how to package or price." Pass conditions: the reframe is structural (offer and getting in front of buyers, not pricing), the market gate (§7.0) is pressure-tested before any pricing talk, warm outreach is surfaced, and prior-role automations built for a past employer are mined as proof and first-buyer material.

3. **Idea-stage, full 5-day arc.** Same founder, projected through Days 3 to 5. Pass conditions: Day 3 offers the pre-launch branch (price the standard package, outreach one-pager, projected cash), Day 4's read works from goal-versus-runway arithmetic rather than stalling on absent revenue, and at least one day produces movement toward an actual conversation, not only another artifact.

4. **Struggling owner, acute cash crisis, engaged-but-terse.** Opener: short sentences, a stated payroll deadline, a large overdue receivable from one client, an unprompted BAS mention. Pass conditions (all verified working today, guard against regression): the hinge reframes to concentration risk rather than racing to a forecast, the "short is not the same as terse" safeguard keeps him engaged, the BAS mention triggers the region question at that moment (not silent inference, not a wait to Day 3), write-a-letter is offered as the keyless overdue-payment route, and any surfaced figures persist into the profile for Day 4.

5. **Struggling owner, declining revenue, going concern.** A trading business with real numbers and a slipping pipeline. Pass conditions: the numbers ladder runs as a live loop in service of the goal (not trivia recitation), missing numbers become a "measure it first" prescription rather than a blocker, and the diagnosis routes off the stated pressure point rather than the shape's default priming.

Scenarios 1 through 3 are the new coverage. Scenarios 4 and 5 lock in what already works so the pre-launch fixes do not quietly break the primary avatar.

## 5. Addendum: the Maria persona (declining revenue, engaged), verified separately

The Maria (12-year commercial cleaning company, revenue down 30%, self-diagnosis "we need more leads") critique agent crashed mid-workflow, so her simulation's findings were verified in a follow-up pass with the same adversarial standard. Result: all six of her substantive findings (3 HIGH, 3 MEDIUM) were REFUTED as already handled or speculative. Grade: A. Highlights of the refutations:

- Gauge misread of a discouraged opener: refuted. The terse branch keys on impatience markers, not brevity or tone; four separate guards (clipped-form definition, impatience-vs-engagement test, the one-open-invitation backstop, the ambiguous branch) route her into the consultation.
- Capacity probe useless for a shrunk business: refuted. Business-method section 2 item 7 carries an explicit idle-capacity branch ("then what's stopped you doubling?"), and Step 6b runs the full numbers ladder regardless, which lands on her stale pricing, dead quotes, and unprofitable clients via the section 3 rubric. One cosmetic note: both worked examples in start-here assume a full business, so a shrinking-business illustrative example is a nice-to-have.
- Brand & Voice marches a B2B referral business into social: refuted. The referral-only check is the first bolded sub-bullet of the cluster with an explicit "check ## How my leads come in, or just ask" directive.
- Chase-quotes needs a pasteable document / stale-scrape overconfidence / uniform celebratory tone: all refuted against the literal text (generation is not improvement, so the ask-for-the-real-thing rule does not gate it; scraped content is always attributed-then-confirmed including an "or is one the old version?" script; celebration is anchored to the kept artifact, register-mirroring persists via ## How to talk to me, and manufactured hype is barred).

The struggling-business story is therefore consistent across both variants: the consultative core is the system's strength, and the concerns raised about it did not survive contact with the actual skill text.

## 6. Methodology note

Four Sonnet persona simulations (Sonnet because it is the production target model), one Opus owner-experience critique per transcript, two Opus structural audits, Opus dedup, one Opus adversarial verifier per HIGH/MEDIUM finding, Opus synthesis. 34 agents total across the main workflow and the Maria follow-up. Of 24 verified findings, 4 survived as real gaps (all idea-stage), 20 were refuted or already handled. Known weakness of this run: the two structural audit agents returned placeholder output (a structured-output emission failure) and contributed nothing; the confirmed findings all trace to simulations and critiques. A future run should re-issue the audits, though the sim+critique coverage independently reached the same idea-stage conclusions the audits were designed to find.

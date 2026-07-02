# RETENTION, DELIVERY & OPERATIONS — Research Report (Domain 5 of 6)

## A. FRAMEWORKS

### A1. The Leaky-Bucket Ceiling Equation (Hormozi, Gym Launch Secrets)
**Procedure:**
1. Compute monthly new customers (N) and monthly churn rate (C, % of base lost per month).
2. Your maximum customer count is fixed: **Ceiling = N / C**. (30 new/month at 10% churn caps you at 300 customers, forever, no matter how hard you market.)
3. To grow the ceiling you have exactly two levers: raise N or cut C. Halving churn doubles the ceiling exactly as much as doubling sign-ups, and costs far less.
4. Stop rule: if churn > ~5%/month on a recurring model, freeze acquisition spend increases and fix retention first. New marketing into a leaky bucket is net-zero growth (Hormozi's gym math: a promo adds 15 members over six weeks while 10% monthly churn eats 15 existing ones).
**Why it works:** It converts "retention matters" from a platitude into arithmetic, and makes retention and acquisition mathematically interchangeable growth levers where retention is the cheaper one. His worked example: dropping churn 10%→3% multiplied LTV ~3.3x; ~$10/month of retention effort per member returned ~11:1.

### A2. Fast LTV / LTGP:CAC Test (Hormozi)
**Procedure:**
1. LTV quick calc: **(avg revenue per customer per period − direct cost to deliver per period) × periods retained**. Always use gross profit, not revenue (LTGP). Periods retained ≈ 1 / churn rate.
2. CAC quick calc: total sales + marketing spend in a period ÷ new customers in that period.
3. Compute the ratio. Thresholds: **< 1:1 = broken unit economics, stop scaling. ~3:1 = minimum healthy floor. > 3:1 = permission to spend aggressively on acquisition.**
4. Segment it: LTGP:CAC by channel, by customer type, by offer. Kill or shrink segments below floor; pour into the outliers.
5. Decision rule: any strategic question reduces to Hormozi's two questions: does it get more customers, or does it make current customers worth more? If neither, it's not the priority.
**Why it works:** One ratio tells you whether the business is a money-printing machine or a treadmill, and segmenting it exposes which customers and channels actually fund the business.

### A3. Four Levers to Raise LTV: Price, Frequency, Duration, Margin (Hormozi)
**Procedure, run in this order (cheapest test first):**
1. **Price:** raise it on new customers first; Hormozi's default diagnosis for small services is underpricing. Premium price funds better delivery, which improves retention (his virtuous cycle).
2. **Margin:** cut delivery cost without cutting perceived value (see A7, Delivery Cube).
3. **Frequency:** more purchase occasions. Distinguish **continuity** (keep paying for access to what they already bought) from **back-end upsell** (pay for MORE: next goal, deeper tier). Both are valid; owners conflate them and build neither. Internal campaigns to existing customers run ~90% margin and cost nothing to market.
4. **Duration:** retention systems proper (A5, A6). Also the accommodating buying curve: ~20% of customers will happily pay 3-5x more, so always have a premium tier; averaging everyone to the middle ("no man's land") leaves LTV on the table.
**Why it works:** LTV is a product of four terms; most owners only ever touch one (duration) and ignore the multiplication.

### A4. Onboarding-to-First-Win (Activation) Protocol (Hormozi)
**Procedure:**
1. Define the **activation moment**: the earliest observable event after which customers demonstrably stay (first result, first use, first delivered job milestone). Pick from data if you have it; pick a plausible proxy if you don't.
2. Engineer the first win to land **within 7 days** of purchase, 14 max. Restructure delivery order so something a customer can feel comes first, even if it's small.
3. First 48 hours: re-sell the decision. Buyer's remorse peaks immediately after purchase; a personal welcome (call, handwritten card, owner video) reaffirms the choice before anything is delivered.
4. Incentivize activation when customers stall: offer a rebate/bonus worth roughly 10-25% of the gap in value, with a tight 7-14 day window, and track which levers move activation. (Secondary source; treat numbers as directional.)
5. Track "% of new customers activated within X days" as a weekly scoreboard number. It is the leading indicator of next quarter's churn.
6. Onboarding costs more than steady-state delivery (he explicitly prices for this), which justifies charging more up front.
**Why it works:** Almost all churn is decided early; people cancel things they never started using. Speed to value beats depth of value in the retention equation.

### A5. The Five Horsemen of Retention, generalized (Hormozi, Gym Launch Secrets)
The original gym prescription, with the generalized rule for any 2-10 person business:
1. **Reach-outs:** personally text every member every 14 days → *scheduled personal contact on a fixed cadence, owned by a named person, not a newsletter.*
2. **Usage tracking:** flag anyone under 3 visits/week by Wednesday → *define a usage/engagement floor, check it mid-week, and intervene the same week, before the customer consciously decides to quit.*
3. **Handwritten cards** at signup and milestones → *low-cost, high-signal personal moments at purchase and at milestones.*
4. **Member events every 21 days** → *engineered community/status moments; people don't quit places where they have relationships and standing. Give community members visible status with a clear roadmap to the next level.*
5. **Exit interviews** that re-sell and can save ~half of cancellations → see A6.
**Stop rule:** these are labor-disciplined systems; assign each horseman an owner and a weekly checkbox or they decay (his own caveat: most owners abandon them).
**Why it works:** Retention is manufactured intimacy at scale: the personal attention every business gives its first 20 customers, systematized so customer #200 gets it too. The deeper reframe: you are in the accountability/relationship business; the product is incidental to why they stay.

### A6. The Cancellation Save (Exit Interview as a Sales Call) (Hormozi)
**Procedure:**
1. No silent cancellations: every cancel triggers a conversation with a trained person (owner at first), within 24 hours.
2. Run it like a discovery call, not an admin task: diagnose why they bought originally, what changed, what result they still want.
3. Offer a repair path matched to the reason: pause instead of cancel, downshift to a cheaper tier, restart onboarding, fix the specific service failure.
4. Expectation: roughly half of cancellations are saveable when treated as a re-sell.
5. Log every exit reason in three buckets: **never activated / product failed them / life happened**. The bucket distribution tells you whether to fix onboarding (A4), delivery quality, or nothing.
6. Cohort timing: chart when customers leave. Whatever the modal exit month is, install an intervention one step before it.
**Why it works:** Cancellation is the cheapest lead you will ever get: they already bought once. And exit data is the only honest churn diagnostic you have.

### A7. Delivery Cube Redesign (Hormozi, $100M Offers)
**Procedure, when margin is thin or the owner is drowning in delivery:**
1. List every promise in the offer. For each, walk the delivery dimensions: one-to-one vs small group vs one-to-many; DIY vs DWY vs DFY; response speed; medium (in person / call / recorded / template / software).
2. Run the **10x / one-tenth test**: "If customers paid 10x, what would we deliver?" and "If they paid one-tenth, how would we still deliver the outcome?" The cheap mechanisms replace expensive ones.
3. Recompose keeping perceived value high and marginal cost low: one-to-many for teaching/updates, templates and recordings for repeat questions, one-to-one reserved for the few moments that actually move the customer's outcome.
4. Change the delivery vehicle when: gross margin < ~50% on a service, OR the owner's calendar is the growth constraint, OR quality varies wildly by who delivers. Productize: fixed scope, fixed price, documented process, deliverable-defined rather than time-defined.
5. Guard rail: never cut the element customers credit for their result; cut the elements that are expensive to deliver but invisible in the outcome.
**Why it works:** Value is perceived; cost is real. Most small businesses deliver expensive things customers don't value and skip cheap things they do (speed, certainty, personal moments).

### A8. Who-Not-How Hiring + Pay for A-Players (Hormozi)
**Procedure:**
1. Past the point where the owner has proven a function works, anything **new** starts with "who," not "how." "The theoretical max of a business is the sum of the knowledge on the team."
2. Pay top of market: "It's better to overpay for one A-player than underpay for three B-players." A-players hire A-players; B-players hire C-players.
3. Hire before breaking point, not after; pay on time without exception (one late paycheck permanently breaks trust).
4. For junior talent, compensation is partly development: weekly 1:1s that invest in the person buy loyalty and discretionary effort salary can't.
5. Two ways humans learn: **modeling** (watch the best person do it) and **role play** (do it with a guide and immediate feedback). Build every training on those two.
**Why it works:** In a 2-10 person business every seat is a large fraction of total capacity; one bad hire is a 10-30% capability tax.

### A9. The 3Ds Training Loop: Document, Demonstrate, Duplicate (Hormozi)
**Procedure, for handing off any task:**
1. **Document:** write the checklist yourself while doing the task (you can't document what you can't do).
2. **Demonstrate:** do it in front of them, narrating against the checklist.
3. **Duplicate:** they do it in front of you, against the same checklist, until output matches. Grade with a rubric, not vibes; give feedback only on the single lowest-scoring section per review.
4. Expectation-setting: a documented process gets a new person to ~80% of your outcome; the remaining 20% is legitimate judgment, don't script it.
5. Loop rule: every time reality beats the checklist, update the checklist (standards compound; that's the asset).
**Why it works:** Replaces "I explained it twice" with a repeatable transfer mechanism, and creates an artifact that survives the employee.

### A10. E-Myth Owner Diagnosis: Technician / Manager / Entrepreneur (GAP-FILLER, Gerber)
**Procedure:**
1. Diagnose the founder's default mode. **Technician** (does the work), **Manager** (orders the work), **Entrepreneur** (designs the business). Most small-business owners are technicians who had an "entrepreneurial seizure."
2. Name the **Fatal Assumption**: "because I understand the technical work, I understand a business that does that work." Different jobs.
3. Stage the business: **Infancy** (owner does everything), **Adolescence** (first hires; owner either retreats into technician work or abdicates), **Maturity** (business runs on a model, not a person). Most 2-10 person businesses are stuck in adolescence.
4. The key question flip: technician asks "what work has to be done?"; entrepreneur asks "**how must the business work?**"
**Why it works (composes with Hormozi):** Hormozi tells you WHAT to fix; Gerber explains WHY the owner keeps un-fixing it (retreat to comfortable technician work). Diagnose the person before prescribing the system, or the system won't stick.

### A11. Franchise-Prototype Build (GAP-FILLER, Gerber, fused with Hormozi's 3Ds)
**Procedure:**
1. Pretend the business is the prototype for 5,000 more. Every process operable by a person with the **minimum necessary skill**, fully documented, producing a uniformly predictable result.
2. **Org chart before headcount:** draw every role the mature business needs (even with 2 people). Put the owner's name in every box. The company builds itself by replacing the owner's name one box at a time, bottom-up (technician boxes first, entrepreneur boxes last).
3. For each box being vacated: write the position's result + standards (the "position contract"), then run Hormozi's 3Ds (A9) to transfer it.
4. Seven-step program, compressed: primary aim (what the owner's life is for) → strategic objective → org strategy → management strategy → people strategy → marketing strategy → systems strategy.
5. Standing rule: schedule recurring time working **ON** the business, defended like customer work. If your business depends on you, you don't own a business, you own a job.
**Why it works:** Documentation converts personal skill into a sellable, delegable, survivable asset. It's the systemization depth Hormozi assumes but rarely spells out for 3-person shops.

### A12. Operating Cadence: Scoreboard + Three Meetings + Speed-Is-King (Hormozi)
**Procedure:**
1. **Scoreboard:** one page, weekly: leads, show/close rate, cash collected, activation %, churn/saves, and the constraint metric of the quarter. The gap against benchmark picks the week's priority.
2. **Three cadences (non-negotiable):** daily huddle under 10 minutes (yesterday's numbers + customer wins); weekly team meeting, tightly scripted; weekly 1:1s where the owner mostly listens.
3. **Priority rule:** work the current constraint only; expect "bottleneck ping-pong." That's the system working, not failing.
4. **More / Better / New:** MORE of what works until volume is the constraint; then BETTER; only NEW when both are exhausted. Risk rises in that order.
5. **Change discipline:** test every change in a contained slice (one rep, one segment, 10% of the list) before rolling out; expect a ~20% short-term dip after any change and don't panic-revert.
6. **Speed-is-king:** when a fix is known, "what are you doing in the next two hours that's more important than this?" End-of-day beats end-of-week ~7x over a year.
**Why it works:** Small businesses don't lose to bad strategy; they lose to slow loops and untracked numbers. Cadence makes every other framework actually happen.

## B. DIAGNOSTIC QUESTIONS & HEURISTICS (in sequence)

**Retention block:**
1. "What % of customers who buy once buy again / are still paying 3, 6, 12 months later?" (Unknown → measure first.)
2. "How many new customers a month, and how many lost?" → compute Ceiling = N/C on the spot. If ceiling ≈ current size, retention is the constraint, full stop.
3. "Of the last 10 customers you lost: how many ever really used/started the thing?" (>3 never activated → onboarding problem, not product problem.)
4. "When do they leave: which month/visit is the cliff?" → intervene one step before the cliff.
5. "What happens in a customer's first 7 days? What win can they point to?" (Silence = churn already scheduled.)
6. "When someone cancels, what happens next?" ("Nothing" = ~half were saveable.)

**LTV/delivery block:**
7. "What does one customer make you in gross profit over their whole life, and what does one cost to get?" If LTGP:CAC < 3, don't discuss more marketing yet.
8. "What's your gross margin on delivery?" (<50% on a service → Delivery Cube redesign first.)
9. "If a customer paid you 10x, what would you give them? If 1/10th, how would you still deliver the result?"
10. "Which parts of delivery only you can do, honestly?" (>3 items = owner is the delivery bottleneck.)

**Owner/team block:**
11. "If you took two weeks off with no phone, what breaks first?" (The answer is the next thing to document via 3Ds.)
12. "Is anything written down such that a competent stranger could do it tomorrow?" (No → E-Myth prototype work precedes hiring.)
13. "Are you hiring the cheapest person who can do the job or the best person you can afford?"
14. "What numbers did you look at this week, and with whom?" (None/alone → install A12 before any other prescription.)
15. "You knew about [problem] for how long? What stopped you fixing it that week?" (Speed-is-king probe.)

**Heuristics:** never-activated churn > 30% → onboarding, not marketing. Modal exit at month 1 → expectations/onboarding mismatch; at month 4-6 → value plateau, add milestone/status system. Owner does >50% of delivery hours at 5+ staff → technician trap. Revenue flat 12+ months while working harder → conversion or retention hidden problem, not traffic.

## C. PRESCRIPTIONS (situation → move, sized 2-10 people)

| Situation | Move(s) |
|---|---|
| Churn unknown / no numbers | One-page scoreboard first (A12); count last 90 days of joins vs losses; compute ceiling (A1) |
| High churn, customers never engaged | Activation protocol (A4): define the first-win moment, restructure week 1, welcome touch in 48h, track activation % weekly |
| High churn, customers engaged then drift | Generalized Five Horsemen (A5): 14-day personal contact cadence + usage floor with same-week intervention + milestone moments |
| Cancellations processed silently | Cancellation-save conversation (A6) with pause/downshift options; log reasons in 3 buckets; expect ~50% save rate |
| LTGP:CAC < 3 but sales fine | Raise price on new customers; then margin redesign (A7); revisit acquisition only after ratio ≥ 3 |
| Revenue capped, owner's calendar full | Delivery Cube (A7): one-to-many teaching, template the repeat questions, keep 1:1 only where it moves outcomes; productize into fixed-scope packages |
| One-off jobs, no repeat revenue | Add continuity AND a back-end upsell; plus a premium tier for the ~20% who'll pay 3-5x (A3) |
| "My staff can't do it like I do" | 3Ds loop (A9) + rubric grading; expect 80% match and accept it; update the doc every time reality wins |
| First hire imminent | E-Myth org chart with owner's name in all boxes (A11); document the box being handed over BEFORE the hire starts; hire for the role's written result |
| Chronically hiring cheap and churning staff | Pay top of market for one A-player instead of two B-players (A8); pay on time, always; weekly 1:1s |
| Owner "too busy" to systemize | Name the technician trap out loud (A10); book a recurring ON-the-business block; start with the "what breaks first if I vanish" answer |
| Everything feels urgent, no rhythm | Install three cadences (A12): 10-min daily huddle, scripted weekly meeting, weekly 1:1s; one constraint metric per quarter |
| Known fix, still not done after weeks | Speed-is-king rule: schedule the 2 hours today |
| Wants to add a new offer/channel | More/Better/New gate: prove more and better are exhausted first; test in a contained slice; expect the 20% dip |

## D. SURFACE MAP

- **A1 Leaky-bucket ceiling** → `knowledge/industry-notes.md`: N/C ceiling math per shape; `renewal-tracker`: report the computed ceiling alongside renewals so retention reads as a growth number.
- **A2 LTGP:CAC** → `profit-per-job`: extend from per-job to per-customer-lifetime gross profit; `grill-me-on-this-decision`: any "spend more on marketing" decision gets the 3:1 gate.
- **A3 Four LTV levers** → `whats-possible`: pitch price/frequency/duration/margin moves as concrete opportunities; `design-nurture-sequence`: nurture toward back-end upsell vs continuity, distinguished explicitly.
- **A4 Activation protocol** → `starter-projects.md`: "customer onboarding to first win" starter project; `follow-up-radar`: flag new customers with no activation event within 7 days.
- **A5 Five Horsemen** → `set-up-a-routine`/`sweep-my-day`: the 14-day reach-out cadence and mid-week usage check as scheduled routines; `industry-notes.md`: per-shape translation (gym visits → clinic rebookings → cafe regulars → course logins).
- **A6 Cancellation save** → `renewal-tracker`: every lapse/cancel spawns a save-conversation task with the 3-bucket reason log; `design-nurture-sequence`: a win-back branch keyed to exit reason.
- **A7 Delivery Cube** → `price-my-work` and `describe-a-product`: run the 10x/one-tenth test when margins are thin; `industry-notes.md` courses/coaching + software shapes: one-to-many defaults.
- **A8 Who-not-how / A-player pay** → `write-a-job-ad`: top-of-market comp framing and outcome-defined roles; `grill-me-on-this-decision`: hire decisions probed with "cheapest adequate vs best affordable."
- **A9 3Ds loop** → `delegate-this-work`: every delegation as Document→Demonstrate→Duplicate with a rubric; `write-a-policy`: policies born from the Document step; `review-team-draft`/`team-review`: grade against the rubric's lowest section only.
- **A10 Technician trap** → `start-here`/`learn-my-business`: diagnose the owner's mode early and store it in the profile; `weekly-review`: surface when the week was all technician hours.
- **A11 Franchise prototype** → `starter-projects.md`: "org chart with your name in every box" starter project; `onboard-team-member`: new hire = handing over a documented box; `sync-team-standards`: the living standards file IS the prototype.
- **A12 Cadence** → `weekly-review`: scoreboard + constraint-of-the-quarter + more/better/new gate + "what are you doing in the next two hours" close; `sweep-my-day`: daily huddle numbers; `cash-flow-forecast`: feeds the weekly scoreboard; `five-day-challenge` Day 5: the self-running system is exactly this cadence.

## E. SOURCES

- https://sobrief.com/books/gym-launch-secrets — Gym Launch Secrets: pie equation, 10%→3% churn = 3.3x LTV, Five Horsemen, three meeting cadences, accountability-business reframe.
- https://podscripts.co/podcasts/the-game-with-alex-hormozi/f-end-of-the-week-ep-356 — speed-is-king doctrine, five horsemen referenced, end-of-day vs end-of-week ~7x.
- https://dickiebush.substack.com/p/i-invested-45000-in-alex-hormozis — VAM notes: constraint analysis, bottleneck ping-pong, weekly test cadence, 31-row rubric, modeling+roleplay, status-based community retention.
- https://artandbiz.substack.com/p/acquisitioncom-workshop-review-15 — who-not-how above scale, "$500k vs $50k team member," theoretical-max-is-team-knowledge, more/better/new, continuity vs back-end upsell, test-small + expect 20% dip, two strategic questions.
- https://michaelcolumbus.com/duplicating-yourself-why-do-standards-exist/ — 3Ds attribution and standards-compounding.
- https://blog.forecastingperformance.com/p/hormozi-s-favorite-analysis — LTV:CAC mechanics, gross-profit-based LTV, 3:1 floor, segmentation.
- https://dansilvestre.com/summaries/the-e-myth-revisited/ — E-Myth: fatal assumption, three personalities, stages, franchise rules, seven-step program.
- LinkedIn recap (activation rebate 10-25%, 7-14 day window) — secondary.
- https://www.gymlaunch.com/summer-retention + 100M Retention Playbook PDF — corroborate Five Horsemen as canonical.

## F. GAPS

1. **3Ds ordering conflicts:** standardized on Document-first (matches the book); the loop matters more than the order.
2. **Activation rebate specifics (10-25%, 7-14 days)** from a LinkedIn recap; numbers directional, mechanism solid.
3. **"Save ~half of cancellations"** from a book summary; direction multiply corroborated.
4. **Hormozi is genuinely thin on micro-business systemization** below ~$1M; E-Myth carries the sub-$1M load by design.
5. **Acquisition.com "value drivers" content is gated;** ops taxonomy reconstructed from attendee notes.
6. **LTV definition inconsistency in the wild:** hard-code gross profit (LTGP) in the doctrine to prevent scale-up prescriptions on fake ratios.
7. **Tension worth encoding:** "systematize personal touch" vs scripted-feeling risk — prescribe the cadence but insist each touch's content is genuinely specific to the customer.
8. Retention masterclass video and $2M onboarding-overhaul case not transcript-verified; claims appear only where corroborated elsewhere.

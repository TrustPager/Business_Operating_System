# Industry Notes — organised by business shape

**Modular domain knowledge, organised around a small set of business *shapes*.** This file is *referenced*, not copied. `/start-here` (Step 5) and `/learn-my-business` read the operator's situation, **match it to a business shape first** (then to any vertical specifics nested under that shape), and fold the relevant gotchas into the `CLAUDE.md` they write. Skills may also consult it directly when business context changes how they should behave.

**Why shapes, not endless niches (D12).** Almost any small business maps onto one of a handful of *shapes* defined by how work flows from first contact to repeat: how leads arrive, how the work gets priced and delivered, and what brings customers back. Cover the shapes well and you serve any industry inclusively, while the proven generic fallback carries anything unusual. Verticals (mortgage broker, electrician, physio) are **inference shortcuts inside a shape**, not gates: a new owner with no matching vertical still gets an excellent, shape-aware first win.

Each shape is the same structure:
- **Pipeline model** — the common stage flow, so Claude can recognise/name stages.
- **What they sell** — typical products/services.
- **Reliefs** — what most eats the owner's week (the relief to target a first win at).
- **Gotchas** — the behaviour-changing rules. This is the real value; the rest is priming.
- **Doctrine fit** — how the business-method diagnosis lands on this shape: the default pressure point to check, the reliefs typed to the diagnosis rows, what standard growth advice lands / adapts / is a trap here, and the shape's guarantee / attraction-offer / referral-ask defaults. References `business-method.md` sections; never restates them. The diagnosis-level summary lives in `business-method.md` §15; this block is the operational detail behind that row.
- **Comms style** — how this operator usually wants to sound.
- **Verticals inside this shape** — named industries that map here, each keeping its own specific gotchas.

> These are *patterns*, not facts about a specific operator. Never write them into a `CLAUDE.md` as if they were read from the workspace — confirm with the operator, and always prefer the real workspace data (pipeline, products, brand) over these defaults. The 'default constraint' in each Doctrine fit block is directional — a default to CHECK with the owner's real numbers (business-method.md §2), never a fact to assert.

**Matching, in one line:** start from the shape (how does work flow here?), then layer the vertical specifics if one of the named industries fits. No shape fits cleanly → use the [Anything else](#anything-else--the-generic-fallback) generic fallback, which is strong on its own.

---

## Shape: Service / professional

*Lead → qualify → quote/proposal → deliver → retain. Sells expertise and outcomes; the proposal or recommendation is the moment the deal is won.*

**Pipeline model:** New enquiry → Discovery / fact-find → Proposal or recommendation prepared → Proposal followed up → Won → Onboarding / delivery → Renewal / referral.

**What they sell:** Advice, audits, project engagements, retainers, comparisons/recommendations, ongoing service relationships.

**Reliefs (target the first win here):** winning the next piece of work (the proposal/recommendation), staying on top of a relationship-driven pipeline, looking as professional as the expertise actually is, and chasing the deals that stall after "sent".

**Gotchas (shape-wide):**
- **Proposals and recommendations stall in "sent".** The follow-up cadence after a proposal is where deals are won or lost — chase deliberately, not once.
- **Relationships and referrals are the lifeblood.** Past clients and referral partners drive new work; surface anniversary/renewal touches and prompt for the referral ask when a deal lands.
- **Sound like the operator, not like marketing.** These clients buy expertise; drafts read as considered and specific, never generic sales copy.
- **A clear record of advice matters.** Log what was recommended/quoted on the opportunity so there's a complete trail.

**Doctrine fit** *(defaults to check, not facts — verify against this owner's numbers; summary row: `business-method.md` §15)*
- **Default constraint to check:** sales-cycle leakage — a SALES/CONVERSION constraint (§3 row 2), not leads: proposals dying in "sent", referral asks never made, renewals unsurfaced. Confirm or deny with three probes: what share of sent proposals get a deliberate follow-up, whether a referral ask happens when a deal lands, and close rate against conversation volume.
- **Reliefs, constraint-typed:** "winning the next piece of work" and "chasing the deals that stall after sent" → conversion; "staying on top of a relationship-driven pipeline" → conversion (cadence); "looking as professional as the expertise actually is" → the Belief variable (§6). None of this shape's reliefs are leads-typed — when this owner asks for "more leads", run the engaged-lead math (§10.3) on the existing pipeline first.
- **Lands directly:** offer construction (§7) on the proposal itself; the discovery arc (§12.5) on discovery calls; warm outreach as the first door (§10.1); the referral ask engineered at the won-deal moment (§10.7).
- **Adapt:** guarantees on regulated advice become service-level (§7.2) — response time, we-handle-everything, never a promised outcome; the attraction offer as a paid audit/discovery credited toward the engagement (§9.3).
- **Traps:** scarcity or countdown pressure on advice decisions (§7.4 — corrodes exactly the trust an expertise sale runs on); discounting to win the work (§8.5).
- **Shape defaults:** guarantee = conditional or service-level (§7.2; regulated advice never guarantees outcomes) · attraction offer = paid audit/discovery credited toward the engagement (§9.3) · referral-ask moment = the won-deal moment (§10.7) — ask for an introduction, not "any names?".

**Comms style:** Polished but human, specific, low-fluff. Reference the client's actual situation, not boilerplate. Relationship-driven and warm where it's a long game.

### Verticals inside this shape

**Mortgage / finance broker**
- **Typical pipeline:** New enquiry → Fact-find scheduled → Documents collected → Pre-approval submitted → Pre-approval received → Property identified → Formal approval → Settled.
- **Typical products:** Home loan (owner-occupier / investor), refinance, top-up / equity release, construction loan, SMSF loan, commercial loan, personal loan, asset / car finance.
- **Gotchas:**
  - **Compliance + data ownership.** Client records must be retained ~7 years; the operator's data should live in *their own* CRM / system of record, not an aggregator's database. Always log comms as activities on the opportunity so there's a complete audit trail.
  - **Credit checks (Equifax) increasingly required upfront.** When a deal moves from "Documents collected" → "Pre-approval submitted", flag if no credit pull is recorded yet.
  - **Referrals are the lifeblood** — past clients, accountants, financial planners, real estate agents. When a deal settles, prompt about asking for a referral.
  - **Birthday / loan-anniversary touches** keep the broker top-of-mind for refinances — surface these in follow-up sweeps.
  - **Never quote a rate** without checking the current panel; **never promise a settlement date** (the lender controls it); avoid the word "guarantee".
  - **Aggregator vs workspace:** the aggregator software is source of truth for the lender lodgement; the operator's own CRM / system of record holds relationship history, comms, notes, follow-ups.
- **Comms style:** Relationship-driven, warm, professional, plain text (no marketing chrome), first names, no jargon.

**Insurance broker**
- **Typical pipeline:** New enquiry → Needs assessment → Quote / comparison prepared → Quote presented → Bound / policy issued → Onboarded → Renewal due.
- **Typical products/services:** Business pack, public/professional liability, commercial property, motor fleet, life / income protection, strata, niche covers.
- **Gotchas:**
  - **Renewals are the business.** Every policy has a renewal date — surfacing upcoming renewals early is the single most valuable follow-up. Treat renewal date like a pipeline trigger.
  - **Disclosure + audit trail.** Advice and recommendations must be logged; keep a clear record of what was quoted and presented on the opportunity.
  - **Never imply cover that isn't bound.** Don't tell a client they're "covered" until the policy is issued; avoid absolute language about claims outcomes.
  - **Compliance language** matters — don't invent product features or limits; confirm against the actual policy.
- **Comms style:** Professional, precise, reassuring. Specific about what's covered and next steps; careful with promises.

**Consultant / professional services**
- **Typical pipeline:** New enquiry → Discovery call → Proposal / SOW sent → Proposal followed up → Won → Onboarding → Delivery → Renewal / upsell.
- **Typical products/services:** Discovery / audit, project engagements, retainers, workshops/training, advisory days.
- **Gotchas:**
  - **Proposals stall in "sent".** The follow-up cadence after a proposal is where deals are won or lost — chase deliberately, not once.
  - **Retainers = recurring value** — track renewal/anniversary and surface upsell moments.
  - **Scope creep + SOWs** — keep the agreed scope on the opportunity; reference it when drafting comms about extra work.
  - **Sound like the operator, not like marketing.** These clients sell expertise; drafts should read as considered and specific, never generic sales copy.
- **Comms style:** Polished but human, specific, low-fluff. Reference the client's actual situation, not boilerplate.

**Technical / specialist services (engineering, environmental, specialist consulting)**
- A service/professional business where the buying decision is graded on *methodology and capability*, often via a formal RFP/tender, with price in a separate schedule.
- **Gotchas:**
  - **The technical section wins it, not the price.** Tender/methodology/capability sections are graded on approach — a separate price-first proposal mode misses the point. (`write-a-proposal` carries a tender/technical-section mode for exactly this.)
  - **Variations and disputes are routine** on technical jobs — a firm, factual variation notice or dispute response is a recurring need (`write-a-letter`).
  - **Defensible pricing** matters when the brief is technical: a number the owner can stand behind (`price-my-work`).
- **Comms style:** Precise, evidence-led, professional. Specific about scope, method, and assumptions.

---

## Shape: Trades / on-the-tools

*Enquiry → quote → job → invoice. The owner is on-site, not at a desk; speed-to-lead and quote follow-through win the work.*

**Pipeline model:** New enquiry → Site visit / quote booked → Quote sent → Quote followed up → Won / scheduled → Job in progress → Completed → Invoiced / paid.

**What they sell:** Call-out / diagnostic, supply-and-install jobs, repairs, maintenance plans, emergency work, larger project quotes.

**Reliefs (target the first win here):** turning a job into a quote fast (a photo is often the whole brief), pricing a job with confidence, winning back missed calls, and chasing quotes before they go cold.

**Gotchas (shape-wide):**
- **Speed-to-lead wins the job.** A missed call or an un-replied enquiry is a lost job — surface these first and offer to draft the recovery message immediately.
- **Quotes go stale fast.** Chase a sent quote within a few days; after ~2 weeks assume it's cold unless re-engaged.
- **Deposits and progress payments** are normal — track what's been invoiced vs paid; flag jobs marked complete that were never invoiced.
- **The operator is on-site, not at a desk.** Prefer SMS over email; keep messages short; one action at a time. Don't expect same-day email reads.
- **Photos drive quotes** — a site photo + a voice note is often the whole brief (`quote-from-photo`).

**Doctrine fit** *(defaults to check, not facts — verify against this owner's numbers; summary row: `business-method.md` §15)*
- **Default constraint to check:** response speed and quote follow-through — a SALES/CONVERSION constraint (§3 row 2), not leads. Second suspect: pricing below the cost floor (PROFIT-PER-UNIT, §3 row 5; §8.6). Confirm or deny with three probes: how fast enquiries get answered, what share of sent quotes ever get a second touch, and whether the quote clears the true cost floor.
- **Reliefs, constraint-typed:** "quoting eats my week" and "chasing quotes before they go cold" → conversion; "winning back missed calls" → conversion (speed); "pricing with confidence" → profit-per-unit. None of this shape's reliefs are leads-typed — when a tradie asks for "more leads", run the local gravity gate (§10.5) before any spend.
- **Lands directly:** the value equation as quote logic (§6); the capacity rule when the calendar is full — price, not volume (§8.3); the local gravity stack as the whole local plan (§10.5); deposits and progress payments as the cash pull-forward levers (§9.5).
- **Adapt:** three-tier quotes with inclusions and proof (§7.1 as a quote stack — options, never pressure); volume routed through systems (missed-call text-back, review asks, quote chases), never through owner hours (§10.2 gate).
- **Traps:** aggressive close scripts and countdown pressure (poison local word-of-mouth); buying leads while calls ring out (§10.5 hard gate); pricing off "competitor average minus 10%" (§8.5).
- **Shape defaults:** guarantee = service-level — turn-up window, workmanship warranty (§7.2), never inflated outcome promises · attraction offer = paid call-out/diagnostic credited against the job (§9.3) · referral-ask moment = job completion, same visit as the review ask (§10.7 + §10.5 tier 2) — ask for an introduction to the neighbour, not "any names?".

**Comms style:** Short, direct, friendly, plain. No corporate tone. Confirm time windows and what's included.

### Verticals inside this shape

**Trades (electrical, plumbing, building, HVAC, telco, landscaping, etc.)**
- The shape-wide pattern above *is* the trades vertical — the gotchas apply directly. Sub-trades differ mainly in job size and whether emergency/call-out work dominates (electrician, plumber) versus project work (builder, landscaper). Larger project trades lean more on the quote-follow-up and progress-payment gotchas; call-out trades lean more on speed-to-lead and missed-call recovery.

**Small manufacturing / fabrication (made-to-order)**
- A trades-shaped business where **the spec, not a photo, is the brief**, and repeat/wholesale accounts replace one-off jobs as the backbone.
- **Typical pipeline:** Enquiry / RFQ → Spec / requirements gathered → Quote prepared → Quote sent → PO received → In production → Dispatched / delivered → Invoiced.
- **Typical products/services:** Made-to-order runs, standard product lines, custom fabrication, repeat/wholesale orders, servicing.
- **Gotchas:**
  - **Quotes hinge on specs.** Don't quote without the spec (materials, quantities, tolerances, lead time) — flag missing inputs rather than guessing numbers.
  - **Lead times and capacity** drive promises — never commit a delivery date without confirming production capacity.
  - **Repeat / wholesale accounts** are the backbone — surface reorder timing and treat key accounts as relationships, not one-off deals.
  - **PO + invoicing discipline** — track quote → PO → dispatch → invoice; flag dispatched jobs not yet invoiced.
- **Comms style:** Precise, factual, specific about quantities, specs, lead times, and price. Professional B2B tone.

---

## Shape: Product-seller / ecommerce-retail

*Browse → order → fulfil → reorder. Sells SKUs and variants, not custom jobs; the catalogue and the listing copy are the shopfront, and average order value plus repeat purchase drive the business.*

**Pipeline model:** Discover / browse → Add to cart / enquire → Order placed → Picked / fulfilled / shipped → Delivered → Review / reorder / win-back.

**What they sell:** Physical or digital products as SKUs with variants (size, colour, pack), bundles, restocks, sometimes a few hero lines plus a long tail.

**Reliefs (target the first win here):** **content and pricing** are the two daily blockers — the blank product-description box, and pricing/AOV decisions across a catalogue. Also: marketing each launch/promo well, and handling supplier/refund/return correspondence.

**Gotchas (shape-wide):**
- **Every product needs description copy.** The blank "description" box is the daily blocker; one product at a time, photo or notes in, on-brand copy out (`describe-a-product`). Lead with what the buyer gets.
- **Listings live or die on the post.** Launches and promos run on social — a strong caption that leads with the outcome for the buyer, not the feature list (`write-post-copy`).
- **Average order value and pricing.** Bundles, pack pricing, and "spend X to get Y" decisions are pricing work; help the owner reason about margin per SKU and AOV, not just a single job price (`price-my-work` adapts to a per-unit/per-bundle frame).
- **SKUs and variants multiply fast.** Keep product/variant data tidy and consistent (a clean product spreadsheet beats a sprawling mess); naming and attribute consistency is what makes a catalogue searchable and shippable.
- **Supplier and returns correspondence is routine.** Refund/return responses, supplier disputes, payment-terms letters — firm and factual, in the owner's voice (`write-a-letter`).
- **Reviews and reorders are the flywheel.** Capturing how buyers actually describe the product feeds every listing and post (`build-customer-voice`); reorder/win-back nudges keep AOV compounding.

**Doctrine fit** *(defaults to check, not facts — verify against this owner's numbers; summary row: `business-method.md` §15)*
- **Default constraint to check:** unit economics and differentiation — PROFIT-PER-UNIT (§3 row 5) plus positioning (§14). Confirm or deny with two probes: contribution margin per order after fulfilment AND acquisition cost, and the repeat-purchase rate.
- **Reliefs, constraint-typed:** "pricing/AOV decisions across a catalogue" → profit-per-unit; "the blank description box" and "marketing each launch well" → positioning and the Belief variable (§14, §6); reorder/win-back nudges → retention (§11).
- **Lands directly:** the money model at full strength (§9 — bundles, upsells, continuity, the 30-day cash test); volume doctrine applied to creative tests (§10.2); the referral ask at the review moment (§10.7).
- **Adapt:** OVERRIDE — judge margin by the cash-conversion cycle (money leaves before it arrives here), not §8.1's service bands.
- **Traps:** scaling ads before contribution margin per order is known (§10.6 gate); deep-discount launches that train buyers to wait for the sale (§8.5).
- **Shape defaults:** guarantee = unconditional for low-ticket consumer products (§7.2) · attraction offer = buy-X-get-Y / bundles (§9.3) · referral-ask moment = the review moment (§10.7) — the ask rides the same message as the review request.

**Comms style:** Benefit-led and concrete, friendly, on-brand. Lead with the outcome the buyer gets; specific about what's included, sizing/fit, and dispatch. Channel-native (a product caption reads differently from a service proposal).

### Verticals inside this shape

**Ecommerce / DTC (online store, marketplace seller)**
- Online-first; the listing IS the shopfront. Description copy, launch posts, and review-mining are the highest-relief minute-one moves. Marketplace sellers (Etsy, eBay, Amazon) have the same content/pricing reliefs plus platform-specific listing rules — keep claims accurate and on-brand.

**Bricks-and-mortar retail / hybrid (shop with a catalogue + some online)**
- Same browse → order → reorder shape with a physical store layer. Local social presence and in-store-to-online continuity matter; the content win (posts, descriptions) and a clean product list still lead.

---

## Shape: Hospitality / walk-in

*Walk-in + bookings/functions. Driven by foot traffic, table/room bookings, and events; Instagram is a primary channel, deposits and rosters are the operating reality.*

**Pipeline model:** Discover (often social / local) → Walk-in OR booking enquiry → Booking / function confirmed (deposit) → Service / event delivered → Review / repeat visit.

**What they sell:** Covers/sittings, function and event packages, group bookings, takeaway/online orders, sometimes retail (merch, packaged goods).

**Reliefs (target the first win here):** **marketing and being found** (social presence is the channel), filling tables/functions, and the admin around bookings, deposits, and rosters.

**Gotchas (shape-wide):**
- **Instagram (and local social) is a primary sales channel, not an afterthought.** A steady, on-brand social presence directly fills tables — the social-strategy and content wins are high-relief here (`build-social-strategy`, `plan-my-content`, `write-post-copy`).
- **Functions and events run on deposits.** A clear deposit and confirmation policy avoids no-shows on big bookings; a function enquiry is a mini-pipeline of its own.
- **Rosters and peaks.** The week revolves around service peaks and staffing; a job ad in the owner's voice and clean staff policies pay off (`write-a-job-ad`, `write-a-policy`).
- **Reviews are the reputation engine.** How guests describe the experience feeds the marketing voice (`build-customer-voice`); respond and lean into the words guests use.
- **Bookings/deposits/cancellations need plain policy.** Clear, on-brand policy text for deposits, cancellations, and group bookings prevents friction (`write-a-policy`).

**Doctrine fit** *(defaults to check, not facts — verify against this owner's numbers; summary row: `business-method.md` §15)*
- **Default constraint to check:** repeat-visit rate first, then off-peak utilization — a RETENTION constraint (§3 row 4), not leads. Quiet Tuesdays are a retention/utilization finding, not a leads problem. Confirm or deny with three probes: what share of guests come back, how full the off-peak sittings run, and whether anything is deliberately engineered to earn visit two.
- **Reliefs, constraint-typed:** "filling tables/functions" → retention/utilization first (visit two), leads second; "marketing and being found" → the content door (§10.1 — one this shape genuinely lives on); bookings/deposits admin → cash pull-forward (§9.5).
- **Lands directly:** LTV thinking — the regular IS the business (§11); referral mechanics as bring-a-friend (§10.7); deposits on functions (§9.5); behind-the-counter content as the standing channel (§10.1).
- **Adapt:** OVERRIDE — there is no pipeline: the "offer" here is whatever earns visit two (loyalty and habit mechanics standing in for continuity, §9.4 adapted).
- **Traps:** countdown scarcity and deep discounting (§7.4, §8.5 — trains deal-hunters and poisons a habit business).
- **Shape defaults:** guarantee = a make-it-right promise, not a mechanic (§7.2 adapted) · attraction offer = bring-a-friend / free-with-consumption (§9.3) · referral-ask moment = the engineered bring-a-friend at the great-night moment (§10.7).

**Comms style:** Warm, inviting, on-brand, visual. Lead with the experience and the result (the night out, the full function); concrete about times, what's included, and how to book.

### Verticals inside this shape

**Cafe / restaurant / bar**
- Covers + bookings + functions. Social presence and a steady content rhythm fill quiet sittings; functions are the high-value bookings to systematise (deposits, confirmations).

**Venue / events / functions-led**
- Function and event packages dominate; each enquiry is a small project (date hold → deposit → run sheet). Proposal-style confirmations and deposit policies matter more than walk-in flow.

**Food retail / takeaway (hybrid hospitality + product)**
- Walk-in plus online/takeaway orders; borrows the product-seller content reliefs (menu/item descriptions, promo posts) on top of the walk-in rhythm.

---

## Shape: Clinic / appointment

*Book → attend → rebook. Driven by the appointment calendar; privacy, reminders, and funding-confirmation are the operating reality.*

**Pipeline model:** New enquiry → Initial appointment booked → Initial consult → Treatment / care plan → In treatment (recurring appointments) → Review → Discharged / maintenance / rebook.

**What they sell:** Initial consults, follow-up sessions, treatment plans/packages, assessments, group programs, telehealth.

**Reliefs (target the first win here):** the admin that protects the calendar — reminders and rebooking (the no-show problem), reading intake/fact-find packs fast, and getting funding/cost wording right before anything goes out.

**Gotchas (shape-wide):**
- **Privacy is paramount.** Health (and similarly sensitive) information must never sit in subject lines or unsecured channels; keep records in the workspace. No clinical advice or diagnosis over SMS/email — drafts book/confirm/remind, never give guidance; defer clinical questions to an appointment.
- **Reminders reduce no-shows.** Appointment reminders and rebooking nudges are the highest-value automation; a calm reminder/rebooking sequence is the standout (logistics-only, never clinical over text).
- **Funding/cost wording must be confirmed first.** Funding schemes (e.g. NDIS, Medicare, private health) change wording and process — confirm the funding type before drafting anything about cost or claiming. Plain-English funding explainers are high-demand (`write-a-policy`).
- **Intake packs arrive as documents.** Payslips, referrals, paper forms, assessments — reading them into a clean summary and naming what's missing is a strong minute-one move (`extract-document`, `template-from-document`).

**Doctrine fit** *(defaults to check, not facts — verify against this owner's numbers; summary row: `business-method.md` §15)*
- **Default constraint to check:** rebooking/recall rate and no-shows — a RETENTION constraint (§3 row 4): the leaky bucket, not the tap. Confirm or deny with three probes: rebooking rate after the initial consult, no-show rate, and recall coverage (what share of lapsed patients ever get a recall touch).
- **Reliefs, constraint-typed:** "reminders and rebooking (the no-show problem)" → retention, and the show-rate doctrine applies in full (§15: the booking is not the win, the show is — remind hard, deposits on long appointments, standby list, track show-rate as a funnel stage); intake-pack reading → delivery/admin; funding wording → compliance, never a growth lever.
- **Lands directly:** activation and recall as retention math (§11.3, §11.1); speed-to-lead on enquiries (§10.5 tier 1); reminder and recall systems as the highest-value automation.
- **Adapt:** COMPLIANCE OVERRIDES EVERYTHING (§7.2, §15): no outcome testimonials or before/afters in owned channels, no result guarantees (service-level only), no urgency or price pressure on clinical decisions; the discovery arc structures logistics and care-plan conversations, never the clinical recommendation (§12.5).
- **Traps:** any proof or scarcity mechanic that touches clinical outcomes (§7.4, §15); treating a quiet book as a leads problem while rebooking and recall sit unmeasured.
- **Shape defaults:** guarantee = service-level only (§7.2 — on-time, logistics, we-handle-the-paperwork; never a clinical outcome) · attraction offer = the initial consult/assessment as the honest entry point (§9.3 adapted — never discounted clinical care under urgency) · referral default = practitioner partnerships, not patient asks (§10.7 adapted).

**Comms style:** Warm, calm, respectful, clear about logistics (time, place, what to bring). Never clinical over text.

### Verticals inside this shape

**Allied health (physio, psychology, OT, dietetics, etc.)**
- **Typical pipeline:** New enquiry → Initial appointment booked → Initial consult → Treatment plan → In treatment → Review → Discharged / maintenance.
- **Typical products/services:** Initial consult, follow-up sessions, treatment plans/packages, assessments, group programs, telehealth.
- **Gotchas:** privacy paramount; no advice/diagnosis over text; reminders reduce no-shows (highest-value automation); funding schemes (NDIS/Medicare/private health) change wording — confirm funding type before drafting about cost or claiming.
- **Comms style:** Warm, calm, respectful, clear about logistics. Never clinical over text.

**Wellness / personal-care appointment businesses (clinics, studios, salons run on bookings)**
- Same book → attend → rebook rhythm with lighter privacy load where no clinical record is involved. Reminders, rebooking, and a steady social presence to fill the calendar are the reliefs; borrows the hospitality social win where being found locally matters.

---

## Shape: Courses / community / coaching

*Audience → free value → offer → member. Sells knowledge and transformation; the content engine is the shopfront, and retention quietly decides everything.*

**Pipeline model:** Discover (content / social / word-of-mouth) → Free tier or lead magnet joined → Engaged / nurtured → Offer presented (launch or evergreen) → Enrolled / member → Onboarded to a first win → Renewing / referring / upgrading.

**What they sell:** Courses, memberships and paid communities, group programs, 1:1 coaching, workshops, digital products (templates, playbooks), sometimes a software or done-for-you upsell at the top of the ladder.

**Reliefs (target the first win here):** the content demand that never stops (the engine is the shopfront), launch and offer copy, onboarding new members to a fast first win, and keeping members month over month.

**Gotchas (shape-wide):**
- **Retention IS the business.** Recurring revenue means a member kept out-earns a member won — watch engagement, not just signups, and build the renewal/win-back rhythm before the next launch.
- **The first win in the first week decides retention.** Member onboarding is a pipeline of its own (welcome → orient → first win → celebrate it publicly); a member who lands a real win in days stays.
- **One idea, many formats.** The content engine runs on repurposing: a single strong idea becomes the post, the email, the lesson, the short. Plan from pillars, not one-off posts (`build-social-strategy`, `plan-my-content`).
- **Free-to-paid is the pipeline.** The free tier or lead magnet is the top of the funnel; the ascension moment (free → paid) is a designed, measured step, not an afterthought.
- **Member words sell the offer.** Wins and testimonials captured at the moment they happen ARE the sales page (`build-customer-voice`); make capturing them systematic, and always attribute real, consented results.
- **Results claims need care.** Income and outcome claims invite platform and consumer-law trouble — anchor every claim in a real, attributable member result and avoid guarantee language.

**Doctrine fit** *(defaults to check, not facts — verify against this owner's numbers; summary row: `business-method.md` §15)*
- **Default constraint to check:** audience/leads to the first ~$10k, then churn and delivery quality (§15) — the one shape where LEADS (§3 row 1) is the honest early default; past that point, re-run the §3 order and check retention first. Confirm or deny with three probes: list/audience growth, monthly churn, and the share of new members who land a first win in week one.
- **Reliefs, constraint-typed:** "the content demand that never stops" → leads (the content door, §10.1); "launch and offer copy" → conversion (§7); "onboarding new members to a fast first win" → activation (§11.3); "keeping members month over month" → retention (§11.1, §11.4).
- **Lands directly:** nearly everything — this is the doctrine's home turf (§15): the value equation, offer construction, the money model, the four doors, and the full retention doctrine all at full strength.
- **Adapt:** protect a practitioner-owner's hours (§8.3) — a coach at delivery capacity prices up or moves 1:1 into group/one-to-many (§11.6) before chasing volume.
- **Traps:** income claims and fake scarcity (§7.4 — real cohort caps are fine, because they're true); competing on information (§14 — the competitive alternative is free content, so the only-we is proximity, accountability, and specificity, never information).
- **Shape defaults:** guarantee = conditional, completion-style (§7.2 — conditions are the actions a successful member takes anyway) · attraction offer = challenge / free tier with a designed ascension moment (§9.3) · referral-ask moment = the celebrated member win (§10.7).

**Comms style:** Founder-voice, energetic but genuine, outcome-and-identity led (speak to who the member is becoming). Plain about what's included, what happens next, and when.

### Verticals inside this shape

**Course creator / educator**
- Launch-based or evergreen; the launch calendar shapes the year and the email list is the asset. Launch copy, open-cart sequences, and post-launch debriefs are the recurring work.

**Paid community operator (Skool, Circle, Discord and similar)**
- Engagement is the retention lever: rituals, live calls, and celebrated member wins keep the room alive. The about/landing page and a clear value ladder do the selling; onboarding to a first win inside the community is the make-or-break week.

**Coach / group program (1:1 or cohort)**
- Fewer, higher-ticket enrolments; discovery calls are the pipeline and the proposal-follow-up gotchas from service/professional apply to the sales side. Cohort start dates create natural launch rhythms.

**Newsletter / audience business**
- The list is the product; consistency compounds. Revenue mixes sponsorship, digital products, and paid tiers — the same free-to-paid ascension design applies.

---

## Shape: Software / digital product

*Sign up → activate → subscribe → renew/expand. Sells a product that works while the founder sleeps; activation and churn are the operating reality.*

**Pipeline model:** Discover → Sign-up / trial / install → Activated (first real value) → Converted to paying → Onboarded / adopted → Renewing / expanding → At-risk / win-back.

**What they sell:** Subscriptions (SaaS), one-time licences, plugins/templates/apps, usage tiers, setup and onboarding services, priority support plans.

**Reliefs (target the first win here):** the activation/onboarding messages that get a signup to first value, quiet accounts drifting toward churn, the support inbox, launch and changelog content, and pricing/packaging decisions.

**Gotchas (shape-wide):**
- **Activation beats acquisition.** A signup who never reaches first value is a churn statistic scheduled in advance — the welcome-to-first-value path is the highest-relief thing to sharpen (`design-nurture-sequence` for the onboarding sequence).
- **Churn compounds monthly.** Recurring math (MRR, LTV against acquisition cost) frames every decision; a retention fix usually out-earns a new-leads push.
- **Support conversations are product research.** The words users use in tickets feed the roadmap, the docs, and the marketing (`build-customer-voice`) — answer warmly, capture verbatim.
- **Ship in public.** Every release is a content moment (changelog → post → email); a visible shipping rhythm reads as a healthy product.
- **The free tier / trial is the top of the pipeline.** Design and measure the upgrade moment deliberately, the same way a shop designs the checkout.
- **Roadmap language stays honest.** Name what's live versus what's planned; never promise a ship date on an unshipped feature.

**Doctrine fit** *(defaults to check, not facts — verify against this owner's numbers; summary row: `business-method.md` §15)*
- **Default constraint to check:** retention/product-fit wearing a marketing costume — check churn and activation before any lead prescription (§3 row 4, per the §3 examination order). Churn above ~5%/mo voids all growth spend (§11.1 hard gate, directional). Confirm or deny with three probes: monthly churn, activation rate (share of signups reaching first real value), and LTGP:CAC (§10.6).
- **Reliefs, constraint-typed:** "the activation/onboarding messages" → activation (§11.3); "quiet accounts drifting toward churn" → retention (§11.4-11.5); "launch and changelog content" → leads (the content door, §10.1); "pricing/packaging decisions" → profit-per-unit (§8).
- **Lands directly:** LTGP:CAC discipline (§10.6); the positioning ladder (§14) — the PRIMARY doctrine for this shape; niche hard (§7.0).
- **Adapt:** the trial/free tier as the attraction offer with a deliberately designed upgrade moment (§9.3); annual prepay as the cash engineering (§9.5).
- **Traps:** discount-to-close (§8.5); buying growth while churn and activation sit unmeasured or failing (§11.1 gate).
- **Shape defaults:** guarantee = activation-conditional (§7.2 — tied to reaching first value, never a business-outcome promise) · attraction offer = the trial/free tier (§9.3) · referral-ask moment = a visible product win (§10.7) — with annual prepay as the standing cash lever (§9.5).

**Comms style:** Clear, human, jargon-free; concrete about what the product does today. Helpful docs-tone in support, founder-voice in launches.

### Verticals inside this shape

**SaaS (subscription app)**
- The shape-wide pattern above *is* this vertical — activation, churn, and the upgrade moment apply directly.

**Plugins / templates / digital downloads (one-time sales)**
- Borrows the product-seller listing and content reliefs (the listing is the shopfront); updates, bundles, and cross-sells drive repeat revenue in place of subscriptions.

**Productised service / agency-to-product hybrid**
- A recurring service sold and delivered like a product (fixed scope, fixed price, subscription billing). The sales side borrows service/professional proposal gotchas; the delivery side borrows activation and churn thinking.

> **Hybrid note (common, expected):** many modern businesses are a blend of these two shapes plus others — a free community that ascends into a paid product, an educator with a software upsell, an open-source tool with a hosted tier. Blend the shapes' gotchas silently; the value-ladder framing (free value → paid offer → deeper product) usually unifies them.

---

## Anything else — the generic fallback

No shape fits cleanly → use the generic `templates/CLAUDE.md` as-is and rely on the real workspace data. The field test confirmed the generic reasoning carries unusual businesses to an excellent first win on its own, so this is a strong default, not a consolation prize. Ask the operator one or two short questions about how their work flows (how leads arrive, how they price, what brings customers back) and their comms style, rather than forcing a shape that doesn't fit. The diagnosis still works shapeless: run the intake and the pressure-point check (business-method.md §2-§3) directly off the owner's answers to those flow questions. If a shape or vertical comes up repeatedly, add it above.

**Never narrate the miss (hard rule).** The owner must never hear that their business "doesn't fit", is "unusual to slot in", that "none of my playbooks apply", or any mention of shapes, playbooks, or matching — that is internal machinery, and hearing it lands as "this system wasn't built for me." Before falling back, check for a **blend**: most businesses that don't match one shape are a mix of two (a community with a software upsell, a shop that also runs workshops, a clinic selling products) — take the gotchas from each part and carry on. Blended or fully generic, the playback sounds exactly as confident and specific as a matched one, and the one or two flow questions read as interest in their business, never as confusion about it.

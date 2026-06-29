# Industry Notes — organised by business shape

**Modular domain knowledge, organised around a small set of business *shapes*.** This file is *referenced*, not copied. `/start-here` (Step 5) and `/learn-my-business` read the operator's situation, **match it to a business shape first** (then to any vertical specifics nested under that shape), and fold the relevant gotchas into the `CLAUDE.md` they write. Skills may also consult it directly when business context changes how they should behave.

**Why shapes, not endless niches (D12).** Almost any small business maps onto one of a handful of *shapes* defined by how work flows from first contact to repeat: how leads arrive, how the work gets priced and delivered, and what brings customers back. Cover the shapes well and you serve any industry inclusively, while the proven generic fallback carries anything unusual. Verticals (mortgage broker, electrician, physio) are **inference shortcuts inside a shape**, not gates: a new owner with no matching vertical still gets an excellent, shape-aware first win.

Each shape is the same structure:
- **Pipeline model** — the common stage flow, so Claude can recognise/name stages.
- **What they sell** — typical products/services.
- **Reliefs** — what most eats the owner's week (the relief to target a first win at).
- **Gotchas** — the behaviour-changing rules. This is the real value; the rest is priming.
- **Comms style** — how this operator usually wants to sound.
- **Verticals inside this shape** — named industries that map here, each keeping its own specific gotchas.

> These are *patterns*, not facts about a specific operator. Never write them into a `CLAUDE.md` as if they were read from the workspace — confirm with the operator, and always prefer the real workspace data (pipeline, products, brand) over these defaults.

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

## Anything else — the generic fallback

No shape fits cleanly → use the generic `templates/CLAUDE.md` as-is and rely on the real workspace data. The field test confirmed the generic reasoning carries unusual businesses to an excellent first win on its own, so this is a strong default, not a consolation prize. Ask the operator one or two short questions about how their work flows (how leads arrive, how they price, what brings customers back) and their comms style, rather than forcing a shape that doesn't fit. If a shape or vertical comes up repeatedly, add it above.

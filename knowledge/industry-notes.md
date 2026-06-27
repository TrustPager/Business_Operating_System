# Industry Notes

**Modular domain knowledge, one section per vertical.** This file is *referenced*, not copied. `/learn-my-business` reads the operator's `company.industry` and pipeline shape, picks the matching section below, and folds its gotchas into the `CLAUDE.md` it writes. Skills may also consult it directly when industry context changes how they should behave.

Adding a new vertical = add a section here. There are no per-industry template files to keep in sync.

Each section is the same shape:
- **Typical pipeline** — common stage flow, so Claude can recognise/name stages.
- **Typical products/services** — what these businesses sell.
- **Gotchas** — the behaviour-changing rules. This is the real value; the rest is priming.
- **Comms style** — how this operator usually wants to sound.

> These are *industry patterns*, not facts about a specific operator. Never write them into a `CLAUDE.md` as if they were read from the workspace — confirm with the operator, and always prefer the real workspace data (pipeline, products, brand) over these defaults.

---

## Mortgage / finance broker

**Typical pipeline:** New enquiry → Fact-find scheduled → Documents collected → Pre-approval submitted → Pre-approval received → Property identified → Formal approval → Settled.

**Typical products:** Home loan (owner-occupier / investor), refinance, top-up / equity release, construction loan, SMSF loan, commercial loan, personal loan, asset / car finance.

**Gotchas:**
- **Compliance + data ownership.** Client records must be retained ~7 years; the operator's data should live in *their own* CRM / system of record, not an aggregator's database. Always log comms as activities on the opportunity so there's a complete audit trail.
- **Credit checks (Equifax) increasingly required upfront.** When a deal moves from "Documents collected" → "Pre-approval submitted", flag if no credit pull is recorded yet.
- **Referrals are the lifeblood** — past clients, accountants, financial planners, real estate agents. When a deal settles, prompt about asking for a referral.
- **Birthday / loan-anniversary touches** keep the broker top-of-mind for refinances — surface these in follow-up sweeps.
- **Never quote a rate** without checking the current panel; **never promise a settlement date** (the lender controls it); avoid the word "guarantee".
- **Aggregator vs workspace:** the aggregator software is source of truth for the lender lodgement; the operator's own CRM / system of record holds relationship history, comms, notes, follow-ups.

**Comms style:** Relationship-driven, warm, professional, plain text (no marketing chrome), first names, no jargon.

---

## Trades / on-the-tools

**Typical pipeline:** New enquiry → Site visit / quote booked → Quote sent → Quote followed up → Won / scheduled → Job in progress → Completed → Invoiced / paid.

**Typical products/services:** Call-out / diagnostic, supply-and-install jobs, repairs, maintenance plans, emergency work, larger project quotes.

**Gotchas:**
- **Speed-to-lead wins the job.** A missed call or an un-replied enquiry is a lost job — surface these first and offer to draft the recovery message immediately.
- **Quotes go stale fast.** Chase a sent quote within a few days; after ~2 weeks assume it's cold unless re-engaged.
- **Deposits and progress payments** are normal — track what's been invoiced vs paid; flag jobs marked complete that were never invoiced.
- **The operator is on-site, not at a desk.** Prefer SMS over email; keep messages short; one action at a time. Don't expect same-day email reads.
- **Photos drive quotes** — a site photo + a voice note is often the whole brief (`/quote-from-photo`).

**Comms style:** Short, direct, friendly, plain. No corporate tone. Confirm time windows and what's included.

---

## Insurance broker

**Typical pipeline:** New enquiry → Needs assessment → Quote / comparison prepared → Quote presented → Bound / policy issued → Onboarded → Renewal due.

**Typical products/services:** Business pack, public/professional liability, commercial property, motor fleet, life / income protection, strata, niche covers.

**Gotchas:**
- **Renewals are the business.** Every policy has a renewal date — surfacing upcoming renewals early is the single most valuable follow-up. Treat renewal date like a pipeline trigger.
- **Disclosure + audit trail.** Advice and recommendations must be logged; keep a clear record of what was quoted and presented on the opportunity.
- **Never imply cover that isn't bound.** Don't tell a client they're "covered" until the policy is issued; avoid absolute language about claims outcomes.
- **Compliance language** matters — don't invent product features or limits; confirm against the actual policy.

**Comms style:** Professional, precise, reassuring. Specific about what's covered and next steps; careful with promises.

---

## Consultant / professional services

**Typical pipeline:** New enquiry → Discovery call → Proposal / SOW sent → Proposal followed up → Won → Onboarding → Delivery → Renewal / upsell.

**Typical products/services:** Discovery / audit, project engagements, retainers, workshops/training, advisory days.

**Gotchas:**
- **Proposals stall in "sent".** The follow-up cadence after a proposal is where deals are won or lost — chase deliberately, not once.
- **Retainers = recurring value** — track renewal/anniversary and surface upsell moments.
- **Scope creep + SOWs** — keep the agreed scope on the opportunity; reference it when drafting comms about extra work.
- **Sound like the operator, not like marketing.** These clients sell expertise; drafts should read as considered and specific, never generic sales copy.

**Comms style:** Polished but human, specific, low-fluff. Reference the client's actual situation, not boilerplate.

---

## Allied health

**Typical pipeline:** New enquiry → Initial appointment booked → Initial consult → Treatment plan → In treatment → Review → Discharged / maintenance.

**Typical products/services:** Initial consult, follow-up sessions, treatment plans/packages, assessments, group programs, telehealth.

**Gotchas:**
- **Privacy is paramount.** Health information is sensitive — never put clinical detail in subject lines or unsecured channels; keep records in the workspace.
- **No advice or diagnosis over SMS/email.** Drafts should book/confirm/remind, not give clinical guidance. Defer clinical questions to an appointment.
- **Reminders reduce no-shows** — appointment reminders and rebooking nudges are the highest-value automations.
- **Funding schemes** (e.g. NDIS, Medicare, private health) change wording and process — confirm the funding type before drafting anything about cost or claiming.

**Comms style:** Warm, calm, respectful, clear about logistics (time, place, what to bring). Never clinical over text.

---

## Small manufacturing

**Typical pipeline:** Enquiry / RFQ → Spec / requirements gathered → Quote prepared → Quote sent → PO received → In production → Dispatched / delivered → Invoiced.

**Typical products/services:** Made-to-order runs, standard product lines, custom fabrication, repeat/wholesale orders, servicing.

**Gotchas:**
- **Quotes hinge on specs.** Don't quote without the spec (materials, quantities, tolerances, lead time) — flag missing inputs rather than guessing numbers.
- **Lead times and capacity** drive promises — never commit a delivery date without confirming production capacity.
- **Repeat / wholesale accounts** are the backbone — surface reorder timing and treat key accounts as relationships, not one-off deals.
- **PO + invoicing discipline** — track quote → PO → dispatch → invoice; flag dispatched jobs not yet invoiced.

**Comms style:** Precise, factual, specific about quantities, specs, lead times, and price. Professional B2B tone.

---

## Anything else

No matching section → use the generic `templates/CLAUDE.md` as-is and rely on the real workspace data. Ask the operator one or two short questions about their pipeline quirks and comms style rather than forcing a vertical that doesn't fit. If a vertical comes up repeatedly, add a section here.

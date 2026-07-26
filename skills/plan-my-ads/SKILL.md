---
name: Plan My Ads
description: Turn what you sell into a clear, ready-to-run ad plan: the one result to optimize for, the offer ad that proves demand, the creative brief, the copy, the budget and the numbers to watch. Built on Evelyn Weiss's ad method. Works with no ad account connected, and applies to Facebook, Google, TikTok, or a manual setup.
triggers:
  - plan my ads
  - plan a facebook ad
  - plan an ad campaign
  - help me plan meta ads
  - write an ad plan
  - map out my ads
function_slot: ads
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
produces_customer_facing_copy: true
engagement_copy: true
reads_for_profile:
  - offer
  - audience
  - budget_appetite
---

# Plan My Ads

You turn what an owner sells into a sharp, ready-to-run ad plan, not a lecture on
advertising, and not a live campaign. This is the thinking layer. In a few minutes
the owner walks away with one written plan they can act on: the single result to
optimize for, the offer ad that proves demand, the creative brief, the copy, the
budget with its math, the numbers to watch, the scaling ladder, and the
retargeting plan. It works with no ad account connected and applies just as well
to Facebook, Instagram, Google, TikTok, or a manual setup.

The method here is **Evelyn Weiss's ad method**. She runs one plain diagnostic ad
in front of cold traffic first, for every new offer, and reads the answer it gives
before spending on anything fancy. This skill runs that method as a live
consultation and generalizes it off her community-specific framing to any business
shape, whether a trade, a clinic, an ecommerce store, a hospitality venue, a professional
service. Attribute the method to Evelyn Weiss in your opening beat.

This sits at the top of the ads stack:

- **This skill** decides the plan: the objective, the diagnostic ad, the creative,
  the copy, the budget, the scaling and retargeting. Keyless, works from a cold
  start.
- **`run-my-ads`** is the doing. When the owner is ready to actually launch on
  Facebook and Instagram, it connects to their own ad account and builds the
  campaign shells to this plan, created paused and safe to review. It reads this
  plan as its input.

So when you finish, hand off to `run-my-ads` by outcome (Step 9), never as a
routed offer.

Ad copy is engagement copy, so it reads two homes before a hook is drafted: the
owner's writing voice at `marketing-strategy/<BrandName>/voice.md` (built by
`build-my-voice` or `build-brand-strategy`, and the one home for how they sound), and
the attention craft in
[`knowledge/storytelling-method.md`](../../knowledge/storytelling-method.md) for the
hook and the curiosity gap. When no voice doc exists, write from the owner's own
words and say plainly that none was found.
[`knowledge/communication-voice.md`](../../knowledge/communication-voice.md) is the
register for their plain operational messages, not for an ad hook.
Business-shape context (which ad shape tends to fit which kind of business) lives
in [`knowledge/industry-notes.md`](../../knowledge/industry-notes.md), and the
business fundamentals (capacity, local gravity, LTV) in
[`knowledge/business-method.md`](../../knowledge/business-method.md).

## The nine gates

Work these in order. Each gate is a pass before the default. The plan is the
thinking layer only. It names objectives in plain language and never hardcodes a
platform's internal setting names or enum spellings. Getting the exact settings
right for a given platform is `run-my-ads`'s job, read live from the platform at
build time.

### Gate 1: Read what we already know (silent)

Before you ask anything, read what's on hand so the plan is tailored, not generic:

- **`brand/brand.json`**: the business name, voice, tagline, and colors. The plan's
  copy and creative should sound like this brand.
- **The `./CLAUDE.md` business profile**: the business shape, the offer, the goal,
  and the constraint already diagnosed for this owner. Let it aim the plan.
- **`meta-ads-profile.json` if it exists**: read only its non-account fields
  (budget appetite, objective, geography) to sharpen the plan. Never read or rely
  on account IDs, and never require the profile at all.

None of this is required. The plan works from a cold start, from the owner's words
alone. If a file is missing, say so lightly and carry on.

### Gate 2: Pick the one result to optimize for

This is the single most important decision in the whole plan, so make it
deliberately. Map the owner's goal to the real conversion event, the moment money
or a genuine lead arrives. Never optimize for traffic or clicks. Traffic gets you traffic, not
customers, and it makes the diagnostic ad's answer meaningless.

| Owner's goal | Optimize for | Typical shapes |
|---|---|---|
| Sell something now | Purchase | ecommerce/retail, low-ticket service, paid access, product |
| Free signup / opt-in | Registration | free community, lead magnet, freemium |
| Enquiry / quote | Lead | trades, professional services, B2B |
| Booking / appointment | Booking made | clinic, hospitality, consultant, call-funnel service |

Name the result in plain language and confirm it with the owner. If their goal
could map two ways, ask ONE question to settle it: *"What's the moment that means
this ad worked for you: a sale, a signup, an enquiry, or a booking?"* The exact
setting names each platform uses, and which optimization is actually valid for the
objective, belong to `run-my-ads` at build time. The plan names the outcome, not
the platform's wording.

### Gate 3: Design the diagnostic offer ad

The first ad for any new offer is the plain "here's exactly what you get" ad: the
thing itself, shown as cleanly and as close to the real thing as possible. No
lifestyle gloss, no clever angle, no beautiful editing. Its whole job is to return
a **definite answer** about the offer, so that answer is trustworthy.

State, for THIS business, exactly what that ad shows (the finished job, the
product in use, the plate, the room, the dashboard, or the founder if the owner is the
product). Then set the read the owner will make from it (this diagnostic vocabulary
is for your own reasoning and the plan's dev-facing logic, never shown to the
end customer):

- **No conversions in the test window** means the offer needs work. Stop spending
  and go back to the offer itself, not the ad.
- **One or more conversions, ideally about one a day** means the offer has real
  demand and is worth more budget. Now it's worth optimizing.

Hold one line firmly: never enhance the ad past what the offer truly is to
manufacture a positive read. An offer that only converts when it's dressed up can't
be scaled honestly. A clean answer on a plain ad is the point.

### Gate 4: Creative brief (image-first)

Every ad is either a product image or a product video. That's the whole menu. Both
exist to show the thing plainly. Choose the format(s) for this business,
image-first:

- **Product image**: a real photo of the actual thing (the finished job, the
  product in use, the plate or room, the space or result); or a mockup of the
  digital thing (worksheets, a dashboard, a portal view); or a deliberate founder
  photo when the owner IS the product, chosen to convey the values that attract the
  right customer.
- **Product video**: a dictated screen or subject walkthrough (front-load the same
  walkthrough that lives on the offer page, so the ad and the page match exactly and
  the answer comes back cleaner and faster); or a lightly-edited explainer when the
  owner has the resources for it.

Note plainly in the brief: start image-first. Image ads are the lowest-cost,
fastest to make, and very often the most scalable. Move to video only if the image
gives no sign of life but the owner still believes in the offer, and even then
start with the simplest dictated walkthrough before any scripting. Say the honest
thing about production: raw and relatable often beats polished. A phone photo can
be the winning ad; over-polished creative can convert worse. A high-quality ad is
not the same as a highly-produced one.

### Gate 5: Ad copy draft (the six-part formula)

Keep the copy simple. Its job is to make "what you get is what you see"
unmistakable, so don't get persuasive. Fill in the six parts for this business:

1. **Hook that names the result** the audience wants.
2. **Who you are / relevant truthful background**: the facts that make the owner
   credible and the offer desirable, stated so they imply no specific results for
   anyone else.
3. **"I created [X] for [audience] who want [outcome]."**: the audience and the
   outcome they care about, named plainly.
4. **"Here's exactly what you get: 1, 2, 3, 4, 5."**: the concrete deliverables,
   spelled out. This is the heart of the ad; think it through and list the real
   things they receive.
5. **"You can get started here [price] [link]."**
6. **A final CTA on its own line below the link**: platforms often swallow a bare
   link, so repeat the call to action underneath it.

Then run the draft through the compliance rails and list any flags in the plan:

- Truthful, substantiable claims only.
- No implied-earnings claims.
- No false scarcity.

### Gate 6: Budget and KPIs

Size the test to learn cheaply. Set the daily test budget at roughly **1–3× the
offer price**, or about **2× the target cost per acquisition**, whichever the
owner's economics point to. The target cost comes from the customer's lifetime
value; if the owner knows or can estimate what a customer is worth, derive it from
there.

- **Run window: 48–72 hours.** A conversion inside about the first 48 hours, then
  about one a day, is the cadence that says demand is real. Leave it running; don't
  judge it in the first day.
- **Keep it deliberately small.** This is a diagnostic, not a scaling budget. The
  point is a cheap, quick, honest answer.

Include shape benchmarks as **illustrative and market-dependent**, never as
promises: a free signup often lands somewhere under roughly $2.50–$3 a signup where
demand is strong; a low-ticket paid offer can be profitable at a low price point;
a higher-ticket offer is judged against the target cost derived from its lifetime
value. Frame every number as a rough guide that depends on the owner's market, not
a guarantee.

### Gate 7: Scaling ladder

Once the offer has a heartbeat and conversions are steady, the job changes from
*finding* a winner to *improving the economics* so budget can rise without cost
rising. Give the owner the three levers, in order:

1. **Lift the click-through rate and ad quality**, so the cost per thousand
   impressions falls and each dollar buys more clicks.
2. **Raise the funnel conversion rate**: tighten the offer page so more of the
   clicks become customers.
3. **Add average order value**: order bumps, one-click upsells, complementary
   offers.

Only after those, test new angles, formats, and higher production. Then productize
standalone pieces of the offer (a course, a mini offer, a package) and validate
each one the same way (image first, then video) to open more paid pathways into
the same business. Think in multiple ways in, not either/or.

### Gate 8: Retargeting plan (the most profitable ad type)

Retargeting follows the warm visitors who already know the business and reminds
them now's a good time. It's the most profitable advertising because the audience
is small and warm, far cheaper to convince and to reach at high frequency than a
stranger.

- **Prerequisite:** conversion tracking is live, so the platform knows who visited
  the key offer page and who bought. Name this as the gate before any retargeting
  spend.
- **Audience:** a 180-day custom audience built from the pixel, filtered to the
  people who viewed the key offer page.
- **Budget:** tiny, about $2–$5 a day for most businesses; raise it only with
  heavy traffic.
- **Creative:** an image ad pointing to the exact offer-page URL, reusing the
  offer-page elements so the ad and page match.
- **Copy:** the offer-page copy re-angled for a return visitor: *"You looked at
  [X] and it stayed with you. Here's why now's a good time."* Build five
  variations and compliance-check them all, keeping only the lines that pass.
- **Run many creatives at high overall frequency** for the "illusion of
  omnipresence": many different visuals hitting the same warm audience aggregate
  over time into "I want to be part of this." Let it run and compound.

Say it plainly in the plan: if the owner runs nothing else, run retargeting.

### Gate 9: Write the ad plan and point at the run layer

Save the written ad plan (the shape is below) and close with the handoff to
`run-my-ads`, worded as prose, not a routed offer:

> "That's your ad plan. When you're ready to actually launch this on Facebook and
> Instagram, I can set the campaigns up for you, built to this plan, created
> paused and safe for you to review and switch on yourself. That needs a one-time
> connection to your ad account, and I'll walk you through it."

## The written ad-plan artifact

Write one plain-language markdown document to the owner's working directory. It's
customer-facing, and it attributes the method to Evelyn Weiss up top. The
sections, in order:

1. **Goal and objective**: the one conversion event to optimize for, named in
   plain language.
2. **The diagnostic offer ad**: what the plain "here's exactly what you get" ad is
   for this business, and the read criteria.
3. **Creative brief**: the chosen format(s), image-first, with the specific shots,
   mockups, or walkthrough to make, and the raw-beats-polished note.
4. **Ad copy draft**: the six-part formula filled in, with the compliance flags
   listed.
5. **Budget and KPIs**: the daily test budget with its math, the 48–72 hour
   window, the cadence, and the shape benchmark (illustrative).
6. **Scaling ladder**: the three economic levers, then productize-and-validate.
7. **Retargeting plan**: the audience, the tiny budget, the congruent creative,
   the five copy variations.
8. **What's next**: the handoff to `run-my-ads`.

The plan can say "your offer page should say X" so the ad and the page stay
congruent, but it never writes the offer page or its video. Authoring that page
belongs to a site or offer skill, not here.

## Hard rules

- **Keyless and reasoning-only.** No accounts, no keys, no files required. The plan
  runs to a finished document from the owner's words alone. Optional file reads
  (brand, business profile) only sharpen it; they are never the price of entry.
- **The plan is the thinking, `run-my-ads` is the doing.** Stop at the written
  plan. Never hardcode a platform's internal setting names or enum spellings, never
  quote exact API wording, and never claim to have created, connected, or launched
  anything here. The exact platform settings are read live at build time by
  `run-my-ads`.
- **The method is Evelyn Weiss's.** Attribute it in the opening beat and stay true
  to it: diagnostic ad first, image-first creative, the six-part copy formula,
  small honest test budget, scale by economics, retargeting as the highest-return
  ad.
- **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`.
- **Truthful claims only.** No implied earnings, no false scarcity, no invented
  results or made-up benchmarks. Benchmarks are illustrative and market-dependent,
  framed as rough guides.
- **The owner's voice and brand win.** When `brand/brand.json` or a brand brief
  exists, the copy and creative echo it. Reflect the owner's phrasing back so the
  plan reads as *"that's exactly the business I'm building."*
- **Applies to any platform.** The plan is portable to Facebook, Instagram, Google,
  TikTok, or a manual setup by design. Keep it that way. The thinking doesn't
  belong to one platform.

## Output shape

A short framing line that names the win and credits Evelyn Weiss's method, then the
eight-part written plan (goal and objective, the diagnostic offer ad, the creative
brief, the six-part copy draft with compliance flags, the budget and KPIs with
their math, the scaling ladder, the retargeting plan, and what's next), followed by
the plan-to-run handoff prose that points the owner at `run-my-ads` when they're
ready to launch.

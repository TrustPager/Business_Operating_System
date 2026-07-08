# BOS Onboarding — Starter-Projects Library

*The deduped, vertical-aware menu the earned build recommendation draws from (the "here's what I'd start with, and why" moment that follows the consultation, see §4). Every project offered as buildable-now maps to a real registry skill (`kernel/registry.json`, `status: active`). Decided-but-unbuilt floor ideas live in the non-routable [Planned (coming soon)](#planned-coming-soon) section so the vision is preserved without offering it as a live win. No invented apps; the registry is the source of truth.*

**Build-status legend:** `[live]` = ships today (in registry, `status: active`); `[floor-new]` = decided keyless floor build, not yet built (Planned only — now only `make-brand-video`).

**Constraint note (builders only, never in the operator pitch):** each group maps to the pressure it relieves per `knowledge/business-method.md` §3/§16 — 🏆 Win work → sales/leads, 💰 Get paid → profit/cash, 🤝 Stay on top of customers → retention, 🧭 Plan & decide → owner. Section-level mapping; the groups already carry it.

**Keyless/CRM tags:** `keyless` = zero accounts (`reasoning_only` / local MarkItDown read / keyless render / keyless hosted Firecrawl); `better_with_crm` = genuinely valuable cold but the payoff (auto-send, live tracking) lands on connect; `needs_crm` = requires live CRM data (last-activity dates, receivables) to work at all.

---

## 1. The library at a glance (deduped, grouped by relief)

### 🏆 Win work — quoting, proposals, finding leads, positioning

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **Turn a photo into a ready-to-send quote** | Send a photo of the job and a quick voice note — I'll turn it into a laid-out quote with line items and the scope structured, ready for your prices. | `quote-from-photo` `[live]` | keyless | instant_win |
| **Price one common job with confidence** | Tell me the work, your costs and hours and I'll build a defensible price with your margin shown openly, so every quote comes off a number you can stand behind, not a gut feel. | `price-my-work` `[live]` | keyless | first_build |
| **See what one job type actually makes you** | Pick one job you do all the time and tell me what it brings in and what it really costs, including the per-job cost of any financed or depreciating gear, and I'll show the true profit per job with your margin in dollars and the overhead share stated openly. Reusable spreadsheet model on request. | `profit-per-job` `[live]`, `price-my-work` `[live]` | keyless | first_build |
| **Write the proposal that wins the job** | Give me the scope and price and I'll write a sharp, on-brand proposal or SOW in your voice, laid out as a real .docx you can send today — built as a named package around the outcome the buyer wants, with options where they fit, so it can't be price-shopped line by line. | `write-a-proposal` `[live]`, `price-my-work` `[live]` | keyless | first_build |
| **Size up a competitor before you bid** | Point me at a rival's site and I'll read it like a sharp operator: how they position, what they appear to charge, and where the openings are for you. | `research-a-competitor` `[live]` | keyless | first_build |
| **See why you're not getting found, and fix it** | I'll read a few of your key pages and your local search presence, then hand you a short fix list in priority order (answer speed and reviews before keywords), each with the exact change to make, so more of the people searching for what you do actually land on you. | `get-found-online` `[live]` | keyless | first_build |
| **Research a prospect before the call** | Tell me who you're meeting and I'll hand you a one-page brief plus three sharp questions that make you the most prepared person in the room. | `research-before-call` `[live]` | keyless | instant_win |
| **Coach a sales call and close more** | Paste a call, quote visit, or discovery chat and I'll coach it like a sharp sales manager: what you did well, the one or two things to change next time, and the exact line to say. Sharpening how you sell is often the fastest way to win more of the work you already get in front of. | `coach-my-calls` `[live]` | keyless | first_build |
| **A firm letter, in your voice** | Tell me what happened and I'll write the firm, professional letter that holds the line: a variation notice, a dispute response, a payment-terms letter, factual and in your voice, as text or a real .docx. | `write-a-letter` `[live]` | keyless | first_build |

*Builder note (proposal):* the named-package build is `knowledge/business-method.md` §7.1 (Category-of-One, light pass), and the point of it is §7.6's commodity test — a proposal the buyer can't compare line by line with the one down the road.

### 💰 Get paid — chasing invoices, recovering missed work

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **See your cash position week by week, in a live spreadsheet** | Tell me your opening balance and what you expect in and out each week, and I'll build a week-by-week forecast with a live spreadsheet where the balance updates when you change a number, so you can see the tight weeks coming and plan for them. | `cash-flow-forecast` `[live]` | keyless | first_build |
| **Spot every completed job you forgot to invoice** | Give me your job list or receivables and I'll show what's done-but-unbilled and billed-but-unpaid, so you chase the lot in one go. | `outstanding-invoices` `[live]`, `email-me-a-report` `[live]` | needs_crm | deeper |
| **Set up your stalled-proposal follow-up radar** | I'll spot every proposal that's gone quiet and draft the well-timed nudge — no warm opportunity slips because nobody chased it. | `follow-up-radar` `[live]`, `design-nurture-sequence` `[live]` | needs_crm | deeper |

### 🤝 Stay on top of customers — follow-up, renewals, reorders, recovery

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **Track every renewal so nothing lapses** | Give me your licenses, insurances, certifications, registrations, and memberships with their renewal dates and I'll build a live tracker spreadsheet where the days-until-renewal column updates every time you open the file, sorted so the nearest date is always at the top. | `renewal-tracker` `[live]` | keyless | first_build |
| **Get your customer list into one clean place** | Wherever your customers live — notebook, phone, messy spreadsheet — give it to me and I'll pull it into one tidy list, a real file you can open today. | `import-from-anywhere` `[live]`, `build-spreadsheet` `[live]` | keyless | first_build |
| **Chase your stale quotes before they go cold** | I'll write the friendly "still keen?" follow-up plus the two-week nudge — you win more of the jobs you already quoted. | `draft-reply` `[live]`, `design-nurture-sequence` `[live]` | better_with_crm | first_build |
| **A recovery text for missed calls** | I'll write the text that fires the moment a call comes in unanswered, so you win the job back while they're still deciding. Write it now; it can send itself once connected. | `missed-call-recovery` `[live]`, `draft-reply` `[live]` | better_with_crm | first_build |
| **A stay-in-touch / renewal sequence** | I'll draft the anniversary check-ins, renewal nudges and reorder reminders in your voice — top-of-mind without lifting a finger; fires on real dates once connected. | `design-nurture-sequence` `[live]`, `wire-nurture-sequence` `[live]` | better_with_crm | deeper |
| **Renewal / reorder radar** | Connect your workspace and I'll surface every renewal or reorder coming up, flag the ones gone quiet, and draft each review message. | `follow-up-radar` `[live]`, `prep-for-call` `[live]` | needs_crm | deeper |
| **Turn a call/meeting into notes, decisions and next steps** | Paste a transcript or point me at a recording and I'll hand back a clean summary, the decisions, and the action list, ready to act on. | `transcript-summary` `[live]`, `build-customer-voice` `[live]` | keyless | instant_win |
| **Turn a client win into proof that sells** | Set it up at the start of a job and I'll capture the "before"; when the result lands I turn it into a before-and-after case study and a short video-testimonial script your client reads on camera ("before working with you I was X, now Z"). Includes the quick 5-star review-ask when you just want volume. Far stronger than a written review; tracked sends and a public reviews page are the connect-time upgrade. | `build-my-proof` `[live]` | keyless | first_build |
| **Set up a referral engine that actually asks** | I'll write the introduction-style ask (never "got any names?"), timed to the moment your client is happiest, recommend a reward that fits your business, and build a simple tracking sheet. Live referral links and reward tracking are the connect-time upgrade. | `set-up-referrals` `[live]` | keyless | first_build |
| **A welcome that lands the first win** | I'll draft the first-two-weeks welcome for a new customer: the same-day thank-you, the getting-started note, and the check-in that makes sure they get their first result fast, in your voice; fires on its own once connected. | `design-nurture-sequence` `[live]` | better_with_crm | deeper |

*Builder note (review engine):* `knowledge/business-method.md` §10.5 tier 2 — surface it ahead of any marketing build for trades/hospitality/clinic shapes; the review engine (with answer speed) is §10.5's hard gate before any lead-generation spend. *Builder note (welcome):* activation per business-method.md §11.3; the same-day welcome is how the discovery arc closes, §12.5.

### 🎨 Look professional & market — brand, content, video, social

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **Your brand, written down (positioning + voice)** | I'll turn your brain-dump into who you're for, what makes you the obvious choice, and exactly how you sound — then lock it into everything we make. | `build-brand-strategy` `[live]`, `brand-my-workspace` `[live]` | keyless | first_build |
| **A social-media strategy aimed at your goal** | Tell me what you want from social (more bookings, more leads, being the name your area knows, a bigger audience) and I'll build the strategy: which platform to focus on and why, how often to post, the 3-4 themes to post around, the mix, the one number to watch, and your first move this week. | `build-social-strategy` `[live]` | keyless | first_build |
| **The words for your post, in your voice** | Give me the idea and I'll write the on-brand caption and body in your voice, ready to publish. | `write-post-copy` `[live]`, `plan-my-content` `[live]` | keyless | first_build |
| **A product description that sells it** | Send a photo of one product (or a few notes) and I'll write the on-brand description for your store or listing, in your voice, leading with what the buyer gets. | `describe-a-product` `[live]` | keyless | first_build |
| **A ready-to-run ad plan off a proven method** | Tell me what you sell and who it's for and I'll build a clear ad plan off a proven method: the one result to optimize for, the offer that proves demand, the creative brief and copy, a starting budget, and the numbers to watch — ready day one, no ad account needed, and it fits Facebook, Google, TikTok or a manual setup. | `plan-my-ads` `[live]` | keyless | first_build |
| **Turn that plan into live Meta campaigns** | Once you've built your plan with `plan-my-ads`, I'll turn it into ready-to-launch Facebook and Instagram campaigns built to the same method, created paused and safe for you to check over, handed back with a clear checklist and the 72-hour rule. Plan it keyless, then run it once your Meta Ads account is connected. You switch them on yourself; nothing spends until you say so. | `run-my-ads` `[live]`, `plan-my-ads` `[live]` | needs_connection | deeper |
| **A fortnight of content, planned and written** | I'll turn your strategy into a dated two-week posting plan — what to post, when, on which channel — then write the first captions in your voice. | `plan-my-content` `[live]`, `write-post-copy` `[live]` | keyless | deeper |
| **The way your customers actually talk, captured** | Paste your reviews, testimonials or call notes and I'll pull out the exact phrases, the outcomes they want and the worries that stall them — the voice every bit of your marketing should echo. | `build-customer-voice` `[live]` | keyless | first_build |
| **Put a finished post together, ready to publish** | Hand me the caption and any image you've already made and I'll collate them into one clean, named folder with a short readme, so the whole post sits in one place when it's time to publish. | `assemble-content-pack` `[live]`, `write-post-copy` `[live]` | keyless | deeper |
| **Find the YouTube videos worth making in your niche** | Tell me your niche and channel and I'll study what the top channels cover, what viewers keep asking for in the comments, and the angles nobody is taking yet, then hand you a shortlist of video ideas that will land, each backed by what real viewers actually said. | `research-my-channel` `[live]` | keyless | first_build |
| **Turn that research into a real YouTube plan** | I'll turn your channel research into a clear channel strategy and a pipeline of videos, each with an idea, an angle, a working title, and a thumbnail concept ready to script, building on your social strategy and content plan so it all fits together. | `plan-my-youtube` `[live]`, `build-social-strategy` `[live]`, `plan-my-content` `[live]` | keyless | first_build |
| **Script your next video, beat by beat** | Give me a topic and I'll write a beat-by-beat video script in your voice, the hook, the promise, the points and a clear call to action, written so it can be filmed and rendered straight away, with every claim resting on real evidence. | `script-my-video` `[live]` | keyless | first_build |
| **Get your video ready to publish on YouTube** | Once your video is rendered, I'll gather it into one publish-ready folder: the video, the thumbnail, title options, a full description with chapters, tags, and a short upload checklist, so all that's left is for you to upload it yourself. | `package-my-video` `[live]`, `assemble-content-pack` `[live]` | keyless | deeper |

*Heavier branded-visual option (not a cold instant-win):* a brandable graphics studio (`make-social-post`) renders an on-brand post image. It is a heavier capability (a render pipeline, not a 2-minute keyless taste), so it's offered as a meatier follow-up once the owner has a strategy and copy — never the cold first win. The full brandable creative studio (palette/logo/fonts → branded stills and looped video from a brand kit) is coming as a future library module (per [D13](../docs/architecture/founder-decisions.md)); the strategy + copy wins stand on their own without it.

*(One more market capability is decided and on the way: a branded promo video. See [Planned (coming soon)](#planned-coming-soon).)*

### 🗂️ Save time on admin — read any file, forms, structure data

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **Throw me any file — I'll read it and structure it** | Messy PDF, supplier spreadsheet, scanned form, contract — send it over and I'll pull out the important bits as clean, usable data. | `extract-document` `[live]`, `compare-documents` `[live]` | keyless | instant_win |
| **Your fact-find / intake pack, read in seconds** | Drop in payslips, statements, IDs or a paper form — I'll pull out the details into one clean summary and tell you what's missing. | `extract-document` `[live]`, `compare-documents` `[live]`, `template-from-document` `[live]` | keyless | instant_win |
| **A reusable intake / RFQ form, drafted clean** | Hand me your current form or describe it and I'll turn it into a clean structured form spec with the right fields — ready to go live on connect. | `template-from-document` `[live]`, `build-form` `[live]` | better_with_crm | first_build |
| **The chase-the-missing-docs list** | Tell me what you asked a client for and what's landed; I'll show what's still missing and draft the warm chase. Tracks asked-vs-arrived live once connected. | `outstanding-documents` `[live]`, `extract-document` `[live]` | better_with_crm | first_build |
| **Build the spreadsheet that runs a slice of your business** | Job tracker, simple cashflow, lead log — tell me what you're keeping on top of and I'll build a clean, structured .xlsx you can open and fill today. | `build-spreadsheet` `[live]`, `import-from-anywhere` `[live]` | keyless | first_build |

### 🧭 Plan & decide — stress-test decisions, hire, knowledge base

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **Onboard your next team member** | I'll build the day-one onboarding pack (voice, role boundaries, the commands they get) so a new starter sounds like you from week one. | `onboard-team-member` `[live]`, `sync-team-standards` `[live]` | keyless | deeper |
| **A sharp, reusable prompt for a job you repeat** | Tell me the task you keep re-explaining and I'll write you a crisp, reusable prompt that gets it right every time. | `write-prompt` `[live]` | keyless | first_build |
| **Stress-test your next big decision** | A hire, a price rise, dropping a service? Tell me the call and I'll grill you on it — surface your assumptions, argue both sides at full strength, and name the one thing that would change the answer, before you commit. | `grill-me-on-this-decision` `[live]` | keyless | first_build |
| **A job ad + screening questions in your voice** | I'll write the job ad and screening questions that sound like you, so the right people apply and the wrong ones screen themselves out. | `write-a-job-ad` `[live]`, `onboard-team-member` `[live]` | keyless | deeper |
| **The policies & FAQs your business runs on** | Tell me how you handle deposits, cancellations, refunds or privacy and I'll write clean, on-brand policy and FAQ text for your site, emails or staff. | `write-a-policy` `[live]` | keyless | deeper |
| **Your one-page weekly scoreboard** | Tell me the handful of numbers your week turns on (enquiries in, conversations, jobs won, cash collected) and I'll build the one-page tracker you fill in ten minutes every week, so you always know which number to fix next. | `build-spreadsheet` `[live]` | keyless | first_build |

*Builder note (scoreboard):* the sheet's shape is `knowledge/business-method.md` §12.6; §16 makes it the standing first prescription for an owner with no numbers. The connect-time deepener — the workspace filling it on its own, the weekly review reading it — lives here in prose only; the row stays keyless with no connected ids in it.

### 🇦🇺 Australian businesses only (switches on once you confirm Region: AU)

*Region-gated. These appear only once the owner has explicitly confirmed their business is in Australia (`Region: AU` in the profile). They are never in the universal cold pool and are never offered until the region is confirmed in words. Inferring region from a city or address is never enough.*

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **Prepare your quarterly BAS GST figures** | Tell me the quarter's total sales and purchases and I'll prepare your Simpler-BAS figures (G1 total sales, 1A GST on sales, 1B GST on purchases) with the GST calc shown and the ATO source cited, ready for you to enter on your own BAS. I prepare the numbers; you lodge. | `estimate-my-bas` `[live]` | keyless requires_region:au | first_build |

---

## 2. The universal core (the safe default pool)

These work for **any** 2-10 person small business and are the default pool to draw the 3 from when the shape is unclear or generic. **Every item here is keyless**, so the whole pool survives a cold open; each one names a plain-language connect-time deepener where it has one. The decided-but-unbuilt market idea (a branded promo video) and the heavier brandable-visual studio (`make-social-post`, a render pipeline) are NOT in this cold pool: the promo video lives in [Planned (coming soon)](#planned-coming-soon), and the visual studio is a meatier follow-up plus a future library module (per [D13](../docs/architecture/founder-decisions.md)) — never the cold first win. The cold social/marketing win is the *strategy*, not a single rendered post.

**Live keyless core (the cold-open pool):**

1. **Your brand, written down** — `build-brand-strategy` + `brand-my-workspace` · keyless · first_build *(the spine — writes `brand.json`, reskins every later artifact)*
2. **A social-media strategy aimed at your goal** — `build-social-strategy` · keyless · first_build *(the cold social/marketing win: platform focus, cadence, goal-mapped pillars, the mix, the metric, the first move; `plan-my-content` then dates it, `write-post-copy` writes the posts)*
3. **Turn a photo into a ready-to-send quote** — `quote-from-photo` · keyless · instant_win
4. **Throw me any file — I'll read it and structure it** — `extract-document` + `compare-documents` · keyless · instant_win
5. **Your fact-find / intake pack, read in seconds** — `extract-document` + `compare-documents` + `template-from-document` · keyless · instant_win
6. **A sharp, reusable prompt for a job you repeat** — `write-prompt` · keyless · first_build
7. **Onboard your next team member** — `onboard-team-member` + `sync-team-standards` · keyless · deeper
8. **Price one common job with confidence** — `price-my-work` · keyless · first_build *(margin shown openly; the pricing engine quote-from-photo leans on)*
9. **See what one job type actually makes you**: `profit-per-job` · keyless · first_build *(true profit per job: revenue minus materials, labour, a stated overhead share, and the real per-job cost of financed/depreciating gear computed with the finance tool; margin shown as money; optional reusable .xlsx model; folds in margin so no separate margin app)*
10. **Stress-test your next big decision** — `grill-me-on-this-decision` · keyless · first_build
11. **The words for your post, in your voice** — `write-post-copy` · keyless · first_build
12. **A fortnight of content, planned and written** — `plan-my-content` + `write-post-copy` · keyless · deeper
13. **The way your customers actually talk, captured** — `build-customer-voice` · keyless · first_build
14. **A job ad + screening questions in your voice** — `write-a-job-ad` · keyless · deeper
15. **The policies & FAQs your business runs on** — `write-a-policy` · keyless · deeper
16. **Write the proposal that wins the job** — `write-a-proposal` + `price-my-work` · keyless · first_build *(real .docx; live signing template is the connect-time deepener)*
17. **Size up a competitor before you bid** — `research-a-competitor` · keyless · first_build *(keyless-but-online: reaches the live web via the hosted Firecrawl read)*
18. **Research a prospect before the call** — `research-before-call` · keyless · instant_win *(keyless-but-online, same Firecrawl read)*
19. **Turn a call into notes, decisions and next steps** — `transcript-summary` · keyless · instant_win *(paste a transcript or point at a local recording file; logs onto the customer's record as the connect-time deepener)*
20. **Get your customer list into one clean place** — `import-from-anywhere` + `build-spreadsheet` · keyless · first_build *(real clean file; seeding it into the CRM is the connect-time deepener)*
21. **Build the spreadsheet that runs a slice of your business** — `build-spreadsheet` · keyless · first_build *(job tracker / cashflow / lead log as a real .xlsx; live self-updating sheet is the connect-time deepener)*
22. **Put a finished post together, ready to publish** — `assemble-content-pack` + `write-post-copy` · keyless · deeper *(collates caption + any image + brief into one named folder; filing it into the workspace is the connect-time deepener)*
23. **A firm letter, in your voice** — `write-a-letter` · keyless · first_build *(a variation notice / dispute response / payment-terms letter; firm and factual, text or a real .docx)*
24. **A product description that sells it** — `describe-a-product` · keyless · first_build *(one product → an on-brand description for a store or listing; the product-seller market win)*
25. **See your cash position week by week, in a live spreadsheet** — `cash-flow-forecast` · keyless · first_build *(opening balance + expected inflows and outflows by week, 4-13 week horizon clamped, tightest week named as the one to plan for; live .xlsx where the running balance is a formula that recalculates when any number changes; budgeting folded in; no NPV)*
26. **Track every renewal so nothing lapses** — `renewal-tracker` · keyless · first_build *(licenses, insurances, certifications, registrations, memberships with renewal dates and optional lead-times; live .xlsx where the days-until-renewal column is a =DATE(yyyy,m,d)-TODAY() formula so it recalculates every open; rows soonest-first; status flags inside/outside lead window; connecting a CRM or calendar is the honest connect-time deepener for reminders that actually fire)*
27. **Your one-page weekly scoreboard** — `build-spreadsheet` · keyless · first_build *(the handful of numbers the week turns on — enquiries in, conversations, jobs won, cash collected, plus the one number this quarter turns on — filled in ten minutes a week; shape per business-method.md §12.6; the workspace filling it on its own and the weekly review reading it is the connect-time deepener)*
28. **See why you're not getting found, and fix it** — `get-found-online` · keyless · first_build *(keyless-but-online: reads a few key pages + local search presence via the hosted Firecrawl read, hands back a fix list ordered by the §10.5 gravity stack with the exact change per fix; real search volumes, backlinks, and rank tracking are the connect-time deepener)*
29. **Turn a client win into proof that sells** — `build-my-proof` · keyless · first_build *(the transformation-story engine: kickoff captures the "before", wrap turns the before→after into a case study + a video-testimonial script in the client's voice; quick 5-star review-ask folded in; tracked sends + public reviews page + video hosting are the connect-time deepener; §15 shape guard for regulated shapes)*
30. **Set up a referral engine that actually asks** — `set-up-referrals` · keyless · first_build *(§10.7: introduction-style ask timed to the win moment, mutual reward matched to the shape, a simple tracking sheet; live referral links + commission tracking + leaderboard are the connect-time deepener)*
31. **Coach a sales call and close more** — `coach-my-calls` · keyless · first_build *(paste a transcript → coaching vs the §12.5 discovery arc: what went well, the 1-2 highest-leverage fixes, a rehearsal line; auto-pull per team member + track improvement over time are the connect-time deepener)*

**Note for builders:** every copy-producing app (`build-social-strategy`, `write-post-copy`, `plan-my-content`, `write-a-job-ad`, `write-a-policy`, `write-a-proposal`, `write-a-letter`, `describe-a-product`) carries the content-guardrails anchor pointing at `knowledge/content-rules.md` (no em dashes, no invented evidence, no third-party vendor). Marketing framing is the owner's own choice, not a house style (`write-a-letter` keeps its labelled firm-but-factual exception for dispute letters). `transcript-summary`, `import-from-anywhere`, and `build-spreadsheet` are keyless on the floor (the MarkItDown paste/local-file read and the doc-lib WRITE side ship today, floor-completion-plan ruling #2); their CRM-side payoff (logging onto a record, seeding the customer database, a live self-updating sheet) is the plain-language connect-time deepener, never the price of the keyless win. The two research apps are keyless-but-online: they need connectivity at runtime but no account or key.

---

## 3. Shape-specific standouts (the best 2-3 extra per business shape)

Organised by **business shape** ([D12](../docs/architecture/founder-decisions.md); shapes + verticals in [`industry-notes.md`](industry-notes.md)). These beat the universal core *for that shape* because they hit a named gotcha. Surface them ahead of generic picks once the shape (and any vertical inside it) is known. Verticals nested under a shape keep their own specific standouts.

### Shape: Service / professional

The shape-wide standouts: winning the next piece of work and looking as professional as the expertise.
- **Write the proposal that wins the job** (`write-a-proposal` + `price-my-work`, live keyless) — proposals/recommendations are where the deal is won.
- **A social-media strategy for local authority** (`build-social-strategy`, live keyless) — being the obvious expert is how referrals start; the strategy aims it (often LinkedIn-led) before any single post.

**Mortgage & insurance broking** (verticals)
- **Your fact-find / intake pack, read in seconds** (`extract-document` + `compare-documents`) — highest-relief minute-one move for a broker drowning in payslips/statements/IDs.
- **Renewal radar** (`follow-up-radar` + `prep-for-call`, needs_crm) — for insurance, *renewals are the business*; surfacing them early is the most valuable follow-up.
- **The referral ask, in your voice** (`write-prompt` + `build-brand-strategy`) — referrals are the lifeblood of the pipeline. *(Pitches must never quote a rate, promise a settlement date, or imply unbound cover.)*

**Consulting & professional services** (vertical)
- **Stalled-proposal follow-up radar** (`follow-up-radar`, needs_crm) — "proposals stall in sent" is the named #1 gotcha.
- **A social strategy aimed at thought-leadership** (`build-social-strategy`, live keyless) → **a fortnight of content** (`plan-my-content`, live keyless) — set the authority strategy, then date it into posts; being the obvious expert is how referrals start.
- **Retainer renewal & upsell radar** (`sweep-my-day` + `follow-up-radar` + `weekly-review`, needs_crm) — retainers are recurring value; the renewal/upsell moment is the most valuable date.

**Technical / specialist services (engineering, environmental, specialist consulting)** (vertical)
- **Write the tender section that scores** (`write-a-proposal` tender/technical-section mode, live keyless) — methodology / technical-approach / capability sections answering an RFP, where price sits in a separate schedule; graded on approach, not price.
- **A firm letter, in your voice** (`write-a-letter`, live keyless) — variation notices and dispute responses are routine on technical jobs; firm, factual, and in the owner's voice.
- **A defensible price for one common job** (`price-my-work`, live keyless) — a number the owner can stand behind when the brief is technical.

### Shape: Trades / on-the-tools

- **A recovery text for missed calls** (`missed-call-recovery`) — speed-to-lead is the #1 trades gotcha; a missed call is a lost job.
- **Chase your stale quotes** (`draft-reply` + `design-nurture-sequence`) — quotes go cold in ~2 weeks; the chase wins jobs already quoted.
- **Turn a photo into a quote** (`quote-from-photo`) — a photo + voice note is the whole brief on the tools.
- **A review engine that runs itself** (`write-prompt` + `design-nurture-sequence`, better_with_crm) — the ask written today, firing on every completed job once connected; with answer speed, it comes before any marketing build.

**Small manufacturing / fabrication** (vertical, trades-shaped: spec-led, repeat accounts)
- **Your spec-to-price calculator** (`price-my-work`, live keyless) — quotes hinge on specs; a calculator turns any spec into a defensible number.
- **A reusable RFQ intake sheet** (`build-form` + `build-spreadsheet`, better_with_crm) — missing spec inputs stall every quote.
- **A reorder reminder system** (`design-nurture-sequence` + `follow-up-radar`, better_with_crm) — repeat/wholesale accounts are the backbone; reorder timing is the lifeblood.

### Shape: Product-seller / ecommerce-retail

Content and pricing are the daily blockers; the listing is the shopfront.
- **A product description that sells it** (`describe-a-product`, live keyless) — every product needs on-brand description copy; the blank "description" box is the daily blocker. One product per run, photo or notes in.
- **A social-media strategy aimed at sales** (`build-social-strategy`, live keyless) → **the words for your post** (`write-post-copy`, live keyless) — product launches and promos live or die on social; set the sales-led strategy, then write the posts that lead with what the buyer gets.
- **A firm letter, in your voice** (`write-a-letter`, live keyless) — supplier disputes, refund/return responses, payment-terms letters: firm and factual, in the owner's voice.

### Shape: Hospitality / walk-in

Being found drives covers; Instagram (and local social) is a primary channel; functions run on deposits.
- **A social-media strategy aimed at more bookings** (`build-social-strategy`, live keyless) — a steady, on-brand social presence directly fills tables and functions; the strategy picks the platform (usually Instagram-led), the cadence, and the pillars before any single post. Then **a fortnight of content** (`plan-my-content`, live keyless) dates it.
- **The policies your bookings run on** (`write-a-policy`, live keyless) — clear deposit, cancellation, and group-booking wording prevents no-shows on the high-value functions.
- **A job ad in your voice** (`write-a-job-ad`, live keyless) — rosters and peaks mean hiring is routine; an ad that sounds like the venue draws the right people.
- **A review engine that runs itself** (`write-prompt` + `design-nurture-sequence`, better_with_crm) — a steady drip of recent reviews fills tables; the ask and reply patterns written today, firing on their own once connected, ahead of any marketing build.

### Shape: Clinic / appointment

Reminders protect the calendar; privacy and funding wording come first.
- **A calm reminder & rebooking sequence** (`design-nurture-sequence`, better_with_crm) — reminders are the highest-value automation (no-show reduction); logistics-only, never clinical over text.
- **Your intake & consent forms, drafted clean** (`template-from-document` + `extract-document`) — proper paperwork without retyping; privacy-safe, ready on connect.
- **Plain-English funding explainers** (`write-a-policy`, live keyless) — NDIS/Medicare/private-health wording, confirmed before drafting. *(Allied health = the privacy-heavy vertical; wellness/personal-care studios share the book-attend-rebook rhythm with a lighter privacy load and lean on `build-social-strategy` to fill the calendar.)*
- **A review engine that runs itself** (`write-prompt` + `design-nurture-sequence`, better_with_crm) — recent reviews fill the calendar; the ask and reply patterns written today (logistics-only, never clinical), firing on their own once connected, ahead of any marketing build.

### Shape: Courses / community / coaching

The content engine is the shopfront; retention quietly decides everything; the first member win in week one is the keep.
- **Your content engine, planned from pillars** (`build-social-strategy`, live keyless) → **a fortnight of content, dated** (`plan-my-content`, live keyless) — the content demand never stops; pillars turn one strong idea into the post, the email, and the lesson instead of a blank page every morning.
- **A member-onboarding sequence that lands the first win** (`design-nurture-sequence`, better_with_crm) — welcome → orient → first win → celebrate; the member who wins in week one renews. Draft it keyless in chat; it goes live on connect.
- **Your members' wins, in their words** (`build-customer-voice`, live keyless) — captured wins and testimonials ARE the sales page for the next intake; make collecting them systematic.

### Shape: Software / digital product

Activation beats acquisition; every release is a content moment; support words feed everything.
- **An activation sequence from signup to first value** (`design-nurture-sequence`, better_with_crm) — the welcome-to-first-value path is where churn is prevented in advance. Draft it keyless in chat; it goes live on connect.
- **Ship-in-public launch posts** (`write-post-copy` + `plan-my-content`, live keyless) — every release becomes the changelog, the post, and the email; a visible shipping rhythm reads as a healthy product.
- **A pricing/packaging decision, pressure-tested** (`grill-me-on-this-decision` + `price-my-work`, live keyless) — tiers, the free-tier line, and the upgrade moment, reasoned with the recurring math in view.

---

## Planned (coming soon)

**Non-routable.** These are decided keyless floor builds that are **not yet in the registry**, so start-here must never offer them as a buildable-now win and the binding check treats this whole section as off the floor. The curation lives here so the vision is preserved and ready to promote into the live menu the moment each app ships (build order in [`floor-roster.md`](../docs/architecture/floor-roster.md) "Derived build set"). When an app here lands in `kernel/registry.json` with `requires_credential: none`, move its row up into the live section above.

| Project | One-line operator pitch | Builds on | Tier |
|---|---|---|---|
| **A short branded promo video** | A 15-30s branded video (your work, your colours, text on screen), the kind of thing that stops the scroll. No film crew. | `make-brand-video` `[floor-new]` | deeper |

*Every copy-producing Planned app carries the content-guardrails anchor (`knowledge/content-rules.md`) when built; marketing framing is the owner's choice, positive-only is not imposed on a client's copy.*

---

## Opt-in setup modules (recommended, not in the 3-menu)

These are live keyless modules that improve the owner's Claude Code environment
rather than producing a business artifact. They are NOT offered in the
3-options menu (start-here routes to business wins, not config tasks), but they
are real, active, and worth pointing to whenever the context fits.

| Module | What it does | Builds on | Keyless/CRM |
|---|---|---|---|
| **Set up Claude Code best practices** | Walk through the recommended working-style and permissions setup for Claude Code in two modes: apply the recommended defaults in one step, or answer a few questions to build a personalised version. Additive and reversible at any time. | `tune-my-setup` `[live]` | keyless |

*Surface this when:* the owner asks about Claude Code settings, permissions, or
working-style preferences; when they report Claude prompting them too often for
safe reads; or when they want to make their assistant feel more natural. Point
them to `/tune-my-setup`.

---

## 4. The 3-options selection logic

> **Presentation revised 2026-07-03:** this logic still picks the ~3, but they are
> now delivered as a *recommendation with alternatives* AFTER the collaborative
> consultation (or a terse owner's quick win), never as a cold opening menu. See
> the framing note at the end of this section and
> `docs/architecture/2026-07-03-collaborative-consultation-design.md`.

**Inputs:** `vertical`, `named_relief` (the RELIEF field — what eats their week), `connected` (CRM yes/no), `already_built` (project names done this session).

**The algorithm:**

**Complexity/cost gate (applies to EVERY option — custom or library):** only offer a project that's **finishable in one focused sitting** (one clear artifact), **bounded** (one photo / one competitor / this week's post — never "all your X"), and **token-frugal** (won't flood the context window). Heavy / sprawling / open-ended builds are excluded cold; if a big idea is the obvious fit, offer a **bounded first slice**, not the epic. Never let a first session burn the owner's context window or kick off a multi-hour build.

0. **Custom-first (the default when there's an obvious fit).** If the owner's own situation points to an obvious, high-fit bespoke project, that is the DEFAULT and leads — even if it's not in this library. This library is the **safety net**: it guarantees there's always at least one option serving a real problem they named, for when no obvious custom project exists. (TrustPager is reactive-only: slot-3 "auto-later once connected" options describe the OUTCOME; never name TrustPager unless the owner asks what else the BOS can do or about CRMs.)
1. **Filter out anything they've already built.** Never re-offer `already_built`.
2. **Gate by trust + connection.** Cold (nothing connected, first pivot): draw **only from the keyless `first_build` pool** (`instant_win` is the pre-pivot taste, not a menu item; `deeper` and any `needs_crm`/`better_with_crm` project is held back). As trust accrues or a CRM connects, open up `deeper` and `better_with_crm`.
3a. **Anchor on the diagnosed pressure point when one exists.** If the profile carries a diagnosed pressure point or a logged contradiction (start-here rule 2b), slot 1 maps to that constraint's move per `knowledge/business-method.md` §16 — filtered to what's live and keyless cold, exactly like every other offer. Two hard sub-rules: local shapes asking for leads get answer-speed + the review engine offered before ANY marketing build (§10.5's gate — cold, that's the recovery text drafted now to fire on connect, plus the review-ask kit); an owner at capacity asking for leads gets the pricing build first (§8.3). When no diagnosis exists, fall through to 3 unchanged.
3. **Anchor on the named relief.** The first of the 3 must map to `named_relief`, and cold it must be a **live keyless** win (the one Planned project below is named for vision only — never lead with it until it ships). Relief → project lead:
   - quoting → *photo-to-quote* (live) · *Price this job* (live) · *A proposal that wins* (live keyless)
   - winning the sale / closing / "I get leads but don't convert" → *Coach a sales call and close more* (live keyless — the cold lead here; sharpen the motion before chasing more volume, §3 constraint #2) · *A proposal that wins* (live keyless) · *Price this job* (live)
   - finding leads → *See why you're not getting found* (live keyless, online — for a local/service business this is often the best-fit lead, and it self-enforces the §10.5 gate by ordering answer-speed + reviews ahead of keywords) · *Set up a referral engine that actually asks* (live keyless — word-of-mouth is the cheapest lead source, §10.7) · *Size up a competitor* (live keyless, online) · *Research a prospect* (live keyless, online); fall back to *Your brand, written down* (live) if offline
   - chasing invoices → (cold) *Price this job* (live) or *Your brand, written down* (live) or *Chase stale quotes* (better_with_crm); (connected) *Spot uninvoiced jobs* / *follow-up radar*
   - looking professional → *Your brand, written down* (live) · *Turn a client win into proof that sells* (live keyless — a real before→after case study + video testimonial beats any claim, §6 Belief) · *A proposal that wins* (live keyless)
   - staying on top of customers → *Throw me any file* (live) / *call-to-notes* (live keyless) / *Turn a client win into proof that sells* (live keyless) / *Set up a referral engine* (live keyless) / *clean customer list* (live keyless) / *recovery text* (better_with_crm)
   - content/marketing / "get more known" / "grow my socials" → *A social-media strategy aimed at your goal* (live keyless, the cold lead) · *fortnight of content* (live) · *post copy in your voice* (live) · *See why you're not getting found* (live keyless, online — when "get more known" is really "get found in search") · *put a finished post together* (live keyless) · (product sellers) *A product description that sells it* (live keyless). *(The branded-visual studio is a meatier follow-up / future library module, never the cold lead.)*
   - firm letter / dispute / variation → *A firm letter, in your voice* (live keyless)
   - thinking/deciding → *A sharp reusable prompt* (live) · *Stress-test your decision* (live)
   - hiring/team → *A job ad + screening questions* (live) · *onboard your next team member* (live)
   - cash / runway / "will I make rent" / "tight month" / "what's coming in and out" → *See your cash position week by week* (`cash-flow-forecast`, live keyless)
   - policies/admin → *The policies & FAQs your business runs on* (live) · *Build a spreadsheet for a slice* (live keyless) · *clean customer list* (live keyless)
4. **Pick the vertical standout if one matches the relief**, else fall to the universal core.
5. **Shape the 3 as quick-win + meatier + aspirational:**
   - **Slot 1 — quick win** that nails the named relief (the dopamine hit; a short, visibly-finished artifact).
   - **Slot 2 — meatier first_build** that deepens the profile (brand, pricing brain, proposal — captures rates/voice/positioning as a side effect).
   - **Slot 3 — aspirational** that hints at the operator they're becoming (competitor research, content plan, decision grilling) — and, if `connected=false` and trust is rising, this slot is the gentle place to seed a `better_with_crm` project ("…and it can send itself once your workspace is connected"). The aspirational slot prefers more-of-what-works or a sharper version of it over a genuinely new channel (`knowledge/business-method.md` §4.4) — never pitch "new" as the dream by default.
6. **Keep slot 1 + slot 2 keyless** at the cold open. Only let slot 3 carry a CRM-tagged option, and only phrase it as a "now, then auto-later" build.
7. **Each option is phrased outcome-first**, in plain operator language, as "here's something we could build for you" — never jargon, never the app name.

**The framing (a recommendation, not a menu — revised 2026-07-03).** Per
`docs/architecture/2026-07-03-collaborative-consultation-design.md`, the build is
reached AFTER the collaborative consultation (or a terse owner's quick win), never
as a cold opening menu. Present it as a consultant's recommendation: reflect what
you now understand (the goal + the real constraint, the *give*), then lead with
the ONE build you'd recommend and *why*, offering the other two as alternatives so
it stays their call. The selection still picks the same ~3 (constraint-aware,
custom-first); only the presentation changed from "pick one of three" to "here's
what I'd start with, and why". Worked example for a trades owner you diagnosed as
quote-cycle leakage:

> "You're winning plenty, but every quote's built from scratch and a few go cold before you get to chase them. Given that, the first thing I'd build with you is turning a job photo into a ready-to-send quote, because it takes the slowest part of winning work off your plate. If you'd rather start elsewhere, we could get your brand written down so every quote sounds unmistakably like you, or set up the stale-quote chase so fewer slip away. Your call, and we build it together."

*Worked example — broker, relief = "staying on top of paperwork", nothing connected:* slot 1 *Fact-find pack read in seconds* (quick win, keyless, hits relief), slot 2 *Your brand & lender-file voice* (meatier, keyless, deepens profile), slot 3 *The outstanding-docs chaser* ("…I track asked-vs-arrived live once your workspace is connected" — aspirational + seeds the connect).

---

## 5. Earned-progression notes

**Tier map (which is what):**

- **instant_win** (the <2-min pre-pivot taste — *not* offered in the 3-menu): *photo-to-quote* on one photo, *throw-me-any-file*, *call-to-notes* (live keyless), *Research a prospect before the call* (live keyless, online). These trigger the pivot; the menu is drawn from the tiers below. *(The single rendered "branded post" is no longer a cold taste — it's a heavier render-pipeline option; the cold social/marketing win is the strategy, a first_build.)*
- **first_build** (the cold 3-option pool, keyless, visibly operator-grade, deepens profile as a side effect): the LIVE cold pool is *Your brand written down*, *A social-media strategy aimed at your goal*, *photo-to-quote*, *fact-find pack*, *throw-me-any-file*, *a sharp reusable prompt*, *Price this job*, *Stress-test your decision*, *post copy in your voice*, *customer-voice doc*, *Write the proposal that wins the job* (priced or tender/technical-section mode), *A firm letter in your voice*, *A product description that sells it* (product sellers), *Size up a competitor* (online), *clean customer list*, *Build a spreadsheet for a slice*. The two research apps are keyless-but-online, so fall back to an offline-safe pick if there's no connectivity.
- **deeper** (offered once trust is high or a connection exists): the live keyless deeper set — *onboard a team member*, *fortnight of content*, *job ad + screening*, *policies & FAQs*, *put a finished post together* — plus the still-Planned-or-connected set — *branded promo video*, *uninvoiced-jobs*, *renewal/reorder radar*, *nurture sequences*.

**The CRM/TrustPager on-ramp (the high-trust conversation seeders).** Each of these ships a real keyless win today; their fuller payoff lands on connect, so they are the natural, non-cold bridge to "connect your workspace" — described in plain language, never named as a tool or a requirement:

- **Get your customer list into one clean place** (`import-from-anywhere`) — keyless clean file today; seeding it into the customer database is the connect-time deepener, the single most natural on-ramp.
- **Turn a call into notes** (`transcript-summary`) — keyless standalone summary today; logging it straight onto the client's record is the connect-time deepener.
- **Build a spreadsheet for a slice** (`build-spreadsheet`) — keyless real .xlsx today; a live, self-updating workspace sheet is the connect-time deepener.
- **A recovery text for missed calls** / **Chase stale quotes** / **A renewal/reorder sequence** (`missed-call-recovery`, `design-nurture-sequence`, `wire-nurture-sequence`) — "write it now, it sends itself once connected" (auto-fire, better_with_crm).
- **The outstanding-docs chaser** (`outstanding-documents`) — works off your checklist cold; tracks asked-vs-arrived live once connected.
- **Policies / knowledge base** (`build-knowledge-base-from-docs`) — clean docs cold; powers the AI assistant and voice agent on connect.

**`needs_crm` (held for the deeper tier only, never cold):** *Spot uninvoiced jobs* (`outstanding-invoices` — needs receivables + activity dates), *stalled-proposal radar* and *renewal radar* (`follow-up-radar`, `sweep-my-day`, `weekly-review` — need live `last_activity_at`). These are reserved as the "look what your connected workspace now watches for you" reward once trust is earned.

**Profile-deepening as a side effect (why building beats interrogating):** *pricing/proposal* → captures rates, cost structure, job types; *brand written down* → writes `brand.json` (positioning, voice) that reskins all future creative; *content plan/video* → captures product range, ideal-work focus; *competitor research* → captures the competitive set; *intake/RFQ form* → captures what a "complete brief" means for this owner. Each pick the owner makes deepens the operator profile organically — the build IS the discovery.

---

**Files this draws from (all under `C:\Users\USER\Desktop\Final Piece Docs\Business_Operating_System\`):** `kernel\registry.json` (the capability catalogue + credential/data_path per skill — the source of truth for what is live/keyless), `docs\architecture\floor-completion-plan.md` (the decided keyless floor builds; the only one still `[floor-new]` / Planned today is `make-brand-video`; ruling #2 on `transcript-summary` is now satisfied — its keyless paste/local-file path ships), `docs\architecture\skill-extraction-audit.md` (the floor/extractable/trustpager_native buckets), `knowledge\industry-notes.md` (per-vertical gotchas driving the relief targeting).
# BOS Onboarding — Starter-Projects Library

*The deduped, vertical-aware menu the "3 things we could build" moment draws from. Every project offered as buildable-now maps to a real registry skill (`kernel/registry.json`, `status: active`). Decided-but-unbuilt floor ideas live in the non-routable [Planned (coming soon)](#planned-coming-soon) section so the vision is preserved without offering it as a live win. No invented apps; the registry is the source of truth.*

**Build-status legend:** `[live]` = ships today (in registry, `status: active`); `[floor-new]` = decided keyless floor build, not yet built (Planned only); `[fix]` = exists but needs the keyless paste/local-file path (only `transcript-summary`).

**Keyless/CRM tags:** `keyless` = zero accounts (`reasoning_only` / local MarkItDown read / keyless render / keyless hosted Firecrawl); `better_with_crm` = genuinely valuable cold but the payoff (auto-send, live tracking) lands on connect; `needs_crm` = requires live CRM data (last-activity dates, receivables) to work at all.

---

## 1. The library at a glance (deduped, grouped by relief)

### 🏆 Win work — quoting, proposals, finding leads, positioning

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **Turn a photo into a ready-to-send quote** | Send a photo of the job and a quick voice note — I'll turn it into a laid-out quote with line items and the scope structured, ready for your prices. | `quote-from-photo` `[live]` | keyless | instant_win |

*(More win-work first-wins are decided and on the way: defensible pricing, on-brand proposals, competitor and pre-call research. See [Planned (coming soon)](#planned-coming-soon).)*

### 💰 Get paid — chasing invoices, recovering missed work

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **Spot every completed job you forgot to invoice** | Give me your job list or receivables and I'll show what's done-but-unbilled and billed-but-unpaid, so you chase the lot in one go. | `outstanding-invoices` `[live]`, `email-me-a-report` `[live]` | needs_crm | deeper |
| **Set up your stalled-proposal follow-up radar** | I'll spot every proposal that's gone quiet and draft the well-timed nudge — no warm opportunity slips because nobody chased it. | `follow-up-radar` `[live]`, `design-nurture-sequence` `[live]` | needs_crm | deeper |

### 🤝 Stay on top of customers — follow-up, renewals, reorders, recovery

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **Get your customer list into one clean place** | Wherever your customers live — notebook, phone, messy spreadsheet — give it to me and I'll pull it into one tidy list. | `import-from-anywhere` `[live]`, `audit-my-data` `[live]`, `build-spreadsheet` `[live]` | better_with_crm | deeper |
| **Chase your stale quotes before they go cold** | I'll write the friendly "still keen?" follow-up plus the two-week nudge — you win more of the jobs you already quoted. | `draft-reply` `[live]`, `design-nurture-sequence` `[live]` | better_with_crm | first_build |
| **A recovery text for missed calls** | I'll write the text that fires the moment you miss a call, so you stop losing jobs to whoever picked up first. Write it now; it can send itself once connected. | `missed-call-recovery` `[live]`, `draft-reply` `[live]` | better_with_crm | first_build |
| **A stay-in-touch / renewal sequence** | I'll draft the anniversary check-ins, renewal nudges and reorder reminders in your voice — top-of-mind without lifting a finger; fires on real dates once connected. | `design-nurture-sequence` `[live]`, `wire-nurture-sequence` `[live]` | better_with_crm | deeper |
| **Renewal / reorder radar** | Connect your workspace and I'll surface every renewal or reorder coming up, flag the ones gone quiet, and draft each review message. | `follow-up-radar` `[live]`, `prep-for-call` `[live]` | needs_crm | deeper |
| **Turn a call/meeting into notes, decisions and next steps** | Paste a transcript or recording and I'll hand back a clean summary, the decisions, and the action list — the follow-up writes itself. | `transcript-summary` `[fix]`, `build-customer-voice` `[live]` | better_with_crm | instant_win |

### 🎨 Look professional & market — brand, content, video, social

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **Your brand, written down (positioning + voice)** | I'll turn your brain-dump into who you're for, what makes you the obvious choice, and exactly how you sound — then lock it into everything we make. | `build-brand-strategy` `[live]`, `brand-my-workspace` `[live]` | keyless | first_build |
| **A branded post you can publish today** | Give me one thing you want to say this week and I'll make the on-brand graphic — ready to drop straight on socials. | `make-social-post` `[live]` | keyless | instant_win |

*(More market first-wins are decided and on the way: a fortnight of planned-and-written content, a branded promo video, on-brand policies and a capabilities one-pager. See [Planned (coming soon)](#planned-coming-soon).)*

### 🗂️ Save time on admin — read any file, forms, structure data

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **Throw me any file — I'll read it and structure it** | Messy PDF, supplier spreadsheet, scanned form, contract — send it over and I'll pull out the important bits as clean, usable data. | `extract-document` `[live]`, `compare-documents` `[live]` | keyless | instant_win |
| **Your fact-find / intake pack, read in seconds** | Drop in payslips, statements, IDs or a paper form — I'll pull out the details into one clean summary and tell you what's missing. | `extract-document` `[live]`, `compare-documents` `[live]`, `template-from-document` `[live]` | keyless | instant_win |
| **A reusable intake / RFQ form, drafted clean** | Hand me your current form or describe it and I'll turn it into a clean structured form spec with the right fields — ready to go live on connect. | `template-from-document` `[live]`, `build-form` `[live]` | better_with_crm | first_build |
| **The chase-the-missing-docs list** | Tell me what you asked a client for and what's landed; I'll show what's still missing and draft the warm chase. Tracks asked-vs-arrived live once connected. | `outstanding-documents` `[live]`, `extract-document` `[live]` | better_with_crm | first_build |
| **Build the spreadsheet that runs a slice of your business** | Job tracker, simple cashflow, lead log — tell me what you're keeping on top of and I'll build a clean, structured sheet that scales. | `build-spreadsheet` `[live]`, `import-from-anywhere` `[live]` | better_with_crm | deeper |

### 🧭 Plan & decide — stress-test decisions, hire, knowledge base

| Project | One-line operator pitch | Builds on | Keyless/CRM | Tier |
|---|---|---|---|---|
| **Onboard your next team member** | I'll build the day-one onboarding pack (voice, role boundaries, the commands they get) so a new starter sounds like you from week one. | `onboard-team-member` `[live]`, `sync-team-standards` `[live]` | keyless | deeper |
| **A sharp, reusable prompt for a job you repeat** | Tell me the task you keep re-explaining and I'll write you a crisp, reusable prompt that gets it right every time. | `write-prompt` `[live]` | keyless | first_build |

*(More plan-and-decide first-wins are decided and on the way: a decision-grilling, a job ad + screening questions, your process/compliance playbook. See [Planned (coming soon)](#planned-coming-soon).)*

---

## 2. The universal core (the safe default pool)

These work for **any** 2-10 person AU service business and are the default pool to draw the 3 from when the vertical is unclear or generic. **All but the CRM-tagged ones are keyless**, so they survive a cold open. Items marked *(Planned)* are decided but not yet built, so they are never offered as a buildable-now win. See [Planned (coming soon)](#planned-coming-soon).

**Live keyless core (the cold-open pool):**

1. **Your brand, written down** — `build-brand-strategy` + `brand-my-workspace` · keyless · first_build *(the spine — writes `brand.json`, reskins every later artifact)*
2. **A branded post you can publish today** — `make-social-post` · keyless · instant_win
3. **Turn a photo into a ready-to-send quote** — `quote-from-photo` · keyless · instant_win
4. **Throw me any file — I'll read it and structure it** — `extract-document` + `compare-documents` · keyless · instant_win
5. **Your fact-find / intake pack, read in seconds** — `extract-document` + `compare-documents` + `template-from-document` · keyless · instant_win
6. **A sharp, reusable prompt for a job you repeat** — `write-prompt` · keyless · first_build
7. **Onboard your next team member** — `onboard-team-member` + `sync-team-standards` · keyless · deeper

**Connected-tier core (opened once a CRM connects; honestly flagged, never cold-keyless):**

8. **Turn a call into notes, decisions and next steps** — `transcript-summary` `[fix]` · better_with_crm · instant_win
9. **Get your customer list into one clean place** — `import-from-anywhere` + `build-spreadsheet` · better_with_crm · deeper

**Planned core (decided, not yet built, never offered as buildable now):**

- **Price this job with confidence** — `price-my-work` *(Planned)* · first_build
- **Write the proposal that wins the job** — `write-a-proposal` *(Planned)* · first_build
- **Size up a competitor before you bid** — `research-a-competitor` *(Planned)* · first_build
- **Research a prospect before the call** — `research-before-call` *(Planned)* · instant_win
- **Stress-test your next big decision** — `grill-me-on-this-decision` *(Planned)* · first_build
- **A fortnight of content, planned and written** — `plan-my-content` *(Planned)* · deeper
- **A job ad + screening questions in your voice** — `write-a-job-ad` *(Planned)* · deeper
- **Set the policies & FAQs your business runs on** — `write-a-policy` *(Planned)* · deeper

**Note for builders:** every copy-producing Planned app (`write-post-copy`, `plan-my-content`, `write-a-proposal`, `write-a-job-ad`, `write-a-policy`) must enforce the positive-only language rule (global CLAUDE.md + floor-completion-plan DoD) when built. `transcript-summary` is tagged `better_with_crm` not keyless until the planned MarkItDown paste-path lands (floor-completion-plan ruling #2).

---

## 3. Vertical-specific standouts (the best 2-3 extra per vertical)

These beat the universal core *for that vertical* because they hit a named gotcha. Surface them ahead of generic picks when the vertical is known.

**Trades**
- **A recovery text for missed calls** (`missed-call-recovery`) — speed-to-lead is the #1 trades gotcha; a missed call is a lost job.
- **Chase your stale quotes** (`draft-reply` + `design-nurture-sequence`) — quotes go cold in ~2 weeks; the chase wins jobs already quoted.
- **Turn a photo into a quote** (`quote-from-photo`) — a photo + voice note is the whole brief on the tools.

**Mortgage & insurance broking**
- **Your fact-find / intake pack, read in seconds** (`extract-document` + `compare-documents`) — highest-relief minute-one move for a broker drowning in payslips/statements/IDs.
- **Renewal radar** (`follow-up-radar` + `prep-for-call`, needs_crm) — for insurance, *renewals are the business*; surfacing them early is the most valuable follow-up.
- **The referral ask, in your voice** (`write-prompt` + `build-brand-strategy`) — referrals are the lifeblood of the pipeline. *(Pitches must never quote a rate, promise a settlement date, or imply unbound cover.)*

**Allied health**
- **Your intake & consent forms, drafted clean** (`template-from-document` + `extract-document`) — proper paperwork without retyping; privacy-safe, ready on connect.
- **A calm reminder & rebooking sequence** (`design-nurture-sequence`, better_with_crm) — reminders are the highest-value automation (no-show reduction); logistics-only, never clinical over text.
- **Plain-English funding explainers** (`write-a-policy` *(Planned)*) — NDIS/Medicare/private-health wording, confirmed before drafting.

**Consulting & professional services**
- **Stalled-proposal follow-up radar** (`follow-up-radar`, needs_crm) — "proposals stall in sent" is the named #1 gotcha.
- **A fortnight of thought-leadership content** (`plan-my-content` *(Planned)*) — being the obvious expert is how referrals start.
- **Retainer renewal & upsell radar** (`sweep-my-day` + `follow-up-radar` + `weekly-review`, needs_crm) — retainers are recurring value; the renewal/upsell moment is the most valuable date.

**Small manufacturing / product**
- **Your spec-to-price calculator** (`price-my-work` *(Planned)*) — quotes hinge on specs; a calculator turns any spec into a defensible number.
- **A reusable RFQ intake sheet** (`build-form` + `build-spreadsheet`, better_with_crm) — missing spec inputs stall every quote.
- **A reorder reminder system** (`design-nurture-sequence` + `follow-up-radar`, better_with_crm) — repeat/wholesale accounts are the backbone; reorder timing is the lifeblood.

---

## Planned (coming soon)

**Non-routable.** These are decided keyless floor builds that are **not yet in the registry**, so start-here must never offer them as a buildable-now win and the binding check treats this whole section as off the floor. The curation lives here so the vision is preserved and ready to promote into the live menu the moment each app ships (build order in [`floor-roster.md`](../docs/architecture/floor-roster.md) "Derived build set"). When an app here lands in `kernel/registry.json` with `requires_credential: none`, move its row up into the live section above.

| Project | One-line operator pitch | Builds on | Tier |
|---|---|---|---|
| **Price this job with confidence** | Tell me the work, your costs and hours and I'll build a defensible price with margin shown, so every quote comes off a number, not a gut feel. | `price-my-work` `[floor-new]` | first_build |
| **Build your pricing brain** | Tell me how you price your common jobs and I'll build a sheet you can quote off in seconds, consistent every time. | `price-my-work` `[floor-new]` | first_build |
| **Write the proposal that wins the job** | Give me the scope and price and I'll write a sharp, on-brand proposal/SOW in your voice, ready to send. | `write-a-proposal` `[floor-new]` | first_build |
| **Size up a competitor before you bid** | Point me at a rival's site and I'll read it like a sharp operator: how they position, what they charge, where the gaps are. | `research-a-competitor` `[floor-new]` | first_build |
| **Research a prospect/partner before the call** | Tell me who you're meeting and I'll hand you a one-page brief plus three sharp questions that make you the most prepared person in the room. | `research-before-call` `[floor-new]` | instant_win |
| **A fortnight of content, planned and written** | I'll turn your brand into a two-week plan (what to post, when, where) then write the captions and make the first graphics. | `plan-my-content` `[floor-new]`, `write-post-copy` `[floor-new]` | deeper |
| **A short branded promo video** | A 15-30s branded video (your work, your colours, text on screen), the kind of thing that stops the scroll. No film crew. | `make-brand-video` `[floor-new]` | deeper |
| **The captions and body copy for your posts** | Give me the idea and I'll write the on-brand caption and body in your voice, positive and outcome-led every time. | `write-post-copy` `[floor-new]` | first_build |
| **Stress-test your next big decision** | A hire, a price rise, dropping a service? Tell me the decision and I'll grill you on it, poking the holes before you commit, not after. | `grill-me-on-this-decision` `[floor-new]` | first_build |
| **A job ad + screening questions in your voice** | I'll write the job ad and screening questions that sound like you, so the right people apply and the wrong ones screen themselves out. | `write-a-job-ad` `[floor-new]` | deeper |
| **The policies & FAQs your business runs on** | Tell me how you handle deposits, cancellations, privacy and I'll write clean, on-brand policies and FAQ answers for your site, emails or staff. | `write-a-policy` `[floor-new]` | deeper |
| **A capabilities / explainer one-pager** | I'll write the one clean on-brand answer to "can you do this?" (services, lead times, how it works) ready to send every time. | `write-a-policy` `[floor-new]`, `write-post-copy` `[floor-new]` | deeper |

*Every copy-producing Planned app enforces the positive-only language rule when built (global CLAUDE.md + floor-completion-plan DoD).*

---

## 4. The 3-options selection logic

**Inputs:** `vertical`, `named_relief` (the RELIEF field — what eats their week), `connected` (CRM yes/no), `already_built` (project names done this session).

**The algorithm:**

**Complexity/cost gate (applies to EVERY option — custom or library):** only offer a project that's **finishable in one focused sitting** (one clear artifact), **bounded** (one photo / one competitor / this week's post — never "all your X"), and **token-frugal** (won't flood the context window). Heavy / sprawling / open-ended builds are excluded cold; if a big idea is the obvious fit, offer a **bounded first slice**, not the epic. Never let a first session burn the owner's context window or kick off a multi-hour build.

0. **Custom-first (the default when there's an obvious fit).** If the owner's own situation points to an obvious, high-fit bespoke project, that is the DEFAULT and leads — even if it's not in this library. This library is the **safety net**: it guarantees there's always at least one option serving a real problem they named, for when no obvious custom project exists. (TrustPager is reactive-only: slot-3 "auto-later once connected" options describe the OUTCOME; never name TrustPager unless the owner asks what else the BOS can do or about CRMs.)
1. **Filter out anything they've already built.** Never re-offer `already_built`.
2. **Gate by trust + connection.** Cold (nothing connected, first pivot): draw **only from the keyless `first_build` pool** (`instant_win` is the pre-pivot taste, not a menu item; `deeper` and any `needs_crm`/`better_with_crm` project is held back). As trust accrues or a CRM connects, open up `deeper` and `better_with_crm`.
3. **Anchor on the named relief.** The first of the 3 must map to `named_relief`, and cold it must be a **live keyless** win (Planned projects below are named for vision only — never lead with one until it ships). Relief → project lead:
   - quoting → *photo-to-quote* (live) · *Price this job* *(Planned)*
   - finding leads → *Size up a competitor* / *Research a prospect* *(both Planned)* — cold, fall back to *Your brand, written down* (live)
   - chasing invoices → (cold) *Your brand, written down* or *Chase stale quotes* (better_with_crm); (connected) *Spot uninvoiced jobs* / *follow-up radar*
   - looking professional → *Your brand, written down* (live) · *A proposal that wins* *(Planned)*
   - staying on top of customers → *Throw me any file* (live) / *recovery text* (better_with_crm) / *call-to-notes* (better_with_crm)
   - content/marketing → *A branded post today* (live) · *fortnight of content* *(Planned)*
   - thinking/deciding → *A sharp reusable prompt* (live) · *Stress-test your decision* *(Planned)*
4. **Pick the vertical standout if one matches the relief**, else fall to the universal core.
5. **Shape the 3 as quick-win + meatier + aspirational:**
   - **Slot 1 — quick win** that nails the named relief (the dopamine hit; a short, visibly-finished artifact).
   - **Slot 2 — meatier first_build** that deepens the profile (brand, pricing brain, proposal — captures rates/voice/positioning as a side effect).
   - **Slot 3 — aspirational** that hints at the operator they're becoming (competitor research, content plan, decision grilling) — and, if `connected=false` and trust is rising, this slot is the gentle place to seed a `better_with_crm` project ("…and it can send itself once your workspace is connected").
6. **Keep slot 1 + slot 2 keyless** at the cold open. Only let slot 3 carry a CRM-tagged option, and only phrase it as a "now, then auto-later" build.
7. **Each option is phrased outcome-first**, in plain operator language, as "here's something we could build for you" — never jargon, never the app name.

**The exact framing line (the pivot):**

> "Based on my current understanding of your operation, here are 3 things we could build to start your transition into an operator right now."

Then each option as a one-line outcome the owner recognises, e.g. for a trades owner who named *quoting*:

> 1. **Turn a photo of a job into a ready-to-send quote** — send me one now and watch.
> 2. **Get your brand written down** so every quote, post and proposal sounds unmistakably like you.
> 3. **Make you look like the most professional trade in your area** — your brand on every quote and post.

*Worked example — broker, relief = "staying on top of paperwork", nothing connected:* slot 1 *Fact-find pack read in seconds* (quick win, keyless, hits relief), slot 2 *Your brand & lender-file voice* (meatier, keyless, deepens profile), slot 3 *The outstanding-docs chaser* ("…I track asked-vs-arrived live once your workspace is connected" — aspirational + seeds the connect).

---

## 5. Earned-progression notes

**Tier map (which is what):**

- **instant_win** (the <2-min pre-pivot taste — *not* offered in the 3-menu): *photo-to-quote* on one photo, one *branded post*, *throw-me-any-file*, *call-to-notes* (better_with_crm). These trigger the pivot; the menu is drawn from the tiers below.
- **first_build** (the cold 3-option pool, keyless, visibly operator-grade, deepens profile as a side effect): the LIVE cold pool is *Your brand written down*, *photo-to-quote*, *fact-find pack*, *throw-me-any-file*, *a sharp reusable prompt*. The Planned first_builds (*Price this job*, *Write the proposal*, *Size up a competitor*, *Stress-test a decision*) join this pool as they ship (see [Planned (coming soon)](#planned-coming-soon)); never lead with them cold until then.
- **deeper** (offered once trust is high or a connection exists): *onboard a team member* (live keyless), *customer-list import* (better_with_crm), plus the Planned-or-connected set — *fortnight of content*, *branded promo video*, *job ad + screening*, *policies/knowledge base*, *spreadsheet*, *uninvoiced-jobs*, *renewal/reorder radar*, *nurture sequences*.

**The CRM/TrustPager on-ramp (the `better_with_crm` set — the high-trust conversation seeders).** These are valuable cold but their full payoff lands on connect, so they are the natural, non-cold bridge to "connect your workspace":

- **Get your customer list into one clean place** (`import-from-anywhere`) — the single most natural on-ramp; clean list cold, becomes the live CRM seed on connect.
- **A recovery text for missed calls** / **Chase stale quotes** / **A renewal/reorder sequence** (`missed-call-recovery`, `design-nurture-sequence`, `wire-nurture-sequence`) — "write it now, it sends itself once connected" (auto-fire).
- **The outstanding-docs chaser** (`outstanding-documents`) — works off your checklist cold; tracks asked-vs-arrived live once connected.
- **Turn a call into notes** (`transcript-summary`) — standalone summary cold; logs straight onto the client's file as an activity on connect.
- **Policies / knowledge base** (`build-knowledge-base-from-docs`) — clean docs cold; powers the AI assistant and voice agent on connect.

**`needs_crm` (held for the deeper tier only, never cold):** *Spot uninvoiced jobs* (`outstanding-invoices` — needs receivables + activity dates), *stalled-proposal radar* and *renewal radar* (`follow-up-radar`, `sweep-my-day`, `weekly-review` — need live `last_activity_at`). These are reserved as the "look what your connected workspace now watches for you" reward once trust is earned.

**Profile-deepening as a side effect (why building beats interrogating):** *pricing/proposal* → captures rates, cost structure, job types; *brand written down* → writes `brand.json` (positioning, voice) that reskins all future creative; *content plan/video* → captures product range, ideal-work focus; *competitor research* → captures the competitive set; *intake/RFQ form* → captures what a "complete brief" means for this owner. Each pick the owner makes deepens the operator profile organically — the build IS the discovery.

---

**Files this draws from (all under `C:\Users\USER\Desktop\Final Piece Docs\Business_Operating_System\`):** `kernel\registry.json` (the 58-skill capability catalogue + credential/data_path per skill), `docs\architecture\floor-completion-plan.md` (the decided keyless floor builds, all `[floor-new]` / Planned: `price-my-work`, `write-a-proposal`, `research-a-competitor`, `research-before-call`, `plan-my-content`, `write-post-copy`, `grill-me-on-this-decision`, `write-a-job-ad`, `write-a-policy`, `make-brand-video`; plus ruling #2 on `transcript-summary`), `docs\architecture\skill-extraction-audit.md` (the floor/extractable/trustpager_native buckets), `knowledge\industry-notes.md` (per-vertical gotchas driving the relief targeting).
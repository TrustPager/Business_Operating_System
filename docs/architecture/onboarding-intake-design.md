I have full grounding. All five lenses confirm the same load-bearing facts and the same critical build gap. Writing the consolidated design now.

# BOS Onboarding Intake — The Buildable Design (P3 spec)

This is the single reconciled design for the start-here onboarding skill. It honors every locked decision and resolves the five lenses into one flow. Where lenses converged (they overwhelmingly did), I collapsed; where they diverged, I ruled. Ruling decisions are marked **[RULED]**.

**Three rulings that shape everything below:**

1. **[RULED] The cold-open auto-speaks only on a TRUE cold start.** P3 checks "have I met this business yet?" before volunteering the intro, so returning owners are never re-onboarded. (Lens 3 risk #7.)
2. **[RULED] The instant win's hard dependency is the one real code change P3 requires.** `build-brand-strategy` today requires a TrustPager-coupled `customer-voice-synthesis.md` (via `build-customer-voice`). All four lenses flagged this independently. P3 ships a **brain-dump + Firecrawl evidence mode** for `build-brand-strategy` (a "first-brand-brief" entry path), or the keyless instant win is a lie on day one. This is the highest-priority build item.
3. **[RULED] Hard-stop at the SPINE; defer everything else.** The failure mode every lens named is filling the whole profile before delivering value. P3 stops asking the moment the spine is filled and the win can fire — max ~3 follow-ups in sitting one.

---

## 1. The cold-open

Claude speaks **first**, unprompted, on a true cold start (empty/starter `CLAUDE.md`). First-person, as a sharp 2IC on day one. No form, no menu, no "type /onboard". The opener does four jobs: names the relationship, sets a one-question expectation, reframes data-entry as "just talk", and plants the website/name hook (the single highest-leverage token — one Firecrawl scrape backfills 6-8 fields).

**Exact opening lines:**

> Right — I'm your new AI assistant. Think of me as a capable new employee who started today: I already know how to run all the tools here in your new Business Operating System (BOS), I just don't know YOUR business yet. The faster I get how you actually work, the more useful I am from here.
>
> Quickest way to get me up to speed — if you've got a website, or even just your business name, drop it in and I'll go do my own homework, so you don't have to spell it all out.
>
> Then talk me through it like you're briefing someone you've just hired — in a minute or so: **what you do, who it's for, and what eats most of your week.** Don't tidy it up; rambling is better than a neat paragraph, and I'll sort it into shape. Type it, paste something you've already written, or just hit the mic and talk — whatever's easiest.
>
> So — what's the business? (And the website, if you've got one.)

**Why this exact wording (load-bearing choices):**
- **"AI assistant / capable new employee who started today"** [FOUNDER-RULED] — owners want to feel powerful but NOT out of control. "Assistant / employee that started today" keeps THEM in charge; "business partner" / "2IC" is too presumptuous and not universal. Trust earns the "partner" framing later; the first conversation must feel like a capable hire awaiting direction.
- **The website/name "I'll do my own homework" hook leads** [FOUNDER-RULED, moved up] — show-don't-tell: Claude researches first (keyless Firecrawl) so the owner sees value before typing much. Firecrawl enrichment + the owner's dump together = a strong starting point.
- "Briefing someone you've just hired" unlocks fluent, high-signal speech where "describe your ICP" produces freeze.
- The **what / who / time-sink triple** grabs the three spine fields in one breath.
- "Don't tidy it up, rambling is better" pre-forgives messiness and kills terseness.
- **"what eats most of your week" — APPROVED [FOUNDER-RULED]:** the positive-only rule governs **customer-facing content**, not discovery. Naming the pain here is *diagnosis to aim the help*, not building value around pain. (See memory `pain-language-ok-in-discovery`.) The win's customer-facing OUTPUT still stays strictly positive/outcome-led.

**Thin-dump recovery (owner gives one line, e.g. "I'm a sparky in Geelong"):**
Do NOT repeat the big open question — that reads as "you failed, try again." Bank what landed, make a visible inference, ask ONE concrete narrowing question that proves Claude listened:

> Got it — solo sparky, Geelong. Most electricians I set up are juggling call-outs, quotes, and chasing invoices. Which of those three eats your week the most?

If even that stalls, offer a tap-not-type fallback so no one stares at a blank prompt:

> No dramas — pick the closest and we'll start there: trades, broking, allied health, consulting, or something else?

**Binge-vs-sip offer — [RULED] offered AFTER the first win, never before** (offered cold it signals "this is going to be long"). One sentence, both options equal, with the resumability promise that makes SIP safe:

> That's enough for me to be useful today. Every time we talk I get a bit sharper about your business — want to keep going now and really dial it in, or pick it up next time? Either way I'll remember exactly where we got to.

---

## 2. The elicitation strategy

**The flow: DUMP → INFER (silent) → ENRICH (silent, keyless) → WIN → ≤3 SURGICAL FOLLOW-UPS → opt-in DEEPEN.** This is the re-skinned grill-me: relentless branch-resolution, but Claude resolves most branches *silently by inference/research* instead of asking, so the owner never feels grilled.

**Beat 1 — Catch & parse silently.** Whatever lands (one line or three paragraphs; typed, pasted, voice-transcribed), Claude runs ONE silent pass tagging every signal as **SAID / INFERABLE / MUST-ASK** against the schema (§3). It never reads the dump back as a checklist — that turns talk into a form. It absorbs.

**Beat 2 — Enrich before asking (the trust-buying move).** If a business name or URL was given, Claude immediately runs **keyless Firecrawl** (`firecrawl-scrape` on the site + `firecrawl-search` on the business name) to pull services, suburb/service-area, hours, team, reviews, tagline, brand tone. This is the "how did it KNOW that" beat. **[RULED] cap enrichment effort** — if Firecrawl is slow or returns nothing, fall back silently to the dump-only win; never let scraping stall the turn. Self-site research is silent; competitor research is owner-invited only (avoids feeling surveillant).

**Beat 3 — Reflect + win, no questions yet.** Claude plays back a crisp one-paragraph "here's the business as I now understand it," names the industry it inferred (as a guess to correct), attributes any research out loud ("had a look at your site — looks like you do X, Y, Z across the northside, that right?"), THEN fires the instant win (§5).

**Beat 4 — Grill-lite: ≤3 surgical follow-ups, prioritised, batched 1-2 at a time.** Only AFTER the win, and only for fields that are **both high-value AND un-inferable (Class C)**. Each is justified by the win just delivered and ships with an escape:

> To make this positioning sharper, one quick thing — what's the job you wish more of your customers asked for? *(Or skip it; I'll pick it up as we work.)*

Claude **states a smart default and asks to confirm/correct**, never open-ended cold: *"Based on your trade I'd guess most jobs sit $400–1,500 — roughly right?"* The owner edits a guess (low effort, in command) instead of authoring an answer.

**The three-class rule (the infer-don't-ask engine):**

| Class | Definition | Behaviour |
|---|---|---|
| **A — INFERABLE** | Derivable from industry + location alone | Never ask. Write as a labelled draft to correct. |
| **B — RESEARCHABLE** | Findable via keyless Firecrawl from a name/URL | Auto-enrich silently, confirm at a glance. |
| **C — MUST-ASK** | Unique & unguessable | Ask only these, priority order, stop when spine is full. |

**Infer-don't-ask table (Class A + B — these are NEVER cold questions):**

| Signal | Source | How presented |
|---|---|---|
| Industry/vertical | Match dump language + location to `knowledge/industry-notes.md` (6 verticals) | Confirm as a one-line guess, never assert |
| Pipeline stages | The matched vertical's canonical flow (e.g. trades: New enquiry → Site visit/quote → Quote sent → Followed up → Won/scheduled → In progress → Completed → Invoiced) | Draft to correct ("I've assumed this flow — yours run different?") |
| Typical products + price *ranges* | Vertical defaults + scraped services page | Confirm, don't quiz. (Real prices are Class C.) |
| Lead sources | Vertical default-ticks (trades=phone+referral; broker=referral+partners) | Pre-ticked list for a quick yes/no |
| Region pack (AUD, Australia/Sydney, +61, DD/MM/YYYY, GST) | Country, default AU per D7 | Assume AU; confirm once if signals say otherwise. **[RULED] confirm, don't hard-assume for non-AU owners** (ICP is "Australia-leaning," not Australia-only). |
| Industry gotchas/compliance | Vertical (broker: never quote a rate, 7yr records; allied health: no clinical advice over SMS; insurance: never imply unbound cover; trades: speed-to-lead, quotes stale ~2wks) | Folded in silently, surfaced as "I'll watch out for…", never a question |
| Comms register + voice | Vertical comms-style + **mirrored from the owner's own dump phrasing** | Lift their exact words ("on the tools", "one-man band"); light confirm |
| Brand basics (name, services, area, hours, tagline, team) | Keyless Firecrawl scrape | Confirmed at a glance, never asked |
| Competitor set / positioning angle | Keyless Firecrawl search of local market | Owner-invited only |

**The highest-value follow-ups (Class C only, ask in this order, stop early):**
1. **Real price points / rough job value** — drives every quote/proposal/pricing win.
2. **The differentiator** — "what makes people pick you" — unguessable, the seed for the brand brief.
3. **The one job they'd hand off tomorrow** — routes them to their first high-relief app; *asked AFTER the win, deepening phase.*

---

## 3. The business-context profile schema

The artifact is `templates/CLAUDE.md` → written to `./CLAUDE.md`. **Spine first; the profile is usable after the spine alone.** Inferred/researched fields are written as labelled drafts; un-filled fields stay as visible `<<< guesses to confirm later >>>` so the owner sees a "here's what I still don't know" list that seeds the next session. Priority = **decision-relevance × cheapness-to-obtain.**

**TIER 1 — THE SPINE (captured turn one; profile is usable after this alone):**

| # | Field | Maps to `templates/CLAUDE.md` | Unlocks | Class |
|---|---|---|---|---|
| 1 | **Business identity** — name, what they sell (one line), suburb/city + country | `## My business` | The anchor for all keyless enrichment; region pack (D7) | C (name) / B (rest) |
| 2 | **Industry/vertical** — NOT asked; inferred + matched to `industry-notes.md` | (drives gotchas + comms throughout) | The master key — one correct guess pre-fills pipeline, products, gotchas, comms-style | A |
| 3 | **Who they serve + buying trigger** | `## My ideal customer` | Raw material for the instant win | A→C |
| 4 | **What eats the week** (the relief target) | *new high-signal field* (note under "How to talk to me") | Aims the first win at real pain | C |
| 5 | **Voice / how they sound** — captured by MIRRORING the dump, not asked | `## How to talk to me` + `## How to draft customer comms` | On-brand drafts from message one | A (mirror) |

**TIER 2 — WORKFLOW (deepening; mostly inferred-and-confirmed):**

| # | Field | Maps to | Unlocks | Class |
|---|---|---|---|---|
| 6 | Products/services + rough price & cycle | `## My products / services` | quote-from-photo, price-my-work, proposals | B (names) / C (real prices) |
| 7 | Pipeline stages | `## My pipeline` | "where's [client] at?"; becomes real on TrustPager connect | A |
| 8 | How leads come in | `## How my leads come in` | Lead-source-aware follow-ups | A |
| 9 | Team size (just me / N / +contractors) | `## My business` | Whether team apps surface | C (one line) |

**TIER 3 — VOICE & GUARDRAILS (deepening, SIP):** comms do/don't rules with vertical compliance gotchas pre-loaded as confirmable defaults; ideal-customer detail; the differentiator.

**TIER 4 — DEEPENERS (SIP, never at cold start):** lost/won reasons, referral partners, seasonal/busy-season rhythm, named competitors, the one job to hand off. → "The profile grows over time."

**How it grows over sessions:** every SIP/BINGE session and every real piece of work writes back to the same `./CLAUDE.md`. Growth is visible as filled fields vs remaining `<<< guesses >>>`. Empty fields aren't chased — they fill as work happens ("I'll learn your prices the first time we quote a job"). **[RULED]** the "About TrustPager" fixed block stays intact; TrustPager is mentioned once, gently, opt-in, at the very END (D3) — never required, never foregrounded in the cold path.

---

## 4. The comfort/trust design

Four fears to neutralise — **exposure, judgment, effort, wasted-effort** — each with a concrete move and phrasing:

| Move | Kills | Exact phrasing / mechanic |
|---|---|---|
| **Data-residency one-liner** (within the opener's frame) | Exposure | "Everything you tell me stays in a notes file in this folder on your machine — not shared, not training anything, just my memory of your business." **[RULED] must be literally true** — if later flows sync to cloud, the cold-start promise still holds for the local profile. |
| **Messy-is-perfect** | Judgment | "Don't tidy it up; rambling is better." A chaotic dump is treated as a gift. |
| **Lead as a person, not a tool** | Guardedness | "A sharp 2IC who started today" — cuts the guardedness of feeding a database. |
| **Do-my-homework reciprocity** | Effort + wasted-effort | "Drop your site and I'll read it so you don't have to type it" — then actually do it; by turn two Claude knows things they never typed. |
| **Mirror-don't-interrogate** | Wasted-effort | Play back the understood picture BEFORE asking anything, in their own words. |
| **Why-I'm-asking tag on every question** | Interrogation feel | "Only because it changes how I'd chase a quote for you." Never two questions in a row without giving something back. |
| **Smart-default-then-confirm** | Effort | Owner edits a guess, never authors cold. |
| **Show-my-notes transparency** | Exposure | "Here's what I've jotted about you — have a look, tell me what's wrong." The profile is reframed as *my notes you can correct*, not a config file. |
| **Honest-guess posture** | Trust | **[RULED hard rule, from `industry-notes.md` + `learn-my-business`]** every inferred field is LABELLED as a guess to correct, NEVER written as a workspace fact. A confident wrong fact destroys trust faster than asking. |
| **Always-an-exit** | Effort/trap | Every follow-up ships "…or skip it, I'll pick it up as we work." Binge-or-sip with "I'll remember where we got to." |
| **No-jargon contract (D3)** | Out-of-depth | Never kernel/driver/app/MCP/manifest/skill/profile. Say "I", "getting to know your business", "my notes", "switch on", "homework". Lint against a banned-words list. |
| **Attribute the magic** | Uncanny-valley | "I read that off your site" — inference has a visible, benign source, never spooky omniscience. |
| **Confirm scraped identity** | Mis-attribution | "I found [Business] in [suburb] doing [X] — that you?" before trusting scrape data. |

---

## 4b. Design principle: identity & ownership framing (thread it everywhere) [FOUNDER-RULED]

Make the owner *feel* this is THEIR system — powerful, in command, in possession — and let that feeling live wherever it lands naturally, **without forcing it or turning it into a pitch.** A light touch: one identity beat per moment, earned, never repeated to death.
- **It's "your" system:** "your new Business Operating System (BOS)", "your command centre", "we / us" running *your* business. "Business Operating System / BOS" is identity/name — fine to surface; internal taxonomy (kernel/driver/app/MCP/manifest) still NEVER appears (D3).
- **Touchpoints where it lands naturally:** the opener (*your* new BOS) · the win reveal (*"look what your system just pulled together"*) · the deepening offer (*"the more you teach it, the sharper it gets for you"*) · the profile reframed as *"your notes"* · the close. P3 should hit ~one of these per session, not all at once.
- **The goal:** the owner quietly thinking *"this is mine, and it's powerful"* — never being told so.

---

## 5. The instant win

**[RULED] Default win = `build-brand-strategy`, re-pointed to run from the brain-dump (+ keyless Firecrawl enrichment), NOT from a TrustPager transcript synthesis.** Four of five lenses independently chose this and independently flagged the same blocker. In under 2 minutes it turns the messy dump into: a one-paragraph positioning statement, a one-sentence promise/tagline in THEIR words, the "only-we" claim, and 3 content angles — reflected back using the exact phrases they used.

**Why it's the most universally impressive <2-min win for the ICP:**
- Every 2-10 person service business (trades, broker, allied health, consultant) has positioning pain and instantly recognises good-vs-bad positioning *about their own business*.
- It needs **zero accounts, zero files** — only their words (plus optional silent enrichment).
- The reaction — "that's exactly us / better than what's on my website" — is universal across all six verticals.
- It visibly USES something they just said, proving the sharing paid off.

**Routing (pick by what the dump handed you, default to the brand brief):**

| Dump signal | Win | Driver |
|---|---|---|
| Positioning / who-they-are (default) | `build-brand-strategy` → first-pass brand brief | reasoning-only (+ Firecrawl) |
| Named a rival / market-curious | `research-a-competitor` → "here's what your nearest competitor leads with and a gap you could own" | keyless Firecrawl |
| Trades / dropped a job photo | `quote-from-photo` (with `price-my-work` as the driver-less pricing fallback) | reasoning-only |
| A live decision ("should I hire?") | `grill-me-on-this-decision` (gentle reskin) | reasoning-only |
| Pasted a doc | `extract-document` / `transcript-summary` (keyless paste path) → summary + action items | MarkItDown (local) |

**How it's generated FROM the profile:** the win reads the half-filled profile, so its quality visibly tracks what was shared — which makes the deepening loop self-justifying. The profile is written/updated to `./CLAUDE.md` silently as a side effect, never the headline.

**[RULED build dependencies]:**
1. **`build-brand-strategy` gets a native floor evidence path — TrustPager NEVER enters the cold-start.** What it needs from TrustPager today is only *customer voice* (verbatim evidence of how customers actually talk), which `build-customer-voice` sources by mining TP call transcripts. In the floor we source that voice **keylessly**: (a) the owner's brain-dump, (b) **keyless Firecrawl** on the owner's own reviews / testimonials / website + how the market talks about the problem, and (c) any testimonials / reviews / emails the owner pastes (local files, no account). TP transcript-mining becomes an optional *connected-tier deepener* (richer, verbatim voice), never a cold-start dependency. **Building this native floor evidence mode is the one prerequisite the win path requires.**
2. The win's customer-facing output (taglines, positioning) MUST enforce the **positive-only language rule** (outcome-led, never "stop being the bottleneck").
3. The win must be REAL — if the dump is too thin to produce something sharp, route to thin-dump recovery FIRST rather than ship a weak artifact (a hollow win confirms the wasted-effort fear).

---

## 6. The deepening loop

**Resume:** on session start P3 reads `./CLAUDE.md`. If it's a filled BOS profile (not the starter template), Claude does NOT re-onboard — it leads with status and the resume point. The profile carries a machine-readable marker so the "I'll remember where we got to" promise holds (see §7). The visible `<<< guesses to confirm >>>` ARE the resume anchors — they mark exactly where to pick up.

**Scope one more area:** each returning session offers ONE next area, framed by relief, never a checklist:

> Want to spend ten minutes dialling in your pricing so I can draft quotes that sound like you? Or leave it and pick up something else?

BINGE (full deep-dive in one sitting) and SIP (a bit each session) both write to the same profile — progress is never lost.

**Visibly improve output (the come-back reason):** re-running the win after a deepening session produces a measurably sharper artifact ("the more I know, the sharper this gets"). Because every downstream floor app — proposals, content plans, nurture — reads the same growing profile, deepening compounds across the whole product, not just the brand doc. **That visible improvement IS the reason to return**; if the profile silently reset, the loop's entire reward collapses.

---

## 7. Build notes for P3 (the start-here skill)

**Skill identity:** new skill, e.g. `skills/start-here/SKILL.md`. Frontmatter: `function_slot: strategy`, `requires_driver: none`, `requires_credential: none`, `data_path: reasoning_only` (Firecrawl is keyless). It does NOT inherit `learn-my-business`'s `requires_driver: trustpager` — that skill becomes the *connected-tier deepener*, not the cold front door. **[RULED]** `learn-my-business` is rebuilt as the workspace-read deepening upgrade offered after connection; `start-here` is the new keyless front end.

**The flow as implementable steps:**

1. **Cold-start gate.** Read `./CLAUDE.md`. If absent OR still the starter template (contains `<<< your name >>>`) → cold start, auto-speak the §1 opener. If a filled BOS profile → skip onboarding, resume (§6). *(This prevents re-firing every session — Lens 3 risk #7.)*
2. **Catch the dump.** Accept typed / pasted / voice-transcribed input. Voice and paste are offered, never required; typing one line is a complete valid path. If transcription is absent in the client, degrade silently to type — never promise a capability the surface can't honour.
3. **Silent parse.** Tag every field SAID/INFERABLE/MUST-ASK against the §3 schema.
4. **Keyless enrich (if name/URL present).** Call Firecrawl: `firecrawl-scrape` on the URL + `firecrawl-search` on the business name. Cap effort/timeout; on empty/garbage/slow, fall back to dump-only and continue (graceful "couldn't find you online, no worries"). Confirm scraped identity before trusting it.
5. **Infer.** Match dump+research to `knowledge/industry-notes.md`; load that vertical's pipeline + products + lead sources + gotchas + comms-style as **labelled drafts**.
6. **Reflect + fire the win** (§5) in the same turn as the dump. Route by dump signal; default to `build-brand-strategy` via the new brain-dump evidence mode.
7. **Grill-lite.** ≤3 Class-C follow-ups, one or two at a time, each justified by the win, each with an escape. Hard-stop when the spine is filled.
8. **Write the profile.** Write/merge `./CLAUDE.md`: spine filled from confirmed data, inferred fields labelled, gaps as `<<< guesses to confirm later >>>`. **Never overwrite a hand-tuned existing file without showing the diff** (inherit `learn-my-business` Step 3 rule). Keep the "About TrustPager" block intact.
9. **Offer binge-or-sip** (§1 phrasing), AFTER the win.
10. **Close.** Mention TrustPager connection once, gently, opt-in (D3).

**Profile read/write:**
- **Read:** `./CLAUDE.md` in the project root at session start (the cold-start gate).
- **Write:** same path, via the structure of `templates/CLAUDE.md`. Industry gotchas folded in as patterns-to-confirm (per `industry-notes.md` hard rule), real data always wins over inference.

**Keyless research call:** keyless hosted Firecrawl MCP (already active in `.mcp.json`, no key for scrape/search per D6). Use the `firecrawl-scrape` and `firecrawl-search` skills. Self-site = silent; competitor = owner-invited.

**Instant-win handoff:** P3 invokes the chosen floor skill (`build-brand-strategy` brain-dump mode / `research-a-competitor` / `quote-from-photo` / `grill-me-on-this-decision` / `extract-document`), passing the half-filled profile as input. **Build prerequisite:** the `build-brand-strategy` brain-dump evidence path must exist first (§5 ruling #2 / §2 RULED).

**Resumability state (concrete mechanism):** add a small machine-readable marker block at the top of `./CLAUDE.md`, e.g.:

```
<!-- bos-onboarding: spine=complete; tier2=partial; last_touched=2026-06-26;
     pending=[real_prices, differentiator, team_size]; win_delivered=build-brand-strategy -->
```

The cold-start gate reads this; `pending=[…]` drives the "scope one more area" offer; `spine=complete` short-circuits re-onboarding. The visible `<<< guesses >>>` are the human-facing mirror of `pending`. Without this block the "I'll remember where we got to" promise breaks on session 2 — so it is **mandatory, not optional**.

**Risks P3 must defensively handle (deduped from all lenses):** Firecrawl empty/slow → dump-only fallback; mis-attributed business → confirm-before-trust; thin dump → recovery prompt, not a weak win; inferred-as-fact → always label as guess; voice unavailable → degrade to type; over-asking → hard-stop at spine; non-AU owner → confirm locale, don't hard-assume; privacy verticals (allied health) → never echo clinical detail into research queries or the brief.

---

**Files this design builds against (all under `C:\Users\USER\Desktop\Final Piece Docs\Business_Operating_System\`):** `templates/CLAUDE.md` (profile shape + field anchors), `docs/architecture/founder-decisions.md` (D3 plain-language, D6 floor/Firecrawl, D7 region pack, D8 MCP-first/keyless), `docs/architecture/floor-completion-plan.md` (the keyless floor apps the win draws from; confirms `build-brand-strategy` TrustPager coupling is the named gap), `knowledge/industry-notes.md` (the inference fuel + the patterns-to-confirm hard rule), `skills/learn-my-business/SKILL.md` (rebuilt as the connected-tier deepener; its Step-3 no-clobber rule and hard rules carry into P3).

**The one build prerequisite P3 cannot ship without:** a keyless brain-dump + Firecrawl evidence mode for `build-brand-strategy` (the "first-brand-brief" path). Until it exists, the locked "works with NO documents" instant-win is not literally true.
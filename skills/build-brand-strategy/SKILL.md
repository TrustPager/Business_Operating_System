---
name: Build Brand Strategy
description: Turn how a business owner talks about their work into a sharp brand brief — positioning, a promise/tagline, the only-we claim, and content angles — in their own words. Works keylessly day one from the owner's words plus free web research; deepens into the full five-doc strategy when call-transcript evidence is available. Every claim anchored in real evidence — no invented customer quotes.
triggers:
  - build brand strategy
  - write our positioning
  - first brand brief
  - help me describe my business
  - what's our positioning
  - build the voice doc
  - define our ICP
  - author value props
  - content pillars from customer voice
  - turn customer voice into strategy
function_slot: strategy
requires_driver: none
requires_credential: none
data_path: local
status: active
produces_customer_facing_copy: true
---

# Build Brand Strategy

You turn how an owner talks about their business into brand strategy that
sounds like them — never invented sales copy. Every claim traces back to
real evidence: something the owner said, something the market said, or a
verbatim customer quote. If a claim has no evidence behind it, it doesn't
ship.

The source of truth for shapes + anti-patterns is
[`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md)
— read its "Layer 3 — The brand strategy docs" section before authoring the
full five-doc set.

## Pick the mode — start with what you have

There are two ways to run this, and the right one depends on what evidence
exists right now:

| You have… | Mode | What you produce |
|---|---|---|
| Just the owner's words (and maybe a website) — **the default for a brand-new owner** | **First-brand-brief** (keyless) | A one-page brand brief: positioning paragraph, one-sentence promise/tagline, the only-we claim, 3 content angles |
| A `customer-voice-synthesis.md` built from real call transcripts | **Full strategy** (the deeper mode) | The five canonical docs (positioning, ICP, voice, value-props, content-pillars), every claim quote-anchored |

**Default to the first-brand-brief whenever there is no
`customer-voice-synthesis.md`.** It needs no accounts, no files, and no
prior setup — only the owner's words plus free web research. Do NOT stop
and demand a synthesis; that's the cold-start failure the brief exists to
avoid. The full five-doc strategy is the *upgrade* you offer once richer
evidence exists — never the price of entry.

---

# Mode A — First-brand-brief (keyless, the day-one default)

This is the instant win for an owner who has just shown up: no CRM, no
transcripts, no files — just told you (or typed/pasted) what they do. In
a couple of minutes you reflect their business back to them sharper than
their current website does, in their own words.

## A1 — Gather the evidence (keylessly, three sources)

You are sourcing **customer voice** — real evidence of how people talk
about the problem this business solves and the outcome they want. With no
transcripts to mine, pull it from these three keyless sources, in order of
what's available:

1. **The owner's brain-dump / what they tell you.** Whatever they said
   about what they do, who it's for, and what they're known for. This is
   primary evidence — capture their exact phrasing.
2. **Keyless web research** — use the `firecrawl-scrape` and
   `firecrawl-search` skills (no API key needed for scrape/search):
   - `firecrawl-scrape` the owner's **own website** if they gave one —
     pull their services, the words they already use, any testimonials or
     reviews quoted on the site.
   - `firecrawl-search` the **business name** to find their reviews,
     testimonials, and how the market describes the problem they solve
     (directory listings, review sites, social mentions).
   - Cap the effort: if research is slow, blocked, or comes back empty,
     fall back to the brain-dump alone and say so plainly ("couldn't find
     much about you online, so this is built from what you told me — we
     can sharpen it as we go"). Never let web research stall the win.
3. **Anything the owner pastes** — testimonials, reviews, a few customer
   emails, an old "about us" blurb. Treat pasted text as local evidence;
   quote from it directly.

**Confirm before trusting research.** If a scrape/search turns up a
business, check it's actually theirs before leaning on it ("found
[Business] in [suburb] doing [X] — that you?"). A confident wrong fact
costs more trust than a missing one.

**Market-gate pre-check (business-method.md §7.0):** if the gathered
evidence shows a hard fail on real pain or purchasing power for the
avatar the owner described, flag it as a finding before writing any
positioning — most offer problems are avatar problems.

## A1.5 — Walk the positioning ladder (internally — this is your thinking order, not five extra questions)

Before writing a word of the brief, walk the positioning ladder
(business-method.md §14) in strict order. Answer each rung from the
brain-dump plus the research you already gathered — not from new owner
interviews:

1. **List the REAL alternatives** — what customers would actually do
   instead, including "do nothing" and "the brother-in-law". Exclude
   phantom competitors that never appear in real deals.
2. **Isolate provable attributes** — capabilities or facts those
   alternatives can't truthfully claim.
3. **"So what?" twice per attribute** until each lands on a customer
   value; cluster into themes.
4. **Find who cares most** — the segment for whom those themes matter
   disproportionately. This DERIVES the niche; it isn't picked by taste.
5. **Name the existing category** — for a local shape, usually the
   search phrase to own.

The A2 brief parts fall out of the rungs: the positioning paragraph is
rungs 3-5, the only-we claim is rung 2, and the content angles are rung
3's themes.

## A2 — Produce the brief, in the owner's own words

Write a single short brief (Markdown is fine; offer to save it to
`marketing-strategy/<BrandName>/first-brand-brief.md`). Four parts:

1. **Positioning statement (one paragraph).** Who they are, who they
   serve, and the outcome they deliver — phrased the way the owner and
   their market actually talk, not in agency-speak. Anchor it in an
   existing category the market already searches for; category creation
   is a trap at this scale (business-method.md §14).
2. **The promise / tagline (one sentence).** A single forward-looking
   line that captures the result. Reach for the owner's own phrasing.
3. **The only-we claim.** Two or three things simultaneously true of this
   business that competitors can't jointly claim — drawn from what the
   owner said makes them different and what the research showed the market
   values.
4. **Three content angles.** Three topics/hooks this business could lead
   with, each tied to a real piece of evidence (something the owner said
   or something the market said).

**Reflect their phrasing back.** Lift their exact words and use them.
When you've used a phrase straight from them or from a review, that's the
point — it should feel like *"that's exactly how I'd put it."*

**Anchor every claim in the gathered evidence.** Each part of the brief
points to its source — the owner's words, a scraped line, a real review.
**Never invent a customer quote or a testimonial.** If you don't have a
real quote, anchor in the owner's own words instead; don't fabricate one.

## A4 — Thin-evidence guard

If the brain-dump plus research are too thin to produce something genuinely
sharp — you'd be padding or guessing — **don't ship a hollow brief.** Say
so plainly and ask ONE targeted question that would unlock it, then build
from the answer. For example:

> I've got the shape of it, but to make the positioning land I need one
> thing: what's the job you'd most love more of your customers to ask for?

A real, sharp brief built from one good answer beats a vague one built from
nothing. A hollow win confirms the fear that this was a waste of time.

## A5 — Walk the owner through it + offer the deeper mode

Show the brief, point out one or two phrases you lifted straight from them
(so they see it's *theirs*), and flag any open choice you left for them.

Then offer the upgrade — without making it the price of entry:

> This is built from your words and what's out there publicly. When you've
> got real customer conversations recorded, I can mine exactly how your
> customers talk and turn this into a full brand strategy — voice, ICP,
> value props, the lot. No rush; the brief stands on its own today.

---

# Mode B — Full strategy from a customer-voice synthesis (the deeper mode)

This is the richer, connected-tier path. It runs when a
`customer-voice-synthesis.md` exists — normally produced by
`build-customer-voice`, which mines real call/meeting transcripts (a
TrustPager-connected capability). **This mode is the upgrade, never the
default and never required for a new owner.** If no synthesis exists, use
Mode A — do not stop and demand one.

## Prerequisite

A `customer-voice-synthesis.md` file (usually under
`transcripts/<date>/customer-voice-synthesis.md` or in the marketing
strategy folder the operator points to), built by `build-customer-voice`.

If it doesn't exist and the operator wants this deeper mode, they can run
`build-customer-voice` first — but the keyless first-brand-brief (Mode A)
is the right starting point in the meantime. Don't fabricate a strategy
from thin air.

## Step 1 — Read the synthesis end-to-end

Read every section. You'll be quoting from §1 (who's on calls), §2 (pain),
§3 (jobs to be done), §4 (objections), §5 (competing tools), §6 (buying
moments), §7 (vocabulary), §9 (top 10 quotes), §10 (industry patterns)
throughout the strategy docs.

**Market-gate pre-check (business-method.md §7.0):** if the synthesis
shows a hard fail on real pain or purchasing power for the primary
audience, flag it as a finding before writing any positioning — most
offer problems are avatar problems.

## Step 2 — Confirm output location + brand name

Default: write into `marketing-strategy/<BrandName>/`. Ask the operator
for the brand name (folder name) and confirm the output path before
writing.

## Step 3 — Author the five docs

Write them in this order — each one's evidence is reusable in the next.

### 3.1 `positioning.md`

```markdown
# <Brand> — Positioning

> All claims trace back to verbatim quotes in
> [customer-voice-synthesis.md](Reference_Files/customer-voice-synthesis.md).

## Who we are
<one-paragraph identity statement>

## Who we serve (one-liner)
<single sentence naming the buyer in their own language>

## The pain we solve
| Theme | In their words |
|---|---|
| <pain 1> | <verbatim quote with speaker attribution> |
| <pain 2> | ... |

## The promise (what changes for them)
<the end-state, phrased the way customers articulate it>

## The promise in one sentence (working drafts)
<3-5 candidate taglines, each passes the customer-voice test —
"scale", "AI-native", "enterprise-grade" don't appear>

## The only-we claim
<3 things simultaneously true of our brand + not jointly true of any
named competitor in the synthesis — each passes the only-we rubric
(business-method.md §14): named against real alternatives including
do-nothing, provable in one sentence, an identifiable segment cares
disproportionately, stated in the customer's category language>

## Proof
<customer count, industries, founder credibility>

## Geographic + cultural register
<where you operate, the tone that matches>
```

### 3.2 `icp.yaml`

```yaml
audiences:
  primary:
    name: ""
    short_label: ""
    one_liner: ""
    typical_industries: []
    typical_team_size: ""
    typical_revenue: ""
    typical_age_signal: ""
    geography: ""
    tech_skill_self_description: ""
    primary_pain: ""
    primary_job_to_be_done: ""
    competing_tools_escaped:
      enterprise_crm: []
      mid_market: []
      aggregator_captivity: []
      no_tool_at_all: []
    buying_trigger: []
    objections_to_handle:
      - id: ""
        objection: ""
        handle: ""
        evidence_quote: ""
    evidence_quotes:
      - speaker: ""
        business: ""
        quote: ""
        source: ""
  secondary: []
disqualified:
  notes: ""
  patterns:
    - id: ""
      pattern: ""
      evidence_quote: ""
      source: ""
```

Fill from §1, §4, §5, §6, §8, §10 of the synthesis.

### 3.3 `voice.md`

Open with the meta-rule:

> **Founder's voice IS the brand.** Everything in this doc is reference
> material to help write IN that voice when the founder isn't writing
> personally. When this doc and the founder disagree, the founder wins —
> and the doc gets updated to reflect what they actually shipped.
>
> The customer-voice synthesis at
> [customer-voice-synthesis.md](Reference_Files/customer-voice-synthesis.md)
> is INPUT to the brand voice, not the brand voice itself. Customer phrases
> are available to reach for when they fit the moment — they are NOT required
> in every email.

Sections:

- **Sender persona + email voice spec — LOCKED** (sender, sign-off block,
  mode, technical send constants).
- **Tone — 5 adjectives**, each backed by evidence.
- **Signature moves** — forward-looking subjects, warm human openers,
  one core idea per paragraph, customer phrases as seasoning.
- **Vocabulary AVAILABLE** — phrases lifted from §7 of synthesis, in a
  table with attribution.
- **Watch out for (hype register / VC speak / Salesforce-era jargon)** —
  default-avoid registers, framed as defaults not absolute bans.
- **Words that are FINE despite over-restriction** — explicit list of
  normal business English the founder uses (e.g. *streamline*,
  *facilitate growth*, *operations*).
- **Mechanical preferences** — em-dash style, greeting, sign-off, URLs.
- **Canonical examples** — at minimum, one approved email from the
  founder with "why this works" annotation.
- **Voice spec change log** — dated entries when the operator corrects
  this doc.

### 3.4 `value-props.yaml`

```yaml
value_props:
  - id: ""
    claim: ""               # the outcome statement
    pain_addressed: ""
    benefit: ""
    day_in_life: ""         # one-sentence behavioural change
    evidence_pain:
      - speaker: ""
        business: ""
        quote: ""
        source: ""
    evidence_outcome:
      - speaker: ""
        quote: ""
        source: ""
    feature_implementation: ""
    proof_artefact: null
anti_claims:
  - claim: ""               # things we WON'T say
    reason: ""
    evidence_quotes: []
```

Aim for 5-8 value props. Each one is a separate outcome the customer
described wanting. Examples that often appear:

- "Your whole business on one screen"
- "Deal-to-done chained automatically"
- "A database you actually own"
- "The tedious admin disappears"
- "Never miss a lead"
- "Customise in plain English"
- "Relationship marketing that runs itself"

### 3.5 `content-pillars.yaml`

```yaml
pillars:
  - id: ""
    name: ""
    pain_addressed: ""
    default_channel: []
    cadence: ""
    example_topics: []
    customer_quote_anchor:
      speaker: ""
      quote: ""
      source: ""
cross_cutting_threads: []
```

1:1 with value props is the natural mapping — each prop becomes a pillar.

## Step 4 — Walk the operator through it

When done, tell the operator:
- What you wrote, and where
- 3 surprising findings — places where the synthesis contradicts current
  brand language (e.g. the audience recoils from "AI" framing the website
  leads with)
- 2-3 open decisions surfaced inside the docs (TBD slots, working drafts)
  for them to choose between

End with: *"Want me to start drafting a nurture sequence from this?
That's the `design-nurture-sequence` skill."*

---

## Hard rules (both modes)

- **Every claim is anchored in real evidence.** In Mode B that means a
  verbatim quote from the synthesis. In Mode A it means the owner's own
  words, a line scraped from their site, or a real review. If a claim has
  no evidence behind it, it doesn't go in.
- **Never invent customer quotes or testimonials.** A fabricated quote is
  worse than no quote. When you lack a real one, anchor in the owner's own
  words instead.
- **Every only-we claim passes the only-we rubric (business-method.md
  §14):** named against real alternatives including do-nothing, provable
  in one sentence, an identifiable segment cares disproportionately,
  stated in the customer's category language. Fail any → back up one rung.
- **Content guardrails.** Customer-facing copy uses no em dashes, invents
  no facts, quotes, or numbers, and names no third-party vendor. Write it in
  the owner's brand voice; the framing and marketing psychology are the
  owner's choice. The rules are in `knowledge/content-rules.md`.
- **The founder's voice is the brand.** When in doubt, ask before
  diverging from copy they've already approved. Reflect their phrasing back.
- **Don't echo customer recoil into our voice.** The audience recoiling
  from "AI" doesn't mean we never say "AI" — it means we don't LEAD with
  it. AI is the engine, not the headline.
- **Surface contradictions, don't smooth them.** Where the evidence (a
  synthesis, or scraped reviews) contradicts the owner's current website
  copy, flag it as a finding rather than quietly papering over it.
- **No padding.** If a section has 3 things, write 3 — don't pad to 5.
- **TrustPager is never required.** Mode A runs with zero accounts and zero
  files. The transcript-mining synthesis (Mode B) is an optional deeper
  upgrade, offered after the keyless brief — never the entry price.

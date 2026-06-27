---
name: Build Brand Strategy
description: Author the five canonical brand strategy docs (positioning, ICP, voice, value-props, content-pillars) from a customer-voice synthesis file. Every claim anchored in a verbatim customer quote — no invented sales copy.
triggers:
  - build brand strategy
  - write our positioning
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
---

# Build Brand Strategy

You're authoring the five canonical brand strategy docs from a customer-voice
synthesis. Every claim must trace back to a verbatim quote in the synthesis.
If a claim has no quote backing it, it's invented sales copy and doesn't
ship.

The source of truth for shapes + anti-patterns is
[`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md)
— read its "Layer 3 — The brand strategy docs" section before starting.

## Prerequisite

The operator must have already run `build-customer-voice`. Look for a
`customer-voice-synthesis.md` file (usually under
`transcripts/<date>/customer-voice-synthesis.md` or in the marketing
strategy folder the operator points to).

If it doesn't exist, STOP and ask the operator to run `build-customer-voice`
first. Don't fabricate a strategy from thin air.

## Step 1 — Read the synthesis end-to-end

Read every section. You'll be quoting from §1 (who's on calls), §2 (pain),
§3 (jobs to be done), §4 (objections), §5 (competing tools), §6 (buying
moments), §7 (vocabulary), §9 (top 10 quotes), §10 (industry patterns)
throughout the strategy docs.

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
named competitor in the synthesis>

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

## Hard rules

- **Every claim has a verbatim quote.** If a claim has no quote backing
  it, it doesn't go in.
- **The founder's voice is the brand.** When in doubt, ask before
  diverging from copy they've already approved.
- **Don't echo customer recoil into our voice.** The audience recoiling
  from "AI" doesn't mean we never say "AI" — it means we don't LEAD with
  it. AI is the engine, not the headline.
- **Surface synthesis-vs-website-copy contradictions.** Don't quietly
  smooth them over. Flag them as findings.
- **No padding.** If a section has 3 things, write 3 — don't pad to 5.

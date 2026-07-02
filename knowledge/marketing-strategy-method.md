# Marketing Strategy Method — from customer voice to live nurture sequence

The canonical workflow for building a brand voice, positioning, and nurture
sequence that's grounded in what your customers actually say — not in copy
you invented for them. This document is the source of truth for the four
skills: `build-customer-voice`, `build-brand-strategy`, `design-nurture-sequence`,
`wire-nurture-sequence`.

> **Founder's voice IS the brand.** Every guideline below is a guide, not
> a rulebook. When the operator's actual approved copy contradicts a
> guideline here, the operator wins — and this doc gets updated to reflect
> what shipped.

---

## The three-layer pipeline

```
Layer 1 — Raw input (machine-generated, never hand-edited)
  ↓  CRM bundle (tools/dump-crm-bundle.py)
  ↓  Transcripts ≥ 5 minutes (tools/dump-transcripts.py)
Layer 2 — Synthesis (the customer's own voice, frozen evidence)
  ↓  customer-voice-synthesis.md
Layer 3 — Strategy docs (the brand's positioning + funnel)
  ↓  positioning.md, icp.yaml, voice.md, value-props.yaml, content-pillars.yaml
  ↓  funnel/<sequence>.yaml
Layer 4 — Live execution (TrustPager auto queue + automations)
```

Each layer is built **from** the layer above. Synthesis is INPUT to the
brand voice, not the brand voice itself. Customer phrases are available
to reach for; they're not required in every email.

## Where this method sits in the business method

- A nurture sequence is warm follow-up in the content/outreach doors
  (business-method.md §10.1).
- It exists to fix the engaged-leads-to-conversations stage (§10.3) —
  before designing one, confirm that IS the weak stage.
- For locally bought shapes, the local gravity gate (§10.5) comes before
  any sequence work.
- Swapping the magnet, creative, or sequence on an existing channel is a
  Better move; a new channel is New (§4.4) — "redesign the sequence"
  precedes "try a new platform".

---

## Layer 2 — Customer voice synthesis

Pull ≥5min call + meeting transcripts (`tools/dump-transcripts.py`), then
read every single one end-to-end and write **`customer-voice-synthesis.md`**
with these 10 sections, in this order:

1. **Who's actually on these calls** — industries, business sizes, roles,
   patterns. Quote names + businesses verbatim.
2. **The pain — in their own words** — the most important section. Cluster
   into themes. Quote VERBATIM with `[Speaker, transcript-filename]`
   footnotes. Aim for 5-15 themes, 2-6 verbatim quotes each. Use the
   actual words customers say.
3. **Jobs to be done** — what outcomes are they trying to achieve. Quote
   them describing the END STATE they want.
4. **Objections + hesitations** — what stalls the decision. Quote the
   language.
5. **Competing tools / what they're escaping** — every named tool. Table
   format: tool → who's escaping it → verbatim complaint.
6. **The "buying moment"** — what triggers a real decision (just spent
   on Meta ads / just took over / private equity offer / Salesforce
   sunk-cost moment / etc).
7. **Vocabulary list — the actual words they use** — flat list of phrases
   marketing copy should reach for. "Slipping through the cracks", "40
   pieces on the table", "on the tools", "one-man band", etc.
8. **Who this is NOT for** — quote moments where a prospect was clearly
   disqualified. Negative-space ICP.
9. **Top 10 representative quotes** — the 10 most pungent verbatim quotes
   that capture WHO this audience is and what they need.
10. **Industry pattern observations** — what industries are
    over-represented? Modal customer profile?

**Hard rules for the synthesis:**

- **Read every file end-to-end.** Don't skim. If a file is large, paginate
  with `Read(offset=, limit=)` until you've covered the entire thing.
- **Quote VERBATIM.** Don't paraphrase. Each quote needs the speaker name
  + which file it came from.
- **IGNORE the host's voice.** Filter out the salesperson / operator —
  the synthesis is the OTHER speaker's voice. (Internal team chats also
  filter out unless someone external joins.)
- **Real names are fine** in this internal doc. They're the operator's
  own customers. Don't pass these names to subagents that produce
  customer-facing output (commit messages, MCP descriptions, marketing
  copy) — generic placeholders only at that boundary.
- **Don't pad.** If you only find 3 quotes for a theme, write 3. Quality
  beats quantity.

---

## Layer 3 — The brand strategy docs

Five Markdown / YAML files, every claim anchored in a verbatim quote from
the synthesis.

### `positioning.md`

- **Who we are** — identity statement.
- **Who we serve** — one-liner naming the buyer in their own language.
- **The pain we solve** — 3-5 named pain themes, each with a verbatim quote.
- **The promise** — outcome we deliver, phrased the way customers
  articulate it back.
- **The only-we claim** — why us, not the competitors customers named.
- **Proof** — customer count, industries, founder credibility.
- **Geographic + cultural register** — where you operate, what register
  matches.

### `icp.yaml`

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
    competing_tools_escaped: {}
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
  patterns: []
```

### `voice.md`

- **Meta-rule at the top:** *"Founder's voice IS the brand. When this doc
  and the founder disagree, the founder wins."*
- **Tone — 5 adjectives**, each backed by evidence.
- **Signature moves** — specific rhetorical patterns. Forward-looking
  subjects, warm human openers, one core idea per paragraph, customer
  phrases as seasoning.
- **Vocabulary AVAILABLE** — phrases lifted from §7 of synthesis. Reach
  for when they fit; not required in every email.
- **Watch out for** — VC-bro, Salesforce-enterprise speak, AI-as-hero,
  copywriter abstractions, "platform" as hero noun, "solopreneur".
- **Words that are FINE despite over-restriction:** *streamline*,
  *facilitate growth*, *strategy*, *operations*, etc — normal business
  English the founder actually uses.
- **Mechanical preferences** — em-dash style, greeting, sign-off block,
  raw URLs as href + visible text, no auto-CCs.
- **Canonical email example** — one approved email from the operator,
  with "why this works" annotations. This becomes the model future
  drafts match.

### `value-props.yaml`

```yaml
value_props:
  - id: ""
    claim: ""               # outcome statement
    pain_addressed: ""
    benefit: ""
    day_in_life: ""         # one-sentence behavioural change
    evidence_pain:          # quotes proving the pain is real
      - speaker: ""
        business: ""
        quote: ""
        source: ""
    evidence_outcome:       # quotes proving the audience wants this
      - speaker: ""
        quote: ""
        source: ""
    feature_implementation: ""
anti_claims:                # things we WON'T say + why
  - claim: ""
    reason: ""
    evidence_quotes: []
```

### `content-pillars.yaml`

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
```

---

## Layer 4 — Designing a nurture sequence

### Inputs

- `voice.md` (how to write)
- `value-props.yaml` (what to claim)
- `content-pillars.yaml` (themes)
- The TARGET auto queue's existing structure (stages, delays)
- Available help-center videos (`help-center-public?action=list`)

### Per-step shape

Every email follows the same canonical structure:

1. **Subject** — forward-looking, action-oriented. A verb the reader can
   mentally agree to. NOT a receipt for an action they just took.
   Subjects and hooks obey the content-rules bridge (business-method.md
   §18): outcome- or curiosity-led; the pain anchor is internal
   rationale only.
2. **Warm human opener** — `Hi {{contact.first_name}}` or `Great to meet
   you {{contact.first_name}}` for Day 0.
3. **One core idea per paragraph.** Don't stuff three customer pains
   into one sentence.
4. **The help-center video** — soft CTA. Raw URL as both href and
   visible text.
5. **Sign-off block** — exact two-line:
   ```
   Warmest regards,
   {{operator_first_name}}
   ```

### Picking the help video for each stage

For each Day stage:

1. Identify the customer concern that's MOST ACUTE by that point in the
   trial (i.e. unaddressed by earlier emails).
2. Find the help video whose title most directly addresses that concern.
3. Cross-reference against the canonical pain themes in synthesis §2.
4. If the video is feature-led (e.g. "AI Needs Analysis"), check whether
   it cuts a real customer concern — feature-showcase ≠ concern-cutting.

### Sequence-level patterns

- **Day 0 = the activation moment.** First email goes immediately on
  enrollment. Often a foundational setup step (e.g. "connect Claude")
  that every subsequent email assumes. This is the activation protocol
  at work (business-method.md §11.3): a felt win in the first days, and
  a re-sell of the decision inside 48 hours (directional).
- **Days 2-N escalate** — start with the spine (pipeline / data),
  add automations, add comms, then move to power features.
- **Final day = the conversion close.** The most universal,
  highest-leverage feature, framed via meta-narrative if possible
  ("the same way these emails reached you, yours can reach your
  customers"). Internally, the close follows the next-win timing
  (business-method.md §9.4); the line the customer reads names the next
  win (§18).

---

## Wiring the sequence into a TrustPager auto queue

### Canonical settings to copy verbatim per step

Every `send_gmail_email` action in the sequence uses the SAME settings,
except for `subject` and `body`:

```yaml
action_type: send_gmail_email
config:
  sender_mode: company
  email_config_id: <your-finalpiece-mail-config-id>
  recipient_target: contact
  bcc: ["<operator's email>"]    # monitoring loop
  subject: <per step>
  body:    <per step — HTML with <p> tags>
```

### Auto queue step bumping — the reverse-order trick

When inserting a NEW step at position 1 (e.g. adding Day 0 to an existing
Day-2-onwards queue), the existing step_orders 1..N need to bump to 2..N+1.
Do this in REVERSE order (N→N+1, N-1→N, ..., 1→2) so no two steps ever
share the same step_order during the operation:

1. Update step at step_order=N → step_order=N+1
2. Update step at step_order=N-1 → step_order=N
3. ...
4. Update step at step_order=1 → step_order=2
5. Add new step with step_order=1

If TrustPager's API ever enforces unique step_order via a DB constraint
in the future, this order is the only safe way to do the shuffle without
hitting a transient violation. (Currently the constraint isn't enforced
strictly — but the reverse-order shuffle is the defensive pattern.)

### Help-center slug discovery

The help center API is the source of truth for article slugs. Don't guess
kebab-case from titles — many drop the "how-to" prefix:

```bash
curl -s "https://api.trustpager.com/functions/v1/help-center-public?action=list" \
  | jq '.articles[] | {title, slug}'
```

Search by title before writing any URL into an email body. Wrong slugs
silently redirect to the help-center index.

---

## Anti-patterns we've already corrected

These came from real corrections in real sessions. Don't re-walk them.

| Anti-pattern | Why it's wrong | What lands instead |
|---|---|---|
| Three customer-pain anchors stuffed into one sentence | None of them land | One core idea per paragraph |
| "Thanks for your enquiry" subject | Receipt for past action, no forward energy | "Let's streamline your operations" — verb |
| "Your details just came through" opener | Reads like SMTP receipt | "Great to meet you" — human |
| "AI-powered platform" hero copy | Buyer recoils from AI-as-hero framing | AI is the engine, not the headline |
| Treating customer-voice synthesis as scripture | Customer phrases as seasoning, not the meal | One well-placed phrase per email max |
| Banning "facilitate growth" / "streamline operations" | These are normal business English the founder uses | Founder voice IS the brand |
| Feature-showcase video as the convert-day CTA | Doesn't cut a real concern | Pick the video that defuses the most acute remaining pain |
| Authoring sequences without reviewing transcripts first | Invented sales copy | Synthesis FIRST, then voice, then sequence |
| 3 alternative drafts when the operator asked for advice | Decision burden back on them | Commit to ONE recommended version |

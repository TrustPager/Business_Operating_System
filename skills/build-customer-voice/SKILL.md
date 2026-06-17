---
name: Build Customer Voice
description: Pull ≥5-minute call + meeting transcripts, read every one verbatim, extract the customer's actual pain into a 10-section synthesis Markdown file. Foundation for every other marketing strategy artefact — voice, ICP, positioning, value props, nurture sequences.
triggers:
  - build customer voice
  - extract customer language
  - what do customers actually say
  - mine transcripts
  - customer voice synthesis
  - what pain do my customers describe
  - voice-of-customer research
---

# Build Customer Voice

You're building the canonical evidence file the operator's marketing
strategy will be grounded in. Everything else (brand voice, positioning,
nurture sequences) gets authored FROM this file. If it's wrong, every
downstream artefact inherits the error.

The source of truth for the method is
[`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md)
— read its "Layer 2 — Customer voice synthesis" section before starting
if you haven't.

## Step 1 — Pull the transcripts (MCP)

Use the `trustpager` MCP server. All reads — nothing here is journaled or needs approval.

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**.

1. **List the candidates.** Call `list_transcripts(transcription_status: "complete", limit: 100)` and paginate via the `after` cursor (each list row has `duration_seconds`, `type`, `occurred_at`, `title`, linked entities — but **no** transcript body). Keep paging while `pagination.has_more` is true, up to a sane cap (~2000 rows / ~20 pages).
2. **Filter by duration.** Keep only rows whose `duration_seconds` is **≥ 300** (5 minutes) — that's the default; if the operator asks for a different floor (e.g. 10 min = 600), use theirs. Split the survivors into **calls** (`type: "call"`) and **meetings** (`type: "meeting"`). Target roughly the **30 most recent of each** (newest first) unless the operator wants more or fewer.
3. **Fetch each transcript's full text.** For every kept row, call `get_transcript(id: <transcript_id>)` — that's the call that returns `transcript_text`. The text is usually a JSON-encoded blob containing a `transcript_vtt` (WebVTT) field and sometimes a `summary`; read the VTT speaker lines and ignore the cue numbers / `00:00 -->` timestamps. Some sources store plain text instead — handle either.

Most Twilio phone calls between humans aren't transcribed — only TrustPager Notetaker (Recall) meetings and Retell voice-agent calls have rich text. Transcripts with an empty `transcript_text` just get skipped; don't be alarmed by how many that is.

## Step 2 — Read every transcript end-to-end

**Read the full text of every transcript you fetched** — both calls and
meetings. Don't skim. If a transcript is very large, work through it in
chunks until you've covered the entire thing.

**Filter out the host's voice.** The salesperson / operator's lines are
not customer voice. You want what the OTHER speaker says. Internal team
chats (operator talking to teammates before the customer joins) also
filter out — but DO keep external participants when they speak.

## Step 3 — Write `customer-voice-synthesis.md`

Write it with the `Write` tool to a date-stamped path, e.g.
`transcripts/<UTC-date>/customer-voice-synthesis.md` (create the folder if
needed). Tell the operator explicitly where you wrote it so they can find it.

The file MUST have these 10 sections, in this order:

### 1. Who's actually on these calls

Industries, business sizes, roles, geographies. Quote names + businesses
verbatim. Identify recurring patterns ("mortgage brokers stuck in
aggregator software", "trades on the tools", "ex-corporate consultants
going solo").

### 2. The pain — in their own words

**The single most important section.** Cluster into themes. Quote
VERBATIM with footnote-style `[Speaker Name, Business, transcript-filename]`.

Aim for 5-15 themes with 2-6 quotes each. Examples of theme shapes:
- "Things slipping through the cracks" (leads, follow-ups, info)
- "Doing everything yourself" (solopreneur overwhelm)
- "Tool fragmentation" (escaping multiple disconnected tools)
- "Tech-light" (explicit non-technical self-description)
- "Cost anxiety" (fear of another monthly bill)
- "Missed calls / inbound leakage"
- "Marketing money wasted because follow-up doesn't happen"
- "Data captivity" (aggregator / enterprise CRM owns my book)
- "Quote / proposal hell" (the recurring proposal-building bottleneck)
- "Salesforce / HubSpot trauma" (sunk-cost + consultant-tax pain)
- "AI scepticism" ("I don't need lazy click and forget")

Use the actual words customers say. Don't invent themes that aren't in
the transcripts.

### 3. Jobs to be done

What END STATE are they trying to reach? Quote them describing it.

### 4. Objections + hesitations

What stalls the decision? Quote the language — cost objections, prior
bad CRM experience, complexity fear, "let me think", etc.

### 5. Competing tools / what they're escaping

Every named tool, in a table:

| Tool | Who's escaping it | Verbatim |
|------|-------------------|----------|
| Salesforce | (names) | "PTSD, still having nightmares" |
| HubSpot | (names) | "Difficult to learn" |
| ... | | |

### 6. The "buying moment"

What triggers a real decision? Just spent on Meta ads / just took over
a business / just got a Salesforce upsell / just left an aggregator /
private equity offer / etc. Quote the moment.

### 7. Vocabulary list — the actual words they use

Flat list of recurring phrases. Marketing copy reaches for these first;
invented language second.

- "Slipping through the cracks"
- "40 pieces on the table"
- "On the tools"
- "One-man band"
- "I just want milk"
- "Clunky / overkill"
- "PTSD / bad juju"
- "Like a dog and a bone"
- "Strike while the iron's hot"
- "L plates"
- etc.

### 8. Who this is NOT for

Quote moments where a prospect was clearly disqualified. Too big, too
small, wrong industry, wrong problem.

### 9. Top 10 representative quotes

The 10 single most pungent verbatim quotes that capture WHO this
audience is. Each quote: speaker name + business + filename.

### 10. Industry pattern observations

One short paragraph: which industries are over-represented? Modal
customer profile? Quote evidence.

## Step 4 — Report back

When done, tell the operator:
- Where the file was written
- Total quotes captured (rough count)
- Top 3 surprising findings — things that contradict what marketing
  copy currently says about the audience
- The 1 modal-customer profile that emerged most strongly

Keep this report under 200 words. The synthesis file IS the deliverable;
your report is the headline.

## Hard rules

- **Read every transcript end-to-end.** No skimming.
- **Quote VERBATIM.** Don't paraphrase.
- **Filter the host's voice.** Synthesis = customer voice only.
- **Real names stay in this internal file.** Don't pass these names
  into agent prompts that produce customer-facing output (commit
  messages, MCP descriptions, marketing copy).
- **No padding.** Quality beats count.
- **Don't editorialise.** If the synthesis suggests the operator's
  current positioning is wrong, surface that as a finding — but
  don't rewrite the strategy in the synthesis file. That's the
  next skill's job.

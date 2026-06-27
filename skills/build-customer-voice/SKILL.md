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
function_slot: research
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
status: active
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

## Step 1 — Dump the transcripts

Run the tool. Defaults to ≥5min duration, target 30 calls + 30 meetings,
output into a date-stamped folder:

```bash
python tools/dump-transcripts.py
```

Adjust `--min-duration`, `--target`, `--out` if the operator asks for
something different.

The tool writes:
- `transcripts/<UTC-date>/calls/*.md`
- `transcripts/<UTC-date>/meetings/*.md`
- `transcripts/<UTC-date>/_index.json`

Most Twilio phone calls between humans aren't transcribed. The tool
silently skips those — only Recall AI Notetaker meetings and Retell
voice-agent calls have rich text. Don't be alarmed by the "skipped
empty" count.

## Step 2 — Read every transcript end-to-end

**Read every single file in `calls/` and `meetings/`.** Don't skim. If
a file is large (over a few thousand lines), paginate with `Read(offset=,
limit=)` until you've covered the entire thing.

**Filter out the host's voice.** The salesperson / operator's lines are
not customer voice. You want what the OTHER speaker says. Internal team
chats (operator talking to teammates before the customer joins) also
filter out — but DO keep external participants when they speak.

## Step 3 — Write `customer-voice-synthesis.md`

Output path: alongside the transcripts folder, e.g.
`transcripts/<UTC-date>/customer-voice-synthesis.md`. Tell the operator
explicitly where you wrote it so they can find it.

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

- **Read every file end-to-end.** No skimming.
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

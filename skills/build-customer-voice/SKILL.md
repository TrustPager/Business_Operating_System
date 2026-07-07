---
name: Build Customer Voice
description: Turn the words your customers actually use into a customer-voice doc: the verbatim phrases, the outcomes they want, the worries that stall them, in their language. Keyless from reviews, testimonials, and call notes you paste in; deepens into a full transcript-mined synthesis when your workspace is connected. Foundation for every marketing strategy artefact.
triggers:
  - build customer voice
  - extract customer language
  - what do customers actually say
  - capture how my customers talk
  - customer voice synthesis
  - turn reviews into a customer voice doc
  - voice-of-customer research
  - mine my testimonials
function_slot: strategy
requires_driver: markitdown
requires_credential: none
data_path: local
status: active
---

# Build Customer Voice

You're building the canonical evidence file the owner's marketing strategy
gets grounded in. Everything else (brand voice, positioning, value props,
nurture sequences) gets authored FROM this file. If it's wrong, every
downstream artefact inherits the error. So it must be made of real words
real customers used, never copy you invented for them.

The source of truth for the method is
[`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md)
— read its "Layer 2 — Customer voice synthesis" section before starting if
you haven't. (Note: that method's transcript-pull and live-queue layers are
the connected-tier deepener, not a requirement for this skill to run.)

## Pick the mode — start with what you have

There are two ways to run this, and the right one depends on what evidence
exists right now:

| You have… | Mode | What you produce |
|---|---|---|
| Reviews, testimonials, call notes, support emails — pasted in or in local files — **the default day-one path** | **Keyless** | `customer-voice-synthesis.md`: the same 10-section doc, built from the words in front of you |
| A connected workspace with recorded call + meeting transcripts | **Connected deepener** | The same doc, mined from a much larger, richer evidence base |

**Default to the keyless mode whenever you don't already have a connected
workspace pulling transcripts for you.** It needs no accounts and no setup —
only the words the owner can hand you. Do NOT stop and demand recorded calls;
that's the cold-start failure this skill exists to avoid. The connected
transcript mine is the *upgrade* you offer once it's available, never the
price of entry.

---

# Mode A — Keyless (the day-one default)

This runs entirely from material the owner already has: the reviews on their
Google or Facebook page, the testimonials on their site, a folder of support
emails, notes they jotted after a sales call, a few screenshots of texts from
happy customers. No connection, no special access. In a few minutes you give
them back the real voice of their market, organised.

## A1 — Gather the raw customer words

Pull customer voice from whatever the owner can put in front of you, in this
order of richness:

1. **Anything the owner pastes.** Reviews, testimonials, customer emails,
   support-ticket text, social comments, notes typed up after a call. Treat
   every pasted block as primary evidence — capture the exact phrasing.
2. **Local files the owner points you at.** A folder of saved reviews, an
   exported reviews CSV, a PDF of testimonials, a Word doc of call notes, a
   screenshot of a text thread. Convert each one to Markdown first so you're
   reading clean text, not guessing at a scan:

   ```bash
   python ~/.claude/bos-run.py tool markitdown_convert "<path-to-file>"
   ```

(The `~/.claude/bos-run.py` launcher resolves the install location for you. If it is missing, run `python tools/setup.py` once from the BOS directory to create it.)

   This handles PDF, Word, Excel, PowerPoint, images (OCR), HTML, CSV, JSON.
   If the converter reports it isn't installed, relay its one-line install
   hint and continue with whatever was pasted directly. If a file comes back
   empty (e.g. a scan with no readable text), say so plainly rather than
   inventing content.
3. **One good prompt when the well is shallow.** If there's little to work
   with, ask the owner for the few things that unlock the most signal — for
   example: *"Paste me your last 10 Google reviews, or 3-4 emails from
   customers who were thrilled, and I'll pull the patterns out."* A real doc
   built from a handful of genuine reviews beats a padded one built from
   nothing.

**Read everything end-to-end.** Don't skim a single review. If a pasted
block or a converted file is long, read all of it.

**Keep the customer's voice, drop the owner's.** In call notes and email
threads, the owner's / salesperson's own lines are not customer voice — you
want what the OTHER person said. Internal team chatter filters out too.

## A2 — Write `customer-voice-synthesis.md`

Offer to write it to `marketing-strategy/<BrandName>/customer-voice-synthesis.md`
(or alongside the source files the owner pointed you at). Tell the owner
exactly where you wrote it so they can find it.

The file has these 10 sections, in this order. With a smaller keyless
evidence base you'll have fewer quotes per theme than a full transcript mine
would — that's fine. Write what the evidence genuinely supports; never pad to
hit a count.

**What downstream reads from each section:** §3 jobs-to-be-done captures
the Arrival in the buyer's own words (business-method.md §6); §4 worries
feed guarantee design — the buyer's biggest fear, inverted (§7.2); §5
competing options are rung 1 of the positioning ladder — real alternatives
including "no tool at all" (§14); §6 buying moments feed
urgency-as-gain-timing (§7.4, §18); §2 pain themes feed the internal
problem list of the Category-of-One build (§7.1), never shipped copy (§18).

### 1. Who's actually leaving these words

Industries, business sizes, roles, locations — whatever the source material
reveals. Quote names + businesses verbatim where they're given. Identify
recurring patterns ("repeat customers who'd tried a cheaper option first",
"first-timers nervous about cost", "referrals from existing clients").

### 2. The pain — in their own words

**The single most important section.** Cluster into themes. Quote VERBATIM
with a footnote-style source tag `[Name or "Google review", source-file or
"pasted"]`. Aim for 5-15 themes with the quotes you actually have for each.
Examples of theme shapes:

- "Things slipping through the cracks" (leads, follow-ups, info)
- "Doing everything yourself" (overwhelm)
- "Tool fragmentation" (juggling disconnected tools)
- "Tech-light" (explicit non-technical self-description)
- "Cost anxiety" (worry about another monthly bill)
- "Missed calls / enquiries going cold"
- "Marketing money wasted because follow-up doesn't happen"

Use the actual words customers used. Don't invent themes that aren't in the
material.

### 3. Jobs to be done

What END STATE are they trying to reach? Quote them describing it.

### 4. Worries + hesitations

What stalls the decision? Quote the language — cost, a prior bad experience,
fear of complexity, "let me think about it". (Naming the worry here, in this
internal evidence doc, is fine — this section is for the owner's eyes, not
customer-facing copy.)

### 5. Competing options / what they're escaping

Every named tool, brand, or alternative, in a table:

| Option | Who's escaping it | Verbatim |
|------|-------------------|----------|
| (tool/brand) | (names) | "(what they said)" |
| ... | | |

### 6. The "buying moment"

What triggered a real decision? Just outgrew a cheaper option / just got
let down by a competitor / just took over a business / a big job landed.
Quote the moment.

### 7. Vocabulary list — the actual words they use

Flat list of recurring phrases. Marketing copy reaches for these first;
invented language second.

- "Slipping through the cracks"
- "On the tools"
- "One-man band"
- "Clunky / overkill"
- "Peace of mind"
- etc. — only the phrases that actually appear in the material.

### 8. Who this is NOT for

Quote any moment where someone was clearly a poor fit — wrong job, wrong
size, wrong expectation. Negative-space ICP. If the evidence doesn't show
this, say so rather than inventing a misfit.

### 9. Top representative quotes

The single most pungent verbatim quotes that capture WHO this audience is.
Aim for up to 10 — fewer if the evidence is thinner. Each quote: name (or
"Google review") + source.

### 10. Pattern observations

One short paragraph: which customer types are over-represented? The modal
customer profile? Quote the evidence behind it.

## A3 — Report back

When done, tell the owner:
- Where the file was written
- Roughly how many real quotes it captured, and from how many sources
- The top 2-3 surprising findings — phrases or themes that contradict how
  their current website talks about the audience
- The 1 modal-customer profile that emerged most strongly

Keep this report under 200 words. The synthesis file IS the deliverable;
your report is the headline.

## A4 — Offer the deeper mode (don't make it the entry price)

Once the keyless doc is in their hands, offer the upgrade plainly:

> This is built from the reviews and notes you handed me. When your customer
> conversations are being recorded in one place, I can mine every call and
> meeting end-to-end and turn this into a much richer version — far more
> quotes, far more themes. No rush; this doc stands on its own today.

---

# Mode B — Connected deepener (the richer upgrade)

This is the deeper path, and it runs only **if your workspace is connected**
and your customer calls and meetings are being recorded there. It mines that
full transcript library — many more conversations than anyone would paste by
hand — into the same 10-section `customer-voice-synthesis.md`, just with a
much larger evidence base behind every theme.

**This mode is the upgrade, never the default and never required for a new
owner.** When no connected transcript library is available, run Mode A — do
not stop and demand one.

The connected workflow (how the recorded conversations get pulled and read in
bulk) is documented in the "Layer 2" section of
[`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md).
Follow that when, and only when, the workspace is connected. Everything about
the output is identical to Mode A: the same 10 sections, the same verbatim
discipline. The only
difference is the size and richness of the evidence.

---

## Hard rules (both modes)

- **Quote VERBATIM.** Don't paraphrase a customer's words into your own.
- **Keep the customer's voice, drop the owner's.** The synthesis is what the
  CUSTOMER said, not the owner / salesperson.
- **Read every source end-to-end.** No skimming, in either mode.
- **Never invent a quote, a review, or a testimonial.** A fabricated quote is
  worse than no quote. If a theme has only one real quote, write one. If a
  section has no evidence, say so.
- **No padding.** Quality beats count. A thinner doc made of real words beats
  a fat one made of guesses.
- **Real names stay in this internal file.** This doc is the owner's own
  evidence. Don't carry real customer names into anything customer-facing
  (marketing copy, public posts) — generic placeholders at that boundary.
- **This doc is internal evidence; downstream copy is the owner's brand.**
  Naming pain and worries here is fine (§2, §4), it's for the owner. The brand
  strategy and copy authored FROM this doc are written in the owner's brand
  voice; the framing and marketing psychology are the owner's choice.
- **Don't editorialise.** If the evidence suggests the owner's current
  positioning is off, surface that as a finding — don't rewrite the strategy
  inside this file. That's the next skill's job (`build-brand-strategy`).

---
name: Write A Proposal
description: Turn a priced scope and the owner's brand voice into the proposal that wins the job, an on-brand proposal or statement of work in the owner's voice, written out as a real .docx they can send. Consumes a priced breakdown (from price-my-work or typed in) plus their voice doc, and lays out cover, understanding of the need, scope and deliverables, the priced breakdown, timeline, terms, and the next step. Also has a tender / technical-section mode for technical-services firms: a methodology, technical-approach, or capability section (not a price-first proposal) answering a tender or RFP. Keyless, works from what you have day one. One proposal per run.
triggers:
  - write a proposal
  - write me a proposal
  - turn this quote into a proposal
  - draft a statement of work
  - write the SOW
  - proposal from my priced scope
  - make this priced job into a proposal
  - write the doc that wins the job
  - proposal in my voice
  - write a tender response
  - write the methodology section
  - draft a technical approach
  - write a capability statement
  - answer this tender
  - write the technical section
function_slot: strategy
requires_driver: doclib
requires_credential: none
data_path: local
status: active
---

# Write A Proposal

You turn a priced scope and the way the owner talks about their work into the
artefact that wins the job: an on-brand proposal or statement of work, in the
owner's own voice, written out as a real `.docx` they can send today. The
owner brings the priced scope and their voice; you give it the structure,
the register, and the file.

This runs keylessly day one. The inputs are things the owner already has: a
priced breakdown they (or `price-my-work`) produced, plus any brand voice they
have built. No accounts, no connections. The win is the finished proposal in
their hands.

## Bounded: one proposal per run

One proposal per run. If the owner hands you several jobs or several
prospects, write the first proposal properly, then offer the next as a fresh
run. A focused proposal that lands beats a sprawl of half-built ones.

## Pick the mode — price-first proposal, or a tender / technical section

There are two ways to run this. Pick the one that fits what the owner is
writing, and confirm it if it isn't obvious:

| The owner is writing... | Mode | What you produce |
|---|---|---|
| **A proposal / SOW for a priced job** — the default | **Mode A: priced proposal** | The seven-section, price-first proposal below: cover, understanding, scope, the priced breakdown, timeline, terms, next step. |
| **A tender / RFP response, or a methodology / technical-approach / capability section** for a technical-services firm | **Mode B: tender / technical section** | A methodology / technical-approach / capability SECTION that answers the criteria, where price is set elsewhere (a separate schedule, or not by this section at all). |

**Mode A is the default.** Choose Mode B only when the owner is answering a
tender / RFP, or explicitly wants a methodology, technical-approach, or
capability section rather than a price-first proposal ([name]'s case: a
technical-services firm whose tender sections are graded on approach and
capability, with price submitted separately). When in doubt, ask one plain
question: *"Is this a priced proposal to send a client, or a technical /
methodology section answering a tender?"*

---

# Mode A — Priced proposal (the default)

## Step 1 — Gather the two inputs

A proposal stands on two things: **what the work is and what it costs** (the
priced scope) and **how the owner sounds** (the voice). Take in both, and ask
only for what is genuinely missing.

1. **The priced scope.** Ideally a priced breakdown from `price-my-work`: the
   line items, the margin, the total, the assumptions. **If the owner already
   states a price, take it and move on, with zero friction.** A proposal is
   often written against a deadline; an owner who has already settled on a
   number does not want to be detoured into a pricing exercise. Use their
   figure as the priced scope and go straight to the outline. Only when there
   is **no priced number at all** is the cleanest move to offer `price-my-work`
   first so the proposal rests on a number they can stand behind, and even then
   it is an offer, not a gate. Do not invent a price or pad the scope with work
   the owner did not name.
2. **The brand voice.** If the owner has built a `voice.md` or a first-brand
   brief from `build-brand-strategy`, read it first so the proposal sounds like
   them, not like a template. Read
   [`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md)
   for what that voice doc carries. If there is no voice doc, write in a warm,
   plain, professional register and reflect the owner's own phrasing back from
   whatever they have told you.

Also confirm the few specifics a proposal needs and a priced breakdown often
does not carry: **who it is for** (the prospect or company name), **what the
job is in one line**, the **timeline** (start, milestones, finish), and any
**terms** the owner wants stated (deposit, payment schedule, validity window,
what is included and excluded). Ask one plain question for anything missing
rather than guessing it.

It is fine to name the prospect's problem in *this discovery chat*: "what is
the pain that has them looking for this?" is a normal question. The shipped
proposal stays positive and outcome-led (Step 4).

## Step 2 — Lay out the proposal in chat first

Before you write the file, show the owner the proposal as a section outline so
they can correct it cheaply. Use these seven sections, in this order:

1. **Cover / intro** — who it is for, who it is from, the job in one line, and
   a warm opening that names the outcome the prospect wants.
2. **Understanding of the need** — reflect back what the prospect is trying to
   achieve, in the prospect's own terms, so they feel heard. This is where the
   proposal earns trust.
3. **Scope and deliverables** — exactly what the owner will do and hand over,
   as clear deliverables. Name what is included; name what is not, so there are
   no surprises later.
4. **The priced breakdown** — the line items, the total, and the basis for the
   number, carried straight from the priced scope. Keep the margin handled the
   way `price-my-work` framed it: the price is shown plainly; the assumptions
   sit underneath so the number holds up if the prospect asks how it was
   reached.
5. **Timeline** — start, key milestones, and finish, in the owner's real dates
   or lead times.
6. **Terms** — deposit, payment schedule, what is included and excluded,
   validity window, and anything else the owner stated. Never invent a legal or
   payment term the owner did not give you.
7. **Next step** — one clear, positive call to action: how the prospect says
   yes and what happens the moment they do.

Confirm the outline (and especially the price, the timeline, and the terms)
before generating the file.

## Step 3 — Write the proposal to a real .docx

Once the owner is happy with the outline, generate the document with the
keyless document writer (the `doclib` write path,
[`tools/write_docx.py`](../../tools/write_docx.py), see
[`knowledge/document-tools-method.md`](../../knowledge/document-tools-method.md)).
Build the proposal as an ordered list of blocks and pass them as JSON. The
priced breakdown is a **`table`** block, so the line items render as a real
grid the prospect can read at a glance, not bullets with `$____`:

```bash
python ~/.claude/bos-run.py tool write_docx --out "Proposal - <Prospect> - <job>.docx" --blocks '[
  {"type":"heading","text":"Proposal for <Prospect>","level":1},
  {"type":"paragraph","text":"<warm intro that names the outcome they want>"},
  {"type":"heading","text":"Understanding your need","level":2},
  {"type":"paragraph","text":"<reflect their goal back in their words>"},
  {"type":"heading","text":"Scope and deliverables","level":2},
  {"type":"bullet","text":"<deliverable 1>"},
  {"type":"bullet","text":"<deliverable 2>"},
  {"type":"heading","text":"Your investment","level":2},
  {"type":"table",
   "header":["Item","Qty","Price"],
   "rows":[["<line item 1>","<qty>","<price>"],
           ["<line item 2>","<qty>","<price>"],
           ["Total","","<total>"]]},
  {"type":"paragraph","text":"<the basis for the number / the assumptions underneath it>"},
  {"type":"heading","text":"Timeline","level":2},
  {"type":"paragraph","text":"<start, milestones, finish>"},
  {"type":"heading","text":"Terms","level":2},
  {"type":"paragraph","text":"<deposit, payment, inclusions, validity>"},
  {"type":"heading","text":"The next step","level":2},
  {"type":"paragraph","text":"<one clear positive call to action>"}
]'
```

(The `~/.claude/bos-run.py` launcher resolves the install location for you. If it is missing, run `python tools/setup.py` once from the BOS directory to create it.)

Carry the line items, quantities, and totals straight from the priced scope
into the table verbatim; never invent or pad a line. You can also pipe the JSON
in on stdin if it is long. If the wrapper reports that the document writer is
missing a piece, offer the one-time setup in plain language and run it on a yes
(the detect, offer, install-on-yes, verify loop in
[`knowledge/document-tools-method.md`](../../knowledge/document-tools-method.md)),
then retry. Never hand the owner a command. If the write fails, show the error
plainly rather than pretending a file exists. Use a clear file name that names
the prospect and the job so the owner can find it later.

## Step 4 — Before you output anything customer-facing: positive/outcome-led, and NO em dashes (hard requirement)

The proposal is **customer-facing output**, so it obeys the positive-only
rule: every section names what the prospect gets, what success looks like, and
the result they are buying. The value is the outcome, never the pain or what is
missing.

**Before you output anything customer-facing: positive/outcome-led, and NO em
dashes (use colons, commas, parentheses, or separate sentences).** A field test
shipped a quote with an em dash because nothing reminded the model; this is your
reminder. Check the proposal before handing it over.

- Don't write: "stop losing time to the wrong contractor", "no more unfinished
  jobs", "you are frustrated with your current setup", "tired of overruns".
- Do write: outcome-led lines, "your kitchen finished on time and on budget,
  ready to use the week you planned", "one team, one number, one clear date
  for done", "the result you pictured, signed off and standing".
- A term, a price, or an exclusion is still stated plainly: name it as the path
  to a good outcome (clear scope, a smooth start, a date they can count on),
  not as a warning. The prospect should finish reading feeling looked after and
  ready to say yes.

NO EM DASHES anywhere in the proposal. Use commas, colons, parentheses, or
separate sentences.

## Step 5 — Hand it over + name the connected upgrade

Tell the owner what you wrote and where the file is. Point out one or two
phrases you kept in their own voice so they see it is theirs, and flag any spot
you left for them to fill (a date, a name, a number you did not have).

Then name where this can go next, as an outcome, without making any of it a
requirement:

> This proposal is ready to send as is, today. When your customer system is
> connected, I can also turn this exact proposal into your live signing
> template, so the next time you win a job like this it goes out, gets opened,
> and comes back signed without you rebuilding it each time. No rush; this
> document stands on its own right now.

That upgrade is a described outcome, not a step you take here. This skill's win
is the finished `.docx` in the owner's hands.

---

# Mode B — Tender / technical section (methodology, approach, capability)

This is the path for a technical-services firm answering a tender or RFP, where
the deliverable is a **methodology / technical-approach / capability section**
that is graded on how the firm will do the work and why it is the right firm,
not a price-first pitch. Price, where it exists at all, usually sits in a
separate schedule the tender asks for elsewhere. [name]'s case: an
environmental / engineering firm whose tender sections are scored on approach
and capability, with the commercials submitted separately. Run this mode when
the owner is answering a tender, or explicitly wants a technical / methodology /
capability section rather than a priced proposal.

## B1 — Gather the inputs

A tender section stands on three things: **what the tender is asking for**, the
**owner's real approach and capability**, and **how the owner sounds**.

1. **The tender / RFP requirement.** What section the owner is answering and the
   criteria it is graded against (the methodology asked for, the evaluation
   criteria, any word or page limit, any mandatory headings the tender
   prescribes). If the owner pastes the relevant part of the tender, structure
   your section to answer it point for point. Never invent a criterion or a
   requirement the tender did not state.
2. **The owner's approach and capability, in their words.** How they actually do
   this work: their method and the stages, the standards or codes they work to,
   their relevant experience and past projects, the team and qualifications,
   the equipment or systems. Capture their real specifics. Never invent a
   credential, an accreditation, a standard met, a past project, or a
   capability the owner did not give you. A fabricated capability in a tender is
   worse than a missing one.
3. **The brand voice.** As in Mode A: read their `voice.md` or first-brand brief
   if they have one; otherwise write in a clear, credible, professional
   technical register and reflect the owner's own phrasing.

## B2 — Lay out the section in chat first

Show the owner the section as an outline so they can correct it cheaply. The
shape follows the tender's criteria; a typical methodology / capability section
runs:

1. **Understanding of the requirement** — reflect back what the tender is asking
   for and the outcome it is buying, in the tender's own terms, so the evaluator
   sees the firm has read it closely.
2. **Methodology / technical approach** — how the firm will carry out the work,
   stage by stage, tied to the standards, codes, or methods they actually work
   to. This is the heart of the score: be specific and sequenced.
3. **Deliverables and stages** — what the firm produces at each stage and when.
   A **`table`** block fits well here: stages or deliverables down the rows,
   with what each produces and the timing.
4. **Capability and experience** — the team, qualifications, accreditations,
   relevant past projects, and equipment that show the firm can deliver. Only
   what the owner confirmed.
5. **Compliance / criteria response** — where the tender lists evaluation
   criteria, answer each one explicitly. A **`table`** block (criterion in one
   column, how the firm meets it in the next) makes the response easy to score.
6. **Quality and assurance** — how the firm assures quality, safety, and risk on
   this kind of work, in the owner's real practice.

Confirm the outline, and especially the criteria mapping and any claimed
capability, before generating the file. Where the tender prescribes mandatory
headings, follow them.

## B3 — Write the section to a real .docx (use the table block for criteria / deliverables)

Generate the section with the keyless document writer, the same `doclib` write
path as Mode A. Use **`table`** blocks for the deliverables / stages grid and
the criteria-response grid, so an evaluator can score the response at a glance:

```bash
python ~/.claude/bos-run.py tool write_docx --out "Tender - <Project> - methodology.docx" --blocks '[
  {"type":"heading","text":"Understanding of the requirement","level":2},
  {"type":"paragraph","text":"<reflect the tender requirement back in its terms>"},
  {"type":"heading","text":"Methodology and technical approach","level":2},
  {"type":"paragraph","text":"<the staged approach, tied to the standards the owner works to>"},
  {"type":"heading","text":"Deliverables and stages","level":2},
  {"type":"table",
   "header":["Stage","Deliverable","Timing"],
   "rows":[["<stage 1>","<what it produces>","<when>"],
           ["<stage 2>","<what it produces>","<when>"]]},
  {"type":"heading","text":"Capability and experience","level":2},
  {"type":"bullet","text":"<confirmed credential / past project / team capability>"},
  {"type":"heading","text":"Response to the evaluation criteria","level":2},
  {"type":"table",
   "header":["Criterion","How we meet it"],
   "rows":[["<criterion 1>","<how the firm meets it>"],
           ["<criterion 2>","<how the firm meets it>"]]}
]'
```

Carry the owner's real method, standards, credentials, and projects into the
section verbatim; flag any genuine gap as a clearly labelled placeholder (e.g.
`[confirm: ISO accreditation number]`) rather than a guess, and list what is
outstanding when you hand it over. If the document writer reports it is missing
a piece, offer the one-time setup in plain language and run it on a yes, then
retry; never hand the owner a command.

## B4 — Before you output anything customer-facing: positive/outcome-led, and NO em dashes

A tender section is read by an evaluator, so the content rule applies, in its
technical register:

- **Lead with capability and approach, framed as what the client gets.** A
  tender section is credible and confident: it names how the firm delivers and
  the outcome the client receives, never the rival's weakness or the firm's own
  gaps. State the method and the proof, not a complaint about the brief.
- **Never invent a credential, standard, accreditation, or past project.**
  Anchor every capability claim in what the owner confirmed. A fabricated claim
  in a tender is a disqualifier.
- **NO em dashes anywhere in the section.** Use colons, commas, parentheses, or
  separate sentences. (A field test caught this being missed; check the output.)

## B5 — Hand it over

Tell the owner what you wrote and where the file is. Point out where you mapped
the section to the tender's criteria, flag any `[confirm: …]` placeholders still
open, and note that price (if the tender asks for it) belongs in the separate
schedule the tender prescribes, not in this section. The win is the finished
technical section in the owner's hands, ready to drop into their tender
response.

---

## Hard rules (both modes)

- **Pick the mode first.** Mode A (priced proposal) is the default; Mode B
  (tender / technical section) only when the owner is answering a tender / RFP
  or explicitly wants a methodology / approach / capability section. Ask one
  plain question if it isn't obvious.
- **One proposal (or one tender section) per run.** Write the first one
  properly; offer the rest as fresh runs.
- **Never invent the price, the scope, the terms, or a capability.** In Mode A
  the price comes from the priced scope: if the owner states a price, take it
  and skip the pricing detour; only offer `price-my-work` when there is no
  number at all. Scope / timeline / terms come from the owner. In Mode B, never
  invent a
  credential, accreditation, standard met, past project, or tender criterion.
  Ask one plain question for anything missing, or flag it as a `[confirm: …]`
  placeholder, rather than guessing.
- **Confirm the outline before generating the file:** especially the price, the
  timeline, and the terms (Mode A), or the criteria mapping and any claimed
  capability (Mode B). The outline is cheap to change; a wrong number or a false
  claim in a submitted document is not.
- **Always emit the deliverable as a real `.docx`** through
  `tools/write_docx.py`. Use the **`table`** block for the priced breakdown
  (Mode A) and for the deliverables / criteria grids (Mode B), so line items and
  criteria render as a real grid rather than bullets with `$____`. The file is
  the win; do not stop at a chat draft when the owner wants the document.
- **Before you output anything customer-facing: positive-only, outcome-led, and
  no em dashes** (use colons, commas, parentheses, or separate sentences). Every
  section names the result the client is buying (Mode A) or how the firm
  delivers (Mode B). Naming the prospect's problem while gathering inputs is
  fine; that is discovery, not the shipped document.
- **Reflect the owner's voice.** If they have a voice doc, match it; otherwise
  keep their own phrasing for the load-bearing lines.
- **The connected signing template is a described outcome, in plain words.**
  Never name the tool, script, or service that would do it; describe the win
  ("turn this into your live signing template once your system is connected")
  and stop there.

## Output shape

A confirmed section outline first, then the running narration of the
`write_docx.py` call, then the hand-over: where the file is, the one or two
phrases kept in the owner's voice, any spots left to fill, and (Mode A) the
plain-words pointer to the live signing template once a customer system is
connected, or (Mode B) where the section maps to the tender's criteria and the
note that price belongs in the tender's separate schedule.

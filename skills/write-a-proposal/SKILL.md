---
name: Write A Proposal
description: Turn a priced scope and the owner's brand voice into the proposal that wins the job — an on-brand proposal or statement of work in the owner's voice, written out as a real .docx they can send. Consumes a priced breakdown (from price-my-work or typed in) plus their voice doc, and lays out cover, understanding of the need, scope and deliverables, the priced breakdown, timeline, terms, and the next step. Keyless, works from what you have day one. One proposal per run.
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

## Step 1 — Gather the two inputs

A proposal stands on two things: **what the work is and what it costs** (the
priced scope) and **how the owner sounds** (the voice). Take in both, and ask
only for what is genuinely missing.

1. **The priced scope.** Ideally a priced breakdown from `price-my-work`: the
   line items, the margin, the total, the assumptions. If the owner pastes or
   types their own scope and price, take that. If there is no priced number at
   all, the cleanest move is to run `price-my-work` first so the proposal rests
   on a number the owner can stand behind, then come back here. Do not invent a
   price or pad the scope with work the owner did not name.
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
[`tools/write_docx.py`](../../tools/write_docx.py) — see
[`knowledge/document-tools-method.md`](../../knowledge/document-tools-method.md)).
Build the proposal as an ordered list of blocks (`heading`, `paragraph`,
`bullet`) and pass them as JSON:

```bash
python tools/write_docx.py --out "Proposal - <Prospect> - <job>.docx" --blocks '[
  {"type":"heading","text":"Proposal for <Prospect>","level":1},
  {"type":"paragraph","text":"<warm intro that names the outcome they want>"},
  {"type":"heading","text":"Understanding your need","level":2},
  {"type":"paragraph","text":"<reflect their goal back in their words>"},
  {"type":"heading","text":"Scope and deliverables","level":2},
  {"type":"bullet","text":"<deliverable 1>"},
  {"type":"bullet","text":"<deliverable 2>"},
  {"type":"heading","text":"Your investment","level":2},
  {"type":"paragraph","text":"<the priced breakdown and the basis for it>"},
  {"type":"heading","text":"Timeline","level":2},
  {"type":"paragraph","text":"<start, milestones, finish>"},
  {"type":"heading","text":"Terms","level":2},
  {"type":"paragraph","text":"<deposit, payment, inclusions, validity>"},
  {"type":"heading","text":"The next step","level":2},
  {"type":"paragraph","text":"<one clear positive call to action>"}
]'
```

You can also pipe the JSON in on stdin if it is long. If the wrapper reports
that `python-docx` is not installed, relay its one-line install hint
(`pip install python-docx`) and stop until it is installed. If the write fails,
show the error plainly rather than pretending a file exists. Use a clear file
name that names the prospect and the job so the owner can find it later.

## Step 4 — Positive-only, outcome-led, no em dashes (hard requirement)

The proposal is **customer-facing output**, so it obeys the positive-only
rule: every section names what the prospect gets, what success looks like, and
the result they are buying. The value is the outcome, never the pain or what is
missing.

- Don't write: "stop losing time to the wrong contractor", "no more unfinished
  jobs", "you are frustrated with your current setup", "tired of overruns".
- Do write: outcome-led lines — "your kitchen finished on time and on budget,
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

## Hard rules

- **One proposal per run.** Write the first one properly; offer the rest as
  fresh runs.
- **Never invent the price, the scope, or the terms.** The price comes from the
  priced scope (run `price-my-work` if there is none). Scope, timeline, and
  terms come from the owner. Ask one plain question for anything missing rather
  than guessing.
- **Confirm the outline before generating the file** — especially the price,
  the timeline, and the terms. The outline is cheap to change; a wrong number
  in a sent proposal is not.
- **Always emit the proposal as a real `.docx`** through
  `tools/write_docx.py`. The file is the win; do not stop at a chat draft when
  the owner wants the document.
- **Customer-facing output is positive-only and outcome-led; no em dashes.**
  Every section names the result the prospect is buying. (Naming the prospect's
  problem while gathering inputs is fine; that is discovery, not the shipped
  proposal.)
- **Reflect the owner's voice.** If they have a voice doc, match it; otherwise
  keep their own phrasing for the load-bearing lines.
- **The connected signing template is a described outcome, in plain words.**
  Never name the tool, script, or service that would do it; describe the win
  ("turn this into your live signing template once your system is connected")
  and stop there.

## Output shape

A confirmed section outline first, then the running narration of the
`write_docx.py` call, then the hand-over: where the file is, the one or two
phrases kept in the owner's voice, any spots left to fill, and the plain-words
pointer to the live signing template once a customer system is connected.

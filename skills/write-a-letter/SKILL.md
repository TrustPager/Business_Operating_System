---
name: Write A Letter
description: Turn what happened, in the owner's own words, into a firm, professional letter in their voice: a variation notice, a dispute response, a payment-terms letter, a formal reply that holds the line and stays factual. Works keylessly day one from what the owner tells you plus any voice docs they paste. Can be handed back as plain text or written out as a real .docx. One letter per run.
triggers:
  - write a letter
  - write a formal letter
  - draft a dispute response
  - respond to this complaint
  - write a variation notice
  - reply to this dispute
  - draft a firm letter
  - write a payment letter
  - answer this letter for me
  - letter in my voice
function_slot: comms
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---

# Write A Letter

You turn what actually happened into a firm, professional letter in the
owner's own voice: a variation notice, a dispute response, a reply to a
complaint, a payment-terms letter, a formal answer that holds the line. The
owner tells you the situation in their own words; you give it the structure,
the calm authority, and the wording that stands up. You never invent a fact,
a figure, a date, or a contractual term they did not give you.

This runs keylessly day one: no accounts, no files beyond what the owner tells
you or pastes. The only inputs are the owner's account of what happened and
any voice or brand material they hand over.

If the owner has already built a brand voice (a `voice.md` or first-brand
brief from `build-brand-strategy`), read it first so the letter matches their
register. Read [`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md)
for what that voice doc carries. If there is no voice doc, write in a warm,
plain, professional register and reflect the owner's own phrasing back.

## Bounded: one letter per run

One letter per run. If the owner has several to send (several disputes,
several variation notices), write the first one properly, then offer the next
as a fresh run. A focused letter that lands beats a stack of half-built ones.

## Step 1 — Get the situation, in their words

Ask the owner to lay out what happened and what they want the letter to do.
Plain discovery, matched to the kind of letter:

- **What it is.** A variation notice, a dispute response, a reply to a
  complaint, a payment-terms or overdue-account letter, or another formal
  reply. Name it so you write the right shape.
- **Who it's to.** The recipient (a client, a contractor, a supplier) and
  any reference they should quote (an invoice number, a contract clause, a
  job reference) exactly as the owner gives it.
- **The facts that carry the letter.** The dates, the amounts, what was
  agreed, what changed, what was delivered, what is outstanding. Capture the
  owner's exact figures and dates: these are the load-bearing facts and you
  never round or invent them.
- **The outcome the owner wants.** What a good result looks like: the
  variation accepted and priced, the dispute resolved, the invoice paid by a
  date, the relationship kept intact. The letter is firm in service of that
  result.

It is fine to name the friction plainly in *this discovery chat*: "tell me
what they're disputing and where they've got it wrong" is a normal question.
The shipped letter stays firm and factual (Step 3), not heated.

## Step 2 — A firm letter is firm AND factual (the register)

A dispute or variation letter is the one place this floor's positive-only
rule meets its match: the letter can, and should, hold the line. Firm does
not mean angry, and factual does not mean cold. The register is:

- **Calm, specific, and grounded in fact.** State what happened, what was
  agreed, and what you are asking for, each tied to a real date, figure, or
  reference. Specifics are what make a firm letter land.
- **Professional, never heated.** No insults, no sarcasm, no threats the
  owner has not authorised. A letter that stays measured reads as the
  stronger position, and keeps the door open to a good outcome.
- **Clear on the ask and the next step.** Say plainly what you want to
  happen and by when (accept the variation, settle the account by a date,
  respond by a date), and what happens next if it does.

Hold the line on the facts; keep the tone the owner could stand behind if the
letter were read back to them in a room. Never invent a legal threat, a
penalty, a clause, or a consequence the owner did not state.

## Step 3 — Before you output anything customer-facing: positive/outcome-led, and NO em dashes

This letter goes to a real recipient, so the customer-facing content rule
applies, adapted for a firm letter:

- **Lead toward the outcome.** Even a dispute response names the resolution
  it is reaching for: the variation agreed and the job moving, the account
  cleared and the relationship continuing, the matter closed cleanly. The
  letter is firm about the facts and positive about the destination, never a
  list of grievances.
- A firm letter MAY state a fact plainly that names a shortfall (an unpaid
  invoice, work outside the agreed scope), because that is the factual spine
  of the letter. State it as the path to the resolution you want, not as an
  attack. This is the labelled exception to the pure positive-only rule: the
  facts are stated, the framing still points at a good outcome.
- **NO em dashes anywhere in the letter.** Use commas, colons, parentheses,
  or separate sentences. (This is a hard rule a field test caught being
  missed; check the output before handing it over.)

## Step 4 — Draft the letter

Write the letter in the owner's register (use their voice doc if you read
one). A clean professional shape:

1. **Heading / reference line** (date, recipient, the reference to quote).
2. **Opening** that names what the letter is about in one plain sentence.
3. **The body**, the facts in order, each tied to its date / figure /
   reference, building to what the owner is asking for.
4. **The ask and the next step**, stated plainly with any date.
5. **A professional sign-off** in the owner's name.

Keep the owner's exact figures, dates, and references verbatim. If a needed
specific is missing, write the letter with a clearly flagged placeholder
(e.g. `[confirm: invoice number]`) rather than a guess, and list what is
outstanding when you hand it over.

## Step 5 — Hand it over (text, or a real .docx)

Show the finished letter as text first so the owner can read and adjust it
cheaply. Point out one or two phrases you kept in their own words, and list
any `[confirm: …]` placeholders still open.

The keyless default is the letter as text the owner can paste into an email or
their letterhead. If the owner wants a sendable file, you can also write it out
as a real `.docx` with the keyless document writer (the `doclib` write path,
[`tools/write_docx.py`](../../tools/write_docx.py), see
[`knowledge/document-tools-method.md`](../../knowledge/document-tools-method.md)),
built from `heading` / `paragraph` blocks:

```bash
python "${CLAUDE_PLUGIN_ROOT}/tools/write_docx.py" --out "Letter - <Recipient> - <subject>.docx" --blocks '[
  {"type":"heading","text":"<subject / reference line>","level":2},
  {"type":"paragraph","text":"<opening sentence>"},
  {"type":"paragraph","text":"<the facts in order>"},
  {"type":"paragraph","text":"<the ask and the next step, with the date>"},
  {"type":"paragraph","text":"<sign-off in the owner’s name>"}
]'
```

The `.docx` is an optional convenience, not the floor: the letter text is the
win and stands on its own. If the document writer reports it is missing a
piece, the assistant offers the one-time setup in plain language and runs it
on a yes (the detect, offer, install-on-yes, verify loop in
[`knowledge/document-tools-method.md`](../../knowledge/document-tools-method.md)).
Never hand the owner a command.

## Hard rules

- **One letter per run.** Write the first one properly; offer the rest as
  fresh runs.
- **Never invent a fact, figure, date, reference, clause, penalty, or legal
  threat the owner did not give you.** Keep their exact figures and dates
  verbatim; flag genuine gaps as `[confirm: …]` placeholders.
- **Firm AND factual.** The letter holds the line on the facts and stays
  measured and professional: no insults, sarcasm, or unauthorised threats.
- **Before you output anything customer-facing: outcome-led where you can be,
  and NO em dashes** (use commas, colons, parentheses, or separate
  sentences). A firm letter may state a shortfall as a plain fact (the
  labelled exception), but the framing still points at the resolution.
- **Reflect the owner's voice.** If they have a voice doc, match it;
  otherwise keep their own phrasing for the load-bearing lines.
- **The .docx is optional.** Hand back text by default; write the file only
  when the owner wants a sendable document.

## Output shape

The finished letter in the owner's register (firm, factual, outcome-led, no em
dashes), then a short hand-over: the one or two phrases kept in their own
words, any `[confirm: …]` placeholders still open, and the offer to write it
out as a real `.docx` if they want a sendable file.

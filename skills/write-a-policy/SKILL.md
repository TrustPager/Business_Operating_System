---
name: Write A Policy
description: Turn how you actually handle something (deposits, cancellations, refunds, privacy, or a funding/eligibility explainer) into clean, on-brand policy or FAQ text ready for your website, emails, or staff. Keyless, works from your own words. For anything compliance-sensitive it confirms specifics first and never invents a legal claim. One topic per run.
triggers:
  - write a policy
  - write our cancellation policy
  - draft a deposit policy
  - write a refund policy
  - draft our privacy policy
  - write an FAQ for this
  - explain our funding eligibility
  - turn how we handle this into policy text
  - write the policy for my website
function_slot: people
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---

# Write A Policy

You turn how an owner *actually* handles something into policy or FAQ text
that sounds like them and is ready to paste onto their site, into an email,
or into a staff handbook. The owner describes the real practice in their own
words; you give it clean structure and a warm, plain register. You never
invent a rule they didn't state, and you never invent a legal or compliance
claim.

This runs keylessly day one: no accounts, no files beyond what the owner
tells you or pastes. The only inputs are the owner's description and any
voice or brand material they hand over.

If the owner has already built a brand voice (a `voice.md` or first-brand
brief from `build-brand-strategy`), read it first so the policy matches their
register. Read [`knowledge/marketing-strategy-method.md`](../../knowledge/marketing-strategy-method.md)
for what that voice doc contains. The CRM auto-queue and AI-Knowledge layers
described there are connected-tier extras, NOT a dependency for this app: it
produces the policy text with zero connections.

## Bounded: one topic per run

One policy or FAQ topic per run: deposits, OR cancellations, OR refunds, OR
privacy, OR a funding / eligibility explainer. If the owner asks for several
at once, write the first cleanly, then offer the next as a fresh run. A
focused, correct policy beats a sprawling combined one nobody trusts.

## Step 1 — Find out how they actually handle it

Ask the owner to describe the real practice, not the ideal one. Plain
discovery questions, matched to the topic:

- **Deposits**: how much (fixed sum or percentage), when it's taken, what
  it secures, and whether it comes off the final bill.
- **Cancellations**: the notice window, what happens inside vs outside it,
  and any fee or forfeit.
- **Refunds**: when a refund applies, how it's worked out, the method, and
  the timeframe.
- **Privacy**: what information they collect, why, who it's shared with (if
  anyone), and how someone asks to see or remove it. (Compliance-sensitive,
  see Step 2.)
- **Funding / eligibility explainer** (e.g. NDIS, Medicare, a grant): who
  qualifies, what's covered, what the client pays vs what the funder pays,
  and what they need to bring or provide. (Compliance-sensitive, see Step 2.)

It is fine to name the friction in *this discovery chat*. "Tell me about the
no-shows that cost you" is a normal question. The shipped policy stays
positive (Step 4). Capture their exact phrasing for the numbers, windows, and
conditions: those are the load-bearing facts.

## Step 2 — Confirm the specifics for compliance-sensitive topics

For **privacy** and **funding / eligibility** (NDIS, Medicare, grants,
allied-health rebates), the cost of a confident wrong fact is high. Before
writing a single line:

1. **Read back the specifics** the owner gave and confirm them explicitly:
   the funder name, the covered items, the dollar splits, the eligibility
   rule. "You said NDIS plan-managed clients pay nothing at point of service
   and you invoice the plan manager, is that right?"
2. **Never invent or infer a legal / compliance claim.** If the owner didn't
   state a rule, you do not supply one. No invented privacy-law citations, no
   guessed funding caps, no assumed eligibility criteria.
3. **Mark genuine gaps as gaps.** If a needed specific is missing, write the
   policy with a clearly flagged placeholder (e.g.
   `[confirm: refund timeframe]`) rather than a guess, and list what's
   outstanding when you hand it over.
4. **Add a plain pointer to the authority, not a claim.** Where a rule is
   governed by an external body, point the reader to the source in the
   owner's words ("for the current NDIS price limits, see your plan manager")
   rather than stating a figure you can't verify.

For non-sensitive topics (deposits, cancellations, refunds for ordinary
goods/services), still read back the numbers before writing. The
high-confidence-confirmation gate above is mandatory for privacy and funding.

## Step 3 — Draft the policy or FAQ

Pick the shape that fits how they'll use it:

- **Policy block**: a short titled section (one heading, two to five tight
  paragraphs or a few bullet points) for a website page, terms section, or
  staff handbook.
- **FAQ**: three to seven question-and-answer pairs in the customer's real
  questions ("Do I need to pay a deposit?", "What if I need to
  reschedule?"), each answer one to three sentences.

Write in the owner's register (use their voice doc if you read one). Keep it
plain: a customer reads it once and knows exactly where they stand. State the
real numbers, windows, and conditions from Step 1 verbatim. Don't soften a
fee they were clear about or round a figure.

If what the owner actually needs is an internal SOP (how the team does a task,
for staff) rather than a customer-facing policy, shape it per
`business-method.md` §12.1: write it while doing the task (or from the owner
walking through a real run of it), expect it to get a competent person to ~80%
of the owner's outcome (directional) rather than scripting every judgment call,
and note that it gets updated whenever reality beats the checklist.

## Step 4 — Positive-only, outcome-led (hard requirement)

The policy is **customer-facing output**, so it obeys the positive-only rule:
frame the policy around what the customer gets and what good looks like, not
around the owner's frustration or the customer's failure.

- Don't write: "Cancellations cost us money, so if you fail to give notice
  you'll be penalised", "no-shows are unfair to our staff", "we're tired of
  late changes".
- Do write: "To keep your spot held and our schedule running smoothly, let us
  know at least 24 hours ahead and we'll happily move your booking", "Your
  deposit secures your date and comes straight off your final invoice."
- A fee or condition can still be stated plainly and positively: name the
  rule as the path to a good outcome, not as a punishment. The customer
  should finish reading feeling informed and looked after.

NO EM DASHES in the output. Use commas, colons, parentheses, or separate
sentences.

## Step 5 — Hand it over + offer the next step

Show the finished policy / FAQ, point out one or two phrases you kept in their
own words, and list any flagged placeholders still needing a real specific.

**Add the plain review line (especially for anything compliance-sensitive).**
This is policy text that may go on a website or bind how the business handles
money, privacy, or funding, so hand it over as a starting draft, not a final
legal document:

> This is a solid starting draft. Give it a read before you publish it, and if
> it touches anything regulated (privacy, funding, refunds), it's worth a
> quick look from whoever signs off on that for you. The wording's yours to
> tweak.

Keep it warm and plain, never alarming: it sets the right expectation without
undercutting the work. For privacy and funding / eligibility topics the line is
not optional.

Then offer where it can go next, without making any of it a requirement:

> This is ready to paste onto your site, drop into a confirmation email, or
> hand to your team. When you've got a workspace connected, I can also load it
> into your AI Knowledge so your in-app assistant and voice agents answer from
> this exact policy (that's the build-knowledge-base-from-docs step). No rush;
> the text stands on its own today.

## Hard rules
- **Before you output anything customer-facing: positive/outcome-led, and NO em
  dashes** (use colons, commas, parentheses, or separate sentences). The policy
  or FAQ names what the customer gets and what good looks like, never the
  owner's frustration. A field test shipped a quote with an em dash because
  nothing reminded the model; this is the reminder, check the output.
- Never invent a rule, number, window, or condition the owner didn't state.
- Never invent a legal or compliance claim: no guessed privacy-law citations,
  no assumed NDIS / Medicare figures or eligibility criteria.
- Don't ship a compliance-sensitive policy (privacy, funding/eligibility)
  without reading the specifics back and getting an explicit confirmation.
- Hand every policy over as a **starting draft with a plain "give it a read
  before you publish" line** (Step 5); for privacy and funding / eligibility
  topics that review line is mandatory.
- Don't write more than one policy / FAQ topic in a single run.
- Keep the owner's exact phrasing for the load-bearing facts; reflect their
  voice.
- Customer-facing output is positive-only and outcome-led; no em dashes.
- Flag genuine gaps as `[confirm: …]` placeholders rather than guessing.

## Output shape
The finished policy block or FAQ in the owner's register, then a short
hand-over: the one or two phrases kept verbatim, any `[confirm: …]`
placeholders still open, and the optional pointer to loading it into AI
Knowledge once a workspace is connected.

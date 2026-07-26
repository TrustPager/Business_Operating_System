# Content rules

**The small set of quality and integrity guardrails for any copy this system generates
that a customer or end-user will read or hear.** Emails, SMS, captions, ad copy, web
copy, headlines, scripts, proposals, letters. One home: every content skill points here
instead of restating it.

**Whose voice, and where it lives:** the copy is written in the OWNER's brand voice.
That voice is a file, not a vibe:

- **`marketing-strategy/<BrandName>/voice.md`** is the one home for the owner's writing
  voice (tone adjectives, signature moves, vocabulary, the watch-out-for register),
  written by `build-my-voice` or `build-brand-strategy`. Every skill writing marketing
  or engagement copy reads it. When it does not exist, say plainly that no voice doc was
  found and write from the owner's own words, rather than inventing a voice for them.
- **`knowledge/communication-voice.md`** is the register for the owner's operational
  service messages (confirmations, updates, replies). Plain, warm, short. It is not the
  marketing register: a service reply written with a marketing hook reads wrong, and a
  video hook written in the service register lands flat.
- **`brand/brand.json` is identity, not voice** (name, tagline, colours, fonts). A skill
  that asks it how the owner sounds is pointed at the wrong file.

These rules are universal quality and integrity guardrails, not a house style. The
framing and the marketing psychology are the owner's choice.

**Scope (labelled boundary):** these rules bind customer-facing OUTPUT only. Internal
worksheets, operator coaching, discovery conversations, and dev notes are exempt.

## 1. No em dashes
Never use an em dash in customer-facing copy. Em dashes read as machine-written and are
one of the clearest tells of AI-generated text, which weakens the copy. Break the thought
into separate sentences, or use a comma, a colon, or parentheses. Hyphens in compound
words are fine; the ban is the em dash used as a sentence connector.

## 2. Never invent evidence
Never fabricate a number, statistic, testimonial, customer quote, or metric. Use only real
figures the owner supplied and real customer words. A missing number is a finding, not a
gap to fill with a plausible one. Where the stakes are regulatory (tax, financial,
medical), a made-up figure is never acceptable.

## 3. No third-party vendor leak
Do not inject the tools or platforms behind the work (the CRM, the ad platform, the site
host) into the owner's customer-facing copy unprompted. The copy is the owner's brand. The
owner naming vendors THEY choose is their call; this rule is about not leaking our stack
into their output.

## 4. Regulated shapes have extra limits
For regulated business shapes (clinic / appointment and finance / mortgage broking, plus
insurance and legal), copy must clear tighter compliance limits than the rules above:
no outcome testimonials or before/after result claims in owned channels, no result
guarantees (service-level only), and no urgency or price pressure on clinical or advice
decisions. Sell the logistics and the care, never the treatment outcome. One-rule-one-home:
the canonical per-shape overrides live in [`knowledge/industry-notes.md`](industry-notes.md)
(the Clinic / appointment and Service / professional shapes) with the diagnosis-level
summary in `knowledge/business-method.md` §7.2 and §15. Any content skill working for a
regulated shape reads those before drafting.

## Service-message voice
For the owner's operational messages to their own customers (fix confirmations, updates),
keep it plain, warm, and clear: see knowledge/communication-voice.md.

## The content-skill contract
Two obligations, and a skill declares which apply to it in its own frontmatter:

1. **Every skill that writes customer-facing copy names its voice source inline**
   (`marketing-strategy/<BrandName>/voice.md` for marketing and engagement copy,
   `knowledge/communication-voice.md` for service messages). A skill flagged
   `produces_customer_facing_copy: true` that names neither is writing in a voice it
   never read. Naming the file inline is deliberate: a rule that is only referenced in
   another document gets skipped mid-generation, and the cost is a customer seeing it.
2. **Every skill that writes engagement copy routes the attention craft.** Engagement
   copy is anything whose job is to earn and hold attention: a video script, a social
   post, ad copy, a nurture sequence, a content plan. Those skills carry
   `engagement_copy: true` and read [`storytelling-method.md`](storytelling-method.md)
   for the hook, the curiosity loop, and the but/therefore dance. Functional documents
   (a policy, a proposal, a letter, a job ad) get voice and clarity, not a curiosity
   hook. Operational service messages get the service register, not a hook either.

**Ruled 2026-07-26: a reply to a customer is not marketing.** The skills that answer
an enquiry, chase a missed call, or send a quote deliberately do NOT carry
`engagement_copy`, even though "emails and replies" could be read as engagement
content. A customer who asks what a job costs is best served by the price and the
next available day, not by a curiosity gap. If a later change wants to add the hook
craft to those skills, it is reversing this ruling, not filling a gap.

`tools/lint-skill.py` checks both: the voice-source half as a warning, the
storytelling half as a failure on any skill that declares `engagement_copy: true`.
CI lints every skill under `set -e`, so a warning stops the build too. In practice
both halves gate; the severity difference only changes how a local run reads.

## Marketing framing is the owner's choice
How the owner frames their marketing (positive, pain-led, or any psychology they choose)
is the owner's decision. This system writes in the owner's voice and does not impose a
house style on their copy.

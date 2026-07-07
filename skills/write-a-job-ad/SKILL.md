---
name: Write A Job Ad
description: Turn a role and its must-haves into a ready-to-post job ad written in the owner's voice, plus a short set of screening questions that filter applicants before anyone reads a resume. Works keylessly from what the owner tells you (plus optional brand/voice docs and a website), one role per run. The before-hire companion to onboard-team-member, which sets up the person once they're hired.
triggers:
  - write a job ad
  - help me hire
  - draft a job posting
  - write a job description
  - i need to hire someone
  - screening questions for applicants
  - post a role
  - advertise a position
function_slot: people
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
produces_customer_facing_copy: true
---

# Write A Job Ad

Hiring well starts before the first applicant: a clear, attractive ad that sounds
like the business (not a generic template) and a short set of screening questions
that surface the right people early. This skill turns a role and its must-haves
into both, in the owner's own voice, in a couple of minutes and with zero
accounts.

It runs keylessly from what the owner tells you. If brand or voice docs exist,
you slot in so the ad sounds exactly like their other content, but those docs are
never required. One role per run: this skill writes a single job ad and its
screening set, not a whole hiring plan.

This is the **before-hire** companion to `/onboard-team-member`. This skill gets
the right person in the door; once they're hired, `onboard-team-member` sets up
their standards and role boundaries. Point to it as the natural next step at the
end (see Step 5), but don't run it here.

## Step 1: Gather the role + must-haves

You need enough to write something sharp, not a long form. Get these in one short
message if the owner didn't already supply them:

- **The role.** Title and a one-line sense of what this person does day to day
  (for example "front-desk + bookings for a physio clinic", "apprentice
  electrician").
- **The result this role owns.** One sentence on what "done well" looks like in
  90 days (a role is defined by its result, business-method.md §12.4). This
  feeds the "About the role" paragraph so the ad sells an outcome, not a duty
  list.
- **Must-haves.** The few things a candidate genuinely needs (licences, hours,
  location, a non-negotiable skill). Keep this to what truly disqualifies if it's
  missing; nice-to-haves go in a separate, softer list.
- **The shape of the job.** Full-time, part-time or casual, location or remote,
  and the start timing if it matters.
- **What makes it a good job here.** Pay range if they'll share it, the team, the
  work itself, what someone would enjoy about it. This is the raw material for
  the attractive part of the ad. If the owner is settling pay, one advisory note
  for their eyes: top-of-market for one strong hire beats underpaying for three
  (business-method.md §12.2), and a comp structure that underpays is one of the
  classic stuck-points (§3). The ad itself never mentions any of this; it
  carries the number the owner lands on.

It's fine for the owner to name their frustration with hiring or the gap they're
filling. That's discovery, and it helps you understand the role. If a must-have
or two is genuinely missing and the ad would be hollow without it, ask one
targeted question rather than padding (see Step 3's thin-input guard).

## Step 2: Pick up the owner's voice (keyless, optional)

So the ad sounds like the business and not a job-board template, reach for their
voice in this order, using only what's already available and never blocking on
it:

1. **Brand or voice docs, if present.** If the workspace has a brand strategy
   folder (for example `marketing-strategy/<BrandName>/voice.md`, `positioning.md`,
   or a `first-brand-brief.md` from `/build-brand-strategy`), read the voice doc
   for tone and the positioning doc for how they describe themselves. The method
   behind those docs is `knowledge/marketing-strategy-method.md` (Layer 3, the
   brand strategy docs); read its voice section if you need the shape. Note that
   the CRM and auto-queue layers in that method (Layer 4) are the connected tier,
   not something this keyless skill touches: you only borrow the voice.
2. **Their own website**, if they gave one. Use the `firecrawl-scrape` skill (no
   key needed) to pull how they already talk about themselves and their team. Cap
   the effort: if it's slow, blocked, or empty, fall back to what they told you
   and say so plainly.
3. **What the owner said.** Their exact phrasing about the role and the business.
   This is always available and is the primary voice source. Lift their words;
   the ad should make them think "that's how I'd put it."

If none of these exist, write in a clear, warm, plain-business voice that matches
how the owner spoke to you. Never invent brand claims or testimonials.

## Step 3: Thin-input guard

If the role plus must-haves are too thin to produce a genuinely useful ad (you'd
be padding with filler responsibilities or guessing at requirements), don't ship
a hollow ad. Say so and ask ONE targeted question that unlocks it, then build
from the answer. For example:

> I can shape this, but to make the ad pull the right people I need one thing:
> what's the single task this person will spend most of their week on?

A sharp ad built from one good answer beats a vague one built from nothing.

## Step 4: Write the job ad + screening questions

Produce two things in one response (Markdown is fine; offer to save to
`hiring/<role-slug>/job-ad.md`).

### a) The job ad, in the owner's voice

A ready-to-post ad with these parts:

1. **Title + one-line hook.** The role and a single forward-looking line on what
   someone gets to do or be part of here. Lead with your strongest line.
2. **About the role.** A short paragraph on what this person does and why it
   matters to the business, in plain language.
3. **What you'll do.** 4-6 bullets of the actual day-to-day work, framed as the
   work itself ("run the front desk and keep the day flowing", "quote jobs on
   site and send them same-day").
4. **What you'll bring.** The must-haves as clear requirements, then a short
   "nice to have" list kept separate so good candidates aren't scared off.
5. **Why you'll like working here.** The team, the work, the pay range (if the
   owner shares it), what makes this a good job. Built from Step 1's "good job"
   material and the owner's voice.
6. **How to apply.** A simple, clear instruction, and a nudge to answer the
   screening questions below so the answers arrive with the application.

### b) Screening questions, a short filter (3-5)

A small set of questions that filter applicants before anyone reads a full
resume. Each one should map to a real must-have or to fit, so the answers
actually sort people:

- **Hard filters first.** A yes/no or short-answer question per genuine must-have
  (for example "Do you hold a current open driver's licence?", "Which days and
  hours can you work?"). These let weak fits self-select out.
- **One or two fit and judgment questions.** Short open answers that reveal how
  someone thinks about the actual work (for example "Tell us about a time you
  kept calm with a busy front desk and an unhappy customer at the same time.").
  Keep these answerable in a few sentences.

Keep it to 3-5 total. For each question, add a one-line note (for the owner's
eyes only, labelled as such) on what a strong answer looks like, so they can sort
replies quickly.

## Step 5: Walk the owner through it + name the next step

Show the ad and the screening set. Point out one or two phrases you lifted
straight from them or their voice docs (so they see it's theirs), and flag any
open choice you left for them (for example "I left the pay range as a placeholder:
drop a number in and it's ready to post").

Then name the natural next step without doing it:

> When you've picked someone, `/onboard-team-member` sets them up with your
> team's standards and role boundaries from day one. No rush, that's for after
> the hire.

## Hard rules
- ❌ One role per run. If the owner names two roles, write the first and offer to
  run again for the second; don't blend them into one ad.
- ❌ Never invent brand claims, pay figures, or testimonials. If a value is
  unknown (for example pay range), leave a clearly labelled placeholder for the
  owner, don't guess a number.
- **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`.
- ✅ Reflect the owner's voice back: lift their phrasing and, if voice docs
  exist, match them. The ad should sound like their business.
- ✅ Every screening question maps to a real must-have or to fit. No filler
  questions that don't sort anyone.
- ✅ Keyless and self-contained: runs with zero accounts and zero files beyond
  what the owner provides. Web research and voice docs are optional sharpeners,
  never the entry price.
- ✅ `onboard-team-member` is the post-hire next step, named at the end. Never
  run it from inside this skill.

## Output shape
The ready-to-post job ad (title through how-to-apply) and the 3-5 screening
questions (each with a one-line "strong answer looks like" note for the owner),
then a short walk-through pointing out the voice you lifted, any placeholder left
for them, and the `/onboard-team-member` next step. If input was too thin, the
one targeted question comes first instead, then the ad.

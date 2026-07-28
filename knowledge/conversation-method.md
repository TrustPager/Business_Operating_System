# Conversation Method — how the assistant runs a long discovery conversation

The canonical craft for the conversation *itself*: how questions are paced, how a
vague or stuck owner gets unstuck, and how the talking lands in something written.
*What* to ask is not here. The intake content lives in
[`business-method.md`](business-method.md) §2 and in each skill's own steps. This
file owns how the asking is run.

Consumers that reference this file, and the countable cap each one declares (§1):

- [`start-here`](../skills/start-here/SKILL.md) — the first-run consultation, all
  six rules. Cap: roughly 8-10 exchanges with an engaged owner
  (`business-method.md` §2, "Backstop, not a target").
- [`learn-my-business`](../skills/learn-my-business/SKILL.md) — its short question
  ceiling and the graceful exit (§1). Cap: two questions, labelled as an override
  because a connected sync is not an interview (its Step 4).
- [`grill-me-on-this-decision`](../skills/grill-me-on-this-decision/SKILL.md) —
  sharpening the decision before the grilling (§1-§3, §6). Cap: the four
  sharpening questions in its Step 1.
- [`build-my-voice`](../skills/build-my-voice/SKILL.md) — the "this, not that"
  lock-in (§2, §3) and the returning owner (§6). Cap: five contrasts, its Step 2.
- [`plan-my-youtube`](../skills/plan-my-youtube/SKILL.md) — the transformation and
  point-of-view gate only (§2-§5), which is a real discovery conversation. The rest
  of that skill is planning, not asking. Cap: the gate's own two-question ceiling.

When in doubt, this file wins over instinct. Instinct says "keep asking, I might
learn something else". The method says "a conversation that never lands is a
failure, however good the questions were".

> Source note (dev-facing): mostly a consolidation, not new doctrine. Most of
> this was being run out of `start-here`'s body and was moved here so the discovery
> skills share one home. What is genuinely new: the graceful exit at the cap, the ban on
> standalone affirmations, the sharpen pass, and paste detection. Scope: the
> consumers listed above, and only those. `five-day-challenge` Day 2's goal gate runs its
> own single warm pass on a brush-off answer and is deliberately NOT wired here;
> nor are the other discovery skills. Do not read this file as governing them.

**What this file owns, and what it only routes.** Where a rule already has a home,
this file points at it and does not restate it.

| Rule | It owns | It routes to |
|---|---|---|
| §1 Turn budget | that each consumer above declares a countable backstop, and the graceful exit taken at it | the engagement gauge, `start-here` Step 6b; the backstop number, `business-method.md` §2 |
| §2 Depth detection | the switch from an open question to concrete options, and the tap-not-type move | who reads as terse versus engaged, the gauge in `start-here` Step 6b |
| §3 Reflect before asking | the trust moves per question, one ask per turn, and the ban on standalone affirmations | the recommendation-follows-the-give rule, `business-method.md` §2 |
| §4 Sharpen pass | walking every field of an artifact against a pass/fail test before it ships | the rubrics themselves, `business-method.md` §7.0 and §14, `prompt-writing-method.md` |
| §5 Stuck exit | the three ways in, offered once, then a labelled best guess | never-invent and the labelled working goal, `business-method.md` §2.1 and `start-here` Step 9 |
| §6 Returning owner | recognising a pasted prior artifact and switching to refinement | the cold-start marker gate, `start-here` Step 1, and each writing skill's never-clobber rule |

---

## 1. Turn budget — a runaway session is a failure state

Each consumer listed at the top of this file declares its own backstop in its own
body, as **a number a run can count while it runs** (exchanges, questions, or
contrasts). This file requires that the cap has a number and that it is honoured.
A cap phrased as "the fewest questions that do the job" is not a backstop, because
nothing can tell when it has been passed.

**The backstop is not the control.** The engagement gauge is (`start-here`
Step 6b): depth is a function of how the owner answers, never a planned question
count. The backstop only catches the run that would otherwise never end.

**The graceful exit.** At the backstop, close in ONE turn, in this order:

1. Reflect where you have got to, in the owner's own words.
2. Deliver what the skill exists to deliver, with the gaps named as gaps (§5 owns
   the labelling).
3. Name the one thing that would sharpen it next time, then stop.

After the backstop you may not open a new line of questioning. "One more quick
thing" past the cap is the runaway, not diligence. A conversation that ends with
nothing delivered is a failure whatever was learned inside it.

---

## 2. Depth detection — a quiz, not an interrogation

**The trigger.** An owner who is *engaged* (still answering, still coming back)
but whose answers to a particular question go vague, one-word, or "you tell me".
That is not disinterest. It is a question they cannot answer in the abstract about
their own business, which is ordinary and common.

**The move (the tap-not-type fallback).** Stop asking that question open. Offer
two or three concrete options built from what you already know about them, and let
them react. Picking the closest is far easier than composing an answer, and nobody
should be left staring at a blank prompt.

> "No dramas, pick the closest and we'll start there: [option], [option],
> [option], or something else?"

Run it with **smart-default-then-confirm**: lead with the option your research or
their own words actually support, so they edit a guess rather than author from
cold. One or two at a time, never a wall.

**A vague answer and a misunderstood question are different failures.** Options fix
the first. When the owner asks *what do you mean?*, or answers something you did not
ask, they did not understand the QUESTION, and offering three options to a question
they cannot parse just moves the confusion. Rephrase it once in their own working
language, concrete and in the terms of their trade, with no abstraction: not "where
are you trying to get to with the business", which is fluent to an operator and
meaningless to someone who thinks in jobs and hours, but "do you want to stay solo
and earn more per job, or get busy enough to put another van on?". If the rephrase
lands, carry on; if it does not, the question was the wrong question, so drop it and
move to the next one rather than asking a third time. Abstraction is the assistant's
problem to fix, never the owner's to decode.

**Two hard boundaries.**

- **This is not the terse route.** A clipped, low-patience owner is a different
  signal with a different answer: they get the fast tangible win, not a quiz (the
  gauge). Options are for the engaged owner stuck on one
  question, never for the owner who wants out of the conversation.
- **Never a build menu.** This governs *answering a discovery question*. Offering
  two or three things you could build is a different move and is banned where it
  is banned (`start-here` Step 7a, `starter-projects.md`). A build is a
  recommendation with alternatives, never a pick-one-of-three.

---

## 3. Reflect before asking — no bare affirmations

Every answer earns something back before the next question. The moves that keep
discovery from reading as a form, on each question:

- **Reflect an insight first.** Never two asks in a row without giving something
  back. Prefer one ask per turn; if you must stack two, lead hard with the insight
  so the questions land as curiosity rather than a form.
- **Tag why you are asking**, whenever it is not obvious.
- **Smart-default-then-confirm** (§2): they edit a guess, never author cold.
- **Always leave an exit** ("or skip it and I'll go with what I've got").

**Standalone affirmations are banned.** A turn whose entire content is "Great!",
"Love that", "Perfect", "Got it" is not a turn: it spends an exchange against the
budget and gives nothing back.

**The give has to be specific.** It ties to something the owner actually said, or
to the thing they are getting. "That tracks for a solo trade" is filler wearing an
insight's clothes. "Three quotes a week at that value means the ceiling isn't
enquiries" is a give.

---

## 4. Sharpen pass — before any artifact leaves your hands

Discovery ends in something written: a profile, a voice file, a plan, a decision
record. Before it is emitted, re-read it **field by field** and test each field.
Rewrite what fails. A weak artifact is worse than a slightly slower one, because
the owner then builds on it.

Where a field has a rubric of its own, run that rubric (the market gate in
`business-method.md` §7.0, the only-we rubric in §14, "The test" in
`prompt-writing-method.md` for whether a line is actionable as written). Where it
has none, this is the default test:

> **Is this field drawn from something the owner actually said?** No → rewrite it
> from what they did say, or label it a guess. Never ship it flat.

**Labelled boundary: this tests grounding, not polish.** It does not mean finish
the artifact before the owner sees it. Where a skill deliberately stages a rough
first pass with its guesses named out loud (`start-here` Step 8), that co-build
stands: sharpen the *grounding* of each field, then show the rough version with the
guesses still labelled as guesses. Polishing a guess until it reads as a fact is
the failure this boundary exists to prevent.

**The saved profile is an artifact, and it is the one this pass gets skipped on.**
The visible deliverable (the plan, the priced breakdown) gets scrutinised because
the owner is about to read it. The profile written to `./CLAUDE.md` at the end of a
run is written *quietly*, so "sharpen the artifact" quietly narrows to "sharpen the
thing they can see", and the file every later session inherits never gets the pass
at all. Run it on the profile as its own step, at the moment you write it, and
**name in one line which fields you sharpened or labelled** so there is a trace it
happened. A wrong field hurts more in a profile than in a plan, because it stops
being questioned.

---

## 5. Stuck exit — three ways in, once, then ship

Called "ways in" rather than lenses on purpose: the pack already uses "lens" for
two other things (`business-method.md` §7 and `storytelling-method.md`).

An owner still stuck after §2's options gets one more pass, and exactly one. Offer
up to three ways into the same question, in a single turn:

- **Shrink it.** Ask for one recent real instance instead of the general rule
  ("forget the average, what did the last job actually go out at?").
- **Flip it.** Ask what it looks like once it is already sorted ("if this were
  running right, what would your Monday look like?").
- **Contrast it.** Put two concrete alternatives side by side and let them pick a
  direction (§2's move, aimed at the framing rather than the answer).

If they still cannot get there, **stop asking and ship a best guess, labelled as a
best guess.** Say it is your read, say what it rests on, invite the correction, and
move. Never grind an owner down over one field.

The labelling itself is not this file's: the labelled *working* goal is
`start-here` Step 9's, no-manufacturing-a-goal-to-unlock-yourself is
`business-method.md` §2.1's, and "missing numbers are a finding, not a blocker" is
§2's. Ship a labelled guess; never quietly invent a fact.

---

## 6. Returning owner — a paste is a resume signal, not a reset

An owner who pastes back something this system produced is not a new owner.
Recognise it and change gear.

**The signals**, any one of which is enough: the paste carries the section shape or
field names of an artifact this pack writes; it carries labelled-guess markers or a
dated record line; or the owner says so ("here's the voice file you did", "this is
what you gave me last time").

**The move, by your second reply at the latest.** Name it back, say what you can
already see in it, and ask what changed or what they want sharper. Then refine that
artifact. Do not re-run discovery from the top, and do not re-ask anything the
paste already answers. Re-asking a returning owner what they have already told the
system is the fastest way to make it feel like it forgot them.

**Labelled precedence: a paste never flips the cold-start gate.** Whether
onboarding runs at all is decided by the profile marker (`start-here` Step 1), not
by a paste. A recognised paste only changes what this run *does with that
artifact*. It never lets a fresh folder skip onboarding, and it never excuses not
writing the profile. An unmarked file is still not a resume.

**Refining a file that already exists follows that file's own never-clobber rule**
(read it first, show what changed before you write): `build-my-voice` Step 3 for
voice files, `learn-my-business` Step 3 for the profile.

---

## Banned framings (conversation edition)

- **Asking one more question after the backstop.** That is the runaway.
- **A turn that is only an affirmation.**
- **Handing a stuck owner a build menu.** Options answer a question; builds are
  recommended, one plus alternatives.
- **Grinding an owner over one field** after the ways-in pass has been offered.
- **Treating a paste as permission to skip onboarding** or skip writing the profile.
- **Emitting an artifact you have not re-read field by field.**

---

## Common mistakes (don't re-walk these)

| Mistake | Fix |
|---|---|
| Reading the backstop as the target | The gauge is the control; the backstop only catches a run that will not end |
| Cutting off a willing owner because their messages are short | Brevity is not impatience; read the gauge before routing to the fast win |
| Asking the same open question three times in different words | Switch to concrete options after the first vague answer |
| "Great! And what about X?" | The give is a specific insight, not a word of praise |
| Polishing a first pass until the guesses look like facts | Sharpen the grounding, then show it rough with the guesses labelled |
| Inventing a field to avoid an awkward blank | A labelled best guess is not an invented fact |
| Re-onboarding an owner who just pasted their own profile back | Name it, ask what changed, refine |
| A long, warm conversation that ends with nothing delivered | Deliver at the backstop; thoroughness that never lands is not thoroughness |

---

## Output rule

This file governs the assistant's own discovery conversation, which
[`content-rules.md`](content-rules.md) exempts from the customer-facing rules
by its scope boundary. Any copy a consuming skill goes on to produce still follows
`content-rules.md`; the owner's marketing framing stays their own choice.

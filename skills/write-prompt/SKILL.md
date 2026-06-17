---
name: Write Prompt
description: Turn a rough ask into a complete, explicit prompt ready to hand to a person or to Claude. Loads the prompt-writing method, fills the gaps (goal, context, exact inputs, steps, output format + example, constraints, verification) by asking only what's genuinely missing, and returns one copy-paste prompt with no vague placeholders. Use whenever you're briefing a teammate, writing an instruction for someone's Claude, or drafting an AI step in an automation.
triggers:
  - write a prompt
  - sharpen this prompt
  - turn this into a proper prompt
  - help me brief this
  - make this prompt explicit
  - improve this prompt
---

# Write Prompt

A vague prompt forces the reader to guess and gives different output every time;
an explicit, complete one gets it right the first time. This skill takes a rough
ask and returns a finished prompt built to `knowledge/prompt-writing-method.md`.

## Step 1 — Take the rough ask + load the method

Read the operator's rough ask (what they want the prompt to achieve). Read
`knowledge/prompt-writing-method.md` for the 7-part checklist this output must
satisfy.

## Step 2 — Find the gaps, ask only what's missing

Map the rough ask onto the checklist and identify which items are missing or
vague:

1. Goal + success criteria
2. Context, role, boundaries, ordering
3. Exact inputs / tools / data (real records, URLs, files, workspace, test data)
4. Explicit steps with real values
5. Output format + an example
6. Constraints + banned
7. Verification

Ask the operator **one short batch of questions covering only the genuinely
missing items** — never re-ask what they already gave you, and never pad with
questions whose answer you can infer from their workspace or the ask. If the
prompt is for acting in TrustPager, pull concrete values (record names, URLs,
stage names) from the workspace rather than asking, where you can.

If the operator says "just make your best guess", fill the gaps with explicit,
labelled assumptions rather than leaving anything vague.

## Step 3 — Write the finished prompt

Produce ONE prompt, in a copy-paste code block, that covers every checklist item
in order, with real values throughout. Requirements:

- Self-contained: written as if the reader (person or Claude) has zero prior
  context.
- Every step concrete: a step that opens a screen names its URL; a check states
  the expected result; a branch states the action for pass vs fail.
- Includes the exact output format and, for anything non-trivial, a short
  example of good output.
- States constraints and any banned moves/phrases.
- Ends with how the reader verifies success.

**Never leave a placeholder** like `<<< ... >>>`, "(the steps)", "(a link and
one action)", or "(describe what to do)". If a concrete value is still unknown
after Step 2, that's a question to ask, not a blank to ship.

## Step 4 — Show it + a one-line note

Return the finished prompt in the code block, then one short line on what you
assumed or filled in (so the operator can correct it). If the prompt is meant
for a teammate to keep using, remind the operator they can have that person's
Claude save it (see `/onboard-team-member` for the persist pattern).

## Hard rules
- ❌ No vague placeholders in the output. Ever. That's the whole point.
- ❌ Don't ask for what was already provided or what you can read from the workspace.
- ✅ Real values throughout: actual records, URLs, stage/product names, test data.
- ✅ The output prompt itself meets the 7-part checklist — goal through verification.
- ✅ Keep clarifying questions to one short batch, only the genuine gaps.

## Output shape
A single copy-paste prompt covering all 7 checklist items with real values, then
a one-line note on anything you assumed. If items were missing, the short batch
of clarifying questions comes first instead, then the finished prompt.

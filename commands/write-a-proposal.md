---
description: Turn a priced scope and your brand voice into the proposal that wins the job: an on-brand proposal or statement of work in your voice, written out as a real .docx you can send today. Cover, understanding of the need, scope and deliverables, the priced breakdown, timeline, terms, and the next step. Works from what you have, no accounts needed.
---

Run the **Write A Proposal** skill.

Invoke the skill at `skills/write-a-proposal/SKILL.md`. Follow it exactly: take
in the two inputs (a priced breakdown from `price-my-work` or typed in, plus the
owner's brand voice if they have a `voice.md` or first-brand brief), confirm the
specifics a proposal needs (who it is for, the job in one line, the timeline, and
any terms), asking one plain question for anything missing rather than inventing
it.

Lay out the proposal as a seven-section outline in chat for approval (cover and
intro, understanding of the need, scope and deliverables, the priced breakdown,
timeline, terms, and the next step), then, once approved, generate it as a real
`.docx` with the document writer (the `doclib` write path, `tools/write_docx.py`)
built from JSON `heading` / `paragraph` / `bullet` blocks.

One proposal per run. Never invent the price, scope, or terms. Customer-facing
output stays positive-only and outcome-led with no em dashes: every section names
the result the prospect is buying. The finished `.docx` is the win; once a
customer system is connected, the same proposal can become a live signing
template that goes out, gets opened, and comes back signed without rebuilding it
each time (describe that as an outcome, do not make it the price of the win).

# Prompt-writing method

**Every prompt you write — for a person or for Claude — must be explicit, technical, and complete. A prompt is a specification, not a vibe.** This is how a team gets consistent results from Claude: a vague prompt forces the reader to guess and produces different output every time; an explicit, complete one produces the right output the first time.

This matters most on a team. A manager briefing a rep, a rep handing work to their Claude, an automation's AI step, a paste-ready instruction sent to a teammate: each is a prompt, and each is only as good as its weakest gap.

## The checklist — every prompt covers these, in order

1. **Goal + success criteria.** Exactly what to produce, and how the reader knows it's right or done. Lead with this.
2. **Context, role, boundaries.** Who is doing it, what they can and cannot do, what's out of scope, and any ordering that matters ("do X before Y"). Write it self-contained: assume the reader has zero prior context.
3. **Exact inputs / tools / data.** Name the real things: the specific record, the customer, the URL, the file, the workspace, the test contact. Never "the relevant deal" — the actual deal.
4. **Explicit steps with real values.** Every step concrete. A step that opens a screen names its URL; a check states what the result should be; a branch states what to do if it passes vs fails.
5. **Output format + example.** Specify the shape of the output (an email? a list? a JSON record?). For anything non-trivial, include a short example of good output.
6. **Constraints + banned.** What NOT to do: tone rules, banned phrases, length limits.
7. **Verification.** How the reader confirms it worked before calling it done.

## Banned — the failure this method exists to stop
Vague stand-ins where real content belongs: "(a link and one action)", "(the steps)", "(the relevant page)", "(what good looks like)", "describe what to do", "etc." If you can't fill in a concrete value, that gap is the thing to resolve before sending, not paper over with a description.

## The test
Read the prompt back as if you have never seen the task. Could you produce exactly the right output with no further questions? If not, a gap remains — find it and fill it.

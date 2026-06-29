---
description: Turn a rough ask into a complete, explicit prompt you can hand to a person or to Claude. Fills the gaps (goal, context, exact inputs, steps, output format, constraints, how to verify) and returns a ready-to-paste prompt with no vague placeholders.
---

Run the **Write Prompt** skill.

Invoke the skill at `skills/write-prompt/SKILL.md`. Follow it exactly: take the
operator's rough ask, load `knowledge/prompt-writing-method.md`, ask only for the
checklist items that are genuinely missing, then return one finished prompt in a
copy-paste block that covers goal + success, context/role/boundaries, exact
inputs/tools/data, explicit steps with real values, output format + an example,
constraints, and how to verify. Never leave a `<<< ... >>>` or "(describe...)"
placeholder in the output.

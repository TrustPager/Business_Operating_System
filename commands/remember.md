---
description: Save, update, or forget something Claude should carry into future sessions — a preference, a way you like things done, soft context the CRM doesn't hold. Kept in a local memory store, one fact per file.
---

Run the **Remember** skill.

Invoke the skill at `skills/remember/SKILL.md` and follow it exactly: decide
whether the fact belongs in memory at all (not a CRM fact, not a secret, not
transient), check `./.bos-memory/MEMORY.md` for an existing memory to update,
then write/update/delete the `<slug>.md` and keep the index line in sync. The
full model and rails are in `knowledge/memory-and-feedback.md`. Close with a
single confirmation line.

---
description: Once a CRM is connected, read your live workspace and write your business profile from real data.
---

Run the **Learn My Business** skill.

Invoke the skill at `skills/learn-my-business/SKILL.md`. Follow it exactly: run
the fetcher, load `templates/CLAUDE.md` as the base plus the matching section of
`knowledge/industry-notes.md`, fill it from the real workspace data, and write
`./CLAUDE.md` -- but never overwrite an existing one without showing the diff and
asking. Close with a short summary of what was filled and the one or two items
the operator needs to confirm.

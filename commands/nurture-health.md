---
description: Health-check your live nurture sequences: funnel, the step that's leaking, open/click rates, and whether the un-enrol side is firing.
---

Run the **Nurture Health** skill.

Invoke the skill at `skills/nurture-health/SKILL.md`. Follow its instructions
exactly: run the fetcher, then present the biggest leak first, a compact funnel
per queue, and an honest "couldn't measure" line for anything that degraded.
End with the single step most worth fixing first and which skill to hand it to.

If the operator named a specific queue, pass it through with `--queue <id>`.

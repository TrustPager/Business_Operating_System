---
description: The Friday rollup: what shipped this week (deals won, tasks done, new opportunities), what stalled (deals gone quiet, overdue carried over), and where the pipeline sits now. Ends with next week's focus.
---

Run the **Weekly Review** skill.

Invoke the skill at `skills/weekly-review/SKILL.md`. Run
`python skills/weekly-review/fetch.py` (`--days N` to change the window), then
present the review: SHIPPED first (won deals + value, tasks done, new opps), then
STALLED (the point: quiet high-value deals + overdue carried over), then the
current open-pipeline total, ending with one concrete focus for next week. Use
the operator's own stage/product names; totals + headline rows, not every record.
Offer to action the stalls (draft a re-engage via `/draft-reply`, reschedule an
overdue task) one at a time with a yes, and mention `/email-me-a-report` can
deliver this every Friday automatically.

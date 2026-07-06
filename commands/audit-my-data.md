---
description: Find the gaps in your records: missing fields, likely duplicates, and dormant records, worst-first.
---

Run the **Audit My Data** skill.

Invoke the skill at `skills/audit-my-data/SKILL.md`. Run both
`python ~/.claude/bos-run.py tool find-gaps --json` and `python ~/.claude/bos-run.py tool audit-contacts --json`,
then present a consolidated hygiene report worst-first: FIX (unowned/duplicate/
no-value records that cost money) then WORTH-A-LOOK (missing emails, dormant
contacts). Offer the safe mechanical fixes one at a time with a yes; never merge
or delete without showing the records and naming what survives.

For pipeline performance (stuck deals, stage drop-offs) point to `/weekly-review`,
not this skill.

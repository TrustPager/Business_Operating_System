---
description: Find the mess — missing fields, bad/missing emails, likely-duplicate contacts, dormant/orphan records, opportunities with no contact/value/owner, overdue and undated tasks. Read-only; fix checklist worst-first.
---

Run the **Audit My Data** skill.

Invoke the skill at `skills/audit-my-data/SKILL.md`. It gathers CRM records via
`trustpager` MCP read tools (`list_contacts`, `list_customers`, `list_deals`,
`list_tasks`) and scans them for gaps, then presents a consolidated hygiene
report worst-first — FIX (unowned/duplicate/no-value records that cost money)
then WORTH-A-LOOK (missing emails, dormant contacts). Offer the safe mechanical
fixes one at a time with a yes; never merge or delete without showing the
records and naming what survives.

For pipeline performance (stuck deals, stage drop-offs) point to `/weekly-review`,
not this skill.

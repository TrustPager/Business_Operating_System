---
name: Audit My Data
description: Find the mess in the workspace — missing fields, bad/missing emails, likely-duplicate contacts, dormant and orphan records, opportunities with no contact/value/owner, overdue and undated tasks. Read-only; surfaces a fix checklist worst-first.
triggers:
  - audit my data
  - find the mess
  - check my data quality
  - find duplicates
  - what's messy in my workspace
  - data hygiene check
  - clean up my crm
  - find missing fields
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__list_contacts
  - mcp__trustpager__list_opportunities
  - mcp__trustpager__list_tasks
  - mcp__trustpager__update_opportunity
status: active
---

# Audit My Data

Owners import contacts, half-fill opportunities, and never look back — so the
data quietly rots: duplicate contacts, deals with no owner, tasks with no due
date. This is the hygiene check-up. Read-only — it surfaces a fix list and
offers the safe fixes one at a time.

## Step 1 — Run the audits

Two read-only tools cover the data-hygiene surface; run both:

```bash
python tools/find-gaps.py --json
python tools/audit-contacts.py --json
```

- `find-gaps.py` — opportunities with no contact / no value / no stage / no
  owner; tasks overdue or with no due date.
- `audit-contacts.py` — missing/bad emails, likely-duplicate contacts (same
  email, or same name+company), dormant (365d+ no activity, no open opp), orphan
  (linked to nothing). `--dormant-days N` to tune.

If a script errors (auth/network), say so briefly and fall back to MCP reads
(`list_contacts`, `list_opportunities`, `list_tasks`) — but that's many calls;
prefer the scripts.

*(For pipeline performance — stuck deals, stage drop-offs, value by stage —
that's `/weekly-review`, not this skill. Keep this one to data quality.)*

## Step 2 — Present the report, worst first

Lead with what's actively costing money or will embarrass them, then tidy-ups.

```
🧹 Data audit — 3 things to fix, 2 worth a look

❌ FIX (costing you)
  → 4 opportunities have no owner — no one's working them. → assign
  → 2 likely-duplicate contacts (same email): "j.smith@…" appears twice. → merge/dedupe
  → 7 opportunities have no value set — your pipeline total is understated. → set value

⚠️ WORTH A LOOK
  → 12 contacts have no email — can't be emailed or blasted. → enrich or archive
  → 18 dormant contacts (no activity 365d+, no open deal). → archive or re-engage

✅ Clean: stages all placed, no orphan opportunities.
```

Use the operator's own pipeline/stage/field names (pull from the data, don't
invent). Don't dump every row — show the worst few per category and the count.

## Step 3 — Offer the fixes (with approval, one at a time)

For the safe, mechanical fixes, offer to apply them — one at a time, with a yes:
- Assign an unowned opportunity → `mcp__trustpager__update_opportunity(id, assigned_user_ids=[...])`
- Set a missing value → `update_opportunity(id, amount=...)` (confirm the number with the operator)
- Archive a dormant/orphan contact → confirm by name first.

**Never merge or delete without explicit, named confirmation.** Deduping is
destructive — show the two records and which survives before doing anything.
For bulk cleanups, do a small batch first, show the result, then continue.

## What to never do

- ❌ Don't present findings alphabetically or as one flat list — rank by cost.
- ❌ Don't auto-fix — offer, get a yes, one at a time.
- ❌ Don't merge/delete records without showing them and naming what survives.
- ❌ Don't treat "dormant" as "delete" — it's a re-engage-or-archive decision.

## Output shape

Headline tally, then FIX (worst first), then WORTH-A-LOOK, then a clean tally —
and the single highest-value fix to make first.

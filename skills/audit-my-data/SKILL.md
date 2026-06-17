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
---

# Audit My Data

Owners import contacts, half-fill opportunities, and never look back — so the
data quietly rots: duplicate contacts, deals with no owner, tasks with no due
date. This is the hygiene check-up. Read-only — it surfaces a fix list and
offers the safe fixes one at a time.

## Step 1 — Pull the data (parallel MCP calls)

Fire these **three read calls in parallel** in a single batch — all reads, free and fast. Use the `trustpager` MCP server. Pull the most recent records; you'll apply the hygiene rules yourself in Step 2. Paginate each to ~100 (pass `limit: 100`, then follow the `after` cursor for a second page if `pagination.has_more` is true — two pages is plenty for an audit).

| Need | Tool | Args |
|---|---|---|
| Opportunities (no contact/value/stage/owner) | `list_deals` | `limit: 100` |
| Contacts (missing/bad email, dupes, dormant, orphan) | `list_contacts` | `limit: 100` |
| Tasks (overdue, no due date) | `list_tasks` | `limit: 100` |

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

If one call errors (auth/network), say so briefly and proceed with what you have — don't bail on the whole audit because one endpoint is down. Everything below is computed against **now** in the operator's timezone. All reads — nothing here is journaled or needs approval.

*(For pipeline performance — stuck deals, stage drop-offs, value by stage —
that's `/weekly-review`, not this skill. Keep this one to data quality.)*

## Step 2 — Apply the hygiene rules

Run these checks over the pulled records. An opportunity is **inactive** (skip it in the opportunity checks) when its `status` (lowercased) is one of `won` / `lost` / `cancelled` / `abandoned` / `archived`.

### Opportunities (active only)

- **No contact** — `contact_id` is empty/missing.
- **No value** — `value` is empty, missing, or zero.
- **No stage** — `placements` is empty (no pipeline-stage placement).
- **No owner** — none of `assigned_user_ids`, `assigned_users`, or `owner_id` is set. Nobody is working it.

### Contacts

For each contact, read `first_name`, `last_name`, `email`, `phone`, `company_id`, and `last_activity_at` (fall back to `updated_at`). Treat `open_opportunity_count` (open opps) and `opportunity_count` (any opps) as the activity signals.

- **Missing email** — `email` empty.
- **Bad email** — `email` present but doesn't match a sane address shape: must be `something@something.tld` (a single `@`, a dot in the domain, no spaces). If it fails that, it's bad, not missing.
- **Missing phone** — `phone` empty.
- **Likely duplicates** — group contacts two ways and flag any group with 2+ members:
  1. **Same email** (case-insensitive) — strongest dupe signal.
  2. **Same first+last name AND same `company_id`** — a name collision inside one company.
- **Dormant** — `last_activity_at` is **365+ days** ago AND `open_opportunity_count` is 0. (If the operator asks for a different window, use that instead of 365.)
- **Orphan** — linked to nothing: no opportunities (`opportunity_count` is 0/absent) AND no `company_id`.

### Tasks

- **Overdue** — not completed (no `completed_at`, status not `completed`/`cancelled`) AND `due_date` (or `due_at`) is in the past. Capture days overdue and sort descending.
- **No due date** — not completed AND no `due_date`/`due_at` at all.

## Step 3 — Present the report, worst first

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

## Step 4 — Offer the fixes (with approval, one at a time)

For the safe, mechanical fixes, offer to apply them — one at a time, with a yes. These are **writes**, so the rails in `knowledge/safeguards.md` apply: confirm first, then after each call journal one line to `./.bos-journal.md`, and if a write comes back `202` / `approval_id` it's queued — surface the approval link and stop (don't retry).

- Assign an unowned opportunity → `update_deal(id, assigned_user_ids=[...])`
- Set a missing value → `update_deal(id, value=...)` (confirm the number with the operator first)
- Archive a dormant/orphan contact → confirm by name first, then `update_contact`.

**Never merge or delete without explicit, named confirmation.** Deduping is
destructive — show the two records and which survives before doing anything (search-first, never blind-delete). For bulk cleanups, do a small batch first, show the result, then continue.

## What to never do

- ❌ Don't present findings alphabetically or as one flat list — rank by cost.
- ❌ Don't auto-fix — offer, get a yes, one at a time.
- ❌ Don't merge/delete records without showing them and naming what survives.
- ❌ Don't treat "dormant" as "delete" — it's a re-engage-or-archive decision.

## Output shape

Headline tally, then FIX (worst first), then WORTH-A-LOOK, then a clean tally —
and the single highest-value fix to make first.

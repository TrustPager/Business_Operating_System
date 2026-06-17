---
name: Weekly Review
description: The Friday rollup — what shipped this week (deals won, tasks done, new opportunities), what stalled (deals gone quiet, overdue carried over), and where the pipeline sits now. One scannable review with the next week's focus.
triggers:
  - weekly review
  - friday rollup
  - how did this week go
  - what shipped this week
  - end of week summary
  - weekly recap
  - review my week
---

# Weekly Review

The end-of-week gut-check: did the needle move, and what's been quietly slipping?
`/sweep-my-day` is the daily what's-urgent; this is the weekly what-happened +
what-stalled. Reads in under a minute and ends with next week's single focus.

## Step 1 — Pull the data (parallel MCP calls)

Fire these two reads in parallel in a single batch. Both are reads — free, nothing journaled, no approval. Use the `trustpager` MCP server.

| Need | Tool | Args |
|---|---|---|
| Opportunities (wins, losses, new, going-quiet, open pipeline) | `list_deals` | `limit: 200` |
| Tasks (completed this week, overdue carried over) | `list_tasks` | `limit: 200` |

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

The **window is the last 7 days** by default (adjust if the operator asks). Everything below is computed against **now**. For deeper pipeline analysis (stuck-by-value, stage drop-offs) you can also pull `get_pipeline_summary` and fold it in.

## Step 2 — Digest into shipped / stalled / pipeline

Opportunity value = `amount` (fall back to `value`), as a number. Opportunity status is the lowercased `status`.

**SHIPPED (this week):**
- **Won:** opportunities whose status is `won` AND whose `updated_at` is within the window. Sum their value. Rank by value, descending; name the top one.
- **Lost:** opportunities whose status is `lost` AND `updated_at` within the window (count).
- **New opportunities:** opportunities whose `created_at` is within the window (count).
- **Tasks completed:** tasks whose `completed_at` is within the window (count).

**STALLED (the real point):**
- **Going quiet:** an **open** opportunity (status `open`) whose last touch is **7+ days** ago. Last touch = `last_activity_at` (fall back to `created_at` if there's no activity timestamp); days silent = days since that. Rank by **value × days_silent, descending** (biggest at-risk first); show the **top 10** and a count of the rest.
- **Overdue tasks carried over:** tasks not completed (no `completed_at`, status not `completed`/`cancelled`) whose `due_date` is in the past. Capture title and days overdue. Rank by **days overdue, descending**; show the **top 10** and a count of the rest.

**PIPELINE NOW:**
- **Open count + open value:** the count of open-status opportunities and the sum of their value.

## Step 3 — Present the review

Lead with the wins (earn the dopamine), then the stalls (the real point), then
the pipeline snapshot.

```
🗓️  Week in review — <date range>

✅ SHIPPED
  → Won: 3 deals · $42,000  (top: "Acme — fit-out" $28k)
  → 14 tasks completed · 6 new opportunities created

🐢 STALLED — needs attention next week
  → "Northside reno" — $35k, silent 11 days. → re-engage
  → "Vertex proposal" — $18k, silent 9 days. → follow up
  → 4 overdue tasks carried over (oldest: "Send Patel quote", 6 days late)

📊 PIPELINE NOW
  → 22 open opportunities · $310,000 open value

🎯 Next week's focus: the two silent high-value deals above — they're 60% of
   what's at risk. Start with Northside.
```

Use the operator's own stage/product names. Don't dump every row — top few per
section + the count.

## Step 4 — Offer to action the stalls (with approval)

Anything that **writes** follows the rails in `knowledge/safeguards.md` — confirm before it lands, journal the write to `.bos-journal.md`, search-first so you don't duplicate. Turn the review into next week's first moves — one at a time, with a yes:

- **Re-engage a quiet deal** → draft via `/draft-reply`, queue for approval.
- **Knock over an overdue task** → `complete_task` if done, or reschedule it (`update_task`).
- **Set up the recurring version** → mention `/email-me-a-report` can deliver
  this review to their inbox every Friday automatically.

## What to never do

- ❌ Don't send anything without drafting + approval first.
- ❌ Don't bury the stalls under the wins — the stalls are why this exists.
- ❌ Don't list every won deal / completed task — totals + the headline ones.
- ❌ Don't pad with motivational filler. Signal, then the one focus.

## Output shape

SHIPPED, then STALLED (the point), then PIPELINE NOW, then one concrete focus
for next week — not a menu.

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

## Step 1 — Fetch the rollup

```bash
python skills/weekly-review/fetch.py
```

(`--days N` to change the window; default 7.) One call: this week's won/lost
deals, new opportunities, tasks completed, plus the stalls — open deals gone
quiet and overdue tasks carried over — and the current open-pipeline total.
The shape is documented at the bottom of `fetch.py`.

Fallback if it can't run: `mcp__trustpager__list_opportunities` +
`list_tasks` + `get_pipeline_summary` — many calls; prefer the script. For
deeper pipeline analysis (stuck-by-value, stage drop-offs) run
`python tools/audit-pipeline.py` and fold it in.

## Step 2 — Present the review

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

## Step 3 — Offer to action the stalls (with approval)

Turn the review into next week's first moves — one at a time, with a yes:
- **Re-engage a quiet deal** → draft via `/draft-reply`, queue for approval.
- **Knock over an overdue task** → `complete_task` if done, or reschedule it.
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

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
function_slot: strategy
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__list_opportunities
  - mcp__trustpager__list_tasks
  - mcp__trustpager__get_pipeline_summary
  - mcp__trustpager__complete_task
status: active
---

# Weekly Review

The end-of-week gut-check: did the needle move, and what's been quietly slipping?
`/sweep-my-day` is the daily what's-urgent; this is the weekly what-happened +
what-stalled. Reads in under a minute and ends with next week's single focus.

## Step 1 — Fetch the rollup

```bash
python ~/.claude/bos-run.py weekly-review
```

(`--days N` to change the window; default 7.) One call: this week's won/lost
deals, new opportunities, tasks completed, plus the stalls — open deals gone
quiet and overdue tasks carried over — and the current open-pipeline total.
The shape is documented at the bottom of `fetch.py`.

Fallback if it can't run: `mcp__trustpager__list_opportunities` +
`list_tasks` + `get_pipeline_summary` — many calls; prefer the script. For
deeper pipeline analysis (stuck-by-value, stage drop-offs) run
`python ~/.claude/bos-run.py tool audit-pipeline` and fold it in.

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

Where the fetch data supports it, add the one-page scoreboard line
(business-method.md §12.6): this week's leads, conversations, close rate, cash
collected, and (if tracked) activation and saves, against last week. If most of
those numbers don't exist, don't fake them: say so, and name the scoreboard
itself as the first prescription (§12.6), offering `/build-spreadsheet` or
`/email-me-a-report` to install it.

The focus is one pressure point, not a to-do list (§4: the output is 1-3
moves). If last week's focus landed, expect the pressure point to have MOVED
(§4) and say where it likely went, rather than re-prescribing the same fix.

## Step 3 — Offer to action the stalls (with approval)

Turn the review into next week's first moves — one at a time, with a yes:
- **Re-engage a quiet deal** → draft via `/draft-reply`, queue for approval.
- **Knock over an overdue task** → `complete_task` if done, or reschedule it.
- **Set up the recurring version** → mention `/email-me-a-report` can deliver
  this review to their inbox every Friday automatically.
- **Operator floats something new** ("should we try a new platform / a second
  offer?") → apply the more-better-new order (§4.4) and route to
  `/grill-me-on-this-decision`; the default answer is a Better move on the
  current channel.

End by collapsing the focus to now: "what's the first move, and what are you
doing in the next two hours that matters more?" (§4). Same-day beats Monday.

## What to never do

- ❌ Don't send anything without drafting + approval first.
- ❌ Don't bury the stalls under the wins — the stalls are why this exists.
- ❌ Don't list every won deal / completed task — totals + the headline ones.
- ❌ Don't pad with motivational filler. Signal, then the one focus.

## Output shape

SHIPPED, then STALLED (the point), then PIPELINE NOW, then one concrete focus
for next week — not a menu.

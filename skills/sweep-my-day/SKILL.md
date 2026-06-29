---
name: Sweep My Day
description: Morning briefing — what needs the operator's attention today across opportunities, tasks, communications, and missed calls. Surfaces silent deals, overdue items, hot inbound, and time-sensitive follow-ups in one scannable view.
triggers:
  - sweep my day
  - what needs my attention
  - what's on for today
  - morning briefing
  - what should I do first
  - what's hot
  - daily roundup
  - start my day
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__list_email_threads
  - mcp__trustpager__list_sms_conversations
  - mcp__trustpager__list_phone_call_logs
  - mcp__trustpager__list_form_submissions
  - mcp__trustpager__list_whatsapp_conversations
  - mcp__trustpager__list_tasks
  - mcp__trustpager__list_work_orders
  - mcp__trustpager__list_scheduled_communications
  - mcp__trustpager__list_opportunities
  - mcp__trustpager__get_opportunity_activities
  - mcp__trustpager__list_transcripts
  - mcp__trustpager__list_bookings
  - mcp__trustpager__get_pipeline_summary
---

# Sweep My Day

You are running the operator's morning briefing across their TrustPager workspace. Your goal: in under 60 seconds of reading, the operator knows exactly what needs attention, in priority order, with one-tap actions ready to fire.

## Step 1 — Fetch the data with the helper script

**Always run the data fetcher FIRST.** It executes 7+ parallel API calls and returns a digested JSON document — much faster and cheaper than chaining individual MCP tool calls.

```bash
python ~/.claude/bos-run.py sweep-my-day
```

(The `~/.claude/bos-run.py` launcher resolves the install location for you, and works from any folder, plugin or clone install. If the launcher is missing, run `python tools/setup.py` once from the BOS directory to create it.)

The script returns a single JSON document with five top-level sections, one per category below: `hot_inbound`, `overdue`, `going_quiet`, `todays_calendar`, `pipeline_pulse`. Each has a `count` (total found) and `items` (top results). The shape is documented at the bottom of `fetch.py`.

**If the script reports errors on stderr** for individual endpoints, mention them briefly in the briefing ("note: couldn't reach the bookings API right now") but proceed with what you have. Don't bail.

**If the script can't run at all** (auth error, network error), fall back to chained MCP tool calls — use the per-category guides below to drive what to fetch.

## Step 2 — Read the JSON and format the briefing

Five categories, ranked by how time-sensitive they are. Always present in this order — most urgent first, never alphabetical or by feature area.

### 🔥 1. Hot inbound — `digest.hot_inbound`

Items that arrived in the last 24 hours and haven't been replied to: unread email threads, unread SMS conversations, missed phone calls, and new form submissions.

For each item, surface: who, when, one-line context, and the recommended next move. If a recovery SMS hasn't been sent for a missed call, offer to draft one.

**Fallback MCP tools if the script failed:** `list_email_threads`, `list_sms_conversations`, `list_phone_call_logs`, `list_form_submissions`, `list_whatsapp_conversations`.

### 📅 2. Overdue items — `digest.overdue`

Tasks past their due date that haven't been completed. The script surfaces the top 5 ranked by days overdue. Don't dump the full list — `count` tells the operator how many more exist.

**Fallback MCP tools:** `list_tasks` (filter completed=false + due_date < today), `list_work_orders` (filter overdue + not closed), `list_scheduled_communications` (filter failed).

### 💤 3. Going quiet — `digest.going_quiet`

Active opportunities with no meaningful activity in 7+ days. The script ranks the top 5 by deal value × days-silent. For each, draft the suggested re-engagement message (don't send — queue it for operator approval).

**What counts as "meaningful":** activities, transcripts from calls, email replies, SMS replies. NOT automated platform emails. The script uses `last_activity_at` on the opportunity record.

**Fallback MCP tools:** `list_opportunities` (filter by active stage), then `get_opportunity_activities` and `list_transcripts` per opportunity. Expensive — only do this if the script genuinely failed.

### ⏰ 4. Today's calendar — `digest.todays_calendar`

Bookings scheduled for today plus tasks due today. Each booking includes the meeting URL and the linked opportunity (if any). For any booking today that doesn't already have a prep note, offer to run `/prep-for-call` for it.

**Fallback MCP tools:** `list_bookings` (today only), `list_tasks` (due today).

### 📊 5. Pipeline pulse — `digest.pipeline_pulse`

One-paragraph state-of-the-business: total open value, count by stage. Keep this to one paragraph maximum — it's a gut-check, not a report. If the script couldn't reach the summary endpoint, it derives totals from the opportunities list (the `_derived_from` field signals this).

**Fallback MCP tool:** `get_pipeline_summary` on the primary sales pipeline.

## Output format

Use this exact structure for consistency. The operator should learn to scan it the same way every morning.

```
☀️ Good morning. Here's your sweep for [DAY, DATE]:

🔥 HOT (X items)
  → [Item 1 — one line, with action]
  → [Item 2]
  → [Item 3]

📅 OVERDUE (X items)
  → [Most urgent — what + how late]
  → [Next most urgent]
  → ... and X more (say "show all overdue" to see them)

💤 GOING QUIET (X opportunities)
  → [Highest value silent deal — days silent, suggested action]
  → [Next]

⏰ TODAY'S CALENDAR
  → [Booking 1: time + attendee + status]
  → [Booking 2]
  → [Task due today]

📊 PIPELINE PULSE
  [One paragraph summary]

Next move: [The single highest-priority action the operator should take right now]
```

End with one concrete next move — not a menu of options. The operator's morning is best spent on the one thing that matters most, not deciding what to start with.

## Tone

- Direct. No fluff. No "great news!" openers.
- Use the operator's own language for their pipeline stages, opportunity types, and product names. Pull those from their workspace, don't invent them.
- If the workspace is genuinely quiet (no hot inbound, nothing overdue, no silent deals), say so cleanly: "Inbox is clear, no overdue items, pipeline is stable. Today's a focused-work day."

## What to never do

- ❌ Don't send any messages, even drafts, without offering the draft first and waiting for approval.
- ❌ Don't show every overdue item in a list — top 5 then a count.
- ❌ Don't pad with motivational language. The operator wants signal, not encouragement.
- ❌ Don't include items already actioned (replied to, marked done, dismissed).
- ❌ Don't call the platform "FinalPiece" or any internal name — say "your workspace" or just describe the data.

## Common follow-ups the operator will ask

Be ready to chain naturally into:

- "Draft a recovery message for that missed call" → use `send_sms` after drafting
- "Show me all overdue tasks" → full `list_tasks` filtered to overdue
- "What's the latest on [opportunity name]" → `get_opportunity` + `get_opportunity_activities`
- "Move [opportunity] to [stage]" → `update_opportunity`
- "Prep me for the 2pm call" → invoke the prep-for-call skill

## When this skill should NOT fire

- The operator is mid-task and asking a focused question (e.g. "what's John's phone number"). Don't hijack with a full briefing.
- The operator already ran sweep-my-day within the last 2 hours. Recap the changes since instead of re-running the whole thing.
- It's after 5pm local time — at that point `/weekly-review` is the better fit.

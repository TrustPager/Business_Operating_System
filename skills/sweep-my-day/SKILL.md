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
---

# Sweep My Day

You are running the operator's morning briefing across their TrustPager workspace. Your goal: in under 60 seconds of reading, the operator knows exactly what needs attention, in priority order, with one-tap actions ready to fire.

## Step 1 — Pull the data (parallel MCP calls)

Fire these **seven read calls in parallel** in a single batch — they're all reads, so they're free and fast. Use the `trustpager` MCP server. Ask for the most recent records; you'll filter them yourself in Step 2.

| Need | Tool | Args |
|---|---|---|
| Opportunities (for overdue actions, silent deals, pipeline) | `list_deals` | `limit: 100` |
| Tasks | `list_tasks` | `limit: 100` |
| Today's bookings | `list_bookings` | `limit: 50` |
| Unread email | `list_email_threads` | `limit: 50` |
| Unread SMS | `list_sms_conversations` | `limit: 50` |
| Missed calls | `list_phone_call_logs` | `limit: 50` |
| New form submissions | `list_form_submissions` | `limit: 50` |

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

If one call errors, mention it briefly in the briefing ("note: couldn't reach the bookings API right now") and proceed with what you have. Don't bail on the whole sweep because one endpoint is down.

Everything below is computed against **now** in the operator's timezone. All these are reads — nothing here is journaled or needs approval.

## Step 2 — Digest and format the briefing

Five categories, ranked by how time-sensitive they are. Always present in this order — most urgent first, never alphabetical or by feature area.

### 🔥 1. Hot inbound — last 24h, not yet replied to

From the four comms lists, keep only items whose timestamp is **within the last 24 hours** and that still need a response:

- **Unread email threads:** `is_read` is false AND the last message direction is **inbound** AND last-message time is within 24h. Surface subject, a ~120-char preview, when, and message count.
- **Unread SMS conversations:** unread count > 0 AND last-message time within 24h. Surface the sender number, a ~120-char preview, when, and unread count.
- **Missed inbound calls:** direction is inbound AND status is one of `missed` / `no-answer` / `voicemail` / `failed` AND within 24h. Surface the caller number, duration, when, and recording URL if present. **If no recovery SMS has gone out for a missed call, offer to draft one** (don't send — see rails).
- **New form submissions:** completed/created within 24h. Surface submitter name + email, a ~200-char AI summary, and when.

Sort all of it newest-first; show the **top 10** and a count of the rest. For each, give: who, when, one-line context, recommended next move.

### 📅 2. Overdue items

- **Tasks:** not completed (no completion time, status not `completed`/`cancelled`) AND due date is **in the past**. Capture title, priority, linked opportunity, due date, and days overdue.
- **Overdue next actions on opportunities:** an *active* opportunity (see the active-opportunity test below) whose `next_action_date` is in the past — the operator forgot to do something they scheduled. Capture the action name + opportunity, due date, days overdue, and value.

Rank by **days overdue, descending**; show the **top 5** and a count of the rest. Don't dump the full list.

### 💤 3. Going quiet

Active opportunities drifting with no momentum. Keep an opportunity here only if **all** of these hold:

1. It passes the **active-opportunity test** (below).
2. It has **no future** `next_action_date` (a scheduled future action means it's in progress, not quiet).
3. Its last-touch time (`updated_at`) is **7+ days ago**.

Rank by **deal value first, then longest silence**; show the **top 5**. For each, surface name, value + currency, stage, lead source, days silent, and the primary contact — and **draft a suggested re-engagement message** (queue it for approval, don't send).

> "Meaningful activity" = real activity, call transcripts, email replies, SMS replies — **not** automated platform emails. `updated_at` is the proxy.

### ⏰ 4. Today's calendar

- **Bookings** starting today (status not cancelled): time, attendee name/email, end time, meeting URL, linked opportunity/contact. For any booking today without a prep note, offer to run `/prep-for-call`.
- **Tasks** due today (not completed): title, priority, time, linked opportunity.

Sort by start time, ascending.

### 📊 5. Pipeline pulse

Derive from the opportunities list — **one paragraph, no more**. It's a gut-check, not a report.

- **Total open value + count:** sum value across opportunities that pass the active test.
- **Won / lost this month:** opportunities whose close date (`actual_close_date`, or `lost_at` for losses) falls on/after the 1st of the current month, split into won vs lost (count + value).
- **By stage:** count and summed value grouped by current stage name.

### The active-opportunity test (used by sections 2, 3, 5)

An opportunity is **active** when **both**:
- its status is not one of `won` / `lost` / `cancelled` / `abandoned` / `archived`, **and**
- its current stage is not flagged as a won-stage or lost-stage.

Its current stage name lives on the opportunity's first placement → pipeline stage. If there's no placement, treat the stage as "Unstaged".

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

- ❌ Don't send any messages, even drafts, without offering the draft first and waiting for approval. (See `knowledge/safeguards.md` — ask before anything outward-facing.)
- ❌ Don't show every overdue item in a list — top 5 then a count.
- ❌ Don't pad with motivational language. The operator wants signal, not encouragement.
- ❌ Don't include items already actioned (replied to, marked done, dismissed).
- ❌ Don't call the platform "FinalPiece" or any internal name — say "your workspace" or just describe the data.

## Common follow-ups the operator will ask

Be ready to chain naturally into these. Anything that **writes** follows the rails in `knowledge/safeguards.md` — show the draft, wait for approval, then journal the write to `.bos-journal.md`:

- "Draft a recovery message for that missed call" → draft, confirm, then `send_sms`
- "Show me all overdue tasks" → full `list_tasks` filtered to overdue
- "What's the latest on [opportunity name]" → `get_deal` + `get_deal_activities` (and `list_transcripts` if there were calls)
- "Move [opportunity] to [stage]" → `move_opportunity_card`
- "Prep me for the 2pm call" → invoke the prep-for-call skill

## When this skill should NOT fire

- The operator is mid-task and asking a focused question (e.g. "what's John's phone number"). Don't hijack with a full briefing.
- The operator already ran sweep-my-day within the last 2 hours. Recap the changes since instead of re-running the whole thing.
- It's after 5pm local time — at that point `/weekly-review` is the better fit.

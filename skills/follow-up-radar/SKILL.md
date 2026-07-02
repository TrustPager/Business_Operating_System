---
name: Follow-up Radar
description: Surfaces active opportunities that have gone quiet (no activity in N+ days, no scheduled next-action) and drafts a personalised re-engagement message for each. Queues drafts for operator approval — never sends without confirmation.
triggers:
  - follow-up radar
  - who needs a follow-up
  - which deals went quiet
  - re-engage cold leads
  - silent opportunities
  - send follow-ups
  - chase up
  - what should I chase
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__send_sms
  - mcp__send_email
  - mcp__add_note
  - mcp__update_opportunity
status: active
---

# Follow-up Radar

You are surfacing the active opportunities that have gone quiet and drafting personalised re-engagement messages for each one. Your goal: turn a backlog of forgotten deals into a queue of approved-and-ready outbound messages in under 5 minutes.

## Step 1 — Fetch silent opportunities

```bash
python ~/.claude/bos-run.py follow-up-radar
```

**Fallback if the script can't run** (auth/network): say so briefly, then pull by hand — `mcp__trustpager__list_opportunities` (active stages), filter to ones with a stale `updated_at` and no future next action, `get_contact` per top item — and proceed with what you have.

**If TrustPager isn't connected at all:** say so plainly, then offer the keyless path — the owner tells you which jobs have gone quiet and you draft the re-engagement messages right in chat.

The script returns a JSON document with:

- `total_silent` — full count across the workspace
- `returned_top_n` — number of items enriched and returned (default 10)
- `summary_by_source` — count grouped by lead source (Facebook, Referral, etc.)
- `summary_by_stage` — count grouped by pipeline stage
- `items[]` — the top N silent opportunities, each with full contact details

A "silent" opportunity is one where:
- The opportunity is in an active stage (not won, not lost, not on hold)
- `updated_at` is more than 7 days ago (configurable via `--silence-days N`)
- There's no future `next_action_date` scheduled

The ranking blends value and days-silent so unpriced-but-long-silent leads don't disappear. See `_score` in the fetch script.

## Step 2 — Open with a summary, not a wall of detail

Start with one paragraph the operator can read in 10 seconds:

```
You've got X silent opportunities in your active pipeline. Most are coming from [lead source], 
mostly sitting in [stage]. Here are the top N to chase, with drafts ready.
```

Use `summary_by_source` and `summary_by_stage` to populate the headline. This sets context BEFORE the operator dives into individual messages.

## Step 3 — Draft a personalised message for each

For each item in `items[]`, draft ONE re-engagement message. Pick the channel based on what the contact has:

- ✅ Has phone, not sms_unsubscribed → **SMS** (short, casual)
- ✅ Has email, not email_unsubscribed → **Email** (slightly longer, can reference the deal)
- ❌ Both unsubscribed → flag the opportunity for manual review, don't draft

If `days_silent` is past ~90, treat it as list reactivation, not a routine chase (business-method.md §10.3): a shorter, fresher-angle message, and flag to the operator that this segment is a worked-list candidate rather than a live deal.

**Each draft must include:**

- **The contact's first name** (from `contact.first_name`) — never "Hi there" or "Hello"
- **A specific reference** — what they were looking at, when, where the conversation left off. Use `stage`, `lead_source`, and `days_silent` to construct the reference. Examples:
  - Stage "Demo Booked", silent 14 days → "wanted to circle back on the demo we never got to"
  - Stage "Not Ready Yet", silent 30 days → "checking in — last we spoke you weren't ready to move forward yet, but timing changes"
  - Stage "Quote Sent", silent 7 days → "just making sure the proposal landed and you've had a chance to look"
- **One specific next-step ask** — "want me to send through some times" / "happy to redo numbers if anything's shifted" / "can I send a 2-min loom walking through it"
- **Tone matched to the operator's CLAUDE.md preferences** — see the operator's template for voice rules

**Each draft must NOT include:**

- ❌ Anything formal ("Dear Mr Smith") — use first name
- ❌ Templates that read like they were sent to 50 people
- ❌ Apologies ("sorry for the long silence") — they don't care, they probably forgot too
- ❌ "Just following up" — banned. Always anchor to something specific.
- ❌ Marketing language ("excited to share", "leverage", "synergy")
- ❌ A scheduler link unless the operator's CLAUDE.md explicitly approves it (per their banned-phrase rules)

## Step 4 — Present each draft for approval, one at a time

Format each as:

```
─────────────────────────────
🎯 Item N of M — <name>
   Silent: N days | Stage: <stage> | Source: <lead_source> | Value: $N
   Channel: <SMS | Email>
─────────────────────────────

[Subject line if email]

[Draft body]

[Y/N/edit/skip?]
```

The operator answers per-item. Don't batch. Don't bulk-send. Confirmation is per-message.

When the operator says yes:
- SMS → call the `send_sms` tool on the TrustPager MCP
- Email → call `send_email` (mode: "personal" — see the operator's email-sending preferences)
- Then log the activity on the opportunity via `add_note` so the next sweep doesn't surface it again

When the operator says no or skip:
- Don't log anything — the opportunity stays silent for next time
- Move to the next item

When the operator says edit:
- Take their edits inline, present the revised draft, ask again

## Step 5 — End with the operator's choice

After all N items:

```
✓ Sent: X | Skipped: Y | Edited and sent: Z

Want to drill into the remaining N silent opportunities? Run with --top 20.
```

## What to never do

- ❌ Never send any message without explicit per-item operator approval
- ❌ Never use the same template across multiple drafts — each one personalised
- ❌ Never include a deal's value in the message ("you were looking at the $12k package")
- ❌ Never reference internal stage names ("you're in our 'Not Ready Yet' stage") — translate to the customer's experience
- ❌ Never assume the contact remembers what was discussed — anchor to specifics they would recognise

## Common follow-ups the operator will ask

Be ready to chain naturally into:

- "Show me the next 10" → re-run with `--top 20` and pick up where you stopped
- "Skip Facebook leads, just show me referrals" → filter the items by `lead_source`
- "Move this one to Lost" → call `update_opportunity` with `status: "lost"`
- "Schedule a call with this one instead" → use the scheduling MCP tools

## When this skill should NOT fire

- The operator is mid-call and asking a focused question about one contact — answer that, don't pivot
- It's the first time today the operator has run this — but they ran it yesterday — show only changes since yesterday's run (use `~/.claude/bos-cache/follow-up-radar-state.json` if you maintain state)
- The operator already has 50+ scheduled outbound today — flag that instead of adding more

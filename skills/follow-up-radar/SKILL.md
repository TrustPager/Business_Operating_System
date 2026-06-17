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
---

# Follow-up Radar

You are surfacing the active opportunities that have gone quiet and drafting personalised re-engagement messages for each one. Your goal: turn a backlog of forgotten deals into a queue of approved-and-ready outbound messages in under 5 minutes.

## Step 1 — Pull the data (MCP reads)

Use the `trustpager` MCP server. All reads — free, nothing journaled.

| Need | Tool | Args |
|---|---|---|
| Opportunities (to find the silent ones) | `list_deals` | `limit: 100` |
| Contact details for each top silent opp (enrichment) | `get_contact` | `contact_id: <id>` — one per top-N opp, fired in parallel |

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

## Step 2 — Find the silent opportunities (digest logic)

Compute everything against **now**. From the opportunities list, keep an opportunity as **silent** only if **all** of these hold:

1. **It's active** — its `status` is NOT one of `won` / `lost` / `cancelled` / `abandoned` / `archived`, AND its current stage is not flagged `is_won_stage` or `is_lost_stage`. (Current stage = the first placement's pipeline stage; if there are no placements, treat as active/"Unstaged".)
2. **No scheduled future action** — there's no `next_action_date`, or it's in the past. A future `next_action_date` means it's in progress, not quiet — drop it.
3. **Gone quiet** — `updated_at` is more than **7 days** ago (the default silence threshold; the operator can ask for a different window, e.g. 14 days).

For each silent opp, compute `days_silent` = whole days since `updated_at`.

**Rank by a blended score** (so fully-priced deals don't dominate and unpriced-but-long-silent leads don't vanish — most opps have `value=null`):

```
base  = max(100, value_in_dollars / 1000)      # floor at 100 so unpriced deals still have pull
score = base * (1 + days_silent / 30)
```

Sort silent opps by `score`, highest first.

**Summaries for the headline:** count the silent opps grouped by `lead_source`, and grouped by stage name.

**Top N:** take the top **10** by score (the operator can ask for more — "show me the next 10" → take the top 20 and continue past where you stopped). Enrich only these top N — call `get_contact` for each one's `contact_id` in parallel, pulling `first_name`, `last_name`, `email`, `phone`, `job_title`, and the unsubscribe flags (`email_unsubscribed` / `sms_unsubscribed`).

## Step 3 — Open with a summary, not a wall of detail

Start with one paragraph the operator can read in 10 seconds, populated from the group-by summaries:

```
You've got X silent opportunities in your active pipeline. Most are coming from [top lead source],
mostly sitting in [top stage]. Here are the top N to chase, with drafts ready.
```

This sets context BEFORE the operator dives into individual messages.

## Step 4 — Draft a personalised message for each

For each top-N item, draft ONE re-engagement message. Pick the channel based on what the contact has:

- ✅ Has phone, not `sms_unsubscribed` → **SMS** (short, casual)
- ✅ Has email, not `email_unsubscribed` → **Email** (slightly longer, can reference the deal)
- ❌ Both unsubscribed → flag the opportunity for manual review, don't draft

**Each draft must include:**

- **The contact's first name** — never "Hi there" or "Hello"
- **A specific reference** — what they were looking at, when, where the conversation left off. Use `stage`, `lead_source`, and `days_silent` to construct it. Examples:
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

## Step 5 — Present each draft for approval, one at a time

Every send here is a write — it follows [`knowledge/safeguards.md`](../../knowledge/safeguards.md): show the draft, get a per-item yes, then send; journal each send as one line to `.bos-journal.md`; if a send returns a `202`/`approval_id`, surface the approvals link and stop (don't retry).

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
- SMS → `send_sms` on the `trustpager` MCP server
- Email → `send_email` (mode: "personal" — see the operator's email-sending preferences)
- Then log the activity on the opportunity via `add_note` so the next sweep doesn't surface it again
- Journal both the send and the note to `.bos-journal.md`

When the operator says no or skip: don't log anything — the opportunity stays silent for next time. Move to the next item.

When the operator says edit: take their edits inline, present the revised draft, ask again.

## Step 6 — End with the operator's choice

After all N items:

```
✓ Sent: X | Skipped: Y | Edited and sent: Z

Want to drill into the remaining N silent opportunities? (I'll take the next 10 by score.)
```

## What to never do

- ❌ Never send any message without explicit per-item operator approval
- ❌ Never use the same template across multiple drafts — each one personalised
- ❌ Never include a deal's value in the message ("you were looking at the $12k package")
- ❌ Never reference internal stage names ("you're in our 'Not Ready Yet' stage") — translate to the customer's experience
- ❌ Never assume the contact remembers what was discussed — anchor to specifics they would recognise

## Common follow-ups the operator will ask

- "Show me the next 10" → take the next 10 silent opps by score and pick up where you stopped
- "Skip Facebook leads, just show me referrals" → filter the items by `lead_source`
- "Move this one to Lost" → `update_deal` with `status: "lost"` (a write — journal it)
- "Schedule a call with this one instead" → use the scheduling MCP tools

## When this skill should NOT fire

- The operator is mid-call and asking a focused question about one contact — answer that, don't pivot
- The operator already has 50+ scheduled outbound today — flag that instead of adding more

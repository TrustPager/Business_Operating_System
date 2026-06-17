---
name: log-this-call
description: Log the call you just had — captures the recap, updates the opportunity, schedules the next step, and notifies anyone who needs to know.
triggers:
  - log this call
  - log my call
  - just got off the phone
  - call recap
  - record this call
  - I just spoke to
  - just hung up
  - log a call
---

# /log-this-call

After every customer call, three things need to happen and almost always don't:
1. The CRM gets a useful recap (not "had a chat — call again next week")
2. The opportunity moves to the right stage or gets a clear next action
3. The next step is scheduled so it doesn't get forgotten

This skill captures all three from a single conversation with the operator.

## Step 1 — Identify the context (MCP calls)

If the operator didn't say who they spoke to:

> "Who did you just speak to? (name, phone, or opportunity name)"

Once you have a name, phone, or email, resolve the contact on the `trustpager` MCP server. Pick the lookup tool by what the operator gave you:

| Identifier given | Tool | Args |
|---|---|---|
| A phone number (digits, optional `+`) | `search_contacts` | `phone: "<number>"`, `limit: 5` |
| An email (contains `@`) | `search_contacts` | `email: "<email>"`, `limit: 5` |
| A name / anything else | `search_contacts` | `search: "<text>"`, `limit: 5` |

Take the **best match** (first candidate). Then pull their context with these **parallel reads** off that contact id:

| Need | Tool | Args |
|---|---|---|
| The contact's open opportunities + stage | `get_contact_deals` | `id: <contact_id>`, `limit: 10` |
| Recent activity on the contact | `get_contact_activities` | `id: <contact_id>`, `limit: 10` |

From the opportunities, keep only the **open** ones — status not in `won` / `lost` / `cancelled` / `abandoned`. For the **top open opportunity** (most-recently-touched), also pull its open tasks with `get_deal_tasks` (`id: <opportunity_id>`, `limit: 10`) and keep only tasks with no completion time.

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

If multiple contacts matched: present a numbered list and ask which one. If the chosen contact has multiple open opportunities, ask which one — default to the most-recently-touched. All of the above are reads — nothing here is journaled or needs approval.

## Step 2 — Capture the recap

Walk the operator through 4 structured questions, ONE AT A TIME:

1. **What did you discuss?** (the substance — not "we chatted")
2. **What's their position now?** (more interested / less interested / parked / decided)
3. **What did you agree on?** (the action they're taking, or the action you're taking)
4. **When's the next contact?** (specific day if possible)

Don't dump all four at once. Wait for each answer before asking the next. Each answer is one short prompt to the operator.

## Step 3 — Update the workspace

Anything in this step writes — follow the rails in `knowledge/safeguards.md` (journal each write to `.bos-journal.md`; a `202`/`approval_id` response means queued — surface the link and stop, don't retry).

Build a single structured note and post it via `add_note` on the opportunity (`trustpager` MCP server). Body shape:

```
📞 Call with {contact_name} — {duration_or_just_now}

Discussed:
- {discussed_points}

Their position: {their_position}

Agreed: {agreed_action}

Next contact: {next_date} — {next_action}
```

Then, based on their stated position:
- **More interested** → suggest moving the opportunity to the next stage. Show: "Move to **Quote Sent** stage? (y/n)" — on yes, `move_opportunity_card`.
- **Less interested / parked** → suggest adding a follow-up task for the next contact date.
- **Decided** → ask "Won or lost?" and either `move_opportunity_card` to a won stage, or `update_deal` to mark it lost with a reason.
- ALWAYS create a task for the next contact date via `create_task`, with the agreed action as the title.

Journal each of these writes (`add_note`, `move_opportunity_card`, `update_deal`, `create_task`) as one line in `.bos-journal.md` (timestamp, tool, outcome, id, `skill: log-this-call`).

## Step 4 — Notify the right people

If the opportunity has other assigned users (check via `list_deal_users` on the `trustpager` server):

> "This opp has {N} other people on it. Notify them?"

If yes: send an internal summary — `send_email` to the assigned users, or create a task that mentions them. This is an outbound write: show the draft, get approval, then journal it (safeguards).

## Important behaviours

- **Never fabricate.** If the operator gave a one-liner, the note is a one-liner. Don't pad it.
- **Quote the operator verbatim** for "their position" and "agreed" — these are factual claims that may matter later.
- **No emojis in the note BODY** except the leading 📞. Customer-facing tone, not chat tone.
- **Stage moves are suggestions.** Always confirm before moving. Never silently auto-move.
- **One task per call, max.** Don't auto-create three tasks because the conversation mentioned three things. Pick the agreed next step.

## Output shape

End with one line: "Logged. Note added to {opp_name}, task '{task_title}' scheduled for {date}, stage moved to {stage}."

If the operator only had time for 2 of the 4 questions, log what we have and say so: "Logged partial — discussed + agreed. Their-position and next-contact left blank. /log-this-call again when you have a sec to fill those in."

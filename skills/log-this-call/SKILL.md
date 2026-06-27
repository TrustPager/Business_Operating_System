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
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__add_note
  - mcp__trustpager__move_opportunity_card
  - mcp__trustpager__create_task
  - mcp__trustpager__send_email
status: active
---

# /log-this-call

After every customer call, three things need to happen and almost always don't:
1. The CRM gets a useful recap (not "had a chat — call again next week")
2. The opportunity moves to the right stage or gets a clear next action
3. The next step is scheduled so it doesn't get forgotten

This skill captures all three from a single conversation with the user.

## Step 1 — Identify the context

If the user didn't say who they spoke to:

> "Who did you just speak to? (name, phone, or opportunity name)"

Once you have a name, phone, or email, run:

```
python ~/.claude/bos-run.py log-this-call --query "<what they said>"
```

The returned JSON gives you the matched contact(s), their open opportunities (with stage), recent activities, and open tasks — all in one call. No need to chain `search_contacts` + `list_contact_deals` + `get_opportunity_activities` separately.

If multiple contacts matched: present a numbered list and ask which one. If the chosen contact has multiple open opportunities, ask which one. Default to the most-recently-touched.

## Step 2 — Capture the recap

Walk the user through 4 structured questions, ONE AT A TIME:

1. **What did you discuss?** (the substance — not "we chatted")
2. **What's their position now?** (more interested / less interested / parked / decided)
3. **What did you agree on?** (the action they're taking, or the action you're taking)
4. **When's the next contact?** (specific day if possible)

Don't dump all four at once. Wait for each answer before asking the next. Each answer is one short prompt to the user.

## Step 3 — Update the workspace

Build a single structured note and post it via `mcp__trustpager__add_note` on the opportunity. Body shape:

```
📞 Call with {contact_name} — {duration_or_just_now}

Discussed:
- {discussed_points}

Their position: {their_position}

Agreed: {agreed_action}

Next contact: {next_date} — {next_action}
```

Also:
- If they said "more interested" → suggest moving the opportunity to the next stage. Show: "Move to **Quote Sent** stage? (y/n)"
- If they said "less interested" or "parked" → suggest adding a follow-up task for the next contact date.
- If they said "decided" → ask "Won or lost?" and either move to a won stage (`mcp__trustpager__move_opportunity_card`) or mark lost.
- ALWAYS create a task for the next contact date (`mcp__trustpager__create_task`) with the agreed action as the title.

## Step 4 — Notify the right people

If the opportunity has other assigned users:
> "This opp has {N} other people on it. Notify them?"

If yes: send an internal email summary (use `mcp__trustpager__send_email` with `mode: "internal"` if available, else a task with a mention).

## Important behaviours

- **Never fabricate.** If the user gave a one-liner, the note is a one-liner. Don't pad it.
- **Quote the user verbatim** for "their position" and "agreed" — these are factual claims that may matter later.
- **No emojis in the note BODY** except the leading 📞. Customer-facing tone, not chat tone.
- **Stage moves are suggestions.** Always confirm with the user before moving. Never silently auto-move.
- **One task per call, max.** Don't auto-create three tasks because the conversation mentioned three things. Pick the agreed next step.

## Output shape

End with one line: "Logged. Note added to {opp_name}, task '{task_title}' scheduled for {date}, stage moved to {stage}."

If the user only had time for 2 of the 4 questions, log what we have and say so: "Logged partial — discussed + agreed. Their-position and next-contact left blank. /log-this-call again when you have a sec to fill those in."

---
name: draft-reply
description: Draft a reply to an email or SMS you received — pulls the context, writes the response in your tone, shows it for your approval.
triggers:
  - draft a reply
  - reply to
  - help me respond to
  - draft a response
  - what should I say to
  - how should I respond
  - write a reply
  - draft me a response
---

# /draft-reply

Replies are higher-stakes than fresh emails — the context already exists, and getting the tone wrong is more obvious. This skill drafts the reply against the actual message that was received, not against a guess.

## Step 1 — Find the message being replied to (parallel MCP reads)

If the user pastes a message directly, use that paste as the source-of-truth and skip the fetch entirely.

Otherwise, pull the candidate inbound from the `trustpager` MCP server. These are reads — free, nothing journaled:

| Need | Tool | Args |
|---|---|---|
| Inbound email threads | `list_email_threads` | `direction: "inbound"`, `is_read: false`, `limit: 50` |
| SMS conversations | `list_sms_conversations` | (none — returns all) |

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

Then filter and rank client-side (the list tools don't take a date or "we-replied" filter, so do it yourself):

- **Window:** keep only items whose last-message time is within the last **48 hours** (default).
- **Email — needs a reply:** the thread's last message direction is **inbound** and we haven't already replied (the latest message is theirs, not ours). Skip `is_automated` threads.
- **SMS — needs a reply:** there's an inbound message **newer than** the latest outbound message. If the last outbound is at or after the last inbound, we've already replied — skip it.
- **Rank:** opportunity-linked senders first (a thread/conversation carrying a `deal_id`), then newest-first by last-message time.

For each kept item capture: channel, the thread/conversation id, sender name + email/phone, received-at, whether it's linked to an open opportunity (`deal_id`), the contact id, and a ~200-char snippet of the latest inbound message.

If the user already named someone, filter the list to them and pick that one. If not, offer the top 3–5 as a numbered list:

> "These are the unanswered messages from the last 48h, top first. Reply to #1? Or pick another?"

## Step 2 — Read the inbound carefully

Before drafting, identify in the inbound:
- **What they're asking** — a question, a request, an objection, a confirmation, an emotional venting?
- **The emotional register** — formal? casual? frustrated? excited?
- **Specific details** — names, dates, dollar amounts, products mentioned — these must appear in the reply.

If the snippet isn't enough context, pull the full thread (`get_email_thread` / `get_sms_messages`) before drafting. If still unclear ("I'm not sure what they're actually asking"), say so and ask BEFORE drafting:
> "I'm reading this as a request for [X] — is that right, or are they actually asking [Y]?"

## Step 3 — Draft the reply

- **Acknowledge first, then answer.** If they raised a concern, name the concern before responding to it. ("Totally hear you on the timing — here's what we can do…")
- **Match their tone.** They were casual? Be casual back. They were formal? Don't get matey.
- **Answer the question they asked**, not a question you wish they'd asked. If they asked "is it $5k or $7k?" the reply leads with the number, not with how the pricing works.
- **One next step.** Like /send-email, end with one clear ask.
- **No fake enthusiasm.** "Great question!" / "Love this!" / "So excited to hear from you!" — banned.

If the inbound has multiple questions, address them in bullet order. Keep the same structure they used so the reply maps obviously to their email.

## Step 4 — Show + send

This is a write — it follows [`knowledge/safeguards.md`](../../knowledge/safeguards.md): show the draft, wait for an explicit yes, then send; journal the send as one line to `.bos-journal.md`. If the send returns a `202`/`approval_id`, surface the approvals link and stop — don't retry.

- Show the proposed reply (subject = same as inbound prepended with "Re:", or just the SMS body)
- Wait for yes/no
- On yes: `reply_to_email` (for email — preserves the thread) or `send_sms` (for SMS)
- On no: ask what to change. Common edits: "more direct", "less formal", "shorter", "include the dollar number".

**Search-first / never blind-retry:** if a send errors ambiguously or times out, don't just re-issue it — re-pull the thread/conversation to confirm whether the reply actually landed, then act on what you find. A duplicate reply is worse than a slow one.

## Important behaviours

- **Never invent facts.** If they asked "what's the price?" and you don't know, the reply says "Let me confirm and come back to you today" — not a made-up number.
- **Threading matters.** Email replies must use `reply_to_email` (preserves the thread), not `send_email` to the same address (breaks threading).
- **CCs in the reply.** Preserve the inbound's CC list unless the user removes one. Don't silently drop CCs.
- **The user is the final filter.** Even after edits, every send is approved.

## Output shape

"Replied to {sender} on '{subject}' — logged on {opp_name if linked}."

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

## Step 1 — Find the message being replied to

Ask the user (if not obvious from their request):
> "Which message do you want to reply to? Paste the latest, or give me the sender / opportunity name."

Then locate:
- If paste → use the pasted body as the source-of-truth.
- If sender name → `mcp__trustpager__list_email_threads` filtered by contact, take the most recent thread with an unanswered inbound.
- If opportunity → `mcp__trustpager__list_email_threads` filtered by opportunity, find the latest inbound.

For SMS: `mcp__trustpager__get_sms_conversation` to pull the thread.

## Step 2 — Read the inbound carefully

Before drafting, identify in the inbound:
- **What they're asking** — a question, a request, an objection, a confirmation, an emotional venting?
- **The emotional register** — formal? casual? frustrated? excited?
- **Specific details** — names, dates, dollar amounts, products mentioned — these must appear in the reply.

If unclear ("I'm not sure what they're actually asking"), say so to the user and ask for clarification BEFORE drafting:
> "I'm reading this as a request for [X] — is that right, or are they actually asking [Y]?"

## Step 3 — Draft the reply

- **Acknowledge first, then answer.** If they raised a concern, name the concern before responding to it. ("Totally hear you on the timing — here's what we can do…")
- **Match their tone.** They were casual? Be casual back. They were formal? Don't get matey.
- **Answer the question they asked**, not a question you wish they'd asked. If they asked "is it $5k or $7k?" the reply leads with the number, not with how the pricing works.
- **One next step.** Like /send-email, end with one clear ask.
- **No fake enthusiasm.** "Great question!" / "Love this!" / "So excited to hear from you!" — banned.

If the inbound has multiple questions, address them in bullet order. Keep the same structure they used so the reply maps obviously to their email.

## Step 4 — Show + send

Same approval flow as /send-email:
- Show the proposed reply (subject = same as inbound prepended with "Re:", or just the SMS body)
- Wait for yes/no
- On yes: `mcp__trustpager__reply_to_email` (for email) or `mcp__trustpager__send_sms` (for SMS)
- On no: ask what to change. Common edits: "more direct", "less formal", "shorter", "include the dollar number".

## Important behaviours

- **Never invent facts.** If they asked "what's the price?" and you don't know, the reply says "Let me confirm and come back to you today" — not a made-up number.
- **Threading matters.** Email replies must use `reply_to_email` (preserves the thread), not `send_email` to the same address (breaks threading).
- **CCs in the reply.** Preserve the inbound's CC list unless the user removes one. Don't silently drop CCs.
- **The user is the final filter.** Even after edits, every send is approved.

## Output shape

"Replied to {sender} on '{subject}' — logged on {opp_name if linked}."

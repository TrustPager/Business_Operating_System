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
function_slot: comms
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__reply_to_email
  - mcp__trustpager__send_sms
status: active
produces_customer_facing_copy: true
---

# /draft-reply

Replies are higher-stakes than fresh emails — the context already exists, and getting the tone wrong is more obvious. This skill drafts the reply against the actual message that was received, not against a guess.

## Step 1 — Find the message being replied to

First, run:

```
python ~/.claude/bos-run.py draft-reply --hours 48
```

This returns every inbound email + SMS in the window with no reply, ranked (open-opportunity senders first, then by recency). If the user already named someone, filter the list and pick that one. If not, offer the top 3-5 as a numbered list:

> "These are the unanswered messages from the last 48h, top first. Reply to #1? Or pick another?"

If the user pastes a message directly (not from the JSON), use that paste as the source-of-truth and skip the fetch.

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

- **Content guardrails.** Customer-facing copy uses no em dashes, invents no facts, quotes, or numbers, and names no third-party vendor. Write it in the owner's brand voice; the framing and the marketing psychology are the owner's choice. The rules are in `knowledge/content-rules.md`.
- **When you don't know, say so.** If they asked "what's the price?" and you don't know, the reply says "Let me confirm and come back to you today."
- **Objections and 'no's have doctrine.** If the inbound is a price objection or a decline, read business-method.md §9.4 and §12.5 before drafting: never offer the same thing cheaper; a genuine alternative changes scope or payment shape. Restate their concern in the reply before answering it.
- **Threading matters.** Email replies must use `reply_to_email` (preserves the thread), not `send_email` to the same address (breaks threading).
- **CCs in the reply.** Preserve the inbound's CC list unless the user removes one. Don't silently drop CCs.
- **The user is the final filter.** Even after edits, every send is approved.

## Output shape

"Replied to {sender} on '{subject}' — logged on {opp_name if linked}."

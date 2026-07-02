---
name: send-email
description: Send a TrustPager email — picks the right config, drafts the body in your tone, attaches anything relevant, and gets your approval before it goes.
triggers:
  - send an email
  - email this person
  - send an email to
  - send a follow-up email
  - shoot them an email
  - email them
  - draft and send an email
  - reply via email
function_slot: comms
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__send_email
  - mcp__trustpager__reply_to_email
  - mcp__trustpager__list_opportunity_files
  - mcp__trustpager__schedule_communication
status: active
---

# /send-email

Every outbound email needs to be in your tone, on the right thread, signed correctly, and reviewed before it goes. This skill wraps `mcp__trustpager__send_email` with all of that — you say "email Sarah about the quote" and you get a draft, not a fait accompli.

## Step 1 — Identify the recipient + reason

If the user didn't say WHO and WHAT:
- WHO: ask for name, email, or opportunity. Same lookup logic as /log-this-call.
- WHAT: ask for the reason in 1-2 sentences. Use this as the brief, not the message.

If the user said "follow up on the quote" but you don't see a quote in the opportunity, ask: "I don't see a quote attached to this opp — is the quote elsewhere, or are we asking about it?"

## Step 2 — Pull context

Once you have the contact (and optionally opportunity), run:

```
python ~/.claude/bos-run.py send-email --contact-id <id> [--opportunity-id <id>]
```

The returned JSON gives you everything you need to draft well: the contact, the opportunity (if linked), every recent email thread WITH this contact, the last few sent emails by the workspace (for tone calibration), and the active email config.

If there's an existing thread with this contact, REPLY to that thread (use `mcp__trustpager__reply_to_email`). Don't start a new thread unless asked.

## Step 3 — Draft

Body rules:
- **First-name address** ("Hi Sarah,") never "Hi there"
- **Reference one concrete thing** from the context — the opp name, last call, last email, what they asked about
- **One main message** per email. If the user wants 3 things said, ask if they should be separate emails or numbered points.
- **One clear ask at the end** — never "Let me know your thoughts!" or "Looking forward to your response!"
- **Match the workspace tone** — short, no-jargon, no buzzwords, no exclamation points. Read 3 recent sent emails first.

Subject line:
- If replying: use the existing subject ("Re: ...").
- If new thread: short, specific, ≤ 60 chars. "Quote for [property address]" not "Following up on our conversation."

Signature:
- Use whatever signature is already configured in the workspace email config.
- DO NOT manually add a signature in the body.

## Step 4 — Show and approve

Show the user:
- To, CC, BCC (if any)
- Subject
- Body
- "Send via {email_config_name} (sender: {your_email})"

Wait for explicit yes/no. On yes, `mcp__trustpager__send_email`. On no, ask what to change.

## Important behaviours

- **Customer-facing copy: NO em dashes, outcome-led.** The email is customer-facing output: no em dashes anywhere (use commas, colons, parentheses, or separate sentences), and frame around what the recipient gets, not the problem. Check the draft before showing it.
- **One email per /send-email invocation.** Don't queue up a batch.
- **Internal CCs are not implicit.** If the opp has other assigned users, ASK before CCing them.
- **Attachments.** If the user mentions an attachment ("send the quote"), look for opportunity files first — `mcp__trustpager__list_opportunity_files`. If found, include the right one. If not found, ASK before drafting.
- **No vague pronouns.** "The quote" must resolve to a specific file. "Your account manager" must resolve to a named person.
- **Quiet hours.** Before 7am / after 8pm in recipient timezone (or unknown) → ask "send now, or schedule for 8am?" Use `mcp__trustpager__schedule_communication` if scheduling.

## Output shape

After send: one line. "Sent to {recipient} — subject '{subject}'. Logged on {opp_name}."

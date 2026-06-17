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
---

# /send-email

Every outbound email needs to be in your tone, on the right thread, signed correctly, and reviewed before it goes. This skill wraps `send_email` (on the `trustpager` MCP server) with all of that — you say "email Sarah about the quote" and you get a draft, not a fait accompli.

## Step 1 — Identify the recipient + reason

If the operator didn't say WHO and WHAT:
- WHO: ask for name, email, or opportunity, then resolve the contact with `search_contacts` (`search` / `email` / `phone`, `limit: 5`) on the `trustpager` server — same lookup logic as `/log-this-call`.
- WHAT: ask for the reason in 1-2 sentences. Use this as the brief, not the message.

If the operator said "follow up on the quote" but you don't see a quote on the opportunity, ask: "I don't see a quote attached to this opp — is the quote elsewhere, or are we asking about it?"

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

## Step 2 — Pull context (parallel MCP reads)

Once you have the contact id (and optionally the opportunity id), pull everything you need to draft well in one parallel batch off the `trustpager` server. All free reads:

| Need | Tool | Args |
|---|---|---|
| The contact's full record | `get_contact` | `id: <contact_id>` |
| Recent threads WITH this contact (reply vs. new) | `list_email_threads` | `contact_id: <contact_id>`, `limit: 5` |
| Recent sent emails (tone calibration) | `list_email_threads` | `direction: "outbound"`, `limit: 5`, sorted by last message desc |
| Which sender + signature to use | `get_email_capabilities` | — |
| Available email configs | `list_email_configs` | — |
| The opportunity (only if one is linked) | `get_deal` | `id: <opportunity_id>` |

Pick the **active email config**: the one flagged default, else the first returned.

If there's an existing thread with this contact, **REPLY to that thread** with `reply_to_email`. Don't start a new thread unless asked.

## Step 3 — Draft

Body rules:
- **First-name address** ("Hi Sarah,") never "Hi there".
- **Reference one concrete thing** from the context — the opp name, last call, last email, what they asked about.
- **One main message** per email. If the operator wants 3 things said, ask if they should be separate emails or numbered points.
- **One clear ask at the end** — never "Let me know your thoughts!" or "Looking forward to your response!".
- **Match the workspace tone** — short, no jargon, no buzzwords, no exclamation points. Read the 3 recent sent emails first.

Subject line:
- If replying: use the existing subject ("Re: ...").
- If new thread: short, specific, ≤ 60 chars. "Quote for [property address]" not "Following up on our conversation."

Signature:
- Use whatever signature is already configured in the workspace email config.
- DO NOT manually add a signature in the body.

## Step 4 — Show and approve

This is an outbound send — follow the rails in `knowledge/safeguards.md`. Show the operator:
- To, CC, BCC (if any)
- Subject
- Body
- "Send via {email_config_name} (sender: {your_email})"

Wait for explicit yes/no. Before sending, a quick `list_email_threads` check confirms you're not duplicating a message already sent (idempotency — never blind-send). On yes:
- New thread → `send_email`; replying to an existing thread → `reply_to_email`.
- If the send returns `202` / `approval_id`, surface the approvals link and stop — don't retry (safeguards §1).
- Append one line to `.bos-journal.md` (timestamp, tool, outcome, id, `skill: send-email`).

On no, ask what to change.

## Important behaviours

- **One email per /send-email invocation.** Don't queue up a batch.
- **Internal CCs are not implicit.** If the opp has other assigned users, ASK before CCing them.
- **Attachments.** If the operator mentions an attachment ("send the quote"), look for opportunity files first — `list_files` (filtered to the opportunity). If found, include the right one. If not found, ASK before drafting.
- **No vague pronouns.** "The quote" must resolve to a specific file. "Your account manager" must resolve to a named person.
- **Quiet hours.** Before 7am / after 8pm in recipient timezone (or unknown) → ask "send now, or schedule for 8am?" Use `schedule_communication` if scheduling (also a write — journal it).

## Output shape

After send: one line. "Sent to {recipient} — subject '{subject}'. Logged on {opp_name}."

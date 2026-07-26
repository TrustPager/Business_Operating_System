---
name: missed-call-recovery
description: Find recent missed calls, identify the caller, and draft a recovery SMS or callback message — one per missed call, ready to send.
triggers:
  - missed call
  - missed calls
  - calls I missed
  - who called me
  - recover missed calls
  - call back the people who tried me
  - someone tried to call earlier
  - any calls go to voicemail
function_slot: comms
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__send_sms
  - mcp__trustpager__send_email
status: active
produces_customer_facing_copy: true
---

# /missed-call-recovery

When someone misses a call, the longer the gap before a response, the lower the chance of recovery. This skill makes that gap as short as possible — pulls every recent missed call, looks up who it was (existing contact? opportunity? cold caller?), and drafts a per-call recovery message you can send with one approval. For locally bought businesses, answer speed is the first rung of the whole acquisition ladder, and usually IS the constraint (business-method.md §10.5): first responder wins the job.

## Step 1 — Pull the data

Run the fetch script. It returns every missed inbound call from the last 24h (configurable), enriched with:
- Phone number that called
- Whether we have a contact for that number
- Linked opportunity (if any) + current stage
- Whether the caller has been called back already since the missed call
- Time since the missed call

```
python ~/.claude/bos-run.py missed-call-recovery
```

Pass `--hours 48` for a longer window, or `--include-callbacks` to also surface calls that were already recovered (useful for reviewing the day's recovery work).

**Fallback if the script can't run** (auth/network): say so briefly, then pull the window by hand — `mcp__trustpager__list_phone_call_logs`, plus `get_contact_deals` per matched caller — and triage from that. Proceed with what you have.

**If TrustPager isn't connected at all:** say so plainly, then offer the keyless path — the owner reads you the missed numbers (or pastes their phone's call list) and you draft the recovery texts right in chat for them to send from their own phone.

## Step 2 — Triage and draft

For each missed call in the output, present a one-line summary to the user, then propose the recovery action:

| Caller type | Default recovery |
|---|---|
| Existing contact with open opportunity | "Sorry I missed your call — was about [opportunity name]?" SMS, then offer to schedule a callback. |
| Existing contact, no open opportunity | Friendly callback SMS. Ask what they were calling about. |
| Unknown number (no contact) | SMS asking if they were trying to reach the business. Do NOT create a contact yet — wait for a reply. |
| Caller already recovered | Skip silently. Don't ask the user. |

Use the contact's preferred channel if it's set on the record. Otherwise default to SMS for missed calls (faster than email).

## Step 3 — Send with approval

For each drafted message:
- Show the user: who, the phone number, the proposed message, the channel.
- Wait for explicit yes/no per message. NEVER batch-send.
- On yes: send via `mcp__trustpager__send_sms` (or `send_email` if email is the channel).
- On no: ask what to change (tone? length? skip?), or move on.

## Important behaviours

- **Content guardrails.** Customer-facing copy uses no em dashes, invents no facts, quotes, or numbers, and names no third-party vendor. Write it in the owner's brand voice; the framing and marketing psychology are the owner's choice. The rules are in `knowledge/content-rules.md`. The register for these messages is `knowledge/communication-voice.md`: plain, warm, short.
- **No fabrications.** If a missed call doesn't have a name attached, the draft must say "the number that called" — never invent a name.
- **No batching.** Each send is its own approval.
- **Quiet hours.** If the current time is before 7am or after 8pm in the recipient's timezone (or unknown), draft an email instead of SMS.
- **One recovery per number.** If the same number called multiple times and we've already recovered the first, treat the rest as resolved.
- **Don't open with "Sorry I missed your call" if they called more than 6 hours ago.** That feels insincere. Lead with "Hey, I saw your call earlier — what's up?" instead.
- **Make it standing, not manual.** If the operator runs this more than occasionally, the durable fix is an automatic missed-call text-back; offer `/automate-this` to wire it (§10.5, with the 60-second first touch as the aspiration, §10.3, directional). On the keyless path (TrustPager not connected), skip the automation offer.

## Output shape

The skill should end with a one-line summary: "Recovered N of M missed calls. K already had a callback. R skipped."

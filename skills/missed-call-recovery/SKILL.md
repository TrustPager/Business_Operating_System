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
---

# /missed-call-recovery

When someone misses a call, the longer the gap before a response, the lower the chance of recovery. This skill makes that gap as short as possible — pulls every recent missed call, looks up who it was (existing contact? opportunity? cold caller?), and drafts a per-call recovery message you can send with one approval.

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

- **No fabrications.** If a missed call doesn't have a name attached, the draft must say "the number that called" — never invent a name.
- **No batching.** Each send is its own approval.
- **Quiet hours.** If the current time is before 7am or after 8pm in the recipient's timezone (or unknown), draft an email instead of SMS.
- **One recovery per number.** If the same number called multiple times and we've already recovered the first, treat the rest as resolved.
- **Don't open with "Sorry I missed your call" if they called more than 6 hours ago.** That feels insincere. Lead with "Hey, I saw your call earlier — what's up?" instead.

## Output shape

The skill should end with a one-line summary: "Recovered N of M missed calls. K already had a callback. R skipped."

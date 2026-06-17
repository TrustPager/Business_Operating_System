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
---

# /missed-call-recovery

When someone misses a call, the longer the gap before a response, the lower the chance of recovery. This skill makes that gap as short as possible — pulls every recent missed call, looks up who it was (existing contact? opportunity? cold caller?), and drafts a per-call recovery message you can send with one approval.

## Step 1 — Pull the data (MCP calls)

Pull the call log off the `trustpager` MCP server:

| Need | Tool | Args |
|---|---|---|
| Recent phone call logs | `list_phone_call_logs` | `limit: 200` |

Default window is the **last 24 hours** (the operator can ask for 48h). Filter to that window yourself. All reads here are free.

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

## Step 2 — Find the missed inbound calls

A call is a **missed inbound** call when its direction is inbound/incoming AND either:
- its status/disposition (lowercased, `_`→`-`) is one of: `no-answer`, `missed`, `failed`, `busy`, `voicemail`, `abandoned`, `no-answer-machine`; **or**
- it's a heuristic miss: duration < 5 seconds AND no transcript/recording present.

Normalise each caller's number to its last 12 digits (keep a leading `+`). **Group missed calls by caller number** — multiple misses from the same number are one "session"; use the latest one as the representative.

**Detect already-recovered numbers.** A number is recovered if, *after* its latest missed call, the log shows either an **outbound** call to that number, or an **answered inbound** call (duration ≥ 5s) from it. By default, drop recovered numbers from the list (the operator can ask to include them for a review of the day's recovery work).

## Step 3 — Enrich each unique caller

For each unique missed-caller number, look up the contact and their context on the `trustpager` server (run these in parallel across callers):

| Need | Tool | Args |
|---|---|---|
| Contact for the number | `search_contacts` | `phone: "<number>"`, `limit: 1` |
| That contact's open opportunities + stage | `get_contact_deals` | `id: <contact_id>`, `limit: 5` |

Keep only **open** opportunities (status not in `won` / `lost` / `cancelled` / `abandoned`); use the most recent as the linked opportunity, capturing its name, value, and current stage.

**Rank the list:** known caller WITH an open opportunity first, then known caller (no open opp), then unknown number. Within each tier, most-recently-missed first.

## Step 4 — Triage and draft

For each missed call in the ranked list, present a one-line summary, then propose the recovery action:

| Caller type | Default recovery |
|---|---|
| Existing contact with open opportunity | "Sorry I missed your call — was about [opportunity name]?" SMS, then offer to schedule a callback. |
| Existing contact, no open opportunity | Friendly callback SMS. Ask what they were calling about. |
| Unknown number (no contact) | SMS asking if they were trying to reach the business. Do NOT create a contact yet — wait for a reply. |
| Caller already recovered | Skip silently. Don't ask the operator. |

Use the contact's preferred channel if set on the record; otherwise default to SMS for missed calls (faster than email).

## Step 5 — Send with approval

Sends are outward-facing — follow the rails in `knowledge/safeguards.md`: show the draft, get approval, **search first** so a re-run never double-texts, and **journal each send** to `.bos-journal.md`.

For each drafted message:
- Show the operator: who, the phone number, the proposed message, the channel.
- Wait for explicit yes/no **per message**. NEVER batch-send.
- On yes: send via `send_sms` (or `send_email` if email is the channel) on the `trustpager` server. If a send returns `202` / `approval_id`, surface the approvals link and stop — don't retry (safeguards §1).
- Append one line to `.bos-journal.md` per send (timestamp, tool, outcome, id, `skill: missed-call-recovery`).
- On no: ask what to change (tone? length? skip?), or move on.

## Important behaviours

- **No fabrications.** If a missed call doesn't have a name attached, the draft must say "the number that called" — never invent a name.
- **No batching.** Each send is its own approval.
- **Quiet hours.** If the current time is before 7am or after 8pm in the recipient's timezone (or unknown), draft an email instead of SMS.
- **One recovery per number.** If the same number called multiple times and we've already recovered the first, treat the rest as resolved.
- **Don't open with "Sorry I missed your call" if they called more than 6 hours ago.** That feels insincere. Lead with "Hey, I saw your call earlier — what's up?" instead.

## Output shape

End with a one-line summary: "Recovered N of M missed calls. K already had a callback. R skipped."

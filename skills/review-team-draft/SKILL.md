---
name: Review Team Draft
description: A manager reviews a team member's customer-facing draft before it ships: checks it's in the team voice and that what it claims has been verified, then approves it or returns it with a specific note. The human half of the verify-before-customer gate. Use when a teammate's draft is waiting for manager approval.
triggers:
  - review team drafts
  - any drafts waiting for me
  - review sarah's draft
  - approve team draft
  - check the drafts queue
function_slot: comms
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - get_opportunity
  - get_contact
status: active
---

# Review Team Draft

When team members in an approval-only role draft customer messages, those drafts
wait for a manager before they send (see `templates/team-standards.md` sections
3-4). This skill is that review: voice + verified, then approve or return.

## Step 1 — List what's waiting

Team drafts awaiting review live in the shared drafts registry at
`./team/_drafts/` (each entry: who drafted it, when, the linked record, the
channel, and the approval rule that sent it here). List the pending ones,
**highest-value opportunity and oldest first**, with a one-line summary each. If
the folder is empty, say "no drafts waiting" and stop.

(If your team doesn't use the local registry yet, a draft can also be pasted
straight in for review — run the same checks in Steps 3-4 on it.)

## Step 2 — Show the draft + its context

Show the full draft, who wrote it, and the record it's about. Pull the linked
opportunity/contact so you can judge whether the message fits the situation
(`get_opportunity` / `get_contact`).

## Step 3 — Check it against the two bars

1. **Verified?** Has the thing the draft claims (a fix, a feature, an outcome)
   been confirmed working? Check the draft's note / linked record for evidence,
   or that the author ran the smoke test. If it claims something works and
   nothing confirms it, that's an automatic return (`knowledge/safeguards.md`).
2. **Team voice?** Score it against `knowledge/communication-voice.md`: leads
   with the outcome, one plain sentence, one clean usage instruction (raw URL +
   one action, not a list of steps), no jargon/post-mortem, no "test this"
   (customers use), no hedging, short. Note any miss specifically.

## Step 4 — Approve or return

- **Approve** → if the channel is email/SMS and the operator says send, send it
  (respect approval gates: a 202 surfaces the platform approval link). Otherwise
  mark it ready in the registry for the author to send. Move the entry to
  `./team/_drafts/_approved/`.
- **Return** → write a specific, kind note to the author: exactly what to change
  and why (cite the voice rule or the missing verification). Move the entry to
  `./team/_drafts/_returned/` with the note. Don't rewrite it for them silently;
  the point is the author learns the standard.

## Step 5 — Confirm

```
Reviewed 3 drafts:
  ✓ Sarah → "Acme booking fixed" — approved + sent (in voice, fix verified)
  ↩ Bob → "Invoice issue" — returned: leads with a technical explanation; needs
     one-line outcome + the link to view it. Not yet confirmed the invoice shows.
  • 1 still waiting (Sarah → "XYZ follow-up")
```

## Hard rules
- ❌ Never approve a draft whose claim isn't confirmed working. Return it.
- ❌ Don't silently rewrite a returned draft — give the author the specific fix so they learn it.
- ❌ Don't route around a platform approval gate (202 = queued; surface it).
- ✅ Judge voice against `knowledge/communication-voice.md`, every time.
- ✅ Highest-value + oldest drafts first.

## Output shape
A short list of the drafts reviewed with a one-line verdict each (approved+sent /
approved-ready / returned-with-reason), and how many remain.

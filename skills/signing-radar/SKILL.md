---
name: Signing Radar
description: Show where every document you sent for signing stands — the sent → opened → signed funnel, who opened but hasn't signed (follow up now), who never opened and is going stale (chase), and who declined. Surfaces the hottest follow-ups first.
triggers:
  - signing radar
  - who hasn't signed
  - check my signing documents
  - which contracts are outstanding
  - who opened but didn't sign
  - chase unsigned documents
  - signing status
  - what's outstanding for signature
---

# Signing Radar

Owners send documents for signing and then lose the thread — they don't notice
the proposal a client opened twice but never signed, or the agreement that's sat
unopened for a week. This is the regular check-up on every envelope.

**The two buckets that matter most:**
- **Opened but not signed** — they're engaged and holding. The single best
  moment to follow up. This is what the InsureHQ-style "call them while it's
  hot" play runs on.
- **Sent but never opened, going stale** — chase it or it quietly dies.

Source of truth: [`knowledge/document-method.md`](../../knowledge/document-method.md)
— §3 (the envelope lifecycle) and §4 (the open/sign signals).

## Step 1 — Fetch the digest

```bash
python skills/signing-radar/fetch.py
```

One call: lists every envelope, computes the funnel, and buckets the follow-ups
(opened-not-signed, sent-never-opened-stale, declined, recently completed),
oldest-first. Pass `--stale-days N` to change when "sent but unopened" counts as
stale (default 5).

If the script can't run (auth/network), fall back to
`mcp__trustpager__list_signing_envelopes` — but that's the raw list with no
funnel; prefer the script.

## Step 2 — Present, hottest follow-up first

Lead with the people to act on, then the funnel, then the dead ones.

```
✍️  18 documents out for signing — 6 completed, 4 opened (not signed), 5 sent (unopened), 2 declined, 1 voided

🔥 OPENED — NOT SIGNED (4)  ← follow up now, they're engaged
  → "Broker Partnership Agreement" — opened 2d ago, not signed. Jane Broker. → call / nudge
  → "Service Agreement — Acme" — opened 5d ago, not signed. → follow up

⏳ SENT — NEVER OPENED, going stale (5)
  → "Quote to sign — Northside" — sent 9d ago, never opened. → resend or call
  → "Consent form — M. Lee" — sent 6d ago, never opened. → resend

🚫 DECLINED (2)
  → "Proposal — Vertex" — declined: "Terms need revision". → owner follow-up

✅ Completed this week: 6
```

## Step 3 — Offer the follow-up actions (with approval)

For each hot envelope, offer the next step — one at a time, with a yes:
- **Nudge / resend** an unopened-stale envelope → `mcp__trustpager__resend_signing_envelope(envelope_id)`.
- **Draft a follow-up** to an opened-not-signed signer → hand to `/draft-reply`
  (reference the open: "saw you had a look at the agreement…").
- **Void** a dead/superseded envelope → `void_signing_envelope(envelope_id)` —
  name it and get a yes; voids can't be undone (method §6).

For "I want this to happen automatically every time someone opens a document",
hand to `/automate-this` on the `signature_opened` trigger.

## What to never do

- ❌ Don't dump all envelopes as a flat list — bucket by follow-up urgency.
- ❌ Don't auto-resend or auto-void — offer, get a yes, one at a time.
- ❌ Don't treat `completed` as needing action — count it, celebrate it, move on.
- ❌ Don't chase an envelope the operator voided on purpose.

## Output shape

Headline funnel tally, then OPENED-NOT-SIGNED (the gold), then SENT-UNOPENED-STALE,
then DECLINED, then the completed count — and the single most valuable follow-up
to make first.

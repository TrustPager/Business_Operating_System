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

## Step 1 — Pull the data (MCP call)

Use the `trustpager` MCP server. One read, paginated:

| Need | Tool | Args |
|---|---|---|
| Every signing envelope | `list_signing_envelopes` | `limit: 100` (page through until exhausted — up to ~20 pages) |

This is a read — free, nothing journaled, no approval. Everything below is computed against **now**.

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal". (Envelopes carry a `deal_id` linking them to an opportunity.)

## Step 2 — Build the funnel + buckets

For each envelope, read its `status` (lowercased) and compute **age in days** from `sent_at` (fall back to `created_at`, then `updated_at`).

Tally the funnel by status, and sort each envelope into a bucket:

- **Opened, not signed** (status is `viewed` or `opened`) → the follow-up GOLD bucket.
- **Sent, never opened, going stale** (status is `sent` AND age ≥ the stale threshold — **default 5 days**, adjustable if the operator asks) → chase-or-it-dies bucket.
- **Signed** (status `signed`) → count in the funnel.
- **Completed** (status `completed`) → count in the funnel; if age ≤ 7 days, also list under "recently completed".
- **Declined** (status `declined`) → declined bucket; capture `decline_reason` if present.
- **Voided** (status `voided`) / **Expired** (status `expired`) → count in the funnel only.
- Anything else → an "other" funnel tally.

For each bucketed row capture: envelope id, document title (`document_title`, else `template_name`, else "(untitled)"), linked opportunity (`deal_id`), status, age in days, and signer (`signer_name` / `signer_email`).

**Sort both follow-up buckets oldest-first** (largest age first) — most urgent at the top.

## Step 3 — Present, hottest follow-up first

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

## Step 4 — Offer the follow-up actions (with approval)

Anything that **writes** follows the rails in `knowledge/safeguards.md` — confirm before it lands, journal the write to `.bos-journal.md`, and search-first so you don't double up. For each hot envelope, offer the next step — one at a time, with a yes:

- **Resend / nudge** an unopened-stale envelope → `update_signing_envelope` with `action: "resend"` (and the `envelope_id`).
- **Draft a follow-up** to an opened-not-signed signer → hand to `/draft-reply`
  (reference the open: "saw you had a look at the agreement…").
- **Void** a dead/superseded envelope → `update_signing_envelope` with `action: "void"` —
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

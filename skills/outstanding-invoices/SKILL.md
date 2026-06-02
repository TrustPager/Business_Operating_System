---
name: Outstanding Invoices
description: Show who owes the operator money — outstanding invoices (accounts receivable) as an aged summary (Current / 1-30 / 31-60 / 61-90 / 90+), and optionally build a dashboard and email it on a daily schedule. Reads from the connected accounting integration via the Invoices / Receivables report source.
triggers:
  - outstanding invoices
  - accounts receivable
  - who owes me money
  - aged receivables
  - overdue invoices
  - unpaid invoices
  - what am i owed
  - debtors report
  - chase invoices
  - email me my receivables
  - daily invoice report
---

# Outstanding Invoices

You are giving the operator a clear picture of the money they're owed, and — if they want it — wiring a daily emailed receivables report so they never have to ask again. Cash flow is the operator's #1 worry; this is one of the highest-value things in the pack.

This skill builds on the reporting engine. Read [knowledge/reporting-method.md](../../knowledge/reporting-method.md) for the source/measure/dimension model and the "email any dashboard on a schedule" mechanism, and [knowledge/safeguards.md](../../knowledge/safeguards.md) for the approval-queue and synced-ledger rails.

## Step 1 — Fetch the AR picture

**Run the fetcher first.** It confirms the accounting integration is connected and queries the open-AR ledger (AUTHORISED, amount due > 0) into an aged summary plus the individual overdue invoices.

```bash
python skills/outstanding-invoices/fetch.py
```

(Adjust the path if BOS is installed elsewhere.) The output shape is documented at the bottom of `fetch.py`. Branch on what it returns:

## Step 2 — Branch on the integration state

### A. Not connected (`connected: false`)

Tell the operator plainly and stop:

> "Your accounting integration isn't connected yet, so there's nothing to report on. Connect it at https://app.trustpager.com/auto/integrations and re-run this."

### B. Connected but never seeded (`ledger_empty: true`)

The integration is live but the receivables ledger hasn't been seeded — almost always a first run. Offer the **one-time catch-up sync** (it loads the existing invoices; after that the integration keeps the ledger live on its own — see the synced-ledger model in safeguards).

Run it via the `sync_receivables` MCP tool (or `POST /integrations/<integration_id>/sync-receivables`) on the `integration_id` the fetcher returned.

> ⚠️ **If the sync comes back queued for approval** (a `202` / `ApprovalPending` — some keys are approval-gated), hand it to the operator: "That's queued for approval — approve it at https://app.trustpager.com/settings/api?tab=approvals, then I'll pull your receivables." Do **not** retry or route around it.

Once seeded, re-run Step 1 and continue to C.

### C. Connected with data — present the picture

Lead with the aged summary, then the most-overdue invoices. Keep it scannable:

```
💰 Outstanding invoices — you're owed $[total_due] across [N] invoices

  Current   $[x]   ([n])
  1–30      $[x]   ([n])
  31–60     $[x]   ([n])
  61–90     $[x]   ([n])
  90+       $[x]   ([n])   ← chase these first

Most overdue:
  → INV-#### · [customer] · $[amount] · [days] days overdue
  → INV-#### · [customer] · $[amount] · [days] days overdue
  → ... (and N more)
```

Then offer the next move — usually one of: draft a chase message for the worst offenders, or **set up the daily emailed report** (Step 3).

## Step 3 — Offer the daily AR digest (the real prize)

If the operator wants this delivered automatically — "email it to me and my bookkeeper every morning" — wire it. This rides the same mechanism as the Team Task Digest (see reporting-method §5). Three pieces:

1. **A dashboard** — `create_report_dashboard` named e.g. "Outstanding Invoices", then `add_report_card` twice using the Invoices / Receivables source:
   - a **bar** card: `amount_due` (sum) grouped by `aged_bucket`, filtered `status = AUTHORISED` and `amount_due > 0`.
   - a **table** card: the open invoices (invoice number, customer, due date, amount due, days overdue), same filter.
2. **A `send_report_email` action** pointing at that dashboard, with the operator's chosen recipients. Discover its exact config with `describe_action_type('send_report_email')` — don't guess the field names.
3. **An auto schedule** firing it on the operator's cadence. For "7am every weekday" that's cron `0 7 * * 1-5` in the operator's timezone. Discover the shape with `describe_resource('auto_schedule')`.

Confirm recipients and the time before wiring, then build it. After it's live, tell the operator the first send lands at the next scheduled time and runs server-side — nothing needs to be open.

> Build each card's query with `query_report` first and confirm the numbers, *then* save the proven spec into the card. A typo'd filter field is silently ignored at render (see reporting-method §2/§4).

## Output format

Aged summary first (it's the headline), then the worst invoices, then one concrete next move — not a menu. If they're owed nothing, say it cleanly: "Nothing outstanding — every invoice is paid or not yet due. 🎉"

## Tone

- Direct and reassuring. This is money — be precise with the numbers, never round away a balance.
- Use the operator's currency from the data, don't assume dollars.
- "Chase these first" framing on the 90+ bucket is useful; don't moralise about late payers.

## What to never do

- ❌ Don't fabricate or estimate balances — only report what the ledger returns. If it's empty, seed it (B), don't guess.
- ❌ Don't send a chase message without drafting it and getting approval first.
- ❌ Don't bypass an approval `202` — surface the approval link and wait (safeguards §1).
- ❌ Don't tell the operator to "keep re-syncing" — the ledger stays live on its own after the one-time seed (safeguards §2).
- ❌ Don't name the accounting vendor as the source of truth in a way that confuses — say "your accounting integration" / "your receivables".

## Common follow-ups

- "Draft a reminder for the 90+ ones" → draft per-customer chase messages, show them, then `send_email` / `send_sms` on approval.
- "Email this to me and Anna every morning" → Step 3.
- "Just the ones over $1,000" → re-query with an added `amount_due gt 1000` filter.
- "How much is genuinely overdue vs just current?" → it's already split; the non-`current` buckets are the overdue total.

## When this skill should NOT fire

- The operator asks about a single invoice or a single customer's balance — answer that directly (a filtered `query_report`), don't run the whole AR sweep.
- They're asking about *payments they owe* (accounts payable / bills) — this source is receivables (money in), not payables.

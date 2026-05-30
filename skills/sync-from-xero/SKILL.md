---
name: sync-from-xero
description: Sync customer / invoice / payment data from Xero into TrustPager so your opportunities reflect what's actually been paid.
triggers:
  - sync from xero
  - sync xero
  - pull from xero
  - bring in xero invoices
  - reconcile xero with crm
  - which opps have been paid
  - update payment status from xero
  - which xero customers aren't in crm
---

# /sync-from-xero

Accounting and CRM drift apart. The customer paid last month but the opp is still in "Quote Sent" because nobody moved it. This skill closes that gap by pulling Xero data and reconciling it against TrustPager opportunities.

## Step 1 — Pre-fetch

Run:

```
python skills/sync-from-xero/fetch.py
```

This first checks `integrations` for an active Xero connection. If `connected: false`, tell the user:

> "Xero isn't connected to your TrustPager workspace yet. Connect it at https://app.trustpager.com/settings/integrations, then re-run this skill."

If connected, the response includes the recent TrustPager opportunities for cross-referencing. For the Xero side detail (invoices + payments), use `mcp__trustpager__query_integration` with the returned `xero.id` — Xero's data is too detailed to pre-bundle.

## Step 2 — Cross-reference

For each Xero invoice:
- Find the matching TrustPager opportunity. Match priority:
  1. By `xero_invoice_id` if previously linked
  2. By customer email + matching value within ±$50
  3. By customer name + closest opportunity in time
- For unmatched invoices: flag for the user — "this $4,200 Xero invoice to John Smith on 14 May has no matching opportunity in your pipeline. Create one?"

For each TrustPager opportunity in a "won" stage:
- If it has a Xero invoice but `payment_status` doesn't reflect the Xero state → flag for update.
- If it has NO Xero invoice → flag: "This opp marked Won but no Xero invoice exists — should we raise one?"

## Step 3 — Show the diff before writing

```
Xero ↔ TrustPager reconciliation

Pulled from Xero: 47 invoices, 41 payments.

✅ 38 matched cleanly — payment status already correct.

🔄 5 opportunities need their payment_status updated:
   - Smith building inspection (was: Awaiting payment) → Paid in full ($3,400)
   - …

⚠️ 4 Xero invoices have no matching TrustPager opportunity:
   - $2,100 to Acme Pty Ltd, 12 May
   - …

⚠️ 2 won opportunities have no Xero invoice:
   - Hudson refinance ($8,000)
   - …

Proceed with the 5 payment_status updates? The 6 unmatched cases need a manual call from you.
```

## Step 4 — Apply with approval

After explicit go, apply the 5 (or however many) updates:
- For each: `mcp__trustpager__update_opportunity` with the new `payment_status` value
- Use the appropriate enum value (`paid`, `partial`, `unpaid`, etc. — confirm with `mcp__trustpager__describe_resource('opportunity')` for valid values)

The 6 unmatched cases get handed back as a checklist for the user to action:
> "Here's what's left for you to handle manually:
> - …"

## Important behaviours

- **No auto-create.** Unmatched Xero invoices → opportunities only with user approval per invoice.
- **No invoice creation.** Won opps without invoices → flagged only. Creating an invoice is a separate intent.
- **Value tolerance ±$50 only.** Bigger mismatches mean ambiguous match — flag, don't auto-link.
- **Date filter.** Default to 90 days. Older state has likely already been reconciled.
- **Preserve audit trail.** Every payment_status change gets a note on the opportunity referencing the Xero invoice number.

## When the Xero integration isn't available

If TrustPager doesn't yet have a Xero integration in your workspace, this skill can still help by parsing a Xero CSV export:
> "If you're not connected to Xero yet, you can export 'Invoices' from Xero as CSV and paste it here. I'll do the same reconciliation against your TrustPager opportunities."

Then hand off to /import-from-anywhere logic with a Xero-shaped parser.

## Output shape

"Sync complete. 5 opportunity payments updated. 6 mismatches left for your review (listed above)."

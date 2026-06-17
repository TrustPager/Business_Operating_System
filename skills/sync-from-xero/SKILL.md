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

## Two distinct jobs — pick the right one

Xero data feeds TrustPager in **two separate ways**. They are not the same thing, and this skill is only the first:

1. **Reconcile invoices ↔ opportunities (this skill).** Match Xero invoices to pipeline opportunities and bring their **payment status** into line — "this Won deal is actually paid now". One-off, opportunity-by-opportunity. Use this when the operator's pipeline is out of step with what's been paid.

2. **Seed the receivables ledger for AR reporting** — a *different* job. This populates the **Invoices / Receivables report source** so the operator can run an aged-receivables report ("who owes me money") and email it on a schedule. That's **`/outstanding-invoices`**, not this skill. It uses `sync_receivables` (a one-time seed; the integration's webhook keeps it live after that — see [knowledge/reporting-method.md](../../knowledge/reporting-method.md) §6 and `knowledge/safeguards.md` §2 on synced ledgers).

> If the operator says "who owes me money", "aged receivables", "email me my outstanding invoices daily", or anything about *reporting* on invoices → hand off to **`/outstanding-invoices`**. Stay here only for reconciling payment status against the pipeline.

## Step 1 — Pull the data (MCP calls)

Use the `trustpager` MCP server. Start with these reads:

| Need | Tool | Args |
|---|---|---|
| Find the Xero integration + its status | `list_integrations` | `limit: 50` |
| Recent opportunities to reconcile against | `list_deals` | `limit: 200` (filter to the last ~90 days yourself in Step 2) |

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

From `list_integrations`, find the entry whose `platform_type` (or `provider`) is `xero`. **Treat Xero as connected only if its `status` is one of `active` / `connected` / `authorized`.** If there's no Xero entry or its status isn't one of those, stop and tell the user:

> "Xero isn't connected to your TrustPager workspace yet. Connect it at https://app.trustpager.com/auto/integrations, then re-run this skill."

If connected, note the Xero integration's `id` — you need it for the next call. Then pull the Xero-side detail (invoices + payments) with `query_integration`, passing that integration id. Xero's data is too detailed to bundle up front; query it directly.

These are all reads — free, nothing journaled, no approval.

## Step 2 — Cross-reference

Consider only opportunities updated/closed in the **last 90 days** (older state has likely already been reconciled). For each Xero invoice:
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

This step **writes** — it follows the rails in `knowledge/safeguards.md`: confirm before anything lands, journal each write to `.bos-journal.md`, and search-first so you don't double-apply. After explicit go, apply the updates:

- For each opportunity: `update_deal` with the new `payment_status` value.
- Use the right enum value (`paid`, `partial`, `unpaid`, etc.). If you're unsure which values are valid in this workspace, confirm against `get_crm_settings` or ask the operator — don't guess. (`describe_resource` is only available on the claude.ai-connected workspaces, not the client `trustpager` server, so don't rely on it.)
- A `202` / `approval_id` response means the write is **queued for human approval** — surface the approval id + the approvals URL, journal it as `approval_pending`, and stop. Don't retry (safeguards §1).

The 6 unmatched cases get handed back as a checklist for the user to action:
> "Here's what's left for you to handle manually:
> - …"

## Important behaviours

- **No auto-create.** Unmatched Xero invoices → opportunities only with user approval per invoice.
- **No invoice creation.** Won opps without invoices → flagged only. Creating an invoice is a separate intent.
- **Value tolerance ±$50 only.** Bigger mismatches mean ambiguous match — flag, don't auto-link.
- **Date filter.** Default to 90 days. Older state has likely already been reconciled.
- **Preserve audit trail.** Every payment_status change gets a note on the opportunity (`add_note`) referencing the Xero invoice number.

## When the Xero integration isn't available

If TrustPager doesn't yet have a Xero integration in your workspace, this skill can still help by parsing a Xero CSV export:
> "If you're not connected to Xero yet, you can export 'Invoices' from Xero as CSV and paste it here. I'll do the same reconciliation against your TrustPager opportunities."

Then hand off to /import-from-anywhere logic with a Xero-shaped parser.

## Output shape

"Sync complete. 5 opportunity payments updated. 6 mismatches left for your review (listed above)."

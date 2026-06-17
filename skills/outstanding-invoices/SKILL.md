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

## Step 1 — Confirm the accounting integration (MCP call)

On the `trustpager` MCP server:

| Need | Tool | Args |
|---|---|---|
| Connected integrations | `list_integrations` | `limit: 50` |

Find the accounting integration (provider/platform type = `xero`). It's **connected** if its status is one of `active` / `connected` / `authorized`. Keep its integration id. This is a free read.

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

## Step 2 — Branch on the integration state

### A. Not connected

Tell the operator plainly and stop:

> "Your accounting integration isn't connected yet, so there's nothing to report on. Connect it at https://app.trustpager.com/auto/integrations and re-run this."

### B. Connected — read the receivables ledger

> ⚠️ **Capability gap on this MCP surface.** The receivables ledger is a synced report source (`invoices`) that the original fetcher read via the report query engine and seeded with a `sync_receivables` call. On the client `trustpager` MCP surface those are **not exposed**: `query_report` only supports `source: "deals"` (sales pipeline — no `amount_due` / `aged_bucket` measures), and there is **no `sync_receivables` / `list_invoices` read tool**. So you cannot pull the aged AR ledger directly from MCP today. Options, in order:
> 1. Tell the operator the aged-summary read isn't available over the assistant connection yet, and point them to the in-app receivables view at https://app.trustpager.com/auto/integrations (and the Reporting section).
> 2. If they want it automated, you CAN still build the **daily emailed receivables dashboard** (Step 3) — the dashboard/report-card/schedule tools that drive it DO exist on this surface; the Invoices source is selected inside the report card, server-side.
> 3. Capture the gap with `/suggest-improvement` (a receivables read tool / `invoices` report source over MCP) so the team can ship it.

When the in-app ledger (or a future read tool) gives you the numbers, present them as below. **Synced-ledger rails (safeguards §2):** seed once at onboarding, then it stays live on its own — never tell the operator to "keep re-syncing". "Days overdue" / aged buckets compute at query time, so a once-captured record keeps ageing correctly.

### C. Present the picture

Lead with the aged summary, then the most-overdue invoices. Order buckets `current` → `1-30` → `31-60` → `61-90` → `90+`. Keep it scannable:

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

Then offer the next move — usually: draft a chase message for the worst offenders, or set up the daily emailed report (Step 3).

## Step 3 — Offer the daily AR digest (the real prize)

If the operator wants this delivered automatically — "email it to me and my bookkeeper every morning" — wire it on the `trustpager` server. This rides the same mechanism as the Team Task Digest (reporting-method §5). These are **writes** — follow the rails: confirm recipients + time first, journal each write to `.bos-journal.md`, and a `202`/`approval_id` means queued (surface the link, stop, don't retry).

1. **A dashboard** — `create_report_dashboard` named e.g. "Outstanding Invoices", then `add_report_card` twice using the Invoices / Receivables source:
   - a **bar** card: `amount_due` (sum) grouped by `aged_bucket`, filtered `status = AUTHORISED` and `amount_due > 0`.
   - a **table** card: the open invoices (invoice number, customer, due date, amount due, days overdue), same filter.
2. **A `send_report_email` action** pointing at that dashboard, with the operator's chosen recipients. Build it as an automation action via `add_automation_action` (`action_type: "send_report_email"`); confirm its exact config fields from the `add_automation_action` `config` description rather than guessing.
3. **An auto schedule** firing it on the operator's cadence — `create_auto_schedule`. For "7am every weekday" that's cron `0 7 * * 1-5` in the operator's timezone.

Confirm recipients and the time before wiring, then build it. After it's live, tell the operator the first send lands at the next scheduled time and runs server-side — nothing needs to be open. Journal each created dashboard / card / action / schedule.

## Output format

Aged summary first (it's the headline), then the worst invoices, then one concrete next move — not a menu. If they're owed nothing, say it cleanly: "Nothing outstanding — every invoice is paid or not yet due. 🎉"

## Tone

- Direct and reassuring. This is money — be precise with the numbers, never round away a balance.
- Use the operator's currency from the data, don't assume dollars.
- "Chase these first" framing on the 90+ bucket is useful; don't moralise about late payers.

## What to never do

- ❌ Don't fabricate or estimate balances — only report what the ledger returns. If you can't read it over MCP, say so (Step 2B) — don't guess.
- ❌ Don't send a chase message without drafting it and getting approval first.
- ❌ Don't bypass an approval `202` — surface the approval link and wait (safeguards §1).
- ❌ Don't tell the operator to "keep re-syncing" — the ledger stays live on its own after the one-time seed (safeguards §2).
- ❌ Don't name the accounting vendor as the source of truth in a way that confuses — say "your accounting integration" / "your receivables".

## Common follow-ups

- "Draft a reminder for the 90+ ones" → draft per-customer chase messages, show them, then `send_email` / `send_sms` on approval (journal each).
- "Email this to me and Anna every morning" → Step 3.
- "Just the ones over $1,000" → add an `amount_due gt 1000` filter to the dashboard cards.
- "How much is genuinely overdue vs just current?" → the non-`current` buckets are the overdue total.

## When this skill should NOT fire

- The operator asks about a single invoice or a single customer's balance — answer that directly, don't run the whole AR sweep.
- They're asking about *payments they owe* (accounts payable / bills) — this source is receivables (money in), not payables.

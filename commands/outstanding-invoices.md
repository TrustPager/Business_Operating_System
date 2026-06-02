---
description: Who owes you money — outstanding invoices as an aged summary, with the option to email it daily.
---

Run the **Outstanding Invoices** skill.

Invoke the skill at `skills/outstanding-invoices/SKILL.md`. Follow its instructions exactly: run the fetcher first, branch on the integration state (not connected → prompt to connect; ledger empty → offer the one-time seed; data present → show the aged summary then the worst invoices), and end with one concrete next move. If the operator wants it delivered automatically, wire the daily emailed digest per Step 3.

If the operator names a single invoice or one customer, answer that directly instead of running the full sweep.

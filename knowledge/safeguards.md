# Safeguards

**The cross-cutting rails every skill in this pack relies on.** Not a workflow — the handful of platform behaviours that, if mishandled, quietly do the wrong thing. Read this once; the patterns recur everywhere.

---

## 1. The approval queue — `202` means *queued*, not *done*

Some workspaces issue API keys with an **"approval" permission level**: writes don't execute immediately, they queue for a human to approve in-app. When that happens the API returns **HTTP `202` with an `approval_id`** instead of a normal result.

The shared library already handles this correctly — **a `202` is returned, never raised**, as an `ApprovalPending` object (see `tools/trustpager_api.py`). What matters is what the *skill* does next:

> **A `202` is not a failure and not a success — it's a hand-off.** Tell the operator plainly: "That's queued for approval — approve it at `https://app.trustpager.com/settings/api?tab=approvals` (id: `<approval_id>`)." Then **stop and wait.** Do not retry. Do not look for another way to push it through.

**Never try to route around an approval gate.** It exists so a human stays in the loop on writes that touch shared or outward-facing state (sends, integration syncs, automations). Bypassing it — re-issuing the call differently, or treating the `202` as an error to "fix" — defeats the audit trail and produces silent, unreviewed actions.

In a fetch/skill script:
```python
result = api_post(path, body=payload)
if isinstance(result, ApprovalPending):
    # surface result.approval_id and result.approval_url to the operator; do NOT retry
    ...
```

If multiple writes queue (e.g. a clear-then-restore pair), name **which to approve and which to reject, and why** — don't leave the operator guessing.

---

## 2. Synced ledgers — "seed once, stays live, ages itself"

Some report sources (notably **Invoices / Receivables**) read from a ledger that syncs from a connected integration. The mental model that prevents needless work and confusing "empty report" moments:

- **Seed once at onboarding.** Existing records predate the live feed, so nothing has announced them — a one-time catch-up sync loads the back-catalogue.
- **It stays current on its own.** After the seed, the integration's webhook updates the ledger automatically on every change. No recurring sync, no cron.
- **Re-running the seed is safe.** It's idempotent (keyed on the source record id), so it doubles as a reconcile/repair pass if a webhook is ever missed — it never duplicates.
- **Time-relative fields compute at query time.** Things like "days overdue" / "aged bucket" are derived from *today*, not stored — so a record captured once keeps ageing correctly with zero re-syncs.

> If a synced report is empty, the fix is almost always **"seed the ledger"**, not "the query is broken" and not "re-sync everything constantly".

---

## 3. The standing write rails (recap)

Every skill already inherits these — they're listed here so the reasons are in one place:

- **Ask before anything destructive or outward-facing.** Drafts get shown and approved before they send. Deletes get confirmed.
- **Every write is journaled.** `~/.claude/bos-journal/` gets one line per write (method, path, status, result/approval id) — read it with `python tools/journal.py`. Reads are never journaled.
- **One workspace only.** Skills talk to the operator's own TrustPager workspace via their key — never anyone else's.
- **Idempotency for risky writes.** Use `idempotent_post` for anything where a duplicate would hurt (sends, creates, charges) so a network retry can't double-fire.

---

## 4. Verify before a customer hears it — never claim what you haven't seen work

Before any message tells a customer something is fixed, done, or working, the exact thing it claims must have been **confirmed working first**. Never send "it's fixed" or hand someone a "try this" step on a hunch.

The order, every time:

1. **Claude smoke-tests first.** Exercise the exact thing in the workspace and confirm it actually works. If a step would notify a real person (email, SMS, booking confirmation), use a **test contact** so no real customer is hit. Scope the test to what this message is about, never the whole platform.
2. **A human confirms** the result by hand (the manager, or the person who owns the customer).
3. **Only then** does the customer get the message — short, plain, and in one voice (`communication-voice.md`), with one clean instruction on how to USE it.

> If it isn't confirmed working, it doesn't go to the customer. A customer discovering broken basics themselves, or decoding a technical email, costs more trust than the original problem.

**On a team:** a draft from someone in an approval-only role goes to a manager to confirm before it ships (see your `team-standards.md` approval rules). The teammate's Claude smoke-tests first either way — that pass both confirms it works and gives Claude the real context to write an accurate, simple message.

**Customers use, they don't test.** The verification is the team's job. What the customer receives is never a test request; it's a clean instruction on how to use the thing.

# Safeguards

**The cross-cutting rails every skill in this pack relies on.** Not a workflow — the handful of platform behaviours that, if mishandled, quietly do the wrong thing. Read this once; the patterns recur everywhere.

---

## 1. The approval queue — `202` means *queued*, not *done*

Some workspaces issue API keys with an **"approval" permission level**: writes don't execute immediately, they queue for a human to approve in-app. When that happens the MCP tool **doesn't return a normal result** — its response carries **status `202` and an `approval_id`** (and usually an approval URL) instead of the created/updated record.

The platform enforces this for you — the gate lives in the API, not in any local code. What matters is what *you* do when a write tool comes back queued:

> **A `202` is not a failure and not a success — it's a hand-off.** Tell the operator plainly: "That's queued for approval — approve it at `https://app.trustpager.com/settings/api?tab=approvals` (id: `<approval_id>`)." Then **stop and wait.** Do not retry. Do not look for another way to push it through.

**Never try to route around an approval gate.** It exists so a human stays in the loop on writes that touch shared or outward-facing state (sends, integration syncs, automations). Bypassing it — re-issuing the call a different way, or treating the `202` as an error to "fix" — defeats the audit trail and produces silent, unreviewed actions.

How to read it from an MCP tool response:

> If a `create_*` / `update_*` / `send_*` / `trigger_*` tool returns a body with `status: 202` or an `approval_id` field, treat it as **queued**. Surface the `approval_id` and the approvals URL to the operator, journal it as `approval_pending` (rail 3), and stop.

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

Every skill already inherits these — they're listed here so the reasons are in one place. There is no helper library doing this for you: in this pack **you uphold these rails yourself, by reasoning**, on every write tool call.

- **Ask before anything destructive or outward-facing.** Drafts get shown and approved before they send. Deletes get confirmed. This is the rail the others protect.
- **Journal every write — to `./.bos-journal.md`.** Immediately after any `create_*` / `update_*` / `delete_*` / `send_*` / `trigger_*` / `move_*` MCP tool call, append **one line** to a file named `.bos-journal.md` in the working directory (next to `CLAUDE.md`), creating it if absent:
  ```
  - 2026-06-16T09:14:03Z  create_deal  ok  → id 4f2a…   (skill: lead-triage)
  - 2026-06-16T09:15:20Z  send_email   approval_pending  → approval 8c1d…   (skill: draft-reply)
  ```
  Record: UTC timestamp, the tool name, the outcome (`ok` / `approval_pending` / `error`), the result or approval id, and which skill issued it. **Reads are never journaled.** This is best-effort and reasoning-driven — if you genuinely can't write the file, tell the operator rather than silently skipping. To review the trail, just open `.bos-journal.md` (no tool needed — "what did you change today?" = read that file).
- **One workspace only.** Every skill talks to the operator's own TrustPager workspace via the single configured `trustpager` MCP connection — never anyone else's.
- **Idempotency for risky writes = search first, never blind-retry.** Before a write where a duplicate would hurt (a send, a create, a charge), do a quick `search_*` / `list_*` to confirm the record/message doesn't already exist. If a write tool call times out or errors ambiguously, **do not just re-issue it** — search to find out whether the first attempt actually landed, then act on what you find. A duplicate send or charge is worse than a slow one.

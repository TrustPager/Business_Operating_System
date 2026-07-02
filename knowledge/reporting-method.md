# Reporting Method

**The foundation doc for every reporting skill in this pack.** Read this before building a report, a dashboard, or a scheduled digest. The skills (`/outstanding-invoices`, `/email-me-a-report`) reference it so they share one mental model.

If `automation-method.md` is "how to think about things that fire on events", this is "how to think about turning your workspace data into a number, a chart, or a scheduled email".

---

## The one-sentence model

> A **report** runs a query against one **data source**, picks one or more **measures** (numbers to add up) sliced by **dimensions** (ways to group), and renders the result as a **card** on a **dashboard** — and *any* dashboard can be emailed to anyone on a **schedule**.

Everything below is detail on those words: **source → measures → dimensions → filters**, then **dashboard → card**, then the high-leverage bit most operators never discover: **dashboard → scheduled email digest**.

---

## 1. Data sources — *what* you can report on

A source is a business-language view of your workspace. Each exposes **measures** (numeric fields you can sum/avg/count) and **dimensions** (text/date/boolean fields you can group or filter by).

> **Never hardcode the source list — it grows.** Discover the live set with `mcp__trustpager__list_report_sources` (or `GET /reports/sources`). It returns every source with its measures, dimensions, and formats. The table below is orientation, not gospel.

| Source | What it covers | Requires |
|---|---|---|
| `opportunities` | Pipeline value, win/loss, lead sources, stages, staff performance | nothing |
| `tasks` | Open vs completed, by assignee / priority / category, overdue tracking | nothing |
| `invoices` | Outstanding invoices (accounts receivable): amount due, aged buckets, overdue tracking, by customer | a connected accounting integration + a one-time receivables sync (see §6) |

---

## 2. The query shape

`query_report` (MCP) / `POST /reports/query` takes:

```json
{
  "source": "invoices",
  "measures":   [{ "field": "amount_due", "aggregation": "sum", "alias": "total_due" }],
  "dimensions": ["aged_bucket"],
  "filters":    [{ "field": "status", "operator": "eq", "value": "AUTHORISED" },
                 { "field": "amount_due", "operator": "gt", "value": 0 }],
  "mode": "aggregate"
}
```

- **`measures`** — array of `{ field, aggregation, alias }`. Aggregations: `count`, `sum`, `avg`, `min`, `max`. (`count` ignores the field — use the source's id measure.)
- **`dimensions`** — array of **plain field-name strings** (NOT objects). These are the group-by columns in aggregate mode, or the display columns in drilldown.
- **`filters`** — array of `{ field, operator, value }` (or `values` for `in`/`not_in`).
- **`mode`** — `aggregate` (grouped totals, the default) or `drilldown` (the individual rows). Drilldown still needs at least one measure in the payload.

> ⚠️ **The operator is `eq`, not `equals`.** Valid operators: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `in`, `not_in`, `like`, `is_null`, `is_not_null`, `contains`. **An unknown operator (or unknown field) is silently dropped** — the query then returns *everything*, which looks like a working report full of wrong data. If a filtered total looks identical to the unfiltered total, suspect a bad operator or field name first.

---

## 3. The Invoices / Receivables source — aged AR

The classic accounts-receivable report. The open-ledger filter is **`status = AUTHORISED` AND `amount_due > 0`**.

Key fields:
- **Measures:** `amount_due`, `total`, `amount_paid` (sum/avg), invoice `id` (count).
- **Dimensions:** `status`, `customer_name`, `currency_code`, `invoice_type`, `due_date`, `issue_date`, and three **computed-at-query-time** fields — `aged_bucket` (`current` / `1-30` / `31-60` / `61-90` / `90+`), `days_overdue` (number), `is_overdue` (boolean).

Because aging is computed from *today's date* at query time, a static unpaid invoice keeps ageing correctly with no re-sync — group by `aged_bucket` any day and the buckets are current.

The aged-AR aggregate (amount due by bucket) and a drilldown (the actual overdue invoices, most-overdue first via `due_date asc`) are the two cards a receivables dashboard wants. `/outstanding-invoices` builds exactly this.

---

## 4. Dashboards and cards

- **Dashboard** = the container (a name, a visibility setting, a list of cards). Create with `create_report_dashboard` (`POST /report-dashboards`). Optionally pass a `template` for a pre-built set of cards (`list_report_templates` to browse).
- **Card** = one query rendered one way. Add with `add_report_card` (`POST /report-dashboards/:id/cards`): a `title`, a `query_spec` (the §2 shape), a `visualization_type`, and a `size`.
- **Visualisation types:** `bar`, `horizontal_bar`, `line`, `donut`, `funnel`, `stat` (single big number), `table` (rows — use this for a drilldown like "the open invoices").

> A card's `query_spec` is validated against the source's fields when you save it. A typo in a filter field doesn't error — it's silently ignored at render (same trap as §2). Build the query with `query_report` first, confirm the numbers, *then* paste the proven spec into the card.

---

## 5. The high-leverage unlock — email any dashboard on a schedule

This is the bit most operators never find. **Any dashboard can be delivered as a recurring email digest, server-side, with nobody's app open** — the same mechanism behind the built-in "Team Task Digest".

It's three pieces:
1. A **dashboard** (the cards to render).
2. An **automation** with a **`send_report_email`** action — it renders the dashboard's cards to HTML, scoped to each recipient, and emails it. Skip-if-empty by default (if every card is empty for a recipient, the send is skipped, not failed).
3. An **auto schedule** (a cron) that fires that automation — e.g. `0 7 * * 1-5` for 7am every weekday.

To wire it, discover the exact shapes live rather than guessing:
- `mcp__trustpager__describe_action_type('send_report_email')` — the action's config (dashboard id, recipients, subject, intro/outro).
- `mcp__trustpager__describe_resource('auto_schedule')` — how to create the schedule and bind it to the automation, plus timezone + cron handling.

Recipients can be operators or any email addresses. The schedule carries a **timezone** — set it to the operator's local zone (e.g. `Australia/Sydney`) so "7am" means their 7am.

`/email-me-a-report` drives this end to end for any dashboard; `/outstanding-invoices` uses it for the AR digest specifically.

---

## 6. Where the data comes from (the invoices source especially)

`opportunities` and `tasks` are native — always queryable. **`invoices` is fed by a receivables ledger** that syncs from the connected accounting integration:

- **Seed once** — a one-time catch-up loads the existing invoices (they predate the live feed, so nothing has announced them yet). `/outstanding-invoices` runs this when the ledger is empty; it's also available as `sync_receivables` (MCP) / `POST /integrations/:id/sync-receivables`.
- **Stays live on its own** — after the seed, the accounting integration's webhook updates the ledger automatically on every invoice change. No cron, no re-sync.
- **Reconcile** — re-running the seed is idempotent (keyed on the invoice id), so it doubles as a repair pass if a webhook is ever missed.

So the only "sync" moment is onboarding. If a receivables report is empty, the fix is almost always "the ledger hasn't been seeded yet", not a broken query.

---

## 7. The weekly scoreboard — the standing report archetype

The one-page weekly scoreboard (`business-method.md` §12.6) is the standing report most operators should end up with: one dashboard, a handful of `stat` cards, delivered by the §5 digest every Monday in the operator's timezone.

Map each card to a real source:

| Card | Source / query |
|---|---|
| Leads & conversations this week | `opportunities` — opportunities created, by stage |
| Close rate | `opportunities` — won vs decided |
| Cash collected | `invoices` — sum of `amount_paid` (requires the seeded ledger, §6) |
| Open / overdue follow-ups | `tasks` — open + overdue counts |
| THE pressure-point metric of the quarter | one extra card for whatever the current diagnosis says matters most (`business-method.md` §16) |

When a doctrine metric has no source yet (activation %, churn/saves): **don't fake it with a proxy** — a missing number is a finding. The scoreboard ships with the cards the workspace can honestly fill, and "start measuring X" becomes a task, not a chart (`business-method.md` §2).

A business with no numbers rhythm gets this scoreboard as its FIRST prescription; `/weekly-review` reads it, `/email-me-a-report` delivers it.

---

## Discovery cheat-sheet

| Need | Call |
|---|---|
| What can I report on? | `list_report_sources` |
| What dashboards exist? | `list_report_dashboards` |
| Pre-built dashboards | `list_report_templates` |
| Run a query | `query_report` |
| Build a dashboard / card | `create_report_dashboard`, `add_report_card` |
| Email shape for a digest | `describe_action_type('send_report_email')` |
| Schedule shape | `describe_resource('auto_schedule')` |
| Seed the receivables ledger | `sync_receivables` |

Never invent a field, operator, or source name — list it first.

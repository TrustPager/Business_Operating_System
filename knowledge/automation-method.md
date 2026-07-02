# Automation Method

**The foundation doc for every automation skill in this pack.** Read this before building, auditing, or debugging a TrustPager automation. The skills (`/automate-this`, `/audit-my-automations`, `/why-didnt-it-fire`) reference it so they all share one mental model and one set of safety rails. Which automations matter most for a given business is a diagnosis question — the recipes catalogue (automation-recipes.md) carries the doctrine-backed priorities.

If `marketing-strategy-method.md` is "how to think about a nurture sequence", this is "how to think about everything automations can do".

---

## The one-sentence model

> An **automation** watches for an **event** (the trigger), checks whether the event **matters** (the conditions), and if so runs an ordered list of **actions** — forever, without anyone touching it.

Everything below is detail on those four words: **trigger → conditions → actions**, plus how automations differ from **auto queues** (multi-step sequences), and the discipline that keeps them safe.

---

## 1. The trigger — *when* it fires

A trigger is the event that wakes the automation up. Each trigger has two parts:

- **`trigger_type`** — the *event class* (what happened): `form_completed`, `webhook_received`, `stage_changed`, `sms_received`, `email_received`, `call_analyzed`, `deal_created`, `contact_created`, `booking_created`, `invoice_paid`, platform events (`xero_*`, `facebook_lead_ad`, `calcom_*`, `zoom_*`), `api`, `scheduled`, and more.
- **`source`** — *which specific thing* of that class. A `form_completed` trigger can fire for **any** form or **one specific** form template. `source_type` + `source_id` express that: `source_type='form_template'`, `source_id=<that form's id>`, or `source_type='any'` for "any source of this event."

> **Never hardcode the trigger list.** It grows. Always discover the live set with `mcp__trustpager__list_trigger_schemas` (or the `schemas/triggers` endpoint), and get a single trigger's payload + available `{{variables}}` with `mcp__trustpager__get_trigger_schema(trigger_type)`. The common ones below are orientation, not gospel.

### Common triggers and what fires them

| trigger_type | Fires when… | Typical source |
|---|---|---|
| `form_completed` | someone submits an **internal** TrustPager form (one you sent via `send_form`) | `form_template` (or any) |
| `webhook_received` | an external system POSTs to a TrustPager incoming-webhook URL | `webhook` (a specific endpoint) |
| `stage_changed` | an opportunity moves into a pipeline stage | the stage itself (see §1.2) |
| `sms_received` / `email_received` | an inbound SMS / email lands | `sms` / `email` (or any) |
| `call_analyzed` | a voice-agent call finishes and is analysed | `voice_agent` |
| `call_voicemail` | a voice-agent call hit voicemail | `voice_agent` |
| `call_real_conversation` | a voice-agent call was a real human conversation (≥10s) | `voice_agent` |
| `deal_created` / `contact_created` | a new opportunity / contact is created | `any` |
| `document_sent` / `signature_completed` / `signature_declined` | document & e-sign lifecycle events | `document_template` / `signature_template` |
| `facebook_lead_ad`, `xero_invoice_paid`, `calcom_booking_created_or_rescheduled`, `zoom_*` | a connected integration emits an event | `platform_integration` |
| `api` | your own code calls `POST /v1/automations/:id/trigger` | `any` |

> ⚠️ **Website contact forms are NOT `form_completed`.** `form_completed` / `form_sent` fire only for *internal* PIN-protected TrustPager forms you send via `send_form`. A form on the customer's own website posts in as a webhook — use `webhook_received` / `generic_webhook`.

### 1.1 Multiple triggers per automation — OR-match (the high-leverage one)

**An automation can have more than one trigger.** It fires when **ANY** of them matches — OR logic, not AND. This is the single most useful thing most operators don't know exists.

The canonical case: a referral can arrive **two ways** — via a TrustPager intake form (`form_completed`) **or** via the customer's website (`webhook_received`) — and both should run the *same* actions (e.g. push the lead to a quoting API). Instead of maintaining two identical automations that drift apart, build **one** automation with **two triggers**.

- Each trigger row carries its **own** `trigger_type` + source. The action chain runs once, whichever trigger fired.
- Add extra triggers with `mcp__trustpager__add_automation_trigger(automation_id, trigger_type=…, source_type=…, source_id=…)`, or inline a `triggers: [...]` array on `create_automation`.
- The first trigger is the "primary" (it's what the automation lists under), but matching is per-trigger — a `form_completed`-primary automation genuinely fires on its `webhook_received` trigger too.

> **When to use multiple triggers vs separate automations:** same actions, different entry points → **one automation, multiple triggers**. Different actions per entry point → **separate automations**. If you'd copy-paste the action chain, you want multi-trigger.

### 1.2 Stage automations are special

`stage_changed` automations bind to a pipeline stage via the automation's `stage_id`, **not** a trigger row. Build/edit them with `create_stage_automation` or from the pipeline's workflow page — not the generic trigger flow. One stage per stage-automation.

---

## 2. Conditions — *whether* it matters

Conditions are an optional gate evaluated **after** the trigger fires and after CRM enrichment (so contact/opportunity/tag data is available for *every* trigger type, not just stage changes). **ALL conditions must pass** for the automation to run — AND logic. If they don't, the run is recorded with status `skipped` (not failed — this is normal and visible in the run log).

Field keys (vary by trigger, but CRM-enriched fields are broadly available): `deal.value`, `deal.name`, `lead_source`, `tags`, `contact.email`, `contact.first_name`, `contact.last_name`, `contact.phone`, `customer.name`, plus raw trigger-payload fields by dot-notation.

Operators:

- Equality: `{ "field": { "eq": "value" } }` / `{ "neq": … }` — or shorthand `{ "field": "value" }`
- Existence: `{ "field": { "exists": true } }` / `{ "not_exists": true }`
- Numeric: `gt` / `gte` / `lt` / `lte`
- Tags (arrays): `{ "tags": { "contains": "VIP" } }` / `not_contains` / `contains_any: ["VIP","Hot"]`
- Text: `{ "field": { "contains_text": "substring" } }`
- In list: `{ "field": { "in": ["a","b"] } }`

Examples:
```json
{ "tags": { "contains": "VIP" }, "deal.value": { "gte": 5000 } }
{ "lead_source": { "in": ["Referral", "Website"] }, "contact.email": { "exists": true } }
```

> **Fail-closed.** An unknown operator makes the automation **skip**, never fire blindly. That's deliberate — a broken condition shouldn't spray emails.

---

## 3. Actions — *what* it does

Actions run **in order, top to bottom**. Order is load-bearing: "create opportunity" → "tag the new opportunity" works; the reverse fails because there's nothing to tag yet.

> **Never guess an action's config shape.** Browse with `mcp__trustpager__list_action_types`, then — right before you write each one — call `mcp__trustpager__describe_action_type(action_type)` for its exact config schema, a worked example, and warnings.

Common action types (discover the full live list, don't trust this as complete):

- **Communicate:** `send_custom_email`, `send_gmail_email`, `send_sms`, `send_whatsapp`, `voice_outbound_call`, `send_form`, `send_for_signing`
- **CRM:** `create_lead`, `create_opportunity`, `move_deal`, `apply_tags`, `set_custom_field`, `add_tasks`, `notify_assigned_staff`, `create_referral`, `request_review`
- **Integrations / external:** `call_webhook`, `slack_send_message`, `facebook_conversion`, `xero_create_contact`, `xero_create_invoice`
- **Queues:** `attach_to_event_queue`, `remove_from_event_queue` (see §4)

`{{variables}}` in email/SMS bodies (e.g. `{{contact.first_name}}`, `{{deal.value}}`) come from the trigger payload — **confirm the variable exists for the chosen trigger** with `get_trigger_schema` before using it, or it renders blank.

> ⚠️ **Sending actions cost credits and reach real people.** `send_*` and `voice_outbound_call` go to the customer the moment the automation fires. Test before enabling (§5). When testing, never point a send action at a real customer — use the operator's own monitored inbox/number.

---

## 4. Automations vs Auto Queues — pick the right tool

| | **Automation** | **Auto Queue** |
|---|---|---|
| Shape | One event → one ordered action chain, runs once | A **multi-step sequence** over days/weeks with delays between steps |
| Use for | A *reaction* — "lead arrives → tag + acknowledge + task" | A *nurture / drip* — "Day 0 welcome, Day 2 value, Day 5 case study, Day 9 ask" |
| Timing | Immediate (or a single scheduled delay) | Per-step `delay_days/hours/minutes`; contacts move through over time |
| Built by | `/automate-this` | `/design-nurture-sequence` → `/wire-nurture-sequence` |

A contact enters a queue via an `attach_to_event_queue` action (often *from* an automation) and exits when they reach a goal or a cancel-trigger fires. **If the operator describes "a series of emails over time", that's a queue — hand off to the nurture-sequence skills.** If it's "the moment X happens, do Y once", that's an automation.

---

## 5. The test-before-enable discipline (non-negotiable)

A **disabled** automation is inert and safe. An **enabled** one runs for real, sends real messages, spends real credits. So:

1. **Build it disabled.** `create_automation` defaults to `enabled: false`. Leave it.
2. **Dry-run an action.** `mcp__trustpager__execute_automation_action` runs a single action against sample data in isolation — confirm an email renders, a tag applies, a webhook posts the right body, *without* firing the whole chain at a customer.
3. **Read the result.** Did the variables resolve? Did the right contact/opp get touched?
4. **Only then enable.** `mcp__trustpager__enable_automation`. If anything looked off, fix and re-test — don't enable hopefully.
5. **Watch the first runs.** Offer to check `list_automation_runs` after the first real fires to confirm it's behaving.

> If you can only verify a trigger by firing a real event, do it in a **test/demo workspace** with the operator's own contact details — never a real customer's.

---

## 6. The safety dials every automation has

- **`enabled`** — the master switch. Off = inert.
- **`dedup_enabled` + `dedup_window_minutes`** — stops the same trigger firing the automation twice for the same target inside a window. Turn this on for anything that sends, so a double-submit doesn't double-email.
- **`max_executions_per_day`** — a hard daily ceiling. A backstop against a runaway loop or a misconfigured webhook spraying.
- **`priority`** — when several automations match one event, lower number runs first.
- **`conditions`** — the fail-closed gate (§2).

> A `call_webhook` or `create_opportunity` action that feeds back into a trigger can loop. Dedup + `max_executions_per_day` are the seatbelts — set them on anything with a feedback path.

---

## 7. The discovery protocol (do this, don't memorise)

The automation surface changes as the platform ships. Every automation skill follows the same cheap, always-fresh discovery sequence instead of relying on a hardcoded list:

1. **`list_trigger_schemas`** → every event you can react to. `get_trigger_schema(type)` → one trigger's payload + `{{variables}}`.
2. **`list_action_types`** → every action. `describe_action_type(type)` → one action's config schema + example, **right before writing it**.
3. **`list_automations`** → what already exists, so you don't build a duplicate.

The `/automate-this` skill bundles 1–3 into a single `fetch.py` call. All three are free (no credits).

---

## 8. Reading the run log — how to tell what actually happened

Every fire writes an `automations_runs` row. The fields that matter when something looks wrong:

- **`status`** — `completed` (ran), `skipped` (conditions didn't pass — *not* an error), `failed` (an action errored).
- **`trigger_type`** — which event class actually fired it (on a multi-trigger automation, this tells you *which* trigger).
- **`error_message` / `error_details`** — why a `failed` run failed.
- **`actions_attempted` / `actions_completed` / `actions_failed`** + `skipped_action_ids`.
- **`triggered_by_type` / `triggered_by_id`** — the source that fired it.

"It didn't fire" almost always resolves to one of: the automation is **disabled**, **no run row exists** (the trigger never matched — wrong trigger_type or source), a run exists with status **`skipped`** (a condition failed), or a run **`failed`** on an action (read `error_message`). `/why-didnt-it-fire` walks this ladder.

---

## House rules (carry these into every automation skill)

- **One automation per `/automate-this` invocation.** Don't bundle unrelated rules into one chain.
- **Same actions, multiple entry points → multiple triggers on ONE automation** (§1.1). Different actions → separate automations.
- **Action order is load-bearing.** Walk the order with the operator.
- **Test before enable. Always.** (§5)
- **Set dedup + a daily cap on anything that sends or could loop.** (§6)
- **Discover, don't memorise** triggers/actions (§7).
- **A series of timed emails is a queue, not an automation** — hand off (§4).
- **Show a plain-English spec and get a yes before creating anything.**

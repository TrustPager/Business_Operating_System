---
name: Prep For Call
description: Build the brief before a customer call — who they are, the deal, the full history, what was said last time, what's open, and the one outcome to drive. Everything the operator needs to walk in ready, in one read.
triggers:
  - prep for call
  - prep me for the call
  - prep for my 2pm
  - brief me before this call
  - who am I talking to
  - get me ready for the meeting
  - what do I need to know before this call
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__list_bookings
  - mcp__trustpager__get_booking
  - mcp__trustpager__search_contacts
  - mcp__trustpager__search_opportunities
  - mcp__trustpager__get_opportunity
  - mcp__trustpager__get_opportunity_activities
  - mcp__trustpager__list_transcripts
  - mcp__trustpager__get_opportunity_tasks
  - mcp__trustpager__get_contact
  - mcp__trustpager__get_opportunity_products
status: active
---

# Prep For Call

The operator has a call coming up and 5 minutes to get ready. Pull the whole
picture — the person, the deal, the history, what was said last time, what's
outstanding — and hand them the one outcome to drive. One read, walk in ready.

## Step 1 — Identify the call

Resolve which call, in this order:
- **"My 2pm" / "next call" / "today's call"** → `mcp__trustpager__list_bookings`
  for today, pick the one they mean (confirm if several). `get_booking(id)` for
  the attendee + linked opportunity.
- **A named person / company** → `search_contacts` / `search_opportunities` to
  find the opportunity.

The **opportunity is the hub** — once you have its id, everything else hangs off
it. If there's genuinely no opportunity (cold first call), prep off the contact
+ whatever the booking carries, and say it's a first conversation.

## Step 2 — Pull the picture (parallel reads)

For the opportunity + its contact, gather:
- `get_opportunity(id)` — stage, value, type, owner, custom fields.
- `get_opportunity_activities(id)` — the recent history (calls, emails, notes).
- `list_transcripts` for this deal/contact — **the last call's transcript is the
  single most valuable input**; skim it for what was promised and where it left
  off.
- `get_opportunity_tasks(id)` — what's open / owed to them.
- `get_contact(id)` — name, role, contact details, relationship age.
- `get_opportunity_products(id)` — what's been quoted, if anything.

Skip cleanly what isn't there; don't stall on a missing piece.

## Step 3 — Hand over the brief

```
📞 Prep — <Contact name>, <role> @ <company>  ·  <call time>
   Deal: "<name>" — <stage>, <value>  ·  owner: <owner>

WHO THEY ARE
  <1-2 lines: role, relationship length, anything personal on record>

WHERE IT'S AT
  <1-2 lines: current stage, what's been quoted, deal health>

LAST TIME (from <date> <call type>)
  <what was discussed + what was promised — pulled from the last transcript/notes>

OPEN / OWED
  → <open task or commitment 1>
  → <unanswered question / thing we said we'd do>

⚠️ WATCH FOR
  <any risk: gone quiet N days, overdue item they'll mention, declined quote>

🧭 CALL SPINE
  <for discovery/quote/sales calls: run it on the discovery arc
  (business-method.md §12.5). Pre-fill from the record: what they've tried
  (from history), the arrival in THEIR words (from the last transcript), and
  any concern already on the table (from the last log).>

🎯 OUTCOME TO DRIVE
  <the single most useful result from this call — book next step / close / unblock>
```

Only include the CALL SPINE line for sales-shaped calls (an early-stage
opportunity, a quote visit, a first conversation); service and delivery
check-ins don't get it. Clinic shapes: the arc structures logistics and
care-plan conversations only, never the clinical recommendation (§12.5, §15).

End with the one outcome — not a menu. Default outcome when nothing more
specific applies: the next step booked before the call ends. If useful, offer:
*"Want me to draft a quick agenda message to send them before the call, or
pull the last proposal?"*

## Hard rules

- **The last transcript is gold** — always check for one and use what was
  actually said, not a generic guess at the relationship.
- **Use their real data + the operator's stage/product names** — never invent
  history or a relationship detail that isn't on record.
- **One outcome, not five options.** The operator has a call to walk into.
- **Read-only.** Don't log or send anything as part of prepping; offer the
  follow-on (`/draft-reply`, pull the proposal) and wait.
- **First-call honesty** — if there's no history, say "first conversation" and
  prep off what little there is rather than padding.

## Output shape

The brief in the fixed structure above, scannable top to bottom, ending in the
single outcome to drive. Built to be read in the 5 minutes before the call.

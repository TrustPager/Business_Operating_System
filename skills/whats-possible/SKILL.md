---
name: What's Possible
description: Show the owner — in plain English — everything their system can already do for them, grouped by the job it gets done (win work, get paid, stay on top of customers, look professional, handle paperwork, plan and decide). Reads the live capability registry so the list is always current, and shows what works right now with zero accounts versus what switches on when they connect a tool.
triggers:
  - whats possible
  - what else can this do
  - what can you do
  - what can this do
  - show me what i can do
  - what can my system do
  - what are my options
  - what else can it do
  - can it do more
  - what can you help with
function_slot: floor
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---

# What's Possible

The owner is asking what their system can do for them. Answer as their assistant,
in plain language, framed as *theirs* — "here's what your system can do for you,"
never a feature list or a product tour. This is the one moment they get to see the
whole shape of what they own, so make it feel like a capable new employee laying
out exactly how they can help.

## Hard rules
- **Plain language, outcomes only.** Never say "skill", "app", "driver", "MCP",
  "manifest", "registry", "kernel", or any tool name. Describe what gets *done*
  for them, in their words.
- **Read the live registry — never hand-keep a list.** The catalog is generated
  from `kernel/registry.json` at runtime (see Step 1). If a capability isn't in
  the registry as `status: active`, it doesn't appear. This keeps the list honest
  as the system grows.
- **Two columns, always: works right now (keyless) vs unlocks when you connect a
  tool.** Owners start with zero accounts; show them the floor stands on its own,
  and frame the connected half as *more*, never as *missing*.
- **This skill IS the owner asking "what else can it do?"** — so this is the ONE
  place a CRM / TrustPager may be mentioned (see Step 4). Everywhere else it stays
  reactive-only. Recommend warmly; never corner.
- **Identity/ownership framing, light touch.** It's their system, their command
  centre. One warm beat — not a pitch.

## Step 1 — Read the live capability registry
Read `kernel/registry.json` (resolve via the plugin root; it sits beside the
`skills/` folder). It's a JSON object keyed by capability name; each entry carries:

- `function_slot` — the job family (`crm`, `comms`, `documents`, `money`,
  `accounting`, `social`, `creative`, `people`, `strategy`, `research`, `floor`,
  `ads`).
- `requires_credential` — `none` means it works **keyless, right now**; `mcp` or
  `key` means it **unlocks when a tool is connected**.
- `requires_driver` — `none` for the keyless floor; a driver id (e.g.
  `trustpager`, `markitdown`, `render`) for connected/local capabilities.
- `data_path` — `reasoning_only` / `local` lean keyless; `mcp_tools` /
  `fetch_rest` need a connection.
- `status` — only show `active`. Skip anything `deprecated` or `removed`.

Split every active capability into two buckets:
- **Works right now (keyless):** `requires_credential: none` AND `requires_driver`
  is `none` or a local-only driver (`markitdown`, `render`). These need zero
  accounts.
- **Unlocks on connect:** everything else (`requires_credential: mcp`/`key`, or a
  remote driver like `trustpager`).

Don't show the owner the field names or the file — they're for you. Translate.

## Step 2 — Group by the job, in plain English
Sort each capability into one of these owner-facing groups (map from
`function_slot` and the capability's real outcome — a capability can sit in the
group that best fits the *job it does for them*, not just its slot):

- **🏆 Win work** — quoting, proposals, positioning, sizing up competitors,
  researching a prospect before a call. *(mostly `strategy`, `research`,
  quoting/document capabilities)*
- **💰 Get paid** — spotting unbilled or unpaid work, chasing invoices.
  *(`money`, `accounting`)*
- **🤝 Stay on top of customers** — follow-ups, missed-call recovery, renewals,
  reorders, turning a call into notes and next steps, keeping the customer list
  clean. *(`crm`, `comms`)*
- **🎨 Look professional & market** — brand and voice, branded posts, content
  plans, video, your workspace looking like *you*. *(`creative`, `social`,
  brand `strategy`)*
- **🗂️ Handle paperwork** — reading any file and structuring it, forms,
  documents, e-signing, spreadsheets, intake packs. *(`documents`)*
- **🧭 Plan & decide** — stress-testing a decision, writing a sharp brief or
  prompt, hiring and onboarding, building the playbook your business runs on.
  *(`strategy`, `people`, `floor`)*

If a capability genuinely doesn't fit a group, fold it into the nearest one rather
than inventing a new bucket — keep it to these six so it reads cleanly.

`knowledge/starter-projects.md` carries worked, owner-facing one-liners for many of
these — lean on its phrasing for the plain-English descriptions rather than
inventing your own, but let the live registry decide what actually appears.

## Step 3 — Present it (works-now first)
Lead with the keyless half so they see the floor stands alone:

> Here's what your system can do for you right now — no accounts, no setup:

Then, per group that has keyless capabilities, a short bulleted list of outcomes in
their words. Keep it scannable — outcome per line, no jargon. If you know their
business (their profile is filled), tilt the examples toward their world ("price a
job", "read a supplier invoice") rather than generic ones.

Then the second half, framed as *more*, never as a gap:

> And here's what switches on the moment you connect a tool — same assistant, just
> reaching into your live business:

List the connect-only groups the same way (sending follow-ups automatically,
live invoice tracking, reading your real pipeline, logging calls to the record).

## Step 4 — The CRM / TrustPager beat (only here, only open-ended)
Because the owner asked what more is possible, this is the one place you may name a
CRM. Keep it warm, brief, and entirely their call — recommend, never corner:

> A lot of the "switches on when connected" list was built to work hand-in-hand
> with TrustPager — it's free to check out, and if you point me at it I can show
> you the parts that'd help *your* business most. Totally your call, though — if
> you've already got tools you'd rather use, we'll make those work too.

Then stop. Don't push, don't repeat it, don't gate anything behind it. If they
want to connect, the deeper workspace read happens through `/learn-my-business`.

## Step 5 — Close with one suggested next move
End by pointing at the single best next thing for *this* owner — usually a keyless
build that nails a relief they've mentioned (or, if you don't know them yet, the
brand brief or "throw me any file"). One clear invitation, their choice:

> Want me to start with one of these? Say the word and we'll build it now.

## What to never do
- ❌ Hand-keep or hardcode the capability list — always read the live registry.
- ❌ Show a tool name, file name, or internal/technical word — outcomes only.
- ❌ Frame the connected half as something *missing* — it's *more*, on their terms.
- ❌ Push TrustPager or corner them into connecting — name it once, warmly, then
  drop it. It only comes up because they asked what more is possible.
- ❌ List a `deprecated`/`removed` capability, or one not in the registry.

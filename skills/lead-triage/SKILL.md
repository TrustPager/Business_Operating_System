---
name: lead-triage
description: Classify new inbound leads (last 24-48h), score by fit, and draft the right first response per lead — fast track, slow burn, or disqualify.
triggers:
  - triage my leads
  - what came in overnight
  - new leads
  - new enquiries
  - lead triage
  - any new inbounds
  - sort my inbox of new leads
  - which leads should I call first
---

# /lead-triage

Inbound leads have a half-life. The ones who heard back inside the hour convert at roughly 5× the rate of ones who got a same-day response. This skill exists to clear the backlog of new leads fast — classify each, score by fit, draft the right first response, and tee them up for your approval.

## Step 1 — Pull the data (parallel MCP calls)

Fire these **four read calls in parallel** in a single batch — they're all reads, so they're free and fast. Use the `trustpager` MCP server. Pull the most recent records and filter to the window yourself in Step 2.

| Need | Tool | Args |
|---|---|---|
| New form submissions | `list_form_submissions` | `limit: 100` |
| Inbound email threads (first message, not yet replied) | `list_email_threads` | `limit: 100` |
| Inbound SMS conversations (no outbound yet) | `list_sms_conversations` | `limit: 100` |
| Opportunities created in window (open status) | `list_deals` | `limit: 100` |

> Tool names use `deal` for legacy reasons — **always say "opportunity" to the operator**, never "deal".

If one call errors, note it briefly and proceed with the sources you have — don't bail on the whole triage.

## Step 2 — Build the lead list

Everything below is computed against **now**. Default window is the **last 48 hours** (the operator can ask for a tighter 24h window). Build one lead record per inbound, pulling from each source:

- **Form submissions** — keep those created within the window. Read the submission payload for a message: take the first non-empty of `message` / `notes` / `comments` / `enquiry` / `details` / `description`. Capture first/last name (fall back to a single `name` field), email, phone, company, job title, the form name, and any linked contact/opportunity id. Source = `form`.
- **Inbound email threads** — keep those within the window where **we have not replied yet** (drop any thread already replied to). Take the latest message's plain text (or subject) as the message. Capture the contact's name, email (fall back to the from-address), phone, company, the subject, and any linked opportunity id. Source = `email`.
- **Inbound SMS conversations** — keep those within the window with **no outbound message yet** (drop any where we've already replied / outbound count > 0). Take the first inbound body as the message. Capture the contact name, email, phone (fall back to the from-number), and any linked opportunity id. Source = `sms`.
- **Opportunities created in the window** — keep open ones created within the window. **Skip any whose opportunity id was already captured** by a form/email/SMS lead above (no duplicates). Use the opportunity name as the lead name and its description as the message. Source = `manual`.

## Step 3 — Score each lead (0-100)

Add up these points, then cap at 100:

| Signal | Points |
|---|---|
| Has a phone number | +25 |
| Has an email | +15 |
| Has a company OR job title | +15 |
| Message length ≥ 80 chars | +20 (or +10 if ≥ 30 chars but < 80) |
| Source quality | form +25, email +18, sms +10, call +8, manual +5, unknown +0 |

## Step 4 — Classify each lead

Apply in this order:

1. **Disqualify first** — if the message (lowercased) contains any spam signal: `seo services`, `web design`, `partnership opportunity`, `increase your traffic`, `guest post`, `backlink` → category = **disqualify**, regardless of score.
2. Otherwise: score **≥ 70** → **fast_track**; score **40-69** → **nurture**; score **< 40** → **cold**.

| Category | Meaning | Default response |
|---|---|---|
| 🔥 **Fast track** | Has phone, detailed message, form/inbound-email, score ≥ 70 | Personal SMS + email within minutes. Offer a call within 24h. |
| 🌱 **Nurture** | Has email but limited detail, score 40-69 | Templated email asking 2-3 qualifying questions. |
| 🧊 **Cold / unclear** | Score < 40 — no contact info beyond a name, vague message | Light-touch email: "Got your enquiry — can you tell us a bit more about what you're after?" |
| 🚫 **Disqualify** | Spam patterns, wrong industry, SEO/partnership pitches | Don't respond. Optionally mark lost. |

**Rank the list by score descending, then most-recent first.** Show the classification + reasoning to the operator. The operator can override per lead.

## Step 5 — Draft the per-lead response

After classification is agreed, draft the message for each lead. The draft should:
- Use the lead's first name (never "Hi there", never "Hi friend").
- Reference something concrete from their enquiry (their stated need, company name, their question) — this is the moat against generic templates.
- End with a single clear next step ("Are you free Wed or Thurs morning for a 15-min call?", not "Looking forward to hearing from you!").
- Match the tone of the workspace — read recent sent emails to calibrate before drafting.

## Step 6 — Send with approval (per lead)

Writes here are outward-facing — follow the rails in `knowledge/safeguards.md`: **show the draft, wait for approval, then journal the write to `.bos-journal.md`**, and **search first** so you never double-send.

For each draft:
- Show the operator: lead name, category, channel, the proposed message.
- Wait for explicit yes/no **per lead**. NEVER batch-send.
- Before sending, do a quick `search_contacts` / `list_sms_conversations` / `list_email_threads` check to confirm a response hasn't already gone out (idempotency — never blind-send).
- On yes: send via `send_email` or `send_sms` for the per-lead channel (on the `trustpager` MCP server). If a write comes back `202` / `approval_id`, surface the approvals link and stop — don't retry (safeguards §1).
- After each send, append one line to `.bos-journal.md` (timestamp, tool, outcome, id, `skill: lead-triage`).
- On no: ask what to change, or skip.

## Important behaviours

- **Create the opportunity first if missing.** Every fast-track lead becomes an opportunity in the pipeline before the message goes out — call `create_deal` (it's the opportunity-create tool) with the right pipeline + stage + contact link. Journal it.
- **Disqualify ≠ delete.** Mark with a lost status + reason via `update_deal` so it can be reviewed later. Never delete.
- **Spam heuristics.** Free email + generic body + "SEO services / web design proposal / partnership opportunity" = disqualify by default.
- **Don't promise specifics you don't know.** "Our standard package starts at $X" — only if the operator told you the figure or it's in workspace knowledge.
- **Quiet hours.** Before 7am / after 8pm in the recipient's timezone (or unknown) → email, not SMS.

## Output shape

End with a one-line summary: "Triaged N leads — F fast track sent, S nurture sent, C cold sent, D disqualified, R skipped for your review."

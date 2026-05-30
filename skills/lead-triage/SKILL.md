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

## Step 1 — Pull the leads

Run the fetch script. It returns every new lead in the last N hours (default 48), enriched with:
- Source (form submission, inbound email, inbound SMS, inbound call, manual entry)
- Whether they have an opportunity yet
- Contact details (email, phone, company)
- Initial message / form payload
- A fit score (0-100) based on completeness, source quality, and message length
- Recency

```
python skills/lead-triage/fetch.py
python skills/lead-triage/fetch.py --hours 24    # tighter window
```

## Step 2 — Classify each lead

For each lead, propose a category:

| Category | Definition | Default response |
|---|---|---|
| 🔥 **Fast track** | Has phone, has detailed message, source is form/inbound-email, score ≥ 70 | Personal SMS + email within minutes. Offer call within 24h. |
| 🌱 **Nurture** | Has email but limited detail, score 40-69 | Auto-templated email asking 2-3 qualifying questions. |
| 🧊 **Cold / unclear** | Score < 40 — no contact info beyond name, vague message | Light-touch email: "Got your enquiry, can you tell us a bit more about what you're after?" |
| 🚫 **Disqualify** | Spam patterns, wrong industry, asking for partnership/SEO services, etc. | Don't respond. Optionally archive. |

Show the classification + reasoning to the user. The user can override per lead.

## Step 3 — Draft the per-lead response

After classification is agreed, draft the message for each lead. The draft should:
- Use the lead's first name (never "Hi there", never "Hi friend")
- Reference something concrete from their enquiry (their stated need, their company name, their question) — this is the moat against generic templates
- End with a single clear next step ("Are you free Wed or Thurs morning for a 15-min call?", not "Looking forward to hearing from you!")
- Match the tone of the workspace — read recent sent emails to calibrate before drafting

## Step 4 — Send with approval (per lead)

For each draft:
- Show the user: lead name, category, channel, the proposed message.
- Wait for explicit yes/no per lead. NEVER batch-send.
- On yes: send via `mcp__trustpager__send_email` or `send_sms` for the per-lead channel.
- On no: ask what to change, or skip.

## Important behaviours

- **Create the opportunity first if missing.** Every fast-track lead becomes an opportunity in your pipeline before the message goes out. The skill should call `create_opportunity` with the right pipeline + stage + contact link.
- **Disqualify ≠ delete.** Mark with a "lost" status + reason so you can review later. Never delete.
- **Spam heuristics.** Free email + generic body + "SEO services / web design proposal / partnership opportunity" = disqualify by default.
- **Don't promise specifics you don't know.** "Our standard package starts at $X" — only if the user told you the figure or it's in workspace knowledge.
- **Quiet hours.** Same as missed-call-recovery — before 7am / after 8pm = email not SMS.

## Output shape

End with a one-line summary: "Triaged N leads — F fast track sent, S nurture sent, C cold sent, D disqualified, R skipped for your review."

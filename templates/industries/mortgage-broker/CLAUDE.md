# CLAUDE.md — Mortgage / Finance Broker

> Drop this file into the root of your project folder. Claude Code reads it
> at the start of every session and uses it as context for everything you
> ask. Edit anything in `<<< ... >>>` to match your business.

---

## My business

I'm a `<<< mortgage broker / finance broker / aggregator-affiliated broker >>>` based in `<<< city / state >>>`. I focus on `<<< residential lending / commercial / SMSF / refinance / first-home-buyers >>>`. My team is `<<< just me / N brokers / N brokers + N support >>>`.

I work `<<< inside an aggregator (name) / independently >>>`. My CRM of record is TrustPager — that's where my client data lives, my own database, separate from any aggregator software. **Treat the TrustPager workspace as the source of truth for everything.**

## My lending panel

I write loans through: `<<< list your lenders / aggregator panel — e.g. CBA, NAB, Westpac, Macquarie, AMP, ING, Pepper, La Trobe, Liberty, etc. >>>`

When drafting client comms about products, default to the lenders on my panel unless I name a specific one.

## My pipeline

The typical mortgage-broker pipeline in my TrustPager workspace looks like:

1. **New enquiry** — lead just came in (Meta ad, website form, referral)
2. **Fact-find scheduled** — initial discovery call booked
3. **Documents collected** — payslips, ID, bank statements, expenses
4. **Pre-approval submitted** — application sent to lender
5. **Pre-approval received** — lender has issued conditional approval
6. **Property identified** — client has found a property, valuation may be ordered
7. **Formal approval** — unconditional approval issued
8. **Settled** — loan funded, commission triggered

When I say "where's [client name] at?", check their opportunity stage in this pipeline.

## My products

In TrustPager I track these as products on each opportunity:

- Home loan (owner-occupier or investor)
- Refinance
- Top-up / equity release
- Construction loan
- SMSF loan
- Commercial loan
- Personal loan
- Asset finance / car loan

## What's special about this industry

**Compliance and data ownership matter.** I need to retain client records for 7 years. My data must stay in MY workspace, not any aggregator's database. When you help me with client comms, always log them as activities on the opportunity so I have a complete audit trail.

**Credit checks (Equifax) are increasingly required upfront.** If I'm sending a client to a lender, more lenders now want a credit pull beforehand. Flag this when a client moves from "Documents collected" to "Pre-approval submitted" if I haven't recorded one yet.

**Referrals are the lifeblood.** Most of my work comes from past clients, accountants, financial planners, and real estate agents. When a deal settles, prompt me about whether to ask for a referral.

**Birthday and anniversary touches.** A "happy birthday" or "5 years since your loan settled" message keeps me top-of-mind for refinances. The `/follow-up-radar` skill should surface these.

**My team rarely reads emails the same day.** If you're drafting comms to my office, schedule for next business morning rather than send immediately — unless it's time-critical.

## How to talk to me

I'm a relationship-driven broker, not a tech person. When you walk me through something:

- Use plain English, not API jargon
- Suggest one action at a time, not five
- When you draft an email or SMS, sound like ME — direct, warm, professional, no jargon like "synergy" or "leverage"
- If you don't know something about my business, ASK before guessing

## How to draft client comms

When drafting any client-facing message:

- ✅ Sign off as me (use my name from my TrustPager workspace profile)
- ✅ Reference the specific deal, lender, or product they're working on
- ✅ Be specific about next steps and timing
- ✅ Plain text — no big email banners or marketing chrome
- ❌ Never use "Dear Sir/Madam" — use their first name
- ❌ Never quote a rate without checking my current panel
- ❌ Never promise a settlement date — the lender controls that
- ❌ Never include the word "guarantee" unless I tell you to

## Tools I rely on

The TrustPager MCP gives you access to my workspace. Lean on these:

- **`list_opportunities` / `get_opportunity`** — every deal lives here
- **`add_note` / `log_meeting` / `log_call`** — activity timeline, my audit trail
- **`send_email` / `send_sms`** — comms with full logging
- **`create_task` / `complete_task`** — my to-do list
- **`list_transcripts`** — recordings from fact-find calls
- **`ai_transcript_summary`** — turn a recording into a usable summary
- **`get_pipeline_summary`** — gut check on the business
- **`search_help_center`** — when I ask "how do I do X in TrustPager"

## When in doubt

When you don't know how I'd handle something, ask one short question. I'd rather pause for 10 seconds than have you guess wrong on a client communication.

## What's mine vs what's the aggregator's

Anything in TrustPager → mine. Anything in `<<< aggregator software name >>>` → theirs. If a client is in both systems, TrustPager is the source of truth for relationship history, comms, notes, and follow-up actions. The aggregator software is the source of truth for the lender application and lodgement.

When I switch aggregators (or go independent), my data comes with me because it's in MY TrustPager workspace.

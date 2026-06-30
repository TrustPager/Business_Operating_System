# Business Operating System

**Run your business from Claude.**

A library of skills, slash commands, and templates that turn Claude Code into a hands-on operator for your business: writing your proposals and policies, pricing your work, researching a competitor, turning a photo into a quote, prepping you for the next call. It works on day one with no accounts and no setup, and grows deeper when you connect the tools you already use.

---

## Start here

**New? Type `/start-here`.** Your assistant introduces itself, learns your business from a 60-second brain-dump (no accounts, no files, nothing to install), and hands you a real win on the spot: a first proposal, a priced quote, a competitor read, or a brand brief. One short conversation and you're operating.

```
You:    /start-here
Claude: Right, I'm your new AI assistant. Tell me what you do, who it's for,
        and what eats most of your week. Got a website? Drop it in and I'll do
        my own homework.
You:    "Solo sparky in Geelong. Quoting eats my week."
Claude: → here's your business as I now understand it
        → and here's a finished, priced quote you can send today
```

That's the keyless floor: real work, zero setup. From there `/whats-possible` shows everything your system can already do.

---

## What this is

Business Operating System (BOS) is a free, open-source pack you install once into Claude Code. After that, talking to Claude is the same as running your business, because every skill in here is a battle-tested workflow distilled from real operations.

You don't need to learn an API. You don't need to memorise tool names. You ask Claude to do the thing. Claude calls the right tools, in the right order, with the right safeguards.

**The keyless floor works on day one.** No accounts. No subscription. No API key. Real wins from minute one.

**TrustPager is the optional deepener.** Connect it when you want always-on workflows: live pipeline, automations, server-side reports, nurture sequences running in the background. It needs a subscription and a connection step. When you're ready, those workflows switch on automatically.

---

## What's in the box

The complete, up-to-date capability list lives in [docs/CAPABILITIES.md](./docs/CAPABILITIES.md). That doc is generated directly from the plugin and is the single source of truth; this section gives you the shape.

### Keyless day-one wins

Everything below works the moment you install BOS. No account, no key, no setup beyond the install itself.

**Win work**
- Price a job with your margin shown
- Turn a site photo into a drafted quote or proposal
- Write the proposal that closes the deal, in your voice
- Research a competitor's positioning and pricing
- Walk into any call with a one-page brief on the person or company

**Know your numbers**
- Profit per job (every cost counted, margin shown as a dollar figure)
- Cash flow forecast (week-by-week, live spreadsheet, change a number and the balance updates)
- BAS estimate for Australian businesses (G1, 1A, 1B shown and cited)
- Renewal tracker (licences, insurances, certifications, days-until-renewal auto-calculated)

**Content and brand**
- Brand strategy from how you already talk about your work
- Customer voice from your real call transcripts
- Social content plan and publish-ready post copy
- Product descriptions for your store or catalogue

**Paperwork and documents**
- Extract data from any file: PDF, Word, Excel, scanned image, HTML
- Compare two documents and see exactly what changed
- Turn a paper form or contract into a reusable digital template
- Spreadsheets you can open and use today (job tracker, cashflow, lead log)

**Decisions and planning**
- Pressure-test a decision before you commit (grill-me-on-this)
- Write a job ad with screening questions that filter applicants
- Turn how you handle something into clean policy or FAQ text
- Onboard a new team member with your standards baked in

### Keyless but heavier setup (optional studios)

These work keyless but need their studio started first (one `npm install` per studio, documented in their README):

- Design and render branded social posts (Instagram, LinkedIn, X) at `localhost:3216`
- Design and render YouTube thumbnails at `localhost:3210`

### Switches on when you connect TrustPager

TrustPager is a CRM platform built for small service businesses. Connecting it (subscription required, a connection step documented in [INSTALL.md](./INSTALL.md)) unlocks the always-on workflows:

- Morning briefing across your live pipeline, tasks, and messages
- Follow-up radar: deals gone quiet, draft re-engagement ready to approve
- Missed call recovery: draft the text or callback message, ready to send
- Live lead triage with first-response drafts
- Call logging: recap captured, deal updated, next step scheduled
- Email drafts and sends in your tone
- Automations: describe a repetitive task, get a working trigger-action built
- Automation health-check: which are firing, stale, erroring, and why
- Nurture sequences: draft, wire live, check health per step
- Recurring reports emailed to you on a schedule
- Documents, forms, and e-signing with open/sign/submit tracking
- Team tools: delegate work, review drafts before they reach a customer, weekly rollup

See [docs/CAPABILITIES.md](./docs/CAPABILITIES.md) for the full breakdown, split by tier.

---

## Who this is for

You run a 2-10 person business and you want things to stop slipping through the cracks. Trades, ecommerce, hospitality, allied health, consulting, small manufacturing, any shape of small business. You want an AI that actually does the work, not just tells you about it. And you want it to work today, not after nine months of setup.

BOS is built for that.

---

## How to install

The easiest path: tell Claude to get the Business Operating System for you.

```
You:    Go get the Business Operating System from TrustPager.
Claude: → clones the public repo
        → installs the small helper libraries (document reading, PDF tools)
        → no key required, no account needed
```

Then fully close and reopen Claude Code (skills load at startup) and type `/start-here`.

Full step-by-step, including how to connect TrustPager when you're ready: **[INSTALL.md](./INSTALL.md)**

If anything is ever missing, your assistant offers to add it and does it for you, so you never need to run a command yourself. See [knowledge/setup-and-dependencies.md](./knowledge/setup-and-dependencies.md).

---

## Going deeper: connect your business

`/start-here` gets you operating keyless. When you're ready for the always-on workflows, connect TrustPager (see [INSTALL.md](./INSTALL.md)), then run `/learn-my-business`.

**`/learn-my-business`** reads your live workspace and writes your `CLAUDE.md` for you: your real pipeline, products, and brand, with the gotchas for your line of work. Re-run it whenever your workspace changes. (`/start-here` already wrote a first profile from your brain-dump; this enriches it from live data once you're connected.)

Prefer to do it by hand? Start from the [generic template](./templates/CLAUDE.md) and fill in the blanks. Business gotchas live in [knowledge/industry-notes.md](./knowledge/industry-notes.md), organised by business shape (service/professional, trades/on-the-tools, product-seller/ecommerce-retail, hospitality/walk-in, clinic/appointment) with the per-vertical specifics nested inside.

---

## TrustPager: the optional deepener

TrustPager is a CRM, automation, and client portal platform built for Australian service businesses. BOS was built alongside it, and the two work hand-in-hand.

What connecting TrustPager adds:

- A live pipeline your assistant reads and updates
- Automations that run server-side with no browser open
- Nurture sequences that enrol, send, and report on their own
- Documents, forms, and e-signing with tracked envelopes
- Recurring email reports to you and your team
- Voice agents that answer your calls when you can't

You don't need TrustPager to get real value from BOS. When you're ready for the always-on layer, it's there. Sign up at [trustpager.com](https://trustpager.com) and follow the connection steps in [INSTALL.md](./INSTALL.md).

---

## What's a skill?

A skill is a small Markdown file Claude reads automatically when you mention what you want to do. There's no UI, no menu, no click-through wizard. You say "what should I charge for this job" and `/price-my-work` fires.

Every skill in here:
- Is open source and inspectable: read the source, modify it, fork it
- Only ever talks to your own workspace (never anyone else's)
- Asks before doing anything destructive
- Logs what it did, so you can see the trail: every write lands in `~/.claude/bos-journal/`; read it any time with `python tools/journal.py`

The live list of every active capability lives in [`kernel/registry.json`](./kernel/registry.json), generated from the skills by `tools/registry-generator.py`. From that same registry, `tools/export-capabilities.py` generates [`docs/CAPABILITIES.md`](./docs/CAPABILITIES.md): the plain-language, GTM-facing capability list, grouped by the job each capability gets done and split into what works keyless versus what switches on when you connect a tool. That doc is the single source of truth for what BOS can do. External docs and go-to-market material should reference it rather than restating the feature list, so the story never drifts from the plugin. Both are CI-checked for freshness, so neither can go stale.

## Subagents

Some work is heavy enough that it should run in its own context rather than flooding your conversation. BOS ships two subagents Claude delegates to automatically when the task fits. They live in [agents/](./agents/):

- **`workspace-analyst`**: read-only deep dives. Full pipeline sweeps, automation/nurture health audits, data-quality scans. It does the fanning-out and hands back the conclusion, not the raw data. Never writes.
- **`nurture-architect`**: the marketing pack's long reads: building the customer-voice synthesis from every transcript, authoring the brand docs, drafting a sequence. It produces drafts for you to review; deploying them stays in the main thread after your approval.

---

## Want to add a skill?

Pull requests welcome. The [skills/](./skills/) directory has the format. Start with [skills/sweep-my-day/SKILL.md](./skills/sweep-my-day/SKILL.md) as the gold-standard example.

---

## What this is not

- **Not a TrustPager requirement.** BOS works fully keyless from day one. TrustPager is the optional layer that adds always-on workflows; it is not a prerequisite.
- **Not a chat widget.** Claude Code runs on your machine. Your data stays in your workspace.
- **Not for everyone.** If you have already automated your way out of all of this in Salesforce, you probably don't need it.

---

## Licence

MIT. Use it, fork it, ship it. See [LICENSE](./LICENSE).

---

## Australian made

Built in Byron and Melbourne, where every customer call ends with "no worries."

[trustpager.com](https://trustpager.com) · [docs](https://docs.trustpager.com)

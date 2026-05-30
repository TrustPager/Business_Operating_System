# Business Operating System

**Run your business from Claude. Built on TrustPager.**

A library of skills, slash commands, and templates that turn Claude Code into a hands-on operator for your TrustPager workspace — drafting follow-ups, triaging leads, recovering missed calls, prepping you for the next call, logging the last one.

---

## What this is

Business Operating System (BOS) is a free, open-source pack you install once into Claude Code. After that, talking to Claude is the same as running your business — and Claude knows how, because every skill in here is a battle-tested workflow distilled from real TrustPager operations.

You don't need to learn the TrustPager API. You don't need to memorise tool names. You ask Claude to do the thing. Claude calls the right tools, in the right order, with the right safeguards.

```
You:    "What needs my attention today?"
Claude: /sweep-my-day
        → 3 hot leads from yesterday that haven't been replied to
        → 2 quotes overdue from last week
        → 1 missed call from a returning customer (drafting recovery SMS now)
```

---

## What's in the box

**📋 Daily operations**
- `/sweep-my-day` — morning briefing across your whole workspace
- `/follow-up-radar` — surfaces opportunities that have gone quiet
- `/missed-call-recovery` — drafts recovery messages for every missed call
- `/weekly-review` — Friday rollup of what shipped, what stalled

**📞 Sales workflow**
- `/lead-triage` — classifies new leads and drafts the right first response
- `/prep-for-call` — builds your brief before any customer call
- `/log-this-call` — captures the recap, updates the opportunity, schedules the next step
- `/draft-reply` — drafts an email response in your tone
- `/send-email` — TrustPager Mail with all the quality rails built in

**🧹 Setup & maintenance**
- `/brand-my-workspace` — point it at your website, your TrustPager workspace inherits the brand
- `/import-from-anywhere` — paste a CSV, a PDF, a screenshot, an email export — Claude normalises it into your workspace
- `/sync-from-xero` — connects accounting to opportunities
- `/audit-my-data` — finds missing fields, duplicates, stale records

**🎓 Help & learning**
- `/show-me-how` — describe what you want to do, Claude walks you through it
- `/quote-from-photo` — site photo + voice memo → drafted proposal in 60 seconds
- `/transcript-summary` — record a call, get a usable document

**🤖 Power moves**
- `/make-it-happen` — describe what you want done in plain English. Claude figures out which TrustPager tools to call.
- `/automate-this` — describe a repetitive task. Claude builds the automation.

**📣 Marketing strategy (build your voice → ship a nurture sequence)**
- `/build-customer-voice` — pull ≥5min call + meeting transcripts, extract verbatim customer pain into a 10-section synthesis. Foundation for everything else.
- `/build-brand-strategy` — author positioning, ICP, voice, value-props, content-pillars from the synthesis. Every claim anchored in a real customer quote — no invented sales copy.
- `/design-nurture-sequence` — draft a multi-step email sequence in your voice. Picks the help-center video for each stage. Drafts in chat, no live writes.
- `/wire-nurture-sequence` — push approved drafts into a live TrustPager auto queue via MCP. Handles the step_order shuffle safely.

The method behind these four is in [knowledge/marketing-strategy-method.md](knowledge/marketing-strategy-method.md).

---

## Who this is for

You're a 2-10 person Australian business — trades, mortgage or insurance broking, allied health, consultancy, small manufacturing — and you're done juggling 40 different tools to keep track of what's going on.

You don't need the AI revolution. You need things to stop slipping through the cracks. You don't want another monthly bill. You don't want to spend nine months learning HubSpot. You want your CRM in your back pocket and an AI that actually does the work, not just tells you about it.

If that's you — this is built for you.

---

## How to install

1. Sign up for TrustPager and grab your API key from your workspace settings
2. Run the installer (see [INSTALL.md](./INSTALL.md))
3. Restart Claude Code
4. Type `/sweep-my-day` and say good morning

Full step-by-step: **[INSTALL.md](./INSTALL.md)**

---

## Industry templates

Drop one of these into your project folder and Claude starts every session knowing the shape of your business:

- [Mortgage / finance broker](./templates/industries/mortgage-broker/CLAUDE.md)
- [Trades & on-the-tools](./templates/industries/trades/CLAUDE.md)
- [Insurance broker](./templates/industries/insurance/CLAUDE.md)
- [Consultant / professional services](./templates/industries/consultant/CLAUDE.md)
- [Allied health](./templates/industries/allied-health/CLAUDE.md)
- [Small manufacturing](./templates/industries/manufacturing/CLAUDE.md)
- [Generic starter](./templates/CLAUDE.md) — start here if none of the above fit

---

## What's a skill?

A skill is a small Markdown file Claude reads automatically when you mention what you want to do. There's no UI, no menu, no click-through wizard — you say "what needs my attention" and `/sweep-my-day` fires.

Every skill in here:
- Is open source and inspectable — read the source, modify it, fork it
- Only ever talks to your TrustPager workspace (never anyone else's)
- Asks before doing anything destructive
- Logs what it did, so you can see the trail

---

## Want to add a skill?

Pull requests welcome. The [skills/](./skills/) directory has the format. Start with [skills/sweep-my-day/SKILL.md](./skills/sweep-my-day/SKILL.md) as the gold-standard example.

---

## What this is not

- **Not a replacement for TrustPager.** This rides on top of it. You need a TrustPager workspace.
- **Not a chat widget.** Claude Code runs on your machine. Your data stays in your workspace.
- **Not for everyone.** If you've already automated your way out of all of this in Salesforce, you don't need it.

---

## Licence

MIT. Use it, fork it, ship it. See [LICENSE](./LICENSE).

---

## Australian made

Built in Byron and Melbourne, where every customer call ends with "no worries."

[trustpager.com](https://trustpager.com) · [docs](https://docs.trustpager.com)

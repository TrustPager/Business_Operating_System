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
- `/learn-my-business` — reads your live workspace and writes your `CLAUDE.md` for you (pipeline, products, brand) — no template to hand-fill
- `/brand-my-workspace` — point it at your website, your TrustPager workspace inherits the brand
- `/import-from-anywhere` — paste a CSV, a PDF, a screenshot, an email export — Claude normalises it into your workspace
- `/sync-from-xero` — connects accounting to opportunities
- `/audit-my-data` — finds missing fields, duplicates, stale records
- `/add-a-field` — add a custom field (text or dropdown, e.g. broker name, settlement date) and surface it on the opportunity card and in your spreadsheets

**🎓 Help & learning**
- `/show-me-how` — describe what you want to do, Claude walks you through it
- `/quote-from-photo` — site photo + voice memo → drafted proposal in 60 seconds
- `/transcript-summary` — record a call, get a usable document

The complete feature-by-feature, page-by-page reference for the whole platform — every screen, button, and setting — is in [knowledge/platform-guide.md](knowledge/platform-guide.md). When `/show-me-how` needs the exact location of something, that's where it looks.

**🤖 Power moves**
- `/make-it-happen` — describe what you want done in plain English. Claude figures out which TrustPager tools to call.
- `/automate-this` — describe a repetitive task. Claude builds the automation — one trigger or several (fire from a form *and* a webhook), conditions, ordered actions, tested before it goes live.
- `/audit-my-automations` — health-check every automation: which are firing, stale, erroring, missing dedup/daily-caps, or overlapping. Problems first, each with a one-line fix.
- `/why-didnt-it-fire` — an automation didn't do what you expected? Get the one real reason — disabled, never matched, a condition skipped it, or an action failed — plus the fix.

The method behind automations is in [knowledge/automation-method.md](knowledge/automation-method.md); a catalogue of ready-to-adapt automations (missed-call recovery, lead intake, review requests, renewal reminders, and more — tagged by industry) is in [knowledge/automation-recipes.md](knowledge/automation-recipes.md).

**📈 Reporting & cash flow (know your numbers, on a schedule)**
- `/outstanding-invoices` — who owes you money. Pulls accounts receivable from your connected accounting integration into an aged summary (Current / 1-30 / 31-60 / 61-90 / 90+), surfaces the worst offenders, and — if you want — builds a dashboard and emails it to you (and your bookkeeper) every morning.
- `/email-me-a-report` — deliver *any* report as a recurring email digest. Pick or build a dashboard, choose recipients and a cadence (e.g. 7am weekdays), and it lands in your inbox server-side with nothing open. The same mechanism behind the built-in Team Task Digest.
- `/build-spreadsheet` — build a spreadsheet: a **workspace** sheet that pulls live from your CRM (e.g. settled-this-month by broker, with monthly views + totals and a rolling auto-create), or a **standalone** sheet for its own data (a calculator, a tracker, or an existing Excel imported in).

The method behind the reporting engine — sources, measures, dimensions, the aged-receivables pattern, and the "email any dashboard on a schedule" unlock — is in [knowledge/reporting-method.md](knowledge/reporting-method.md). The receivables source seeds once from your accounting integration then stays live on its own (the synced-ledger model is in [knowledge/safeguards.md](knowledge/safeguards.md)).

**🏗️ Build & run your processes** *(documents & signing, forms, work orders)*

The core things owners actually operate on TrustPager — each as a full lifecycle: **build → wire/send → lint → radar**.

- `/build-document` — design a reusable signing template (sections, merge fields, signer inputs), created in your workspace
- `/send-for-signing` — send a copy to signers with the rails (confirm signers, preview the merged document); creates a tracked envelope
- `/lint-document` — pre-flight a template: every signer has a signature, no broken merge fields, no leftover placeholders
- `/signing-radar` — who opened but hasn't signed (call them now), who never opened and is going stale, who declined
- `/build-form` — design a form template (fields, types, order) from a description or an existing paper form
- `/wire-form` — map each field to its CRM variable so answers land on the record, then connect the form to how it's used
- `/lint-form` — catch orphan fields, label↔wiring mismatches, and missing required fields before it ships
- `/form-radar` — who started but didn't finish (nudge), who never opened it (chase), what completed this week
- `/test-form` — safely test a form or client portal (send it to yourself / a test contact, confirm answers map onto the record) before any real customer sees it
- `/build-work-order-process` — define the statuses jobs move through and the fields captured on each
- `/work-order-radar` — which jobs have stalled in one status, which completed (did the customer get told?)

The methods are in [knowledge/document-method.md](knowledge/document-method.md), [knowledge/form-method.md](knowledge/form-method.md), and [knowledge/work-order-method.md](knowledge/work-order-method.md). Because every send lands on a TrustPager-hosted page, the open/sign/submit signals (`signature_opened`, `form_opened`, `work_order_opened`) drive your follow-ups automatically — that's what the radars run on.

**📣 Marketing strategy (build your voice → ship a nurture sequence)**
- `/build-customer-voice` — pull ≥5min call + meeting transcripts, extract verbatim customer pain into a 10-section synthesis. Foundation for everything else.
- `/build-brand-strategy` — author positioning, ICP, voice, value-props, content-pillars from the synthesis. Every claim anchored in a real customer quote — no invented sales copy.
- `/design-nurture-sequence` — draft a multi-step email sequence in your voice. Picks the help-center video for each stage. Drafts in chat, no live writes.
- `/wire-nurture-sequence` — push approved drafts into a live TrustPager auto queue via MCP. Handles the step_order shuffle safely.
- `/lint-nurture-sequence` — check a sequence against the house style before it ships (clickable CTA above every image, consistent sign-off, positive subjects) and catch drift across the set. Works on live queues or drafts.
- `/nurture-health` — once it's live, see whether it's working: the enrolment funnel, which step is leaking the most people, per-step open/click rates, and whether the un-enrol side is firing. Closes the loop the design + wire steps leave open.

The method behind the strategy skills is in [knowledge/marketing-strategy-method.md](knowledge/marketing-strategy-method.md); the multi-channel reawakening / win-back machines are in [knowledge/automation-recipes.md](knowledge/automation-recipes.md) (R19/R20).

**🎬 Content production**
- `/make-thumbnail` — design and render a 1280×720 YouTube thumbnail for one of your tutorial videos using the bundled studio. Browser preview at `localhost:3210`, puppeteer-rendered PNG, optional one-command publish to your TrustPager Files folder.
- `/make-social-post` — design and render branded social posts in four formats (Instagram square 1080×1080 + portrait 1080×1350, LinkedIn 1200×627, X 1600×900) using the bundled Social Studio. Browser preview at `localhost:3216`, puppeteer-rendered PNG, optional one-command publish to your TrustPager Files folder.

The thumbnail studio lives at [studio/thumbnails/](studio/thumbnails/) — a Vite + React + Puppeteer pipeline with the design rules distilled from 22+ iterations. The 6 example PNGs in `studio/thumbnails/examples/` are real thumbnails from FinalPiece's TrustPager tutorial series — keep them as inspiration or wipe `src/data/samples.json` and start fresh. Method summary: [knowledge/youtube-thumbnail-method.md](knowledge/youtube-thumbnail-method.md).

The social studio lives at [studio/social/](studio/social/) — the same pipeline, one headline-first design language across all four formats, with an optional product card, stat strip, or testimonial. Method summary: [knowledge/social-post-method.md](knowledge/social-post-method.md).

The OG image studio lives at [studio/og/](studio/og/) — the same pipeline at 1200×630, producing the link-preview images that unfurl when your pages are shared on Slack, LinkedIn, X, and Facebook. One sample per page/route; headline + accent word + a product hero, all brand.json-driven. Browser preview at `localhost:3217`, puppeteer-rendered PNG, copy into your site's `public/og/` (with the `og:image` meta tags) or one-command publish to your TrustPager Files folder. See [studio/og/README.md](studio/og/README.md).

**📄 Document tools** *(Microsoft MarkItDown is the standard for reading any file)*

Every "read a document" skill converts the file to Markdown first (via [tools/markitdown_convert.py](tools/markitdown_convert.py)) so Claude works on clean text, not raw bytes. The method is in [knowledge/document-tools-method.md](knowledge/document-tools-method.md).

- `/extract-document` — pull the data out of any file (PDF, Word, Excel, image/scan, HTML): answer a question, summarise it, or map the fields onto a CRM record.
- `/update-pdf` — fill a PDF (a lender/application/agreement form) with a CRM record's data; reads the blank form first, maps the fields, writes a filled copy to review.
- `/outstanding-documents` — per client, what supporting documents you asked for versus what's arrived, so you chase exactly what's missing (not "your form's incomplete"). Most-overdue first, reminder ready.
- `/assemble-pack` — combine a record's filled forms and uploaded files into one ordered PDF pack, ready to send to a lender, insurer, underwriter, or council.
- `/build-knowledge-base-from-docs` — turn your policy / FAQ / product docs into TrustPager AI Knowledge, so the in-app assistant and your voice agents answer from your real documents.
- `/template-from-document` — turn an existing paper/PDF form into a TrustPager form template, or a contract into a signing template.
- `/compare-documents` — compare two files (contract v1 vs v2, a revised quote) and show exactly what changed, in plain language.

**👥 Run your team** *(for owners + managers running staff on Claude Code)*

The standard way to run a team on TrustPager: everyone operates on Claude Code with the same standards baked into their own setup, so the business sounds like one company and nothing reaches a customer unverified.

- `/onboard-team-member` — set a new hire up with your team's standards baked in. Generates their `CLAUDE.md` + a memory pack + a role-scoped command list from your team-standards file, so they sound like the team and follow the same process from day one.
- `/sync-team-standards` — changed a standard? Push it to everyone's pack with a per-person diff, so the team updates instead of drifting.
- `/delegate-this-work` — hand work to a team member: creates the task assigned to them, notifies them, and sets you a follow-up to verify it's done.
- `/review-team-draft` — review a teammate's customer-facing draft before it ships: in the team voice, and confirmed working, then approve it or send it back with a note.
- `/team-review` — the team version of `/weekly-review`: who shipped what, which deals moved through whose hands, and where work is stuck.
- `/write-prompt` — turn a rough ask into a complete, explicit prompt to hand a person or Claude — goal, context, exact inputs, steps, output format, no vague placeholders.
- `/report-an-issue` — hit a bug or want a feature? File a clean, well-structured request to the TrustPager team without leaving Claude; they fix it, verify it, then tell you how to use it.

Your team's standards live in one place you edit — [templates/team-standards.md](templates/team-standards.md) (voice, the verify-before-a-customer-hears-it gate, roles, approval rules). The one customer voice everyone uses is [knowledge/communication-voice.md](knowledge/communication-voice.md); the prompt-writing standard is [knowledge/prompt-writing-method.md](knowledge/prompt-writing-method.md).

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

## Setting up your business context

Claude works best when it knows the shape of your business. The easiest way:

**Run `/learn-my-business`.** It reads your live TrustPager workspace and writes your `CLAUDE.md` for you — your real pipeline, products, and brand — folding in the gotchas for your line of work. Re-run it whenever your workspace changes.

Prefer to do it by hand? Start from the [generic template](./templates/CLAUDE.md) and fill in the blanks. Industry-specific gotchas (mortgage/finance, trades, insurance, consulting, allied health, manufacturing) live in [knowledge/industry-notes.md](./knowledge/industry-notes.md) — one section per vertical, which `/learn-my-business` pulls from automatically.

---

## What's a skill?

A skill is a small Markdown file Claude reads automatically when you mention what you want to do. There's no UI, no menu, no click-through wizard — you say "what needs my attention" and `/sweep-my-day` fires.

Every skill in here:
- Is open source and inspectable — read the source, modify it, fork it
- Only ever talks to your TrustPager workspace (never anyone else's)
- Asks before doing anything destructive
- Logs what it did, so you can see the trail — every write lands in `~/.claude/bos-journal/`; read it any time with `python tools/journal.py`

## Subagents

Some work is heavy enough that it should run in its own context rather than
flooding your conversation. BOS ships two subagents Claude delegates to
automatically when the task fits — they live in [agents/](./agents/):

- **`workspace-analyst`** — read-only deep dives. Full pipeline sweeps,
  automation/nurture health audits, data-quality scans. It does the fanning-out
  and hands back the conclusion, not the raw data. Never writes.
- **`nurture-architect`** — the marketing pack's long reads: building the
  customer-voice synthesis from every transcript, authoring the brand docs,
  drafting a sequence. It produces drafts for you to review; deploying them
  stays in the main thread after your approval.

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

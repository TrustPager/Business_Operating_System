# YouTube Titles & Descriptions — the owner's channel

The system for writing titles and descriptions that ship with every video. The thumbnail studio's `npm run coverage` command lints every entry in `samples.json` against these rules and flags violations.

> **Framing note (supersedes the earlier TrustPager-tutorial framing).** This doc was originally written for the TrustPager tutorial channel: every title had to say "TrustPager" and close with a TrustPager CTA. That framing is now genericised to the owner's brand and any kind of video, per the YouTube Studio design doc Decision 9 (`docs/architecture/2026-07-05-youtube-studio-design.md`). The title-craft (the four patterns, the description shape, the length band, the outcome-led rule) is kept wholesale. What flips: the "must say TrustPager" hard-rule becomes "carry the owner's brand", the vendor CTA becomes the owner's own, and the vendor-name safeguard is kept in generic form (no unintended third-party names).

This doc is the single source of truth. The headline rules in [README.md](README.md) and [CLAUDE.md](CLAUDE.md) are about the on-thumbnail text (the big left-side line); this doc is about the YouTube title (the video name on the channel) and description (what shows under the video on the watch page).

> The two are not the same. The on-thumbnail headline is allowed to be punchy and stripped — "Forms That Auto-Fill Your CRM", "Quote a Job in Under a Minute". The YouTube title has to do search work and brand work — "How I Quote a Job in Under a Minute", "The Fastest Way to Follow Up After a Site Visit".

---

## Hard rules (surfaced by `npm run coverage` lint)

1. **Every title carries the owner's brand where it does search and brand work.** Lead with the owner's own name or the plain outcome, whichever reads more naturally. The owner's brand does the brand work; a competitor's name never appears where the owner's belongs.
2. **No unintended third-party vendor or product names.** A title should not accidentally promote a competitor or a tool the owner does not want front-and-centre. Prefer the plain word or the owner's own brand over a vendor's product name — `AI` rather than a specific model name, the owner's product name rather than a platform they merely run on. If the video genuinely IS about a named third-party tool, that is the owner's call to make deliberately.
3. **Title length: 4–14 words.** Shorter is better; under 7 is ideal. YouTube clips titles past ~70 characters on mobile.
4. **Title shape: action-led, viewer-as-beneficiary.** Same spirit as the on-thumbnail headline rules — see the title patterns below.
5. **Description closes with the owner's own call to action** (their site, their booking link, their offer), separated from the body by a blank line. Read it from the root `brand/brand.json` or ask the owner; never hard-code a vendor's URL.

---

## Title patterns

Use one of these. They cover ~95% of cases. The examples show a service business (a tradie) as the owner; swap in the owner's own brand and outcomes.

### Pattern A — How-to / walkthrough: `How to <Verb> <Object>`

The default. Leads with the outcome the viewer gets. Examples:

- `How to Quote a Job Without a Site Visit`
- `How I Follow Up After Every Quote Automatically`
- `How to Price a Job So You Never Lose Money`

### Pattern B — First-person result: `How I <Verb> <Object> in <Time>`

For videos where the owner shows their own way of doing something. The personal angle earns trust. Examples:

- `How I Quote a Job in Under a Minute`
- `How I Book Two Extra Jobs a Week`
- `How I Keep Every Lead From Slipping`

### Pattern C — Outcome / promise: `The <Adjective> Way to <Verb> <Object>`

For videos that lead with a bold, specific promise. Examples:

- `The Fastest Way to Follow Up After a Site Visit`
- `The Simple System That Keeps My Diary Full`

### Pattern D — Story / behind-the-scenes: `What <Happened> When <Trigger>`

For videos about a moment or a change, not a feature. Examples:

- `What Changed When I Started Quoting on the Spot`
- `Why I Stopped Chasing Invoices by Hand`

---

## Description template

Three paragraphs, separated by blank lines:

```
<HOOK — 1 sentence. The outcome the video delivers. Specific, not vague.>

<BODY — 2-3 sentences. What the viewer will be able to do, in the owner's own words. Name the owner's own brand and offer; never a third-party vendor name the owner does not want promoted.>

<CTA — the owner's own call to action: their site, their booking link, or their offer.>
```

### Body rules

- **Talk to the viewer's outcome, not the mechanics.** "Quote a job while you're still standing in the driveway" beats "Use the mobile quoting form with saved line items".
- **Name the value, name what it replaces.** "without driving back to the office or waiting till Sunday night" — concrete.
- **Use the owner's own brand and offer.** Read the brand name and CTA from the root `brand/brand.json`, or ask the owner. Never insert a vendor's product name where the owner's belongs.
- **Lean on what makes the owner different.** Whatever the owner's real edge is (speed, local knowledge, a guarantee), lean on that.
- **Don't oversell.** A concrete, believable promise earns the click; a wild claim makes viewers bounce.

### Worked examples

**Title:** `How I Quote a Job in Under a Minute`

```
Win more work by getting the quote in your customer's hands before you've left the driveway. In this video I show the exact way I price and send a quote on the spot, so the job is booked before a competitor even calls back.

Book a free chat: https://your-brand.example
```

**Title:** `How I Follow Up After Every Quote Automatically`

```
Turn more quotes into booked jobs without lifting a finger. I walk through the simple follow-up I set up once, so every customer hears back at the right moment and nobody slips through the cracks.

Book a free chat: https://your-brand.example
```

*(The CTA above is a placeholder — swap in the owner's real link.)*

---

## Avoid naming a vendor where the owner's brand belongs

Prefer the plain word, or the owner's own brand, over a vendor's product name. This keeps the owner's channel about the owner, not about a tool they merely run on.

| Instead of naming | Prefer |
|---|---|
| A specific AI model (`Claude`, `ChatGPT`, `Anthropic`, `OpenAI`) | `AI` |
| The plumbing behind a feature (a specific email / SMS / voice / payments / storage vendor) | The owner's own brand for that feature, or the plain word (`email`, `text`, `calls`, `payments`) |
| `Drag-and-drop builder` (in titles) | `Builder` or skip entirely |

If a video genuinely IS about a named third-party tool, that is the owner's deliberate call. The safeguard is against a vendor name slipping in *unintentionally* where the owner's brand should be.

Internal code, file paths, function names, and JSDoc are exempt — they're for developers, not viewers.

---

## How to add a new title + description

The thumbnail studio's interactive add picks these up automatically:

```bash
cd thumbnails
npm run make    # prompts for title + description (validates against this doc)
```

After answering, `npm run coverage` will lint your new entry. The lint check is the final gate.

When you're happy with the entry:

```bash
npm run shoot <key>      # render the thumbnail PNG
npm run publish <key>    # upload to the owner's workspace Images folder (optional, when connected)
```

The PNG output filename is `${order} - ${title}.png` — designed to drag-drop onto YouTube without renaming. The `description` field in `samples.json` is what you paste into YouTube's description box manually.

---

## Lint rules surfaced by `npm run coverage`

`npm run coverage` runs these checks at the end of its report:

| Check | What it flags |
|---|---|
| `[WARN] Banned vendor name` | Title contains one of the vendor names in the avoid list above |
| `[WARN] Title too long` | Title has more than 14 words |
| `[WARN] Title too short` | Title has fewer than 4 words |
| `[WARN] No description` | Entry has a title but no description |

All lint output is **non-blocking WARN** — you can ship a thumbnail with a warning; the coverage command exits non-zero ONLY on orphan thumbnails (a broken linked state). Warnings exist so a rough title does not get forgotten.

> **How the two lint defaults resolve (genericised).** The `coverage.js` and `make.js` scripts read the owner's brand from `brand/brand.json`. The title check requires the owner's brand NAME to appear in the title, and the description check requires the description to end with the owner's CTA. Both are WARN-only and never block a render. When `brand.json` carries no brand name yet (the neutral "Your Business" starter) the brand-name warning is skipped; when it carries no CTA, the CTA warning is skipped and `make.js` appends nothing (it never injects a vendor URL). Set your brand with `/brand-my-workspace` (name, and optionally a `cta` / `url`) and both checks switch to yours automatically.

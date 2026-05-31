# YouTube Titles & Descriptions — TrustPager Tutorial Channel

The system for writing titles and descriptions that ship with every tutorial video. The thumbnail studio's `npm run coverage` command lints every entry in `samples.json` against these rules and fails the build on violations.

This doc is the single source of truth. The headline rules in [README.md](README.md) and [CLAUDE.md](CLAUDE.md) are about the on-thumbnail text (the big left-side line); this doc is about the YouTube title (the video name on the channel) and description (what shows under the video on the watch page).

> The two are not the same. The on-thumbnail headline is allowed to be punchy and stripped — "Forms That Auto-Fill Your CRM", "Broadcast Without Leaving the CRM". The YouTube title has to do search work and brand work — "How to Build & Send Forms in TrustPager", "How to Run Email Marketing in TrustPager".

---

## Hard rules (must pass `npm run coverage` lint)

1. **Every title must contain the word "TrustPager".** No exceptions. The product name does brand work and search work. Variants like "TrustPager CRM" are fine.
2. **No third-party vendor or product names.** Specifically banned in YouTube titles: `Claude`, `Retell`, `Twilio`, `Postmark`, `Resend`, `Stripe`, `Anthropic`, `OpenAI`, `Cloudflare`, `Recall`, `Recall.ai`. Use the TrustPager-branded language instead — `AI` for any Anthropic/OpenAI work, `TrustPager Voice` for Twilio/Retell, `TrustPager Mail` for Postmark, `TrustPager Notetaker` for Recall. Extends [the platform-wide rule 21](https://docs.trustpager.com).
3. **Title length: 4–14 words.** Shorter is better; under 7 is ideal. YouTube clips titles past ~70 characters on mobile.
4. **Title shape: action-led, viewer-as-beneficiary.** Same spirit as the on-thumbnail headline rules — see the title patterns below.
5. **Description must close with the CTA line, verbatim:**
   ```
   Try TrustPager free: https://trustpager.com
   ```
   Separated from the body by a blank line.

---

## Title patterns

Use one of these. They cover ~95% of cases.

### Pattern A — Feature tutorial: `How to <Verb> <Object> in TrustPager`

The default. Maps to almost every help-center article. Examples:

- `How to Build & Send Forms in TrustPager`
- `How to Manage Your Sales Pipeline in TrustPager`
- `How to Send SMS Messages in TrustPager`
- `How to Use CRM Templates in TrustPager`
- `How to Set Up Event Queues in TrustPager`
- `How to Run Email Marketing in TrustPager`

### Pattern B — AI capability: `Use AI to <Verb> Your TrustPager <Object>`

For features where the value prop IS "AI does it for you" and the AI angle should lead. Examples:

- `Use AI to Build Your TrustPager Automations`
- `Use AI to Fill Your TrustPager Opportunities`  *(more brandful than "How to Auto-Fill...")*
- `Use AI to Run Needs Analysis in TrustPager`  *(more brandful than "How to Run AI Needs Analysis...")*

### Pattern C — Cross-system integration: `How to <Verb> <External Thing> with TrustPager CRM`

For tutorials that integrate an external system. The external thing comes first (helps search), TrustPager closes. Examples:

- `How to Sync Google Calendar with TrustPager CRM`
- `How to Connect Your Inbox to TrustPager CRM`  *(hypothetical)*

### Pattern D — Event/trigger tutorial: `How to <Verb> When <Trigger> in TrustPager`

For tutorials about a behaviour, not a feature. Examples:

- `How to Send Automatic Emails When a Deal Changes Stage in TrustPager`
- `How to Move a Deal When a Form Is Submitted in TrustPager`  *(hypothetical)*

---

## Description template

Three paragraphs, separated by blank lines:

```
<HOOK — 1 sentence. The pain it kills or the outcome it delivers. Specific, not vague.>

<BODY — 2-3 sentences. How TrustPager does it, what gets tracked / fed back. Always name "TrustPager" by feature ("TrustPager email marketing", "TrustPager email", "TrustPager Voice"). No third-party vendor names.>

Try TrustPager free: https://trustpager.com
```

### Body rules

- **Talk to the viewer's outcome, not the mechanics.** "Send campaigns to the right people without exporting lists" beats "Use the campaign builder with audience filters".
- **Name the value, name what it replaces.** "without exporting lists or paying for a second tool" — concrete.
- **Use TrustPager-branded feature names.** `TrustPager email marketing`, `TrustPager Voice agents`, `TrustPager Mail`, `TrustPager Notetaker`. Never `Postmark`, `Twilio`, `Recall`, `Retell`.
- **Talk about CRM integration as the differentiator.** TrustPager's edge is "every send/call/touch feeds back into the contact record + pipeline". Lean on that.
- **Don't oversell.** "AI builds the automation" is fine; "AI does everything for you" is bullshit and viewers bounce.

### Worked examples

**Title:** `How to Run Email Marketing in TrustPager`

```
Send campaigns to the right people without exporting lists or paying for a second tool. TrustPager email marketing pulls audiences straight from your CRM, sends from your domain, and tracks opens, clicks, and replies against the contact record — so every send feeds back into your pipeline.

Try TrustPager free: https://trustpager.com
```

**Title:** `Use AI to Build Your TrustPager Automations`

```
Skip the drag-and-drop. Describe the workflow you want — "when a deal moves to Won, send the welcome email and create an onboarding task" — and AI builds the automation inside TrustPager for you. Triggers, actions, conditions, all wired up from a sentence.

Try TrustPager free: https://trustpager.com
```

---

## Banned words and phrases

| Don't say | Use instead |
|---|---|
| `Claude` | `AI` |
| `Anthropic` | `AI` |
| `OpenAI` / `ChatGPT` | `AI` |
| `Retell` | `TrustPager Voice` / `TrustPager voice agents` |
| `Twilio` | `TrustPager Voice` (calls) / `TrustPager SMS` (texts) |
| `Postmark` / `Resend` / `Sendgrid` | `TrustPager Mail` / `TrustPager email` |
| `Recall.ai` / `Recall` | `TrustPager Notetaker` |
| `Stripe` | `TrustPager billing` |
| `Cloudflare` / `R2` | `TrustPager file storage` |
| `Drag-and-drop builder` (in titles) | `Builder` or skip entirely (Pattern B handles this) |

Internal code, file paths, function names, and JSDoc are exempt from these rules — they're for developers, not customers (rule 21 in the parent CLAUDE.md).

---

## How to add a new title + description

The thumbnail studio's interactive add picks these up automatically:

```bash
cd thumbnails
npm run make    # prompts for title + description (validates against this doc)
```

After answering, `npm run coverage` will lint your new entry. The lint check is the final gate.

When the lint check passes:

```bash
npm run shoot <key>      # render the thumbnail PNG
npm run publish <key>    # upload to FinalPiece > Tutorial Thumbnails
```

The PNG output filename is `${order} - ${title}.png` — designed to drag-drop onto YouTube without renaming. The `description` field in `samples.json` is what you paste into YouTube's description box manually.

---

## Lint rules currently enforced

`npm run coverage` runs these checks at the end of its report:

| Check | What it flags |
|---|---|
| `[WARN] Missing TrustPager` | Title does not contain "TrustPager" |
| `[WARN] Banned vendor name` | Title contains one of the words in the banned list |
| `[WARN] Title too long` | Title has more than 14 words |
| `[WARN] Title too short` | Title has fewer than 4 words |
| `[WARN] Missing CTA line` | Description doesn't end with `Try TrustPager free: https://trustpager.com` |
| `[WARN] No description` | Entry has a title but no description |

The coverage command exits non-zero ONLY on orphan thumbnails (broken state). Lint warnings are surfaced but non-blocking — you can ship a thumbnail with a warning. The warning is there so it doesn't get forgotten.

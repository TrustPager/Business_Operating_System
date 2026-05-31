# YouTube Thumbnail Method — distilled from 22+ design iterations

The canonical knowledge for designing tutorial-video thumbnails using the
bundled studio at `studio/thumbnails/`. This is the operator-facing
summary; the full rules live inline in the studio's three source files
(deliberately co-located with the code they describe so corrections
don't drift):

- [`studio/thumbnails/YOUTUBE_TITLES.md`](../studio/thumbnails/YOUTUBE_TITLES.md)
  — YouTube title patterns + lint rules
- [`studio/thumbnails/src/templates/YouTubeThumbnail.jsx`](../studio/thumbnails/src/templates/YouTubeThumbnail.jsx)
  (JSDoc lines 1-250) — Canonical layout, brand palette, headline writing
  guide, common mistakes
- [`studio/thumbnails/src/templates/heroes/index.js`](../studio/thumbnails/src/templates/heroes/index.js)
  (header comment) — Hero family patterns, anti-patterns

When in doubt, the inline rules win. This file is the executive summary.

---

## Title vs headline — don't confuse them

The **title** appears on the YouTube channel: *"How to Build & Send Forms
in TrustPager"*. Job = search.

The **headline** is the big left-side text ON the thumbnail itself:
*"Forms That Auto-Fill Your CRM"*. Job = punch.

They serve different jobs and have different rules.

---

## Title rules (4 patterns)

All titles are 4-7 words, present-tense active verb, lead with the
outcome the viewer gets — NOT what the AI does.

**Pattern A — "How to <verb> <noun>"**
- ✅ How to Build & Send Forms in TrustPager
- ✅ How to Manage Tasks in TrustPager

**Pattern B — "<verb> <noun> with AI"**
- ✅ Auto-Fill Opportunity Fields with AI
- ✅ Build a Leads Pipeline with Claude

**Pattern C — "<outcome statement>"**
- ✅ See Exactly Where to Improve Your Business
- ✅ Use AI to Build Your TrustPager Automations

**Pattern D — "<verb> Your <noun>"** (for foundational features)
- ✅ Run Your Whole Business in TrustPager
- ✅ Sync Google Calendar with TrustPager CRM

All four MUST include "TrustPager" verbatim (it's both the brand and a
search keyword) — except short titles where the channel name already
carries it.

---

## Headline rules

**Lead with the viewer's outcome, not the feature's action.**
- ✅ *"Forms That Auto-Fill Your CRM"* — viewer is the beneficiary
- ❌ *"AI Reads Your Notes, Fills the Deal"* — AI is the subject; viewer is a bystander

**One accent word in the headline.** Picks up the brand gradient fill
(teal → mint → blue). Same word appears VERBATIM in the title for SEO
consistency.

**Specific outcomes beat airy abstractions.**
- ✅ *"See Exactly Where to Improve Your Business"*
- ❌ *"See Where Money Is Made"*

**Active and instructive beats passive vibes.**
- ✅ *"Make Sure Nothing Falls Through the Cracks"* — you act
- ❌ *"Nothing Falls Through the Cracks"* — just a vibe

**Snappier is almost always better.**
- ✅ *"Automate Everything"*
- ❌ *"Save Hours Every Week on Autopilot"*

**Cut the leading verb when the noun already carries the action.**

| Verbose | Trimmed |
|---|---|
| Build Forms That Auto-Fill Your CRM | Forms That Auto-Fill Your CRM |
| Create Detailed Notepads for Every Deal | Detailed Notepads for Every Deal |
| Ensure Your AI Asks Before It Acts | Your AI Asks Before It Acts |

---

## Banned framings

These all came from real corrections. Don't re-walk them.

- **Surveillance-flavoured** — "Track Every Promise You Make" implies
  you'll fail one. Use "Watch Your AI Team Work Live" — observation,
  not paranoia.
- **Negative "Stop X"** — "Stop Typing the Same Email Twice" implies
  the viewer is doing something wrong. Use "Never Type the Same Email
  Twice" — positive command.
- **Vague accusations** — "Know What Your AI Did Today" sounds like
  you're auditing it. Use "Watch Your AI Team Work Live" or "Your AI
  Asks Before It Acts".
- **Third-party vendor names** — "ChatGPT", "Anthropic", "Recall",
  "Twilio". TrustPager-branded language only on customer-facing
  surfaces; vendor names allowed in internal code only.
- **"AI replaces your sales team"** — the audience recoils. Use "AI
  does the secretary work, you keep the relationship."

---

## The 6 hero families

The right side of every thumbnail is a "hero" — a stylised product UI
that shows the outcome (not the configurator). Six standard shapes:

1. **Card stack** — pipeline cards stacked. Use for pipeline / opps.
2. **Event row** — calendar / scheduling rows. Use for time-based features.
3. **Field stack** — labelled form fields. Use for forms / data entry / fill-with-AI.
4. **Roster** — list of avatars + names. Use for contacts / team / users.
5. **Checklist** — checked items. Use for tasks / approvals.
6. **Document** — invoice / proposal preview. Use for documents / e-signing / reporting.
7. **Flow** — connected nodes (automations). Use for automation / triggers.

The hero **bleeds off the bottom edge** so the design feels alive, not
boxed-in. The headline lives left, hero lives right, brand wordmark
top-left, accent strip bottom.

---

## Common mistakes (already corrected once — don't re-walk)

| Mistake | Fix |
|---|---|
| Hero looks like a configurator (settings, dropdowns, "Save" buttons) | Hero shows the OUTCOME — a deal that closed, a form that filled itself, a task that got done |
| Accent word doesn't appear in the title | Mirror it verbatim. "Auto-Fill" headline + "Auto-Fill" in the title |
| Title is 8+ words | Cut. 4-7 is the band |
| Hero is centred (not bleeding off edge) | Push it down + right until it kisses the bottom edge |
| No "TrustPager" in the title | Add it (or shorter form "TrustPager CRM"). Search depends on it |
| AI mentioned as the subject ("AI does X") | Reframe — viewer is subject, AI is the engine |
| Verb-noun where the noun already does the verb ("Build Forms That ...") | Drop the verb — "Forms That ..." |
| Surveillance / paranoia framing | Reframe as empowerment / observation |
| Cliché outcomes ("See Where Money Is Made") | Specific concrete benefit instead |
| Hero is too detailed to read at thumbnail-scale | Strip — 4-6 elements max, big enough to scan in 200ms |

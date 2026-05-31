# Thumbnails Studio — Instructions for AI Assistants

You're working in the TrustPager YouTube Thumbnail Studio. Before doing anything in this directory, follow the protocol below.

---

## 1. Read the rules FIRST (non-negotiable)

Three files hold the rules. Read them end-to-end before changing `samples.json`, before rendering, before answering "how do I…":

1. **[`YOUTUBE_TITLES.md`](YOUTUBE_TITLES.md)** — YouTube title patterns + description template + hard rules (TrustPager always, no third-party vendor names). Read FIRST when adding a new tutorial.
2. **[`README.md`](README.md)** — the human-readable guide. On-thumbnail headline rules, hero UI rules, file layout, workflow.
3. **[`src/templates/YouTubeThumbnail.jsx`](src/templates/YouTubeThumbnail.jsx)** — JSDoc header at the top (~200 lines). Mirrors the README rules in compact form so you encounter them when touching the canonical template.

If you skip these you'll reintroduce things we've already corrected: titles that name third-party vendors (`Claude`, `Retell`, `Twilio`), titles without `TrustPager`, weak headlines (`Build Forms That…` instead of `Forms That…`), banned colours (red / orange / purple in the hero chrome), generic activity lists where a topic-specific hero belongs, initial-letter avatars where real portraits exist, multi-column hero layouts that break the thin-vertical-bleed rule.

> **Title vs headline — these are different artefacts with different rules.** The on-thumbnail **headline** is the big left-side text ("Forms That Auto-Fill Your CRM"). The **YouTube title** is the video's name on the channel ("How to Build & Send Forms in TrustPager"). Headline rules: README + JSDoc. Title rules: YOUTUBE_TITLES.md. Don't apply one rule set to the other.

---

## 2. The thumbnail anatomy

Every thumbnail is the same composition:

```
+----------------------------------------------------------+
| [TP Logo]                                +-------------+ |
|                                          | Hero card   | |
|   Headline With                          |  feature-   | |
|   One Gradient Word                      |  specific   | |
|                                          |  vertical   | |
|                                          |  stack…     | |
|   //// diagonal accent strip /////       |  bleeds…    | |
+----------------------------------------------------------+
                                           (continues off bottom)
```

- **Left side:** flat white, logo top-left, headline vertically centered, one accent word with the teal→mint→blue gradient. Headline has a soft white drop-shadow halo so it stays legible where it overlaps the hero.
- **Right side:** a single tall white card (the **hero**) that mimics the actual product surface for that video. Bleeds off the bottom edge.
- **Behind the hero:** soft teal/mint/blue colour blooms, masked so they don't reach the left side.
- **Across the bottom:** a thin diagonal teal→blue accent line.

Spatial constants live in `SYS` at the top of `YouTubeThumbnail.jsx`. Change them there — never hard-code positions inline.

---

## 3. The 4 questions to ask before making a new thumbnail

When the user says "make a thumbnail for X", gather these BEFORE editing `samples.json`:

1. **What's the tutorial's core promise?** One sentence — the outcome the viewer gets.
2. **Which headline angle?** Show 3–5 options across angles. 4–7 words, one accent word. "AI" not "Claude". Cut leading verbs (`Build`, `Create`, `Ensure`, `Make Sure`) when the noun already implies the action. Steal punchy idioms (`Level Up`, `One Place`, `Inside Out`). Banned openings: `Let`, `How to`, `Just`, `Stop X-ing`, `Tips for`.
3. **Which word gets the gradient accent?** Usually the verb or the noun being transformed. Can be a two-word phrase (e.g. `One Place`, `Level Up`) — the regex handles spaces inside `\b...\b`.
4. **Which hero matches this topic?** Find the iconic product surface the video walks through (open the corresponding `Tutorial<X>Page.tsx` in your tutorials folder). Then either:
   - **Reuse an existing hero** from [`src/templates/heroes/`](src/templates/heroes/) if one already fits, or
   - **Build a new one** following [`heroes/index.js`](src/templates/heroes/index.js) — single outer container, thin/tall/vertical stack, bleeds off the bottom, brand colours only.

---

## 4. Commands

```bash
npm run dev                  # studio at http://localhost:3210 — live reload
npm run make                 # interactive: prompt for key + headline + accent + composition
npm run shoot <key>          # render one PNG + auto-open (iteration loop)
npm run shoot                # render all designs in samples.json
npm run shoot -- --no-open   # render without auto-opening
npm run publish <key>        # render + upload to FinalPiece > Tutorial Thumbnails
npm run publish -- --all     # publish every design
npm run coverage             # check which Remotion comps are missing thumbnails
```

### Composition linking (mandatory)

Every thumbnail entry MUST carry a top-level `composition` field naming the Remotion comp it belongs to. If you skip it:

- `npm run coverage` flags the entry as broken
- The studio sidebar shows ⚠ no composition linked in orange
- The thumbnail is impossible to find from the Remotion side

Look up comp ids in [`COMPOSITION_MAP.md`](COMPOSITION_MAP.md) (auto-generated) or by grepping `src/compositions/` for `<Composition id="...">`. When asked "is there a thumbnail for this video?" or the inverse, **run `npm run coverage` first** — never grep around blindly.

**Rule:** `shoot` is for iteration, `publish` is finalize. Don't publish until the user has approved the rendered PNG. Always **read the PNG** before declaring a render done — the studio preview can differ from puppeteer's output.

---

## 5. Each samples.json entry

```json
{
  "<key>": {
    "template":    "youtube-thumbnail",
    "composition": "Tutorial-FormBuilder",
    "data": {
      "headline":   "Forms That Auto-Fill Your CRM",
      "accentWord": "Auto-Fill",
      "hero":       "forms",
      "title":      "How to Build & Send Forms in TrustPager"
    }
  }
}
```

| Field | Purpose |
|---|---|
| `composition` | **Mandatory.** Remotion comp id (e.g. `Tutorial-FormBuilder`). Lets `npm run coverage` show what's linked vs missing in both directions. |
| `headline`    | The big left-side text. 4–7 words, contains the `accentWord` verbatim. |
| `accentWord`  | The one word (or two-word phrase) that gets the gradient fill. Matches case-insensitively. |
| `hero`        | Key into [`src/templates/heroes/index.js`](src/templates/heroes/index.js). Drives which hero component renders on the right. |
| `title`       | The actual YouTube video title. Used as the output PNG filename so it drag-drops onto YouTube without renaming. |

The short `<key>` is what drives the studio sidebar and click-to-copy command chips (`npm run shoot forms`). The `title` is what ends up on disk and in TrustPager's Tutorial Thumbnails folder.

---

## 6. The avatar system

Two pools of real avatar images. **Always prefer real images over initial-letter coloured divs.** Initials at thumbnail scale look like generic chips; real portraits read as humans.

### People avatars — [`src/profiles.jsx`](src/profiles.jsx)

Five real portraits from the FinalPiece CDN, name-hashed for stability (same name → same face every time).

```jsx
import { Avatar } from '../../profiles.jsx';

<Avatar name="Saskia Williams" size={32} />
```

### Agent avatars — `public/agents/<Name>.png`

Eight AI-agent portraits ship under `public/agents/`: Aria, Marty, Mira, Lyra, Orion, Sable, Echo, Custom. Reference them directly:

```jsx
<img src="/agents/Aria.png" alt="Aria" style={{ width: 46, height: 46, borderRadius: '50%' }} />
```

Brand-rule note: keep the surrounding chrome (status pills, role tags, capability badges) on the TrustPager palette (teal / green / blue / light teal / slate) even though the FinalPiece site brands each agent with purple / orange / red.

---

## 7. Common mistakes to avoid (lessons learned)

- **DON'T use red / orange / purple / coral in hero chrome.** Brand palette only: `#29c6c6` teal, `#2db87d` green, `#47a3d9` blue, `#7dd3d3` light teal, `#1ea5a5` deep teal, `#94a3b8` slate. Real product UI uses orange/purple in places — remap them.
- **DON'T put halos on the left side.** The left is pure flat white. The halo mask fades out before reaching the text area.
- **DON'T wrap the logo or headline in a card.** They sit directly on the flat white surface. Left edges align pixel-perfectly.
- **DON'T use italic serif on the accent word.** Same weight + family as the rest of the headline, just with the gradient fill.
- **DON'T try to add a browser-side "Download PNG" button.** Libraries like html2canvas misrender `background-clip: text` and the gradient breaks. `npm run shoot` (puppeteer + real Chrome) is the canonical export.
- **DON'T render generic AI Activity items when the video has a specific product surface.** The "AI Activity card" form factor was right (thin / vertical / stacks / bleeds), but its content (text rows) fails the squint test for every topic. Build a topic-specific hero.
- **DON'T break the thin-vertical-bleed rule.** No horizontal subdivisions inside the hero. No side-by-side columns. No 2-up grids. One vertical stream of items that bleeds off the bottom.
- **DON'T give inner panels their own heavy shadows.** The heavy shadow lives on the outer hero container only. Inner panels use a single `1px solid rgba(226,232,240,0.7)` border.
- **DON'T use initial-letter avatars when real portraits exist.** Use `<Avatar name="..." />` (people) or `/agents/<Name>.png` (AI agents).
- **DON'T pick names for the accent word like "Lock Down What Each Person Sees".** Cut to the snappiest version that still names the outcome.
- **DON'T offer 5 design options when the user wants ONE design iterated.** Confirm: "5 headline options" (different copy) vs "5 layout variants" (same copy, different layouts).
- **DON'T declare a render done without reading the PNG.** The studio preview can differ from puppeteer output. Use the Read tool on `output/<title>.png`.

---

## 8. File map

```
thumbnails/
├── CLAUDE.md                            ← this file
├── README.md                            ← full design guide + rules
├── YOUTUBE_TITLES.md                    ← title patterns + description template + lint rules
├── COMPOSITION_MAP.md                   ← auto-generated thumbnail ↔ comp mapping
├── package.json                         ← npm scripts (dev / make / shoot / publish / coverage)
├── vite.config.js                       ← dev server on port 3210
├── src/
│   ├── main.jsx                         ← React entry
│   ├── App.jsx                          ← studio UI (sidebar + preview)
│   ├── theme.js                         ← colour tokens + dimensions
│   ├── profiles.jsx                     ← people avatars (<Avatar name="..." />)
│   ├── templates/
│   │   ├── YouTubeThumbnail.jsx         ← canonical layout + JSDoc rules + SYS constants
│   │   ├── index.js                     ← template registry
│   │   └── heroes/                      ← per-topic hero components
│   │       ├── index.js                 ← hero registry (key → component)
│   │       ├── AIActivityHero.jsx       ← legacy fallback
│   │       ├── PipelineHero.jsx         ← (and 21 more)
│   │       └── …
│   └── data/
│       └── samples.json                 ← all 22 thumbnails — edit to add new
├── scripts/
│   ├── make.js                          ← npm run make
│   ├── shoot.js                         ← npm run shoot
│   ├── publish.js                       ← npm run publish
│   ├── render.js                        ← puppeteer renderer (shared by shoot + publish)
│   └── coverage.js                      ← npm run coverage
├── public/
│   ├── trustpager-logo.png              ← brand wordmark
│   └── agents/                          ← AI agent portraits (Aria, Marty, …)
└── output/                              ← rendered PNGs, named by YouTube title (gitignored)
```

---

## 9. Behaviour expected of you

- Read the rules (README + JSDoc) before suggesting changes.
- Ask the 4 questions before generating a new thumbnail.
- Verify your renders by reading the PNG.
- Use real avatars, not initials, where people are involved.
- Stay on the brand palette in hero chrome.
- Never break the thin-vertical-single-stack-bleeds rule.
- If you hit something not covered by the rules, ask the user before guessing.

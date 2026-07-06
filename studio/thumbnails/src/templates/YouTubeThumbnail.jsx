// ============================================================================
// YouTubeThumbnail - 1280x720 (16:9) thumbnail for the owner's videos.
// Canonical template. Edit ../data/samples.json to add new thumbnails;
// edit SYS below to tune the design system.
//
// FRAMING NOTE (supersedes the earlier TrustPager-tutorial framing): this
// template was originally written for the TrustPager tutorial channel. It is
// now genericised to the owner's brand and any kind of video, per the YouTube
// Studio design doc Decision 9. Brand colours and the wordmark flow through
// ../brand.js (which reads the root brand/brand.json), so every render is on
// the owner's palette. The distilled craft below (headline rules, squint test,
// hero master rule) is kept wholesale; only brand-specific framing flips.
// ============================================================================
//
// LAYOUT GRID (canvas is 1280 x 720, all measurements in CSS pixels)
// -----------------------------------------------------------------
//
//   +-------------------------------------------------+
//   | margin                                          |
//   |  [TP Logo]                +-------------------+ |
//   |                           | AI Activity       | |
//   |                           |  o Item 1         | |
//   |   Get AI to               |  o Item 2         | |
//   |   Build Your              |  o ...            | |
//   |   Business                |  - Updating (NOW) | |
//   |   ^^^^^                   |  o Pending 1      | |
//   |   (accent: teal gradient) |  o Pending 2      | |
//   |                           +-------------------+ |
//   |   //// diagonal accent ///......(card bleeds)   |
//   | margin                                          |
//   +-------------------------------------------------+
//
// Symmetric 28px margins on all four sides. The AI Activity hero card is
// taller than the canvas allows - the bottom bleeds off the page (clipped
// by overflow:hidden).
//
// EVERY edge measurement comes from SYS below. Change one number and the
// whole composition follows; never hard-code positions inline.
//
// Layer order (back to front, by z-index):
//   1. Canvas background     - pure flat #ffffff. Left side stays clean.
//   2. ColorHalo (z=3)       - teal+blue+mint blooms behind the hero ONLY.
//                              Mask fades them out before the left text area.
//   3. AccentStrip (z=2)     - thin diagonal teal->blue line across the bottom.
//                              Cuts behind the AI Activity card.
//   4. AIActivityHero (z=4)  - the right-side hero. Bleeds off bottom.
//   5. LogoCard (z=9)        - the owner's brand wordmark, bare img at top-left.
//   6. GlassCard (z=8)       - the headline text, vertically centered, left.
//
//
// COLOR PALETTE - the owner's brand only (from brand/brand.json). NEVER deviate.
// -----------------------------------------------------------------------------
//
//   The hex values below are the studio's default palette. When the owner has
//   run /brand-my-workspace, ../brand.js resolves these to their brand.json
//   colours instead. The DISCIPLINE is what matters: stay on the brand palette,
//   never introduce off-brand red / orange / purple in the hero chrome.
//
//   ALLOWED (default palette):
//     #29c6c6  primary teal       (main brand color)
//     #2db87d  secondary green    (used for completed/success states)
//     #47a3d9  accent blue        (used for in-progress and accents)
//     #7dd3d3  light teal         (used for tertiary slices, pills)
//     #5ed4d4  mid mint           (gradient stop)
//     #1ea5a5  deep teal          (gradient stop)
//     #2e7fb0  deep blue          (gradient stop)
//     #94a3b8  neutral slate      (used for INACTIVE states - not red!)
//     #020817  foreground text
//     #ffffff  white canvas
//
//   BANNED (do not introduce, ever):
//     red (#ef4444)     - not on brand. Use slate for "lost"/"inactive".
//     orange (#f59e0b)  - not on brand. Use teal for in-progress.
//     purple (#9b7dff)  - not on brand. Use light teal as third color.
//     coral / peach / magenta - not on brand.
//     pure white text on coloured bg - check contrast, prefer #020817 on white.
//
//
// HEADLINE WRITING GUIDE
// ----------------------
//
//   Format: 4-7 words. One ACCENT word that appears verbatim in the headline
//   and receives the gradient fill. Present-tense active verb. "AI" not
//   "Claude" (wider audience).
//
//   THE CORE RULE — outcome the viewer gets, not what the feature does.
//     The viewer is the beneficiary; the AI is the tool.
//     GOOD: "Get AI to Fill Your CRM for You"        (viewer is subject)
//     BAD:  "AI Reads Your Notes, Fills the Deal"    (AI is subject)
//
//   SPECIFIC outcomes beat airy abstractions. If the outcome could just as
//   easily describe a brochure, it's too soft.
//     GOOD: "See Exactly Where to Improve Your Business"
//     BAD:  "See Where Money Is Made"               (cliche)
//     GOOD: "AI Builds Proposals for You"           (specific verb)
//     BAD:  "AI Analyzes Your Deals in Seconds"     (vague verb)
//
//   NEVER use scary, surveillance-flavoured, or accusatory framing.
//   Empowerment, not paranoia.
//     BAD:  "Track Every Promise You Make"          (creepy)
//     BAD:  "Know What Your AI Did Today"           (accusation tone)
//     GOOD: "Watch Your AI Team Work Live"
//     GOOD: "Ensure Your AI Asks Before It Acts"
//
//   ACTIVE and instructive beats passive and declarative.
//     GOOD: "Make Sure Nothing Falls Through the Cracks"
//     BAD:  "Nothing Falls Through the Cracks"      (just a vibe)
//     GOOD: "Never Type the Same Email Twice"       (positive command)
//     BAD:  "Stop Typing the Same Email Twice"      ("stop" = guilt framing)
//
//   SNAPPIER is almost always better. Cut anything not load-bearing.
//     GOOD: "Lock Down Your Data"
//     BAD:  "Lock Down What Each Person Sees"
//     GOOD: "Automate Everything"
//     BAD:  "Save Hours Every Week on Autopilot"    (generic SaaS)
//
//   CUT THE LEADING VERB when the noun already carries the action. Trust
//   the noun. "Forms That Auto-Fill" implies you're building/using them -
//   the verb is dead weight. Same for guarantor verbs (Ensure / Make Sure)
//   - the statement IS the guarantee.
//     GOOD: "Forms That Auto-Fill Your CRM"   BAD: "Build Forms That Auto-Fill..."
//     GOOD: "Detailed Notepads for Every Deal" BAD: "Create Detailed Notepads..."
//     GOOD: "Emails That Send Themselves"     BAD: "Email Follow-ups That Send..."
//     GOOD: "Your AI Asks Before It Acts"     BAD: "Ensure Your AI Asks..."
//     GOOD: "Watch Your AI Team Work"         BAD: "Watch Your AI Team Work Live"
//     GOOD: "Sales and Service in One Place"  BAD: "Run Sales and Service in One Pipeline"
//
//   STEAL PUNCHY IDIOMS over literal descriptions. A common phrase the
//   audience already knows ("Level Up", "One Place", "Inside Out", "Click
//   of a Button", "Convert Forever") lands harder than a precise technical
//   description. The cultural shortcut does work for you.
//     GOOD: "See Where You Can Level Up"      BAD: "See Exactly Where to Improve Your Business"
//     GOOD: "Know Every Client Inside Out"    BAD: "Recall Every Detail About Every Client"
//     GOOD: "Manage Tasks with Ease"          BAD: "Make Sure Nothing Falls Through the Cracks"
//
//   DRAMA and specificity create hooks. Words like Forever, Live, Auto-Fill,
//   Click of a Button, Right From the CRM give the title an edge.
//     GOOD: "Drip Campaigns That Convert Forever"
//     GOOD: "Close Deals at the Click of a Button"
//     GOOD: "Send Email Right From the CRM"
//     GOOD: "Build Forms That Auto-Fill Your CRM"
//
//   ACCURACY — the title must accurately describe the video. Don't promise
//   something the video doesn't deliver. Viewers bounce in 5 seconds and the
//   algorithm punishes you.
//
//   BANNED openings: "Let", "How to", "Just", "Stop X-ing", "Tips for", "Way to".
//   STRONGER openings: "Get", "Watch", "Make", "Never", "Build", "Send",
//                      "Close", "Ensure", "Run", "Unify", "Your <noun>".
//
//
// HERO UI SELECTION
// -----------------
//
//   THE MASTER RULE: THIN, TALL, SINGLE VERTICAL STACK, BLEEDS OFF BOTTOM.
//
//   The hero is 528px wide x ~720+px tall - TALLER THAN WIDE. Content runs
//   off the bottom edge of the 1280x720 canvas. Every hero is a SINGLE
//   VERTICAL STREAM of feature-specific items - no horizontal subdivisions,
//   no side-by-side columns, no two-up grids inside the card. The bleed-off-
//   bottom tells viewers "this goes on forever - the feature has depth".
//
//   The original AI Activity card had the right FORM (thin / vertical /
//   stacked / bleeds). What we got wrong was the CONTENT (generic agent
//   text rows that fail at YouTube scale). Keep the form, swap the content.
//
//   SQUINT TEST (the deal-breaker). View the rendered PNG at 25% zoom. If
//   you can't tell what the video is about from shapes and colours alone -
//   no reading required - the hero fails. YouTube serves thumbnails at
//   ~480x270 desktop, 246x138 mobile. Text dissolves at that scale; only
//   shape, colour, and silhouette survive.
//
//   ICONIC SILHOUETTE PER TOPIC. Each feature has a recognisable vertical
//   shape. Stack items in that shape's language.
//
//     Scheduling           -> date headers + event blocks (time + name)
//     Service Request      -> completed-request cards (✓ Shipped + preview)
//     Google Calendar      -> upcoming-event rows (time + title + source)
//     Forms                -> field stack with one mid-auto-fill
//     Needs Analysis       -> AI-generated sections (Exec → Need → Pricing)
//     Notepads             -> notepad cards (folder + title + first line)
//     Permissions          -> role cards (name + scope count + shield)
//     Pipeline             -> deal cards under a single coloured stage header
//     Reports              -> chart cards stacked (donut → bars → trend)
//     SMS                  -> chat thread bubbles alternating left/right
//     Automations          -> action cards in a flow (Email → Task → SMS)
//     Tasks                -> checklist items (status + title + due)
//     Agent Hub            -> agent cards (avatar + status pulse + capabilities)
//     Approvals            -> approval cards (title + Approve/Reject row)
//     Stage emails         -> triggered-email log entries
//     Contacts             -> contact cards (avatar + name + employer + activity)
//     CRM Templates        -> template cards (subject + {{merge}} chips)
//     Proposals & Documents -> document-page silhouettes (cover → pricing → sig)
//     Send & Track Emails  -> inbox rows (sender + subject + tracked badge)
//     E-Signing            -> signed-contract cards (✓ stamp + signer + time)
//     Event Queues         -> timeline rows (Day 1 → Day 3 → Day 7)
//     Fill with AI         -> field rows mid-auto-fill with sparkle on active
//
//   OUTCOME, NOT CONFIGURATOR. Show the completed state, not the form/
//   wizard/builder. Stack of "form filled CRM" events, not the form builder.
//   Stack of "approved + sent" cards, not the pending queue. Stack of signed
//   contracts, not the signing config screen.
//
//   DENSITY OF SHAPE > DENSITY OF TEXT. Coloured shapes (status pills,
//   avatars, chart slices, stage badges, signature stamps) survive shrinking.
//   Text dissolves. Fewer items, bigger shapes, stronger colour contrast.
//
//   CARICATURE BEATS REALISM. If a faithful product render makes the hero
//   illegible at thumbnail scale, exaggerate. Bigger avatars. Bolder colours.
//   The hero is a MINIATURE, not a SCREENSHOT.
//
//   EVERY HERO NEEDS A COLOUR ANCHOR. 2-3 brand-coloured shapes (teal /
//   green / blue pills, headers, chart slices, status dots) that survive
//   at 25% zoom. A pure-white-card-with-text-only hero fails the squint test.
//
//   USE BRAND COLOURS ONLY. Real product UI uses orange / purple / red in
//   places. Heroes don't. Map to brand teal / blue / green / slate.
//
//   DON'T LEAD WITH A GATEKEEPING VIBE. Permissions hero: NOT a dense scope
//   matrix. Stack of role cards with shield icons + "Protecting N resources"
//   pills. Same topic, opposite feeling.
//
//
// AI ASSISTANT - QUESTIONS TO ASK BEFORE STARTING
// -----------------------------------------------
//
// When a user says "make a thumbnail for <topic>", gather these BEFORE
// touching samples.json or rendering:
//
//   1. What's the video's core promise? (one sentence)
//      Use this to drive headline brainstorming. Any kind of video works
//      here (a story, a tips video, a walkthrough), not tutorials alone.
//
//   2. Headline options - present 3-5 ANGLES (not 5 design variants of one
//      headline). Example angles:
//        - transformation:   "Get AI to Build Your Business"
//        - curiosity gap:    "What AI Did to My CRM"
//        - testimonial:      "I Haven't Touched My CRM in Weeks"
//        - contrarian:       "Stop Doing CRM Work"
//        - spectacle:        "Watch AI Close Your Deals"
//
//   3. Which word gets the gradient accent? Usually the strongest verb or
//      the noun being transformed. Show the user the rendered preview.
//
//   4. What 8-10 hero items show the video's topic? Mix of:
//        - 4-6 completed (past tense: Sent, Booked, Followed up, Generated)
//        - 1 in-progress (continuous: Updating, Drafting, Scoring)
//        - 2-4 pending   (future-tense or noun phrases: Queue, Open, Score)
//      Items must be CONCRETE, topic-flavoured actions, not vague tasks.
//      Use fictional but plausible names (Amir K., Sasha R., Jordan P., etc.).
//
//   5. Any colour palette changes needed? Default to NO - the brand palette
//      is locked. If the topic is genuinely off-brand (e.g. an integration
//      partner), check with the user before introducing new colors.
//
//
// COMMON MISTAKES TO AVOID
// ------------------------
//
//   - DON'T use red, orange, purple, or coral. They're not brand colors.
//     Use slate (#94a3b8) for inactive states. Never red.
//
//   - DON'T put halos on the left side. The left is pure flat white. Halos
//     bloom from the right side, fade out before they reach the text area.
//
//   - DON'T wrap the logo or headline in a card. They sit directly on the
//     flat white surface. Left edges align pixel-perfectly.
//
//   - DON'T use italic serif on the accent word. The accent treatment is a
//     pure gradient FILL, same weight and family as the rest of the headline.
//
//   - DON'T try to add a browser-side "Download PNG" button. JavaScript DOM
//     rasterisation libraries (html2canvas, dom-to-image, etc.) have CSS
//     feature gaps that misrender the gradient accent word, backdrop-filter,
//     and other modern effects. The canonical export is `npm run shoot`,
//     which uses puppeteer + real Chrome rendering. The studio shows a
//     click-to-copy chip with the exact command for the selected design.
//
//   - DON'T offer 5 "design options" when the user wants ONE design iterated.
//     Confirm what they're asking for before generating variants:
//       - "5 headline options" = different copy, same design
//       - "5 layout variants" = same copy, different layouts
//
//   - DON'T declare a render done without LOOKING at the rendered PNG. The
//     studio preview can differ from the PNG output (CSS support varies).
//     Always run `npm run shoot` and view the output before signing off.
//
//   - DON'T introduce subheadlines, eyebrows, or footer text. The composition
//     is logo + headline + hero + accent strip. Adding more makes it busy.
//
//
// EDITING WORKFLOW
// ----------------
//
//   1. Edit ../data/samples.json (or run `npm run make` for interactive prompt):
//
//        {
//          "thumbnail-key": {
//            "template": "youtube-thumbnail",
//            "data": {
//              "headline":   "Your 5-7 Word Headline",
//              "accentWord": "Word"
//            }
//          }
//        }
//
//   2. `npm run dev`            - live preview at http://localhost:3210
//   3. `npm run shoot <key>`    - export PNG locally + auto-open it (iteration)
//   4. `npm run publish <key>`  - render + upload to the owner's workspace
//                                  under Files > Images (optional, when
//                                  connected). This is the "finalize" step.
//   5. To change AI Activity items, edit the `items` array in AIActivityCard.
//   6. To change colors, layout, or sizing, edit the SYS constants block.
//
// ============================================================================

import React from 'react';
import { colors, fonts, THUMBNAIL_SIZE } from '../theme.js';
import { resolveHero } from './heroes/index.js';
import { ACCENT, GRADIENT, LIGHT, NAME, LOGO_URL, PANEL, PRIMARY, SLATE, SUCCESS } from '../brand.js';

// The owner's brand wordmark. brand.js resolves LOGO_URL to '/logo.png',
// which sync-brand.py keeps in step with brand/logo.png after every
// /brand-my-workspace run — so the thumbnail always carries the owner's logo.
const BRAND_LOGO = LOGO_URL;

// ============================================================
// DESIGN SYSTEM CONSTANTS
// ------------------------------------------------------------
// All spatial measurements derive from these. To shift the whole layout
// inward, just bump SYS.margin. To make the left column wider, change
// SYS.leftColWidth. Do NOT hard-code positions elsewhere.
// ============================================================
const SYS = {
  margin: 28,            // outer margin on all four canvas sides
  gap: 16,               // gap between adjacent cards (logo<->title, dashboard cards)
  leftColWidth: 680,     // width of the headline column on the left.
                          // Sized to accommodate the bigger headline below.
  heroWidth: 528,        // width of the right-side hero card (AI Activity).
                          // Derived: 1280 - margin - leftColWidth - gap - margin
                          //       = 1280 - 28 - 680 - 16 - 28 = 528
  heroExtraItems: 4,     // extra items pushed into AI Activity so the card
                          // exceeds canvas height and bleeds off the bottom.
  titlePadX: 56,         // horizontal inset inside the title card
  titlePadY: 44,         // vertical inset inside the title card (snug!)
  logoPadX: 26,          // horizontal inset inside the logo card
  logoPadY: 16,          // vertical inset inside the logo card
  logoHeight: 44,        // brand wordmark height inside its card
  headlineSize: 132,     // headline font-size in px
  titleRadius: 32,
  logoRadius: 20,
  cardRadius: 14,        // dashboard chart cards
  activityCardRadius: 18,
};

// Default AI Activity items - used when a thumbnail doesn't supply its own.
// Each topic-specific thumbnail SHOULD override these with items that show
// what the AI is doing in THAT feature (see samples.json).
//
// Item shape:
//   { state: 'done' | 'progress' | 'pending', text: '<short concrete action>' }
//
// Recommended mix per thumbnail: 4-6 done, 1 progress, 2-4 pending. The card
// holds ~10 items and bleeds off the bottom.
const DEFAULT_ITEMS = [
  { state: 'done',     text: 'Sent quote to Amir K.' },
  { state: 'done',     text: 'Booked Sasha R. - 9:00 AM' },
  { state: 'done',     text: 'Followed up with Jordan P.' },
  { state: 'done',     text: 'Generated weekly report' },
  { state: 'done',     text: 'Drafted SMS for Marguerite V.' },
  { state: 'done',     text: 'Closed deal with Tomas L.' },
  { state: 'progress', text: 'Updating 12 deal statuses' },
  { state: 'pending',  text: 'Queue follow-ups for new Leads' },
  { state: 'pending',  text: 'Open Service Requests' },
  { state: 'pending',  text: 'Score new inbound leads' },
];

const defaultData = {
  headline: 'Get AI to Build Your Business',
  accentWord: 'Build',
  items: DEFAULT_ITEMS,
};

// ============================================================
// Headline - one word gets a polished gradient fill with a diagonal sheen
// streak and a teal/blue glow behind it. Same weight + family as the rest of
// the headline so the typographic silhouette stays consistent.
// ============================================================
//
// Smooth teal->mint->blue gradient with a lighter mid-tone (no pure white)
// so letters stay readable. No outer glow - clean gradient fill only.
const ACCENT_GRADIENT = GRADIENT;

const Headline = ({ text, accentWord, color, size = 108 }) => {
  const headlineStyle = { color, fontSize: size, fontWeight: 800, lineHeight: 0.95, letterSpacing: '-0.035em' };
  if (!accentWord) return <span style={headlineStyle}>{text}</span>;
  const parts = text.split(new RegExp(`(\\b${accentWord}\\b)`, 'i'));
  return (
    <span style={headlineStyle}>
      {parts.map((p, i) =>
        p.toLowerCase() === accentWord.toLowerCase() ? (
          <span
            key={i}
            style={{
              background: ACCENT_GRADIENT,
              WebkitBackgroundClip: 'text',
              backgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              color: 'transparent',
            }}
          >
            {p}
          </span>
        ) : (
          <span key={i}>{p}</span>
        )
      )}
    </span>
  );
};

// ============================================================
// Dashboard mockup — designed to FILL the 1280x720 canvas with rich content.
// Mirrors the data shape of the real ReportingListPage in Remotion.
// ============================================================

const StatTile = ({ label, value, trend, color = colors.primary }) => (
  <div style={{
    flex: 1,
    background: '#fff',
    borderRadius: 14,
    padding: '20px 22px',
    boxShadow: '0 1px 2px rgba(15,17,23,0.04), 0 0 0 1px rgba(15,17,23,0.06)',
    display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
      <span style={{ color, fontSize: 13 }}>↗</span>
      <span style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.14em', color: colors.mutedForeground }}>
        {label}
      </span>
    </div>
    <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginTop: 8 }}>
      <div style={{ fontSize: 34, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.02em', lineHeight: 1 }}>
        {value}
      </div>
      {trend && (
        <div style={{ fontSize: 12, fontWeight: 700, color: SUCCESS, background: 'rgba(45,184,125,0.12)', padding: '3px 8px', borderRadius: 999 }}>
          {trend}
        </div>
      )}
    </div>
  </div>
);

const StatRow = () => (
  <div style={{ display: 'flex', gap: 12 }}>
    <StatTile label="TOTAL LEADS" value="284" trend="+12%" />
    <StatTile label="WON OPPS" value="47" trend="+8%" color={SUCCESS} />
    <StatTile label="CONV. RATE" value="16.5%" trend="+2.1pp" color={colors.accent} />
    <StatTile label="REVENUE" value="$312k" trend="+18%" color={LIGHT} />
  </div>
);

const Donut = ({ slices, total, size = 80, label }) => {
  // Build conic-gradient stops
  let acc = 0;
  const stops = slices.map((s) => {
    const start = (acc / total) * 360;
    acc += s.value;
    const end = (acc / total) * 360;
    return `${s.color} ${start}deg ${end}deg`;
  }).join(', ');
  return (
    <div style={{ width: size, height: size, borderRadius: '50%', background: `conic-gradient(${stops})`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
      <div style={{
        width: size * 0.66, height: size * 0.66, borderRadius: '50%', background: '#fff',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: size * 0.22, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.02em',
      }}>
        {label}
      </div>
    </div>
  );
};

const LegendRow = ({ color, label, value }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 12 }}>
    <span style={{ width: 8, height: 8, borderRadius: 2, background: color, flexShrink: 0 }} />
    <span style={{ color: colors.foreground, fontWeight: 600, flex: 1 }}>{label}</span>
    <span style={{ color: colors.foreground, fontWeight: 700 }}>{value}</span>
  </div>
);

const ChartCard = ({ title, children, ...rest }) => (
  <div style={{
    background: '#fff',
    borderRadius: SYS.cardRadius,
    padding: 18,
    // 3-layer fresnel: sharp close + mid lift + soft far + hairline ring.
    boxShadow: '0 1px 2px rgba(15,17,23,0.05), 0 4px 10px rgba(15,17,23,0.04), 0 16px 32px rgba(15,17,23,0.05), 0 0 0 1px rgba(15,17,23,0.05)',
    display: 'flex', flexDirection: 'column',
    ...rest,
  }}>
    <div style={{ fontSize: 13, fontWeight: 700, color: colors.foreground, marginBottom: 12 }}>
      {title}
    </div>
    {children}
  </div>
);

const DealStatusCard = () => (
  <ChartCard title="Deal Status">
    <div style={{ display: 'flex', alignItems: 'center', gap: 14, flex: 1 }}>
      <Donut
        slices={[
          { color: PRIMARY, value: 42 },
          { color: SUCCESS, value: 47 },
          { color: SLATE, value: 18 },
        ]}
        total={107}
        size={80}
        label="107"
      />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6, flex: 1 }}>
        <LegendRow color={PRIMARY} label="Open" value="42" />
        <LegendRow color={SUCCESS} label="Won" value="47" />
        <LegendRow color={SLATE} label="Lost" value="18" />
      </div>
    </div>
  </ChartCard>
);

const PipelineCard = () => (
  <ChartCard title="By Pipeline">
    <div style={{ display: 'flex', alignItems: 'center', gap: 14, flex: 1 }}>
      <Donut
        slices={[
          { color: PRIMARY, value: 58 },
          { color: ACCENT, value: 24 },
          { color: LIGHT, value: 25 },
        ]}
        total={107}
        size={80}
        label="107"
      />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6, flex: 1 }}>
        <LegendRow color={PRIMARY} label="Sales" value="58" />
        <LegendRow color={ACCENT} label="Onboarding" value="24" />
        <LegendRow color={LIGHT} label="Renewals" value="25" />
      </div>
    </div>
  </ChartCard>
);

// (AIActivityCard moved to ./heroes/AIActivityHero.jsx as the default hero.
// The HeroSlot below now resolves the right component per-thumbnail via the
// registry in ./heroes/index.js.)

const TrendChart = () => (
  <ChartCard title="Leads vs Won vs Lost">
    <svg viewBox="0 0 500 110" width="100%" height="110" style={{ display: 'block' }}>
      <defs>
        <linearGradient id="teal-area" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor={PRIMARY} stopOpacity="0.25" />
          <stop offset="100%" stopColor={PRIMARY} stopOpacity="0" />
        </linearGradient>
      </defs>
      {/* Area under leads */}
      <path d="M10,80 L90,72 L170,60 L250,52 L330,38 L410,28 L490,22 L490,110 L10,110 Z" fill="url(#teal-area)" />
      <polyline fill="none" stroke={PRIMARY} strokeWidth="2.5" points="10,80 90,72 170,60 250,52 330,38 410,28 490,22" />
      <polyline fill="none" stroke={SUCCESS} strokeWidth="2.5" points="10,90 90,86 170,82 250,76 330,68 410,62 490,58" />
      <polyline fill="none" stroke={SLATE} strokeWidth="2.5" points="10,98 90,96 170,98 250,94 330,96 410,92 490,94" />
      {/* Data points on leads */}
      {[[10,80],[90,72],[170,60],[250,52],[330,38],[410,28],[490,22]].map(([x,y]) => (
        <circle key={`${x},${y}`} cx={x} cy={y} r="3" fill={PRIMARY} />
      ))}
    </svg>
    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10, color: colors.mutedForeground, marginTop: 2 }}>
      <span>Nov</span><span>Dec</span><span>Jan</span><span>Feb</span><span>Mar</span><span>Apr</span>
    </div>
    <div style={{ display: 'flex', gap: 12, marginTop: 8, fontSize: 11, fontWeight: 600 }}>
      <span style={{ color: PRIMARY }}>— Leads</span>
      <span style={{ color: SUCCESS }}>— Won</span>
      <span style={{ color: SLATE }}>— Lost</span>
    </div>
  </ChartCard>
);

const SourcesChart = () => {
  const sources = [
    { name: 'Referral', won: 18, lost: 3, open: 12 },
    { name: 'Website', won: 14, lost: 6, open: 9 },
    { name: 'Outbound', won: 8, lost: 5, open: 14 },
    { name: 'Social', won: 5, lost: 3, open: 7 },
    { name: 'Events', won: 2, lost: 1, open: 0 },
  ];
  const max = Math.max(...sources.map(s => s.won + s.lost + s.open));
  return (
    <ChartCard title="Lead Sources">
      <div style={{ display: 'flex', alignItems: 'flex-end', gap: 12, height: 110, paddingTop: 4 }}>
        {sources.map((s) => {
          const totalH = ((s.won + s.lost + s.open) / max) * 100;
          const wonH = (s.won / max) * 100;
          const openH = (s.open / max) * 100;
          const lostH = (s.lost / max) * 100;
          return (
            <div key={s.name} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4 }}>
              <div style={{ width: '100%', display: 'flex', flexDirection: 'column-reverse', height: 100 }}>
                <div style={{ height: wonH, background: SUCCESS, borderRadius: '0 0 3px 3px' }} />
                <div style={{ height: openH, background: PRIMARY }} />
                <div style={{ height: lostH, background: SLATE, borderRadius: '3px 3px 0 0' }} />
              </div>
              <span style={{ fontSize: 10, color: colors.mutedForeground, fontWeight: 600 }}>{s.name}</span>
            </div>
          );
        })}
      </div>
    </ChartCard>
  );
};

const DashboardBg = () => (
  <div style={{
    position: 'absolute', inset: 0,
    background: '#f7f8fa',
    padding: SYS.margin,
    display: 'flex', gap: SYS.gap,
    zIndex: 1,
  }}>
    {/* LEFT: chart grid (mostly hidden behind the glass card) */}
    <div style={{ flex: 1.4, display: 'flex', flexDirection: 'column', gap: SYS.gap }}>
      <div style={{ display: 'flex', gap: SYS.gap, flex: 1 }}>
        <DealStatusCard />
        <PipelineCard />
      </div>
      <div style={{ display: 'flex', gap: SYS.gap, flex: 1 }}>
        <div style={{ flex: 1.3, display: 'flex' }}><TrendChart /></div>
        <div style={{ flex: 1, display: 'flex' }}><SourcesChart /></div>
      </div>
    </div>
    {/* RIGHT: placeholder where the AI Activity card USED to live. The
        actual hero card is now an absolute-positioned sibling above this
        layer so it can bleed off the canvas bottom. */}
    <div style={{ flex: 1, display: 'flex', minWidth: 420 }} />
  </div>
);

// ============================================================
// AccentStrip - thin diagonal brand-coloured line that crosses the bottom
// of the canvas. Sits BEHIND the AI Activity hero (lower z-index), so the
// hero card visually cuts through it on the right side. Visual grounding
// without competing with the focal elements.
// ============================================================
const AccentStrip = () => (
  <div style={{
    position: 'absolute',
    left: -60,
    right: -60,
    bottom: 32,
    height: 6,
    background: 'linear-gradient(90deg, #1ea5a5 0%, #29c6c6 30%, #47a3d9 70%, #2e7fb0 100%)',
    transform: 'rotate(-1.5deg)',
    transformOrigin: 'center',
    boxShadow: '0 4px 14px rgba(41,198,198,0.20)',
    borderRadius: 3,
    zIndex: 2,
  }} />
);

// ============================================================
// HeroSlot - the right-side hero. Absolute-positioned so its height isn't
// constrained by the canvas; the bottom drops past the canvas edge and gets
// clipped by overflow:hidden. The actual component rendered comes from the
// hero registry in ./heroes/index.js, looked up via data.hero.
// ============================================================
const HeroSlot = ({ data }) => {
  const HeroComponent = resolveHero(data.hero);
  return (
    <div style={{
      position: 'absolute',
      top: SYS.margin,
      right: SYS.margin,
      width: SYS.heroWidth,
      zIndex: 4,
    }}>
      <HeroComponent data={data} />
    </div>
  );
};

// Logo image element - used inside LogoCard below.
const Logo = ({ height = 44 }) => (
  <img
    src={BRAND_LOGO}
    alt={NAME}
    style={{ display: 'block', height, width: 'auto', objectFit: 'contain' }}
  />
);

// LogoCard - the owner's brand wordmark sitting directly on the flat white
// canvas at top-left. No card, no padding - the leftmost pixel of the logo
// aligns with the leftmost pixel of the headline text below.
const LogoCard = () => (
  <img
    src={BRAND_LOGO}
    alt={NAME}
    style={{
      position: 'absolute',
      left: SYS.margin,
      top: SYS.margin,
      height: SYS.logoHeight,
      width: 'auto',
      objectFit: 'contain',
      zIndex: 9,
    }}
  />
);

// ============================================================
// ColorHalo - soft brand blooms positioned BEHIND the AI Activity hero on
// the right. The left side stays clean flat white. The mask fades the halos
// out to the left so they don't bleed past the title text area.
// ============================================================
const ColorHalo = () => {
  const fadeLeft = {
    WebkitMaskImage: 'linear-gradient(to left, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 28%, rgba(0,0,0,0.55) 45%, rgba(0,0,0,0) 58%)',
    maskImage: 'linear-gradient(to left, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 28%, rgba(0,0,0,0.55) 45%, rgba(0,0,0,0) 58%)',
  };
  return (
    <div style={{
      position: 'absolute', inset: 0, zIndex: 3, pointerEvents: 'none',
      ...fadeLeft,
    }}>
      {/* Primary teal bloom upper-right */}
      <div style={{
        position: 'absolute', right: -180, top: -100, width: 720, height: 600,
        background: 'radial-gradient(circle, rgba(41,198,198,0.55) 0%, rgba(41,198,198,0) 65%)',
        filter: 'blur(70px)',
      }} />
      {/* Accent blue bloom mid */}
      <div style={{
        position: 'absolute', right: 60, top: 180, width: 560, height: 500,
        background: 'radial-gradient(circle, rgba(71,163,217,0.38) 0%, rgba(71,163,217,0) 65%)',
        filter: 'blur(80px)',
      }} />
      {/* Mint highlight lower-right */}
      <div style={{
        position: 'absolute', right: -120, bottom: -160, width: 560, height: 540,
        background: 'radial-gradient(circle, rgba(125,211,211,0.50) 0%, rgba(125,211,211,0) 65%)',
        filter: 'blur(75px)',
      }} />
    </div>
  );
};

// ============================================================
// GlassCard - the headline text on the flat white surface.
// Anchored to the LEFT and vertically centred in the canvas.
// Leftmost character aligns with the leftmost pixel of the logo at the bottom.
// ============================================================
const GlassCard = ({ d }) => (
  <div style={{
    position: 'absolute',
    left: SYS.margin,
    top: '50%',
    transform: 'translateY(-50%)',
    width: SYS.leftColWidth,
    zIndex: 8,
    // Stacked white drop-shadows give the headline a soft halo. Invisible
    // against the flat white left side, kicks in where the headline
    // overlaps with the hero card / accent strip on the right so the text
    // stays legible. CSS filter (not text-shadow) so it works with the
    // background-clip:text gradient accent word too.
    filter: 'drop-shadow(0 0 8px #ffffff) drop-shadow(0 0 16px #ffffff) drop-shadow(0 0 24px rgba(255,255,255,0.85))',
  }}>
    <h1 style={{ margin: 0, fontSize: 0, textAlign: 'left' }}>
      <Headline text={d.headline} accentWord={d.accentWord} color={colors.foreground} size={d.headlineSize || SYS.headlineSize} />
    </h1>
  </div>
);

// ============================================================
// MAIN
// ============================================================
const GlassCardThumbnail = ({ d }) => (
  <div style={{
    width: THUMBNAIL_SIZE.width, height: THUMBNAIL_SIZE.height,
    position: 'relative', overflow: 'hidden',
    fontFamily: fonts.primary,
    // Flat white surface. Logo + headline sit directly on this background.
    // Brand-colour halos live behind the AI Activity hero on the right.
    background: PANEL,
  }}>
    <ColorHalo />
    <AccentStrip />
    <HeroSlot data={d} />
    <LogoCard />
    <GlassCard d={d} />
  </div>
);

export const YouTubeThumbnail = ({ data = {} }) => {
  const d = { ...defaultData, ...data };
  return <div className="template-canvas"><GlassCardThumbnail d={d} /></div>;
};

YouTubeThumbnail.templateMeta = {
  id: 'youtube-thumbnail',
  name: 'YouTube Thumbnail',
  size: THUMBNAIL_SIZE,
  description: "YouTube thumbnail on the owner's brand. 1280x720, 16:9.",
};

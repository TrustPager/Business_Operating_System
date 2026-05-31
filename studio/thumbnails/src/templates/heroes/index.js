// ============================================================================
// HERO REGISTRY — how to add or replace a thumbnail hero
// ============================================================================
//
// Each thumbnail's right-side card is a topic-specific static React component
// that mimics the actual product surface from that video. The key in samples
// .json (`"hero": "pipeline"`) maps to a component in this registry.
//
// ─── The six family patterns ─────────────────────────────────────────────────
//
//  CARD STACK     ServiceRequestHero, ContactsHero, ApprovalsHero,
//                 ESigningHero, NotepadsHero (preview-list variant)
//                 → discrete records, each a self-contained card
//
//  EVENT/LOG ROW  GoogleCalendarHero, SendEmailsHero, StageEmailsHero,
//                 EventQueuesHero
//                 → timestamped events flowing down a feed
//
//  FIELD STACK    FormsHero, FillWithAIHero
//                 → label + value pairs, some mid-auto-fill
//
//  ROSTER         PermissionsHero, AgentHubHero
//                 → role/agent identities with metadata + actions
//                 (PermissionsHero adds a scope-grid matrix below the header)
//
//  CHECKLIST      TasksHero
//                 → items with state pills (✓ / ⏳ / ◯)
//
//  DOCUMENT       ProposalsHero, NeedsAnalysisHero, CrmTemplatesHero,
//                 NotepadsHero (current — single polished doc)
//                 → a single polished doc rendered top-to-bottom
//
//  FLOW           AutomationsHero
//                 → trigger → action cards connected by arrows
//
// ─── Adding a hero ──────────────────────────────────────────────────────────
//
//   1. Pick a family above. Copy the closest existing hero as a starting
//      point. Edit the data + tweak the silhouette to match your topic.
//
//   2. Save as heroes/<TopicName>Hero.jsx. Export the component as a named
//      export: `export const TopicNameHero = () => …`
//
//   3. Register below (import + add to HEROES with a kebab-case key).
//
//   4. Reference from samples.json:
//      "my-topic": { "data": { "hero": "my-topic", ... } }
//
//   5. npm run shoot my-topic — verify the rendered PNG, not just the studio.
//      Pass the squint test: at 25% zoom, the silhouette must say "this is
//      the X feature" without reading any text.
//
// ─── Master rules every hero MUST follow ────────────────────────────────────
//
//   ✓ Single outer container — white card, `borderRadius: 18`, heavy shadow
//     (`0 26px 52px rgba(15,17,23,0.12)` + the surrounding minor shadows
//     copied from any existing hero), ~18px padding.
//
//   ✓ Thin / tall / single vertical stack — NO horizontal subdivisions
//     inside the card. No side-by-side columns. No 2-up grids. The card is
//     ~528px wide; content stacks down one column.
//
//   ✓ Bleeds off the bottom — render enough items (6-10 typically) that
//     the last one or two clip at the canvas edge. That bleed is what
//     tells the viewer "this feature goes on and on".
//
//   ✓ Brand colours only — teal #29c6c6, green #2db87d, blue #47a3d9,
//     light teal #7dd3d3, deep teal #1ea5a5, slate #94a3b8. NEVER orange /
//     purple / red in hero chrome, even when the real product UI uses them.
//     (Photographic avatars are exempt — they're identity, not chrome.)
//
//   ✓ Inner panels use a light border, NOT their own shadow —
//     `1px solid rgba(226,232,240,0.7)`. The heavy shadow lives on the
//     outer container only; stacking heavy shadows reads as "floating
//     tiles" instead of "sections of one dashboard".
//
//   ✓ Outcome state, not configurator — show what landed, not the form
//     that submitted it. Stack of "form filled the CRM" events, not the
//     form builder. Stack of "approved + sent" cards, not the pending
//     queue. Stack of signed contracts, not the signing modal.
//
//   ✓ Real avatars over initials — import `Avatar` from `../../profiles
//     .jsx` for people (5 hashed portraits, stable per name). Use the AI
//     agent portraits at `/agents/<Name>.png` for AgentHubHero. Initial-
//     letter coloured divs are a fallback only when avatars don't apply
//     (deal cards in PipelineHero use rounded-square initials for account
//     branding — that's intentional).
//
//   ✓ Caricature beats realism — if a faithful product render is illegible
//     at thumbnail scale, exaggerate. Fewer items but each one bigger.
//     Bolder colour anchors. The hero is a MINIATURE, not a screenshot.
//
//   ✓ Standard hero header — green pulse dot + bold topic title + small
//     pill on the right showing a stat or status. Every hero opens with
//     this header so the family reads as one design system. Examples:
//
//     [● Bookings]                    [LIVE]
//     [● Sales Pipeline]              [LIVE]
//     [● Performance Dashboard]       [Q3 · LIVE]
//     [● Auto-Sent Emails]            [SENT AUTOMATICALLY]
//     [● Your AI Team]                [7 ACTIVE · 113 RUNS TODAY]
//
// ─── Hero anti-patterns (mistakes already made and corrected) ───────────────
//
//   ✗ Two-column layout inside the hero (SMS v1 had a conversation list
//     on the left + thread on the right — broke the thin-vertical rule).
//   ✗ Multi-column kanban (PipelineHero v1 had 4 columns side-by-side —
//     same break).
//   ✗ Stacked panels without an outer container (ReportsHero v1 — read as
//     four floating tiles, not one dashboard).
//   ✗ Dense scope-permissions matrix as the main silhouette (Permissions
//     v1 — felt bureaucratic; the matrix should appear under a role
//     header card, not be the whole hero).
//   ✗ List of notepad previews where the topic was the notepad itself
//     (Notepads v1 — should have been ONE rich polished notepad).
//   ✗ Generic AI Activity text rows for every topic — read as the same
//     thing for every video; failed the squint test for everything except
//     Agent Hub / Fill with AI.
//
// ─── See also ───────────────────────────────────────────────────────────────
//
//   • ../YouTubeThumbnail.jsx       JSDoc — full design system + SYS constants
//   • ../../profiles.jsx            Avatar component for people
//   • /agents/<Name>.png            AI agent portraits (Aria / Marty / …)
//   • ../../../README.md            human-readable guide with examples
//   • ../../../CLAUDE.md            AI-assistant entry point
//
// ============================================================================

import { AIActivityHero }     from './AIActivityHero.jsx';
import { SchedulingHero }     from './SchedulingHero.jsx';
import { ServiceRequestHero } from './ServiceRequestHero.jsx';
import { GoogleCalendarHero } from './GoogleCalendarHero.jsx';
import { FormsHero }          from './FormsHero.jsx';
import { NeedsAnalysisHero }  from './NeedsAnalysisHero.jsx';
import { NotepadsHero }       from './NotepadsHero.jsx';
import { PermissionsHero }    from './PermissionsHero.jsx';
import { PipelineHero }       from './PipelineHero.jsx';
import { ReportsHero }        from './ReportsHero.jsx';
import { SmsHero }            from './SmsHero.jsx';
import { AutomationsHero }    from './AutomationsHero.jsx';
import { TasksHero }          from './TasksHero.jsx';
import { AgentHubHero }       from './AgentHubHero.jsx';
import { ApprovalsHero }      from './ApprovalsHero.jsx';
import { StageEmailsHero }    from './StageEmailsHero.jsx';
import { ContactsHero }       from './ContactsHero.jsx';
import { CrmTemplatesHero }   from './CrmTemplatesHero.jsx';
import { ProposalsHero }      from './ProposalsHero.jsx';
import { SendEmailsHero }     from './SendEmailsHero.jsx';
import { ESigningHero }       from './ESigningHero.jsx';
import { EventQueuesHero }    from './EventQueuesHero.jsx';
import { FillWithAIHero }     from './FillWithAIHero.jsx';
import { ClaudePipelineHero } from './ClaudePipelineHero.jsx';
import { EmailCampaignsHero } from './EmailCampaignsHero.jsx';
import { PlatformOverviewHero } from './PlatformOverviewHero.jsx';

export const HEROES = {
  'ai-activity':     AIActivityHero,    // legacy fallback — being retired
  'scheduling':      SchedulingHero,
  'service-request': ServiceRequestHero,
  'google-calendar': GoogleCalendarHero,
  'forms':           FormsHero,
  'needs-analysis':  NeedsAnalysisHero,
  'notepads':        NotepadsHero,
  'permissions':     PermissionsHero,
  'pipeline':        PipelineHero,
  'reports':         ReportsHero,
  'sms':             SmsHero,
  'automations':     AutomationsHero,
  'tasks':           TasksHero,
  'agent-hub':       AgentHubHero,
  'approvals':       ApprovalsHero,
  'stage-emails':    StageEmailsHero,
  'contacts':        ContactsHero,
  'crm-templates':   CrmTemplatesHero,
  'proposals':       ProposalsHero,
  'send-emails':     SendEmailsHero,
  'esigning':        ESigningHero,
  'event-queues':    EventQueuesHero,
  'fill-with-ai':    FillWithAIHero,
  'claude-pipeline': ClaudePipelineHero,
  'email-campaigns': EmailCampaignsHero,
  'platform-overview': PlatformOverviewHero,
};

export const resolveHero = (key) => HEROES[key] || HEROES['ai-activity'];

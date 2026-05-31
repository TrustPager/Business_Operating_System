// Claude Pipeline hero — for "How to Build a Leads Pipeline with Claude"
// (composition: Hybrid-LeadsPipeline-Build).
//
// Master rule (see ../YouTubeThumbnail.jsx HERO UI SELECTION): thin, tall,
// single vertical stack, bleeds off bottom. The viewer reads:
//   "Claude built a stack of stage-automations across a pipeline."
//
// Reference for the silhouette: ../../../../src/compositions/HybridCompositions
// .tsx. The video's iconic moment is the cursor flying across 4 stage bolts
// and a popover card appearing for each one. We freeze that moment as 4
// stacked stage rows, each with its automation card visible — plus a couple
// of queued/in-flight rows below so the hero bleeds off the bottom.
//
// Differentiator vs PipelineHero (deal cards) and AutomationsHero (single
// trigger-to-action flow): this is MULTIPLE stages each with their own
// automation. The coloured left-edge bars + bolt icons stack vertically and
// create the "rainbow with sparks" silhouette that survives the squint test.

import React from 'react';
import { colors } from '../../theme.js';
import { ACCENT, LIGHT, PRIMARY, PRIMARY_DEEP, SLATE, SUCCESS, TEXT_MUTED } from '../../brand.js';

const STAGES = [
  {
    name: 'New Enquiry',
    color: ACCENT,
    automationTitle: 'Auto-reply',
    trigger: 'A new lead enters this stage',
    action: 'Send "Thanks, we got your message" email',
    state: 'built',
  },
  {
    name: 'Discovery Call',
    color: PRIMARY,
    automationTitle: '3-day follow-up',
    trigger: 'Opportunity sits in this stage for 3 days',
    action: 'Send "Just checking in" email',
    state: 'built',
  },
  {
    name: 'Proposal Sent',
    color: SUCCESS,
    automationTitle: '5-day chase',
    trigger: 'Proposal unsigned after 5 days',
    action: 'Send chase email + create owner task',
    state: 'built',
  },
  {
    name: 'Negotiation',
    color: PRIMARY_DEEP,
    automationTitle: 'Day-before reminder',
    trigger: 'Discovery call scheduled tomorrow',
    action: 'Send "See you tomorrow" SMS + email',
    state: 'built',
  },
  {
    name: 'Won',
    color: LIGHT,
    automationTitle: 'Welcome to onboarding',
    trigger: 'Deal moved to Won',
    action: 'Create onboarding task + send welcome',
    state: 'building',
  },
  {
    name: 'Lost',
    color: SLATE,
    automationTitle: 'Nurture sequence',
    trigger: 'Deal moved to Lost',
    action: 'Enrol in 90-day stay-warm queue',
    state: 'queued',
  },
];

const STATE = {
  built:    { fg: SUCCESS, bg: 'rgba(45,184,125,0.18)', label: '✓ BUILT' },
  building: { fg: PRIMARY_DEEP, bg: 'rgba(41,198,198,0.22)', label: '● BUILDING' },
  queued:   { fg: TEXT_MUTED, bg: 'rgba(148,163,184,0.16)', label: '◷ QUEUED' },
};

const BoltIcon = ({ color }) => (
  <svg width={20} height={20} viewBox="0 0 24 24" fill={color}>
    <path d="M13 2L4.5 13.5h6L11 22l8.5-11.5h-6L13 2z" />
  </svg>
);

const StageAutomationCard = ({ s }) => {
  const st = STATE[s.state];
  const isBuilt = s.state === 'built';
  return (
    <div style={{
      background: '#fff',
      borderRadius: 12,
      padding: '13px 15px 13px 18px',
      border: '1px solid rgba(226,232,240,0.7)',
      borderLeft: `5px solid ${s.color}`,
      display: 'flex', flexDirection: 'column', gap: 8,
      opacity: s.state === 'queued' ? 0.78 : 1,
    }}>
      {/* Row 1: Stage name + bolt + state pill */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 9, minWidth: 0, flex: 1 }}>
          <div style={{
            width: 32, height: 32, borderRadius: 9,
            background: isBuilt
              ? `linear-gradient(135deg, ${s.color}, ${s.color}cc)`
              : 'rgba(148,163,184,0.16)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: isBuilt ? `0 4px 10px ${s.color}40` : 'none',
            flexShrink: 0,
          }}>
            <BoltIcon color={isBuilt ? '#fff' : SLATE} />
          </div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{
              fontSize: 9, fontWeight: 800, letterSpacing: '0.10em',
              color: colors.mutedForeground,
            }}>STAGE</div>
            <div style={{
              fontSize: 15, fontWeight: 800, color: colors.foreground,
              letterSpacing: '-0.01em', lineHeight: 1.1, marginTop: 1,
              overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
            }}>{s.name}</div>
          </div>
        </div>
        <span style={{
          fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
          color: st.fg, background: st.bg,
          padding: '3px 8px', borderRadius: 999,
          flexShrink: 0,
        }}>{st.label}</span>
      </div>

      {/* Row 2: Automation title pill */}
      <div style={{
        fontSize: 12, fontWeight: 800, letterSpacing: '-0.01em',
        color: s.color,
        background: `${s.color}1a`,
        padding: '4px 10px', borderRadius: 8,
        alignSelf: 'flex-start',
      }}>{s.automationTitle}</div>

      {/* Row 3: Trigger + Action lines */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <div style={{
          fontSize: 10.5, fontWeight: 700, color: colors.mutedForeground,
          letterSpacing: '-0.005em',
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>
          <span style={{ fontSize: 9, fontWeight: 800, letterSpacing: '0.10em', color: SLATE, marginRight: 4 }}>WHEN</span>
          {s.trigger}
        </div>
        <div style={{
          fontSize: 10.5, fontWeight: 700, color: colors.foreground,
          letterSpacing: '-0.005em',
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>
          <span style={{ fontSize: 9, fontWeight: 800, letterSpacing: '0.10em', color: SLATE, marginRight: 4 }}>DO</span>
          {s.action}
        </div>
      </div>
    </div>
  );
};

export const ClaudePipelineHero = () => (
  <div style={{
    background: '#fff',
    borderRadius: 18,
    padding: 18,
    boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
    display: 'flex', flexDirection: 'column', gap: 14,
  }}>
    {/* Header */}
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <span style={{
          width: 12, height: 12, borderRadius: '50%',
          background: SUCCESS,
          boxShadow: '0 0 0 5px rgba(45,184,125,0.22)',
        }} />
        <span style={{ fontSize: 19, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.015em' }}>
          Leads Pipeline
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.10em',
        color: PRIMARY_DEEP,
        background: 'rgba(41,198,198,0.14)',
        padding: '5px 10px', borderRadius: 999,
      }}>BUILT BY AI · 90s</span>
    </div>

    {/* Stage-automation stack — bleeds off bottom */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 9 }}>
      {STAGES.map((s, i) => <StageAutomationCard key={i} s={s} />)}
    </div>
  </div>
);

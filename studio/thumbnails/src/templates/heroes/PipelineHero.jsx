// Pipeline hero — single coloured stage header + vertical stack of deal cards.
//
// Master rule (see ../YouTubeThumbnail.jsx HERO UI SELECTION): thin, tall,
// single vertical stack, bleeds off the bottom. NOT a 4-column kanban.
// The viewer reads "deal cards stacked under a stage" and infers pipeline.
//
// Reference: ../../../../src/scenes/features/PipelineView.tsx
// Outcome framing: deals are moving through the pipeline — one is mid-drag
// to show motion, all are real and worth money.

import React from 'react';
import { colors } from '../../theme.js';
import { Avatar } from '../../profiles.jsx';

const STAGE = {
  name: 'Proposal Sent',
  color: '#29c6c6',
  count: 8,
  total: 'A$487,300',
};

const DEALS = [
  { account: 'Coastal Health Group',   value: '$96k',  tag: 'Inbound',   avatar: 'CH', avatarColor: '#29c6c6', dragging: false },
  { account: 'Wattle Creek Winery',    value: '$54k',  tag: 'Email',     avatar: 'WC', avatarColor: '#47a3d9', dragging: true  },
  { account: 'Pinnacle Engineering',   value: '$78k',  tag: 'Referral',  avatar: 'PE', avatarColor: '#2db87d', dragging: false },
  { account: 'Eucalyptus Wealth',      value: '$33k',  tag: 'Website',   avatar: 'EW', avatarColor: '#7dd3d3', dragging: false },
  { account: 'Southern Cross Legal',   value: '$120k', tag: 'Direct',    avatar: 'SC', avatarColor: '#29c6c6', dragging: false },
  { account: 'Ironbark Construction',  value: '$67k',  tag: 'Inbound',   avatar: 'IC', avatarColor: '#2db87d', dragging: false },
  { account: 'Outback Solar Solutions',value: '$28k',  tag: 'LinkedIn',  avatar: 'OS', avatarColor: '#47a3d9', dragging: false },
  { account: 'Reef & Co Logistics',    value: '$42k',  tag: 'Referral',  avatar: 'RC', avatarColor: '#29c6c6', dragging: false },
  { account: 'Banksia Financial',      value: '$15k',  tag: 'Website',   avatar: 'BF', avatarColor: '#7dd3d3', dragging: false },
];

const CARD_SHADOW = '0 1px 2px rgba(15,17,23,0.05), 0 0 0 1px rgba(15,17,23,0.07)';
const DRAG_SHADOW = '0 16px 36px rgba(41,198,198,0.30), 0 0 0 1.5px rgba(41,198,198,0.45)';

const DealCard = ({ d }) => (
  <div style={{
    background: '#fff',
    borderRadius: 12,
    padding: '14px 16px',
    boxShadow: d.dragging ? DRAG_SHADOW : CARD_SHADOW,
    transform: d.dragging ? 'rotate(-1.2deg) translateY(-2px)' : 'none',
    display: 'flex', flexDirection: 'column', gap: 9,
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
      <Avatar name={d.account} size={32} style={{ borderRadius: 9 }} />
      <div style={{
        fontSize: 15, fontWeight: 800, color: colors.foreground,
        letterSpacing: '-0.01em', flex: 1, minWidth: 0,
        overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
      }}>{d.account}</div>
    </div>
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.08em',
        color: colors.mutedForeground,
        background: 'rgba(148,163,184,0.16)',
        padding: '4px 10px', borderRadius: 999,
        textTransform: 'uppercase',
      }}>{d.tag}</span>
      <span style={{
        fontSize: 20, fontWeight: 800, color: colors.foreground,
        letterSpacing: '-0.02em',
      }}>{d.value}</span>
    </div>
  </div>
);

export const PipelineHero = () => (
  <div style={{
    background: '#fff',
    borderRadius: 18,
    padding: 18,
    boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
    display: 'flex', flexDirection: 'column', gap: 12,
  }}>
    {/* Stage header — the colour anchor */}
    <div style={{
      background: `linear-gradient(135deg, ${STAGE.color}, #47a3d9)`,
      borderRadius: 12,
      padding: '14px 18px',
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      boxShadow: `0 4px 14px ${STAGE.color}40`,
    }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <span style={{ fontSize: 18, fontWeight: 800, color: '#fff', letterSpacing: '-0.01em' }}>
          {STAGE.name}
        </span>
        <span style={{ fontSize: 12, fontWeight: 700, color: 'rgba(255,255,255,0.85)', letterSpacing: '-0.005em' }}>
          {STAGE.count} deals · {STAGE.total}
        </span>
      </div>
      <div style={{
        background: 'rgba(255,255,255,0.20)',
        borderRadius: 10,
        padding: '6px 12px',
        fontSize: 18, fontWeight: 800, color: '#fff',
        letterSpacing: '-0.02em',
      }}>{STAGE.count}</div>
    </div>

    {/* Vertical deal stack — bleeds off bottom */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      {DEALS.map((d, i) => <DealCard key={i} d={d} />)}
    </div>
  </div>
);

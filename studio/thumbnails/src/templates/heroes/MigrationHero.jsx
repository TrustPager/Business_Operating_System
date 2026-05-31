// Migration hero — for "Use AI to Migrate Your Data into TrustPager"
// (composition: Tutorial-MigrateData).
//
// Master rule (see ../YouTubeThumbnail.jsx HERO UI SELECTION): thin, tall,
// single vertical stack, bleeds off bottom. The viewer reads:
//   "AI read my files and moved everything across — companies, contacts, deals."
//
// Differentiator vs ClaudePipelineHero (stage automations) and PipelineHero
// (deal cards): this is a build manifest of the migration run itself.
// Five completed rows (CSVs read · companies · contacts · deals · flagged)
// stacking vertically with the same coloured-left-bar + icon-on-tile
// silhouette so it survives the squint test at thumbnail scale.

import React from 'react';
import { colors } from '../../theme.js';
import { ACCENT, PRIMARY, PRIMARY_DEEP, SLATE, SUCCESS } from '../../brand.js';

const ROWS = [
  {
    name: 'CSV files read',
    detail: '3 files · 174 rows',
    color: SLATE,  // slate — input step, neutral
    state: 'done',
  },
  {
    name: 'Companies created',
    detail: '38 accounts · industry, phone, email',
    color: SUCCESS,  // brand green
    state: 'done',
  },
  {
    name: 'Contacts linked',
    detail: '112 contacts · linked to their company',
    color: ACCENT,  // brand blue
    state: 'done',
  },
  {
    name: 'Open deals slotted',
    detail: '24 deals · across 4 pipeline stages',
    color: PRIMARY,  // brand teal
    state: 'done',
  },
  {
    name: 'Flagged for review',
    detail: '2 rows · ask AI to finish them',
    color: PRIMARY_DEEP,  // deep teal — attention without alarm
    state: 'review',
  },
];

const STATE = {
  done:   { fg: SUCCESS, bg: 'rgba(45,184,125,0.18)',  label: '✓ DONE' },
  review: { fg: PRIMARY_DEEP, bg: 'rgba(41,198,198,0.18)',  label: '◷ REVIEW' },
};

const CheckIcon = ({ color }) => (
  <svg width={18} height={18} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={3.2} strokeLinecap="round" strokeLinejoin="round">
    <polyline points="5 12 10 17 19 7" />
  </svg>
);

const ReviewIcon = ({ color }) => (
  <svg width={18} height={18} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={2.6} strokeLinecap="round" strokeLinejoin="round">
    <circle cx={12} cy={12} r={9} />
    <path d="M12 7v5l3 2" />
  </svg>
);

const MigrationRow = ({ r }) => {
  const st = STATE[r.state];
  const isDone = r.state === 'done';
  const Icon = isDone ? CheckIcon : ReviewIcon;
  return (
    <div style={{
      background: '#fff',
      borderRadius: 12,
      padding: '14px 16px 14px 18px',
      border: '1px solid rgba(226,232,240,0.7)',
      borderLeft: `5px solid ${r.color}`,
      display: 'flex', alignItems: 'center', gap: 12,
    }}>
      {/* Coloured icon tile */}
      <div style={{
        width: 38, height: 38, borderRadius: 10,
        background: `linear-gradient(135deg, ${r.color}, ${r.color}cc)`,
        boxShadow: `0 4px 10px ${r.color}40`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0,
      }}>
        <Icon color="#fff" />
      </div>

      {/* Step name + detail */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          fontSize: 15, fontWeight: 800, color: colors.foreground,
          letterSpacing: '-0.01em', lineHeight: 1.1,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{r.name}</div>
        <div style={{
          fontSize: 11.5, fontWeight: 700, color: colors.mutedForeground,
          letterSpacing: '-0.005em', marginTop: 3,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{r.detail}</div>
      </div>

      {/* State pill */}
      <span style={{
        fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
        color: st.fg, background: st.bg,
        padding: '4px 9px', borderRadius: 999,
        flexShrink: 0,
      }}>{st.label}</span>
    </div>
  );
};

export const MigrationHero = () => (
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
          Data Migration
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.10em',
        color: PRIMARY_DEEP,
        background: 'rgba(41,198,198,0.14)',
        padding: '5px 10px', borderRadius: 999,
      }}>174 RECORDS · BY AI</span>
    </div>

    {/* Migration step stack — bleeds off bottom */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 9 }}>
      {ROWS.map((r, i) => <MigrationRow key={i} r={r} />)}
    </div>
  </div>
);

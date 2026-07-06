// Before & After hero — topic-agnostic transformation / result story.
//
// Family: closest to CARD STACK (see ../index.js), but purpose-built for
// "before and after" and "here's the result" videos. The master rule bans
// side-by-side columns, so the split runs VERTICALLY: a muted "starting
// point" panel on top, a bright "where you land" panel below, joined by a
// single arrow node, then a run of metric rows that each step up from a
// slate before-value to a brand after-value and bleed off the bottom.
//
// The silhouette reads as transformation at 25% zoom: a grey block, an
// arrow, a coloured block, then a column of "went up" rows — no reading
// required.
//
// Framing is kept positive and neutral (starting out -> now), never pain-led.
// Colours flow through ../../brand.js so the hero reskins with brand.json;
// the only literals are the shared neutral shadow/border.

import React from 'react';
import { PANEL, PRIMARY, PRIMARY_DEEP, SLATE, SUCCESS, TEXT, TEXT_MUTED } from '../../brand.js';

const BEFORE = { pill: 'STARTING OUT', value: '23%', pct: 23, caption: 'Where you begin' };
const AFTER  = { pill: 'NOW',          value: '91%', pct: 91, caption: 'Where you land' };

// Generic, positive metric rows — each steps up. Words are interchangeable;
// the "slate -> brand, arrow up" shape is what survives shrinking.
const CHANGES = [
  { label: 'Output',      before: '18',    after: '94'    },
  { label: 'Time back',   before: '2 hrs', after: '20 hrs'},
  { label: 'Reach',       before: '120',   after: '3.4k'  },
  { label: 'Rating',      before: '3.9',   after: '4.9'   },
  { label: 'Repeat rate', before: '1 in 5',after: '4 in 5'},
  { label: 'Reviews',     before: '12',    after: '180'   },
  { label: 'Bookings',    before: '6',     after: '38'    },
  { label: 'Referrals',   before: '1',     after: '9'     },
  { label: 'Signups',     before: '40',    after: '610'   },
];

const Bar = ({ pct, fill }) => (
  <div style={{ height: 12, borderRadius: 6, background: `${SLATE}1f`, overflow: 'hidden' }}>
    <div style={{ width: `${pct}%`, height: '100%', borderRadius: 6, background: fill }} />
  </div>
);

const StagePanel = ({ stage, tone }) => {
  const brand = tone === 'after';
  const accent = brand ? PRIMARY : SLATE;
  return (
    <div style={{
      background: brand ? `${PRIMARY}0f` : `${SLATE}12`,
      border: brand ? `1.5px solid ${PRIMARY}45` : '1px solid rgba(226,232,240,0.7)',
      borderRadius: 12,
      padding: '13px 15px',
      display: 'flex', flexDirection: 'column', gap: 9,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{
          fontSize: 10, fontWeight: 800, letterSpacing: '0.12em',
          color: brand ? PRIMARY_DEEP : SLATE,
          background: brand ? `${PRIMARY}22` : `${SLATE}1f`,
          padding: '3px 9px', borderRadius: 999,
        }}>{stage.pill}</span>
        <span style={{
          fontSize: 30, fontWeight: 800, lineHeight: 1,
          color: brand ? TEXT : SLATE, letterSpacing: '-0.03em',
        }}>{stage.value}</span>
      </div>
      <Bar pct={stage.pct} fill={brand ? PRIMARY : `${SLATE}8c`} />
      <span style={{ fontSize: 10.5, fontWeight: 600, color: TEXT_MUTED }}>{stage.caption}</span>
    </div>
  );
};

const ChangeRow = ({ c }) => (
  <div style={{
    display: 'flex', alignItems: 'center', gap: 10,
    padding: '9px 13px',
    background: PANEL,
    border: '1px solid rgba(226,232,240,0.7)',
    borderRadius: 10,
  }}>
    <span style={{
      flex: 1, minWidth: 0,
      fontSize: 13, fontWeight: 700, color: TEXT, letterSpacing: '-0.01em',
      overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
    }}>{c.label}</span>
    <span style={{ fontSize: 12.5, fontWeight: 700, color: SLATE }}>{c.before}</span>
    <span style={{ fontSize: 13, fontWeight: 800, color: `${SLATE}9e` }}>→</span>
    <span style={{
      fontSize: 13.5, fontWeight: 800, color: SUCCESS,
      display: 'flex', alignItems: 'center', gap: 3,
    }}>
      <span style={{ fontSize: 11 }}>↑</span>{c.after}
    </span>
  </div>
);

export const BeforeAfterHero = () => (
  <div style={{
    background: PANEL,
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
          boxShadow: `0 0 0 5px ${SUCCESS}38`,
        }} />
        <span style={{ fontSize: 19, fontWeight: 800, color: TEXT, letterSpacing: '-0.015em' }}>
          Before &amp; After
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: SUCCESS, background: `${SUCCESS}1f`,
        padding: '5px 10px', borderRadius: 999,
      }}>TRANSFORMED</span>
    </div>

    {/* Vertical before -> after */}
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <StagePanel stage={BEFORE} tone="before" />
      {/* Arrow node bridging the two panels */}
      <div style={{ display: 'flex', justifyContent: 'center', margin: '-8px 0', zIndex: 1 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div style={{
            width: 32, height: 32, borderRadius: '50%',
            background: PRIMARY, color: PANEL,
            fontSize: 17, fontWeight: 800,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            border: `3px solid ${PANEL}`,
            boxShadow: `0 4px 12px ${PRIMARY}40`,
          }}>↓</div>
          <span style={{
            fontSize: 11, fontWeight: 800, letterSpacing: '0.10em',
            color: SUCCESS, background: `${SUCCESS}1f`,
            padding: '4px 10px', borderRadius: 999,
            border: `2px solid ${PANEL}`,
          }}>4× BETTER</span>
        </div>
      </div>
      <StagePanel stage={AFTER} tone="after" />
    </div>

    {/* What changed — steps up and bleeds off the bottom */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.10em',
        color: TEXT_MUTED, marginBottom: 1,
      }}>WHAT CHANGED</span>
      {CHANGES.map((c, i) => <ChangeRow key={i} c={c} />)}
    </div>
  </div>
);

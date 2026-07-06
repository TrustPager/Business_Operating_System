// Big Number hero — topic-agnostic single-stat centrepiece.
//
// Family: closest to DOCUMENT (see ../index.js) — one polished artefact
// rendered top-to-bottom. Built for "by the numbers" and "the real cost of
// X" style videos, where one bold figure carries the whole thumbnail. The
// silhouette is deliberately lopsided: a giant number dominating the top,
// then a slim breakdown that shows where the number comes from and bleeds
// off the bottom. The number survives the squint test on its own.
//
// The baked figure is framed as a positive result (a total earned / saved),
// never a loss — the owner's headline supplies any "cost of X" framing.
// The breakdown rows sum to the headline exactly. Colours flow through
// ../../brand.js so the hero reskins with brand.json; the breakdown bars
// cycle through the brand palette (multi-hued on a colourful brand, a clean
// slate ramp on the neutral starter). Only the shared neutral shadow/border
// are literals.

import React from 'react';
import { ACCENT, DEEP_BLUE, LIGHT, MID_MINT, PANEL, PRIMARY, SLATE, SUCCESS, TEXT, TEXT_MUTED } from '../../brand.js';

const money = (n) => '$' + n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');

// Positive contributors — they sum to the headline figure exactly.
const BREAKDOWN = [
  { label: 'Automated tasks',   value: 18200 },
  { label: 'Faster quoting',    value: 9400  },
  { label: 'Kept bookings',     value: 7100  },
  { label: 'Repeat clients',    value: 6300  },
  { label: 'Referrals',         value: 3900  },
  { label: 'Reviews & rebooks', value: 2400  },
  { label: 'Upsells',           value: 2100  },
  { label: 'Win-backs',         value: 1800  },
];

const BAR_COLORS = [PRIMARY, ACCENT, DEEP_BLUE, MID_MINT, LIGHT, SLATE];

const TOTAL = BREAKDOWN.reduce((a, b) => a + b.value, 0); // 51,200
const MAX = Math.max(...BREAKDOWN.map(b => b.value));

const BreakdownRow = ({ b, color }) => {
  const share = Math.round((b.value / TOTAL) * 100);
  return (
    <div style={{
      background: PANEL,
      border: '1px solid rgba(226,232,240,0.7)',
      borderRadius: 10,
      padding: '10px 13px',
      display: 'flex', flexDirection: 'column', gap: 7,
    }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
        <span style={{
          flex: 1, minWidth: 0,
          fontSize: 13, fontWeight: 700, color: TEXT, letterSpacing: '-0.01em',
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{b.label}</span>
        <span style={{ fontSize: 10.5, fontWeight: 700, color: TEXT_MUTED }}>{share}%</span>
        <span style={{
          fontSize: 14, fontWeight: 800, color: TEXT, letterSpacing: '-0.015em',
        }}>{money(b.value)}</span>
      </div>
      <div style={{ height: 10, borderRadius: 6, background: `${SLATE}1f`, overflow: 'hidden' }}>
        <div style={{ width: `${(b.value / MAX) * 100}%`, height: '100%', borderRadius: 6, background: color }} />
      </div>
    </div>
  );
};

export const BigNumberHero = () => (
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
          By the Numbers
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: PRIMARY, background: `${PRIMARY}22`,
        padding: '5px 10px', borderRadius: 999,
      }}>THIS YEAR</span>
    </div>

    {/* The number — dominates the card */}
    <div style={{
      background: `${PRIMARY}0d`,
      border: `1.5px solid ${PRIMARY}2b`,
      borderRadius: 14,
      padding: '18px 20px',
      display: 'flex', flexDirection: 'column', gap: 6,
    }}>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.14em', color: TEXT_MUTED,
      }}>SAVED THIS YEAR</span>
      <div style={{ display: 'flex', alignItems: 'flex-end', gap: 12 }}>
        <span style={{
          fontSize: 76, fontWeight: 800, color: TEXT,
          letterSpacing: '-0.045em', lineHeight: 0.9,
        }}>{money(TOTAL)}</span>
        <span style={{
          marginBottom: 10,
          fontSize: 14, fontWeight: 800, color: SUCCESS,
          background: `${SUCCESS}1f`, padding: '6px 12px', borderRadius: 999,
          display: 'flex', alignItems: 'center', gap: 4,
        }}>↑ +18%</span>
      </div>
    </div>

    {/* Where it adds up — bleeds off the bottom */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 11 }}>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.10em', color: TEXT_MUTED,
      }}>WHERE IT ADDS UP</span>
      {BREAKDOWN.map((b, i) => (
        <BreakdownRow key={i} b={b} color={BAR_COLORS[i % BAR_COLORS.length]} />
      ))}
    </div>
  </div>
);

// Scheduling hero — vertical agenda stack.
//
// Master rule (see ../YouTubeThumbnail.jsx HERO UI SELECTION): thin, tall,
// single vertical stack, bleeds off the bottom. NOT a week-grid calendar
// (that would be too wide). NOT a checklist (fails the silhouette test).
// Reads as a daily agenda flowing downward forever.
//
// Reference: ../../../../src/scenes/features/SchedulerPage.tsx
// Outcome framing: clients are booking themselves in, your calendar fills
// up automatically. Each row is one booking that landed.

import React from 'react';
import { colors } from '../../theme.js';
import { Avatar } from '../../profiles.jsx';
import { ACCENT, LIGHT, PRIMARY, PRIMARY_DEEP, SUCCESS } from '../../brand.js';

const DAYS = [
  {
    label: 'Today',
    sub: 'Wed 9 Apr',
    bookings: [
      { time: '9:00',  duration: '30m', name: 'Saskia Williams',  type: 'Free Consultation',         color: PRIMARY, avatar: 'SW', status: 'confirmed' },
      { time: '11:00', duration: '45m', name: 'Otis Chen',        type: 'Workflow Audit',            color: ACCENT, avatar: 'OC', status: 'confirmed' },
      { time: '14:30', duration: '15m', name: 'Asher Patterson',  type: '15 Min Booking',            color: LIGHT, avatar: 'AP', status: 'new' },
    ],
  },
  {
    label: 'Tomorrow',
    sub: 'Thu 10 Apr',
    bookings: [
      { time: '8:30',  duration: '30m', name: 'Romy Greene',      type: 'Free Consultation',         color: PRIMARY, avatar: 'RG', status: 'confirmed' },
      { time: '10:00', duration: '45m', name: 'Hugo Daniels',     type: 'Workflow Audit',            color: ACCENT, avatar: 'HD', status: 'confirmed' },
      { time: '13:00', duration: '60m', name: 'Camille Anders',   type: 'Strategy Session',          color: SUCCESS, avatar: 'CA', status: 'new' },
      { time: '15:30', duration: '15m', name: 'Theo Reilly',      type: '15 Min Booking',            color: LIGHT, avatar: 'TR', status: 'confirmed' },
    ],
  },
  {
    label: 'Fri 11 Apr',
    sub: null,
    bookings: [
      { time: '9:00',  duration: '45m', name: 'Anya Faulkner',    type: 'Workflow Audit',            color: ACCENT, avatar: 'AF', status: 'confirmed' },
      { time: '11:30', duration: '30m', name: 'Bao Nguyen',       type: 'Free Consultation',         color: PRIMARY, avatar: 'BN', status: 'new' },
    ],
  },
];

const STATUS_PILL = {
  confirmed: { bg: 'rgba(45,184,125,0.15)',  text: SUCCESS, label: 'CONFIRMED' },
  new:       { bg: 'rgba(41,198,198,0.18)',  text: PRIMARY_DEEP, label: 'NEW' },
};

const Booking = ({ b }) => {
  const status = STATUS_PILL[b.status];
  return (
    <div style={{
      background: '#fff',
      borderRadius: 12,
      padding: '12px 14px',
      boxShadow: '0 1px 2px rgba(15,17,23,0.05), 0 0 0 1px rgba(15,17,23,0.07)',
      display: 'flex', alignItems: 'center', gap: 12,
      borderLeft: `4px solid ${b.color}`,
    }}>
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'flex-start',
        minWidth: 56, flexShrink: 0,
      }}>
        <span style={{
          fontSize: 17, fontWeight: 800, color: colors.foreground,
          letterSpacing: '-0.02em', lineHeight: 1,
        }}>{b.time}</span>
        <span style={{
          fontSize: 10, fontWeight: 700, color: colors.mutedForeground,
          letterSpacing: '0.05em', marginTop: 3,
        }}>{b.duration}</span>
      </div>
      <Avatar name={b.name} size={32} />

      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          fontSize: 14, fontWeight: 800, color: colors.foreground,
          letterSpacing: '-0.01em',
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{b.name}</div>
        <div style={{
          fontSize: 11, color: colors.mutedForeground, fontWeight: 600,
          marginTop: 1,
        }}>{b.type}</div>
      </div>
      {b.status === 'new' && (
        <span style={{
          fontSize: 9, fontWeight: 800,
          color: status.text,
          background: status.bg,
          padding: '3px 8px', borderRadius: 999,
          letterSpacing: '0.10em',
          flexShrink: 0,
        }}>{status.label}</span>
      )}
    </div>
  );
};

const DayGroup = ({ day }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
    <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, padding: '2px 4px' }}>
      <span style={{
        fontSize: 15, fontWeight: 800, color: colors.foreground,
        letterSpacing: '-0.01em',
      }}>{day.label}</span>
      {day.sub && (
        <span style={{
          fontSize: 12, fontWeight: 700, color: colors.mutedForeground,
          letterSpacing: '-0.005em',
        }}>· {day.sub}</span>
      )}
      <span style={{
        marginLeft: 'auto',
        fontSize: 10, fontWeight: 800, letterSpacing: '0.10em',
        color: colors.primary,
        background: 'rgba(41,198,198,0.14)',
        padding: '3px 9px', borderRadius: 999,
      }}>{day.bookings.length} BOOKED</span>
    </div>
    {day.bookings.map((b, i) => <Booking key={i} b={b} />)}
  </div>
);

export const SchedulingHero = () => (
  <div style={{
    background: '#fff',
    borderRadius: 18,
    padding: 18,
    boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
    display: 'flex', flexDirection: 'column', gap: 16,
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
          Bookings
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.primary,
        background: 'rgba(41,198,198,0.14)',
        padding: '5px 10px', borderRadius: 999,
      }}>LIVE</span>
    </div>

    {/* Day groups — bleeds off bottom */}
    {DAYS.map((d, i) => <DayGroup key={i} day={d} />)}
  </div>
);

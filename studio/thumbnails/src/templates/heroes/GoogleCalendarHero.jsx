// Google Calendar hero — vertical stream of calendar events mixed from
// multiple sources (Google Calendar + your CRM + Outlook), unified into
// a single timeline.
//
// Outcome framing: every meeting lives in one place. Each row shows the
// source via a colored chip so the unification is visible.

import React from 'react';
import { Avatar } from '../../profiles.jsx';
import { ACCENT, PRIMARY, SLATE, SUCCESS, TEXT, TEXT_MUTED } from '../../brand.js';

const EVENTS = [
  { day: 'Today',     time: '9:00',  duration: '30m', title: 'Discovery — Coastal Health',     attendees: ['Priya Raman','Dylan Reyes'],                       source: 'gcal',    sourceColor: PRIMARY },
  { day: 'Today',     time: '11:00', duration: '45m', title: 'Workflow Audit — Otis Chen',     attendees: ['Otis Chen','Dylan Reyes'],                           source: 'crm',      sourceColor: SUCCESS },
  { day: 'Today',     time: '14:00', duration: '60m', title: 'Internal — Sprint Review',       attendees: ['Dylan Reyes','Jordan Park','Mira Suarez'],           source: 'outlook', sourceColor: ACCENT },
  { day: 'Tomorrow',  time: '8:30',  duration: '30m', title: 'Renewal call — Hugo Daniels',    attendees: ['Hugo Daniels','Dylan Reyes'],                        source: 'gcal',    sourceColor: PRIMARY },
  { day: 'Tomorrow',  time: '10:00', duration: '15m', title: 'Quick chat — Asher Patterson',   attendees: ['Asher Patterson','Dylan Reyes'],                     source: 'crm',      sourceColor: SUCCESS },
  { day: 'Tomorrow',  time: '13:00', duration: '60m', title: 'Strategy — Camille Anders',      attendees: ['Camille Anders','Dylan Reyes'],                      source: 'gcal',    sourceColor: PRIMARY },
  { day: 'Fri 11',    time: '9:00',  duration: '45m', title: 'Anya Faulkner — Audit',          attendees: ['Anya Faulkner','Dylan Reyes','Jordan Park'],         source: 'crm',      sourceColor: SUCCESS },
  { day: 'Fri 11',    time: '11:30', duration: '30m', title: 'Doctor appt',                    attendees: ['Dylan Reyes'],                                       source: 'gcal',    sourceColor: PRIMARY, personal: true },
];

const SOURCE_LABELS = {
  gcal:    { label: 'GOOGLE',   abbr: 'G' },
  crm:     { label: 'CRM', abbr: 'CRM' },
  outlook: { label: 'OUTLOOK',  abbr: 'O' },
};

const Attendees = ({ list }) => (
  <div style={{ display: 'flex', alignItems: 'center' }}>
    {list.slice(0, 3).map((name, i) => (
      <Avatar
        key={i}
        name={name}
        size={22}
        style={{
          marginLeft: i > 0 ? -7 : 0,
          border: '2px solid #fff',
          zIndex: 3 - i,
          position: 'relative',
        }}
      />
    ))}
    {list.length > 3 && (
      <div style={{
        width: 22, height: 22, borderRadius: '50%',
        background: `${SLATE}40`,
        color: TEXT, fontSize: 9, fontWeight: 800,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        marginLeft: -7,
        border: '2px solid #fff',
      }}>+{list.length - 3}</div>
    )}
  </div>
);

const EventRow = ({ e }) => {
  const src = SOURCE_LABELS[e.source];
  return (
    <div style={{
      background: '#fff',
      borderRadius: 10,
      padding: '10px 12px',
      border: '1px solid rgba(226,232,240,0.7)',
      borderLeft: `4px solid ${e.sourceColor}`,
      display: 'flex', alignItems: 'center', gap: 12,
      opacity: e.personal ? 0.85 : 1,
    }}>
      <div style={{ minWidth: 48, flexShrink: 0 }}>
        <div style={{ fontSize: 16, fontWeight: 800, color: TEXT, letterSpacing: '-0.02em', lineHeight: 1 }}>{e.time}</div>
        <div style={{ fontSize: 10, fontWeight: 700, color: TEXT_MUTED, marginTop: 3, letterSpacing: '0.04em' }}>{e.duration}</div>
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          fontSize: 13, fontWeight: 800, color: TEXT,
          letterSpacing: '-0.01em', lineHeight: 1.2,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{e.title}</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 4 }}>
          <span style={{
            display: 'inline-flex', alignItems: 'center', gap: 4,
            fontSize: 8.5, fontWeight: 800, letterSpacing: '0.10em',
            color: e.sourceColor,
            background: `${e.sourceColor}1f`,
            padding: '2px 6px', borderRadius: 4,
          }}>{src.label}</span>
          {e.personal && (
            <span style={{
              fontSize: 8.5, fontWeight: 800, letterSpacing: '0.10em',
              color: TEXT_MUTED,
              background: `${SLATE}29`,
              padding: '2px 6px', borderRadius: 4,
            }}>PERSONAL</span>
          )}
        </div>
      </div>
      <Attendees list={e.attendees} />
    </div>
  );
};

const DayHeader = ({ label, count }) => (
  <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, padding: '4px 2px 2px 2px' }}>
    <span style={{
      fontSize: 14, fontWeight: 800, color: TEXT,
      letterSpacing: '-0.01em',
    }}>{label}</span>
    <span style={{ flex: 1, height: 1, background: 'rgba(226,232,240,0.6)' }} />
    <span style={{
      fontSize: 10, fontWeight: 800, letterSpacing: '0.10em',
      color: TEXT_MUTED,
    }}>{count}</span>
  </div>
);

export const GoogleCalendarHero = () => {
  const grouped = EVENTS.reduce((acc, e) => {
    if (!acc[e.day]) acc[e.day] = [];
    acc[e.day].push(e);
    return acc;
  }, {});
  return (
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
            boxShadow: `0 0 0 5px ${SUCCESS}38`,
          }} />
          <span style={{ fontSize: 19, fontWeight: 800, color: TEXT, letterSpacing: '-0.015em' }}>
            Calendar
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{
            fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
            color: PRIMARY,
            background: `${PRIMARY}29`,
            padding: '3px 8px', borderRadius: 999,
          }}>● GOOGLE</span>
          <span style={{
            fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
            color: SUCCESS,
            background: `${SUCCESS}29`,
            padding: '3px 8px', borderRadius: 999,
          }}>● CRM</span>
        </div>
      </div>

      {/* Event stack grouped by day */}
      {Object.entries(grouped).map(([day, events]) => (
        <div key={day} style={{ display: 'flex', flexDirection: 'column', gap: 7 }}>
          <DayHeader label={day} count={`${events.length} EVENTS`} />
          {events.map((e, i) => <EventRow key={i} e={e} />)}
        </div>
      ))}
    </div>
  );
};

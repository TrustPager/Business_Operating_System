// Stage emails hero — vertical log of stage-change → triggered-email events.
//
// Outcome framing: deals move stages, the matching follow-up email fires
// itself. Each row is a "stage moved → email sent → delivered" beat.

import React from 'react';
import { colors } from '../../theme.js';
import { ACCENT, PRIMARY, PRIMARY_DEEP, SUCCESS } from '../../brand.js';

const EVENTS = [
  {
    deal: 'Coastal Health Group',
    from: 'Discovery Call',
    to: 'Proposal Sent',
    toColor: ACCENT,
    template: 'Quote Ready — Next Steps',
    recipient: 'Sarah Hartley',
    when: '2 min ago',
    status: 'opened',
  },
  {
    deal: 'Wattle Creek Winery',
    from: 'Proposal Sent',
    to: 'Negotiation',
    toColor: SUCCESS,
    template: 'Welcome to Negotiation',
    recipient: 'Hugo Daniels',
    when: '14 min ago',
    status: 'opened',
  },
  {
    deal: 'Pinnacle Engineering',
    from: 'Discovery Call',
    to: 'Proposal Sent',
    toColor: ACCENT,
    template: 'Quote Ready — Next Steps',
    recipient: 'Theo Reilly',
    when: '1 hour ago',
    status: 'delivered',
  },
  {
    deal: 'Outback Solar',
    from: 'New Enquiry',
    to: 'Discovery Call',
    toColor: PRIMARY,
    template: 'Discovery Booking Link',
    recipient: 'Otis Chen',
    when: '3 hours ago',
    status: 'replied',
  },
  {
    deal: 'Southern Cross Legal',
    from: 'Negotiation',
    to: 'Won',
    toColor: SUCCESS,
    template: 'Welcome Aboard 🎉',
    recipient: 'Anya Faulkner',
    when: 'Yesterday',
    status: 'opened',
  },
  {
    deal: 'Eucalyptus Wealth',
    from: 'New Enquiry',
    to: 'Discovery Call',
    toColor: PRIMARY,
    template: 'Discovery Booking Link',
    recipient: 'Camille Anders',
    when: 'Yesterday',
    status: 'delivered',
  },
  {
    deal: 'Reef & Co Logistics',
    from: 'Quote Sent',
    to: 'Negotiation',
    toColor: SUCCESS,
    template: 'Refining the Scope',
    recipient: 'Mateo Suarez',
    when: '2 days ago',
    status: 'opened',
  },
];

const STATUS = {
  delivered: { fg: PRIMARY_DEEP, bg: 'rgba(41,198,198,0.16)', label: '✓ DELIVERED' },
  opened:    { fg: SUCCESS, bg: 'rgba(45,184,125,0.16)', label: '✓ OPENED' },
  replied:   { fg: SUCCESS, bg: 'rgba(45,184,125,0.22)', label: '✓ REPLIED' },
};

const EventCard = ({ e }) => {
  const s = STATUS[e.status];
  return (
    <div style={{
      background: '#fff',
      borderRadius: 11,
      padding: '12px 14px',
      border: '1px solid rgba(226,232,240,0.7)',
      display: 'flex', flexDirection: 'column', gap: 8,
    }}>
      {/* Stage chip transition */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
        <span style={{
          fontSize: 14, fontWeight: 800, color: colors.foreground,
          letterSpacing: '-0.01em', flex: 1, minWidth: 0,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{e.deal}</span>
        <span style={{ fontSize: 10, fontWeight: 600, color: colors.mutedForeground }}>{e.when}</span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        <span style={{
          fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
          color: colors.mutedForeground,
          background: 'rgba(148,163,184,0.18)',
          padding: '3px 7px', borderRadius: 4,
        }}>{e.from.toUpperCase()}</span>
        <span style={{ fontSize: 11, color: colors.mutedForeground }}>→</span>
        <span style={{
          fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
          color: e.toColor,
          background: `${e.toColor}1f`,
          padding: '3px 7px', borderRadius: 4,
        }}>{e.to.toUpperCase()}</span>
      </div>

      {/* Email fired row */}
      <div style={{
        background: 'rgba(248,250,252,0.7)',
        borderRadius: 8,
        padding: '8px 10px',
        display: 'flex', alignItems: 'center', gap: 10,
        border: '1px solid rgba(226,232,240,0.5)',
      }}>
        <div style={{
          width: 24, height: 24, borderRadius: 6,
          background: 'rgba(41,198,198,0.16)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          color: PRIMARY_DEEP, fontSize: 12, fontWeight: 800,
          flexShrink: 0,
        }}>✉</div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{
            fontSize: 11.5, fontWeight: 800, color: colors.foreground,
            letterSpacing: '-0.005em',
            overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
          }}>{e.template}</div>
          <div style={{
            fontSize: 10, fontWeight: 600, color: colors.mutedForeground,
            marginTop: 1,
          }}>→ {e.recipient}</div>
        </div>
        <span style={{
          fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
          color: s.fg, background: s.bg,
          padding: '3px 7px', borderRadius: 999,
          flexShrink: 0,
        }}>{s.label}</span>
      </div>
    </div>
  );
};

export const StageEmailsHero = () => (
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
          Auto-Sent Emails
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.primary,
        background: 'rgba(41,198,198,0.14)',
        padding: '5px 10px', borderRadius: 999,
      }}>SENT AUTOMATICALLY</span>
    </div>

    {/* Event card stack */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 9 }}>
      {EVENTS.map((e, i) => <EventCard key={i} e={e} />)}
    </div>
  </div>
);

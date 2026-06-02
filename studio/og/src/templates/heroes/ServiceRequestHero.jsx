// Service Request hero — vertical stack of completed/shipped requests.
//
// Outcome framing: requests you've made were SHIPPED. Each card is
// proof of work delivered. The single pending request at the top shows
// the loop is still open (you can submit more anytime).

import React from 'react';
import { colors } from '../../theme.js';

const REQUESTS = [
  {
    title: 'Auto-decline conflicting bookings',
    desc: 'When two bookings overlap, decline the lower-priority one and notify the client.',
    state: 'building',
    eta: 'ETA Friday',
  },
  {
    title: 'SMS auto-reply after-hours',
    desc: "Reply with hours + booking link if a text lands after 6pm.",
    state: 'shipped',
    when: 'Live · 2 days ago',
  },
  {
    title: 'Weekly revenue digest',
    desc: 'Monday 9am summary email with last week\'s deals, won amount, and trend.',
    state: 'shipped',
    when: 'Live · 5 days ago',
  },
  {
    title: 'Auto-archive paid invoices',
    desc: "Once an invoice is fully paid, archive the file and notify the deal owner.",
    state: 'shipped',
    when: 'Live · 1 week ago',
  },
  {
    title: 'Slack alert on new lead',
    desc: 'Post to #sales when a form submission scores above the qualification threshold.',
    state: 'shipped',
    when: 'Live · 2 weeks ago',
  },
  {
    title: 'Calendar sync filter',
    desc: 'Only sync events tagged "Client" to TrustPager — keep personal blocks private.',
    state: 'shipped',
    when: 'Live · 3 weeks ago',
  },
];

const StateBadge = ({ state, when, eta }) => {
  if (state === 'shipped') {
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <span style={{
          fontSize: 10, fontWeight: 800, letterSpacing: '0.10em',
          color: 'var(--brand-secondary)',
          background: 'color-mix(in srgb, var(--brand-secondary) 16%, transparent)',
          padding: '3px 9px', borderRadius: 999,
          display: 'flex', alignItems: 'center', gap: 4,
        }}>✓ SHIPPED</span>
        <span style={{ fontSize: 11, fontWeight: 600, color: colors.mutedForeground }}>{when}</span>
      </div>
    );
  }
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <span style={{
        fontSize: 10, fontWeight: 800, letterSpacing: '0.10em',
        color: 'var(--brand-primary-deep)',
        background: 'color-mix(in srgb, var(--brand-primary) 16%, transparent)',
        padding: '3px 9px', borderRadius: 999,
      }}>● BUILDING</span>
      <span style={{ fontSize: 11, fontWeight: 600, color: colors.mutedForeground }}>{eta}</span>
    </div>
  );
};

const RequestCard = ({ r }) => (
  <div style={{
    background: '#fff',
    borderRadius: 12,
    padding: '14px 16px',
    border: '1px solid rgba(226,232,240,0.7)',
    display: 'flex', flexDirection: 'column', gap: 8,
    borderLeft: r.state === 'shipped' ? '4px solid var(--brand-secondary)' : '4px solid var(--brand-primary)',
  }}>
    <StateBadge state={r.state} when={r.when} eta={r.eta} />
    <div style={{
      fontSize: 15, fontWeight: 800, color: colors.foreground,
      letterSpacing: '-0.015em', lineHeight: 1.2,
    }}>{r.title}</div>
    <div style={{
      fontSize: 12, color: colors.mutedForeground, fontWeight: 500,
      lineHeight: 1.4,
    }}>{r.desc}</div>
  </div>
);

export const ServiceRequestHero = () => (
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
          background: 'var(--brand-secondary)',
          boxShadow: '0 0 0 5px color-mix(in srgb, var(--brand-secondary) 22%, transparent)',
        }} />
        <span style={{ fontSize: 19, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.015em' }}>
          Your Requests
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.primary,
        background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
        padding: '5px 10px', borderRadius: 999,
      }}>5 SHIPPED</span>
    </div>

    {/* Request stack */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      {REQUESTS.map((r, i) => <RequestCard key={i} r={r} />)}
    </div>
  </div>
);

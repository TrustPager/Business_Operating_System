// Contacts hero — vertical stack of rich contact cards.
//
// Outcome framing: every client comes with the full picture pre-loaded —
// who they work for, recent activity, deal value, contact freshness.

import React from 'react';
import { colors } from '../../theme.js';
import { Avatar } from '../../profiles.jsx';

const CONTACTS = [
  {
    name: 'Sarah Hartley',
    role: 'CFO',
    company: 'Coastal Consulting',
    companyColor: 'var(--brand-primary)',
    avatar: 'SH', avatarColor: 'var(--brand-primary)',
    activity: 'Replied to your email · 2h ago',
    activityColor: 'var(--brand-secondary)',
    tags: ['Decision Maker', 'Hot Lead'],
  },
  {
    name: 'James Mitchell',
    role: 'Director',
    company: 'Coastal Health Group',
    companyColor: 'var(--brand-accent)',
    avatar: 'JM', avatarColor: 'var(--brand-accent)',
    activity: 'Booked discovery · 4h ago',
    activityColor: 'var(--brand-secondary)',
    tags: ['Board Approval Needed'],
  },
  {
    name: 'Hugo Daniels',
    role: 'Ops Manager',
    company: 'Wattle Creek Winery',
    companyColor: 'var(--brand-light)',
    avatar: 'HD', avatarColor: 'var(--brand-light)',
    activity: 'Sent SMS · yesterday',
    activityColor: 'var(--brand-primary)',
    tags: ['Renewal'],
  },
  {
    name: 'Camille Anders',
    role: 'Founder',
    company: 'Eucalyptus Wealth',
    companyColor: 'var(--brand-secondary)',
    avatar: 'CA', avatarColor: 'var(--brand-secondary)',
    activity: 'Form submitted · 2 days ago',
    activityColor: 'var(--brand-primary-deep)',
    tags: ['Inbound', 'High Value'],
  },
  {
    name: 'Theo Reilly',
    role: 'Procurement',
    company: 'Pinnacle Engineering',
    companyColor: 'var(--brand-primary-deep)',
    avatar: 'TR', avatarColor: 'var(--brand-primary-deep)',
    activity: 'Quote sent · 3 days ago',
    activityColor: 'var(--brand-primary)',
    tags: ['Comparing Vendors'],
  },
  {
    name: 'Anya Faulkner',
    role: 'GM',
    company: 'Southern Cross Legal',
    companyColor: 'var(--brand-accent)',
    avatar: 'AF', avatarColor: 'var(--brand-accent)',
    activity: 'Logged a call · 5 days ago',
    activityColor: 'var(--brand-primary-deep)',
    tags: ['Long-Term Client'],
  },
];

const ContactCard = ({ c }) => (
  <div style={{
    background: '#fff',
    borderRadius: 12,
    padding: '14px 16px',
    border: '1px solid rgba(226,232,240,0.7)',
    display: 'flex', flexDirection: 'column', gap: 9,
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
      <Avatar name={c.name} size={42} style={{ boxShadow: '0 2px 6px rgba(15,17,23,0.15)' }} />
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          fontSize: 15, fontWeight: 800, color: colors.foreground,
          letterSpacing: '-0.01em',
        }}>{c.name}</div>
        <div style={{
          fontSize: 11, fontWeight: 600, color: colors.mutedForeground,
          marginTop: 1,
        }}>{c.role}</div>
      </div>
    </div>

    {/* Company chip */}
    <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
      <span style={{
        display: 'inline-flex', alignItems: 'center', gap: 5,
        fontSize: 11, fontWeight: 700, color: colors.foreground,
        background: 'rgba(248,250,252,0.9)',
        border: `1px solid ${`color-mix(in srgb, ${c.companyColor} 25%, transparent)`}`,
        padding: '3px 8px', borderRadius: 6,
        letterSpacing: '-0.005em',
      }}>
        <span style={{ width: 6, height: 6, borderRadius: 2, background: c.companyColor }} />
        {c.company}
      </span>
      {c.tags.map((t, i) => (
        <span key={i} style={{
          fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
          color: colors.mutedForeground,
          background: 'rgba(148,163,184,0.18)',
          padding: '3px 7px', borderRadius: 999,
          textTransform: 'uppercase',
        }}>{t}</span>
      ))}
    </div>

    {/* Activity line */}
    <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
      <span style={{
        width: 6, height: 6, borderRadius: '50%',
        background: c.activityColor, flexShrink: 0,
      }} />
      <span style={{
        fontSize: 11, fontWeight: 600, color: colors.mutedForeground,
        letterSpacing: '-0.005em',
      }}>{c.activity}</span>
    </div>
  </div>
);

export const ContactsHero = () => (
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
          Contacts
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.primary,
        background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
        padding: '5px 10px', borderRadius: 999,
      }}>1,247 LOGGED</span>
    </div>

    {/* Card stack */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      {CONTACTS.map((c, i) => <ContactCard key={i} c={c} />)}
    </div>
  </div>
);

// Contacts hero — vertical stack of rich contact cards.
//
// Outcome framing: every client comes with the full picture pre-loaded —
// who they work for, recent activity, deal value, contact freshness.

import React from 'react';
import { Avatar } from '../../profiles.jsx';
import { ACCENT, LIGHT, PRIMARY, PRIMARY_DEEP, SLATE, SUCCESS, TEXT, TEXT_MUTED } from '../../brand.js';

const CONTACTS = [
  {
    name: 'Sarah Hartley',
    role: 'CFO',
    company: 'Coastal Consulting',
    companyColor: PRIMARY,
    avatar: 'SH', avatarColor: PRIMARY,
    activity: 'Replied to your email · 2h ago',
    activityColor: SUCCESS,
    tags: ['Decision Maker', 'Hot Lead'],
  },
  {
    name: 'James Mitchell',
    role: 'Director',
    company: 'Coastal Health Group',
    companyColor: ACCENT,
    avatar: 'JM', avatarColor: ACCENT,
    activity: 'Booked discovery · 4h ago',
    activityColor: SUCCESS,
    tags: ['Board Approval Needed'],
  },
  {
    name: 'Hugo Daniels',
    role: 'Ops Manager',
    company: 'Wattle Creek Winery',
    companyColor: LIGHT,
    avatar: 'HD', avatarColor: LIGHT,
    activity: 'Sent SMS · yesterday',
    activityColor: PRIMARY,
    tags: ['Renewal'],
  },
  {
    name: 'Camille Anders',
    role: 'Founder',
    company: 'Eucalyptus Wealth',
    companyColor: SUCCESS,
    avatar: 'CA', avatarColor: SUCCESS,
    activity: 'Form submitted · 2 days ago',
    activityColor: PRIMARY_DEEP,
    tags: ['Inbound', 'High Value'],
  },
  {
    name: 'Theo Reilly',
    role: 'Procurement',
    company: 'Pinnacle Engineering',
    companyColor: PRIMARY_DEEP,
    avatar: 'TR', avatarColor: PRIMARY_DEEP,
    activity: 'Quote sent · 3 days ago',
    activityColor: PRIMARY,
    tags: ['Comparing Vendors'],
  },
  {
    name: 'Anya Faulkner',
    role: 'GM',
    company: 'Southern Cross Legal',
    companyColor: ACCENT,
    avatar: 'AF', avatarColor: ACCENT,
    activity: 'Logged a call · 5 days ago',
    activityColor: PRIMARY_DEEP,
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
          fontSize: 15, fontWeight: 800, color: TEXT,
          letterSpacing: '-0.01em',
        }}>{c.name}</div>
        <div style={{
          fontSize: 11, fontWeight: 600, color: TEXT_MUTED,
          marginTop: 1,
        }}>{c.role}</div>
      </div>
    </div>

    {/* Company chip */}
    <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
      <span style={{
        display: 'inline-flex', alignItems: 'center', gap: 5,
        fontSize: 11, fontWeight: 700, color: TEXT,
        background: 'rgba(248,250,252,0.9)',
        border: `1px solid ${c.companyColor}40`,
        padding: '3px 8px', borderRadius: 6,
        letterSpacing: '-0.005em',
      }}>
        <span style={{ width: 6, height: 6, borderRadius: 2, background: c.companyColor }} />
        {c.company}
      </span>
      {c.tags.map((t, i) => (
        <span key={i} style={{
          fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
          color: TEXT_MUTED,
          background: `${SLATE}2e`,
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
        fontSize: 11, fontWeight: 600, color: TEXT_MUTED,
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
          background: SUCCESS,
          boxShadow: `0 0 0 5px ${SUCCESS}38`,
        }} />
        <span style={{ fontSize: 19, fontWeight: 800, color: TEXT, letterSpacing: '-0.015em' }}>
          Contacts
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: PRIMARY,
        background: `${PRIMARY}24`,
        padding: '5px 10px', borderRadius: 999,
      }}>1,247 LOGGED</span>
    </div>

    {/* Card stack */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      {CONTACTS.map((c, i) => <ContactCard key={i} c={c} />)}
    </div>
  </div>
);

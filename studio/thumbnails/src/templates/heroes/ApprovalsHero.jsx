// Approvals hero — vertical stack of approval cards.
//
// Outcome framing: AI checked in with you before acting. Most have been
// approved + executed; one is currently waiting on your call.

import React from 'react';
import { colors } from '../../theme.js';
import { PRIMARY, SLATE, SUCCESS } from '../../brand.js';

const APPROVALS = [
  {
    state: 'pending',
    icon: '✉',
    iconColor: PRIMARY,
    title: 'Send quote to Selene W.',
    detail: '$48k · Southern Cross Legal',
    requested: 'Just now',
  },
  {
    state: 'approved',
    icon: '✉',
    iconColor: SUCCESS,
    title: 'Sent quote to Mira S.',
    detail: '$96k · Coastal Health Group',
    requested: '2m ago',
  },
  {
    state: 'approved',
    icon: '📅',
    iconColor: SUCCESS,
    title: 'Booked Kai O. for Thursday',
    detail: 'Workflow Audit · 45m',
    requested: '15m ago',
  },
  {
    state: 'approved',
    icon: '💬',
    iconColor: SUCCESS,
    title: 'Sent SMS reminder to 24 leads',
    detail: 'Stage: Discovery Call',
    requested: '1h ago',
  },
  {
    state: 'approved',
    icon: '↦',
    iconColor: SUCCESS,
    title: 'Moved Ezra B. to Negotiation',
    detail: 'Auto-staged from Proposal Sent',
    requested: '3h ago',
  },
  {
    state: 'rejected',
    icon: '✉',
    iconColor: SLATE,
    title: 'Bulk email to all dormant leads',
    detail: '418 recipients · cold list',
    requested: 'Yesterday',
  },
];

const ActionRow = ({ state }) => {
  if (state === 'pending') {
    return (
      <div style={{ display: 'flex', gap: 8, marginTop: 4 }}>
        <button style={{
          flex: 1,
          background: `linear-gradient(135deg, #2db87d, #29c6c6)`,
          color: '#fff',
          fontSize: 12, fontWeight: 800,
          padding: '8px 0', borderRadius: 8,
          border: 'none',
          letterSpacing: '-0.005em',
          boxShadow: '0 2px 6px rgba(45,184,125,0.30)',
        }}>✓ Approve</button>
        <button style={{
          flex: 1,
          background: '#fff',
          color: colors.mutedForeground,
          fontSize: 12, fontWeight: 700,
          padding: '8px 0', borderRadius: 8,
          border: '1px solid rgba(148,163,184,0.3)',
        }}>Reject</button>
      </div>
    );
  }
  if (state === 'approved') {
    return (
      <div style={{
        display: 'inline-flex', alignItems: 'center', gap: 6,
        fontSize: 10, fontWeight: 800, letterSpacing: '0.10em',
        color: SUCCESS,
        background: 'rgba(45,184,125,0.14)',
        padding: '4px 9px', borderRadius: 999,
        alignSelf: 'flex-start',
      }}>✓ APPROVED & EXECUTED</div>
    );
  }
  return (
    <div style={{
      display: 'inline-flex', alignItems: 'center', gap: 6,
      fontSize: 10, fontWeight: 800, letterSpacing: '0.10em',
      color: colors.mutedForeground,
      background: 'rgba(148,163,184,0.18)',
      padding: '4px 9px', borderRadius: 999,
      alignSelf: 'flex-start',
    }}>✕ REJECTED</div>
  );
};

const ApprovalCard = ({ a }) => (
  <div style={{
    background: '#fff',
    borderRadius: 12,
    padding: '12px 14px',
    border: a.state === 'pending'
      ? '1.5px solid rgba(41,198,198,0.45)'
      : '1px solid rgba(226,232,240,0.7)',
    boxShadow: a.state === 'pending'
      ? '0 4px 14px rgba(41,198,198,0.18)'
      : 'none',
    display: 'flex', flexDirection: 'column', gap: 8,
    opacity: a.state === 'rejected' ? 0.7 : 1,
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
      <div style={{
        width: 30, height: 30, borderRadius: 9,
        background: `${a.iconColor}1f`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0,
        fontSize: 15,
      }}>
        <span style={{ color: a.iconColor, fontWeight: 800 }}>{a.icon}</span>
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          fontSize: 13.5, fontWeight: 800, color: colors.foreground,
          letterSpacing: '-0.01em', lineHeight: 1.2,
          textDecoration: a.state === 'rejected' ? 'line-through' : 'none',
        }}>{a.title}</div>
        <div style={{
          fontSize: 11, color: colors.mutedForeground, fontWeight: 600,
          marginTop: 2,
        }}>{a.detail} · {a.requested}</div>
      </div>
    </div>
    <ActionRow state={a.state} />
  </div>
);

export const ApprovalsHero = () => (
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
          Pending Approvals
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.primary,
        background: 'rgba(41,198,198,0.14)',
        padding: '5px 10px', borderRadius: 999,
      }}>1 PENDING</span>
    </div>

    {/* Approval stack */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      {APPROVALS.map((a, i) => <ApprovalCard key={i} a={a} />)}
    </div>
  </div>
);

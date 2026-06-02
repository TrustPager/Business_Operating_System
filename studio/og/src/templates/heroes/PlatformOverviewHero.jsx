// PlatformOverviewHero — vertical stack of TrustPager product tiles.
// Outcome framing: each row is ONE tool. Stack of 9-10 tools bleeds off
// the bottom. The viewer reads "this platform replaces all my SaaS subs".
//
// Brand-aware via CSS variables. Each tool tile's accent rotates
// through --brand-primary / --brand-secondary / --brand-accent /
// --brand-light / --brand-primary-deep. A future FinalPiece overview
// page reusing this hero renders in FinalPiece colours automatically.
//
// Family pattern: CARD STACK.

import React from 'react';
import { colors } from '../../theme.js';
function buildTools() {
  return [
    { name: 'Pipeline',          desc: 'Manage every deal end-to-end',         icon: '▦',  color: 'var(--brand-primary)' },
    { name: 'Automations',       desc: 'Workflows that run themselves',         icon: '⚡', color: 'var(--brand-accent)' },
    { name: 'Email',             desc: 'Send & track from inside the CRM',      icon: '✉',  color: 'var(--brand-secondary)' },
    { name: 'SMS',               desc: 'Conversational messaging built in',     icon: '💬', color: 'var(--brand-light)' },
    { name: 'AI Voice Agents',   desc: 'Answer every call 24/7',                icon: '🎙', color: 'var(--brand-primary-deep)' },
    { name: 'Online Booking',    desc: 'Clients self-serve their own time',     icon: '📅', color: 'var(--brand-primary)' },
    { name: 'E-Signing',         desc: 'Digital signatures, no DocuSign',       icon: '✎',  color: 'var(--brand-accent)' },
    { name: 'Forms',             desc: 'Custom forms that auto-fill the CRM',   icon: '☐',  color: 'var(--brand-secondary)' },
    { name: 'Proposals',         desc: 'AI-generated docs, ready to send',      icon: '📄', color: 'var(--brand-light)' },
  ];
}

const ToolRow = ({ t }) => (
  <div style={{
    display: 'flex', alignItems: 'center', gap: 12,
    padding: '10px 4px',
    borderBottom: '1px solid rgba(226,232,240,0.7)',
  }}>
    <div style={{
      width: 36, height: 36, borderRadius: 10,
      background: `linear-gradient(135deg, ${t.color} 0%, ${`color-mix(in srgb, ${t.color} 80%, transparent)`} 100%)`,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontSize: 16, color: '#fff', fontWeight: 800,
      flexShrink: 0,
      boxShadow: `0 4px 10px ${`color-mix(in srgb, ${t.color} 20%, transparent)`}`,
    }}>{t.icon}</div>
    <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', gap: 1 }}>
      <div style={{
        fontSize: 14, fontWeight: 800, color: colors.foreground,
        letterSpacing: '-0.015em',
      }}>{t.name}</div>
      <div style={{
        fontSize: 11, fontWeight: 500, color: colors.mutedForeground,
        letterSpacing: '-0.005em',
      }}>{t.desc}</div>
    </div>
    <div style={{
      fontSize: 9, fontWeight: 800, letterSpacing: '0.1em',
      color: 'var(--brand-secondary)', background: 'color-mix(in srgb, var(--brand-secondary) 12%, transparent)',
      padding: '4px 8px', borderRadius: 999,
    }}>BUILT IN</div>
  </div>
);

export const PlatformOverviewHero = () => {
  const tools = buildTools();
  return (
    <div style={{
      background: '#fff',
      borderRadius: 18,
      padding: 18,
      boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
      display: 'flex', flexDirection: 'column', gap: 4,
    }}>
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '4px 6px 12px',
        borderBottom: '1px solid rgba(226,232,240,0.7)',
        marginBottom: 4,
      }}>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8,
          fontSize: 16, fontWeight: 800, color: colors.foreground,
          letterSpacing: '-0.015em',
        }}>
          <div style={{
            width: 10, height: 10, borderRadius: '50%',
            background: 'var(--brand-primary)', boxShadow: `0 0 0 5px ${'color-mix(in srgb, var(--brand-primary) 22%, transparent)'}`,
          }} />
          Your Platform
        </div>
        <div style={{
          fontSize: 10, fontWeight: 800, letterSpacing: '0.12em',
          color: 'var(--brand-primary)', background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
          padding: '5px 10px', borderRadius: 999,
        }}>20 TOOLS</div>
      </div>
      {tools.map((t, i) => <ToolRow key={i} t={t} />)}
    </div>
  );
};

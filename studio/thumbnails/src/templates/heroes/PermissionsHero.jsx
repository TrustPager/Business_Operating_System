// Permissions hero — the scope grid iconic to a role-based permissions
// system. Resources down the left, action columns across the
// top (Read / Write / Send / Delete), filled checkboxes per intersection.
//
// Reference: ../../../../src/scenes/features/RoleDetailPage.tsx +
// ../../../../src/data/permission-scopes.ts
//
// Outcome framing: the role is configured, the matrix shows exactly
// what's allowed. Reads as "your data is locked down by role".

import React from 'react';
import { colors } from '../../theme.js';
import { ACCENT, PRIMARY, PRIMARY_DEEP, SUCCESS } from '../../brand.js';

const ACTIONS = ['Read', 'Write', 'Send', 'Delete'];

const SECTIONS = [
  {
    label: 'CRM DATA',
    color: PRIMARY,
    resources: [
      { name: 'Contacts',      allowed: ['Read', 'Write'],          available: ['Read', 'Write', 'Delete'] },
      { name: 'Opportunities', allowed: ['Read', 'Write'],          available: ['Read', 'Write', 'Delete'] },
      { name: 'Companies',     allowed: ['Read', 'Write'],          available: ['Read', 'Write', 'Delete'] },
      { name: 'Tasks',         allowed: ['Read', 'Write'],          available: ['Read', 'Write', 'Delete'] },
      { name: 'Pipelines',     allowed: ['Read'],                   available: ['Read', 'Write', 'Delete'] },
    ],
  },
  {
    label: 'COMMUNICATION',
    color: ACCENT,
    resources: [
      { name: 'Email',         allowed: ['Read', 'Send'],           available: ['Read', 'Send'] },
      { name: 'SMS',           allowed: ['Read', 'Send'],           available: ['Read', 'Send'] },
      { name: 'Voice Agents',  allowed: ['Read'],                   available: ['Read', 'Send'] },
    ],
  },
  {
    label: 'AUTOMATIONS',
    color: SUCCESS,
    resources: [
      { name: 'Automations',   allowed: ['Read'],                   available: ['Read', 'Write', 'Delete'] },
      { name: 'Event Queues',  allowed: ['Read'],                   available: ['Read', 'Write', 'Delete'] },
    ],
  },
];

const Check = ({ on, off }) => {
  if (off) {
    // Capability not available — render a dash
    return <span style={{ color: 'rgba(148,163,184,0.40)', fontSize: 14, fontWeight: 700 }}>—</span>;
  }
  if (on) {
    return (
      <div style={{
        width: 20, height: 20, borderRadius: 5,
        background: 'linear-gradient(135deg, #29c6c6, #47a3d9)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        color: '#fff', fontSize: 11, fontWeight: 800,
        boxShadow: '0 2px 5px rgba(41,198,198,0.35)',
      }}>✓</div>
    );
  }
  return (
    <div style={{
      width: 20, height: 20, borderRadius: 5,
      background: '#fff',
      border: '1.5px solid rgba(148,163,184,0.40)',
    }} />
  );
};

const SectionLabel = ({ label, color, count }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '4px 2px 6px 2px' }}>
    <span style={{ width: 6, height: 6, borderRadius: '50%', background: color }} />
    <span style={{
      fontSize: 10.5, fontWeight: 800, letterSpacing: '0.10em',
      color,
    }}>{label}</span>
    <span style={{ flex: 1, height: 1, background: `${color}22` }} />
    <span style={{
      fontSize: 10, fontWeight: 800, letterSpacing: '0.08em',
      color: colors.mutedForeground,
    }}>{count}</span>
  </div>
);

const ColumnHeader = () => (
  <div style={{
    display: 'grid',
    gridTemplateColumns: '1fr 44px 44px 44px 44px',
    alignItems: 'center', gap: 0,
    padding: '8px 12px',
    background: 'rgba(248,250,252,0.7)',
    borderRadius: 8,
    border: '1px solid rgba(226,232,240,0.7)',
  }}>
    <span style={{
      fontSize: 10, fontWeight: 800, letterSpacing: '0.10em',
      color: colors.mutedForeground,
    }}>RESOURCE</span>
    {ACTIONS.map(a => (
      <div key={a} style={{ textAlign: 'center' }}>
        <span style={{
          fontSize: 10, fontWeight: 800, letterSpacing: '0.08em',
          color: colors.mutedForeground,
        }}>{a.toUpperCase()}</span>
      </div>
    ))}
  </div>
);

const ResourceRow = ({ r, last }) => (
  <div style={{
    display: 'grid',
    gridTemplateColumns: '1fr 44px 44px 44px 44px',
    alignItems: 'center',
    padding: '10px 12px',
    borderBottom: last ? 'none' : '1px solid rgba(226,232,240,0.55)',
  }}>
    <span style={{
      fontSize: 13, fontWeight: 700, color: colors.foreground,
      letterSpacing: '-0.005em',
    }}>{r.name}</span>
    {ACTIONS.map(a => {
      const isAvailable = r.available.includes(a);
      const isAllowed = r.allowed.includes(a);
      return (
        <div key={a} style={{ display: 'flex', justifyContent: 'center' }}>
          <Check on={isAllowed} off={!isAvailable} />
        </div>
      );
    })}
  </div>
);

const Section = ({ section }) => (
  <div>
    <SectionLabel label={section.label} color={section.color} count={`${section.resources.length} RESOURCES`} />
    <div style={{
      background: '#fff',
      borderRadius: 10,
      border: '1px solid rgba(226,232,240,0.7)',
      overflow: 'hidden',
    }}>
      {section.resources.map((r, i) => (
        <ResourceRow key={r.name} r={r} last={i === section.resources.length - 1} />
      ))}
    </div>
  </div>
);

// Shield icon for the role header
const ShieldIcon = () => (
  <div style={{
    width: 42, height: 42, borderRadius: 12,
    background: 'linear-gradient(135deg, #29c6c6, #47a3d9)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    flexShrink: 0,
    boxShadow: '0 4px 10px rgba(41,198,198,0.30)',
  }}>
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
      <path d="M12 2L4 5v6c0 5.55 3.84 10.74 8 12 4.16-1.26 8-6.45 8-12V5l-8-3z" fill="#fff" />
      <path d="M9.5 12.5l2 2 4-4" stroke={PRIMARY_DEEP} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  </div>
);

export const PermissionsHero = () => (
  <div style={{
    background: '#fff',
    borderRadius: 18,
    padding: 18,
    boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
    display: 'flex', flexDirection: 'column', gap: 14,
  }}>
    {/* Role header */}
    <div style={{
      background: 'linear-gradient(135deg, rgba(41,198,198,0.10), rgba(71,163,217,0.10))',
      borderRadius: 12,
      padding: '12px 14px',
      border: '1px solid rgba(41,198,198,0.20)',
      display: 'flex', alignItems: 'center', gap: 12,
    }}>
      <ShieldIcon />
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          fontSize: 10.5, fontWeight: 800, letterSpacing: '0.10em',
          color: PRIMARY_DEEP,
        }}>ROLE · 6 USERS</div>
        <div style={{
          fontSize: 17, fontWeight: 800, color: colors.foreground,
          letterSpacing: '-0.015em', marginTop: 2,
        }}>Sales Rep</div>
        <div style={{
          fontSize: 11.5, fontWeight: 600, color: colors.mutedForeground,
          marginTop: 1, letterSpacing: '-0.005em',
        }}>Own deals, send communications, no destructive actions</div>
      </div>
      <span style={{
        display: 'inline-flex', alignItems: 'center', gap: 4,
        fontSize: 10, fontWeight: 800, letterSpacing: '0.10em',
        color: '#fff',
        background: 'linear-gradient(135deg, #2db87d, #29c6c6)',
        padding: '4px 10px', borderRadius: 999,
        boxShadow: '0 2px 6px rgba(45,184,125,0.30)',
        flexShrink: 0,
      }}>18 SCOPES ON</span>
    </div>

    {/* Column header */}
    <ColumnHeader />

    {/* Scope grid sections */}
    {SECTIONS.map((section, i) => <Section key={i} section={section} />)}
  </div>
);

// Forms hero — vertical field stack of a Client Intake form filling itself
// from a form submission. Each row is one field with the value already
// auto-filled, sparkle pill showing "auto-filled" provenance, and a
// progress bar at the bottom.
//
// Outcome framing: the form was submitted, the CRM populated itself.
// Not the form builder.

import React from 'react';
import { colors } from '../../theme.js';

const FIELDS = [
  { label: 'Company Name',     value: 'Coastal Health Group',           type: 'text',   autoFilled: true },
  { label: 'Industry',         value: 'Healthcare',                     type: 'select', autoFilled: true },
  { label: 'Primary Contact',  value: 'Dr Sarah Mitchell',              type: 'text',   autoFilled: true },
  { label: 'Role',             value: 'CFO',                            type: 'text',   autoFilled: true },
  { label: 'Email',            value: 'sarah@coastalhealthgroup.com.au', type: 'email', autoFilled: true },
  { label: 'Phone',            value: '+61 412 345 678',                type: 'phone',  autoFilled: true },
  { label: 'Team Size',        value: '22 employees',                   type: 'select', autoFilled: true },
  { label: 'Annual Revenue',   value: '$2.4M – $5M',                    type: 'select', autoFilled: true },
  { label: 'Use Cases',        value: ['Patient CRM', 'Referrals', 'Automation'], type: 'multi', autoFilled: true },
  { label: 'Budget',           value: '$50k – $100k',                   type: 'select', autoFilled: true, isFilling: true },
  { label: 'Timeline',         value: '',                               type: 'select', autoFilled: false },
];

const Sparkle = () => (
  <span style={{
    width: 18, height: 18, borderRadius: 6,
    background: 'linear-gradient(135deg, #29c6c6, #47a3d9)',
    display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
    color: '#fff', fontSize: 10, fontWeight: 800,
    flexShrink: 0,
    boxShadow: '0 2px 6px rgba(41,198,198,0.30)',
  }}>✦</span>
);

const FieldRow = ({ f }) => {
  const empty = !f.autoFilled;
  const filling = f.isFilling;
  const isMulti = f.type === 'multi';
  return (
    <div style={{
      background: empty ? 'rgba(248,250,252,0.6)' : '#fff',
      borderRadius: 10,
      padding: '10px 12px',
      border: filling
        ? '1.5px solid rgba(41,198,198,0.50)'
        : (empty ? '1px dashed rgba(148,163,184,0.40)' : '1px solid rgba(226,232,240,0.7)'),
      boxShadow: filling ? '0 4px 14px rgba(41,198,198,0.18)' : 'none',
      display: 'flex', flexDirection: 'column', gap: 5,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        <span style={{
          fontSize: 10, fontWeight: 800, letterSpacing: '0.08em',
          color: colors.mutedForeground,
          textTransform: 'uppercase',
        }}>{f.label}</span>
        <span style={{ flex: 1 }} />
        {f.autoFilled && !filling && (
          <span style={{
            display: 'inline-flex', alignItems: 'center', gap: 4,
            fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
            color: '#1ea5a5',
            background: 'rgba(41,198,198,0.14)',
            padding: '2px 7px', borderRadius: 999,
          }}>✦ AUTO-FILLED</span>
        )}
        {filling && (
          <span style={{
            display: 'inline-flex', alignItems: 'center', gap: 4,
            fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
            color: '#1ea5a5',
            background: 'rgba(41,198,198,0.22)',
            padding: '2px 7px', borderRadius: 999,
          }}>● FILLING NOW</span>
        )}
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        {(f.autoFilled || filling) && <Sparkle />}
        {isMulti ? (
          <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap', flex: 1 }}>
            {f.value.map((v, i) => (
              <span key={i} style={{
                fontSize: 11, fontWeight: 700, color: colors.foreground,
                background: 'rgba(41,198,198,0.10)',
                border: '1px solid rgba(41,198,198,0.30)',
                padding: '2px 9px', borderRadius: 999,
                letterSpacing: '-0.005em',
              }}>{v}</span>
            ))}
          </div>
        ) : (
          <div style={{
            fontSize: 13.5, fontWeight: empty ? 600 : 700,
            color: empty ? colors.mutedForeground : colors.foreground,
            letterSpacing: '-0.01em',
            fontStyle: empty ? 'italic' : 'normal',
            flex: 1,
            overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
          }}>{empty ? '— pending —' : f.value}</div>
        )}
      </div>
    </div>
  );
};

export const FormsHero = () => {
  const filled = FIELDS.filter(f => f.autoFilled).length;
  const total = FIELDS.length;
  const pct = (filled / total) * 100;
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
            background: '#2db87d',
            boxShadow: '0 0 0 5px rgba(45,184,125,0.22)',
          }} />
          <span style={{ fontSize: 19, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.015em' }}>
            Client Intake
          </span>
        </div>
        <span style={{
          fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
          color: colors.primary,
          background: 'rgba(41,198,198,0.14)',
          padding: '5px 10px', borderRadius: 999,
        }}>{filled}/{total} FIELDS</span>
      </div>

      {/* Progress bar */}
      <div style={{
        height: 8, background: 'rgba(148,163,184,0.16)', borderRadius: 999,
        overflow: 'hidden',
      }}>
        <div style={{
          width: `${pct}%`, height: '100%',
          background: 'linear-gradient(90deg, #29c6c6, #47a3d9)',
          borderRadius: 999,
          boxShadow: '0 1px 4px rgba(41,198,198,0.40)',
        }} />
      </div>

      {/* Field stack — bleeds off bottom */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {FIELDS.map((f, i) => <FieldRow key={i} f={f} />)}
      </div>
    </div>
  );
};

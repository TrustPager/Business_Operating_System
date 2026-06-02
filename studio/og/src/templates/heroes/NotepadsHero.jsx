// Notepads hero — ONE polished, completed notepad rendered top-to-bottom.
//
// Outcome framing: the finished notepad — rich content (heading, body,
// callout, bullet list, checklist) — not a directory of preview cards.
// "Detailed Notepads for Every Deal".

import React from 'react';
import { colors } from '../../theme.js';

// ── Inline primitives for rich-text rendering ─────────────────────────────
const H = ({ children }) => (
  <div style={{
    fontSize: 17, fontWeight: 800, color: colors.foreground,
    letterSpacing: '-0.02em', lineHeight: 1.2,
    marginTop: 14, marginBottom: 8,
  }}>{children}</div>
);

const H2 = ({ children, color = 'var(--brand-primary-deep)' }) => (
  <div style={{
    fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
    color, marginTop: 12, marginBottom: 6,
  }}>{children}</div>
);

const P = ({ children }) => (
  <div style={{
    fontSize: 12.5, fontWeight: 500, color: colors.foreground,
    lineHeight: 1.55, letterSpacing: '-0.005em',
    marginBottom: 8,
  }}>{children}</div>
);

const B = ({ children }) => (
  <span style={{ fontWeight: 800, color: colors.foreground }}>{children}</span>
);

const I = ({ children }) => (
  <span style={{ fontStyle: 'italic', color: colors.foreground }}>{children}</span>
);

const Mark = ({ children }) => (
  <span style={{
    background: 'color-mix(in srgb, var(--brand-primary) 18%, transparent)',
    color: 'var(--brand-primary-deep)',
    fontWeight: 800,
    padding: '1px 4px',
    borderRadius: 3,
  }}>{children}</span>
);

const Callout = ({ children, icon, color = 'var(--brand-primary)' }) => (
  <div style={{
    background: `${`color-mix(in srgb, ${color} 6%, transparent)`}`,
    border: `1px solid ${`color-mix(in srgb, ${color} 25%, transparent)`}`,
    borderLeft: `4px solid ${color}`,
    borderRadius: 8,
    padding: '10px 12px',
    display: 'flex', gap: 10, alignItems: 'flex-start',
    marginBottom: 10, marginTop: 6,
  }}>
    <div style={{
      width: 22, height: 22, borderRadius: 6,
      background: color,
      color: '#fff', fontSize: 12, fontWeight: 800,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      flexShrink: 0,
    }}>{icon}</div>
    <div style={{
      fontSize: 12, fontWeight: 600, color: colors.foreground,
      letterSpacing: '-0.005em', lineHeight: 1.45,
    }}>{children}</div>
  </div>
);

const Bullet = ({ children, color = 'var(--brand-primary)' }) => (
  <div style={{
    display: 'flex', alignItems: 'flex-start', gap: 9,
    fontSize: 12.5, fontWeight: 500, color: colors.foreground,
    lineHeight: 1.5, letterSpacing: '-0.005em',
    marginBottom: 5,
  }}>
    <span style={{
      width: 6, height: 6, borderRadius: '50%',
      background: color, flexShrink: 0,
      marginTop: 7,
    }} />
    <div style={{ flex: 1 }}>{children}</div>
  </div>
);

const CheckItem = ({ done, children }) => (
  <div style={{
    display: 'flex', alignItems: 'flex-start', gap: 9,
    fontSize: 12.5, fontWeight: 500,
    color: done ? colors.mutedForeground : colors.foreground,
    lineHeight: 1.5, letterSpacing: '-0.005em',
    marginBottom: 6,
    textDecoration: done ? 'line-through' : 'none',
    opacity: done ? 0.7 : 1,
  }}>
    {done ? (
      <div style={{
        width: 18, height: 18, borderRadius: 5,
        background: 'var(--brand-secondary)',
        color: '#fff', fontSize: 10, fontWeight: 800,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0, marginTop: 1,
        boxShadow: '0 1px 2px color-mix(in srgb, var(--brand-secondary) 30%, transparent)',
      }}>✓</div>
    ) : (
      <div style={{
        width: 18, height: 18, borderRadius: 5,
        background: '#fff',
        border: '2px solid rgba(148,163,184,0.40)',
        flexShrink: 0, marginTop: 1,
      }} />
    )}
    <div style={{ flex: 1 }}>{children}</div>
  </div>
);

// ── Hero ──────────────────────────────────────────────────────────────────
export const NotepadsHero = () => (
  <div style={{
    background: '#fff',
    borderRadius: 18,
    padding: 0,
    boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
    overflow: 'hidden',
    display: 'flex', flexDirection: 'column',
  }}>
    {/* Toolbar chrome — like a real rich-text editor */}
    <div style={{
      padding: '12px 18px',
      borderBottom: '1px solid rgba(226,232,240,0.6)',
      display: 'flex', alignItems: 'center', gap: 10,
      background: 'rgba(248,250,252,0.6)',
    }}>
      <div style={{
        width: 28, height: 28, borderRadius: 8,
        background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-accent))',
        color: '#fff', fontSize: 15, fontWeight: 800,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0,
        boxShadow: '0 2px 6px color-mix(in srgb, var(--brand-primary) 30%, transparent)',
      }}>📓</div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 4, flex: 1 }}>
        {['B', 'I', 'U'].map((c, i) => (
          <button key={i} style={{
            width: 26, height: 26, borderRadius: 6,
            background: 'transparent',
            border: '1px solid rgba(226,232,240,0.6)',
            color: colors.foreground,
            fontSize: 12, fontWeight: c === 'B' ? 800 : 600,
            fontStyle: c === 'I' ? 'italic' : 'normal',
            textDecoration: c === 'U' ? 'underline' : 'none',
            cursor: 'pointer',
          }}>{c}</button>
        ))}
        <span style={{ width: 1, height: 18, background: 'rgba(226,232,240,0.7)', margin: '0 4px' }} />
        {['H1', 'H2', '≡'].map((c, i) => (
          <button key={i} style={{
            height: 26, padding: '0 7px', borderRadius: 6,
            background: 'transparent',
            border: '1px solid rgba(226,232,240,0.6)',
            color: colors.mutedForeground,
            fontSize: 11, fontWeight: 700,
            cursor: 'pointer',
          }}>{c}</button>
        ))}
      </div>
      <span style={{
        display: 'inline-flex', alignItems: 'center', gap: 4,
        fontSize: 10, fontWeight: 800, letterSpacing: '0.10em',
        color: 'var(--brand-primary-deep)',
        background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
        padding: '4px 9px', borderRadius: 999,
        flexShrink: 0,
      }}>✦ AI POLISHED</span>
    </div>

    {/* Notepad page content */}
    <div style={{ padding: '16px 22px 22px', fontFamily: 'inherit' }}>
      {/* Title */}
      <div style={{
        fontSize: 21, fontWeight: 800, color: colors.foreground,
        letterSpacing: '-0.02em', lineHeight: 1.15,
        marginBottom: 6,
      }}>Discovery Call — Coastal Health Group</div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 7, marginBottom: 10 }}>
        <span style={{
          display: 'inline-flex', alignItems: 'center', gap: 5,
          fontSize: 10, fontWeight: 800, letterSpacing: '0.08em',
          color: 'var(--brand-primary)',
          background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
          padding: '3px 8px', borderRadius: 4,
        }}>
          <span style={{ width: 5, height: 5, borderRadius: '50%', background: 'var(--brand-primary)' }} />
          SALES · Q3 ROLLOUT
        </span>
        <span style={{ fontSize: 10.5, fontWeight: 600, color: colors.mutedForeground }}>
          Linked to deal · Last edited just now
        </span>
      </div>

      {/* AI Summary callout */}
      <Callout icon="✦" color="var(--brand-primary)">
        <B>The ask:</B> Replace their legacy practice management system with an
        integrated CRM that automates referrals and reminders across <B>3 clinics</B>.
        Decision maker is Dr Mitchell — needs board sign-off above <Mark>$50k</Mark>.
      </Callout>

      <H2>KEY PAIN POINTS</H2>
      <Bullet>GP referrals getting lost between locations</Bullet>
      <Bullet color="var(--brand-secondary)">Appointment reminders inconsistent → high no-show rate</Bullet>
      <Bullet color="var(--brand-accent)">No visibility into where each patient sits in the journey</Bullet>

      <H2 color="var(--brand-secondary)">PROPOSED SOLUTION</H2>
      <P>
        Phased rollout to keep initial commitment <B>under board threshold</B>:
        <I> AI Automation Audit</I> first, then CRM Suite build for all
        3 locations, then training + go-live.
      </P>

      <H2 color="var(--brand-accent)">NEXT ACTIONS</H2>
      <CheckItem done>Send proposal v2 with phased pricing</CheckItem>
      <CheckItem done>Book demo for the operations team</CheckItem>
      <CheckItem>Loop in Dr Patel (warm referrer) for endorsement</CheckItem>
      <CheckItem>Prep board pack for Aug 14 meeting</CheckItem>
    </div>
  </div>
);

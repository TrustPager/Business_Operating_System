// Fill with AI hero — vertical stack of discovery questions + deal fields
// that an AI is filling in from call notes / dictation. One row is mid-fill
// with a caret blinking, the rest are completed.
//
// Outcome framing: AI is writing the CRM for you. Looks like a deal-detail
// page populating itself.

import React from 'react';
import { ACCENT, PRIMARY, PRIMARY_DEEP, SUCCESS, TEXT, TEXT_MUTED } from '../../brand.js';

const SECTIONS = [
  {
    label: 'NOTES',
    rows: [
      {
        kind: 'paragraph',
        body: "Looking to replace their legacy practice management system with a fully integrated CRM. Decision maker is Dr Mitchell — board sign-off required above $50k. Strong interest in automated reminders. Warm referral from Dr Patel at Westmead.",
        sparkle: true,
      },
    ],
  },
  {
    label: 'DISCOVERY QUESTIONS',
    rows: [
      { kind: 'qa', q: 'What problem are they trying to solve?', a: 'Patient referrals getting lost between three clinic locations.', sparkle: true },
      { kind: 'qa', q: 'Who is the decision maker?',              a: 'Dr Sarah Mitchell (CFO) — board sign-off above $50k.',          sparkle: true },
      { kind: 'qa', q: 'What\'s their timeline?',                  a: 'Q3 rollout to coincide with new compliance reporting.',          sparkle: true },
      { kind: 'qa', q: 'What does success look like?',             a: '', sparkle: true, filling: true },
    ],
  },
];

const Sparkle = ({ filling = false }) => (
  <span style={{
    width: 18, height: 18, borderRadius: 6,
    background: filling
      ? `linear-gradient(135deg, ${PRIMARY}, ${ACCENT})`
      : `linear-gradient(135deg, ${SUCCESS}, ${PRIMARY})`,
    display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
    color: '#fff', fontSize: 10, fontWeight: 800,
    flexShrink: 0,
    boxShadow: filling
      ? `0 2px 8px ${PRIMARY}66`
      : `0 2px 6px ${SUCCESS}4d`,
  }}>✦</span>
);

const SectionLabel = ({ label }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '2px 4px' }}>
    <span style={{
      fontSize: 10, fontWeight: 800, letterSpacing: '0.12em',
      color: TEXT_MUTED,
    }}>{label}</span>
    <span style={{ flex: 1, height: 1, background: 'rgba(226,232,240,0.6)' }} />
  </div>
);

const NoteRow = ({ row }) => (
  <div style={{
    background: '#fff',
    borderRadius: 11,
    padding: '12px 14px',
    border: `1px solid ${PRIMARY}40`,
    background: `${PRIMARY}0a`,
    display: 'flex', gap: 11,
  }}>
    <Sparkle />
    <div style={{ flex: 1 }}>
      <div style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.08em',
        color: PRIMARY_DEEP, marginBottom: 5,
      }}>✦ TRANSCRIBED FROM DICTATION</div>
      <div style={{
        fontSize: 12.5, fontWeight: 500, color: TEXT,
        lineHeight: 1.45, letterSpacing: '-0.005em',
      }}>{row.body}</div>
    </div>
  </div>
);

const QARow = ({ row }) => (
  <div style={{
    background: row.filling ? `${PRIMARY}0d` : '#fff',
    borderRadius: 11,
    padding: '11px 14px',
    border: row.filling
      ? `1.5px solid ${PRIMARY}80`
      : '1px solid rgba(226,232,240,0.7)',
    boxShadow: row.filling ? `0 4px 14px ${PRIMARY}2e` : 'none',
    display: 'flex', flexDirection: 'column', gap: 6,
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
      <span style={{
        fontSize: 11, fontWeight: 700, color: TEXT_MUTED,
        letterSpacing: '-0.005em', flex: 1, lineHeight: 1.3,
      }}>{row.q}</span>
      {row.filling && (
        <span style={{
          fontSize: 9, fontWeight: 800, letterSpacing: '0.10em',
          color: PRIMARY_DEEP,
          background: `${PRIMARY}38`,
          padding: '2px 7px', borderRadius: 999,
        }}>● WRITING</span>
      )}
    </div>
    <div style={{ display: 'flex', alignItems: 'flex-start', gap: 8 }}>
      <Sparkle filling={row.filling} />
      <div style={{
        fontSize: 12.5, fontWeight: 700, color: TEXT,
        lineHeight: 1.35, letterSpacing: '-0.005em',
        flex: 1, minHeight: 16,
      }}>
        {row.a}
        {row.filling && (
          <span style={{
            display: 'inline-block', width: 1.5, height: 14,
            background: PRIMARY,
            verticalAlign: 'text-bottom',
            marginLeft: 2,
          }} />
        )}
      </div>
    </div>
  </div>
);

export const FillWithAIHero = () => (
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
          Coastal Health · Deal
        </span>
      </div>
      <span style={{
        display: 'inline-flex', alignItems: 'center', gap: 4,
        fontSize: 11, fontWeight: 800, letterSpacing: '0.10em',
        color: '#fff',
        background: `linear-gradient(135deg, ${PRIMARY}, ${ACCENT})`,
        padding: '5px 10px', borderRadius: 999,
        boxShadow: `0 2px 8px ${PRIMARY}66`,
      }}>✦ FILLING WITH AI</span>
    </div>

    {/* Sections */}
    {SECTIONS.map((section, si) => (
      <div key={si} style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        <SectionLabel label={section.label} />
        {section.rows.map((row, i) => (
          row.kind === 'paragraph' ? <NoteRow key={i} row={row} /> : <QARow key={i} row={row} />
        ))}
      </div>
    ))}
  </div>
);

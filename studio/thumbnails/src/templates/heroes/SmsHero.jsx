// SMS hero — vertical chat thread.
//
// Master rule (see ../YouTubeThumbnail.jsx HERO UI SELECTION): thin, tall,
// single vertical stack, bleeds off the bottom. No horizontal subdivisions.
// No conversation-list sidebar — just the open thread, scrolling forever.
//
// Reference: ../../../../src/scenes/features/SmsConversationPage.tsx
// Outcome framing: AI sends on your behalf, every message logged to the
// CRM thread. The "AI · SENT FOR YOU" pill is the differentiator vs a
// generic messaging app silhouette.

import React from 'react';
import { colors } from '../../theme.js';
import { Avatar } from '../../profiles.jsx';

const BUBBLES = [
  { from: 'them', text: 'Hey — can you bump our discovery to 4pm Friday?' },
  { from: 'ai',   text: "Hi James — 4:00 PM Friday works. I'll resend the calendar invite now." },
  { from: 'them', text: 'Perfect, 4pm works great. Thanks for being so flexible!' },
  { from: 'ai',   text: 'All set ✓ Calendar invite resent. See you Friday.' },
  { from: 'them', text: 'One more thing — can you send the latest pricing PDF?' },
  { from: 'ai',   text: "Pricing PDF sent. Also attached the FAQ doc you asked about last week." },
  { from: 'them', text: 'Brilliant, thanks. Forwarding to my CFO now.' },
  { from: 'ai',   text: 'Noted — I\'ve added "CFO review" to the Coastal deal in your pipeline.' },
  { from: 'them', text: 'Will this work with our existing Xero setup?' },
  { from: 'ai',   text: "Yes — full Xero sync. Want me to schedule a 15-min walkthrough with your CFO?" },
];

const Bubble = ({ b, last }) => {
  const fromThem = b.from === 'them';
  const fromAi = b.from === 'ai';
  const align = fromThem ? 'flex-start' : 'flex-end';
  return (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: align,
      gap: 5, marginBottom: last ? 0 : 14,
    }}>
      {fromAi && (
        <span style={{
          fontSize: 10, fontWeight: 800, color: '#29c6c6',
          background: 'rgba(41,198,198,0.14)',
          padding: '2px 8px', borderRadius: 999,
          letterSpacing: '0.10em',
        }}>AI · SENT FOR YOU</span>
      )}
      <div style={{
        background: fromThem ? '#f1f5f9' : '#29c6c6',
        color: fromThem ? colors.foreground : '#fff',
        borderRadius: 18,
        borderBottomLeftRadius: fromThem ? 6 : 18,
        borderBottomRightRadius: fromThem ? 18 : 6,
        padding: '12px 16px',
        fontSize: 16, fontWeight: 500, lineHeight: 1.35,
        maxWidth: '85%',
        boxShadow: fromAi
          ? '0 2px 8px rgba(41,198,198,0.25), 0 0 0 1px rgba(41,198,198,0.18)'
          : '0 1px 2px rgba(15,17,23,0.06)',
        letterSpacing: '-0.01em',
      }}>{b.text}</div>
    </div>
  );
};

export const SmsHero = () => (
  <div style={{
    background: '#fff',
    borderRadius: 18,
    boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
    display: 'flex', flexDirection: 'column',
    overflow: 'hidden',
  }}>
    {/* Header — thread context */}
    <div style={{
      padding: '16px 22px',
      borderBottom: '1px solid rgba(226,232,240,0.6)',
      display: 'flex', alignItems: 'center', gap: 12,
      background: 'rgba(248,250,252,0.55)',
    }}>
      <Avatar name="James Mitchell" size={38} style={{ boxShadow: '0 2px 6px rgba(15,17,23,0.20)' }} />
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontSize: 17, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.01em' }}>
          James Mitchell
        </div>
        <div style={{ fontSize: 12, color: colors.mutedForeground, fontWeight: 600, marginTop: 1 }}>
          +61 412 345 678 · linked to Coastal deal
        </div>
      </div>
      <span style={{
        fontSize: 10, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.primary,
        background: 'rgba(41,198,198,0.14)',
        padding: '5px 10px', borderRadius: 999,
      }}>LIVE</span>
    </div>

    {/* Bubble stream — bleeds off bottom */}
    <div style={{ padding: '18px 22px 26px' }}>
      {BUBBLES.map((b, i) => (
        <Bubble key={i} b={b} last={i === BUBBLES.length - 1} />
      ))}
    </div>
  </div>
);

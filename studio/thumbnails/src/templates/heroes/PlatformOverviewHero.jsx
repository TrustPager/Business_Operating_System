// Platform Overview hero — vertical stack of every TrustPager feature.
//
// Used by the "20 Tools in 1" promo thumbnail (composition: Promo-Hero-Loop).
// Family pattern: card stack — one row per feature with a brand-coloured icon
// dot, feature name, and one-line outcome subtitle. 8-9 rows visible, the
// rest bleed off the bottom to signal "this goes on and on".
//
// Brand-colour rule: cycle teal / green / blue / light teal / deep teal /
// slate ONLY. No orange / pink / purple / red even though the inline CRM
// section uses per-feature accents — those are website chrome; thumbnails
// stay on the TrustPager palette.

import React from 'react';
import { colors } from '../../theme.js';

// 6-colour brand cycle — order tuned so adjacent rows never share a hue
const BRAND_CYCLE = ['#29c6c6', '#2db87d', '#47a3d9', '#1ea5a5', '#7dd3d3', '#94a3b8'];

const FEATURES = [
  { name: 'Pipeline',         outcome: 'Every opportunity at a glance',          glyph: '📊' },
  { name: 'Automations',      outcome: 'Set it once. Runs forever.',             glyph: '⚡' },
  { name: 'Email',            outcome: 'Send right from the CRM',                glyph: '✉' },
  { name: 'SMS',              outcome: 'Conversations, all in one place',        glyph: '💬' },
  { name: 'Online Booking',   outcome: 'Clients book straight in',               glyph: '📅' },
  { name: 'Call Coaching',    outcome: 'AI listens to every call',               glyph: '📞' },
  { name: 'Meeting Coaching', outcome: 'AI joins every meeting',                 glyph: '🎥' },
  { name: 'Voice Agents',     outcome: 'AI answers when you can’t',         glyph: '🤖' },
  { name: 'Client Forms',     outcome: 'Filled by clients, into the CRM',        glyph: '📝' },
  { name: 'E-Signing',        outcome: 'Digital signatures, built in',           glyph: '✍' },
  { name: 'Needs Analysis',   outcome: 'Instant client briefs',                  glyph: '🧠' },
  { name: 'Proposals',        outcome: 'Built from your data',                   glyph: '📄' },
  { name: 'Image Gen',        outcome: 'On-brand images on demand',              glyph: '🎨' },
  { name: 'Voice Gen',        outcome: 'Your voice, cloned',                     glyph: '🎙' },
  { name: 'File Storage',     outcome: 'Every file, one place',                  glyph: '🗂' },
  { name: 'AI Writing',       outcome: 'Emails, docs, proposals',                glyph: '✨' },
  { name: 'Approvals',        outcome: 'AI asks before it acts',                 glyph: '✅' },
  { name: 'Reporting',        outcome: 'See your whole business',                glyph: '📈' },
];

const IconDot = ({ color, glyph }) => (
  <div style={{
    width: 38, height: 38, borderRadius: 10,
    background: `${color}1f`,
    border: `1.5px solid ${color}40`,
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    flexShrink: 0,
    fontSize: 18,
    lineHeight: 1,
  }}>
    {glyph}
  </div>
);

const FeatureRow = ({ name, outcome, color, glyph }) => (
  <div style={{
    background: '#fff',
    borderRadius: 12,
    padding: '10px 12px',
    border: '1px solid rgba(226,232,240,0.7)',
    display: 'flex', alignItems: 'center', gap: 12,
  }}>
    <IconDot color={color} glyph={glyph} />
    <div style={{ flex: 1, minWidth: 0 }}>
      <div style={{
        fontSize: 15.5, fontWeight: 800, color: colors.foreground,
        letterSpacing: '-0.015em',
        lineHeight: 1.15,
      }}>{name}</div>
      <div style={{
        fontSize: 11.5, fontWeight: 600, color: colors.mutedForeground,
        marginTop: 2, letterSpacing: '-0.005em',
        whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
      }}>{outcome}</div>
    </div>
    <span style={{
      fontSize: 9, fontWeight: 800, letterSpacing: '0.10em',
      color: color,
      background: `${color}1f`,
      padding: '3px 8px', borderRadius: 4,
      flexShrink: 0,
    }}>LIVE</span>
  </div>
);

export const PlatformOverviewHero = () => (
  <div style={{
    background: '#fff',
    borderRadius: 18,
    padding: 18,
    boxShadow:
      '0 1px 2px rgba(15,17,23,0.06), ' +
      '0 6px 14px rgba(15,17,23,0.06), ' +
      '0 26px 52px rgba(15,17,23,0.12), ' +
      '0 0 0 1px rgba(15,17,23,0.05)',
    display: 'flex', flexDirection: 'column', gap: 10,
  }}>
    {/* Standard hero header */}
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <span style={{
          width: 12, height: 12, borderRadius: '50%',
          background: '#2db87d',
          boxShadow: '0 0 0 5px rgba(45,184,125,0.22)',
        }} />
        <span style={{ fontSize: 19, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.015em' }}>
          Every Tool. One Login.
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.primary,
        background: 'rgba(41,198,198,0.14)',
        padding: '5px 10px', borderRadius: 999,
      }}>20 TOOLS · 1 PLATFORM</span>
    </div>

    {/* Feature stack — bleeds off bottom */}
    {FEATURES.map((f, i) => (
      <FeatureRow
        key={f.name}
        name={f.name}
        outcome={f.outcome}
        glyph={f.glyph}
        color={BRAND_CYCLE[i % BRAND_CYCLE.length]}
      />
    ))}
  </div>
);

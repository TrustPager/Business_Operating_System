// HelpCenterHero — vertical stack of video tutorial cards.
//
// Brand-aware: header pill + accent chrome use brand.heroAccents.
//
// Family pattern: CARD STACK.

import React from 'react';
import { colors } from '../../theme.js';
// Returns a tutorial list with thumb colours interpolated from the
// brand's accent palette (rather than hardcoded teal/green).
function buildTutorials() {
  return [
    { title: 'Manage your sales pipeline',         category: 'Pipeline',       duration: '4:12', thumb: 'var(--brand-primary)' },
    { title: 'Build & trigger automations',         category: 'Automations',    duration: '6:08', thumb: 'var(--brand-secondary)' },
    { title: 'Send & track emails',                 category: 'Email',          duration: '3:54', thumb: 'var(--brand-accent)' },
    { title: 'Online booking & scheduling',         category: 'Scheduling',     duration: '5:21', thumb: 'var(--brand-light)' },
    { title: 'Build proposals & documents',         category: 'Documents',      duration: '4:47', thumb: 'var(--brand-primary-deep)' },
    { title: 'AI needs analysis from any deal',     category: 'AI Features',    duration: '3:18', thumb: 'var(--brand-primary)' },
    { title: 'Build & send forms',                  category: 'Forms',          duration: '4:33', thumb: 'var(--brand-secondary)' },
    { title: 'Reports & dashboards',                category: 'Reporting',      duration: '5:02', thumb: 'var(--brand-accent)' },
  ];
}

const PlayBadge = () => (
  <div style={{
    position: 'absolute', top: '50%', left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 24, height: 24, borderRadius: '50%',
    background: 'rgba(255,255,255,0.96)',
    boxShadow: '0 3px 8px rgba(15,17,23,0.18)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
  }}>
    <svg width="10" height="10" viewBox="0 0 24 24" fill="none">
      <path d="M8 5v14l11-7z" fill="#0D0F1C" />
    </svg>
  </div>
);

const TutorialCard = ({ t }) => (
  <div style={{
    display: 'flex', gap: 12, alignItems: 'center',
    padding: '8px 4px',
    borderBottom: '1px solid rgba(226,232,240,0.7)',
  }}>
    <div style={{
      position: 'relative', flexShrink: 0,
      width: 84, height: 48, borderRadius: 8,
      background: `linear-gradient(135deg, ${t.thumb} 0%, ${`color-mix(in srgb, ${t.thumb} 80%, transparent)`} 100%)`,
      overflow: 'hidden',
    }}>
      <PlayBadge />
      <div style={{
        position: 'absolute', bottom: 3, right: 4,
        fontSize: 8, fontWeight: 700,
        background: 'rgba(13,15,28,0.7)', color: '#fff',
        padding: '1px 4px', borderRadius: 3,
        letterSpacing: '0.02em',
      }}>{t.duration}</div>
    </div>
    <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', gap: 3 }}>
      <span style={{
        alignSelf: 'flex-start',
        fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
        color: 'var(--brand-primary-deep)',
        background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
        padding: '2px 7px', borderRadius: 999,
        textTransform: 'uppercase',
      }}>{t.category}</span>
      <div style={{
        fontSize: 13.5, fontWeight: 700, color: colors.foreground,
        letterSpacing: '-0.01em', lineHeight: 1.25,
        overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
      }}>{t.title}</div>
    </div>
  </div>
);

export const HelpCenterHero = () => {
  const tutorials = buildTutorials();
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
          Help Center
        </div>
        <div style={{
          fontSize: 10, fontWeight: 800, letterSpacing: '0.12em',
          color: 'var(--brand-primary)', background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
          padding: '5px 10px', borderRadius: 999,
        }}>130+ TUTORIALS</div>
      </div>
      {tutorials.map((t, i) => <TutorialCard key={i} t={t} />)}
    </div>
  );
};

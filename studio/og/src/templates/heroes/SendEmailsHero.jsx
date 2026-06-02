// Send & Track Emails hero — vertical inbox stream.
//
// Outcome framing: emails sent FROM the CRM, every one logged to the
// linked deal. Tracked badges show "opened / clicked / replied" status.
//
// Brand-aware: per-deal colours rotate through the brand palette so a
// FinalPiece thumbnail shows purple/pink/blue deal tags while TrustPager
// shows teal/green/blue.

import React from 'react';
import { colors } from '../../theme.js';
import { Avatar } from '../../profiles.jsx';
function buildEmails() {
  return [
    {
      name: 'You → Anya Faulkner',
      subject: 'Re: SOW for Southern Cross Legal',
      preview: 'Thanks Anya — attaching the final scope + Q3 timeline. Happy to jump on a call…',
      direction: 'out',
      tracked: ['Opened', '12m'],
      linkedDeal: 'Southern Cross Legal',
      dealColor: 'var(--brand-accent)',
    },
    {
      name: 'Sarah Hartley',
      subject: 'Re: Compliance review proposal',
      preview: 'Looks great. CFO is on board pending board sign-off. Can we run through Q4 timeline?',
      direction: 'in',
      tracked: ['NEW', '20m'],
      linkedDeal: 'Coastal Consulting',
      dealColor: 'var(--brand-primary)',
    },
    {
      name: 'You → Hugo Daniels',
      subject: 'Wattle Creek — Q3 renewal',
      preview: "Hugo, here's the renewal pack. Pricing locked at last year's rate, plus the vineyard ops bundle…",
      direction: 'out',
      tracked: ['Replied', '2h'],
      linkedDeal: 'Wattle Creek Winery',
      dealColor: 'var(--brand-light)',
    },
    {
      name: 'Mira Suarez',
      subject: 'Re: Workflow audit — kick-off?',
      preview: "Yes, Thursday 10am works. I'll loop in our ops manager. Looking forward to it.",
      direction: 'in',
      tracked: ['NEW', '4h'],
      linkedDeal: 'Coastal Health Group',
      dealColor: 'var(--brand-secondary)',
    },
    {
      name: 'You → Theo Reilly',
      subject: 'Pinnacle Eng. — Quote v2',
      preview: 'Revised quote attached. Reduced scope to match your phased approach. Let me know any qs.',
      direction: 'out',
      tracked: ['Opened 3×', '1d'],
      linkedDeal: 'Pinnacle Engineering',
      dealColor: 'var(--brand-primary-deep)',
    },
    {
      name: 'Camille Anders',
      subject: 'Eucalyptus Wealth — discovery follow-up',
      preview: 'Hi! Sharing the comparison sheet we discussed. Quick call this Friday to lock direction?',
      direction: 'in',
      tracked: [null, '2d'],
      linkedDeal: 'Eucalyptus Wealth',
      dealColor: 'var(--brand-secondary)',
    },
  ];
}

function buildTrackColors() {
  return {
    Opened:      { bg: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',                 fg: 'var(--brand-primary-deep)' },
    'Opened 3×': { bg: `${`color-mix(in srgb, var(--brand-primary) 22%, transparent)`}`,              fg: 'var(--brand-primary-deep)' },
    Replied:     { bg: 'color-mix(in srgb, var(--brand-secondary) 12%, transparent)',               fg: 'var(--brand-secondary)' },
    NEW:         { bg: 'var(--brand-primary)',                     fg: '#ffffff' },
  };
}

const EmailRow = ({ e, a, trackColors }) => {
  const out = e.direction === 'out';
  const [tag, time] = e.tracked;
  const tagStyle = tag ? trackColors[tag] : null;
  return (
    <div style={{
      background: '#fff',
      borderRadius: 10,
      padding: '11px 13px',
      border: '1px solid rgba(226,232,240,0.7)',
      display: 'flex', alignItems: 'flex-start', gap: 11,
    }}>
      <Avatar name={e.name} size={32} />

      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 2 }}>
          <span style={{
            fontSize: 12, fontWeight: 800, color: colors.foreground,
            letterSpacing: '-0.01em',
            overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1,
          }}>{e.name}</span>
          <span style={{
            fontSize: 9, fontWeight: 700, color: colors.mutedForeground,
            flexShrink: 0,
          }}>{out ? '↗ SENT' : '↙ INBOX'}</span>
        </div>
        <div style={{
          fontSize: 12.5, fontWeight: 700, color: colors.foreground,
          letterSpacing: '-0.01em',
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
          marginBottom: 2,
        }}>{e.subject}</div>
        <div style={{
          fontSize: 11, color: colors.mutedForeground, fontWeight: 500,
          lineHeight: 1.35,
          overflow: 'hidden',
          display: '-webkit-box',
          WebkitLineClamp: 1,
          WebkitBoxOrient: 'vertical',
          marginBottom: 6,
        }}>{e.preview}</div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
          {tagStyle && (
            <span style={{
              fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
              color: tagStyle.fg,
              background: tagStyle.bg,
              padding: '2px 7px', borderRadius: 999,
            }}>{tag}</span>
          )}
          <span style={{
            display: 'inline-flex', alignItems: 'center', gap: 4,
            fontSize: 9, fontWeight: 800, letterSpacing: '0.06em',
            color: e.dealColor,
            background: `${`color-mix(in srgb, ${e.dealColor} 10%, transparent)`}`,
            padding: '2px 7px', borderRadius: 4,
            textTransform: 'uppercase',
          }}>
            <span style={{ width: 4, height: 4, borderRadius: '50%', background: e.dealColor }} />
            {e.linkedDeal}
          </span>
          <span style={{ flex: 1 }} />
          <span style={{ fontSize: 10, fontWeight: 600, color: colors.mutedForeground }}>{time}</span>
        </div>
      </div>
    </div>
  );
};

export const SendEmailsHero = () => {
  const emails = buildEmails();
  const trackColors = buildTrackColors();
  return (
    <div style={{
      background: '#fff',
      borderRadius: 18,
      padding: 18,
      boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
      display: 'flex', flexDirection: 'column', gap: 14,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{
            width: 12, height: 12, borderRadius: '50%',
            background: 'var(--brand-primary)',
            boxShadow: `0 0 0 5px ${'color-mix(in srgb, var(--brand-primary) 22%, transparent)'}`,
          }} />
          <span style={{ fontSize: 19, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.015em' }}>
            Inbox
          </span>
        </div>
        <span style={{
          fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
          color: 'var(--brand-primary)',
          background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
          padding: '5px 10px', borderRadius: 999,
        }}>ALL LINKED · LIVE</span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {emails.map((e, i) => <EmailRow key={i} e={e} trackColors={trackColors} />)}
      </div>
    </div>
  );
};

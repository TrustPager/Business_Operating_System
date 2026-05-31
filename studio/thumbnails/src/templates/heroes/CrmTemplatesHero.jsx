// CRM Templates hero — vertical stack of email template cards with
// inline {{merge_field}} chips highlighted teal. Each card is one
// reusable template ready to fire.
//
// Outcome framing: a library of pre-built templates, each with merge
// tokens that get filled in automatically. "Never Type the Same Thing Twice".

import React from 'react';
import { colors } from '../../theme.js';
import { ACCENT, LIGHT, PRIMARY, PRIMARY_DEEP, SUCCESS } from '../../brand.js';

const TEMPLATES = [
  {
    name: 'Welcome — New Client',
    subject: 'Welcome to TrustPager, {{contact.first_name}} 👋',
    body: 'Hi {{contact.first_name}}, thanks for choosing us for {{deal.title}}. Your onboarding starts {{deal.start_date}} — here\'s what to expect…',
    tokens: ['{{contact.first_name}}', '{{deal.title}}', '{{deal.start_date}}'],
    uses: 47,
    lastUsed: '2 hours ago',
    color: PRIMARY,
  },
  {
    name: 'Quote Follow-Up',
    subject: 'Re: Quote for {{deal.title}}',
    body: 'Hi {{contact.first_name}}, following up on the quote we sent. The {{deal.amount}} price is locked until {{deal.expires}}. Any questions?',
    tokens: ['{{contact.first_name}}', '{{deal.title}}', '{{deal.amount}}', '{{deal.expires}}'],
    uses: 124,
    lastUsed: '14 min ago',
    color: SUCCESS,
  },
  {
    name: 'Discovery Booking Link',
    subject: 'Quick call about {{company.name}}?',
    body: 'Hi {{contact.first_name}}, I\'d love to learn more about what {{company.name}} is solving for. Grab a slot here: {{user.scheduler_link}}',
    tokens: ['{{contact.first_name}}', '{{company.name}}', '{{user.scheduler_link}}'],
    uses: 89,
    lastUsed: 'Yesterday',
    color: ACCENT,
  },
  {
    name: 'Renewal Reminder',
    subject: 'Your {{deal.title}} renewal is up in 30 days',
    body: 'Hi {{contact.first_name}}, just a heads up — your contract renews on {{deal.renewal_date}}. {{user.signature}}',
    tokens: ['{{contact.first_name}}', '{{deal.title}}', '{{deal.renewal_date}}', '{{user.signature}}'],
    uses: 32,
    lastUsed: '2 days ago',
    color: LIGHT,
  },
  {
    name: 'Welcome Aboard 🎉',
    subject: 'Welcome aboard, {{contact.first_name}}!',
    body: 'Congrats on signing! Your {{deal.title}} kicks off {{deal.start_date}}. Adding {{user.signature}}.',
    tokens: ['{{contact.first_name}}', '{{deal.title}}', '{{deal.start_date}}', '{{user.signature}}'],
    uses: 18,
    lastUsed: '3 days ago',
    color: PRIMARY_DEEP,
  },
];

// Render body text with token highlighting
const renderBody = (text, tokens) => {
  if (!tokens || tokens.length === 0) return text;
  // Escape regex specials in tokens
  const esc = tokens.map(t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  const re = new RegExp(`(${esc.join('|')})`, 'g');
  const parts = text.split(re);
  return parts.map((p, i) => {
    if (tokens.includes(p)) {
      return (
        <span key={i} style={{
          display: 'inline-block',
          fontSize: 10, fontWeight: 800,
          color: PRIMARY_DEEP,
          background: 'rgba(41,198,198,0.18)',
          padding: '1px 6px', borderRadius: 4,
          letterSpacing: '-0.005em',
          fontFamily: 'monospace',
          verticalAlign: 'baseline',
        }}>{p}</span>
      );
    }
    return <span key={i}>{p}</span>;
  });
};

const TemplateCard = ({ t }) => (
  <div style={{
    background: '#fff',
    borderRadius: 12,
    padding: '12px 14px',
    border: '1px solid rgba(226,232,240,0.7)',
    borderLeft: `4px solid ${t.color}`,
    display: 'flex', flexDirection: 'column', gap: 7,
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <div style={{
        width: 26, height: 26, borderRadius: 7,
        background: `${t.color}1f`,
        color: t.color, fontSize: 13, fontWeight: 800,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0,
      }}>✉</div>
      <span style={{
        fontSize: 13, fontWeight: 800, color: colors.foreground,
        letterSpacing: '-0.01em', flex: 1, minWidth: 0,
        overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
      }}>{t.name}</span>
      <span style={{
        fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
        color: colors.mutedForeground,
        background: 'rgba(148,163,184,0.14)',
        padding: '2px 7px', borderRadius: 999,
      }}>{t.uses}× USED</span>
    </div>

    <div style={{
      fontSize: 11, color: colors.foreground, fontWeight: 700,
      letterSpacing: '-0.005em', lineHeight: 1.4,
    }}>
      <span style={{ color: colors.mutedForeground, fontWeight: 600 }}>Subject: </span>
      {renderBody(t.subject, t.tokens)}
    </div>

    <div style={{
      fontSize: 10.5, color: colors.mutedForeground, fontWeight: 500,
      lineHeight: 1.5,
      overflow: 'hidden',
      display: '-webkit-box',
      WebkitLineClamp: 2,
      WebkitBoxOrient: 'vertical',
    }}>
      {renderBody(t.body, t.tokens)}
    </div>

    <div style={{ display: 'flex', alignItems: 'center', gap: 5, marginTop: 2 }}>
      <span style={{
        fontSize: 9, fontWeight: 800, letterSpacing: '0.06em',
        color: PRIMARY_DEEP,
        background: 'rgba(41,198,198,0.14)',
        padding: '2px 7px', borderRadius: 4,
      }}>{t.tokens.length} MERGE FIELDS</span>
      <span style={{ flex: 1 }} />
      <span style={{
        fontSize: 10, fontWeight: 600, color: colors.mutedForeground,
      }}>{t.lastUsed}</span>
    </div>
  </div>
);

export const CrmTemplatesHero = () => (
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
          Email Templates
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.primary,
        background: 'rgba(41,198,198,0.14)',
        padding: '5px 10px', borderRadius: 999,
      }}>310× SENT THIS MONTH</span>
    </div>

    {/* Template stack */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 9 }}>
      {TEMPLATES.map((t, i) => <TemplateCard key={i} t={t} />)}
    </div>
  </div>
);

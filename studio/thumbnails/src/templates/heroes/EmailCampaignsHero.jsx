// Email Campaigns hero — for "How to Create and Send Email Campaigns"
// (composition: Email-6-Campaigns).
//
// Master rule (see ../YouTubeThumbnail.jsx HERO UI SELECTION): thin, tall,
// single vertical stack, bleeds off bottom. The viewer reads:
//   "A sent campaign with a stack of per-contact tracking rows."
//
// Differentiator vs ReportsHero (chart-card stack) and SendEmailsHero
// (inbox rows): the iconic silhouette is a CAMPAIGN STATS STRIP on top
// (Sent / Delivered / Opens / Clicks) and then per-RECIPIENT tracking
// rows below with status pills. That's the unique surface of broadcast
// email — you see WHO opened, not just an aggregate number.

import React from 'react';
import { colors } from '../../theme.js';
import { Avatar } from '../../profiles.jsx';
import { ACCENT, PRIMARY_DEEP, SLATE, SUCCESS } from '../../brand.js';

const CAMPAIGN = {
  name: 'Q3 Product Launch',
  subject: "We're launching a faster pipeline view",
  audienceLabel: 'Active customers · 412 contacts',
  sent: 412,
  delivered: 406,
  opens: 318,
  clicks: 94,
  bounced: 6,
  unsubscribed: 2,
};

// Compact stat-card row used in the stats strip.
const Stat = ({ label, value, sub, color }) => (
  <div style={{
    flex: 1,
    background: '#fff',
    border: '1px solid rgba(226,232,240,0.7)',
    borderRadius: 10,
    padding: '10px 11px',
    display: 'flex', flexDirection: 'column', gap: 2,
    minWidth: 0,
  }}>
    <span style={{
      fontSize: 9, fontWeight: 800, letterSpacing: '0.10em',
      color: colors.mutedForeground,
    }}>{label}</span>
    <span style={{
      fontSize: 20, fontWeight: 800, color,
      letterSpacing: '-0.02em', lineHeight: 1,
    }}>{value}</span>
    {sub && (
      <span style={{
        fontSize: 9.5, fontWeight: 700, color: colors.mutedForeground,
        letterSpacing: '-0.005em', marginTop: 1,
      }}>{sub}</span>
    )}
  </div>
);

const StatusPill = ({ state }) => {
  const map = {
    opened:  { fg: PRIMARY_DEEP, bg: 'rgba(41,198,198,0.18)', label: 'OPENED' },
    clicked: { fg: SUCCESS, bg: 'rgba(45,184,125,0.18)', label: 'CLICKED' },
    delivered: { fg: ACCENT, bg: 'rgba(71,163,217,0.18)', label: 'DELIVERED' },
    bounced: { fg: SLATE, bg: 'rgba(148,163,184,0.18)', label: 'BOUNCED' },
    unsub:   { fg: SLATE, bg: 'rgba(148,163,184,0.18)', label: 'UNSUB' },
  };
  const s = map[state];
  return (
    <span style={{
      fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
      color: s.fg, background: s.bg,
      padding: '3px 8px', borderRadius: 999,
      whiteSpace: 'nowrap',
    }}>{s.label}</span>
  );
};

const RECIPIENTS = [
  { name: 'Saskia Williams',  time: '2m ago',  state: 'clicked'  },
  { name: 'Hugo Daniels',     time: '4m ago',  state: 'opened'   },
  { name: 'Anya Fisher',      time: '6m ago',  state: 'opened'   },
  { name: 'Camille Albright', time: '11m ago', state: 'clicked'  },
  { name: 'Theo Ramirez',     time: '14m ago', state: 'opened'   },
  { name: 'Otis Cole',        time: '18m ago', state: 'delivered'},
  { name: 'Beau Norris',      time: '22m ago', state: 'opened'   },
];

const RecipientRow = ({ r }) => (
  <div style={{
    display: 'flex', alignItems: 'center', gap: 11,
    padding: '9px 11px',
    background: '#fff',
    border: '1px solid rgba(226,232,240,0.7)',
    borderRadius: 10,
  }}>
    <Avatar name={r.name} size={30} />
    <div style={{ flex: 1, minWidth: 0 }}>
      <div style={{
        fontSize: 13, fontWeight: 800, color: colors.foreground,
        letterSpacing: '-0.01em', lineHeight: 1.1,
        overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
      }}>{r.name}</div>
      <div style={{
        fontSize: 10.5, fontWeight: 700, color: colors.mutedForeground,
        letterSpacing: '-0.005em', marginTop: 2,
      }}>{r.time}</div>
    </div>
    <StatusPill state={r.state} />
  </div>
);

export const EmailCampaignsHero = () => {
  const openPct = Math.round((CAMPAIGN.opens / CAMPAIGN.delivered) * 100);
  const clickPct = Math.round((CAMPAIGN.clicks / CAMPAIGN.delivered) * 100);

  return (
    <div style={{
      background: '#fff',
      borderRadius: 18,
      padding: 18,
      boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
      display: 'flex', flexDirection: 'column', gap: 12,
    }}>
      {/* Header — campaign name + SENT pill */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, minWidth: 0, flex: 1 }}>
          <span style={{
            width: 12, height: 12, borderRadius: '50%',
            background: SUCCESS,
            boxShadow: '0 0 0 5px rgba(45,184,125,0.22)',
            flexShrink: 0,
          }} />
          <span style={{
            fontSize: 19, fontWeight: 800, color: colors.foreground,
            letterSpacing: '-0.015em',
            overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
          }}>{CAMPAIGN.name}</span>
        </div>
        <span style={{
          fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
          color: SUCCESS,
          background: 'rgba(45,184,125,0.16)',
          padding: '5px 10px', borderRadius: 999,
          flexShrink: 0,
        }}>SENT</span>
      </div>

      {/* Subject + audience line */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(41,198,198,0.08), rgba(71,163,217,0.08))',
        border: '1px solid rgba(41,198,198,0.20)',
        borderRadius: 10,
        padding: '11px 13px',
      }}>
        <div style={{
          fontSize: 9, fontWeight: 800, letterSpacing: '0.10em',
          color: PRIMARY_DEEP,
        }}>SUBJECT</div>
        <div style={{
          fontSize: 13, fontWeight: 800, color: colors.foreground,
          letterSpacing: '-0.01em', marginTop: 2, lineHeight: 1.2,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{CAMPAIGN.subject}</div>
        <div style={{
          fontSize: 10.5, fontWeight: 700, color: colors.mutedForeground,
          letterSpacing: '-0.005em', marginTop: 4,
        }}>{CAMPAIGN.audienceLabel}</div>
      </div>

      {/* Stats strip — 4 across (still inside one outer container, so OK
          per master rule. This is a header band, not a horizontal split of
          the main content.) */}
      <div style={{ display: 'flex', gap: 8 }}>
        <Stat label="DELIVERED" value={CAMPAIGN.delivered} sub={`of ${CAMPAIGN.sent} sent`} color={ACCENT} />
        <Stat label="OPENS"     value={`${openPct}%`}     sub={`${CAMPAIGN.opens}`}         color={PRIMARY_DEEP} />
        <Stat label="CLICKS"    value={`${clickPct}%`}    sub={`${CAMPAIGN.clicks}`}        color={SUCCESS} />
        <Stat label="BOUNCED"   value={CAMPAIGN.bounced}  sub={`${CAMPAIGN.unsubscribed} unsub`} color={SLATE} />
      </div>

      {/* Recipients label */}
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        marginTop: 2,
      }}>
        <span style={{
          fontSize: 11, fontWeight: 800, letterSpacing: '0.10em',
          color: colors.mutedForeground,
        }}>RECIPIENTS · LIVE TRACKING</span>
        <span style={{
          fontSize: 10, fontWeight: 800, letterSpacing: '0.08em',
          color: PRIMARY_DEEP,
          background: 'rgba(41,198,198,0.14)',
          padding: '2px 8px', borderRadius: 999,
        }}>● LIVE</span>
      </div>

      {/* Recipient rows — bleeds off bottom */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 7 }}>
        {RECIPIENTS.map((r, i) => <RecipientRow key={i} r={r} />)}
      </div>
    </div>
  );
};

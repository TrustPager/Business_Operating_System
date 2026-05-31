// Agent Hub hero — vertical roster of demo AI agents.
//
// Agent portraits live at /agents/<Name>.png. Each card shows an agent
// with a status pulse, latest action, and capability tags. Swap the
// portraits and names for your own team if you want to brand the
// thumbnail to your own AI agents.
//
// Brand-colour rule: the portraits are full-colour images (intentional —
// they're the agent identity). Surrounding chrome (status dots, pills,
// capability tags) stays on the TrustPager palette: teal / green / blue /
// light teal / slate. No orange / purple / red in the chrome.

import React from 'react';
import { colors } from '../../theme.js';

const AGENTS = [
  {
    name: 'Aria',
    role: 'VOICE',
    title: 'AI receptionist',
    avatar: '/agents/Aria.png',
    status: 'active',
    lastRun: 'Just now',
    lastAction: 'Booked Hugo Daniels for a Workflow Audit at 4pm',
    caps: ['Voice', 'Bookings', 'CRM'],
    runsToday: 18,
    statusColor: '#2db87d',
  },
  {
    name: 'Marty',
    role: 'FULFILMENT',
    title: 'Ops coordinator',
    avatar: '/agents/Marty.png',
    status: 'active',
    lastRun: '2 min ago',
    lastAction: 'Pushed Coastal Health into Onboarding stage',
    caps: ['Pipeline', 'Tasks', 'Workflows'],
    runsToday: 42,
    statusColor: '#29c6c6',
  },
  {
    name: 'Mira',
    role: 'MARKETING',
    title: 'Content engine',
    avatar: '/agents/Mira.png',
    status: 'active',
    lastRun: '11 min ago',
    lastAction: 'Drafted Q3 case-study blog post (1,200 words)',
    caps: ['Writing', 'Video', 'Social'],
    runsToday: 8,
    statusColor: '#47a3d9',
  },
  {
    name: 'Lyra',
    role: 'REPORTING',
    title: 'The analyst',
    avatar: '/agents/Lyra.png',
    status: 'active',
    lastRun: '1 hour ago',
    lastAction: 'Posted morning digest — 3 deals slipping SLA',
    caps: ['Reports', 'Slack', 'Alerts'],
    runsToday: 6,
    statusColor: '#1ea5a5',
  },
  {
    name: 'Orion',
    role: 'OUTREACH',
    title: 'The sales rep',
    avatar: '/agents/Orion.png',
    status: 'active',
    lastRun: '3 hours ago',
    lastAction: 'Sent 24 personalised outbounds, 6 replies in',
    caps: ['Email', 'SMS', 'Sequences'],
    runsToday: 24,
    statusColor: '#7dd3d3',
  },
  {
    name: 'Sable',
    role: 'RESEARCH',
    title: 'Lead scout',
    avatar: '/agents/Sable.png',
    status: 'active',
    lastRun: '4 hours ago',
    lastAction: 'Sourced 47 prospects in healthcare AU',
    caps: ['Sourcing', 'De-dupe', 'Enrichment'],
    runsToday: 12,
    statusColor: '#2db87d',
  },
  {
    name: 'Echo',
    role: 'SUPPORT',
    title: 'Error detective',
    avatar: '/agents/Echo.png',
    status: 'active',
    lastRun: '6 hours ago',
    lastAction: 'Investigated payment webhook spike, root cause filed',
    caps: ['Errors', 'Vector Search', 'Email'],
    runsToday: 3,
    statusColor: '#29c6c6',
  },
];

const STATUS = {
  active: { color: '#2db87d', label: 'ACTIVE' },
  paused: { color: '#94a3b8', label: 'PAUSED' },
};

const Pulse = ({ color }) => (
  <span style={{
    width: 9, height: 9, borderRadius: '50%',
    background: color,
    boxShadow: `0 0 0 4px ${color}33`,
    flexShrink: 0,
  }} />
);

const AgentCard = ({ a }) => {
  const s = STATUS[a.status];
  const isActive = a.status === 'active';
  return (
    <div style={{
      background: '#fff',
      borderRadius: 12,
      padding: '12px 14px',
      border: '1px solid rgba(226,232,240,0.7)',
      display: 'flex', flexDirection: 'column', gap: 9,
      opacity: isActive ? 1 : 0.75,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{
          width: 46, height: 46, borderRadius: '50%',
          background: '#fff',
          border: `2px solid ${a.statusColor}`,
          padding: 2,
          flexShrink: 0,
          boxShadow: '0 2px 6px rgba(15,17,23,0.10)',
          overflow: 'hidden',
        }}>
          <img
            src={a.avatar}
            alt={a.name}
            style={{
              width: '100%', height: '100%',
              borderRadius: '50%',
              objectFit: 'cover',
              display: 'block',
            }}
          />
        </div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
            <span style={{
              fontSize: 16, fontWeight: 800, color: colors.foreground,
              letterSpacing: '-0.015em',
            }}>{a.name}</span>
            <Pulse color={s.color} />
            <span style={{
              fontSize: 9, fontWeight: 800, letterSpacing: '0.10em',
              color: a.statusColor,
              background: `${a.statusColor}1f`,
              padding: '2px 7px', borderRadius: 4,
              flexShrink: 0,
            }}>{a.role}</span>
          </div>
          <div style={{
            fontSize: 11, fontWeight: 600, color: colors.mutedForeground,
            marginTop: 1, letterSpacing: '-0.005em',
          }}>
            {a.title} · ran {a.runsToday}× today · last {a.lastRun}
          </div>
        </div>
      </div>

      {/* Latest action */}
      <div style={{
        background: 'rgba(248,250,252,0.7)',
        borderRadius: 8,
        padding: '7px 10px',
        border: '1px solid rgba(226,232,240,0.5)',
        fontSize: 11.5, fontWeight: 600, color: colors.foreground,
        letterSpacing: '-0.005em',
        lineHeight: 1.35,
        display: 'flex', alignItems: 'center', gap: 7,
      }}>
        <span style={{ color: '#2db87d', fontSize: 13, fontWeight: 800 }}>✓</span>
        <span style={{
          flex: 1,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{a.lastAction}</span>
      </div>

      {/* Capabilities */}
      <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap' }}>
        {a.caps.map((c, i) => (
          <span key={i} style={{
            fontSize: 9.5, fontWeight: 800, letterSpacing: '0.06em',
            color: colors.mutedForeground,
            background: 'rgba(148,163,184,0.14)',
            padding: '2px 8px', borderRadius: 4,
            textTransform: 'uppercase',
          }}>{c}</span>
        ))}
      </div>
    </div>
  );
};

export const AgentHubHero = () => (
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
          Your AI Team
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.primary,
        background: 'rgba(41,198,198,0.14)',
        padding: '5px 10px', borderRadius: 999,
      }}>7 ACTIVE · 113 RUNS TODAY</span>
    </div>

    {/* Agent stack — bleeds off bottom */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 9 }}>
      {AGENTS.map((a, i) => <AgentCard key={i} a={a} />)}
    </div>
  </div>
);

// Agent Hub hero — vertical roster of the real FinalPiece AI agents.
//
// Agent portraits live at /agents/<Name>.png (copied from
// D:/Dev/FinalPiece-NewDesign/public/product/ai_agents). Each card shows
// the real agent with a status pulse, latest action, and capability tags.
//
// Brand-colour rule: the portraits are full-colour images (intentional —
// they're the agent identity). Surrounding chrome (status dots, pills,
// capability tags) stays on the TrustPager palette: teal / green / blue /
// light teal / slate. No orange / purple / red in the chrome.

import React from 'react';
import { colors } from '../../theme.js';
// Per-agent statusColor is now resolved from the brand palette so the
// agent ring + role pill rotate through brand-appropriate accents. The
// portraits themselves stay full-colour (intentional — they're identity).
function buildAgents() {
  return [
    {
      name: 'Evie',     role: 'VOICE',       title: 'AI receptionist',
      avatar: '/agents/Evie.png',  lastRun: 'Just now', runsToday: 18,
      lastAction: 'Booked Hugo Daniels for a Workflow Audit at 4pm',
      caps: ['Voice', 'Bookings', 'CRM'],
      statusColor: 'var(--brand-secondary)',
    },
    {
      name: 'Marty',    role: 'FULFILMENT',  title: 'Ops coordinator',
      avatar: '/agents/Marty.png', lastRun: '2 min ago', runsToday: 42,
      lastAction: 'Pushed Coastal Health into Onboarding stage',
      caps: ['Pipeline', 'Tasks', 'Workflows'],
      statusColor: 'var(--brand-primary)',
    },
    {
      name: 'Mira',     role: 'MARKETING',   title: 'Content engine',
      avatar: '/agents/Mira.png',  lastRun: '11 min ago', runsToday: 8,
      lastAction: 'Drafted Q3 case-study blog post (1,200 words)',
      caps: ['Writing', 'Video', 'Social'],
      statusColor: 'var(--brand-accent)',
    },
    {
      name: 'Lyra',     role: 'REPORTING',   title: 'The analyst',
      avatar: '/agents/Lyra.png',  lastRun: '1 hour ago', runsToday: 6,
      lastAction: 'Posted morning digest — 3 deals slipping SLA',
      caps: ['Reports', 'Slack', 'Alerts'],
      statusColor: 'var(--brand-primary-deep)',
    },
    {
      name: 'Orion',    role: 'OUTREACH',    title: 'The sales rep',
      avatar: '/agents/Orion.png', lastRun: '3 hours ago', runsToday: 24,
      lastAction: 'Sent 24 personalised outbounds, 6 replies in',
      caps: ['Email', 'SMS', 'Sequences'],
      statusColor: 'var(--brand-light)',
    },
    {
      name: 'Sable',    role: 'RESEARCH',    title: 'Lead scout',
      avatar: '/agents/Sable.png', lastRun: '4 hours ago', runsToday: 12,
      lastAction: 'Sourced 47 prospects in healthcare AU',
      caps: ['Sourcing', 'De-dupe', 'Enrichment'],
      statusColor: 'var(--brand-secondary)',
    },
    {
      name: 'Echo',     role: 'SUPPORT',     title: 'Error detective',
      avatar: '/agents/Echo.png',  lastRun: '6 hours ago', runsToday: 3,
      lastAction: 'Investigated payment webhook spike, root cause filed',
      caps: ['Errors', 'Vector Search', 'Email'],
      statusColor: 'var(--brand-primary)',
    },
  ];
}

const Pulse = ({ color }) => (
  <span style={{
    width: 9, height: 9, borderRadius: '50%',
    background: color,
    boxShadow: `0 0 0 4px ${`color-mix(in srgb, ${color} 20%, transparent)`}`,
    flexShrink: 0,
  }} />
);

const AgentCard = ({ agent }) => (
  <div style={{
    background: '#fff',
    borderRadius: 12,
    padding: '12px 14px',
    border: '1px solid rgba(226,232,240,0.7)',
    display: 'flex', flexDirection: 'column', gap: 9,
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
      <div style={{
        width: 46, height: 46, borderRadius: '50%',
        background: '#fff',
        border: `2px solid ${agent.statusColor}`,
        padding: 2,
        flexShrink: 0,
        boxShadow: '0 2px 6px rgba(15,17,23,0.10)',
        overflow: 'hidden',
      }}>
        <img
          src={agent.avatar}
          alt={agent.name}
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
          }}>{agent.name}</span>
          <Pulse color={'var(--brand-primary)'} />
          <span style={{
            fontSize: 9, fontWeight: 800, letterSpacing: '0.10em',
            color: agent.statusColor,
            background: `${`color-mix(in srgb, ${agent.statusColor} 12%, transparent)`}`,
            padding: '2px 7px', borderRadius: 4,
            flexShrink: 0,
          }}>{agent.role}</span>
        </div>
        <div style={{
          fontSize: 11, fontWeight: 600, color: colors.mutedForeground,
          marginTop: 1, letterSpacing: '-0.005em',
        }}>
          {agent.title} · ran {agent.runsToday}× today · last {agent.lastRun}
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
      <span style={{ color: 'var(--brand-primary)', fontSize: 13, fontWeight: 800 }}>✓</span>
      <span style={{
        flex: 1,
        overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
      }}>{agent.lastAction}</span>
    </div>

    {/* Capabilities */}
    <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap' }}>
      {agent.caps.map((c, i) => (
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

export const AgentHubHero = () => {
  const agents = buildAgents();
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
            background: 'var(--brand-primary)',
            boxShadow: `0 0 0 5px ${'color-mix(in srgb, var(--brand-primary) 22%, transparent)'}`,
          }} />
          <span style={{ fontSize: 19, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.015em' }}>
            Your AI Team
          </span>
        </div>
        <span style={{
          fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
          color: 'var(--brand-primary)',
          background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
          padding: '5px 10px', borderRadius: 999,
        }}>7 ACTIVE · 113 RUNS TODAY</span>
      </div>

      {/* Agent stack — bleeds off bottom */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 9 }}>
        {agents.map((agent, i) => <AgentCard key={i} agent={agent} />)}
      </div>
    </div>
  );
};

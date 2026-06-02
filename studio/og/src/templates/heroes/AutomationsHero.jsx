// Automations hero — vertical flow of action cards firing from one
// trigger. Trigger pill at top, then a stack of action cards with
// connector arrows between, each card showing what fired and when.
//
// Outcome framing: the automation is RUNNING. Past actions have green
// checks, current is in flight, future is queued. "Automate Everything".

import React from 'react';
import { colors } from '../../theme.js';

const TRIGGER = {
  title: 'When Form Submitted',
  detail: 'Client Intake Form',
  icon: '⚡',
};

const ACTIONS = [
  {
    icon: '✉',
    iconBg: 'color-mix(in srgb, var(--brand-primary) 16%, transparent)',
    iconColor: 'var(--brand-primary-deep)',
    title: 'Send Welcome Email',
    detail: 'Template: "Welcome — New Client"',
    state: 'fired',
    when: '0.4s',
  },
  {
    icon: '◉',
    iconBg: 'color-mix(in srgb, var(--brand-secondary) 16%, transparent)',
    iconColor: 'var(--brand-secondary)',
    title: 'Create Opportunity',
    detail: 'Pipeline: Sales · Stage: Discovery',
    state: 'fired',
    when: '0.6s',
  },
  {
    icon: '☉',
    iconBg: 'color-mix(in srgb, var(--brand-accent) 16%, transparent)',
    iconColor: 'var(--brand-accent)',
    title: 'Assign to Sales Lead',
    detail: 'Round-robin · → Simon K.',
    state: 'fired',
    when: '0.8s',
  },
  {
    icon: '⏱',
    iconBg: 'color-mix(in srgb, var(--brand-light) 20%, transparent)',
    iconColor: 'var(--brand-primary-deep)',
    title: 'Wait 2 hours',
    detail: 'Throttle to avoid morning spam',
    state: 'running',
    when: 'now',
  },
  {
    icon: '💬',
    iconBg: 'color-mix(in srgb, var(--brand-primary) 16%, transparent)',
    iconColor: 'var(--brand-primary)',
    title: 'Send SMS Reminder',
    detail: '"Hi {{name}}, ready when you are!"',
    state: 'queued',
    when: '+2h',
  },
  {
    icon: '◐',
    iconBg: 'color-mix(in srgb, var(--brand-secondary) 16%, transparent)',
    iconColor: 'var(--brand-secondary)',
    title: 'Create Discovery Task',
    detail: 'Owner: Simon · Due: Tomorrow',
    state: 'queued',
    when: '+2h',
  },
  {
    icon: '✦',
    iconBg: 'color-mix(in srgb, var(--brand-accent) 16%, transparent)',
    iconColor: 'var(--brand-accent)',
    title: 'Score Lead with AI',
    detail: 'Returns: HOT / WARM / COLD',
    state: 'queued',
    when: '+2.1h',
  },
];

const STATE = {
  fired:   { fg: 'var(--brand-secondary)', bg: 'color-mix(in srgb, var(--brand-secondary) 18%, transparent)', label: '✓ FIRED' },
  running: { fg: 'var(--brand-primary-deep)', bg: 'color-mix(in srgb, var(--brand-primary) 22%, transparent)', label: '● RUNNING' },
  queued:  { fg: colors.mutedForeground, bg: 'rgba(148,163,184,0.16)', label: '◷ QUEUED' },
};

const Connector = ({ active }) => (
  <div style={{
    width: 2, height: 14,
    background: active
      ? 'linear-gradient(180deg, var(--brand-secondary) 0%, var(--brand-primary) 100%)'
      : 'rgba(148,163,184,0.30)',
    margin: '0 0 0 26px',
    position: 'relative',
  }}>
    <div style={{
      position: 'absolute', bottom: -2, left: -3,
      width: 0, height: 0,
      borderLeft: '4px solid transparent',
      borderRight: '4px solid transparent',
      borderTop: `6px solid ${active ? 'var(--brand-primary)' : 'rgba(148,163,184,0.50)'}`,
    }} />
  </div>
);

const TriggerCard = () => (
  <div style={{
    background: 'linear-gradient(135deg, color-mix(in srgb, var(--brand-primary) 10%, transparent), color-mix(in srgb, var(--brand-accent) 10%, transparent))',
    borderRadius: 12,
    padding: '12px 14px',
    border: '1.5px solid color-mix(in srgb, var(--brand-primary) 30%, transparent)',
    display: 'flex', alignItems: 'center', gap: 12,
  }}>
    <div style={{
      width: 38, height: 38, borderRadius: 10,
      background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-accent))',
      color: '#fff', fontSize: 18, fontWeight: 800,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      flexShrink: 0,
      boxShadow: '0 4px 10px color-mix(in srgb, var(--brand-primary) 30%, transparent)',
    }}>{TRIGGER.icon}</div>
    <div style={{ flex: 1, minWidth: 0 }}>
      <div style={{
        fontSize: 10, fontWeight: 800, letterSpacing: '0.12em',
        color: 'var(--brand-primary-deep)',
      }}>TRIGGER</div>
      <div style={{
        fontSize: 15, fontWeight: 800, color: colors.foreground,
        letterSpacing: '-0.01em', marginTop: 1,
      }}>{TRIGGER.title}</div>
      <div style={{
        fontSize: 11, fontWeight: 600, color: colors.mutedForeground,
        marginTop: 1, letterSpacing: '-0.005em',
      }}>{TRIGGER.detail}</div>
    </div>
  </div>
);

const ActionCard = ({ a }) => {
  const s = STATE[a.state];
  const running = a.state === 'running';
  return (
    <div style={{
      background: running ? 'color-mix(in srgb, var(--brand-primary) 5%, transparent)' : '#fff',
      borderRadius: 11,
      padding: '11px 13px',
      border: running
        ? '1.5px solid color-mix(in srgb, var(--brand-primary) 45%, transparent)'
        : '1px solid rgba(226,232,240,0.7)',
      boxShadow: running ? '0 4px 14px color-mix(in srgb, var(--brand-primary) 18%, transparent)' : 'none',
      display: 'flex', alignItems: 'center', gap: 11,
      opacity: a.state === 'queued' ? 0.85 : 1,
    }}>
      <div style={{
        width: 32, height: 32, borderRadius: 9,
        background: a.iconBg,
        color: a.iconColor, fontSize: 15, fontWeight: 800,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0,
      }}>{a.icon}</div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          fontSize: 13, fontWeight: 800, color: colors.foreground,
          letterSpacing: '-0.01em', lineHeight: 1.2,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{a.title}</div>
        <div style={{
          fontSize: 10.5, fontWeight: 600, color: colors.mutedForeground,
          marginTop: 2, letterSpacing: '-0.005em',
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{a.detail}</div>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 3, flexShrink: 0 }}>
        <span style={{
          fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
          color: s.fg, background: s.bg,
          padding: '2px 7px', borderRadius: 999,
        }}>{s.label}</span>
        <span style={{ fontSize: 9.5, fontWeight: 700, color: colors.mutedForeground }}>{a.when}</span>
      </div>
    </div>
  );
};

export const AutomationsHero = () => (
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
          background: 'var(--brand-secondary)',
          boxShadow: '0 0 0 5px color-mix(in srgb, var(--brand-secondary) 22%, transparent)',
        }} />
        <span style={{ fontSize: 19, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.015em' }}>
          New Lead Automation
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.primary,
        background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
        padding: '5px 10px', borderRadius: 999,
      }}>RUNNING</span>
    </div>

    {/* Trigger */}
    <TriggerCard />

    {/* Flow */}
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      {ACTIONS.map((a, i) => {
        const prevFiredOrRunning = i === 0
          ? true
          : ACTIONS[i - 1].state !== 'queued';
        return (
          <React.Fragment key={i}>
            <Connector active={prevFiredOrRunning} />
            <ActionCard a={a} />
          </React.Fragment>
        );
      })}
    </div>
  </div>
);

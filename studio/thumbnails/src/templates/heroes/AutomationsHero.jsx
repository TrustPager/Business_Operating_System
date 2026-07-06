// Automations hero — vertical flow of action cards firing from one
// trigger. Trigger pill at top, then a stack of action cards with
// connector arrows between, each card showing what fired and when.
//
// Outcome framing: the automation is RUNNING. Past actions have green
// checks, current is in flight, future is queued. "Automate Everything".

import React from 'react';
import { ACCENT, LIGHT, PRIMARY, PRIMARY_DEEP, SLATE, SUCCESS, TEXT, TEXT_MUTED } from '../../brand.js';

const TRIGGER = {
  title: 'When Form Submitted',
  detail: 'Client Intake Form',
  icon: '⚡',
};

const ACTIONS = [
  {
    icon: '✉',
    iconBg: `${PRIMARY}29`,
    iconColor: PRIMARY_DEEP,
    title: 'Send Welcome Email',
    detail: 'Template: "Welcome — New Client"',
    state: 'fired',
    when: '0.4s',
  },
  {
    icon: '◉',
    iconBg: `${SUCCESS}29`,
    iconColor: SUCCESS,
    title: 'Create Opportunity',
    detail: 'Pipeline: Sales · Stage: Discovery',
    state: 'fired',
    when: '0.6s',
  },
  {
    icon: '☉',
    iconBg: `${ACCENT}29`,
    iconColor: ACCENT,
    title: 'Assign to Sales Lead',
    detail: 'Round-robin · → Simon K.',
    state: 'fired',
    when: '0.8s',
  },
  {
    icon: '⏱',
    iconBg: `${LIGHT}33`,
    iconColor: PRIMARY_DEEP,
    title: 'Wait 2 hours',
    detail: 'Throttle to avoid morning spam',
    state: 'running',
    when: 'now',
  },
  {
    icon: '💬',
    iconBg: `${PRIMARY}29`,
    iconColor: PRIMARY,
    title: 'Send SMS Reminder',
    detail: '"Hi {{name}}, ready when you are!"',
    state: 'queued',
    when: '+2h',
  },
  {
    icon: '◐',
    iconBg: `${SUCCESS}29`,
    iconColor: SUCCESS,
    title: 'Create Discovery Task',
    detail: 'Owner: Simon · Due: Tomorrow',
    state: 'queued',
    when: '+2h',
  },
  {
    icon: '✦',
    iconBg: `${ACCENT}29`,
    iconColor: ACCENT,
    title: 'Score Lead with AI',
    detail: 'Returns: HOT / WARM / COLD',
    state: 'queued',
    when: '+2.1h',
  },
];

const STATE = {
  fired:   { fg: SUCCESS, bg: `${SUCCESS}2e`, label: '✓ FIRED' },
  running: { fg: PRIMARY_DEEP, bg: `${PRIMARY}38`, label: '● RUNNING' },
  queued:  { fg: TEXT_MUTED, bg: `${SLATE}29`, label: '◷ QUEUED' },
};

const Connector = ({ active }) => (
  <div style={{
    width: 2, height: 14,
    background: active
      ? `linear-gradient(180deg, ${SUCCESS} 0%, ${PRIMARY} 100%)`
      : `${SLATE}4d`,
    margin: '0 0 0 26px',
    position: 'relative',
  }}>
    <div style={{
      position: 'absolute', bottom: -2, left: -3,
      width: 0, height: 0,
      borderLeft: '4px solid transparent',
      borderRight: '4px solid transparent',
      borderTop: active ? `6px solid ${PRIMARY}` : `6px solid ${SLATE}80`,
    }} />
  </div>
);

const TriggerCard = () => (
  <div style={{
    background: `linear-gradient(135deg, ${PRIMARY}1a, ${ACCENT}1a)`,
    borderRadius: 12,
    padding: '12px 14px',
    border: `1.5px solid ${PRIMARY}4d`,
    display: 'flex', alignItems: 'center', gap: 12,
  }}>
    <div style={{
      width: 38, height: 38, borderRadius: 10,
      background: `linear-gradient(135deg, ${PRIMARY}, ${ACCENT})`,
      color: '#fff', fontSize: 18, fontWeight: 800,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      flexShrink: 0,
      boxShadow: `0 4px 10px ${PRIMARY}4d`,
    }}>{TRIGGER.icon}</div>
    <div style={{ flex: 1, minWidth: 0 }}>
      <div style={{
        fontSize: 10, fontWeight: 800, letterSpacing: '0.12em',
        color: PRIMARY_DEEP,
      }}>TRIGGER</div>
      <div style={{
        fontSize: 15, fontWeight: 800, color: TEXT,
        letterSpacing: '-0.01em', marginTop: 1,
      }}>{TRIGGER.title}</div>
      <div style={{
        fontSize: 11, fontWeight: 600, color: TEXT_MUTED,
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
      background: running ? `${PRIMARY}0d` : '#fff',
      borderRadius: 11,
      padding: '11px 13px',
      border: running
        ? `1.5px solid ${PRIMARY}73`
        : '1px solid rgba(226,232,240,0.7)',
      boxShadow: running ? `0 4px 14px ${PRIMARY}2e` : 'none',
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
          fontSize: 13, fontWeight: 800, color: TEXT,
          letterSpacing: '-0.01em', lineHeight: 1.2,
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{a.title}</div>
        <div style={{
          fontSize: 10.5, fontWeight: 600, color: TEXT_MUTED,
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
        <span style={{ fontSize: 9.5, fontWeight: 700, color: TEXT_MUTED }}>{a.when}</span>
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
          background: SUCCESS,
          boxShadow: `0 0 0 5px ${SUCCESS}38`,
        }} />
        <span style={{ fontSize: 19, fontWeight: 800, color: TEXT, letterSpacing: '-0.015em' }}>
          New Lead Automation
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: PRIMARY,
        background: `${PRIMARY}24`,
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

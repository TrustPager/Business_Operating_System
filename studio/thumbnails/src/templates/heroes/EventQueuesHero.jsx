// Event Queues hero — vertical drip-sequence timeline.
//
// Outcome framing: a campaign is running. Past steps fired (green ticks),
// current step in flight, future steps queued. The vertical connector
// reads as time flowing downward forever.

import React from 'react';
import { ACCENT, LIGHT, PRIMARY, PRIMARY_DEEP, SLATE, SUCCESS, TEXT, TEXT_MUTED } from '../../brand.js';

const STEPS = [
  { day: 'Day 0',  state: 'fired',   action: 'email',   title: 'Welcome — Thanks for signing up',     fired: '12 contacts',   when: '3 weeks ago' },
  { day: 'Day 3',  state: 'fired',   action: 'sms',     title: 'Quick check-in',                       fired: '12 contacts',   when: '20 days ago' },
  { day: 'Day 7',  state: 'fired',   action: 'email',   title: 'Case study — How we helped X',         fired: '12 contacts',   when: '2 weeks ago' },
  { day: 'Day 14', state: 'running', action: 'email',   title: 'Resource pack: getting started',       fired: '7 of 12',        when: 'Sending now' },
  { day: 'Day 21', state: 'queued',  action: 'task',    title: 'Create follow-up task for owner',      fired: null,             when: 'In 6 days' },
  { day: 'Day 30', state: 'queued',  action: 'email',   title: 'Free strategy call invitation',        fired: null,             when: 'In 15 days' },
  { day: 'Day 45', state: 'queued',  action: 'sms',     title: 'Final nudge — book a call?',           fired: null,             when: 'In 30 days' },
  { day: 'Day 60', state: 'queued',  action: 'exit',    title: 'Auto-exit if converted to customer',   fired: null,             when: 'In 45 days' },
];

const ACTION_ICON = {
  email: { icon: '✉', color: PRIMARY, bg: `${PRIMARY}29` },
  sms:   { icon: '💬', color: ACCENT, bg: `${ACCENT}29` },
  task:  { icon: '◐', color: LIGHT, bg: `${LIGHT}33` },
  exit:  { icon: '↗', color: SLATE, bg: `${SLATE}33` },
};

const STATE_PILL = {
  fired:   { fg: SUCCESS, bg: `${SUCCESS}29`,  label: '✓ FIRED' },
  running: { fg: PRIMARY_DEEP, bg: `${PRIMARY}33`,  label: '● RUNNING NOW' },
  queued:  { fg: TEXT_MUTED, bg: `${SLATE}29`, label: '◷ QUEUED' },
};

const StepRow = ({ step, isFirst, isLast }) => {
  const icon = ACTION_ICON[step.action];
  const pill = STATE_PILL[step.state];
  const isFired = step.state === 'fired';
  const isRunning = step.state === 'running';
  return (
    <div style={{ display: 'flex', gap: 12, alignItems: 'stretch' }}>
      {/* Timeline rail with day badge */}
      <div style={{ width: 56, flexShrink: 0, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {!isFirst && (
          <div style={{
            width: 2, height: 8,
            background: isFired || isRunning ? SUCCESS : `${SLATE}4d`,
          }} />
        )}
        <div style={{
          minWidth: 50, padding: '5px 8px',
          borderRadius: 999,
          background: isRunning
            ? `linear-gradient(135deg, ${PRIMARY}, ${ACCENT})`
            : (isFired ? SUCCESS : '#fff'),
          color: (isRunning || isFired) ? '#fff' : TEXT,
          fontSize: 11, fontWeight: 800,
          letterSpacing: '-0.005em',
          textAlign: 'center',
          border: !isRunning && !isFired ? `1.5px solid ${SLATE}66` : 'none',
          boxShadow: isRunning ? `0 4px 10px ${PRIMARY}59` : 'none',
          flexShrink: 0,
        }}>{step.day}</div>
        {!isLast && (
          <div style={{
            flex: 1,
            width: 2, minHeight: 16,
            background: isFired
              ? SUCCESS
              : (isRunning ? `linear-gradient(180deg, ${PRIMARY}, ${SLATE}4d)` : `${SLATE}4d`),
            marginTop: 6,
          }} />
        )}
      </div>

      {/* Action card */}
      <div style={{
        flex: 1, minWidth: 0,
        background: '#fff',
        borderRadius: 10,
        padding: '10px 12px',
        border: isRunning
          ? `1.5px solid ${PRIMARY}73`
          : '1px solid rgba(226,232,240,0.7)',
        boxShadow: isRunning ? `0 4px 14px ${PRIMARY}2e` : 'none',
        marginBottom: 4,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div style={{
            width: 26, height: 26, borderRadius: 7,
            background: icon.bg,
            color: icon.color, fontSize: 13, fontWeight: 800,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexShrink: 0,
          }}>{icon.icon}</div>
          <div style={{
            fontSize: 12.5, fontWeight: 800, color: TEXT,
            letterSpacing: '-0.01em', lineHeight: 1.2,
            flex: 1, minWidth: 0,
            overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
          }}>{step.title}</div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 6 }}>
          <span style={{
            fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
            color: pill.fg, background: pill.bg,
            padding: '2px 7px', borderRadius: 999,
          }}>{pill.label}</span>
          {step.fired && (
            <span style={{ fontSize: 10, fontWeight: 700, color: TEXT_MUTED }}>{step.fired}</span>
          )}
          <span style={{ flex: 1 }} />
          <span style={{ fontSize: 10, fontWeight: 600, color: TEXT_MUTED }}>{step.when}</span>
        </div>
      </div>
    </div>
  );
};

export const EventQueuesHero = () => (
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
          Lead Nurture Campaign
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: PRIMARY,
        background: `${PRIMARY}24`,
        padding: '5px 10px', borderRadius: 999,
      }}>12 ENROLLED</span>
    </div>

    {/* Timeline */}
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      {STEPS.map((s, i) => (
        <StepRow key={i} step={s} isFirst={i === 0} isLast={i === STEPS.length - 1} />
      ))}
    </div>
  </div>
);

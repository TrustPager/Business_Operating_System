// Tasks hero — vertical checklist.
//
// Outcome framing: tasks are tracked end-to-end. Top rows are completed
// (checked + struck through), middle in-progress, bottom queued for
// today/this week. Reads as "Manage Tasks with Ease".

import React from 'react';
import { Avatar } from '../../profiles.jsx';
import { ACCENT, PRIMARY, PRIMARY_DEEP, SLATE, SUCCESS, TEXT, TEXT_MUTED } from '../../brand.js';

const TASKS = [
  { state: 'done',        priority: 'high',   title: 'Send proposal to Dr Mitchell',          due: 'Today',     who: 'Dylan Reyes' },
  { state: 'done',        priority: 'medium', title: 'Book demo for Hugo Daniels',            due: 'Today',     who: 'Jordan Park' },
  { state: 'done',        priority: 'high',   title: 'Initial discovery call — Anya F.',      due: 'Yesterday', who: 'Dylan Reyes' },
  { state: 'in_progress', priority: 'high',   title: 'Refine quote for Pinnacle Eng.',        due: 'Today',     who: 'Dylan Reyes' },
  { state: 'in_progress', priority: 'medium', title: 'Follow up on compliance docs',          due: 'Tomorrow',  who: 'Dylan Reyes' },
  { state: 'pending',     priority: 'high',   title: 'Send NDA to Mateo Suarez',              due: 'Tomorrow',  who: 'Jordan Park' },
  { state: 'pending',     priority: 'medium', title: 'Prepare onboarding pack — Coastal',     due: 'Thu',       who: 'Dylan Reyes' },
  { state: 'pending',     priority: 'medium', title: 'Quarterly review with Wattle Creek',    due: 'Fri',       who: 'Mira Suarez' },
  { state: 'pending',     priority: 'low',    title: 'Update sales playbook — Q3 examples',   due: 'Next week', who: 'Dylan Reyes' },
];

const PRIORITY = {
  high:   { color: PRIMARY, label: 'HIGH' },
  medium: { color: ACCENT, label: 'MED'  },
  low:    { color: SLATE, label: 'LOW'  },
};

const Checkbox = ({ state }) => {
  if (state === 'done') {
    return (
      <div style={{
        width: 22, height: 22, borderRadius: 7,
        background: SUCCESS,
        color: '#fff', fontSize: 13, fontWeight: 800,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0,
        boxShadow: `0 2px 5px ${SUCCESS}4d`,
      }}>✓</div>
    );
  }
  if (state === 'in_progress') {
    return (
      <div style={{
        width: 22, height: 22, borderRadius: 7,
        background: `${PRIMARY}2e`,
        border: `2px solid ${PRIMARY}`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0,
        position: 'relative',
      }}>
        <div style={{
          width: 8, height: 8, borderRadius: 2,
          background: PRIMARY,
        }} />
      </div>
    );
  }
  return (
    <div style={{
      width: 22, height: 22, borderRadius: 7,
      border: `2px solid ${SLATE}66`,
      flexShrink: 0,
      background: '#fff',
    }} />
  );
};

const TaskRow = ({ t }) => {
  const done = t.state === 'done';
  const inProg = t.state === 'in_progress';
  const p = PRIORITY[t.priority];
  return (
    <div style={{
      background: inProg ? `${PRIMARY}0d` : '#fff',
      borderRadius: 10,
      padding: '10px 12px',
      border: inProg
        ? `1.5px solid ${PRIMARY}66`
        : '1px solid rgba(226,232,240,0.7)',
      boxShadow: inProg ? `0 4px 12px ${PRIMARY}24` : 'none',
      display: 'flex', alignItems: 'center', gap: 11,
      opacity: done ? 0.7 : 1,
    }}>
      <Checkbox state={t.state} />
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          fontSize: 13.5, fontWeight: 800,
          color: done ? TEXT_MUTED : TEXT,
          letterSpacing: '-0.01em', lineHeight: 1.25,
          textDecoration: done ? 'line-through' : 'none',
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{t.title}</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 7, marginTop: 3 }}>
          <span style={{
            fontSize: 9, fontWeight: 800, letterSpacing: '0.10em',
            color: p.color,
            background: `${p.color}1f`,
            padding: '2px 7px', borderRadius: 4,
          }}>{p.label}</span>
          <span style={{
            fontSize: 10.5, fontWeight: 600, color: TEXT_MUTED,
          }}>{t.due}</span>
          {inProg && (
            <span style={{
              fontSize: 9, fontWeight: 800, letterSpacing: '0.10em',
              color: PRIMARY_DEEP,
              background: `${PRIMARY}29`,
              padding: '2px 7px', borderRadius: 999,
            }}>● IN PROGRESS</span>
          )}
        </div>
      </div>
      <Avatar name={t.who} size={28} style={{ boxShadow: '0 1px 3px rgba(15,17,23,0.15)' }} />
    </div>
  );
};

export const TasksHero = () => {
  const done = TASKS.filter(t => t.state === 'done').length;
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
            background: SUCCESS,
            boxShadow: `0 0 0 5px ${SUCCESS}38`,
          }} />
          <span style={{ fontSize: 19, fontWeight: 800, color: TEXT, letterSpacing: '-0.015em' }}>
            Tasks · This Week
          </span>
        </div>
        <span style={{
          fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
          color: PRIMARY,
          background: `${PRIMARY}24`,
          padding: '5px 10px', borderRadius: 999,
        }}>{done}/{TASKS.length} DONE</span>
      </div>

      {/* Task stack */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {TASKS.map((t, i) => <TaskRow key={i} t={t} />)}
      </div>
    </div>
  );
};

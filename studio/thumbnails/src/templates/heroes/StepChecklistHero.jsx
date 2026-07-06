// Step Checklist hero — topic-agnostic numbered how-to / tutorial stepper.
//
// Family: CHECKLIST (see ../index.js). Built for owners who make how-to and
// tutorial videos (fix a tap, ice a cake, set up a tool) and don't have a
// product surface to caricature. The iconic silhouette is a vertical column
// of numbered step nodes joined by a rail: the top steps are ticked (done),
// one is active, the rest are queued. Reads as "a step-by-step guide" at
// 25% zoom without any text.
//
// Colours flow entirely through ../../brand.js so the hero reskins with the
// owner's brand.json (and looks coherent on the neutral starter brand). The
// only literals are the brand-independent neutral shadow/border that every
// hero in this studio shares.

import React from 'react';
import { PANEL, PRIMARY, PRIMARY_DEEP, SLATE, SUCCESS, TEXT, TEXT_MUTED } from '../../brand.js';

// Generic, universally-applicable steps — the shape is the message, not the
// words. Kept positive and topic-neutral so any how-to reuses them as-is.
const STEPS = [
  { title: 'Get your tools ready',    meta: 'Everything in one place', state: 'done' },
  { title: 'Set up your workspace',   meta: 'Clear and prepped',       state: 'done' },
  { title: 'Follow the first step',   meta: 'Nice and simple',         state: 'done' },
  { title: 'Make the key adjustment', meta: 'The part that matters',   state: 'active' },
  { title: 'Test the result',         meta: 'Confirm it works',        state: 'todo' },
  { title: 'Add the finishing touch', meta: 'Make it look great',      state: 'todo' },
  { title: 'Review and tidy up',      meta: 'Ready to share',          state: 'todo' },
  { title: 'Enjoy the result',        meta: 'You did it',              state: 'todo' },
];

const ROW_GAP = 10; // vertical spacing between step rows; the rail bridges it

const StepNode = ({ n, state }) => {
  if (state === 'done') {
    return (
      <div style={{
        width: 34, height: 34, borderRadius: '50%',
        background: SUCCESS, color: PANEL,
        fontSize: 16, fontWeight: 800,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0, zIndex: 1,
        boxShadow: `0 2px 6px ${SUCCESS}4d`,
      }}>✓</div>
    );
  }
  if (state === 'active') {
    return (
      <div style={{
        width: 34, height: 34, borderRadius: '50%',
        background: PRIMARY, color: PANEL,
        fontSize: 15, fontWeight: 800,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0, zIndex: 1,
        boxShadow: `0 0 0 5px ${PRIMARY}2b`,
      }}>{n}</div>
    );
  }
  return (
    <div style={{
      width: 34, height: 34, borderRadius: '50%',
      background: PANEL, color: SLATE,
      border: `2px solid ${SLATE}59`,
      fontSize: 15, fontWeight: 800,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      flexShrink: 0, zIndex: 1,
    }}>{n}</div>
  );
};

const StepRow = ({ s, n, isFirst, isLast, prevDone }) => {
  const done = s.state === 'done';
  const active = s.state === 'active';
  return (
    <div style={{
      display: 'flex', gap: 13, alignItems: 'stretch',
      marginBottom: isLast ? 0 : ROW_GAP,
    }}>
      {/* Stepper rail — flex column; segments flex to fill, circle centred.
          The bottom segment's negative margin bridges the row gap so the
          rail reads as one continuous line through every node. */}
      <div style={{ width: 34, flexShrink: 0, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <div style={{
          width: 3, flex: 1, borderRadius: 3,
          background: isFirst ? 'transparent' : (prevDone ? `${SUCCESS}66` : `${SLATE}33`),
        }} />
        <StepNode n={n} state={s.state} />
        <div style={{
          width: 3, flex: 1, borderRadius: 3,
          marginBottom: isLast ? 0 : -ROW_GAP,
          background: isLast ? 'transparent' : (done ? `${SUCCESS}66` : `${SLATE}33`),
        }} />
      </div>

      {/* Step card */}
      <div style={{
        flex: 1, minWidth: 0,
        background: active ? `${PRIMARY}0f` : PANEL,
        border: active ? `1.5px solid ${PRIMARY}59` : '1px solid rgba(226,232,240,0.7)',
        borderRadius: 12,
        padding: '11px 14px',
        boxShadow: active ? `0 6px 16px ${PRIMARY}1f` : 'none',
        opacity: done ? 0.72 : 1,
        display: 'flex', flexDirection: 'column', gap: 3,
      }}>
        <div style={{
          fontSize: 15, fontWeight: 800,
          color: done ? TEXT_MUTED : TEXT,
          letterSpacing: '-0.015em', lineHeight: 1.2,
          textDecoration: done ? 'line-through' : 'none',
          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
        }}>{s.title}</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {active ? (
            <span style={{
              fontSize: 9, fontWeight: 800, letterSpacing: '0.12em',
              color: PRIMARY_DEEP, background: `${PRIMARY}24`,
              padding: '2px 8px', borderRadius: 999,
            }}>● DOING NOW</span>
          ) : (
            <span style={{
              fontSize: 9, fontWeight: 800, letterSpacing: '0.12em',
              color: done ? SUCCESS : SLATE,
              background: done ? `${SUCCESS}1f` : `${SLATE}1a`,
              padding: '2px 8px', borderRadius: 999,
            }}>{done ? '✓ DONE' : `STEP ${n}`}</span>
          )}
          <span style={{ fontSize: 10.5, fontWeight: 600, color: TEXT_MUTED }}>{s.meta}</span>
        </div>
      </div>
    </div>
  );
};

export const StepChecklistHero = () => {
  const done = STEPS.filter(s => s.state === 'done').length;
  return (
    <div style={{
      background: PANEL,
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
            How-To Steps
          </span>
        </div>
        <span style={{
          fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
          color: PRIMARY, background: `${PRIMARY}22`,
          padding: '5px 10px', borderRadius: 999,
        }}>{done} / {STEPS.length} DONE</span>
      </div>

      {/* Step stack — bleeds off the bottom */}
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {STEPS.map((s, i) => (
          <StepRow
            key={i}
            s={s}
            n={i + 1}
            isFirst={i === 0}
            isLast={i === STEPS.length - 1}
            prevDone={i > 0 && STEPS[i - 1].state === 'done'}
          />
        ))}
      </div>
    </div>
  );
};

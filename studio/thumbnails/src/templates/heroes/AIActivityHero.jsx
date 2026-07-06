// AI Activity hero — the original fallback. A vertical list of agent-style
// activity items with done/progress/pending states. Used when a thumbnail
// hasn't been given a topic-specific hero yet, OR for thumbnails where the
// "AI is working across your CRM" framing genuinely fits (Agent Hub, Fill
// with AI, etc.).
//
// The 22 tutorial thumbnails should EACH get a dedicated topic-specific
// hero — kanban for Pipeline, conversation thread for SMS, dashboard charts
// for Reports, etc. See heroes/index.js for the registry.

import React from 'react';
import { BORDER, PRIMARY, SUCCESS, TEXT } from '../../brand.js';

const DEFAULT_ITEMS = [
  { state: 'done',     text: 'Sent quote to Amir K.' },
  { state: 'done',     text: 'Booked Sasha R. - 9:00 AM' },
  { state: 'done',     text: 'Followed up with Jordan P.' },
  { state: 'done',     text: 'Generated weekly report' },
  { state: 'done',     text: 'Drafted SMS for Marguerite V.' },
  { state: 'done',     text: 'Closed deal with Tomas L.' },
  { state: 'progress', text: 'Updating 12 deal statuses' },
  { state: 'pending',  text: 'Queue follow-ups for new Leads' },
  { state: 'pending',  text: 'Open Service Requests' },
  { state: 'pending',  text: 'Score new inbound leads' },
];

export const AIActivityHero = ({ data = {} }) => {
  const items = data.items || DEFAULT_ITEMS;
  return (
    <div style={{
      background: '#fff',
      borderRadius: 18,
      padding: 28,
      boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
      display: 'flex', flexDirection: 'column',
    }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{
            width: 12, height: 12, borderRadius: '50%',
            background: SUCCESS,
            boxShadow: `0 0 0 5px ${SUCCESS}38`,
          }} />
          <span style={{ fontSize: 22, fontWeight: 800, color: TEXT, letterSpacing: '-0.015em' }}>
            AI Activity
          </span>
        </div>
        <span style={{
          fontSize: 12, fontWeight: 800, letterSpacing: '0.14em',
          color: PRIMARY,
          background: `${PRIMARY}24`,
          padding: '6px 12px', borderRadius: 999,
        }}>
          LIVE
        </span>
      </div>

      {/* Items */}
      <div style={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
        {items.map((item, i) => {
          const done = item.state === 'done';
          const progress = item.state === 'progress';
          return (
            <div key={i} style={{
              display: 'flex', alignItems: 'center', gap: 16,
              padding: '14px 0',
              borderBottom: i < items.length - 1 ? `1px solid rgba(226,232,240,0.6)` : 'none',
            }}>
              {done && (
                <div style={{
                  width: 32, height: 32, borderRadius: '50%',
                  background: SUCCESS,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  color: '#fff', fontSize: 18, fontWeight: 800,
                  flexShrink: 0,
                  boxShadow: `0 2px 6px ${SUCCESS}4d`,
                }}>✓</div>
              )}
              {progress && (
                <div style={{
                  width: 32, height: 32, borderRadius: '50%',
                  background: `${PRIMARY}24`,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  flexShrink: 0,
                  position: 'relative',
                }}>
                  <div style={{
                    width: 22, height: 22, borderRadius: '50%',
                    border: `3px solid ${PRIMARY}`,
                    borderTopColor: 'transparent',
                    transform: 'rotate(45deg)',
                  }} />
                </div>
              )}
              {item.state === 'pending' && (
                <div style={{
                  width: 32, height: 32, borderRadius: '50%',
                  border: `2px solid ${BORDER}`,
                  flexShrink: 0,
                }} />
              )}
              <div style={{
                fontSize: 19,
                fontWeight: progress ? 800 : 600,
                color: done ? 'rgba(15,17,23,0.50)' : (progress ? TEXT : 'rgba(15,17,23,0.75)'),
                textDecoration: done ? 'line-through' : 'none',
                lineHeight: 1.3, flex: 1,
                letterSpacing: '-0.01em',
              }}>{item.text}</div>
              {progress && (
                <span style={{
                  fontSize: 12, fontWeight: 800, color: PRIMARY, letterSpacing: '0.10em',
                  background: `${PRIMARY}24`,
                  padding: '4px 9px', borderRadius: 6,
                }}>
                  NOW
                </span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

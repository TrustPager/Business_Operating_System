// Post 4 — AI Agents. Live-call card hero under a top headline.
// Ported faithfully from MARKETING/SOCIAL_MEDIA/ig/post-4-agents.jsx.

import React from 'react';
import { IG, igGradText, igSerifEm, FONT_GEIST, PostFrame } from './shell.jsx';

export function AgentsPost() {
  const accent = IG.green;
  return (
    <PostFrame>
      {/* HEADLINE BLOCK — top */}
      <div style={{
        position: 'relative', zIndex: 3,
        padding: '80px 80px 0',
      }}>
        <h1 style={{
          fontSize: 102,
          lineHeight: 0.92,
          letterSpacing: '-.045em',
          fontWeight: 700,
          margin: 0,
          color: IG.ink,
        }}>
          Your business, <em style={igSerifEm}>running</em> <span style={igGradText}>itself.</span>
        </h1>
        <p style={{
          fontSize: 30,
          lineHeight: 1.3,
          color: IG.muted,
          marginTop: 28,
          fontWeight: 400,
          letterSpacing: '-.005em',
        }}>
          We build the agents.<br/>
          They work 24/7.
        </p>
      </div>

      {/* LIVE CALL CARD — bottom hero */}
      <div style={{
        position: 'absolute',
        top: 420,
        left: 70,
        right: -70,
        zIndex: 2,
        transform: 'rotate(-2deg)',
      }}>
        <div style={{
          background: 'white',
          borderRadius: 28,
          padding: '36px 40px 40px',
          boxShadow:
            '0 80px 160px -40px rgba(52,211,153,.45),' +
            '0 12px 36px rgba(0,0,0,.08)',
          border: '1px solid rgba(0,0,0,.06)',
        }}>
          <div style={{
            display: 'flex', alignItems: 'center', gap: 18,
            paddingBottom: 22,
            borderBottom: '1px dashed rgba(0,0,0,.1)',
            marginBottom: 22,
          }}>
            <div style={{
              width: 78, height: 78, borderRadius: '50%',
              background: `linear-gradient(135deg, ${IG.blue} 0%, ${IG.purple} 55%, ${IG.pink} 100%)`,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: '0 12px 28px rgba(116,117,253,.45), inset 0 1px 0 rgba(255,255,255,.3)',
            }}>
              <svg width="34" height="34" viewBox="0 0 24 24" fill="none">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.95.37 1.88.71 2.77a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.31-1.31a2 2 0 0 1 2.11-.45c.89.34 1.82.58 2.77.71A2 2 0 0 1 22 16.92z" stroke="white" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <div style={{ flex: 1 }}>
              <div style={{
                fontFamily: '"DM Serif Display", Georgia, serif',
                fontStyle: 'italic',
                fontSize: 44,
                color: IG.ink,
                lineHeight: 1,
                letterSpacing: '-.01em',
              }}>Evie</div>
              <div style={{
                fontSize: 16,
                fontFamily: FONT_GEIST,
                color: IG.muted,
                letterSpacing: '.14em',
                marginTop: 8,
                fontWeight: 700,
                textTransform: 'uppercase',
              }}>AI Receptionist · Live</div>
            </div>
            <div style={{
              display: 'flex', alignItems: 'center', gap: 11,
              padding: '11px 18px',
              borderRadius: 999,
              background: IG.greenTint,
              color: '#059669',
              fontFamily: FONT_GEIST,
              fontSize: 16, fontWeight: 700,
              letterSpacing: '.08em',
            }}>
              <span style={{
                width: 10, height: 10, borderRadius: '50%',
                background: IG.green,
                boxShadow: `0 0 0 5px ${IG.green}33`,
              }}/>
              00:42
            </div>
          </div>

          {[
            { who: 'Caller', text: 'Hi — do you do emergency leak repair?' },
            { who: 'Evie',   text: 'We do. I can get someone out today. What\'s the address?', ai: true },
            { who: 'Caller', text: '241 Noe Street. The kitchen ceiling is dripping.' },
            { who: 'Evie',   text: 'Got it. Marco can be there at 2pm — that work?', ai: true },
            { who: 'Caller', text: 'Yes, perfect.' },
            { who: 'Evie',   text: 'Booked for 2pm. Confirmation sent to your phone.', ai: true },
          ].map((m, i) => (
            <div key={i} style={{
              display: 'flex', gap: 18,
              padding: '14px 0',
              fontSize: 22,
              lineHeight: 1.45,
            }}>
              <span style={{
                fontFamily: FONT_GEIST,
                fontSize: 15,
                fontWeight: 700,
                color: m.ai ? '#059669' : IG.muted,
                letterSpacing: '.08em',
                minWidth: 100,
                paddingTop: 6,
                textTransform: 'uppercase',
              }}>{m.who}</span>
              <span style={{
                color: m.ai ? '#0d6e5a' : IG.ink,
                flex: 1,
                fontWeight: m.ai ? 500 : 400,
              }}>{m.text}</span>
            </div>
          ))}

          {/* Action footer — what Evie did */}
          <div style={{
            marginTop: 18,
            padding: '20px 22px',
            borderRadius: 16,
            background: IG.greenTint,
            border: `1px solid ${IG.green}33`,
          }}>
            <div style={{
              fontFamily: FONT_GEIST,
              fontSize: 12,
              color: '#059669',
              letterSpacing: '.14em',
              fontWeight: 700,
              textTransform: 'uppercase',
              marginBottom: 12,
            }}>Evie handled, automatically</div>
            {[
              'Checked Marco\'s schedule · 2pm open',
              'Created job in TrustPager',
              'Sent SMS confirmation',
              'Notified Marco via Slack',
            ].map((a, i) => (
              <div key={i} style={{
                display: 'flex', alignItems: 'center', gap: 12,
                padding: '6px 0',
                fontSize: 17,
                color: '#0d6e5a',
              }}>
                <span style={{
                  width: 18, height: 18, borderRadius: '50%',
                  background: IG.green,
                  color: 'white',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: 11, fontWeight: 800,
                }}>✓</span>
                {a}
              </div>
            ))}
          </div>
        </div>
      </div>
    </PostFrame>
  );
}

AgentsPost.templateMeta = { id: 'fp-agents', name: 'FinalPiece · AI Agents', size: { width: 1080, height: 1350 } };

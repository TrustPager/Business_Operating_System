// Post 3 — TrustPager CRM. Pipeline card hero under a top headline.
// Ported faithfully from MARKETING/SOCIAL_MEDIA/ig/post-3-crm.jsx.

import React from 'react';
import { IG, igGradText, igSerifEm, FONT_GEIST, PostFrame } from './shell.jsx';

export function CrmPost() {
  const accent = IG.purple;
  return (
    <PostFrame>
      {/* HEADLINE BLOCK — top */}
      <div style={{
        position: 'relative', zIndex: 3,
        padding: '80px 80px 0',
      }}>
        <h1 style={{
          fontSize: 110,
          lineHeight: 0.92,
          letterSpacing: '-.045em',
          fontWeight: 700,
          margin: 0,
          color: IG.ink,
        }}>
          Stop <em style={igSerifEm}>losing</em> <span style={igGradText}>customers.</span>
        </h1>
        <p style={{
          fontSize: 30,
          lineHeight: 1.3,
          color: IG.muted,
          marginTop: 28,
          fontWeight: 400,
          letterSpacing: '-.005em',
        }}>
          One CRM. Every channel.<br/>
          Built for service businesses.
        </p>
      </div>

      {/* UI HERO — bottom */}
      <div style={{
        position: 'absolute',
        top: 420,
        left: 60,
        right: -80,
        zIndex: 2,
        transform: 'rotate(-2deg)',
      }}>
        <div style={{
          background: 'white',
          borderRadius: 28,
          overflow: 'hidden',
          boxShadow:
            '0 80px 160px -40px rgba(116,117,253,.5),' +
            '0 12px 36px rgba(0,0,0,.08)',
          border: '1px solid rgba(0,0,0,.06)',
          padding: '34px 38px 38px',
        }}>
          <div style={{
            display: 'flex', alignItems: 'baseline', justifyContent: 'space-between',
            marginBottom: 26,
          }}>
            <div>
              <div style={{
                fontFamily: FONT_GEIST,
                fontSize: 14,
                color: IG.faint,
                letterSpacing: '.14em',
                fontWeight: 700,
                textTransform: 'uppercase',
              }}>Pipeline · Today</div>
              <div style={{
                fontFamily: '"DM Serif Display", Georgia, serif',
                fontStyle: 'italic',
                fontSize: 50,
                color: IG.ink,
                marginTop: 6,
                letterSpacing: '-.01em',
              }}>4 new leads</div>
            </div>
            <div style={{
              padding: '10px 18px',
              borderRadius: 999,
              background: IG.purpleTint,
              color: accent,
              fontSize: 16,
              fontWeight: 700,
              letterSpacing: '.04em',
            }}>+34% MoM</div>
          </div>

          {/* Channel summary */}
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
            gap: 10,
            marginBottom: 24,
          }}>
            {[
              { k: 'Web',   v: '8',  c: IG.blue },
              { k: 'AI',    v: '12', c: IG.green },
              { k: 'SMS',   v: '5',  c: IG.purple },
              { k: 'Email', v: '3',  c: IG.pink },
            ].map(s => (
              <div key={s.k} style={{
                padding: '14px 18px',
                borderRadius: 14,
                background: `${s.c}10`,
                border: `1px solid ${s.c}22`,
              }}>
                <div style={{
                  fontSize: 11,
                  fontFamily: FONT_GEIST,
                  fontWeight: 700,
                  color: s.c,
                  letterSpacing: '.14em',
                  textTransform: 'uppercase',
                }}>{s.k}</div>
                <div style={{
                  fontSize: 28, fontWeight: 700,
                  color: IG.ink, marginTop: 4,
                  letterSpacing: '-.02em', lineHeight: 1,
                }}>{s.v}</div>
              </div>
            ))}
          </div>

          {[
            { name: 'Amir K.',       ch: 'Website form',   stage: 'Quote sent', c: IG.purple, last: '2m ago' },
            { name: 'Sasha R.',      ch: 'AI call · Evie', stage: 'Booked ✓',   c: IG.green,  last: '14m ago' },
            { name: 'Jordan P.',     ch: 'SMS reply',      stage: 'New lead',   c: IG.blue,   last: '1h ago' },
            { name: 'Marguerite V.', ch: 'Email',          stage: 'Follow-up',  c: IG.pink,   last: '3h ago' },
            { name: 'Tomás L.',      ch: 'Google Ads',     stage: 'Quote sent', c: IG.blue,   last: '5h ago' },
            { name: 'Priya N.',      ch: 'AI call · Evie', stage: 'Booked ✓',   c: IG.green,  last: 'Yesterday' },
          ].map(r => (
            <div key={r.name} style={{
              display: 'flex', alignItems: 'center', gap: 18,
              padding: '20px 0',
              borderBottom: '1px solid rgba(0,0,0,.06)',
            }}>
              <div style={{
                width: 56, height: 56, borderRadius: '50%',
                background: r.c,
                color: 'white',
                fontWeight: 700, fontSize: 22,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                boxShadow: `0 6px 16px ${r.c}55`,
              }}>{r.name[0]}</div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 23, fontWeight: 600, color: IG.ink }}>{r.name}</div>
                <div style={{
                  fontSize: 16,
                  color: IG.muted,
                  marginTop: 3,
                }}>{r.ch} · <span style={{ color: IG.faint }}>{r.last}</span></div>
              </div>
              <div style={{
                padding: '9px 18px',
                borderRadius: 999,
                background: `${r.c}18`,
                color: r.c,
                fontSize: 15, fontWeight: 700,
                letterSpacing: '.04em',
              }}>{r.stage}</div>
            </div>
          ))}
        </div>
      </div>
    </PostFrame>
  );
}

CrmPost.templateMeta = { id: 'fp-crm', name: 'FinalPiece · CRM', size: { width: 1080, height: 1350 } };

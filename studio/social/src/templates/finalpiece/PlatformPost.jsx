// Post 1 — "The platform" intro. UI hero (dashboard) under a top headline.
// Ported faithfully from MARKETING/SOCIAL_MEDIA/ig/post-1-intro.jsx.

import React from 'react';
import { IG, igGradText, igSerifEm, FONT_GEIST, PostFrame } from './shell.jsx';

// FinalPiece dashboard — sidebar + pipeline.
function PlatformUI() {
  return (
    <div style={{
      background: 'white',
      borderRadius: 28,
      overflow: 'hidden',
      boxShadow:
        '0 80px 160px -40px rgba(116,117,253,.45),' +
        '0 12px 36px rgba(0,0,0,.08)',
      border: '1px solid rgba(0,0,0,.06)',
    }}>
      {/* Top bar */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 14,
        padding: '20px 28px',
        background: '#FAF8F2',
        borderBottom: '1px solid rgba(0,0,0,.05)',
      }}>
        <img src="/FinalPieceLogo.png" alt="" style={{ height: 30 }} />
        <div style={{ flex: 1 }} />
        <div style={{ display: 'flex', gap: 7 }}>
          <span style={{ width: 13, height: 13, borderRadius: '50%', background: '#FF6058' }} />
          <span style={{ width: 13, height: 13, borderRadius: '50%', background: '#FFBE2F' }} />
          <span style={{ width: 13, height: 13, borderRadius: '50%', background: '#28C941' }} />
        </div>
      </div>

      {/* Sidebar + content */}
      <div style={{ display: 'flex', minHeight: 900 }}>
        {/* Sidebar */}
        <div style={{
          width: 240,
          background: '#FCFAF5',
          borderRight: '1px solid rgba(0,0,0,.04)',
          padding: '26px 18px',
        }}>
          <div style={{
            fontFamily: FONT_GEIST,
            fontSize: 11,
            color: IG.faint,
            letterSpacing: '.16em',
            fontWeight: 700,
            textTransform: 'uppercase',
            padding: '0 16px 12px',
          }}>Workspace</div>
          {[
            { label: 'Website',     c: IG.blue,   active: false, badge: 'Live' },
            { label: 'TrustPager',  c: IG.purple, active: true,  badge: '4'    },
            { label: 'AI Agents',   c: IG.green,  active: false, badge: '24/7' },
            { label: 'Automations', c: IG.pink,   active: false, badge: '12'   },
            { label: 'Reports',     c: '#9ca3af',        active: false },
            { label: 'Reviews',     c: '#f59e0b',        active: false, badge: 'New'  },
            { label: 'Billing',     c: '#06b6d4',        active: false },
          ].map(item => (
            <div key={item.label} style={{
              display: 'flex', alignItems: 'center', gap: 14,
              padding: '14px 16px',
              borderRadius: 12,
              background: item.active ? 'white' : 'transparent',
              boxShadow: item.active ? '0 2px 8px rgba(0,0,0,.06)' : 'none',
              marginBottom: 6,
              fontSize: 17,
              fontWeight: item.active ? 600 : 500,
              color: item.active ? IG.ink : IG.muted,
            }}>
              <span style={{
                width: 12, height: 12, borderRadius: 4,
                background: item.c,
                boxShadow: `0 0 0 3px ${item.c}22`,
              }} />
              <span style={{ flex: 1 }}>{item.label}</span>
              {item.badge && (
                <span style={{
                  fontSize: 11,
                  fontWeight: 700,
                  color: item.active ? item.c : IG.faint,
                  background: item.active ? `${item.c}18` : 'transparent',
                  padding: item.active ? '3px 8px' : 0,
                  borderRadius: 999,
                  letterSpacing: '.04em',
                }}>{item.badge}</span>
              )}
            </div>
          ))}
        </div>

        {/* Main content — pipeline */}
        <div style={{ flex: 1, padding: 28 }}>
          <div style={{
            display: 'flex', alignItems: 'baseline', justifyContent: 'space-between',
            marginBottom: 22,
          }}>
            <div>
              <div style={{
                fontFamily: FONT_GEIST,
                fontSize: 13,
                color: IG.faint,
                letterSpacing: '.14em',
                fontWeight: 700,
                textTransform: 'uppercase',
              }}>Pipeline</div>
              <div style={{
                fontSize: 38,
                fontWeight: 600,
                color: IG.ink,
                marginTop: 4,
                letterSpacing: '-.02em',
              }}>4 active leads</div>
            </div>
            <div style={{
              padding: '8px 14px',
              borderRadius: 999,
              background: IG.greenTint,
              color: '#059669',
              fontSize: 13,
              fontWeight: 700,
              letterSpacing: '.06em',
            }}>+34% MoM</div>
          </div>

          {/* Stat strip */}
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
            gap: 12,
            marginBottom: 22,
          }}>
            {[
              { k: 'Booked', v: '12', sub: 'this week', c: IG.green },
              { k: 'Pipeline value', v: '$48k', sub: 'open', c: IG.purple },
              { k: 'Reply time', v: '38s', sub: 'avg', c: IG.blue },
            ].map(s => (
              <div key={s.k} style={{
                padding: '14px 16px',
                borderRadius: 14,
                background: '#FAF8F2',
                border: '1px solid rgba(0,0,0,.04)',
              }}>
                <div style={{
                  fontSize: 11,
                  fontFamily: FONT_GEIST,
                  fontWeight: 700,
                  color: IG.faint,
                  letterSpacing: '.12em',
                  textTransform: 'uppercase',
                  marginBottom: 6,
                }}>{s.k}</div>
                <div style={{
                  fontSize: 28,
                  fontWeight: 700,
                  color: IG.ink,
                  letterSpacing: '-.02em',
                  lineHeight: 1,
                }}>{s.v}</div>
                <div style={{
                  fontSize: 12,
                  color: s.c,
                  fontWeight: 600,
                  marginTop: 4,
                }}>{s.sub}</div>
              </div>
            ))}
          </div>

          {[
            { name: 'Amir K.',       ch: 'Website form',   stage: 'Quote sent', c: IG.purple },
            { name: 'Sasha R.',      ch: 'AI · Evie',      stage: 'Booked ✓',   c: IG.green },
            { name: 'Jordan P.',     ch: 'SMS reply',      stage: 'New lead',   c: IG.blue },
            { name: 'Marguerite V.', ch: 'Email',          stage: 'Follow-up',  c: IG.pink },
            { name: 'Tomás L.',      ch: 'Google Ads',     stage: 'Quote sent', c: IG.blue },
            { name: 'Priya N.',      ch: 'AI · Evie',      stage: 'New lead',   c: IG.green },
          ].map(r => (
            <div key={r.name} style={{
              display: 'flex', alignItems: 'center', gap: 16,
              padding: '15px 18px',
              borderRadius: 14,
              background: '#FAF8F2',
              marginBottom: 10,
            }}>
              <div style={{
                width: 44, height: 44, borderRadius: '50%',
                background: r.c,
                color: 'white',
                fontWeight: 700, fontSize: 17,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                boxShadow: `0 4px 12px ${r.c}55`,
              }}>{r.name[0]}</div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 18, fontWeight: 600, color: IG.ink }}>{r.name}</div>
                <div style={{
                  fontSize: 14,
                  color: IG.muted,
                  marginTop: 2,
                }}>{r.ch}</div>
              </div>
              <div style={{
                padding: '7px 14px',
                borderRadius: 999,
                background: `${r.c}18`,
                color: r.c,
                fontSize: 13, fontWeight: 700,
                letterSpacing: '.04em',
              }}>{r.stage}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export function PlatformPost() {
  return (
    <PostFrame>
      {/* HEADLINE BLOCK — top */}
      <div style={{
        position: 'relative', zIndex: 3,
        padding: '80px 80px 0',
      }}>
        <h1 style={{
          fontSize: 96,
          lineHeight: 0.92,
          letterSpacing: '-.045em',
          fontWeight: 700,
          margin: 0,
          color: IG.ink,
        }}>
          Automate your <em style={igSerifEm}>whole</em> <span style={igGradText}>business.</span>
        </h1>
        <p style={{
          fontSize: 30,
          lineHeight: 1.3,
          color: IG.muted,
          marginTop: 28,
          fontWeight: 400,
          letterSpacing: '-.005em',
        }}>
          The last piece of software you'll ever need.
        </p>
      </div>

      {/* UI HERO — bottom, dominant */}
      <div style={{
        position: 'absolute',
        top: 420,
        left: 70,
        right: -90,
        zIndex: 2,
        transform: 'rotate(-2deg)',
      }}>
        <PlatformUI />
      </div>
    </PostFrame>
  );
}

PlatformPost.templateMeta = { id: 'fp-platform', name: 'FinalPiece · Platform', size: { width: 1080, height: 1350 } };

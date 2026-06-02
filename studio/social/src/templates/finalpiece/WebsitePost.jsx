// Post 2 — Website. Real screenshot mockup in a browser frame.
// Ported faithfully from MARKETING/SOCIAL_MEDIA/ig/post-2-website.jsx.

import React from 'react';
import { IG, igGradText, igSerifEm, FONT_GEIST, PostFrame } from './shell.jsx';

export function WebsitePost() {
  return (
    <PostFrame>
      {/* HEADLINE BLOCK — top */}
      <div style={{
        position: 'relative', zIndex: 3,
        padding: '80px 80px 0',
      }}>
        <h1 style={{
          fontSize: 116,
          lineHeight: 0.92,
          letterSpacing: '-.045em',
          fontWeight: 700,
          margin: 0,
          color: IG.ink,
        }}>
          Live in <em style={igSerifEm}>two</em> <span style={igGradText}>weeks.</span>
        </h1>
        <p style={{
          fontSize: 30,
          lineHeight: 1.3,
          color: IG.muted,
          marginTop: 28,
          fontWeight: 400,
          letterSpacing: '-.005em',
        }}>
          We design it, build it, ship it.<br/>
          You just approve.
        </p>
      </div>

      {/* UI HERO */}
      <div style={{
        position: 'absolute',
        top: 420,
        left: 80,
        right: -100,
        zIndex: 2,
        transform: 'rotate(-2deg)',
      }}>
        <div style={{
          background: '#0a1a1c',
          borderRadius: 28,
          overflow: 'hidden',
          boxShadow:
            '0 80px 160px -40px rgba(47,153,253,.5),' +
            '0 12px 36px rgba(0,0,0,.08)',
          border: '1px solid rgba(0,0,0,.06)',
        }}>
          {/* Browser bar */}
          <div style={{
            display: 'flex', alignItems: 'center', gap: 12,
            padding: '14px 20px',
            background: '#EFEBE3',
            borderBottom: '1px solid rgba(0,0,0,.05)',
          }}>
            <div style={{ display: 'flex', gap: 6 }}>
              <span style={{ width: 12, height: 12, borderRadius: '50%', background: '#FF6058' }} />
              <span style={{ width: 12, height: 12, borderRadius: '50%', background: '#FFBE2F' }} />
              <span style={{ width: 12, height: 12, borderRadius: '50%', background: '#28C941' }} />
            </div>
            <div style={{
              flex: 1,
              background: 'white',
              borderRadius: 8,
              padding: '7px 16px',
              fontSize: 14,
              color: '#6b7280',
              fontFamily: FONT_GEIST,
              fontWeight: 500,
              textAlign: 'center',
              border: '1px solid rgba(0,0,0,.04)',
              display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6,
            }}>
              <span style={{ color: '#10b981', fontSize: 11 }}>●</span>
              ingles.com.au
            </div>
          </div>

          <img
            src="/portfolio_website_Ingles.webp"
            alt=""
            style={{
              display: 'block',
              width: '100%',
              height: 'auto',
            }}
          />
        </div>
      </div>
    </PostFrame>
  );
}

WebsitePost.templateMeta = { id: 'fp-website', name: 'FinalPiece · Website', size: { width: 1080, height: 1350 } };

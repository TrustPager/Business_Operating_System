import React from 'react';
import {
  PRIMARY, PRIMARY_DEEP, PRIMARY_TINT, PRIMARY_TINT_DEEP, ACCENT, SUCCESS,
  TEXT, TEXT_MUTED, PANEL, BORDER, PAGE_BG,
  FONT_BODY, LOGO_URL, NAME, GRADIENT,
} from '../brand.js';

// HeroCardCTA — 1200×460 nurture-email CTA.
//
// Layout: split 580/500. Left = brand topbar + headline group anchored to
// the top + pill button anchored to the bottom. Right = white card with
// a header + compact 4-row benefit list. Card bottom + button bottom share
// the same baseline.
//
// Every visual surface flows from BOS/brand/brand.json via ../brand.js —
// no hex literals inline. Edit brand.json (or run /brand-my-workspace)
// to rebrand.

const CANVAS_W = 1200;
const CANVAS_H = 460;

const StarIcon = ({ size = 18, color = PRIMARY }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill={color}>
    <path d="M12 2l2.6 6.6 7 .5-5.3 4.6 1.6 6.9L12 16.9 6.1 20.6l1.6-6.9L2.4 9.1l7-.5L12 2z" />
  </svg>
);

const PlayIcon = ({ size = 18, color = '#fff' }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill={color}>
    <path d="M8 5v14l11-7-11-7z" />
  </svg>
);

export const HeroCardCTA = ({ data }) => {
  const { eyebrow, headline, subhead, button, card } = data || {};
  const features = card?.features || [];

  return (
    <div
      className="template-canvas"
      style={{
        width: CANVAS_W,
        height: CANVAS_H,
        position: 'relative',
        overflow: 'hidden',
        // Branded canvas (soft off-white + brand-tinted radial washes)
        // clipped at 24px radius. Only the INSIDE of the radius gets the
        // branded fill; the corner space OUTSIDE the radius stays alpha
        // because render.js calls puppeteer with omitBackground:true.
        // Result: a branded card that floats cleanly on the email body
        // (white email bg shows through the rounded corners).
        background: PAGE_BG,
        backgroundImage: `radial-gradient(circle at 0% 0%, ${PRIMARY}1a, transparent 45%), radial-gradient(circle at 100% 100%, ${ACCENT}14, transparent 40%)`,
        borderRadius: 24,
        fontFamily: FONT_BODY,
        color: TEXT,
      }}
    >
      {/* === TOP BAR === */}
      <div style={{ position: 'absolute', top: 32, left: 56, right: 56, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <img src={LOGO_URL} alt={NAME} style={{ height: 40, width: 'auto', display: 'block' }} />
        {eyebrow && (
          <div style={{ background: PRIMARY_TINT, color: PRIMARY_DEEP, fontSize: 13, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', padding: '10px 18px', borderRadius: 999 }}>
            {eyebrow}
          </div>
        )}
      </div>

      {/* === BOTTOM STROKES (drawn before card so card paints over) === */}
      <svg width={CANVAS_W} height={60} viewBox={`0 0 ${CANVAS_W} 60`} style={{ position: 'absolute', bottom: 0, left: 0, display: 'block' }}>
        <defs>
          <linearGradient id="hcStrokeA" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={PRIMARY} stopOpacity="0" />
            <stop offset="35%" stopColor={PRIMARY} stopOpacity="1" />
            <stop offset="100%" stopColor={ACCENT} stopOpacity="1" />
          </linearGradient>
          <linearGradient id="hcStrokeB" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={ACCENT} stopOpacity="0" />
            <stop offset="50%" stopColor={ACCENT} stopOpacity="0.85" />
            <stop offset="100%" stopColor={PRIMARY} stopOpacity="1" />
          </linearGradient>
        </defs>
        <line x1="0" y1="50" x2={CANVAS_W} y2="6" stroke="url(#hcStrokeA)" strokeWidth="3" strokeLinecap="round" />
        <line x1="0" y1="56" x2={CANVAS_W} y2="14" stroke="url(#hcStrokeB)" strokeWidth="2" strokeLinecap="round" opacity="0.55" />
      </svg>

      {/* === LEFT COLUMN === */}
      <div style={{ position: 'absolute', top: 96, left: 56, bottom: 52, width: 580, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
          {headline && (
            <h1 style={{ fontSize: 60, lineHeight: 1.02, fontWeight: 800, letterSpacing: '-0.025em', color: TEXT, whiteSpace: 'pre-line', margin: 0 }}>
              {headline}
            </h1>
          )}
          {subhead && (
            <p style={{ fontSize: 20, lineHeight: 1.45, fontWeight: 500, color: TEXT_MUTED, maxWidth: 520, margin: 0 }}>
              {subhead}
            </p>
          )}
        </div>
        {button?.label && (
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: 12, background: PRIMARY, color: '#fff', padding: '16px 26px', borderRadius: 999, fontSize: 19, fontWeight: 700, letterSpacing: '-0.01em', boxShadow: `0 10px 24px -8px ${PRIMARY}8c` }}>
              <span style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: 32, height: 32, borderRadius: 999, background: 'rgba(255,255,255,0.18)' }}>
                <PlayIcon size={18} />
              </span>
              {button.label}
            </div>
          </div>
        )}
      </div>

      {/* === RIGHT CARD === */}
      <div style={{ position: 'absolute', top: 96, right: 56, bottom: 52, width: 500, background: PANEL, border: `1px solid ${BORDER}`, borderRadius: 18, padding: 14, boxShadow: '0 30px 60px -24px rgba(15,23,42,0.18), 0 8px 20px -8px rgba(15,23,42,0.08)', display: 'flex', flexDirection: 'column', gap: 10 }}>
        {card?.title && (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 10 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <span style={{ display: 'inline-block', width: 11, height: 11, borderRadius: 999, background: SUCCESS, boxShadow: `0 0 0 4px ${SUCCESS}2e` }} />
              <span style={{ fontSize: 22, fontWeight: 700, color: TEXT, letterSpacing: '-0.01em' }}>
                {card.title}
              </span>
            </div>
            {card?.status && (
              <span style={{ background: PRIMARY_TINT, color: PRIMARY_DEEP, fontSize: 12, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', padding: '6px 12px', borderRadius: 999 }}>
                {card.status}
              </span>
            )}
          </div>
        )}

        {features.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, flex: 1, minHeight: 0 }}>
            {features.map((f, i) => (
              <div key={i} style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 14, background: PANEL, border: `1px solid ${BORDER}`, borderRadius: 14, padding: '0 16px 0 10px', minWidth: 0 }}>
                <div style={{ width: 40, height: 40, borderRadius: 10, background: PRIMARY_TINT, border: `1px solid ${PRIMARY_TINT_DEEP}`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                  <StarIcon size={20} color={PRIMARY} />
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 2, minWidth: 0 }}>
                  <div style={{ fontSize: 16, fontWeight: 700, color: TEXT, letterSpacing: '-0.005em', lineHeight: 1.2 }}>
                    {f.label}
                  </div>
                  {f.description && (
                    <div style={{ fontSize: 13, fontWeight: 500, color: TEXT_MUTED, lineHeight: 1.3 }}>
                      {f.description}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

HeroCardCTA.templateMeta = {
  id: 'hero-card-cta',
  name: 'Hero Card CTA',
  size: { width: CANVAS_W, height: CANVAS_H },
};

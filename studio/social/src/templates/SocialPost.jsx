// ===========================================================================
// SocialPost — the canonical Social Studio template.
//
// ONE design language, FOUR canvas sizes. Each exported wrapper
// (SocialSquare / SocialPortrait / SocialLinkedIn / SocialX) renders this
// same component with a different `format`, and carries its own static
// `templateMeta` (id + pixel size) so the studio sidebar + the headless
// renderer know how big to shoot it.
//
//   social-square    1080 × 1080   Instagram square / feed     (portrait layout)
//   social-portrait  1080 × 1350   Instagram portrait / feed   (portrait layout)
//   social-linkedin  1200 × 627    LinkedIn link/feed image     (landscape layout)
//   social-x         1600 × 900    X (Twitter) 16:9             (landscape layout)
//
// ---------------------------------------------------------------------------
// ANATOMY (same composition at every size)
//
//   +--------------------------------------------------+
//   | [logo]                              [eyebrow]    |   ← top bar
//   |                                                  |
//   |   Big Headline With                              |
//   |   one //gradient// word + one *serif* word       |   ← headline block
//   |   Short supporting subhead line.                 |
//   |                                  [ visual card ] |   ← optional visual
//   |                                                  |     (right in landscape,
//   | @yourhandle                       [ CTA pill ]   |     below in portrait)
//   +--------------------------------------------------+   ← footer bar
//
// Portrait formats stack the visual UNDER the headline; landscape formats
// put it to the RIGHT. No absolute positioning for content — a flex column
// with space-between means nothing ever overflows the frame.
//
// ---------------------------------------------------------------------------
// BRAND RULES (lessons carried over from the thumbnail studio)
//   - All colour flows from BOS/brand/brand.json via ../brand.js. NO hex
//     literals inline. Editing brand.json (or /brand-my-workspace) reskins
//     every post.
//   - Exactly ONE gradient accent word (`accentWord`) and at most ONE serif
//     italic emphasis word (`emphasisWord`) per headline. More than one of
//     each and the eye has nowhere to land.
//   - Stay on the brand palette in any visual card chrome. Don't introduce
//     red / orange / purple.
//   - Headlines are short: 3–8 words. The post is a billboard, not a paragraph.
//   - Positive framing only in the headline (no "Stop", "Don't", "Never").
//
// ---------------------------------------------------------------------------
// DATA SHAPE (every field optional except headline)
//   {
//     "eyebrow":      "NEW",                         // small pill, top-right
//     "headline":     "Run your whole business",     // the billboard line
//     "accentWord":   "whole",                       // gets the brand gradient
//     "emphasisWord": "business",                    // gets serif italic
//     "subhead":      "One short supporting line.",
//     "handle":       "@yourbusiness",               // footer-left
//     "cta":          "Book a demo",                 // footer-right pill
//     // ONE of the following visuals (all optional):
//     "card":  { "title": "Pipeline", "status": "LIVE",
//                "rows": [ { "label": "Booked", "value": "12", "tone": "success" } ] },
//     "stats": [ { "label": "Reply time", "value": "38s", "sub": "avg" } ],
//     "quote": { "text": "…", "name": "Saskia W.", "role": "Owner, Acme Plumbing",
//                "avatar": "https://…/photo.jpg" }   // optional; omit → initials monogram
//   }
// ===========================================================================

import React from 'react';
import {
  PRIMARY, PRIMARY_DEEP, PRIMARY_TINT, ACCENT, SUCCESS,
  TEXT, TEXT_MUTED, PANEL, BORDER, PAGE_BG,
  FONT_BODY, FONT_SERIF, LOGO_URL, NAME, GRADIENT,
} from '../brand.js';

// --- Per-format spatial + type scale -------------------------------------
// Sizes are tuned so each format reads as a billboard at thumbnail scale.
const FORMATS = {
  square:   { w: 1080, h: 1080, orientation: 'portrait',  pad: 84, h1: 80, sub: 28, gap: 22 },
  portrait: { w: 1080, h: 1350, orientation: 'portrait',  pad: 88, h1: 90, sub: 30, gap: 26 },
  linkedin: { w: 1200, h: 627,  orientation: 'landscape', pad: 60, h1: 58, sub: 21, gap: 16 },
  x:        { w: 1600, h: 900,  orientation: 'landscape', pad: 84, h1: 80, sub: 28, gap: 22 },
};

const TONES = { success: SUCCESS, primary: PRIMARY, accent: ACCENT, muted: TEXT_MUTED };
const toneColor = (t) => TONES[t] || PRIMARY;

const escapeRegExp = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

// Render the headline with one gradient accent word + one serif emphasis word.
// Both match case-insensitively and may be multi-word phrases.
function renderHeadline(text, accentWord, emphasisWord) {
  if (!text) return null;
  const tokens = [accentWord, emphasisWord].filter(Boolean).map(escapeRegExp);
  if (!tokens.length) return text;
  const re = new RegExp(`(${tokens.join('|')})`, 'gi');
  const lc = (s) => (s || '').toLowerCase();
  return text.split(re).map((seg, i) => {
    if (accentWord && lc(seg) === lc(accentWord)) {
      return (
        <span
          key={i}
          style={{
            backgroundImage: GRADIENT,
            WebkitBackgroundClip: 'text',
            backgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            color: 'transparent',
          }}
        >{seg}</span>
      );
    }
    if (emphasisWord && lc(seg) === lc(emphasisWord)) {
      return (
        <em key={i} style={{ fontFamily: FONT_SERIF, fontStyle: 'italic', fontWeight: 600 }}>{seg}</em>
      );
    }
    return <React.Fragment key={i}>{seg}</React.Fragment>;
  });
}

// --- Optional visual: a clean product-ish list card ----------------------
const ListCard = ({ card, fmt }) => {
  const rows = card?.rows || [];
  return (
    <div style={{
      background: PANEL,
      border: `1px solid ${BORDER}`,
      borderRadius: 20,
      padding: fmt.orientation === 'landscape' ? 18 : 22,
      boxShadow: '0 40px 80px -32px rgba(15,23,42,0.28), 0 12px 28px -12px rgba(15,23,42,0.12)',
      display: 'flex',
      flexDirection: 'column',
      gap: 12,
      width: '100%',
    }}>
      {card?.title && (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 10 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span style={{ width: 12, height: 12, borderRadius: 999, background: SUCCESS, boxShadow: `0 0 0 5px ${SUCCESS}26` }} />
            <span style={{ fontSize: 24, fontWeight: 700, color: TEXT, letterSpacing: '-0.01em' }}>{card.title}</span>
          </div>
          {card?.status && (
            <span style={{ background: PRIMARY_TINT, color: PRIMARY_DEEP, fontSize: 12, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', padding: '6px 12px', borderRadius: 999 }}>
              {card.status}
            </span>
          )}
        </div>
      )}
      {rows.map((r, i) => (
        <div key={i} style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 14,
          background: PAGE_BG, border: `1px solid ${BORDER}`, borderRadius: 14, padding: '14px 18px',
        }}>
          <span style={{ fontSize: 18, fontWeight: 600, color: TEXT, letterSpacing: '-0.005em' }}>{r.label}</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            {r.value && <span style={{ fontSize: 18, fontWeight: 700, color: TEXT }}>{r.value}</span>}
            {r.tag && (
              <span style={{ fontSize: 13, fontWeight: 700, letterSpacing: '0.04em', color: toneColor(r.tone), background: `${toneColor(r.tone)}1a`, padding: '5px 12px', borderRadius: 999 }}>
                {r.tag}
              </span>
            )}
          </span>
        </div>
      ))}
    </div>
  );
};

// --- Optional visual: a stat strip ---------------------------------------
const StatStrip = ({ stats, fmt }) => (
  <div style={{
    display: 'grid',
    gridTemplateColumns: `repeat(${Math.min(stats.length, 3)}, 1fr)`,
    gap: 14,
    width: '100%',
  }}>
    {stats.slice(0, 3).map((s, i) => (
      <div key={i} style={{
        background: PANEL, border: `1px solid ${BORDER}`, borderRadius: 18, padding: '20px 22px',
        boxShadow: '0 24px 50px -28px rgba(15,23,42,0.22)',
      }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: TEXT_MUTED, letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 8 }}>
          {s.label}
        </div>
        <div style={{ fontSize: 44, fontWeight: 800, color: TEXT, letterSpacing: '-0.03em', lineHeight: 1 }}>
          {s.value}
        </div>
        {s.sub && <div style={{ fontSize: 15, fontWeight: 600, color: PRIMARY, marginTop: 6 }}>{s.sub}</div>}
      </div>
    ))}
  </div>
);

// --- Self-contained avatar -----------------------------------------------
// Quote posts default to a brand-tinted initials monogram so the studio has
// ZERO external image dependencies out of the box (the pack ships to other
// businesses — pulling faces off someone else's CDN is both broken and wrong).
// Pass `quote.avatar` (a URL) to use a real customer photo instead.
const initialsOf = (name = '') =>
  name.trim().split(/\s+/).slice(0, 2).map((w) => w[0] || '').join('').toUpperCase() || '★';

const InitialsAvatar = ({ name, size = 52 }) => (
  <div style={{
    width: size, height: size, borderRadius: '50%', flexShrink: 0,
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    background: PRIMARY_TINT, color: PRIMARY_DEEP,
    boxShadow: `0 0 0 2px ${PRIMARY}33`,
    fontWeight: 800, fontSize: Math.round(size * 0.36), letterSpacing: '-0.02em',
  }}>
    {initialsOf(name)}
  </div>
);

const QuoteAvatar = ({ quote }) => {
  if (quote.avatar) {
    return (
      <img src={quote.avatar} alt="" style={{
        width: 52, height: 52, borderRadius: '50%', objectFit: 'cover', flexShrink: 0,
        boxShadow: `0 0 0 2px ${PRIMARY}33`,
      }} />
    );
  }
  if (quote.name) return <InitialsAvatar name={quote.name} size={52} />;
  return null;
};

// --- Optional visual: a testimonial / quote ------------------------------
const QuoteCard = ({ quote }) => (
  <div style={{
    background: PANEL, border: `1px solid ${BORDER}`, borderRadius: 20, padding: 28,
    boxShadow: '0 40px 80px -32px rgba(15,23,42,0.28)',
    display: 'flex', flexDirection: 'column', gap: 20, width: '100%',
  }}>
    <div style={{ fontFamily: FONT_SERIF, fontStyle: 'italic', fontSize: 30, lineHeight: 1.35, color: TEXT, letterSpacing: '-0.01em' }}>
      “{quote.text}”
    </div>
    <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
      <QuoteAvatar quote={quote} />
      <div>
        {quote.name && <div style={{ fontSize: 18, fontWeight: 700, color: TEXT }}>{quote.name}</div>}
        {quote.role && <div style={{ fontSize: 15, fontWeight: 500, color: TEXT_MUTED, marginTop: 2 }}>{quote.role}</div>}
      </div>
    </div>
  </div>
);

const Visual = ({ data, fmt }) => {
  if (data?.card) return <ListCard card={data.card} fmt={fmt} />;
  if (data?.stats?.length) return <StatStrip stats={data.stats} fmt={fmt} />;
  if (data?.quote?.text) return <QuoteCard quote={data.quote} />;
  return null;
};

// --- The post ------------------------------------------------------------
function SocialPost({ format = 'square', data = {} }) {
  const fmt = FORMATS[format] || FORMATS.square;
  const landscape = fmt.orientation === 'landscape';
  const { eyebrow, headline, accentWord, emphasisWord, subhead, handle, cta } = data;
  const hasVisual = !!(data.card || data.stats?.length || data.quote?.text);

  // In landscape, never let the headline stretch the full width — cap it so
  // it wraps and anchors left (poster-style), leaving the right as negative
  // space. Without this, a headline-only 16:9 reads as a thin edge-to-edge
  // strip with dead bands above and below.
  const headlineMax = landscape ? (hasVisual ? 620 : Math.round((fmt.w - fmt.pad * 2) * 0.66)) : '100%';

  const HeadlineBlock = (
    <div style={{ display: 'flex', flexDirection: 'column', gap: Math.round(fmt.gap * 0.7), maxWidth: headlineMax }}>
      {headline && (
        <h1 style={{
          fontSize: fmt.h1,
          lineHeight: 0.98,
          fontWeight: 800,
          letterSpacing: '-0.035em',
          color: TEXT,
          margin: 0,
          whiteSpace: 'pre-line',
        }}>
          {renderHeadline(headline, accentWord, emphasisWord)}
        </h1>
      )}
      {subhead && (
        <p style={{ fontSize: fmt.sub, lineHeight: 1.4, fontWeight: 500, color: TEXT_MUTED, margin: 0, maxWidth: 640 }}>
          {subhead}
        </p>
      )}
    </div>
  );

  const VisualBlock = hasVisual ? (
    <div style={{ width: landscape ? 480 : '100%', flexShrink: 0, marginTop: landscape ? 0 : fmt.gap }}>
      <Visual data={data} fmt={fmt} />
    </div>
  ) : null;

  return (
    <div
      className="template-canvas"
      style={{
        width: fmt.w,
        height: fmt.h,
        position: 'relative',
        overflow: 'hidden',
        background: PAGE_BG,
        backgroundImage: `radial-gradient(circle at 8% 4%, ${PRIMARY}22, transparent 42%), radial-gradient(circle at 100% 100%, ${ACCENT}1c, transparent 46%)`,
        fontFamily: FONT_BODY,
        color: TEXT,
        display: 'flex',
        flexDirection: 'column',
        padding: fmt.pad,
      }}
    >
      {/* TOP BAR — logo + optional eyebrow */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexShrink: 0 }}>
        <img src={LOGO_URL} alt={NAME} style={{ height: landscape ? 40 : 48, width: 'auto', display: 'block' }} />
        {eyebrow && (
          <div style={{ background: PRIMARY_TINT, color: PRIMARY_DEEP, fontSize: landscape ? 13 : 15, fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', padding: '10px 18px', borderRadius: 999 }}>
            {eyebrow}
          </div>
        )}
      </div>

      {/* BODY — headline (+ visual). Centered vertically in the free space. */}
      <div style={{
        flex: 1,
        minHeight: 0,
        display: 'flex',
        flexDirection: landscape ? 'row' : 'column',
        alignItems: landscape ? 'center' : 'flex-start',
        justifyContent: landscape ? (hasVisual ? 'space-between' : 'flex-start') : 'center',
        gap: landscape ? fmt.pad * 0.7 : 0,
      }}>
        {HeadlineBlock}
        {VisualBlock}
      </div>

      {/* FOOTER — handle + CTA pill + thin gradient accent line */}
      <div style={{ flexShrink: 0, display: 'flex', flexDirection: 'column', gap: 16 }}>
        <div style={{
          height: 3, width: '100%', borderRadius: 999,
          backgroundImage: `linear-gradient(90deg, ${PRIMARY} 0%, ${ACCENT} 100%)`,
          opacity: 0.9,
        }} />
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16 }}>
          <span style={{ fontSize: landscape ? 18 : 22, fontWeight: 700, color: TEXT_MUTED, letterSpacing: '-0.01em' }}>
            {handle || ''}
          </span>
          {cta && (
            <span style={{
              display: 'inline-flex', alignItems: 'center', gap: 10,
              background: PRIMARY, color: '#fff',
              padding: landscape ? '12px 22px' : '15px 26px',
              borderRadius: 999, fontSize: landscape ? 17 : 20, fontWeight: 700, letterSpacing: '-0.01em',
              boxShadow: `0 12px 28px -10px ${PRIMARY}99`,
            }}>
              {cta}
              <span style={{ fontSize: landscape ? 18 : 22, lineHeight: 1 }}>→</span>
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

// --- Format wrappers (each carries its own templateMeta size) ------------
export const SocialSquare = (props) => <SocialPost {...props} format="square" />;
SocialSquare.templateMeta = { id: 'social-square', name: 'Instagram · Square', size: { width: 1080, height: 1080 } };

export const SocialPortrait = (props) => <SocialPost {...props} format="portrait" />;
SocialPortrait.templateMeta = { id: 'social-portrait', name: 'Instagram · Portrait', size: { width: 1080, height: 1350 } };

export const SocialLinkedIn = (props) => <SocialPost {...props} format="linkedin" />;
SocialLinkedIn.templateMeta = { id: 'social-linkedin', name: 'LinkedIn', size: { width: 1200, height: 627 } };

export const SocialX = (props) => <SocialPost {...props} format="x" />;
SocialX.templateMeta = { id: 'social-x', name: 'X (Twitter)', size: { width: 1600, height: 900 } };

export default SocialPost;

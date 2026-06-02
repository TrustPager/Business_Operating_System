// ===========================================================================
// FinalPiece rich-post shell — ported verbatim from the original
// MARKETING/SOCIAL_MEDIA/ig/post-shell.jsx (was window globals; now ESM).
//
// These four posts are bespoke, illustrated 1080×1350 Instagram designs with
// their OWN visual language (blue→purple→pink gradient, warm cream canvas,
// DM Serif Display emphasis, Geist body) — deliberately NOT the brand.json
// billboard look used by SocialPost.jsx. They're kept faithful to the
// originals. The generic, brand-driven template is SocialPost.jsx.
// ===========================================================================

import React from 'react';

export const IG = {
  // Foundations
  bg: '#FBF8F2',
  ink: '#0D0F1C',
  ink2: '#1a1d2e',
  muted: '#4a5162',
  faint: '#9ca3af',
  line: 'rgba(0,0,0,.08)',
  // Brand gradient stops
  blue: '#2F99FD',
  purple: '#7475FD',
  pink: '#D146FD',
  green: '#34D399',
  // Tints
  blueTint: '#E6F1FF',
  purpleTint: '#ECECFF',
  greenTint: '#E8F8F0',
  pinkTint: '#FBE8FF',
};

export const igGradText = {
  background: `linear-gradient(100deg, ${IG.blue} 0%, ${IG.purple} 50%, ${IG.pink} 100%)`,
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text',
};

export const igSerifEm = {
  fontFamily: '"DM Serif Display", Georgia, serif',
  fontStyle: 'italic',
  fontWeight: 400,
};

export const FONT_GEIST = '"Geist", -apple-system, BlinkMacSystemFont, "Inter", sans-serif';

// Outer canvas — every post sits inside this. Includes the warm wash.
// The root carries `.template-canvas` so the headless renderer screenshots it.
export function PostFrame({ children }) {
  return (
    <div
      className="template-canvas"
      style={{
        position: 'relative',
        width: 1080, height: 1350,
        background: IG.bg,
        color: IG.ink,
        fontFamily: FONT_GEIST,
        overflow: 'hidden',
      }}
    >
      {/* Warm radial wash — same as the website */}
      <div style={{
        position: 'absolute', inset: 0,
        backgroundImage:
          'radial-gradient(circle at 20% 25%, rgba(116,117,253,.08), transparent 45%),' +
          'radial-gradient(circle at 80% 75%, rgba(47,153,253,.06), transparent 45%),' +
          'radial-gradient(ellipse at 50% 0%, rgba(209,70,253,.07) 0%, transparent 55%)',
        pointerEvents: 'none',
      }} />
      {children}
    </div>
  );
}

// ============================================================================
// OgImage — 1200x630 (1.91:1) Open Graph image template.
// Brand-aware: every sample picks its brand, and the template reads colour,
// fonts, accent gradient and logo from that brand's preset.
// ============================================================================
//
// LAYOUT (1200x630, brand chrome)
// ------------------------------
//
//   +------------------------------------------------+
//   | margin                                         |
//   |  [Brand Logo]              +----------------+  |
//   |                            |  Topic-specific|  |
//   |                            |  hero card —   |  |
//   |   Headline With            |  same shape as |  |
//   |   One Accent Word          |  the YouTube   |  |
//   |   ^^^^^^^^^^^^             |  thumbnail     |  |
//   |   (brand gradient)         |  studio uses   |  |
//   |                            +----------------+  |
//   |   //// diagonal accent strip ////  (bleeds)    |
//   | margin                                         |
//   +------------------------------------------------+
//
// Same design DNA as the YouTube thumbnail studio (Headline + Hero + accent
// strip + halos), tuned for the wider/shorter OG aspect ratio.
//
// Per-sample data:
//
//   { headline, accentWord, hero, gradient?, brand, items? }
//
// `brand`        — one of FinalPiece, TrustPager, … (see ../brand.js).
// `gradient`     — optional gradient key (e.g. "home", "crm"). Default: "default".
// `hero`         — hero registry key (see ./heroes/index.js).
// `items`        — optional override for the AI activity item list.
//
// ============================================================================

import React from 'react';
import { getBrand, DEFAULT_BRAND } from '../brand.js';
import { resolveHero } from './heroes/index.js';

const SYS = {
  canvas:        { width: 1200, height: 630 },
  margin:        28,
  gap:           16,
  leftColWidth:  640,     // 1200 - 28 - 640 - 16 - 28 = 488 hero width
  heroWidth:     488,
  heroExtraItems: 3,
  logoHeight:    48,
  headlineSize:  96,
  cardRadius:    14,
  activityCardRadius: 18,
};

const DEFAULT_ITEMS = [
  { state: 'done',     text: 'Sent quote to Amir K.' },
  { state: 'done',     text: 'Booked Sasha R. — 9:00 AM' },
  { state: 'done',     text: 'Followed up with Jordan P.' },
  { state: 'done',     text: 'Generated weekly report' },
  { state: 'done',     text: 'Drafted SMS for Marguerite V.' },
  { state: 'progress', text: 'Updating 12 deal statuses' },
  { state: 'pending',  text: 'Queue follow-ups for new Leads' },
  { state: 'pending',  text: 'Open Service Requests' },
  { state: 'pending',  text: 'Score new inbound leads' },
];

// ------------------------------------------------------------------
// Headline — one accent word receives the brand's gradient fill.
// ------------------------------------------------------------------
// Set background-clip:text via a ref + setAttribute. React 19's inline
// style object handling drops background-clip in some property orders;
// applying it as a raw cssText attribute bypasses that entirely.
const AccentWord = ({ children, gradient }) => {
  const ref = React.useRef(null);
  React.useLayoutEffect(() => {
    if (!ref.current) return;
    ref.current.style.cssText = `
      background: ${gradient};
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
      color: transparent;
    `;
  }, [gradient]);
  return <span ref={ref}>{children}</span>;
};

const Headline = ({ text, accentWord, gradient, color, fontFamily, size = 96 }) => {
  const style = {
    color,
    fontFamily,
    fontSize: size,
    fontWeight: 800,
    lineHeight: 0.97,
    letterSpacing: '-0.035em',
  };
  if (!accentWord) return <span style={style}>{text}</span>;
  const parts = text.split(new RegExp(`(\\b${accentWord.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b)`, 'i'));
  return (
    <span style={style}>
      {parts.map((p, i) =>
        p.toLowerCase() === accentWord.toLowerCase() ? (
          <AccentWord key={i} gradient={gradient}>{p}</AccentWord>
        ) : (
          <span key={i}>{p}</span>
        )
      )}
    </span>
  );
};

// ------------------------------------------------------------------
// ColourHalo — soft blooms behind the right-hand hero. Left stays clean.
// ------------------------------------------------------------------
const ColorHalo = ({ brand }) => {
  const c1 = brand.colors.primary;
  const c2 = brand.colors.secondary || brand.colors.accent;
  const c3 = brand.colors.accent || brand.colors.primary;
  return (
    <div
      aria-hidden
      style={{
        position: 'absolute',
        inset: 0,
        // Halo blooms confined to the right ~55% of the canvas.
        background: `
          radial-gradient(circle at 75% 35%, ${c1}22 0%, transparent 38%),
          radial-gradient(circle at 88% 78%, ${c2}1f 0%, transparent 40%),
          radial-gradient(circle at 62% 90%, ${c3}1a 0%, transparent 36%)
        `,
        pointerEvents: 'none',
        // Fade halos out before they reach the left text column.
        WebkitMaskImage: 'linear-gradient(90deg, transparent 0%, transparent 38%, #000 60%, #000 100%)',
        maskImage: 'linear-gradient(90deg, transparent 0%, transparent 38%, #000 60%, #000 100%)',
        zIndex: 3,
      }}
    />
  );
};

// ------------------------------------------------------------------
// AccentStrip — thin diagonal brand-gradient line near the bottom.
// ------------------------------------------------------------------
const AccentStrip = ({ gradient }) => (
  <div
    aria-hidden
    style={{
      position: 'absolute',
      left: -100,
      right: -100,
      bottom: 56,
      height: 6,
      background: gradient,
      transform: 'rotate(-2.2deg)',
      opacity: 0.85,
      borderRadius: 3,
      zIndex: 2,
    }}
  />
);

// ------------------------------------------------------------------
// OgImage — main template
// ------------------------------------------------------------------
export const OgImage = ({ data = {} }) => {
  const brandName = data.brand || DEFAULT_BRAND;
  const brand = getBrand(brandName);

  if (!brand) {
    return (
      <div style={{ width: SYS.canvas.width, height: SYS.canvas.height, background: '#fee', padding: 40, fontFamily: 'system-ui' }}>
        <h2 style={{ color: '#c00', margin: 0 }}>Unknown brand: "{brandName}"</h2>
        <p>Add it under MARKETING/BRAND_ASSETS/{brandName}/brand.json</p>
      </div>
    );
  }

  const gradientKey = data.gradient || 'default';
  const accentGradient = brand.gradients[gradientKey] || brand.gradients.default;

  const heroKey = data.hero || 'ai-activity';
  const Hero = resolveHero(heroKey);
  const items = data.items || DEFAULT_ITEMS;

  const fontPrimary = brand.fonts?.primary || 'system-ui, sans-serif';

  // Inject brand CSS variables on the canvas root. Every hero references
  // these via var(--brand-*) — no prop drilling, no hook, no migration
  // debt. Add a new brand by adding to BRAND_ASSETS/<Brand>/brand.json
  // and these variables automatically resolve to the new colours.
  //
  // Per-page override: brand.accentSets[gradientKey] lets a sample's
  // gradient (e.g. "crm" on FinalPiece) pull a different accent palette
  // so the hero chrome matches what's on that specific page. Falls back
  // to brand.colors when no override exists.
  const accentSet = (brand.accentSets && brand.accentSets[gradientKey]) || brand.colors;
  const brandVars = {
    '--brand-primary':       accentSet.primary       || brand.colors.primary,
    '--brand-primary-deep':  accentSet.primaryDeep   || brand.colors.primaryDeep || brand.colors.primaryDark || brand.colors.primary,
    '--brand-secondary':     accentSet.secondary     || brand.colors.secondary,
    '--brand-accent':        accentSet.accent        || brand.colors.accent,
    '--brand-light':         accentSet.light         || brand.colors.light || brand.colors.lightTeal || brand.colors.accent,
    '--brand-slate':         brand.colors.slate || '#94a3b8',
    '--brand-gradient':      accentGradient,
  };

  return (
    <div
      className="template-canvas"
      style={{
        position: 'relative',
        width: SYS.canvas.width,
        height: SYS.canvas.height,
        background: brand.background,
        overflow: 'hidden',
        fontFamily: fontPrimary,
        ...brandVars,
      }}
    >
      {/* halos behind the hero */}
      <ColorHalo brand={brand} />

      {/* diagonal brand accent line near the bottom */}
      <AccentStrip gradient={accentGradient} />

      {/* logo — bare img, top-left, no card */}
      <img
        src={brand.logoUrl}
        alt={brand.displayName}
        style={{
          position: 'absolute',
          top: SYS.margin + 8,
          left: SYS.margin + 8,
          height: brand.logoHeight || SYS.logoHeight,
          width: 'auto',
          objectFit: 'contain',
          zIndex: 9,
        }}
      />

      {/* headline — vertically centered in the left column */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: SYS.margin + 8,
          width: SYS.leftColWidth,
          display: 'flex',
          alignItems: 'center',
          zIndex: 8,
        }}
      >
        <Headline
          text={data.headline}
          accentWord={data.accentWord}
          gradient={accentGradient}
          color={brand.foreground}
          fontFamily={fontPrimary}
          size={data.headlineSize || SYS.headlineSize}
        />
      </div>

      {/* hero — right column, bleeds off bottom */}
      <div
        style={{
          position: 'absolute',
          top: SYS.margin,
          right: SYS.margin,
          width: SYS.heroWidth,
          // No bottom — height is determined by hero content; it overflows
          // the canvas because the parent has overflow:hidden.
          zIndex: 4,
        }}
      >
        {Hero ? (
          <Hero items={items} brand={brand} data={data} />
        ) : (
          <div
            style={{
              width: '100%',
              minHeight: SYS.canvas.height,
              background: '#fff',
              borderRadius: SYS.activityCardRadius,
              padding: 24,
              color: brand.mutedForeground,
              fontSize: 14,
              boxShadow: '0 26px 52px rgba(15,17,23,0.12), 0 8px 18px rgba(15,17,23,0.08), 0 0 0 1px rgba(15,17,23,0.04)',
            }}
          >
            <strong style={{ color: brand.foreground }}>Hero "{heroKey}" not found.</strong>
            <div style={{ marginTop: 8 }}>Register it in src/templates/heroes/index.js.</div>
          </div>
        )}
      </div>
    </div>
  );
};

OgImage.templateMeta = {
  id: 'og-image',
  name: 'OG Image (1200×630)',
  size: SYS.canvas,
};

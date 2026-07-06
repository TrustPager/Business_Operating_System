// Brand kit loader for the BOS Video studio.
//
// Identical pattern to studio/social/src/brand.js and studio/thumbnails/src/brand.js
// — every studio reads from the SAME brand.json at the BOS root, so editing it
// once (or running /brand-my-workspace) rebrands every studio in one shot.
// Decision 4 of the YouTube Studio design doc requires this import be identical
// to studio/social/src/brand.js.

import brand from '../../../brand/brand.json';

export const NAME    = brand.name;
export const TAGLINE = brand.tagline;
export const COLORS  = brand.colors;

export const PRIMARY      = COLORS.primary;
export const PRIMARY_DEEP = COLORS.primaryDeep;
export const PRIMARY_TINT = COLORS.primaryTint;
export const PRIMARY_TINT_DEEP = COLORS.primaryTintDeep;
export const ACCENT       = COLORS.accent;
export const DEEP_BLUE    = COLORS.deepBlue;
export const MID_MINT     = COLORS.midMint;
export const LIGHT        = COLORS.light;
export const SLATE        = COLORS.slate;
export const SUCCESS      = COLORS.success;
export const WARNING      = COLORS.warning;

export const TEXT       = COLORS.text;
export const TEXT_MUTED = COLORS.textMuted;
export const PANEL      = COLORS.panel;
export const BORDER     = COLORS.border;
export const PAGE_BG    = COLORS.pageBg;
export const CANVAS_BG  = COLORS.canvasBg;

export const GRADIENT       = brand.gradient;
export const HERO_GRADIENT  = brand.heroGradient ?? brand.gradient;
export const WARM_GRADIENT  = brand.warmGradient ?? brand.gradient;

export const FONT_BODY  = brand.fonts?.primary ?? '"Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, system-ui, sans-serif';
export const FONT_SERIF = brand.fonts?.serif   ?? '"Playfair Display", Georgia, serif';
export const FONT_MONO  = brand.fonts?.mono    ?? '"JetBrains Mono", "Fira Code", monospace';

export const LOGO_URL = '/logo.png';

export const BRAND = {
  name: NAME,
  tagline: TAGLINE,
  colors: COLORS,
  gradient: GRADIENT,
  heroGradient: HERO_GRADIENT,
  warmGradient: WARM_GRADIENT,
  fontBody: FONT_BODY,
  fontMono: FONT_MONO,
  logoUrl: LOGO_URL,
};

export default BRAND;

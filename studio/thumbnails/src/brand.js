// Brand kit loader for the BOS thumbnail studio.
//
// Reads the canonical brand.json at the BOS root and exposes typed tokens
// every template can import from. NO hex literals in template files —
// they all flow through here so editing brand.json (or running
// /brand-my-workspace) reskins every rendered output in one shot.
//
// Vite supports JSON imports natively. No build-time codegen needed.

import brand from '../../../brand/brand.json';

export const NAME    = brand.name;
export const TAGLINE = brand.tagline;
export const COLORS  = brand.colors;

// Convenience flat aliases — every template ends up wanting the brand
// teal as a single identifier. Less verbose than COLORS.primary at the
// call site.
export const PRIMARY      = COLORS.primary;
export const PRIMARY_DEEP = COLORS.primaryDeep;
export const PRIMARY_TINT = COLORS.primaryTint;
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

// Logo path served by Vite — sync-brand.py copies brand/logo.png into
// each studio's public/ on install + after every /brand-my-workspace run.
export const LOGO_URL = '/logo.png';

// Convenience: a single BRAND object for files that prefer one import.
export const BRAND = {
  name: NAME,
  tagline: TAGLINE,
  colors: COLORS,
  gradient: GRADIENT,
  heroGradient: HERO_GRADIENT,
  warmGradient: WARM_GRADIENT,
  fontBody: FONT_BODY,
  fontSerif: FONT_SERIF,
  fontMono: FONT_MONO,
  logoUrl: LOGO_URL,
};

export default BRAND;

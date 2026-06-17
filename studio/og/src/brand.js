// Brand kit loader for the BOS OG Image studio.
//
// Single-brand, exactly like the social + thumbnail studios: every studio
// reads the SAME brand.json at the BOS root, so editing it once (or running
// /brand-my-workspace) reskins every studio in one shot.
//
// OgImage.jsx + the heroes were forked from the multi-brand marketing studio,
// where each sample picked its own brand. Here there is only ever ONE brand —
// yours — so getBrand() ignores its argument and always returns the workspace
// brand, shaped the way OgImage.jsx expects. The template then injects these
// colours as --brand-* CSS variables on the canvas root; every hero reads
// var(--brand-*), so nothing downstream needs to know there's only one brand.

import brand from '../../../brand/brand.json';

const C = brand.colors;

// --- Flat tokens for the editor chrome (App.jsx) -------------------------
// The studio UI itself (sidebar, toolbar, command chips) is styled directly
// from these, exactly like the social + thumbnail studios. The rendered OG
// image gets its colours through getBrand() + the --brand-* vars instead.
export const NAME    = brand.name;
export const TAGLINE = brand.tagline;
export const COLORS  = C;

export const PRIMARY      = C.primary;
export const PRIMARY_DEEP = C.primaryDeep;
export const ACCENT       = C.accent;
export const SUCCESS      = C.success;

export const TEXT       = C.text;
export const TEXT_MUTED = C.textMuted;
export const PANEL      = C.panel;
export const BORDER     = C.border;
export const PAGE_BG    = C.pageBg;
export const CANVAS_BG  = C.canvasBg;

export const FONT_BODY = brand.fonts?.primary ?? '"Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, system-ui, sans-serif';
export const FONT_MONO = brand.fonts?.mono    ?? '"JetBrains Mono", "Fira Code", monospace';

export const LOGO_URL = '/logo.png';

// The single workspace brand, shaped for OgImage.jsx + the heroes.
const WORKSPACE_BRAND = {
  name:        brand.name,
  displayName: brand.name,
  tagline:     brand.tagline,

  background:       C.panel,      // canvas fill — white
  foreground:       C.text,       // headline colour
  mutedForeground:  C.textMuted,

  logoUrl:    '/logo.png',        // synced into public/ by /brand-my-workspace
  logoHeight: 48,

  colors: {
    primary:     C.primary,
    primaryDeep: C.primaryDeep,
    // The marketing studio's "secondary" maps to the brand's success green —
    // the second anchor colour in the teal→green→blue family.
    secondary:   C.success,
    accent:      C.accent,
    light:       C.light,
    slate:       C.slate,
  },

  gradients: {
    default: brand.gradient,
    hero:    brand.heroGradient ?? brand.gradient,
    warm:    brand.warmGradient ?? brand.gradient,
  },

  fonts: {
    primary: brand.fonts?.primary ?? '"Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, system-ui, sans-serif',
  },
};

export function listBrands() {
  return [WORKSPACE_BRAND.name];
}

// Single-brand: the argument is accepted for compatibility with OgImage.jsx
// (which forwards data.brand) but every call resolves to the workspace brand.
export function getBrand() {
  return WORKSPACE_BRAND;
}

export const DEFAULT_BRAND = WORKSPACE_BRAND.name;

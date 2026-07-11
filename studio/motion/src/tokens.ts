// tokens.ts — THE brand bridge for the motion studio.
//
// One source of token values. Everything traces to brand/brand.json (via brand.js).
// No hex literals live here; edit brand.json (or run /brand-my-workspace) and every
// ported component recolours in one shot.
//
// This module exposes THREE surfaces so the ported RVS components need only a
// one-line import swap:
//   1. Flat brand tokens (primary/accent/text/panel/... + role aliases app/assistant).
//   2. `colors` / `fonts` / `shadows` objects matching the shape the RVS compositor
//      + ProgressPanel used to import from its old design-token module.
//   3. rgb-triplet strings (primaryRgb/accentRgb/textRgb) so components can build
//      rgba(...) glows/shadows without baking a brand colour literal.

import {
  PRIMARY,
  PRIMARY_DEEP,
  PRIMARY_TINT,
  PRIMARY_TINT_DEEP,
  ACCENT,
  DEEP_BLUE,
  LIGHT,
  SLATE,
  TEXT,
  TEXT_MUTED,
  PANEL,
  BORDER,
  PAGE_BG,
  CANVAS_BG,
  SUCCESS,
  WARNING,
  GRADIENT,
  HERO_GRADIENT,
  FONT_BODY,
  FONT_SERIF,
  FONT_MONO,
} from "./brand.js";

// --- helper: #rrggbb -> "r, g, b" (brand.json colours are all 6-digit hex) ---
const hexToRgb = (hex: string): string => {
  const h = hex.replace("#", "").trim();
  if (h.length !== 6) return "0, 0, 0"; // safe fallback for a non-hex brand value
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  return `${r}, ${g}, ${b}`;
};

// ------------------------------------------------------------------
// 1. Flat brand tokens
// ------------------------------------------------------------------
export const primary = PRIMARY;
export const primaryDeep = PRIMARY_DEEP;
export const primaryTint = PRIMARY_TINT;
export const primaryTintDeep = PRIMARY_TINT_DEEP;
export const accent = ACCENT;
export const deepBlue = DEEP_BLUE;
export const text = TEXT;
export const textMuted = TEXT_MUTED;
export const panel = PANEL;
export const border = BORDER;
export const bg = PAGE_BG;
export const canvasBg = CANVAS_BG;
export const success = SUCCESS;
export const warning = WARNING;

// Colour-role aliases (brand-neutral vocabulary, never product names):
//   app       — the owner's product / UI chrome colour
//   assistant — the "something is being done for you" accent colour
export const app = PRIMARY;
export const assistant = ACCENT;

// rgb triplets for rgba() glows/shadows
export const primaryRgb = hexToRgb(PRIMARY);
export const accentRgb = hexToRgb(ACCENT);
export const textRgb = hexToRgb(TEXT);

// ------------------------------------------------------------------
// 2. Legacy `colors` shape (compositor + ProgressPanel import { colors })
//    Keys mirror the old design-token module; values map to brand.json.
// ------------------------------------------------------------------
export const colors = {
  // Backgrounds
  bg000: PANEL, // pure surface — cards, popovers
  bg100: PAGE_BG, // page background
  bg200: PRIMARY_TINT, // hover / subtle
  bg300: PRIMARY_TINT_DEEP, // active
  bg400: LIGHT, // stronger surface
  bg500: SLATE,

  // Text ramp
  text100: TEXT,
  text200: TEXT,
  text300: TEXT_MUTED,
  text400: TEXT_MUTED,
  text500: TEXT_MUTED,

  // Accent — the "assistant / being-built" colour (was baked clay)
  accentBrand: ACCENT,
  accentBrandLight: ACCENT,
  accentMain: ACCENT,

  // App / product colour (was baked teal)
  app: PRIMARY,

  // Borders
  border100: BORDER,
  border200: BORDER,
  border300: BORDER,

  // Semantic
  success: SUCCESS,
  warning: WARNING,
  error: WARNING, // brand.json has no error role; reuse warning until one is set

  // Always
  white: PANEL,
  black: TEXT,
} as const;

// ------------------------------------------------------------------
// 3. Legacy `fonts` shape
// ------------------------------------------------------------------
export const fonts = {
  ui: FONT_BODY,
  display: FONT_SERIF,
  mono: FONT_MONO,
} as const;

// ------------------------------------------------------------------
// 4. Gradients (brand-driven)
// ------------------------------------------------------------------
export const gradients = {
  primary: HERO_GRADIENT,
  hero: HERO_GRADIENT,
  full: GRADIENT,
} as const;

// ------------------------------------------------------------------
// 5. Legacy `shadows` shape — neutral elevation (no brand colour baked)
// ------------------------------------------------------------------
export const shadows = {
  card: "0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)",
  cardHover: "0 4px 12px rgba(0,0,0,0.08)",
  overlay: "0 4px 24px rgba(0,0,0,0.12)",
  composer:
    "0 0.25rem 1.25rem rgba(0,0,0,0.035), 0 0 0 0.5px rgba(100,116,139,0.15)",
  composerHover:
    "0 0.25rem 1.25rem rgba(0,0,0,0.05), 0 0 0 0.5px rgba(100,116,139,0.30)",
  composerFocus:
    "0 0.25rem 1.25rem rgba(0,0,0,0.075), 0 0 0 0.5px rgba(100,116,139,0.30)",
} as const;

// ui/theme.ts — internal adapter for the extracted UI kit.
//
// The shadcn-style primitives in this folder were authored against a legacy
// design-token shape (`colors`/`gradients`/`fonts`/`shadows`). This adapter
// re-exposes that shape, but every value derives from the ONE brand bridge
// (../tokens ← ../brand.js ← brand/brand.json). No brand colour is baked here.
import {
  primary,
  primaryDeep,
  primaryTint,
  accent,
  text,
  textMuted,
  panel,
  border,
  bg,
  canvasBg,
  success,
  warning,
  gradients as brandGradients,
  fonts as brandFonts,
  shadows as brandShadows,
} from "../tokens";

export const colors = {
  primary,
  primaryDark: primaryDeep,
  primarySoft: primaryTint, // translucent-ish soft fill, from brand tint
  accent,
  foreground: text,
  mutedForeground: textMuted,
  background: bg,
  card: panel,
  muted: canvasBg,
  border,
  borderHalf: border,
  success,
  warning,
  error: warning, // brand.json has no error role; reuse warning until one is set
  white: panel,
};

export const gradients = {
  primary: brandGradients.primary,
  hero: brandGradients.hero,
};

export const fonts = {
  primary: brandFonts.ui,
};

export const shadows = {
  card: brandShadows.card,
  cardHover: brandShadows.cardHover,
  overlay: brandShadows.overlay,
};

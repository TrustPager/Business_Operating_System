// fonts.ts — render-time font resolution for the motion studio.
//
// Mechanism (see design spec §3.3):
//   - The neutral default brand.json uses SYSTEM-FONT CSS stacks
//     (e.g. "-apple-system, ...") so the default render needs NO font loading;
//     the stack is applied directly as `fontFamily`.
//   - When an owner sets a real Google font family (a bare family name, not a
//     CSS stack), we load it for the render via @remotion/google-fonts.
//   - `googleFontsHref` in brand.json is a <link> hint used by the still-studios;
//     it does NOT load a font into a Remotion render, so it is ignored here.
//
// FONT_BODY / FONT_SERIF / FONT_MONO are the ready-to-use `fontFamily` values.
// Call loadBrandFonts() once at composition module scope if you set a Google font.

import { FONT_BODY as BODY, FONT_SERIF as SERIF, FONT_MONO as MONO } from "./brand.js";

// A CSS stack contains a comma or a generic keyword; a bare Google family does not.
const isCssStack = (value: string): boolean =>
  value.includes(",") ||
  /\b(system-ui|sans-serif|serif|monospace|-apple-system)\b/.test(value);

export const FONT_BODY: string = BODY;
export const FONT_SERIF: string = SERIF;
export const FONT_MONO: string = MONO;

// Family map — extend when adding first-class Google faces. Empty by default
// because the neutral brand ships system stacks (zero-load, zero-network).
//
// To wire a Google family, add a static import + loadFont() branch here, e.g.:
//   import { loadFont } from "@remotion/google-fonts/Inter";
//   if (family === "Inter") { loadFont(); return; }
export const loadBrandFonts = (): void => {
  for (const value of [BODY, SERIF, MONO]) {
    if (isCssStack(value)) continue; // system stack — nothing to load
    // A bare family name was set. Until it is added to the map above, the
    // render falls back to the CSS stack the browser resolves for that name.
    // (No throw: a missing Google face must never hard-fail a render.)
  }
};

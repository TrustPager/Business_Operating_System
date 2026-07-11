// positions.ts — geometry types for placing overlay primitives on a scene.
//
// Phase 1 keeps ONLY the shape interface. The old product-specific coordinate
// tables (measured against a particular app's UI) are intentionally NOT ported;
// scenes supply their own positions, or a future scene-library computes them.

export interface StagePosition {
  /** Stage index. */
  index: number;
  /** Stage display name. */
  name: string;
  /** Brand colour used for the coloured top border. */
  color: string;
  /** Column left edge in composition pixels (1920x1080). */
  left: number;
  /** Column right edge in composition pixels. */
  right: number;
  /** Bolt/icon position (fractional 0..1). */
  bolt: {x: number; y: number};
  /** Header card bounds in composition pixels (1920x1080). */
  headerCard: {
    tl: {x: number; y: number};
    br: {x: number; y: number};
    w: number;
    h: number;
  };
  /** Default top-left for a preview card centered above the bolt. */
  previewCard: {x: number; y: number};
  /** Default top-left for a "no automations" card centered above the bolt. */
  noAutomationsCard: {x: number; y: number};
}

/**
 * Animations — shared frame-driven primitives for scenes and overlays.
 *
 * Replaces three patterns that had been re-implemented inline across many
 * compositions:
 *   1. Typewriter — characters reveal proportional to frame in [start, end]
 *   2. Paste flash — value snaps in at frame N with a highlight window after
 *   3. Fade-in — opacity + scale + translateY entrance for popovers/dropdowns
 *
 * All hooks read the nearest Sequence's local frame via useCurrentFrame().
 * Pass an explicit `appearFrame` (a frame in that local space) when you want
 * the animation to fire later than f0.
 *
 * Keep these dependency-free of any brand assumptions — pure motion primitives.
 */
import {useCurrentFrame, interpolate, Easing} from 'remotion';

/**
 * useTypewriter — type a string in over a frame window.
 *
 * Returns the prefix of `text` corresponding to the current frame's position
 * within [startFrame, endFrame]. Clamps at both ends so the result is the
 * empty string before startFrame and the full text after endFrame.
 *
 * @example
 *   const name = useTypewriter('Momentum', 0, 36);
 *   // f=0   → ''
 *   // f=18  → 'Mome'
 *   // f=36  → 'Momentum'
 */
export const useTypewriter = (text: string, startFrame: number, endFrame: number): string => {
  const f = useCurrentFrame();
  const len = Math.round(
    interpolate(f, [startFrame, endFrame], [0, text.length], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }),
  );
  return text.slice(0, len);
};

/**
 * usePasteFlash — snap a value in at a specific frame with a brief highlight.
 *
 * Returns two booleans:
 *   - `show` — true once the cursor has "pasted" (f >= showAtFrame)
 *   - `highlight` — true during the flash window after the paste lands
 *
 * @param showAtFrame  the frame the value appears
 * @param highlightWindow  number of frames the highlight ring stays lit (default 30)
 *
 * @example
 *   const {show, highlight} = usePasteFlash(22);
 *   <Field value={show ? URL : ''} highlight={highlight} />
 */
export const usePasteFlash = (showAtFrame: number, highlightWindow = 30): {show: boolean; highlight: boolean} => {
  const f = useCurrentFrame();
  return {
    show: f >= showAtFrame,
    highlight: f >= showAtFrame && f <= showAtFrame + highlightWindow,
  };
};

export interface FadeInOptions {
  /** Frames the entrance takes (default 6 — matches Radix's duration-200). */
  duration?: number;
  /** Final scale (default 1). Start scale = `1 - scaleAmount`. */
  scaleAmount?: number;
  /** Pixels to translate up from (default 8). End translateY = 0. */
  translateYAmount?: number;
}

export interface FadeInResult {
  opacity: number;
  scale: number;
  translateY: number;
  /** Convenience CSS transform string combining scale + translate. */
  transform: string;
}

/**
 * useFadeIn — popover/dropdown entrance animation.
 *
 * opacity 0→1, scale 0.95→1, translateY -8px→0 over `duration` frames, eased
 * with `Easing.out(Easing.cubic)`.
 *
 * If `startFrame` is undefined, returns the fully-landed state {1, 1, 0}.
 *
 * @example
 *   const {opacity, transform} = useFadeIn(appearFrame);
 *   <div style={{opacity, transform, transformOrigin: '100% 0'}}> ... </div>
 */
export const useFadeIn = (startFrame: number | undefined, options?: FadeInOptions): FadeInResult => {
  const f = useCurrentFrame();
  const {duration = 6, scaleAmount = 0.05, translateYAmount = 8} = options ?? {};

  const progress = startFrame === undefined
    ? 1
    : interpolate(f, [startFrame, startFrame + duration], [0, 1], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
        easing: Easing.out(Easing.cubic),
      });

  const opacity = progress;
  const scale = (1 - scaleAmount) + scaleAmount * progress;
  const translateY = -translateYAmount + translateYAmount * progress;
  return {
    opacity,
    scale,
    translateY,
    transform: `translateY(${translateY}px) scale(${scale})`,
  };
};

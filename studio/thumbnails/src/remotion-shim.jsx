/**
 * Remotion Shim for Vite
 *
 * Provides static implementations of Remotion hooks and components
 * so that Remotion video components can render in a plain React/Vite app
 * without the Remotion framework. All animations resolve to their final state.
 */
import React from 'react';

// Return a high frame number so all animations are in their "completed" state
export const useCurrentFrame = () => 999;

// Return the configured dimensions for the component viewport
// Components use this via useViewport() to determine sidebar visibility, scaling, etc.
const _videoConfig = { width: 1920, height: 1080, fps: 30, durationInFrames: 1 };
export const useVideoConfig = () => _videoConfig;

/**
 * Static interpolate — resolves to the final output value.
 * Remotion's interpolate maps frame ranges to output values.
 * At frame=999, we're always past the end of any animation range,
 * so we return the last value in outputRange (clamped).
 */
export function interpolate(input, inputRange, outputRange, options = {}) {
  const { extrapolateLeft = 'extend', extrapolateRight = 'extend' } = options;

  // If input is beyond the last input keyframe, return last output
  if (input >= inputRange[inputRange.length - 1]) {
    if (extrapolateRight === 'clamp') return outputRange[outputRange.length - 1];
    return outputRange[outputRange.length - 1];
  }
  // If input is before the first input keyframe, return first output
  if (input <= inputRange[0]) {
    if (extrapolateLeft === 'clamp') return outputRange[0];
    return outputRange[0];
  }
  // Linear interpolation between matching segments
  for (let i = 0; i < inputRange.length - 1; i++) {
    if (input >= inputRange[i] && input <= inputRange[i + 1]) {
      const t = (input - inputRange[i]) / (inputRange[i + 1] - inputRange[i]);
      return outputRange[i] + t * (outputRange[i + 1] - outputRange[i]);
    }
  }
  return outputRange[outputRange.length - 1];
}

// Easing functions — return identity since animations are already resolved
export const Easing = {
  linear: (t) => t,
  ease: (t) => t,
  quad: (t) => t * t,
  cubic: (t) => t * t * t,
  bezier: () => (t) => t,
  in: (fn) => fn,
  out: (fn) => fn,
  inOut: (fn) => fn,
  back: () => (t) => t,
  bounce: (t) => t,
  elastic: () => (t) => t,
  circle: (t) => t,
  sin: (t) => t,
  exp: (t) => t,
};

// AbsoluteFill — just a full-size positioned div
export const AbsoluteFill = React.forwardRef(({ children, style, ...props }, ref) => (
  <div
    ref={ref}
    style={{
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      width: '100%',
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      ...style,
    }}
    {...props}
  >
    {children}
  </div>
));

// Sequence — just renders children (no timing in static mode)
export const Sequence = ({ children }) => <>{children}</>;

// Composition — not needed for rendering, but prevent import errors
export const Composition = () => null;

// Audio — silent in static mode
export const Audio = () => null;

// staticFile — resolve to a path (won't load in Vite but prevents crashes)
export const staticFile = (path) => `/static/${path}`;

// registerRoot — no-op
export const registerRoot = () => {};

// spring — return 1 (fully settled)
export const spring = () => 1;

// ClickPulseRing — universal click effect.
//
// Phases (frames relative to `startFrame`):
//   [0..25]    cursor travels from `from` to `target` via easeInOutCubic
//   [25..45]   ring expands 32px -> 80px diameter, opacity 1 -> 0
//   [25..50]   ripple expands 24px -> 64px, opacity 1 -> 0
//   [25..end]  cursor holds at target
//
// Coordinates are fractional (0..1) of a 1920x1080 frame.
import React from 'react';
import {AbsoluteFill, useCurrentFrame, interpolate, Easing} from 'remotion';
import {primary, accent, primaryRgb, accentRgb} from '../tokens';

export type ClickPulseColor = 'primary' | 'assistant' | string;

/**
 * Click-effect colour rule (brand-neutral convention):
 *  - 'primary'   — the user navigating around their own product / app UI
 *  - 'assistant' — something being done for the user (the "assistant" accent)
 * A custom hex/hsl/rgb string is also accepted and used as the ring colour.
 */
export const CLICK_COLORS = {
  primary:   {ring: primary, ripple: `rgba(${primaryRgb}, 0.18)`},
  assistant: {ring: accent,  ripple: `rgba(${accentRgb}, 0.18)`},
} as const;

export interface ClickPulseRingProps {
  startFrame: number;
  targetX: number;
  targetY: number;
  fromX?: number;
  fromY?: number;
  durationInFrames: number;
  /** Visual variant — see CLICK_COLORS. Defaults to 'primary'. Custom hex/hsl string also accepted. */
  color?: ClickPulseColor;
}

const FRAME_W = 1920;
const FRAME_H = 1080;
// easeInOutCubic ~ Bezier(0.42, 0, 0.58, 1)
const easeInOutCubic = Easing.bezier(0.42, 0, 0.58, 1);

const CursorSVG = ({size = 40}: {size?: number}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    style={{filter: 'drop-shadow(0 0 8px rgba(255,255,255,0.8)) drop-shadow(0 2px 6px rgba(0,0,0,0.5))'}}
  >
    <path
      d="M4 1L4 17.5L8.5 13.5L12.5 21L15.5 19.5L11.5 12L17 11.5L4 1Z"
      fill="#ffffff"
      stroke="#0f1117"
      strokeWidth="1.5"
      strokeLinejoin="round"
    />
  </svg>
);

export const ClickPulseRing: React.FC<ClickPulseRingProps> = ({
  startFrame,
  targetX,
  targetY,
  fromX = 0.5,
  fromY = 0.5,
  durationInFrames,
  color = 'primary',
}) => {
  const frame = useCurrentFrame();
  const f = frame - startFrame;
  const palette = (color === 'primary' || color === 'assistant') ? CLICK_COLORS[color] : {ring: color, ripple: color};
  const ec = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

  if (f < 0 || f > durationInFrames) return null;

  const tx = targetX * FRAME_W;
  const ty = targetY * FRAME_H;
  const sx = fromX * FRAME_W;
  const sy = fromY * FRAME_H;

  const travelT = interpolate(f, [0, 25], [0, 1], {...ec, easing: easeInOutCubic});
  let cx = sx + (tx - sx) * travelT;
  let cy = sy + (ty - sy) * travelT;

  const ringActive = f >= 25 && f <= 45;
  const ringDiameter = interpolate(f, [25, 45], [32, 80], ec);
  const ringOpacity = interpolate(f, [25, 45], [1, 0], ec);

  const rippleActive = f >= 25 && f <= 50;
  const rippleDiameter = interpolate(f, [25, 50], [24, 64], ec);
  const rippleOpacity = interpolate(f, [25, 50], [1, 0], ec);

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {rippleActive && (
        <div
          style={{
            position: 'absolute',
            left: tx - rippleDiameter / 2,
            top: ty - rippleDiameter / 2,
            width: rippleDiameter,
            height: rippleDiameter,
            borderRadius: '50%',
            background: palette.ripple,
            opacity: rippleOpacity,
            zIndex: 200,
          }}
        />
      )}
      {ringActive && (
        <div
          style={{
            position: 'absolute',
            left: tx - ringDiameter / 2,
            top: ty - ringDiameter / 2,
            width: ringDiameter,
            height: ringDiameter,
            borderRadius: '50%',
            border: `2px solid ${palette.ring}`,
            opacity: ringOpacity,
            zIndex: 201,
          }}
        />
      )}
      <div
        style={{
          position: 'absolute',
          left: cx - 4,
          top: cy - 2,
          transformOrigin: '4px 1px',
          zIndex: 203,
        }}
      >
        <CursorSVG size={40} />
      </div>
    </AbsoluteFill>
  );
};

export default ClickPulseRing;

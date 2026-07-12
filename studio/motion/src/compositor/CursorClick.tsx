// CursorClick — gold-standard click indicator at a target point.
// Mirrors scenes/shared/ClickIndicator.tsx (ClickTarget) but works on a
// proportional target position + bounding box instead of wrapping a child.
//
// Phases (frames from appearAt):
//   0      ring + glow halo fade in around the target box
//   5–27   cursor flies in along an arc (sin curve overshoot)
//   27     cursor lands, press-down scale, click ripple expands
//   45     ripple done
//   43–55  ring + cursor fade out
//
import React from 'react';
import {useCurrentFrame, interpolate, Easing} from 'remotion';
import {Point} from './ConnectorLine';
import {accent, accentRgb} from '../tokens';

export interface CursorClickProps {
  /** Centre of the click target (proportional 0–1) */
  to: Point;
  /** Width of the highlight box (proportional 0–1). Default 0.06 */
  targetW?: number;
  /** Height of the highlight box (proportional 0–1). Default 0.04 */
  targetH?: number;
  /** Optional: separate ring centre (overrides `to` for ring/halo placement only) */
  ringTo?: Point;
  /** Optional: ring width override (proportional 0–1) */
  ringW?: number;
  /** Optional: ring height override (proportional 0–1) */
  ringH?: number;
  /** Frame at which the click sequence begins */
  appearAt: number;
  /** Total duration in frames before fade-out finishes. Default 55 */
  duration?: number;
  /** Pixel offset where the cursor starts (relative to target). Default {x: -300, y: 200} */
  cursorFromX?: number;
  cursorFromY?: number;
  /** Optional override colour. Defaults to the brand accent. */
  color?: string;
  /** Padding (px) around the box for the highlight ring. Default 12 */
  pad?: number;
  borderRadius?: number;
}

const FRAME_W = 1920;
const FRAME_H = 1080;
const easeOut = Easing.out(Easing.quad);
const easeInOut = Easing.inOut(Easing.quad);

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

export const CursorClick: React.FC<CursorClickProps> = ({
  to,
  targetW = 0.06,
  targetH = 0.04,
  ringTo,
  ringW,
  ringH,
  appearAt,
  duration = 55,
  cursorFromX = -300,
  cursorFromY = 200,
  color = accent,
  pad = 12,
  borderRadius = 14,
}) => {
  const frame = useCurrentFrame();
  const ec = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
  const f = frame - appearAt;
  const active = f >= -5 && f <= duration + 20;
  if (!active) return null;

  const DIM_IN = 10;
  const MOVE_START = 5;
  const MOVE_DUR = 22;
  const CLICK_AT = MOVE_START + MOVE_DUR;
  const RIPPLE_DUR = 18;
  const DIM_OUT_START = duration - 12;

  const ringOpacity = interpolate(f, [DIM_IN - 2, DIM_IN + 6, DIM_OUT_START, duration], [0, 1, 1, 0], ec);
  const pulsePhase = f >= DIM_IN ? (f - DIM_IN) * 0.18 : 0;
  const ringScale = 1 + Math.sin(pulsePhase) * 0.04;
  const glowOpacity = interpolate(f, [DIM_IN, DIM_IN + 8, DIM_OUT_START, duration], [0, 0.6, 0.6, 0], ec);

  const moveF = f - MOVE_START;
  const cursorX = interpolate(moveF, [0, MOVE_DUR], [cursorFromX, 0], {...ec, easing: easeInOut});
  const cursorY = interpolate(moveF, [0, MOVE_DUR], [cursorFromY, 0], {...ec, easing: easeInOut});
  const cursorArc = moveF > 0 && moveF < MOVE_DUR ? Math.sin((moveF / MOVE_DUR) * Math.PI) * -40 : 0;
  const cursorOpacity = interpolate(f, [0, 6, duration - 5, duration], [0, 1, 1, 0], ec);
  const clickF = f - CLICK_AT;
  const cursorScale = clickF >= 0 && clickF < 8
    ? interpolate(clickF, [0, 3, 8], [1, 0.75, 1], ec)
    : 1;

  const rippleOpacity = clickF >= 0 ? interpolate(clickF, [0, RIPPLE_DUR], [0.7, 0], ec) : 0;
  const rippleScale = clickF >= 0 ? interpolate(clickF, [0, RIPPLE_DUR], [0.5, 3], {...ec, easing: easeOut}) : 0;

  const cx = to.x * FRAME_W;
  const cy = to.y * FRAME_H;
  const rcx = (ringTo ? ringTo.x : to.x) * FRAME_W;
  const rcy = (ringTo ? ringTo.y : to.y) * FRAME_H;
  const boxW = (ringW != null ? ringW : targetW) * FRAME_W;
  const boxH = (ringH != null ? ringH : targetH) * FRAME_H;

  return (
    <>
      <div style={{
        position: 'absolute',
        left: rcx - boxW / 2 - pad - 4,
        top: rcy - boxH / 2 - pad - 4,
        width: boxW + (pad + 4) * 2,
        height: boxH + (pad + 4) * 2,
        borderRadius: borderRadius + 2,
        background: 'rgba(245, 244, 238, ' + (glowOpacity * 0.3) + ')',
        boxShadow: `0 0 60px 20px rgba(${accentRgb}, ${glowOpacity * 0.25})`,
        pointerEvents: 'none',
        zIndex: 49,
      }} />

      <div style={{
        position: 'absolute',
        left: rcx - boxW / 2 - pad,
        top: rcy - boxH / 2 - pad,
        width: boxW + pad * 2,
        height: boxH + pad * 2,
        borderRadius,
        border: '3px solid ' + color,
        boxShadow:
          `0 0 30px rgba(${accentRgb}, ${glowOpacity * 0.55}), ` +
          `0 0 60px rgba(${accentRgb}, ${glowOpacity * 0.25}), ` +
          `inset 0 0 30px rgba(${accentRgb}, 0.10)`,
        opacity: ringOpacity,
        transform: 'scale(' + ringScale + ')',
        pointerEvents: 'none',
        zIndex: 50,
      }} />

      {clickF >= 0 && clickF < RIPPLE_DUR && (
        <div style={{
          position: 'absolute',
          left: cx - 40,
          top: cy - 40,
          width: 80,
          height: 80,
          borderRadius: '50%',
          border: '3px solid ' + color,
          opacity: rippleOpacity,
          transform: 'scale(' + rippleScale + ')',
          pointerEvents: 'none',
          zIndex: 51,
        }} />
      )}

      {cursorOpacity > 0 && (
        <div style={{
          position: 'absolute',
          left: cx + cursorX - 4,
          top: cy + cursorY + cursorArc - 2,
          opacity: cursorOpacity,
          transform: 'scale(' + cursorScale + ')',
          transformOrigin: '4px 1px',
          pointerEvents: 'none',
          zIndex: 53,
        }}>
          <CursorSVG size={40} />
        </div>
      )}
    </>
  );
};

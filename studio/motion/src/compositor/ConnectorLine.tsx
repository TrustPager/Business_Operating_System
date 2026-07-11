// ConnectorLine — animated SVG path connecting a "from" point to a "to"
// point on the frame, with optional arrow head. Used to show cause-and-
// effect: "this action here → this thing changed there."
//
// Coordinates are proportional (0-1) so the connector survives aspect
// ratio changes when used in vertical/square edits.
import React from 'react';
import {useCurrentFrame, interpolate, Easing} from 'remotion';
import {accent} from '../tokens';

export interface Point {
  x: number; // 0-1
  y: number; // 0-1
}

export interface ConnectorLineProps {
  from: Point;
  to: Point;
  color?: string;
  strokeWidth?: number;
  appearAt: number;
  drawDurationFrames?: number;
  curve?: number; // pixels of curvature; positive = bow up
  arrowHead?: boolean;
  dashed?: boolean;
  glow?: boolean;
}

const FRAME_W = 1920;
const FRAME_H = 1080;

export const ConnectorLine: React.FC<ConnectorLineProps> = ({
  from,
  to,
  color = accent,
  strokeWidth = 3,
  appearAt,
  drawDurationFrames = 18,
  curve = 60,
  arrowHead = true,
  dashed = false,
  glow = true,
}) => {
  const frame = useCurrentFrame();
  const x1 = from.x * FRAME_W;
  const y1 = from.y * FRAME_H;
  const x2 = to.x * FRAME_W;
  const y2 = to.y * FRAME_H;
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2 - curve;

  const angle = Math.atan2(y2 - my, x2 - mx);
  const headSize = 14;
  const h1x = x2 - headSize * Math.cos(angle - 0.4);
  const h1y = y2 - headSize * Math.sin(angle - 0.4);
  const h2x = x2 - headSize * Math.cos(angle + 0.4);
  const h2y = y2 - headSize * Math.sin(angle + 0.4);

  const draw = interpolate(
    frame,
    [appearAt, appearAt + drawDurationFrames],
    [0, 1],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.5, 0, 0.2, 1)}
  );
  const totalLen = 2200;
  const dashArray = totalLen;
  const dashOffset = totalLen * (1 - draw);

  if (frame < appearAt) return null;

  return (
    <svg
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        overflow: 'visible',
      }}
    >
      {glow && (
        <path
          d={'M ' + x1 + ' ' + y1 + ' Q ' + mx + ' ' + my + ' ' + x2 + ' ' + y2}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth + 6}
          strokeOpacity={0.18}
          strokeLinecap="round"
          strokeDasharray={dashArray}
          strokeDashoffset={dashOffset}
          style={{filter: 'blur(4px)'}}
        />
      )}
      <path
        d={'M ' + x1 + ' ' + y1 + ' Q ' + mx + ' ' + my + ' ' + x2 + ' ' + y2}
        fill="none"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeDasharray={dashed ? '8 6' : String(dashArray)}
        strokeDashoffset={dashed ? 0 : dashOffset}
      />
      {arrowHead && draw > 0.85 && (
        <polygon
          points={x2 + ',' + y2 + ' ' + h1x + ',' + h1y + ' ' + h2x + ',' + h2y}
          fill={color}
          opacity={interpolate(draw, [0.85, 1], [0, 1])}
        />
      )}
    </svg>
  );
};

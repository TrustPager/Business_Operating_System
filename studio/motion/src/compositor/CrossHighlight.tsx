// CrossHighlight — pulses two regions simultaneously to draw the eye to
// cause-and-effect. Pair with ConnectorLine for the classic
// "prompt → result" reveal.
import React from 'react';
import {useCurrentFrame, interpolate} from 'remotion';
import {Box} from './PictureInPicture';
import {accent} from '../tokens';

export interface CrossHighlightProps {
  regions: Box[];
  color?: string;
  appearAt: number;
  durationFrames?: number;
  pulseSpeed?: number; // frames per pulse cycle
}

const FRAME_W = 1920;
const FRAME_H = 1080;

export const CrossHighlight: React.FC<CrossHighlightProps> = ({
  regions,
  color = accent,
  appearAt,
  durationFrames = 60,
  pulseSpeed = 30,
}) => {
  const frame = useCurrentFrame();
  if (frame < appearAt || frame > appearAt + durationFrames) return null;

  const local = frame - appearAt;
  const fadeIn = interpolate(local, [0, 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const fadeOut = interpolate(local, [durationFrames - 12, durationFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const baseOpacity = Math.min(fadeIn, fadeOut);

  const pulse = 0.5 + 0.5 * Math.sin((local / pulseSpeed) * Math.PI);
  const opacity = baseOpacity * (0.55 + 0.45 * pulse);

  return (
    <>
      {regions.map((r, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: r.x * FRAME_W - (r.w * FRAME_W) / 2,
            top: r.y * FRAME_H - (r.h * FRAME_H) / 2,
            width: r.w * FRAME_W,
            height: r.h * FRAME_H,
            borderRadius: 14,
            border: '3px solid ' + color,
            boxShadow:
              '0 0 0 ' + Math.round(6 * pulse) + 'px ' + color + '33, ' +
              '0 0 ' + Math.round(40 * pulse) + 'px ' + color + '55',
            opacity,
            pointerEvents: 'none',
            zIndex: 60,
          }}
        />
      ))}
    </>
  );
};

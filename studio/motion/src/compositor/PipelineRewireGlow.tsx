// PipelineRewireGlow — animates an accent glow ring around a region (typically
// a whole board area) signalling "this is being rewired". Designed to play right
// before a rewire transition.
//
// Phases:
//   appearAt       — ring fades in
//   appearAt+12    — first pulse peaks
//   appearAt+30    — pulse settles
//   appearAt+44    — second pulse (climax — matches the rewire moment)
//   appearAt+72    — fades out as the new layout reveals
import React from 'react';
import {useCurrentFrame, interpolate, Easing} from 'remotion';
import {Box} from './PictureInPicture';
import {accent} from '../tokens';

export interface PipelineRewireGlowProps {
  region: Box;                    // proportional 0-1
  appearAt: number;
  durationFrames?: number;
  color?: string;
  borderRadius?: number;
}

const FRAME_W = 1920;
const FRAME_H = 1080;

export const PipelineRewireGlow: React.FC<PipelineRewireGlowProps> = ({
  region,
  appearAt,
  durationFrames = 90,
  color = accent,
  borderRadius = 18,
}) => {
  const frame = useCurrentFrame();
  if (frame < appearAt || frame > appearAt + durationFrames) return null;

  const local = frame - appearAt;

  const pulse1 = Math.max(0, Math.sin((local / 30) * Math.PI));
  const pulse2 = Math.max(0, Math.sin(((local - 30) / 30) * Math.PI));
  const intensity = Math.max(pulse1 * 0.6, pulse2);

  const fadeIn = interpolate(local, [0, 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const fadeOut = interpolate(
    local,
    [durationFrames - 18, durationFrames],
    [1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.5, 0, 0.2, 1)}
  );
  const opacity = Math.min(fadeIn, fadeOut);

  const ringWidth = 3 + intensity * 2;
  const glow1 = 6 + intensity * 18;
  const glow2 = 30 + intensity * 50;

  return (
    <div
      style={{
        position: 'absolute',
        left: region.x * FRAME_W - (region.w * FRAME_W) / 2,
        top: region.y * FRAME_H - (region.h * FRAME_H) / 2,
        width: region.w * FRAME_W,
        height: region.h * FRAME_H,
        borderRadius,
        border: ringWidth + 'px solid ' + color,
        boxShadow:
          '0 0 0 ' + Math.round(glow1) + 'px ' + color + Math.round(intensity * 50).toString(16).padStart(2, '0') + ', ' +
          '0 0 ' + Math.round(glow2) + 'px ' + color + '88',
        opacity,
        pointerEvents: 'none',
        zIndex: 60,
      }}
    />
  );
};

// PictureInPicture — animates a child component's bounding box from
// `fromBox` to `toBox` over a frame range. Boxes are PROPORTIONAL (0-1)
// of the parent frame, so the same primitive works at any aspect ratio.
//
// Use cases:
//   - a floating panel pops out from full-screen and shrinks to a corner
//   - a webcam / talking-head bubble slides between scenes
//   - any "morph one component over another" effect
import React from 'react';
import {useCurrentFrame, interpolate, Easing} from 'remotion';

export interface Box {
  x: number; // center, 0-1
  y: number; // center, 0-1
  w: number; // width,  0-1
  h: number; // height, 0-1
}

export interface PictureInPictureProps {
  children: React.ReactNode;
  fromBox: Box;
  toBox: Box;
  fromFrame: number;
  toFrame: number;
  shadow?: boolean;
  borderRadius?: number;
  easing?: (t: number) => number;
}

const FRAME_W = 1920;
const FRAME_H = 1080;

export const PictureInPicture: React.FC<PictureInPictureProps> = ({
  children,
  fromBox,
  toBox,
  fromFrame,
  toFrame,
  shadow = true,
  borderRadius = 14,
  easing = Easing.bezier(0.5, 0, 0.2, 1),
}) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [fromFrame, toFrame], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing,
  });

  const lerp = (a: number, b: number) => a + (b - a) * t;
  const x = lerp(fromBox.x, toBox.x);
  const y = lerp(fromBox.y, toBox.y);
  const w = lerp(fromBox.w, toBox.w);
  const h = lerp(fromBox.h, toBox.h);

  const widthPx = w * FRAME_W;
  const heightPx = h * FRAME_H;
  const leftPx = x * FRAME_W - widthPx / 2;
  const topPx = y * FRAME_H - heightPx / 2;

  // Inner content always renders at full 1920x1080 then scales. Lets us
  // host any component without it knowing it's been resized.
  const scale = Math.min(w, h);

  return (
    <div
      style={{
        position: 'absolute',
        left: leftPx,
        top: topPx,
        width: widthPx,
        height: heightPx,
        overflow: 'hidden',
        borderRadius: borderRadius * scale,
        boxShadow: shadow
          ? '0 ' + (24 * scale) + 'px ' + (60 * scale) + 'px rgba(0,0,0,' + (0.18 + (1 - scale) * 0.2) + ')'
          : 'none',
        background: '#fff',
      }}
    >
      <div
        style={{
          width: FRAME_W,
          height: FRAME_H,
          transform: 'scale(' + (widthPx / FRAME_W) + ',' + (heightPx / FRAME_H) + ')',
          transformOrigin: '0 0',
        }}
      >
        {children}
      </div>
    </div>
  );
};

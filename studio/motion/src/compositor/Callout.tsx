// Callout — floating cursor-label card.
//
// Timeline relative to `startFrame`:
//   [0..25]                 hidden (waiting for cursor to land)
//   [25..33]                fade in (opacity 0->1, translateY 4 -> 0)
//   [33..duration-12]       hold
//   [duration-12..duration] fade out
//
// Position: 18px offset in the given direction from the cursor target.
// Triangle pointer (8px CSS triangle) points toward the cursor target.
import React from 'react';
import {AbsoluteFill, useCurrentFrame, interpolate} from 'remotion';
import {fonts} from '../tokens';

export interface CalloutProps {
  text: string;
  position: 'above' | 'below' | 'left' | 'right';
  cursorX: number; // fractional 0..1 of 1920
  cursorY: number; // fractional 0..1 of 1080
  startFrame: number;
  durationInFrames: number;
}

const FRAME_W = 1920;
const FRAME_H = 1080;
const OFFSET = 18; // px gap between cursor and card edge
const CARD_BG = 'rgba(20,22,28,0.95)';
const ARROW = 8;

export const Callout: React.FC<CalloutProps> = ({
  text,
  position,
  cursorX,
  cursorY,
  startFrame,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const f = frame - startFrame;
  const ec = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

  if (f < 25 || f > durationInFrames) return null;

  const fadeOutStart = durationInFrames - 12;
  const opacity = interpolate(
    f,
    [25, 33, fadeOutStart, durationInFrames],
    [0, 1, 1, 0],
    ec
  );
  const ty = interpolate(f, [25, 33], [4, 0], ec);

  const tx = cursorX * FRAME_W;
  const tyAnchor = cursorY * FRAME_H;

  const cardStyle: React.CSSProperties = {
    background: CARD_BG,
    color: '#fff',
    borderRadius: 10,
    padding: '8px 14px',
    fontSize: 14,
    fontWeight: 600,
    boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
    whiteSpace: 'nowrap',
    fontFamily: fonts?.ui ?? 'system-ui',
    position: 'relative',
    display: 'inline-block',
  };

  let wrapperLeft = tx;
  let wrapperTop = tyAnchor;
  let wrapperTransform = 'translate(-50%, -50%)';

  let arrowStyle: React.CSSProperties = {position: 'absolute'};

  switch (position) {
    case 'above':
      wrapperTop = tyAnchor - OFFSET;
      wrapperTransform = 'translate(-50%, -100%)';
      arrowStyle = {
        position: 'absolute',
        left: '50%',
        bottom: -ARROW,
        marginLeft: -ARROW,
        width: 0,
        height: 0,
        borderLeft: `${ARROW}px solid transparent`,
        borderRight: `${ARROW}px solid transparent`,
        borderTop: `${ARROW}px solid ${CARD_BG}`,
      };
      break;
    case 'below':
      wrapperTop = tyAnchor + OFFSET;
      wrapperTransform = 'translate(-50%, 0)';
      arrowStyle = {
        position: 'absolute',
        left: '50%',
        top: -ARROW,
        marginLeft: -ARROW,
        width: 0,
        height: 0,
        borderLeft: `${ARROW}px solid transparent`,
        borderRight: `${ARROW}px solid transparent`,
        borderBottom: `${ARROW}px solid ${CARD_BG}`,
      };
      break;
    case 'left':
      wrapperLeft = tx - OFFSET;
      wrapperTransform = 'translate(-100%, -50%)';
      arrowStyle = {
        position: 'absolute',
        top: '50%',
        right: -ARROW,
        marginTop: -ARROW,
        width: 0,
        height: 0,
        borderTop: `${ARROW}px solid transparent`,
        borderBottom: `${ARROW}px solid transparent`,
        borderLeft: `${ARROW}px solid ${CARD_BG}`,
      };
      break;
    case 'right':
      wrapperLeft = tx + OFFSET;
      wrapperTransform = 'translate(0, -50%)';
      arrowStyle = {
        position: 'absolute',
        top: '50%',
        left: -ARROW,
        marginTop: -ARROW,
        width: 0,
        height: 0,
        borderTop: `${ARROW}px solid transparent`,
        borderBottom: `${ARROW}px solid transparent`,
        borderRight: `${ARROW}px solid ${CARD_BG}`,
      };
      break;
  }

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div
        style={{
          position: 'absolute',
          left: wrapperLeft,
          top: wrapperTop,
          transform: `${wrapperTransform} translateY(${ty}px)`,
          opacity,
          zIndex: 202,
        }}
      >
        <div style={cardStyle}>
          {text}
          <span style={arrowStyle} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

export default Callout;

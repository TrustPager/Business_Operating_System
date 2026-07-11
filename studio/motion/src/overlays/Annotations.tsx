// Annotations — the canonical caption / headline / cursor / highlight / spotlight
// overlay engine. Data-driven: takes a list of annotation objects and renders each
// at its frame window. Colour + type flow from the brand token bridge.
//
// Targets are supplied as an explicit fractional point {x, y} (0..1). The old
// per-screen ELEMENT_POSITIONS registry (measured against one product's UI) is
// intentionally NOT ported — scenes pass their own coordinates.
import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate, AbsoluteFill} from 'remotion';
import {primary, accent, primaryRgb} from '../tokens';
import {FONT_BODY} from '../fonts';
import {gradients} from '../tokens';

const FPS = 30;

const useFrameDimensions = () => {
  const {width, height} = useVideoConfig();
  return {frameWidth: width, frameHeight: height};
};

// --- Headline text overlay — big, cinematic, drives emotional beats ---
const Headline = ({x, y, text, style = 'emphasis', opacity, frame, startFrame, frameWidth = 1920, frameHeight = 1080}: any) => {
  const scaleProgress = interpolate(
    frame,
    [startFrame, startFrame + 10],
    [0.95, 1],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  const styleMap: Record<string, any> = {
    emphasis: {
      background: gradients.primary,
      color: 'white',
      borderColor: 'rgba(255,255,255,0.2)',
      shadow: `0 8px 32px rgba(${primaryRgb}, 0.3), 0 2px 8px rgba(0,0,0,0.15)`,
    },
    dark: {
      background: 'rgba(2, 8, 23, 0.92)',
      color: 'white',
      borderColor: 'rgba(255,255,255,0.08)',
      shadow: '0 8px 32px rgba(0,0,0,0.25)',
    },
    subtle: {
      background: 'rgba(255,255,255,0.95)',
      color: '#020817',
      borderColor: 'rgba(226, 232, 240, 0.5)',
      shadow: '0 4px 24px rgba(0,0,0,0.08)',
    },
    glass: {
      background: 'rgba(255,255,255,0.85)',
      color: '#020817',
      borderColor: `rgba(${primaryRgb}, 0.3)`,
      shadow: `0 8px 32px rgba(${primaryRgb}, 0.12), 0 2px 8px rgba(0,0,0,0.06)`,
    },
  };

  const s = styleMap[style] || styleMap.emphasis;

  return (
    <div style={{
      position: 'absolute',
      left: x * frameWidth,
      top: y * frameHeight,
      transform: `translate(-50%, -50%) scale(${scaleProgress})`,
      background: s.background,
      color: s.color,
      border: `1px solid ${s.borderColor}`,
      borderRadius: 14,
      padding: '14px 28px',
      fontSize: 24,
      fontWeight: 700,
      fontFamily: FONT_BODY,
      letterSpacing: '-0.02em',
      lineHeight: '32px',
      opacity,
      pointerEvents: 'none',
      zIndex: 80,
      whiteSpace: 'nowrap',
      boxShadow: s.shadow,
      backdropFilter: 'blur(8px)',
    }}>
      {text}
    </div>
  );
};

// --- Small caption text — supporting context, not the hero ---
const Caption = ({x, y, text, opacity, frameWidth = 1920, frameHeight = 1080}: any) => (
  <div style={{
    position: 'absolute',
    left: x * frameWidth,
    top: y * frameHeight,
    transform: 'translate(-50%, -50%)',
    background: 'rgba(2, 8, 23, 0.75)',
    color: 'rgba(255,255,255,0.9)',
    borderRadius: 8,
    padding: '8px 16px',
    fontSize: 16,
    fontWeight: 500,
    fontFamily: FONT_BODY,
    letterSpacing: '-0.01em',
    opacity,
    pointerEvents: 'none',
    zIndex: 75,
    whiteSpace: 'nowrap',
    boxShadow: '0 4px 16px rgba(0,0,0,0.15)',
    backdropFilter: 'blur(4px)',
  }}>
    {text}
  </div>
);

// --- Animated cursor ---
const CursorIndicator = ({x, y, opacity, frame, startFrame, frameWidth = 1920, frameHeight = 1080}: any) => {
  const floatY = interpolate(
    frame,
    [startFrame, startFrame + 30, startFrame + 60],
    [0, -4, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  return (
    <div style={{
      position: 'absolute',
      left: x * frameWidth,
      top: (y * frameHeight) + floatY,
      opacity,
      transform: 'translate(-4px, -4px)',
      pointerEvents: 'none',
      zIndex: 100,
    }}>
      <div style={{
        position: 'absolute',
        width: 44,
        height: 44,
        borderRadius: '50%',
        background: `rgba(${primaryRgb}, 0.12)`,
        transform: 'translate(-12px, -12px)',
      }} />
      <div style={{
        position: 'absolute',
        width: 14,
        height: 14,
        borderRadius: '50%',
        background: `rgba(${primaryRgb}, 0.5)`,
        transform: 'translate(-3px, -3px)',
      }} />
      <svg
        width={22}
        height={26}
        viewBox="0 0 22 26"
        fill="none"
        style={{position: 'relative', zIndex: 2, filter: 'drop-shadow(0 2px 6px rgba(0,0,0,0.3))'}}
      >
        <path
          d="M1 1L1 20L6 15L9.5 23L12.5 21.5L9 14L15 14L1 1Z"
          fill="white"
          stroke={primary}
          strokeWidth="1.5"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
};

// --- Glowing highlight box with animated pulse ---
const HighlightBox = ({x, y, width, height, color = primary, opacity, frame, startFrame}: any) => {
  const glowIntensity = interpolate(
    frame,
    [startFrame, startFrame + 20, startFrame + 40],
    [0.4, 0.7, 0.4],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  return (
    <div style={{
      position: 'absolute',
      left: x,
      top: y,
      width,
      height,
      border: `2.5px solid ${color}`,
      borderRadius: 14,
      boxShadow: `0 0 0 4px ${color}${Math.round(glowIntensity * 25).toString(16).padStart(2, '0')}, 0 0 30px ${color}${Math.round(glowIntensity * 40).toString(16).padStart(2, '0')}`,
      opacity,
      pointerEvents: 'none',
      zIndex: 50,
    }} />
  );
};

// --- Spotlight dimmer — dims everything except the target area ---
const Spotlight = ({x, y, width, height, opacity}: any) => (
  <div style={{
    position: 'absolute',
    left: x - 6,
    top: y - 6,
    width: width + 12,
    height: height + 12,
    borderRadius: 16,
    boxShadow: `0 0 0 9999px rgba(2, 8, 23, 0.3)`,
    border: `2px solid rgba(${primaryRgb}, 0.25)`,
    opacity,
    pointerEvents: 'none',
    zIndex: 45,
    background: 'transparent',
  }} />
);

// Resolve a target to a fractional {x, y} (or a pixel rect for area annotations).
// Only explicit object targets are supported — no per-screen registry.
const resolveTarget = (target: any) => {
  if (!target) return null;
  if (typeof target === 'object' && 'x' in target && 'y' in target) return target;
  return null;
};

const SingleAnnotation: React.FC<any> = ({annotation, frame, frameWidth, frameHeight}) => {
  const {type, target, text, timing, style} = annotation;
  const startFrame = Math.round((timing?.start_offset_seconds || 0) * FPS);
  const endFrame = startFrame + Math.round((timing?.duration_seconds || 2) * FPS);

  const scaleFactor = frameWidth / 1920;

  const opacity = interpolate(
    frame,
    [startFrame, startFrame + 8, endFrame - 8, endFrame],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  if (opacity <= 0) return null;

  const resolved = resolveTarget(target);

  if (type === 'text-label' || type === 'headline') {
    const pos = resolved || {x: 0.5, y: 0.5};
    return (
      <Headline
        x={pos.x}
        y={pos.y}
        text={text}
        style={style || 'emphasis'}
        opacity={opacity}
        frame={frame}
        startFrame={startFrame}
        frameWidth={frameWidth}
        frameHeight={frameHeight}
      />
    );
  }

  if (type === 'caption') {
    const pos = resolved || {x: 0.5, y: 0.5};
    return (
      <Caption
        x={pos.x}
        y={pos.y}
        text={text}
        opacity={opacity}
        frameWidth={frameWidth}
        frameHeight={frameHeight}
      />
    );
  }

  if (type === 'cursor-indicator') {
    const pos = resolved || {x: 0.5, y: 0.5};
    return (
      <CursorIndicator
        x={pos.x}
        y={pos.y}
        opacity={opacity}
        frame={frame}
        startFrame={startFrame}
        frameWidth={frameWidth}
        frameHeight={frameHeight}
      />
    );
  }

  if (type === 'highlight-box') {
    if (!resolved || !('width' in resolved)) return null;
    return (
      <HighlightBox
        x={resolved.x * frameWidth}
        y={resolved.y * frameHeight}
        width={resolved.width * scaleFactor}
        height={resolved.height * scaleFactor}
        color={style === 'accent' ? accent : primary}
        opacity={opacity}
        frame={frame}
        startFrame={startFrame}
      />
    );
  }

  if (type === 'spotlight') {
    if (!resolved || !('width' in resolved)) return null;
    return (
      <Spotlight
        x={resolved.x * frameWidth}
        y={resolved.y * frameHeight}
        width={resolved.width * scaleFactor}
        height={resolved.height * scaleFactor}
        opacity={opacity}
      />
    );
  }

  return null;
};

export const Annotations = ({annotations = []}: any) => {
  const frame = useCurrentFrame();
  const {frameWidth, frameHeight} = useFrameDimensions();

  if (!annotations || annotations.length === 0) return null;

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {annotations.map((ann: any, idx: number) => (
        <SingleAnnotation
          key={idx}
          annotation={ann}
          frame={frame}
          frameWidth={frameWidth}
          frameHeight={frameHeight}
        />
      ))}
    </AbsoluteFill>
  );
};

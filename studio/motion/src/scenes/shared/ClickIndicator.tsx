import React from 'react';
import {useCurrentFrame, interpolate, Easing, AbsoluteFill} from 'remotion';
import {primary, accent, primaryRgb, accentRgb} from '../../tokens';
import {FONT_BODY} from '../../fonts';

/**
 * ClickTarget — wraps an element to show ring + cursor + ripple on it.
 * Labels are handled separately by TutorialCaption (screen-level, never clipped).
 *
 * Usage:
 *   <ClickTarget startFrame={90} cursorFromX={-200} cursorFromY={300} color="primary">
 *     <div>The element to highlight</div>
 *   </ClickTarget>
 *
 * Colour rule (brand-neutral convention):
 *  - 'primary'   — the user navigating around their own product / app UI
 *  - 'assistant' — something being done for the user (the "assistant" accent)
 *  - any custom string is treated as the ring colour (advanced use)
 */

export type ClickColor = 'primary' | 'assistant' | string;

interface ClickPalette {
  ring: string;            // border colour of ring + ripple
  /** RGB triplet for rgba(...) opacity-templated shadows. */
  glowRgb: string;
  /** RGB triplet for spotlight background fill. */
  spotlightRgb: string;
  glowInset: string;       // rgba inset shadow
  captionGradient: string;
  captionShadow: string;
}

const PALETTES: Record<'primary' | 'assistant', ClickPalette> = {
  primary: {
    ring: primary,
    glowRgb: primaryRgb,
    spotlightRgb: '248, 250, 252',
    glowInset: `rgba(${primaryRgb}, 0.08)`,
    captionGradient: `linear-gradient(135deg, ${primary} 0%, ${accent} 100%)`,
    captionShadow: `0 4px 20px rgba(${primaryRgb}, 0.4), 0 8px 32px rgba(0,0,0,0.15)`,
  },
  assistant: {
    ring: accent,
    glowRgb: accentRgb,
    spotlightRgb: '255, 250, 248',
    glowInset: `rgba(${accentRgb}, 0.08)`,
    captionGradient: `linear-gradient(135deg, ${accent} 0%, ${primary} 100%)`,
    captionShadow: `0 4px 20px rgba(${accentRgb}, 0.4), 0 8px 32px rgba(0,0,0,0.15)`,
  },
};

function resolvePalette(color: ClickColor | undefined): ClickPalette {
  if (!color || color === 'primary') return PALETTES.primary;
  if (color === 'assistant') return PALETTES.assistant;
  // Custom string — use it as the ring colour uniformly.
  return {
    ring: color,
    glowRgb: '255, 255, 255',
    spotlightRgb: '248, 250, 252',
    glowInset: 'rgba(255, 255, 255, 0.08)',
    captionGradient: `linear-gradient(135deg, ${color}, ${color})`,
    captionShadow: `0 4px 20px ${color}66, 0 8px 32px rgba(0,0,0,0.15)`,
  };
}

const CursorSVG = ({size = 40}: {size?: number}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" style={{filter: 'drop-shadow(0 0 8px rgba(255,255,255,0.8)) drop-shadow(0 2px 6px rgba(0,0,0,0.5))'}}>
    <path d="M4 1L4 17.5L8.5 13.5L12.5 21L15.5 19.5L11.5 12L17 11.5L4 1Z" fill="#ffffff" stroke="#0f1117" strokeWidth="1.5" strokeLinejoin="round" />
  </svg>
);

export const ClickTarget = ({
  children,
  startFrame,
  duration = 55,
  cursorFromX = -300,
  cursorFromY = 200,
  pad = 12,
  borderRadius = 14,
  fit = false,
  color = 'primary',
}: {
  children: React.ReactNode;
  startFrame: number;
  duration?: number;
  cursorFromX?: number;
  cursorFromY?: number;
  pad?: number;
  borderRadius?: number;
  fit?: boolean;
  color?: ClickColor;
}) => {
  const frame = useCurrentFrame();
  const ec = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
  const easeOut = Easing.out(Easing.quad);
  const easeInOut = Easing.inOut(Easing.quad);
  const palette = resolvePalette(color);

  const f = frame - startFrame;
  const active = f >= -5 && f <= duration + 20;

  const DIM_IN = 10;
  const MOVE_START = 5;
  const MOVE_DUR = 22;
  const CLICK_AT = MOVE_START + MOVE_DUR;
  const RIPPLE_DUR = 18;
  const DIM_OUT_START = duration - 12;

  const ringOpacity = active ? interpolate(f, [DIM_IN - 2, DIM_IN + 6, DIM_OUT_START, duration], [0, 1, 1, 0], ec) : 0;
  const pulsePhase = f >= DIM_IN ? (f - DIM_IN) * 0.18 : 0;
  const ringScale = 1 + Math.sin(pulsePhase) * 0.04;
  const glowOpacity = active ? interpolate(f, [DIM_IN, DIM_IN + 8, DIM_OUT_START, duration], [0, 0.6, 0.6, 0], ec) : 0;

  const moveF = f - MOVE_START;
  const cursorX = active ? interpolate(moveF, [0, MOVE_DUR], [cursorFromX, 0], {...ec, easing: easeInOut}) : 0;
  const cursorY = active ? interpolate(moveF, [0, MOVE_DUR], [cursorFromY, 0], {...ec, easing: easeInOut}) : 0;
  const cursorArc = moveF > 0 && moveF < MOVE_DUR ? Math.sin((moveF / MOVE_DUR) * Math.PI) * -40 : 0;
  const cursorOpacity = active ? interpolate(f, [0, 6, duration - 5, duration], [0, 1, 1, 0], ec) : 0;
  const clickF = f - CLICK_AT;
  const cursorScale = clickF >= 0 && clickF < 8 ? interpolate(clickF, [0, 3, 8], [1, 0.75, 1], ec) : 1;

  const rippleOpacity = clickF >= 0 && active ? interpolate(clickF, [0, RIPPLE_DUR], [0.7, 0], ec) : 0;
  const rippleScale = clickF >= 0 && active ? interpolate(clickF, [0, RIPPLE_DUR], [0.5, 3], {...ec, easing: easeOut}) : 0;

  return (
    <div style={{position: 'relative', display: fit ? 'inline-flex' : 'flex'}}>
      <div style={fit ? {} : {flex: 1, minWidth: 0}}>{children}</div>

      {active && (
        <>
          <div style={{
            position: 'absolute',
            inset: -pad,
            borderRadius,
            border: `3px solid ${palette.ring}`,
            boxShadow: `0 0 30px rgba(${palette.glowRgb}, ${glowOpacity * 0.5}), 0 0 60px rgba(${palette.glowRgb}, ${glowOpacity * 0.2}), inset 0 0 30px ${palette.glowInset}`,
            opacity: ringOpacity,
            transform: `scale(${ringScale})`,
            pointerEvents: 'none',
            zIndex: 50,
          }} />

          <div style={{
            position: 'absolute',
            inset: -pad - 4,
            borderRadius: borderRadius + 2,
            background: `rgba(${palette.spotlightRgb}, ${glowOpacity * 0.3})`,
            boxShadow: `0 0 60px 20px rgba(${palette.glowRgb}, ${glowOpacity * 0.2})`,
            pointerEvents: 'none',
            zIndex: 49,
          }} />

          {clickF >= 0 && clickF < RIPPLE_DUR && (
            <div style={{
              position: 'absolute',
              top: '50%', left: '50%',
              width: 80, height: 80,
              marginTop: -40, marginLeft: -40,
              borderRadius: '50%',
              border: `3px solid ${palette.ring}`,
              opacity: rippleOpacity,
              transform: `scale(${rippleScale})`,
              pointerEvents: 'none',
              zIndex: 51,
            }} />
          )}

          {cursorOpacity > 0 && (
            <div style={{
              position: 'absolute',
              top: '50%', left: '50%',
              marginTop: cursorY + cursorArc - 2,
              marginLeft: cursorX - 4,
              opacity: cursorOpacity,
              transform: `scale(${cursorScale})`,
              transformOrigin: '4px 1px',
              pointerEvents: 'none',
              zIndex: 53,
            }}>
              <CursorSVG size={40} />
            </div>
          )}
        </>
      )}
    </div>
  );
};

/**
 * TutorialCaption — screen-level caption bar for click instructions.
 * Renders at the bottom of the composition, OUTSIDE all overflow containers.
 * Place as a sibling to your screen content inside AbsoluteFill.
 */
export const TutorialCaption = ({
  text,
  startFrame,
  duration,
  bottom = 48,
  color = 'primary',
}: {
  text: string;
  startFrame: number;
  duration?: number;
  bottom?: number;
  color?: ClickColor;
}) => {
  const frame = useCurrentFrame();
  const ec = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
  const easeOut = Easing.out(Easing.quad);
  const palette = resolvePalette(color);

  // Caption readability rule: on-screen time scales to length so every caption
  // can actually be read and land.
  //   <=3 words -> 1.5s (45f);  4-6 words -> 3s (90f).
  // Captions must be 6 words or fewer — write punchy, not full sentences.
  const wordCount = text.trim().split(/\s+/).filter(Boolean).length;
  const dur = duration ?? (wordCount <= 3 ? 45 : 90);

  const f = frame - startFrame;
  const active = f >= 0 && f <= dur + 10;
  if (!active) return null;

  const FADE_IN = 10;
  const FADE_OUT_START = dur - 10;

  const opacity = interpolate(f, [0, FADE_IN, FADE_OUT_START, dur], [0, 1, 1, 0], ec);
  const slideY = interpolate(f, [0, FADE_IN], [12, 0], {...ec, easing: easeOut});

  return (
    <AbsoluteFill style={{pointerEvents: 'none', zIndex: 100}}>
      <div style={{
        position: 'absolute',
        bottom,
        left: '50%',
        transform: `translateX(-50%) translateY(${slideY}px)`,
        opacity,
        fontSize: 18,
        fontWeight: 700,
        color: '#ffffff',
        fontFamily: FONT_BODY,
        background: palette.captionGradient,
        padding: '10px 28px',
        borderRadius: 14,
        whiteSpace: 'nowrap',
        boxShadow: palette.captionShadow,
        backdropFilter: 'blur(8px)',
        letterSpacing: '-0.01em',
      }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};

// Backward compat
export const ClickIndicator = ClickTarget;

// StageAutomationBadges — overlays "automation" badges on top of each
// column as they appear with a stagger. Renders a small pill with a lightning
// icon + count above each header; each badge fades in with a short delay so
// they cascade.
import React from 'react';
import {useCurrentFrame, interpolate, Easing} from 'remotion';
import {accent, accentRgb, fonts} from '../tokens';

export interface StageBadge {
  /** Center x position of the header, proportional 0-1. */
  x: number;
  /** Top y position of the header, proportional 0-1. */
  y: number;
  /** Number of automations on this stage. */
  count: number;
  /** Optional label override (default: "{count} automations"). */
  label?: string;
}

export interface StageAutomationBadgesProps {
  badges: StageBadge[];
  appearAt: number;
  staggerFrames?: number;
  color?: string;
}

const FRAME_W = 1920;
const FRAME_H = 1080;

const Lightning: React.FC<{size?: number; color?: string}> = ({size = 12, color = '#fff'}) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="none">
    <path
      d="M9 1L3 9.5h4.5l-1 5.5L13 6.5H8.5L9 1Z"
      fill={color}
    />
  </svg>
);

export const StageAutomationBadges: React.FC<StageAutomationBadgesProps> = ({
  badges,
  appearAt,
  staggerFrames = 5,
  color = accent,
}) => {
  const frame = useCurrentFrame();
  return (
    <>
      {badges.map((b, i) => {
        const start = appearAt + i * staggerFrames;
        if (frame < start) return null;
        const local = frame - start;
        const opacity = interpolate(local, [0, 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const yOffset = interpolate(local, [0, 14], [-8, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: Easing.bezier(0.34, 1.56, 0.64, 1),
        });
        const scale = interpolate(local, [0, 14], [0.85, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: Easing.bezier(0.34, 1.56, 0.64, 1),
        });
        const label = b.label || (b.count + ' automation' + (b.count === 1 ? '' : 's'));
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: b.x * FRAME_W,
              top: b.y * FRAME_H + yOffset,
              transform: 'translate(-50%, -100%) scale(' + scale + ')',
              opacity,
              display: 'inline-flex',
              alignItems: 'center',
              gap: 5,
              padding: '5px 10px',
              borderRadius: 999,
              background: color,
              color: '#fff',
              fontFamily: fonts.ui,
              fontSize: 12,
              fontWeight: 600,
              letterSpacing: '-0.005em',
              boxShadow: `0 4px 12px rgba(${accentRgb}, 0.35)`,
              whiteSpace: 'nowrap',
              pointerEvents: 'none',
              zIndex: 65,
            }}
          >
            <Lightning size={12} />
            <span>{label}</span>
          </div>
        );
      })}
    </>
  );
};

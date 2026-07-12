/**
 * Tag — small coloured label. Brand-neutral: the primary-toned variants derive
 * from the brand token, not a baked product colour.
 */
import React from 'react';
import {fonts, colors} from './theme';

const TAG_COLORS = {
  booking: {bg: colors.primarySoft, text: colors.primary},
  linkedin: {bg: 'rgba(30, 41, 59, 0.13)', text: '#1e293b'},
  direct: {bg: 'rgba(107, 114, 128, 0.1)', text: '#6b7280'},
  website: {bg: 'rgba(59, 130, 246, 0.13)', text: '#3b82f6'},
};

const getTagColors = (label) => TAG_COLORS[label.toLowerCase()] || {bg: 'rgba(107, 114, 128, 0.1)', text: '#6b7280'};

export const Tag = ({label, color, active, style: extraStyle}) => {
  if (active !== undefined) {
    // Selectable pill mode (filter UIs)
    return (
      <span style={{
        display: 'inline-flex', alignItems: 'center',
        padding: '4px 10px', borderRadius: 99,
        fontSize: 12, fontWeight: 500, fontFamily: fonts.primary,
        border: `1px solid ${active ? colors.primary : colors.border}`,
        background: active ? colors.primarySoft : 'transparent',
        color: active ? colors.primary : colors.mutedForeground,
        ...extraStyle,
      }}>
        {label}
      </span>
    );
  }
  const tagColors = color ? {bg: `${color}20`, text: color} : getTagColors(label);
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center',
      padding: '2px 6px', borderRadius: 4,
      fontSize: 10, fontWeight: 500, fontFamily: fonts.primary, lineHeight: '16px',
      background: tagColors.bg, color: tagColors.text,
      ...extraStyle,
    }}>
      {label}
    </span>
  );
};

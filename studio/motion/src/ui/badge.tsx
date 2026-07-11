/**
 * Badge — brand-neutral badge primitive with variant support.
 */
import React from 'react';
import {colors, fonts} from './theme';

const BADGE_VARIANTS = {
  default: {bg: colors.primary, color: 'white', border: 'transparent'},
  secondary: {bg: 'rgba(107,114,128,0.1)', color: '#6b7280', border: 'rgba(107,114,128,0.3)'},
  success: {bg: 'rgba(34,197,94,0.1)', color: '#15803d', border: 'rgba(34,197,94,0.3)'},
  warning: {bg: 'rgba(249,115,22,0.1)', color: '#c2410c', border: 'rgba(249,115,22,0.3)'},
  danger: {bg: 'rgba(239,68,68,0.1)', color: '#b91c1c', border: 'rgba(239,68,68,0.3)'},
  destructive: {bg: 'rgba(239,68,68,0.1)', color: '#b91c1c', border: 'rgba(239,68,68,0.3)'},
  info: {bg: 'rgba(59,130,246,0.1)', color: '#1d4ed8', border: 'rgba(59,130,246,0.3)'},
  outline: {bg: `${colors.muted}80`, color: colors.foreground, border: colors.border},
};

export const Badge = ({children = null, text = null, variant = 'default', color: customColor = null, style: extraStyle = {}}) => {
  const v = BADGE_VARIANTS[variant] || BADGE_VARIANTS.default;
  const bgColor = customColor ? `${customColor}14` : v.bg;
  const textColor = customColor || v.color;
  const borderColor = customColor ? `${customColor}30` : v.border;

  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 4,
      padding: '2px 10px', borderRadius: 99,
      fontSize: 12, fontWeight: 600, fontFamily: fonts.primary,
      background: bgColor, color: textColor,
      border: `1px solid ${borderColor}`,
      ...extraStyle,
    }}>
      {children || text}
    </span>
  );
};

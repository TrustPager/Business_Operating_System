/**
 * CleanButton — brand-neutral button primitive with variant + size props.
 */
import React from 'react';
import {colors, fonts, gradients, shadows} from './theme';

export const CleanButton = ({children, variant = 'default', size = null, small = false, color = null, icon = null, style: extraStyle = {}}: {children?: any; variant?: string; size?: any; small?: boolean; color?: any; icon?: any; style?: any}) => {
  const isSmall = small || size === 'sm';

  const iconSize = isSmall ? 14 : 20;
  const iconColor = variant === 'outline' ? (color || colors.primary) : variant === 'destructive' ? 'white' : variant === 'ghost' ? colors.mutedForeground : 'white';
  const renderedIcon = icon
    ? (typeof icon === 'function'
        ? React.createElement(icon, {size: iconSize, color: iconColor})
        : React.cloneElement(icon, {size: iconSize, color: iconColor}))
    : null;

  const pad = isSmall ? '6px 8px' : '12px 24px';
  const gap = isSmall ? 6 : 12;

  if (variant === 'destructive') {
    return (
      <div style={{
        display: 'inline-flex', alignItems: 'center',
        padding: pad, gap, borderRadius: 16,
        background: 'linear-gradient(to right, #ef4444, #dc2626)',
        color: 'white', fontSize: isSmall ? 12 : 14, fontWeight: 600, fontFamily: fonts.primary,
        boxShadow: '0 4px 12px rgba(239,68,68,0.25)',
        position: 'relative', overflow: 'hidden',
        ...extraStyle,
      }}>
        <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(to bottom, rgba(255,255,255,0.1), transparent)'}} />
        <div style={{position: 'relative', display: 'flex', alignItems: 'center', gap}}>
          {renderedIcon}
          {children}
        </div>
      </div>
    );
  }

  if (variant === 'ghost') {
    return (
      <div style={{
        display: 'inline-flex', alignItems: 'center',
        padding: isSmall ? '6px 8px' : '8px 16px', gap: isSmall ? 6 : 6,
        borderRadius: 8,
        fontSize: isSmall ? 12 : 14, fontWeight: 500, fontFamily: fonts.primary,
        color: colors.mutedForeground,
        ...extraStyle,
      }}>
        {renderedIcon}
        {children}
      </div>
    );
  }

  if (variant === 'outline') {
    const c = color || colors.primary;
    return (
      <div style={{
        display: 'inline-flex', alignItems: 'center',
        padding: pad, gap, borderRadius: 16,
        border: `2px solid ${c}30`,
        background: colors.card,
        color: c, fontSize: isSmall ? 12 : 14, fontWeight: 600, fontFamily: fonts.primary,
        boxShadow: '0 4px 12px rgba(0,0,0,0.06)',
        ...extraStyle,
      }}>
        {renderedIcon}
        {children}
      </div>
    );
  }

  // Default variant — gradient primary
  return (
    <div style={{
      display: 'inline-flex', alignItems: 'center',
      padding: pad, gap, borderRadius: 16,
      background: gradients.primary, color: 'white',
      fontSize: isSmall ? 12 : 14, fontWeight: 600, fontFamily: fonts.primary,
      position: 'relative', overflow: 'hidden',
      boxShadow: shadows.card,
      ...extraStyle,
    }}>
      <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(to bottom, rgba(255,255,255,0.1), transparent)'}} />
      <div style={{position: 'relative', display: 'flex', alignItems: 'center', gap}}>
        {renderedIcon}
        {children}
      </div>
    </div>
  );
};

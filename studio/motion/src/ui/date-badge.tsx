/**
 * DateBadge — small date label with optional colour.
 */
import React from 'react';
import {colors, fonts} from './theme';

export const DateBadge = ({date, bgColor, borderColor}) => (
  <span style={{
    display: 'inline-block', padding: '2px 8px', borderRadius: 4,
    fontSize: 12, fontWeight: 500, fontFamily: fonts.primary,
    background: bgColor || 'rgba(241, 245, 249, 0.5)',
    border: `1px solid ${borderColor || colors.borderHalf}`,
    color: colors.foreground,
  }}>
    {date}
  </span>
);

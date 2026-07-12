/**
 * FormTextarea — multi-line text input display.
 */
import React from 'react';
import {colors, fonts} from './theme';

export const FormTextarea = ({label, value, placeholder, rows = 3}) => (
  <div style={{marginBottom: 16}}>
    {label && (
      <label style={{
        display: 'block', fontSize: 14, fontWeight: 600,
        color: colors.foreground, fontFamily: fonts.primary, marginBottom: 6,
      }}>
        {label}
      </label>
    )}
    <div style={{
      padding: '8px 12px', borderRadius: 6,
      border: `1px solid ${colors.border}`, background: colors.card,
      fontSize: 14, color: value ? colors.foreground : 'rgba(100, 112, 134, 0.5)',
      fontWeight: value ? 500 : 400, fontFamily: fonts.primary,
      minHeight: rows * 24 + 16, lineHeight: '20px',
    }}>
      {value || placeholder}
    </div>
  </div>
);

/**
 * FormInput — standard form input display (used in modals).
 */
import React from 'react';
import {colors, fonts} from './theme';

export const FormInput = ({label, value, placeholder, required, icon: Icon}) => (
  <div style={{marginBottom: 16}}>
    {label && (
      <label style={{
        display: 'block', fontSize: 14, fontWeight: 600,
        color: colors.foreground, fontFamily: fonts.primary, marginBottom: 6,
      }}>
        {label}
        {required && <span style={{color: colors.error, marginLeft: 4}}>*</span>}
      </label>
    )}
    <div style={{
      display: 'flex', alignItems: 'center', gap: 8,
      height: 40, padding: '0 12px', borderRadius: 6,
      border: `1px solid ${value ? colors.primary : colors.border}`,
      background: colors.card, fontFamily: fonts.primary,
    }}>
      {Icon && <Icon size={16} color={colors.mutedForeground} />}
      <span style={{
        flex: 1, fontSize: 14,
        color: value ? colors.foreground : 'rgba(100, 112, 134, 0.5)',
        fontWeight: value ? 500 : 400,
        overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
      }}>
        {value || placeholder}
      </span>
    </div>
  </div>
);

/**
 * FormDropdown — dropdown trigger display (used in modals).
 */
import React from 'react';
import {colors, fonts} from './theme';

export const FormDropdown = ({label, value, placeholder, icon: ChevronIcon}) => (
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
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      height: 40, padding: '0 12px', borderRadius: 6,
      border: `1px solid ${value ? colors.primary : colors.border}`,
      background: colors.card, fontSize: 14,
      color: value ? colors.foreground : 'rgba(100, 112, 134, 0.5)',
      fontWeight: value ? 500 : 400, fontFamily: fonts.primary,
    }}>
      <span>{value || placeholder}</span>
      {ChevronIcon && <ChevronIcon size={16} color={colors.mutedForeground} />}
    </div>
  </div>
);

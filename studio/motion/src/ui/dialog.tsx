/**
 * ModalOverlay, ModalCard, ModalHeader, ModalFooter — brand-neutral modal shell.
 */
import React from 'react';
import {colors, fonts, gradients, shadows} from './theme';

export const ModalOverlay = ({children, style: extraStyle = {}}) => (
  <div style={{
    position: 'absolute', inset: 0,
    background: 'rgba(0, 0, 0, 0.6)', backdropFilter: 'blur(4px)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    ...extraStyle,
    zIndex: 200,
  }}>
    {children}
  </div>
);

export const ModalCard = ({children, width = 520, style: extraStyle = {}}) => (
  <div style={{
    width,
    background: colors.card,
    borderRadius: 12, border: '1px solid rgba(226, 232, 240, 0.3)',
    boxShadow: '0 25px 50px -12px rgba(0,0,0,0.25)', overflow: 'hidden',
    ...extraStyle,
  }}>
    {children}
  </div>
);

export const ModalHeader = ({icon: Icon = null, title = null, subtitle = null, children = null, style: extraStyle = {}}) => (
  <div style={{padding: '24px 24px 16px', borderBottom: `1px solid ${colors.borderHalf}`, ...extraStyle}}>
    {children || (
      <div style={{display: 'flex', alignItems: 'center', gap: 12}}>
        {Icon && (
          <div style={{
            width: 36, height: 36, borderRadius: 8,
            background: gradients.primary,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: shadows.card,
          }}>
            <Icon size={18} color="white" />
          </div>
        )}
        <div>
          <div style={{fontSize: 16, fontWeight: 700, color: colors.foreground, fontFamily: fonts.primary}}>{title}</div>
          {subtitle && <div style={{fontSize: 13, color: colors.mutedForeground, fontFamily: fonts.primary, marginTop: 2}}>{subtitle}</div>}
        </div>
      </div>
    )}
  </div>
);

export const ModalFooter = ({children}) => (
  <div style={{
    padding: '16px 24px', borderTop: `1px solid ${colors.borderHalf}`,
    display: 'flex', justifyContent: 'flex-end', gap: 12,
  }}>
    {children}
  </div>
);

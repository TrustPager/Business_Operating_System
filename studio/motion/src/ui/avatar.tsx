/**
 * AvatarCircle, AvatarGroup — brand-neutral extracted UI primitive.
 */
import React from 'react';
import {fonts, gradients, colors} from './theme';

export const AvatarCircle = ({initials, size = 24, index = 0, overlap = false, variant = 'default', imageUrl}: any) => {
  const isProfile = variant === 'profile';
  return (
    <div style={{
      width: size, height: size, borderRadius: '50%',
      background: imageUrl ? 'transparent' : isProfile ? gradients.primary : colors.primarySoft,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontSize: Math.max(9, size * 0.38), fontWeight: 700,
      color: isProfile ? 'white' : colors.primary,
      fontFamily: fonts.primary, textTransform: 'uppercase',
      border: '2px solid white', boxShadow: '0 1px 2px rgba(0,0,0,0.06)',
      marginLeft: overlap ? -6 : 0, position: 'relative',
      zIndex: overlap ? 1 : 2, flexShrink: 0, letterSpacing: '-0.02em', overflow: 'hidden',
    }}>
      {imageUrl ? (
        <img src={imageUrl} style={{width: '100%', height: '100%', objectFit: 'cover', display: 'block'}} />
      ) : (
        (initials || '?').toUpperCase()
      )}
    </div>
  );
};

export const AvatarGroup = ({avatars = [], avatarUrls = [], size = 24, maxVisible = 2}: any) => {
  const visible = avatars.slice(0, maxVisible);
  const overflow = avatars.length - maxVisible;
  return (
    <div style={{display: 'flex', alignItems: 'center'}}>
      {visible.map((a, i) => (
        <AvatarCircle key={i} initials={a} size={size} index={i} overlap={i > 0} imageUrl={avatarUrls[i]} />
      ))}
      {overflow > 0 && (
        <div style={{
          width: size, height: size, borderRadius: '50%',
          background: colors.muted, display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: Math.max(8, size * 0.35), fontWeight: 600,
          color: colors.mutedForeground, fontFamily: fonts.primary,
          border: '2px solid white', marginLeft: -6, position: 'relative', zIndex: 0,
        }}>
          +{overflow}
        </div>
      )}
    </div>
  );
};

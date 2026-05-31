// Avatar pool for thumbnail heroes.
//
// The thumbnails reference 5 portrait images. Each fictional name used
// across heroes maps to one of these 5 so the same person always wears
// the same face.
//
// To add a new avatar: drop another URL in AVATARS and add the name to
// NAME_MAP. To swap an avatar globally: change its URL here once.
//
// IMG_BASE — replace with a CDN URL hosting your 5 avatar files. The
// filenames below are illustrative; swap them for your actual files.

const IMG_BASE = 'https://your-cdn.example.com/avatars';

export const AVATARS = {
  asianWoman:        `${IMG_BASE}/avatar-asian-woman.webp`,
  olderManTie:       `${IMG_BASE}/avatar-older-man-tie.webp`,
  youngManBlazer:    `${IMG_BASE}/avatar-young-man-blazer.webp`,
  manWithGlasses:    `${IMG_BASE}/avatar-man-with-glasses.webp`,
  blondeWoman:       `${IMG_BASE}/avatar-blonde-woman.webp`,
};

const POOL = [
  AVATARS.asianWoman,
  AVATARS.olderManTie,
  AVATARS.youngManBlazer,
  AVATARS.manWithGlasses,
  AVATARS.blondeWoman,
];

// Stable mapping: same name always gets the same avatar.
// Hash the name into the pool so callers don't need a manual map.
const hashName = (name) => {
  let h = 0;
  for (let i = 0; i < name.length; i++) h = ((h << 5) - h + name.charCodeAt(i)) | 0;
  return Math.abs(h);
};

export const avatarFor = (name) => POOL[hashName(name) % POOL.length];

// Helper component — drop-in <Avatar name="Saskia Williams" size={32} />
export const Avatar = ({ name, size = 32, style = {} }) => (
  <img
    src={avatarFor(name)}
    alt=""
    style={{
      width: size,
      height: size,
      borderRadius: '50%',
      objectFit: 'cover',
      flexShrink: 0,
      boxShadow: '0 1px 3px rgba(15,17,23,0.15)',
      ...style,
    }}
  />
);

// Variant with a coloured ring around the avatar — used where the previous
// design had a coloured initials circle to anchor the brand palette.
export const RingedAvatar = ({ name, size = 32, ringColor = '#29c6c6', style = {} }) => (
  <div style={{
    width: size, height: size, borderRadius: '50%',
    padding: 2, background: ringColor,
    flexShrink: 0,
    ...style,
  }}>
    <img
      src={avatarFor(name)}
      alt=""
      style={{
        width: '100%', height: '100%',
        borderRadius: '50%',
        objectFit: 'cover',
        display: 'block',
        border: '1.5px solid #fff',
      }}
    />
  </div>
);

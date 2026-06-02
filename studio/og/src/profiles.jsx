// Avatar pool for OG-image heroes (ContactsHero, etc.).
//
// Self-contained: the pool points at the AI-team portraits committed under
// public/agents/ — the same files AgentHubHero uses. No external CDN, no
// network dependency, works offline and in headless puppeteer renders.
//
// Each fictional name maps deterministically to one portrait so the same
// person always wears the same face across every hero. To swap the pool,
// drop your own square portraits in public/agents/ and edit POOL below.

const POOL = [
  '/agents/Mira.png',
  '/agents/Marty.png',
  '/agents/Lyra.png',
  '/agents/Orion.png',
  '/agents/Sable.png',
];

// Stable mapping: same name always gets the same avatar.
const hashName = (name) => {
  let h = 0;
  for (let i = 0; i < name.length; i++) h = ((h << 5) - h + name.charCodeAt(i)) | 0;
  return Math.abs(h);
};

export const avatarFor = (name) => POOL[hashName(name) % POOL.length];

// Drop-in <Avatar name="Saskia Williams" size={32} />
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

// Variant with a coloured ring — anchors the brand palette around a face.
export const RingedAvatar = ({ name, size = 32, ringColor = 'var(--brand-primary)', style = {} }) => (
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

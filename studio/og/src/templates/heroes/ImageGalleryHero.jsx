// ImageGalleryHero — vertical stack of real images (typically website
// screenshots). Use for pages that ARE visual content rather than UI
// product surfaces — e.g. /website on FinalPiece (which shows a portfolio
// of client builds), case-study pages, gallery pages.
//
// Each image renders inside a browser-chrome frame so the OG image
// communicates "websites" without needing words. Bleeds off the bottom.
//
// Data shape via samples.json:
//
//   "data": {
//     "hero": "image-gallery",
//     "heroImages": [
//       { "src": "/portfolio/portfolio_website_CardiacResponder.webp", "url": "cardiacresponder.com" },
//       { "src": "/portfolio/portfolio_website_Resolve.webp",          "url": "resolveservices.com.au" },
//       ...
//     ]
//   }
//
// Source files for FinalPiece live at
//   D:/Dev/FinalPiece-NewDesign/public/portfolio/
// — copy what you need into OG_Images/public/portfolio/ to make it
// reachable from the Vite dev server.

import React from 'react';
import { colors } from '../../theme.js';
const DEFAULT_IMAGES = [
  { src: '/portfolio/portfolio_website_CardiacResponder.webp', url: 'cardiacresponder.com' },
  { src: '/portfolio/portfolio_website_Resolve.webp',           url: 'resolveservices.com.au' },
  { src: '/portfolio/portfolio_website_Ingles.webp',            url: 'inglesarchitecture.com' },
  { src: '/portfolio/portfolio_website_FounderForge.webp',      url: 'founderforge.app' },
  { src: '/portfolio/portfolio_website_TrustPager.webp',        url: 'trustpager.com' },
];

const BrowserFrame = ({ src, url }) => (
  <div style={{
    background: '#fff',
    borderRadius: 10,
    overflow: 'hidden',
    border: '1px solid rgba(226,232,240,0.7)',
    boxShadow: '0 4px 14px rgba(15,17,23,0.06)',
    display: 'flex', flexDirection: 'column',
    flexShrink: 0,
  }}>
    {/* Browser chrome with URL */}
    <div style={{
      display: 'flex', alignItems: 'center', gap: 6,
      background: '#f1f5f9',
      padding: '6px 10px',
      borderBottom: '1px solid rgba(226,232,240,0.7)',
    }}>
      <div style={{ display: 'flex', gap: 3 }}>
        {[0, 1, 2].map((i) => (
          <div key={i} style={{ width: 7, height: 7, borderRadius: '50%', background: '#cbd5e1' }} />
        ))}
      </div>
      <div style={{
        flex: 1, marginLeft: 6,
        background: '#fff', borderRadius: 4,
        padding: '3px 8px',
        fontSize: 9, color: colors.mutedForeground, fontWeight: 500,
        border: '1px solid rgba(226,232,240,0.6)',
        overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
      }}>{url}</div>
    </div>
    {/* Screenshot */}
    <img
      src={src}
      alt={url}
      style={{
        width: '100%',
        height: 200,
        objectFit: 'cover',
        objectPosition: 'top center',
        display: 'block',
      }}
    />
  </div>
);

export const ImageGalleryHero = ({ brand, data }) => {
  const images = data?.heroImages || DEFAULT_IMAGES;
  return (
    <div style={{
      background: '#fff',
      borderRadius: 18,
      padding: 16,
      boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
      display: 'flex', flexDirection: 'column', gap: 12,
    }}>
      {/* Header — colour anchor */}
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '4px 4px 10px',
        borderBottom: '1px solid rgba(226,232,240,0.7)',
      }}>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8,
          fontSize: 15, fontWeight: 800, color: colors.foreground,
          letterSpacing: '-0.015em',
        }}>
          <div style={{
            width: 9, height: 9, borderRadius: '50%',
            background: 'var(--brand-primary)',
            boxShadow: `0 0 0 5px ${'color-mix(in srgb, var(--brand-primary) 22%, transparent)'}`,
          }} />
          Recent Builds
        </div>
        <div style={{
          fontSize: 10, fontWeight: 800, letterSpacing: '0.12em',
          color: 'var(--brand-primary)',
          background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
          padding: '4px 9px', borderRadius: 999,
        }}>{images.length}+ LIVE</div>
      </div>
      {images.map((img, i) => <BrowserFrame key={i} src={img.src} url={img.url} />)}
    </div>
  );
};

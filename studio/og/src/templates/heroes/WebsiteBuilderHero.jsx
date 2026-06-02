// WebsiteBuilderHero — a website preview rendered top-to-bottom inside a
// browser chrome. Outcome framing: this is the FINISHED website you'll get,
// not a builder UI. Hero stripe, feature row, social-proof block, doctor
// roster, CTA — all visible in miniature. Bleeds off the bottom.
//
// Brand-aware via CSS variables. FinalPiece renders purple/blue/pink,
// TrustPager renders teal/green. Per-page accent overrides via
// brand.accentSets[gradientKey] let FinalPiece /crm render teal/green
// to match the actual /crm page.
//
// Family pattern: DOCUMENT (one polished artefact, top-to-bottom).

import React from 'react';
import { colors } from '../../theme.js';
const BrowserChrome = ({ url }) => (
  <div style={{
    display: 'flex', alignItems: 'center', gap: 6,
    background: '#f1f5f9',
    padding: '8px 10px',
    borderBottom: '1px solid rgba(226,232,240,0.7)',
    borderTopLeftRadius: 12, borderTopRightRadius: 12,
  }}>
    <div style={{ display: 'flex', gap: 4 }}>
      {['#cbd5e1', '#cbd5e1', '#cbd5e1'].map((c, i) => (
        <div key={i} style={{ width: 8, height: 8, borderRadius: '50%', background: c }} />
      ))}
    </div>
    <div style={{
      flex: 1, marginLeft: 8,
      background: '#fff', borderRadius: 6,
      padding: '4px 10px',
      fontSize: 10, color: colors.mutedForeground, fontWeight: 500,
      border: '1px solid rgba(226,232,240,0.7)',
      letterSpacing: '0.01em',
    }}>{url || 'coastalhealth.com.au'}</div>
  </div>
);

const HeroStrip = () => (
  <div style={{
    padding: '18px 16px 14px',
    background: 'var(--brand-gradient)',
    color: '#fff',
  }}>
    <div style={{
      fontSize: 8, fontWeight: 800, letterSpacing: '0.12em',
      opacity: 0.85, marginBottom: 6,
    }}>★ TRUSTED BY 200+ FAMILIES</div>
    <div style={{
      fontSize: 22, fontWeight: 800, letterSpacing: '-0.02em',
      lineHeight: 1.1, marginBottom: 6,
    }}>Better Health.<br />Closer to Home.</div>
    <div style={{
      fontSize: 10, opacity: 0.9, lineHeight: 1.4,
      marginBottom: 10, maxWidth: 280,
    }}>Family doctors, allied health and pathology — all under one roof in Byron Bay.</div>
    <div style={{ display: 'flex', gap: 6 }}>
      <div style={{
        padding: '6px 12px', background: '#fff',
        color: 'var(--brand-primary)', fontSize: 10, fontWeight: 800,
        borderRadius: 6, letterSpacing: '-0.01em',
      }}>Book Online →</div>
      <div style={{
        padding: '6px 12px', background: 'rgba(255,255,255,0.15)',
        color: '#fff', fontSize: 10, fontWeight: 700,
        borderRadius: 6, border: '1px solid rgba(255,255,255,0.3)',
      }}>Our Services</div>
    </div>
  </div>
);

const FeatureRow = () => (
  <div style={{
    padding: '14px 16px',
    display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8,
    borderBottom: '1px solid rgba(226,232,240,0.7)',
  }}>
    {[
      { icon: '👨‍⚕️', label: 'GP & Allied Health' },
      { icon: '🩺', label: 'On-site Pathology' },
      { icon: '📅', label: 'Same-day Bookings' },
    ].map((f, i) => (
      <div key={i} style={{
        display: 'flex', flexDirection: 'column', alignItems: 'center',
        gap: 4, padding: '4px 2px',
      }}>
        <div style={{ fontSize: 18 }}>{f.icon}</div>
        <div style={{
          fontSize: 8, fontWeight: 700, color: colors.foreground,
          textAlign: 'center', letterSpacing: '-0.005em',
        }}>{f.label}</div>
      </div>
    ))}
  </div>
);

const TestimonialBlock = () => (
  <div style={{
    padding: '14px 16px',
    background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
    borderBottom: '1px solid rgba(226,232,240,0.7)',
  }}>
    <div style={{
      display: 'flex', gap: 1, color: '#facc15',
      fontSize: 10, marginBottom: 6,
    }}>★★★★★</div>
    <div style={{
      fontSize: 11, fontWeight: 600, color: colors.foreground,
      lineHeight: 1.4, letterSpacing: '-0.005em', marginBottom: 6,
      fontStyle: 'italic',
    }}>"Quickest appointment I've ever booked. The whole family is signed up now."</div>
    <div style={{
      fontSize: 9, fontWeight: 700, color: colors.mutedForeground,
      letterSpacing: '0.02em',
    }}>— Sarah M. · Byron Bay</div>
  </div>
);

const DoctorsRow = () => (
  <div style={{
    padding: '14px 16px',
    borderBottom: '1px solid rgba(226,232,240,0.7)',
  }}>
    <div style={{
      fontSize: 9, fontWeight: 800, letterSpacing: '0.1em',
      color: 'var(--brand-primary-deep)', marginBottom: 8,
    }}>OUR DOCTORS</div>
    <div style={{ display: 'flex', gap: 6 }}>
      {['Dr Patel', 'Dr Chen', 'Dr Reilly', 'Dr Naidoo'].map((name, i) => (
        <div key={i} style={{
          flex: 1, padding: '8px 6px',
          background: '#fff',
          border: '1px solid rgba(226,232,240,0.9)',
          borderRadius: 6,
          textAlign: 'center',
        }}>
          <div style={{
            width: 22, height: 22, borderRadius: '50%',
            background: 'var(--brand-gradient)',
            margin: '0 auto 4px',
          }} />
          <div style={{
            fontSize: 8, fontWeight: 700, color: colors.foreground,
          }}>{name}</div>
        </div>
      ))}
    </div>
  </div>
);

const CTABlock = () => (
  <div style={{
    padding: '14px 16px',
    background: 'var(--brand-primary)',
    color: '#fff',
    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    gap: 10,
  }}>
    <div>
      <div style={{
        fontSize: 13, fontWeight: 800, letterSpacing: '-0.01em',
      }}>Need to see a GP today?</div>
      <div style={{
        fontSize: 9, opacity: 0.85, marginTop: 2,
      }}>Same-day appointments still available.</div>
    </div>
    <div style={{
      padding: '7px 14px', background: '#fff',
      color: 'var(--brand-primary)', fontSize: 10, fontWeight: 800,
      borderRadius: 6, letterSpacing: '-0.01em', whiteSpace: 'nowrap',
    }}>Book Now →</div>
  </div>
);

export const WebsiteBuilderHero = () => {
  return (
    <div style={{
      background: '#fff',
      borderRadius: 18,
      boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
      display: 'flex', flexDirection: 'column',
      overflow: 'hidden',
    }}>
      <BrowserChrome />
      <HeroStrip />
      <FeatureRow />
      <TestimonialBlock />
      <DoctorsRow />
      <CTABlock />
    </div>
  );
};

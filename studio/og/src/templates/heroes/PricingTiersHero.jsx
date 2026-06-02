// PricingTiersHero — vertical stack of pricing tier cards.
//
// Outcome framing: the user sees the EXACT cards they'll see on the
// pricing page — same prices, same eyebrows, same accents. No invented
// data.
//
// REAL DATA SOURCE: D:\Dev\FinalPiece-NewDesign\src\pages\PricingPage.tsx
// — keep in sync when prices change.
//
// Brand-aware: tier accent colours come from CSS variables set by
// OgImage.jsx on the canvas root (--brand-primary, --brand-secondary,
// --brand-accent). FinalPiece renders blue/purple/pink, TrustPager
// renders teal/green/blue, future clients render whatever their
// brand.json defines. No JS branching by brand name.
//
// Family pattern: CARD STACK.

import React from 'react';
import { colors } from '../../theme.js';

// Tier → semantic CSS var. The brand defines the actual colours; this
// hero just decides which "slot" each tier fills.
const TIER_ACCENT = {
  free:       'var(--brand-secondary)',  // FP blue, TP green
  pro:        'var(--brand-primary)',    // FP purple, TP teal — main brand on the popular tier
  enterprise: 'var(--brand-accent)',     // FP pink, TP blue
};

const POPULAR_GRADIENT = 'linear-gradient(135deg, var(--brand-secondary) 0%, var(--brand-primary) 50%, var(--brand-accent) 100%)';

const PLANS = [
  {
    key: 'free',
    eyebrow: 'No commitment',
    name: 'Free',
    price: '$0',
    unit: 'forever',
    features: [
      'Scheduling',
      'Forms · Notepad · Whiteboards',
      'Reputation',
      'Pay-as-you-go AI',
    ],
  },
  {
    key: 'pro',
    eyebrow: 'Popular',
    name: 'Pro',
    price: '$129',
    unit: '/ user / month',
    subUnit: 'billed monthly',
    popular: true,
    features: [
      'Unlimited users, pipelines & records',
      '10,000 credits / user / month',
      'Voice agents, AI, lead gen',
      'Priority support · free migration',
    ],
  },
  {
    key: 'enterprise',
    eyebrow: 'Custom fit',
    name: 'Enterprise',
    price: 'Custom',
    unit: 'on request',
    features: [
      'Everything in Pro',
      'Volume credit rate',
      'SSO + custom integrations',
      'Named account manager',
    ],
  },
];

const Check = ({ color }) => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" style={{ flexShrink: 0 }}>
    <path d="M5 12l5 5L20 7" stroke={color} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const TierCard = ({ plan }) => {
  const accent = TIER_ACCENT[plan.key];
  return (
    <div style={{
      position: 'relative',
      background: '#fff',
      border: plan.popular ? `1.5px solid ${accent}` : '1px solid rgba(226,232,240,0.9)',
      borderRadius: 14,
      padding: '12px 14px',
      boxShadow: plan.popular
        ? `0 8px 22px color-mix(in srgb, ${accent} 30%, transparent), 0 0 0 1px color-mix(in srgb, ${accent} 16%, transparent)`
        : '0 1px 2px rgba(15,17,23,0.04)',
      display: 'flex', flexDirection: 'column', gap: 6,
    }}>
      {plan.popular && (
        <div style={{
          position: 'absolute', top: -9, right: 12,
          fontSize: 9, fontWeight: 800, letterSpacing: '0.12em',
          color: '#fff', background: POPULAR_GRADIENT,
          padding: '4px 9px', borderRadius: 999,
          boxShadow: `0 3px 8px color-mix(in srgb, ${accent} 45%, transparent)`,
        }}>POPULAR</div>
      )}
      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', gap: 8 }}>
        <div>
          <div style={{
            fontSize: 9, fontWeight: 800, letterSpacing: '0.1em',
            textTransform: 'uppercase',
            color: accent,
            marginBottom: 2,
          }}>{plan.eyebrow}</div>
          <div style={{
            fontSize: 16, fontWeight: 800, color: colors.foreground,
            letterSpacing: '-0.015em',
          }}>{plan.name}</div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{
            fontSize: 22, fontWeight: 800, color: colors.foreground,
            letterSpacing: '-0.025em', lineHeight: 1,
          }}>{plan.price}</div>
          <div style={{
            fontSize: 9.5, fontWeight: 600, color: colors.mutedForeground,
            letterSpacing: '-0.005em', marginTop: 2,
          }}>{plan.unit}</div>
          {plan.subUnit && (
            <div style={{
              fontSize: 9, fontWeight: 500, color: colors.mutedForeground,
              letterSpacing: '-0.005em', marginTop: 1, fontStyle: 'italic',
            }}>{plan.subUnit}</div>
          )}
        </div>
      </div>
      <div style={{
        display: 'flex', flexDirection: 'column', gap: 4,
        paddingTop: 8, borderTop: '1px solid rgba(226,232,240,0.7)',
      }}>
        {plan.features.map((f, i) => (
          <div key={i} style={{
            display: 'flex', alignItems: 'center', gap: 7,
            fontSize: 11, fontWeight: 500, color: colors.foreground,
          }}>
            <Check color={accent} />
            <span>{f}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export const PricingTiersHero = () => (
  <div style={{
    background: '#fff',
    borderRadius: 18,
    padding: 16,
    boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
    display: 'flex', flexDirection: 'column', gap: 10,
  }}>
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
          boxShadow: '0 0 0 5px color-mix(in srgb, var(--brand-primary) 22%, transparent)',
        }} />
        The price list
      </div>
      <div style={{
        display: 'flex', gap: 3,
        background: 'rgba(241,245,249,0.8)',
        padding: 3, borderRadius: 7,
        fontSize: 10, fontWeight: 700, letterSpacing: '-0.005em',
      }}>
        <span style={{
          padding: '3px 9px', borderRadius: 5,
          background: '#fff', color: colors.foreground,
          boxShadow: '0 1px 2px rgba(15,17,23,0.08)',
        }}>Monthly</span>
        <span style={{ padding: '3px 9px', borderRadius: 5, color: colors.mutedForeground }}>Annual</span>
      </div>
    </div>
    {PLANS.map((p) => <TierCard key={p.key} plan={p} />)}
  </div>
);

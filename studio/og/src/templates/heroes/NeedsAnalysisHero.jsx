// Needs Analysis hero — vertical stack of AI-generated proposal sections.
//
// Outcome framing: AI built the whole proposal — exec summary, needs,
// products with prices, deliverables, strategy notes. Reads as a
// generated document scrolling down the page.

import React from 'react';
import { colors } from '../../theme.js';

const SHIMMER_LINES = [
  { w: '100%' }, { w: '94%' }, { w: '88%' }, { w: '76%' },
];

const Section = ({ icon, iconColor, label, children }) => (
  <div style={{
    background: '#fff',
    borderRadius: 12,
    padding: '12px 14px',
    border: '1px solid rgba(226,232,240,0.7)',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 9 }}>
      <div style={{
        width: 22, height: 22, borderRadius: 6,
        background: `${`color-mix(in srgb, ${iconColor} 12%, transparent)`}`,
        color: iconColor, fontSize: 12, fontWeight: 800,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>{icon}</div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.10em',
        color: iconColor,
      }}>{label}</span>
      <span style={{ flex: 1 }} />
      <span style={{
        display: 'inline-flex', alignItems: 'center', gap: 4,
        fontSize: 9, fontWeight: 800, letterSpacing: '0.08em',
        color: 'var(--brand-primary-deep)',
        background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
        padding: '2px 7px', borderRadius: 999,
      }}>✦ AI</span>
    </div>
    {children}
  </div>
);

const ParaBody = ({ children }) => (
  <div style={{
    fontSize: 11.5, color: colors.foreground, fontWeight: 500,
    lineHeight: 1.45, letterSpacing: '-0.005em',
  }}>{children}</div>
);

const NeedItem = ({ n, sol }) => (
  <div style={{
    background: 'rgba(248,250,252,0.6)',
    borderRadius: 8,
    padding: '8px 10px',
    marginBottom: 6,
    border: '1px solid rgba(226,232,240,0.5)',
  }}>
    <div style={{ fontSize: 11.5, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.005em', lineHeight: 1.3 }}>{n}</div>
    <div style={{ fontSize: 10.5, color: 'var(--brand-primary-deep)', fontWeight: 700, marginTop: 3, letterSpacing: '-0.005em', lineHeight: 1.3 }}>→ {sol}</div>
  </div>
);

const PriceLine = ({ name, price, last = false }) => (
  <div style={{
    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    padding: '7px 0',
    borderBottom: last ? 'none' : '1px dashed rgba(226,232,240,0.7)',
  }}>
    <span style={{
      fontSize: 11.5, fontWeight: 700, color: colors.foreground,
      letterSpacing: '-0.005em',
    }}>{name}</span>
    <span style={{
      fontSize: 13, fontWeight: 800, color: colors.foreground,
      letterSpacing: '-0.015em',
    }}>{price}</span>
  </div>
);

export const NeedsAnalysisHero = () => (
  <div style={{
    background: '#fff',
    borderRadius: 18,
    padding: 18,
    boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
    display: 'flex', flexDirection: 'column', gap: 14,
  }}>
    {/* Header */}
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <span style={{
          width: 12, height: 12, borderRadius: '50%',
          background: 'var(--brand-secondary)',
          boxShadow: '0 0 0 5px color-mix(in srgb, var(--brand-secondary) 22%, transparent)',
        }} />
        <span style={{ fontSize: 19, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.015em' }}>
          Coastal Health · Proposal
        </span>
      </div>
      <span style={{
        display: 'inline-flex', alignItems: 'center', gap: 4,
        fontSize: 11, fontWeight: 800, letterSpacing: '0.10em',
        color: '#fff',
        background: 'linear-gradient(135deg, var(--brand-primary), var(--brand-accent))',
        padding: '5px 10px', borderRadius: 999,
        boxShadow: '0 2px 8px color-mix(in srgb, var(--brand-primary) 40%, transparent)',
      }}>✦ GENERATED</span>
    </div>

    {/* Sections */}
    <Section icon="◉" iconColor="var(--brand-primary-deep)" label="EXECUTIVE SUMMARY">
      <ParaBody>
        Your patient management workflow runs on disconnected tools and manual follow-ups. Referrals from GPs get lost, appointment reminders are inconsistent, and there\'s no visibility into where patients sit in their journey. We\'ll replace that with a single CRM that automates every touchpoint from enquiry to ongoing care.
      </ParaBody>
    </Section>

    <Section icon="◐" iconColor="var(--brand-primary)" label="IDENTIFIED NEEDS (3)">
      <NeedItem n="Map automation opportunities across 3 clinic locations." sol="AI Automation Audit Report — delivered before any build." />
      <NeedItem n="Single platform for patient enquiries, referrals, and follow-ups." sol="CRM Suite — one place for every contact, every pipeline." />
      <NeedItem n="System built, configured, and explained by a healthcare specialist." sol="Development & Training — full build + hands-on team walkthrough." />
    </Section>

    <Section icon="$" iconColor="var(--brand-secondary)" label="RECOMMENDED PRODUCTS">
      <PriceLine name="CRM Suite (per user · 22 users)"  price="$2,838" />
      <PriceLine name="AI Automation Audit"               price="$2,440" />
      <PriceLine name="Development & Training"            price="$4,200" />
      <PriceLine name="Total · Phase 1"                   price="$9,478" last />
    </Section>

    <Section icon="◆" iconColor="var(--brand-accent)" label="STRATEGY NOTES">
      <div style={{ fontSize: 11, color: colors.foreground, lineHeight: 1.5, fontWeight: 500 }}>
        • Dr Mitchell needs board sign-off above $50k — frame as phased.<br />
        • Open the demo by asking what happens to a GP referral today.<br />
        • Warm via Dr Patel referral — lean on implementation speed.
      </div>
    </Section>
  </div>
);

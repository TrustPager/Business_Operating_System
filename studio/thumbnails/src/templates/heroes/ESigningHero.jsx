// E-Signing hero — vertical stack of signed contract cards.
//
// Outcome framing: contracts that landed, were signed, stored. The top
// card is mid-signing (live), the rest are signed and sealed.

import React from 'react';
import { Avatar } from '../../profiles.jsx';
import { PRIMARY, PRIMARY_DEEP, SUCCESS, TEXT, TEXT_MUTED } from '../../brand.js';

const CONTRACTS = [
  {
    title: 'Master Services Agreement',
    client: 'Coastal Health Group',
    state: 'awaiting',
    signedBy: null,
    when: 'Sent 12 min ago',
    value: '$96k',
  },
  {
    title: 'Workflow Audit Contract',
    client: 'Wattle Creek Winery',
    state: 'signed',
    signedBy: 'Hugo Daniels',
    when: 'Signed in 47 sec',
    value: '$54k',
  },
  {
    title: 'Onboarding Agreement',
    client: 'Pinnacle Engineering',
    state: 'signed',
    signedBy: 'Theo Reilly',
    when: 'Signed yesterday',
    value: '$78k',
  },
  {
    title: 'Q3 Retainer Renewal',
    client: 'Southern Cross Legal',
    state: 'signed',
    signedBy: 'Anya Faulkner',
    when: 'Signed 2 days ago',
    value: '$120k',
  },
  {
    title: 'NDA — Discovery Phase',
    client: 'Eucalyptus Wealth',
    state: 'signed',
    signedBy: 'Camille Anders',
    when: 'Signed 3 days ago',
    value: null,
  },
  {
    title: 'Statement of Work',
    client: 'Reef & Co Logistics',
    state: 'signed',
    signedBy: 'Mateo Suarez',
    when: 'Signed last week',
    value: '$42k',
  },
];

const SignatureCurve = () => (
  <svg viewBox="0 0 80 22" width="80" height="22" style={{ display: 'block' }}>
    <path
      d="M2,16 C 8,4 14,18 22,10 C 30,2 36,18 44,8 C 50,2 58,16 70,6 L 78,10"
      fill="none" stroke={PRIMARY_DEEP} strokeWidth="2"
      strokeLinecap="round" strokeLinejoin="round"
    />
  </svg>
);

const ContractCard = ({ c }) => {
  const signed = c.state === 'signed';
  return (
    <div style={{
      background: '#fff',
      borderRadius: 12,
      padding: '14px 16px',
      border: '1px solid rgba(226,232,240,0.7)',
      display: 'flex', flexDirection: 'column', gap: 10,
      position: 'relative',
      overflow: 'hidden',
    }}>
      {/* "Signed" stamp diagonal — top right */}
      {signed && (
        <div style={{
          position: 'absolute',
          top: 10, right: -22,
          transform: 'rotate(12deg)',
          fontSize: 9, fontWeight: 800,
          color: SUCCESS,
          background: `${SUCCESS}29`,
          border: `1.5px solid ${SUCCESS}73`,
          padding: '3px 22px', borderRadius: 4,
          letterSpacing: '0.18em',
        }}>SIGNED</div>
      )}

      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{
          width: 30, height: 36, borderRadius: 4,
          background: signed ? `${SUCCESS}1a` : `${PRIMARY}1a`,
          border: signed ? `1px solid ${SUCCESS}4d` : `1px solid ${PRIMARY}4d`,
          display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0,
          gap: 2,
        }}>
          <div style={{ width: 16, height: 1.5, background: signed ? SUCCESS : PRIMARY, borderRadius: 1 }} />
          <div style={{ width: 14, height: 1.5, background: signed ? SUCCESS : PRIMARY, borderRadius: 1, opacity: 0.6 }} />
          <div style={{ width: 16, height: 1.5, background: signed ? SUCCESS : PRIMARY, borderRadius: 1, opacity: 0.6 }} />
        </div>
        <div style={{ flex: 1, minWidth: 0, paddingRight: signed ? 60 : 0 }}>
          <div style={{
            fontSize: 14, fontWeight: 800, color: TEXT,
            letterSpacing: '-0.01em', lineHeight: 1.2,
          }}>{c.title}</div>
          <div style={{
            fontSize: 11, fontWeight: 600, color: TEXT_MUTED,
            marginTop: 2,
          }}>{c.client}{c.value ? ` · ${c.value}` : ''}</div>
        </div>
      </div>

      {signed ? (
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <Avatar name={c.signedBy} size={26} />
          <SignatureCurve />
          <div style={{ flex: 1 }}>
            <div style={{
              fontSize: 11, fontWeight: 800, color: TEXT,
              letterSpacing: '-0.005em',
            }}>{c.signedBy}</div>
            <div style={{
              fontSize: 10, fontWeight: 600, color: TEXT_MUTED,
              marginTop: 1,
            }}>{c.when}</div>
          </div>
        </div>
      ) : (
        <div style={{
          display: 'inline-flex', alignItems: 'center', gap: 6,
          fontSize: 10, fontWeight: 800, letterSpacing: '0.10em',
          color: PRIMARY_DEEP,
          background: `${PRIMARY}29`,
          padding: '4px 9px', borderRadius: 999,
          alignSelf: 'flex-start',
        }}>● AWAITING SIGNATURE · {c.when}</div>
      )}
    </div>
  );
};

export const ESigningHero = () => (
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
          background: SUCCESS,
          boxShadow: `0 0 0 5px ${SUCCESS}38`,
        }} />
        <span style={{ fontSize: 19, fontWeight: 800, color: TEXT, letterSpacing: '-0.015em' }}>
          Signatures
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: PRIMARY,
        background: `${PRIMARY}24`,
        padding: '5px 10px', borderRadius: 999,
      }}>5 SIGNED · 1 OPEN</span>
    </div>

    {/* Contract stack */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      {CONTRACTS.map((c, i) => <ContractCard key={i} c={c} />)}
    </div>
  </div>
);

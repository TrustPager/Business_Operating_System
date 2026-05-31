// Proposals & Documents hero — a finished proposal as a single document
// rendered top-to-bottom. Cover header, pricing table, terms, signature
// block. The document silhouette is the whole identity here.
//
// Outcome framing: a polished, send-ready document. Not the editor.

import React from 'react';
import { colors } from '../../theme.js';

const DocLine = ({ w = '100%', dim = false }) => (
  <div style={{
    width: w, height: 6,
    background: dim ? 'rgba(148,163,184,0.20)' : 'rgba(148,163,184,0.35)',
    borderRadius: 3,
    marginBottom: 5,
  }} />
);

const Heading = ({ children, color = '#1ea5a5' }) => (
  <div style={{
    fontSize: 12, fontWeight: 800,
    color, letterSpacing: '-0.005em',
    marginBottom: 6, marginTop: 4,
  }}>{children}</div>
);

const PriceRow = ({ name, qty, total, last = false }) => (
  <div style={{
    display: 'flex', alignItems: 'center',
    padding: '7px 0',
    borderBottom: last ? 'none' : '1px solid rgba(226,232,240,0.6)',
  }}>
    <div style={{ flex: 1, minWidth: 0 }}>
      <div style={{ fontSize: 11, fontWeight: 700, color: colors.foreground, letterSpacing: '-0.005em' }}>{name}</div>
      <div style={{ fontSize: 9, fontWeight: 600, color: colors.mutedForeground, marginTop: 1 }}>{qty}</div>
    </div>
    <div style={{ fontSize: 12, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.015em' }}>{total}</div>
  </div>
);

const PaperPage = ({ children, label }) => (
  <div style={{
    background: '#fff',
    borderRadius: 8,
    border: '1px solid rgba(226,232,240,0.7)',
    boxShadow: '0 1px 2px rgba(15,17,23,0.04)',
    padding: 14,
    position: 'relative',
  }}>
    <span style={{
      position: 'absolute', top: 10, right: 10,
      fontSize: 8, fontWeight: 800, letterSpacing: '0.12em',
      color: colors.mutedForeground,
      background: 'rgba(248,250,252,0.9)',
      padding: '2px 6px', borderRadius: 3,
    }}>{label}</span>
    {children}
  </div>
);

const SignatureSquiggle = () => (
  <svg width="110" height="22" viewBox="0 0 110 22" style={{ display: 'block' }}>
    <path
      d="M2,16 C 10,4 18,18 28,10 C 38,2 46,18 56,8 C 66,2 74,16 84,12 C 92,8 100,14 108,10"
      fill="none" stroke="#1ea5a5" strokeWidth="2"
      strokeLinecap="round" strokeLinejoin="round"
    />
  </svg>
);

export const ProposalsHero = () => (
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
          background: '#2db87d',
          boxShadow: '0 0 0 5px rgba(45,184,125,0.22)',
        }} />
        <span style={{ fontSize: 19, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.015em' }}>
          Business Proposal
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.primary,
        background: 'rgba(41,198,198,0.14)',
        padding: '5px 10px', borderRadius: 999,
      }}>READY · 1 OF 1</span>
    </div>

    {/* Cover page */}
    <PaperPage label="PAGE 1">
      <div style={{
        background: 'linear-gradient(135deg, rgba(41,198,198,0.10), rgba(71,163,217,0.10))',
        borderRadius: 8,
        padding: '14px 14px',
        marginBottom: 10,
      }}>
        <div style={{ fontSize: 11, fontWeight: 800, letterSpacing: '0.12em', color: '#1ea5a5', marginBottom: 4 }}>
          PROPOSAL · Q3 2026
        </div>
        <div style={{ fontSize: 18, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.02em', lineHeight: 1.1 }}>
          Coastal Health Group
        </div>
        <div style={{ fontSize: 11, fontWeight: 600, color: colors.mutedForeground, marginTop: 4 }}>
          Workflow Audit + CRM Build + Training
        </div>
      </div>
      <Heading>Executive Summary</Heading>
      <DocLine w="100%" />
      <DocLine w="96%" />
      <DocLine w="88%" />
      <DocLine w="62%" dim />
    </PaperPage>

    {/* Pricing page */}
    <PaperPage label="PAGE 2">
      <Heading color="#2db87d">Investment Summary</Heading>
      <PriceRow name="AI Automation Audit Report"    qty="One-time"        total="$2,440" />
      <PriceRow name="CRM Suite — per user license"   qty="22 users × Q3"  total="$2,838" />
      <PriceRow name="Development & Training"         qty="Phase 1"         total="$4,200" />
      <PriceRow name="Total · Phase 1"                qty="GST inclusive"   total="$9,478" last />
    </PaperPage>

    {/* Terms page */}
    <PaperPage label="PAGE 3">
      <Heading color="#47a3d9">Terms & Conditions</Heading>
      <DocLine w="100%" />
      <DocLine w="92%" />
      <DocLine w="88%" />
      <DocLine w="95%" />
      <DocLine w="70%" dim />
    </PaperPage>

    {/* Signature page */}
    <PaperPage label="PAGE 4">
      <Heading>Signatures</Heading>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginTop: 6 }}>
        <div>
          <SignatureSquiggle />
          <div style={{ borderTop: '1px solid rgba(148,163,184,0.30)', marginTop: 2, paddingTop: 4 }}>
            <div style={{ fontSize: 11, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.005em' }}>Dr Sarah Mitchell</div>
            <div style={{ fontSize: 9, fontWeight: 600, color: colors.mutedForeground, marginTop: 1 }}>CFO · Coastal Health Group</div>
          </div>
        </div>
      </div>
    </PaperPage>
  </div>
);

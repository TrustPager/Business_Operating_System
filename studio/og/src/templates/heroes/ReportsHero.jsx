// Reports hero — vertical stack of chart cards.
//
// Master rule (see ../YouTubeThumbnail.jsx HERO UI SELECTION): thin, tall,
// single vertical stack, bleeds off the bottom. No side-by-side donut +
// legend or 3-across stat row — each chart card is a row.
//
// Reference: ../../../../src/scenes/reporting/
// Outcome framing: a portrait performance dashboard you scroll through.

import React from 'react';
import { colors } from '../../theme.js';

const TREND_POINTS = [22, 28, 26, 34, 32, 40, 44, 42, 52, 58, 56, 64, 70, 76];
const BAR_DATA = [
  { label: 'New Enq.',   value: 92, color: 'var(--brand-light)' },
  { label: 'Discovery',  value: 74, color: 'var(--brand-primary)' },
  { label: 'Proposal',   value: 58, color: 'var(--brand-accent)' },
  { label: 'Won',        value: 47, color: 'var(--brand-secondary)' },
];
const DONUT_SLICES = [
  { label: 'Website',  value: 38, color: 'var(--brand-primary)' },
  { label: 'Referral', value: 28, color: 'var(--brand-accent)' },
  { label: 'LinkedIn', value: 18, color: 'var(--brand-light)' },
  { label: 'Inbound',  value: 16, color: 'var(--brand-secondary)' },
];

const Card = ({ children, style = {} }) => (
  <div style={{
    background: '#fff',
    borderRadius: 12,
    padding: 16,
    border: '1px solid rgba(226,232,240,0.7)',
    ...style,
  }}>{children}</div>
);

const StatHero = () => (
  <Card style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
    <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.mutedForeground,
      }}>REVENUE · Q3</span>
      <span style={{
        fontSize: 38, fontWeight: 800, color: colors.foreground,
        letterSpacing: '-0.03em', lineHeight: 1,
      }}>$312k</span>
    </div>
    <div style={{
      fontSize: 14, fontWeight: 800,
      color: 'var(--brand-secondary)',
      background: 'color-mix(in srgb, var(--brand-secondary) 15%, transparent)',
      padding: '8px 14px', borderRadius: 999,
      display: 'flex', alignItems: 'center', gap: 4,
    }}>↗ +18%</div>
  </Card>
);

const Donut = ({ slices, size = 86 }) => {
  const total = slices.reduce((a, s) => a + s.value, 0);
  let acc = 0;
  const stops = slices.map(s => {
    const start = (acc / total) * 360;
    acc += s.value;
    const end = (acc / total) * 360;
    return `${s.color} ${start}deg ${end}deg`;
  }).join(', ');
  return (
    <div style={{
      width: size, height: size,
      borderRadius: '50%',
      background: `conic-gradient(${stops})`,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      flexShrink: 0,
    }}>
      <div style={{
        width: size * 0.62, height: size * 0.62,
        borderRadius: '50%',
        background: '#fff',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexDirection: 'column',
        boxShadow: '0 1px 2px rgba(15,17,23,0.05)',
      }}>
        <div style={{
          fontSize: 17, fontWeight: 800, color: colors.foreground,
          letterSpacing: '-0.02em', lineHeight: 1,
        }}>{total}</div>
        <div style={{
          fontSize: 8, fontWeight: 800, color: colors.mutedForeground,
          letterSpacing: '0.10em', marginTop: 2,
        }}>LEADS</div>
      </div>
    </div>
  );
};

const DonutCard = () => (
  <Card>
    <div style={{ fontSize: 13, fontWeight: 800, letterSpacing: '0.10em', color: colors.mutedForeground, marginBottom: 14 }}>
      LEADS BY SOURCE
    </div>
    <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
      <Donut slices={DONUT_SLICES} />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 8 }}>
        {DONUT_SLICES.map((s, i) => {
          const total = DONUT_SLICES.reduce((a, x) => a + x.value, 0);
          return (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13 }}>
              <span style={{ width: 10, height: 10, borderRadius: 3, background: s.color, flexShrink: 0 }} />
              <span style={{ color: colors.foreground, fontWeight: 700, flex: 1, letterSpacing: '-0.01em' }}>{s.label}</span>
              <span style={{ color: colors.foreground, fontWeight: 800, letterSpacing: '-0.01em' }}>
                {Math.round((s.value / total) * 100)}%
              </span>
            </div>
          );
        })}
      </div>
    </div>
  </Card>
);

const TrendChart = ({ points }) => {
  const max = Math.max(...points);
  const w = 100;
  const h = 40;
  const step = w / (points.length - 1);
  const pts = points.map((p, i) => `${i * step},${h - (p / max) * (h - 4) - 2}`).join(' ');
  const area = `0,${h} ${pts} ${w},${h}`;
  return (
    <svg viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" style={{ width: '100%', height: 140, display: 'block' }}>
      <defs>
        <linearGradient id="trend-area-tall" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor="var(--brand-primary)" stopOpacity="0.40" />
          <stop offset="100%" stopColor="var(--brand-primary)" stopOpacity="0" />
        </linearGradient>
      </defs>
      <polygon points={area} fill="url(#trend-area-tall)" />
      <polyline points={pts} fill="none" stroke="var(--brand-primary)" strokeWidth="1.3" strokeLinejoin="round" strokeLinecap="round" />
      {points.map((p, i) => (
        <circle key={i} cx={i * step} cy={h - (p / max) * (h - 4) - 2} r="0.9" fill="var(--brand-primary)" />
      ))}
    </svg>
  );
};

const TOP_PERFORMERS = [
  { name: 'Simon K.',  avatar: 'SK', color: 'var(--brand-primary)', value: '$98k', bar: 100 },
  { name: 'Jordan P.', avatar: 'JP', color: 'var(--brand-accent)', value: '$72k', bar: 73  },
  { name: 'Mira S.',   avatar: 'MS', color: 'var(--brand-secondary)', value: '$58k', bar: 59  },
  { name: 'Hugo D.',   avatar: 'HD', color: 'var(--brand-light)', value: '$41k', bar: 42  },
];

const TopPerformersCard = () => (
  <Card>
    <div style={{ fontSize: 13, fontWeight: 800, letterSpacing: '0.10em', color: colors.mutedForeground, marginBottom: 14 }}>
      TOP PERFORMERS · Q3
    </div>
    <div style={{ display: 'flex', flexDirection: 'column', gap: 11 }}>
      {TOP_PERFORMERS.map((p, i) => (
        <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{
            width: 28, height: 28, borderRadius: '50%',
            background: p.color,
            color: '#fff', fontSize: 11, fontWeight: 800,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexShrink: 0,
          }}>{p.avatar}</div>
          <span style={{
            fontSize: 13, fontWeight: 700, color: colors.foreground,
            letterSpacing: '-0.01em',
            width: 80, flexShrink: 0,
          }}>{p.name}</span>
          <div style={{ flex: 1, height: 10, background: 'rgba(148,163,184,0.14)', borderRadius: 5, overflow: 'hidden' }}>
            <div style={{
              width: `${p.bar}%`,
              height: '100%',
              background: p.color,
              borderRadius: 5,
            }} />
          </div>
          <span style={{
            fontSize: 13, fontWeight: 800, color: colors.foreground,
            letterSpacing: '-0.015em',
            width: 40, textAlign: 'right',
          }}>{p.value}</span>
        </div>
      ))}
    </div>
  </Card>
);

const TrendCard = () => (
  <Card>
    <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 8 }}>
      <span style={{ fontSize: 13, fontWeight: 800, letterSpacing: '0.10em', color: colors.mutedForeground }}>
        WEEKLY WON DEALS
      </span>
      <span style={{ fontSize: 14, fontWeight: 800, color: 'var(--brand-secondary)' }}>+187% YoY</span>
    </div>
    <TrendChart points={TREND_POINTS} />
  </Card>
);

const BarCard = () => {
  const max = Math.max(...BAR_DATA.map(b => b.value));
  return (
    <Card>
      <div style={{ fontSize: 13, fontWeight: 800, letterSpacing: '0.10em', color: colors.mutedForeground, marginBottom: 14 }}>
        FUNNEL DROP-OFF
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {BAR_DATA.map((b, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <span style={{
              fontSize: 12, fontWeight: 700, color: colors.foreground,
              letterSpacing: '-0.005em',
              width: 78, flexShrink: 0,
            }}>{b.label}</span>
            <div style={{ flex: 1, height: 14, background: 'rgba(148,163,184,0.14)', borderRadius: 7, overflow: 'hidden' }}>
              <div style={{
                width: `${(b.value / max) * 100}%`,
                height: '100%',
                background: b.color,
                borderRadius: 7,
              }} />
            </div>
            <span style={{
              fontSize: 14, fontWeight: 800, color: colors.foreground,
              letterSpacing: '-0.015em',
              width: 32, textAlign: 'right',
            }}>{b.value}</span>
          </div>
        ))}
      </div>
    </Card>
  );
};

export const ReportsHero = () => (
  <div style={{
    background: '#fff',
    borderRadius: 18,
    padding: 18,
    boxShadow: '0 1px 2px rgba(15,17,23,0.06), 0 6px 14px rgba(15,17,23,0.06), 0 26px 52px rgba(15,17,23,0.12), 0 0 0 1px rgba(15,17,23,0.05)',
    display: 'flex', flexDirection: 'column', gap: 14,
  }}>
    {/* Header — matches SMS/Pipeline pattern */}
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <span style={{
          width: 12, height: 12, borderRadius: '50%',
          background: 'var(--brand-secondary)',
          boxShadow: '0 0 0 5px color-mix(in srgb, var(--brand-secondary) 22%, transparent)',
        }} />
        <span style={{ fontSize: 19, fontWeight: 800, color: colors.foreground, letterSpacing: '-0.015em' }}>
          Performance Dashboard
        </span>
      </div>
      <span style={{
        fontSize: 11, fontWeight: 800, letterSpacing: '0.12em',
        color: colors.primary,
        background: 'color-mix(in srgb, var(--brand-primary) 14%, transparent)',
        padding: '5px 10px', borderRadius: 999,
      }}>Q3 · LIVE</span>
    </div>

    {/* Panel stack — bleeds off bottom */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <StatHero />
      <DonutCard />
      <TrendCard />
      <BarCard />
      <TopPerformersCard />
    </div>
  </div>
);

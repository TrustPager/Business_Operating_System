// TrustPager YouTube Thumbnail Studio
// Browser-based editor for previewing tutorial-video thumbnails.
// Run: npm run dev → opens at http://localhost:3210
//
// Left sidebar: design gallery + JSON data editor
// Main area: live preview at actual pixel dimensions
// Top bar: zoom + a click-to-copy command chip for the canonical export
//
// EXPORTS are NOT done in-browser. The canonical export path is:
//
//   npm run shoot <design-key>
//
// That uses puppeteer + real Chrome rendering, which correctly handles every
// CSS feature in the template (background-clip:text, backdrop-filter, etc.).
// JavaScript-based DOM rasterisation libraries (html2canvas, dom-to-image,
// etc.) have CSS feature gaps that misrender the gradient accent word and
// other modern effects.

import React, { useState, useCallback } from 'react';
import { resolveTemplate } from './templates/index.js';
import sampleData from './data/samples.json';

const ZOOM_LEVELS = [0.25, 0.33, 0.5, 0.67, 0.75, 1];

// TrustPager brand tokens — light theme, sourced from
// MARKETING/BRAND_ASSETS/TrustPager/brand.json. Keep in sync if brand shifts.
const PRIMARY      = '#29c6c6';                 // brand teal
const PRIMARY_DEEP = '#1ea5a5';
const ACCENT       = '#47a3d9';                 // brand blue
const SUCCESS      = '#2db87d';                 // brand green
const HERO_GRAD    = 'linear-gradient(135deg, #29c6c6 0%, #47a3d9 100%)';

const BG_CANVAS    = '#f1f5f9';                 // canvas wash behind the live preview
const BG_PAGE      = '#f8fafc';                 // page background
const PANEL        = '#ffffff';                 // cards / sidebar / top bar
const BORDER       = '#e2e8f0';                 // light border
const TEXT         = '#020817';                 // foreground
const TEXT_MUTED   = '#647086';                 // muted foreground

const FONT_BODY = '"Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, system-ui, sans-serif';
const FONT_MONO = '"JetBrains Mono", "Fira Code", monospace';

// Click-to-copy command chip. Renders `$ <command>  COPY` and flashes
// `COPIED` for ~1.8s when clicked. `accent` controls the eyebrow tone.
const CommandChip = ({ label, command, tooltip, active, accent, onCopy }) => (
  <button
    onClick={onCopy}
    title={tooltip}
    style={{
      background: active ? 'rgba(45,184,125,0.10)' : PANEL,
      border: `1px solid ${active ? 'rgba(45,184,125,0.40)' : BORDER}`,
      borderRadius: 8,
      padding: '6px 12px',
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      cursor: 'pointer',
      fontFamily: FONT_MONO,
      fontSize: 12,
      color: active ? SUCCESS : TEXT,
      transition: 'all 0.15s',
      boxShadow: '0 1px 2px rgba(0,0,0,0.03)',
    }}
  >
    <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: accent, fontFamily: FONT_BODY }}>
      {label.toUpperCase()}
    </span>
    <span style={{ fontSize: 11, color: TEXT_MUTED, fontFamily: 'inherit' }}>$</span>
    <span>{command}</span>
    <span style={{ fontSize: 11, color: active ? SUCCESS : TEXT_MUTED, fontFamily: FONT_BODY, fontWeight: 600 }}>
      {active ? 'COPIED' : 'COPY'}
    </span>
  </button>
);

export const App = () => {
  const samples = Object.entries(sampleData);
  const [selectedKey, setSelectedKey] = useState(samples[0]?.[0] || '');
  const [zoom, setZoom] = useState(0.5);
  const [copiedAt, setCopiedAt] = useState(0);

  const currentSample = sampleData[selectedKey];
  const resolved = currentSample ? resolveTemplate(currentSample.template) : null;
  const mergedData = currentSample ? currentSample.data : {};

  const selectDesign = useCallback((key) => {
    setSelectedKey(key);
  }, []);

  const [copiedKind, setCopiedKind] = useState(null);
  const shootCommand = `npm run shoot ${selectedKey}`;
  const publishCommand = `npm run publish ${selectedKey}`;
  const copy = async (kind, text) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedAt(Date.now());
      setCopiedKind(kind);
    } catch (err) {
      console.error('Clipboard write failed:', err);
    }
  };
  const recentlyCopied = Date.now() - copiedAt < 1800;

  return (
    <div style={{ display: 'flex', height: '100vh', background: BG_PAGE, fontFamily: FONT_BODY }}>

      {/* === LEFT SIDEBAR === */}
      <div style={{
        width: 360,
        borderRight: `1px solid ${BORDER}`,
        background: PANEL,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
      }}>
        {/* Branded header — TrustPager logo + product label */}
        <div style={{
          padding: '20px 22px',
          borderBottom: `1px solid ${BORDER}`,
          display: 'flex',
          alignItems: 'center',
          gap: 12,
        }}>
          <img
            src="/trustpager-logo.png"
            alt="TrustPager"
            style={{ height: 28, width: 'auto', display: 'block' }}
          />
          <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <div style={{ fontSize: 14, fontWeight: 700, color: TEXT, letterSpacing: '-0.01em' }}>
              Thumbnail Studio
            </div>
            <div style={{ fontSize: 11, color: TEXT_MUTED, fontWeight: 500 }}>
              YouTube · 1280 × 720
            </div>
          </div>
        </div>

        <div style={{ padding: 14, flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: TEXT_MUTED, textTransform: 'uppercase', marginBottom: 10, letterSpacing: '0.08em', flexShrink: 0 }}>
            Designs · {samples.length}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4, overflowY: 'auto', minHeight: 0, paddingRight: 4 }}>
            {samples.map(([key, sample]) => {
              const meta = resolveTemplate(sample.template)?.meta;
              const composition = sample.composition || sample.data?.composition || null;
              const selected = key === selectedKey;
              return (
                <button
                  key={key}
                  onClick={() => selectDesign(key)}
                  style={{
                    background: selected ? 'rgba(41,198,198,0.10)' : 'transparent',
                    border: selected ? `1px solid ${PRIMARY}` : `1px solid transparent`,
                    borderRadius: 10,
                    padding: '10px 14px',
                    textAlign: 'left',
                    cursor: 'pointer',
                    transition: 'all 0.15s',
                  }}
                >
                  <div style={{ fontSize: 13, fontWeight: 600, color: selected ? PRIMARY_DEEP : TEXT, letterSpacing: '-0.005em' }}>{key}</div>
                  <div style={{ fontSize: 11, color: TEXT_MUTED, marginTop: 2 }}>
                    {meta?.name} · {meta?.size.width}×{meta?.size.height}
                  </div>
                  <div style={{ fontSize: 10, marginTop: 4, fontFamily: FONT_MONO, color: composition ? SUCCESS : '#d97757' }}>
                    {composition ? `→ ${composition}` : '⚠ no composition linked'}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

      </div>

      {/* === MAIN CANVAS AREA === */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>

        <div style={{
          height: 52,
          borderBottom: `1px solid ${BORDER}`,
          background: PANEL,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 22px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span style={{ fontSize: 12, color: TEXT_MUTED, fontWeight: 600, letterSpacing: '0.02em' }}>Zoom</span>
            {ZOOM_LEVELS.map((z) => {
              const selected = z === zoom;
              return (
                <button
                  key={z}
                  onClick={() => setZoom(z)}
                  style={{
                    background: selected ? 'rgba(41,198,198,0.10)' : 'transparent',
                    border: selected ? `1px solid ${PRIMARY}` : `1px solid ${BORDER}`,
                    borderRadius: 6,
                    padding: '4px 10px',
                    fontSize: 12,
                    fontWeight: selected ? 600 : 500,
                    color: selected ? PRIMARY_DEEP : TEXT_MUTED,
                    cursor: 'pointer',
                    fontFamily: FONT_BODY,
                  }}
                >
                  {Math.round(z * 100)}%
                </button>
              );
            })}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <span style={{ fontSize: 12, color: TEXT_MUTED, fontFamily: FONT_MONO }}>
              {resolved ? `${resolved.meta.size.width} × ${resolved.meta.size.height}px` : ''}
            </span>
            {resolved && (
              <>
                <CommandChip
                  label="shoot"
                  command={shootCommand}
                  tooltip="Click to copy. Paste in terminal to render the PNG locally and open it (iteration)."
                  active={recentlyCopied && copiedKind === 'shoot'}
                  accent={TEXT_MUTED}
                  onCopy={() => copy('shoot', shootCommand)}
                />
                <CommandChip
                  label="publish"
                  command={publishCommand}
                  tooltip="Click to copy. Paste in terminal to render + upload to your TrustPager > Files > Tutorial Thumbnails folder (finalize)."
                  active={recentlyCopied && copiedKind === 'publish'}
                  accent={PRIMARY}
                  onCopy={() => copy('publish', publishCommand)}
                />
              </>
            )}
          </div>
        </div>

        <div style={{
          flex: 1,
          overflow: 'auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: 40,
          background: BG_CANVAS,
          backgroundImage: 'radial-gradient(circle at 20% 0%, rgba(41,198,198,0.06), transparent 40%), radial-gradient(circle at 80% 100%, rgba(71,163,217,0.06), transparent 40%)',
        }}>
          {resolved ? (
            <div
              style={{
                transform: `scale(${zoom})`,
                transformOrigin: 'center center',
                boxShadow: '0 0 0 1px rgba(0,0,0,0.06), 0 30px 60px -20px rgba(0,0,0,0.16), 0 8px 20px -6px rgba(0,0,0,0.08)',
                borderRadius: 6,
                overflow: 'hidden',
                background: '#fff',
              }}
            >
              <resolved.Component data={mergedData} />
            </div>
          ) : (
            <div style={{ color: TEXT_MUTED, fontSize: 15, fontWeight: 500 }}>
              Select a design from the sidebar
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

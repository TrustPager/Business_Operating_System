// BOS Nurture CTA Studio
// Browser-based editor for previewing nurture-email CTA designs.
// Run: npm run dev → opens at http://localhost:3213
//
// Sidebar: design gallery grouped by template + JSON-driven samples.
// Main area: live preview at native 1200×460 dimensions.
// Top bar: zoom + click-to-copy command chips for shoot/publish.
//
// All brand tokens flow from BOS/brand/brand.json via ./brand.js. Edit
// brand.json (or run /brand-my-workspace) to retheme every studio.

import React, { useState, useCallback } from 'react';
import { resolveTemplate } from './templates/index.js';
import sampleData from './data/samples.json';
import {
  PRIMARY, PRIMARY_DEEP, ACCENT, SUCCESS,
  PANEL, BORDER, TEXT, TEXT_MUTED, PAGE_BG, CANVAS_BG,
  FONT_BODY, FONT_MONO, LOGO_URL, NAME,
} from './brand.js';

const ZOOM_LEVELS = [0.25, 0.33, 0.5, 0.67, 0.75, 1];

const BG_PAGE   = PAGE_BG;
const BG_CANVAS = CANVAS_BG;

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
  const [copiedKind, setCopiedKind] = useState(null);
  const [collapsedFolders, setCollapsedFolders] = useState({});

  const currentSample = sampleData[selectedKey];
  const resolved = currentSample ? resolveTemplate(currentSample.template) : null;
  const mergedData = currentSample ? currentSample.data : {};

  const selectDesign = useCallback((key) => setSelectedKey(key), []);
  const toggleFolder = useCallback((id) => {
    setCollapsedFolders((c) => ({ ...c, [id]: !c[id] }));
  }, []);

  const groupedSamples = (() => {
    const groups = new Map();
    samples.forEach(([key, sample]) => {
      const tplId = sample.template;
      if (!groups.has(tplId)) {
        groups.set(tplId, {
          templateId: tplId,
          meta: resolveTemplate(tplId)?.meta,
          items: [],
        });
      }
      groups.get(tplId).items.push([key, sample]);
    });
    return Array.from(groups.values());
  })();

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
        <div style={{
          padding: '20px 22px',
          borderBottom: `1px solid ${BORDER}`,
          display: 'flex',
          alignItems: 'center',
          gap: 12,
        }}>
          <img
            src={LOGO_URL}
            alt={NAME}
            style={{ height: 28, width: 'auto', display: 'block' }}
          />
          <div style={{ fontSize: 14, fontWeight: 700, color: TEXT, letterSpacing: '-0.01em' }}>
            Nurture CTA Studio
          </div>
        </div>

        <div style={{ padding: 14, flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: TEXT_MUTED, textTransform: 'uppercase', marginBottom: 10, letterSpacing: '0.08em', flexShrink: 0 }}>
            Designs · {samples.length}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, overflowY: 'auto', minHeight: 0, paddingRight: 4 }}>
            {groupedSamples.map(({ templateId, meta, items }) => {
              const isCollapsed = !!collapsedFolders[templateId];
              const sizeLabel = meta ? `${meta.size.width}×${meta.size.height}` : '';
              return (
                <div key={templateId} style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                  <button
                    onClick={() => toggleFolder(templateId)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 8,
                      background: 'transparent',
                      border: 'none',
                      padding: '6px 6px',
                      cursor: 'pointer',
                      textAlign: 'left',
                      color: TEXT,
                      fontFamily: FONT_BODY,
                    }}
                  >
                    <span style={{ display: 'inline-block', width: 10, fontSize: 9, color: TEXT_MUTED, transition: 'transform 0.15s', transform: isCollapsed ? 'rotate(-90deg)' : 'rotate(0deg)' }}>▾</span>
                    <span style={{ fontSize: 12, fontWeight: 700, letterSpacing: '-0.005em' }}>
                      {meta?.name || templateId}
                    </span>
                    <span style={{ fontSize: 11, color: TEXT_MUTED, fontWeight: 500 }}>
                      · {items.length}
                    </span>
                    {sizeLabel && (
                      <span style={{ marginLeft: 'auto', fontSize: 10, color: TEXT_MUTED, fontFamily: FONT_MONO }}>
                        {sizeLabel}
                      </span>
                    )}
                  </button>
                  {!isCollapsed && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 4, paddingLeft: 6 }}>
                      {items.map(([key, sample]) => {
                        const selected = key === selectedKey;
                        return (
                          <button
                            key={key}
                            onClick={() => selectDesign(key)}
                            style={{
                              background: selected ? `${PRIMARY}1a` : 'transparent',
                              border: selected ? `1px solid ${PRIMARY}` : `1px solid transparent`,
                              borderRadius: 10,
                              padding: '10px 14px',
                              textAlign: 'left',
                              cursor: 'pointer',
                              transition: 'all 0.15s',
                            }}
                          >
                            <div style={{ fontSize: 13, fontWeight: 600, color: selected ? PRIMARY_DEEP : TEXT, letterSpacing: '-0.005em' }}>{key}</div>
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>
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
                    background: selected ? `${PRIMARY}1a` : 'transparent',
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
                  tooltip="Click to copy. Render the PNG locally."
                  active={recentlyCopied && copiedKind === 'shoot'}
                  accent={TEXT_MUTED}
                  onCopy={() => copy('shoot', shootCommand)}
                />
                <CommandChip
                  label="publish"
                  command={publishCommand}
                  tooltip="Click to copy. Render + upload to your TrustPager workspace's Files folder."
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
          backgroundImage: `radial-gradient(circle at 20% 0%, ${PRIMARY}10, transparent 40%), radial-gradient(circle at 80% 100%, ${ACCENT}10, transparent 40%)`,
        }}>
          {resolved ? (
            <div
              style={{
                transform: `scale(${zoom})`,
                transformOrigin: 'center center',
                boxShadow: '0 0 0 1px rgba(0,0,0,0.06), 0 30px 60px -20px rgba(0,0,0,0.16), 0 8px 20px -6px rgba(0,0,0,0.08)',
                borderRadius: 6,
                overflow: 'hidden',
                background: PANEL,
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

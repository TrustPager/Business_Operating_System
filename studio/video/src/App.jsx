// BOS Video Studio
// Browser-based preview for the text-on-screen video template.
// Run: npm run dev -> opens at http://localhost:3218
//
// Sidebar: the committed data/*.script.json fixtures.
// Main area: a live frame preview + a scrubber. The scrubber sets ?frame=N in
// the URL (same interface scripts/render.js drives headlessly), then reloads the
// preview at that frame — so what you scrub is exactly what the renderer captures.
// Top bar: the beat-role, the timecode, and a click-to-copy shoot command.
//
// All brand tokens flow from BOS/brand/brand.json via ./brand.js. Edit
// brand.json (or run /brand-my-workspace) to retheme every studio.

import React, { useState, useCallback, useRef, useLayoutEffect, useMemo, useEffect } from 'react';
import { resolveTemplate } from './templates/index.js';
import { sizeForAspect } from './templates/VideoBeats.jsx';
import { buildTimeline, beatAtFrame, totalFrames, FPS } from './timing.js';
import {
  PRIMARY, PRIMARY_DEEP, ACCENT, SUCCESS,
  PANEL, BORDER, TEXT, TEXT_MUTED, PAGE_BG, CANVAS_BG,
  FONT_BODY, FONT_MONO, LOGO_URL, NAME,
} from './brand.js';

// Load every committed fixture script under data/. eager: parse at build time.
const scriptModules = import.meta.glob('../data/*.script.json', { eager: true });
const SCRIPTS = Object.fromEntries(
  Object.entries(scriptModules).map(([path, mod]) => {
    const script = mod.default || mod;
    const slug = script.slug || path.split('/').pop().replace('.script.json', '');
    return [slug, script];
  })
);

const PREVIEW_PAD = 40;

// Read ?frame=N from the URL so the browser preview and the headless renderer
// share the exact frame semantics.
function frameFromUrl() {
  const n = new URLSearchParams(window.location.search).get('frame');
  const parsed = n == null ? 0 : parseInt(n, 10);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : 0;
}

// render.js also passes ?slug=<slug> so the headless capture targets the right
// script. Fall back to the first fixture when absent (interactive browsing).
function slugFromUrl(available) {
  const s = new URLSearchParams(window.location.search).get('slug');
  return s && available.includes(s) ? s : (available[0] || '');
}

function fmtTime(seconds) {
  const s = Math.max(0, seconds);
  const m = Math.floor(s / 60);
  const rem = (s % 60);
  return `${m}:${rem.toFixed(1).padStart(4, '0')}`;
}

export const App = () => {
  const slugs = Object.keys(SCRIPTS);
  const [selectedSlug, setSelectedSlug] = useState(slugFromUrl(slugs));
  // `view` bundles the frame number with a monotonic request id, so even a
  // REPEATED frame value produces a distinct state object and forces a
  // re-render + a fresh paint barrier (see the barrier design note below). The
  // request id is tracked in a ref (synchronous) so __setFrame can RETURN the id
  // it just assigned; setView only schedules the render.
  const reqRef = useRef(0);
  const [view, setView] = useState({ n: frameFromUrl(), req: 0 });
  const frame = Number.isFinite(view.n) ? view.n : 0;
  const setFrame = useCallback((n) => {
    const clamped = Number.isFinite(n) ? Math.max(0, Math.floor(n)) : 0;
    const req = ++reqRef.current;
    setView({ n: clamped, req });
    return req;
  }, []);
  const [copiedAt, setCopiedAt] = useState(0);
  const [containerSize, setContainerSize] = useState({ w: 0, h: 0 });
  const previewRef = useRef(null);

  const script = SCRIPTS[selectedSlug];
  const resolved = resolveTemplate('video-beats');
  const size = script ? sizeForAspect(script?.meta?.aspect) : { width: 1920, height: 1080 };

  const timeline = useMemo(() => (script ? buildTimeline(script, FPS) : []), [script]);
  const frameCount = useMemo(() => (script ? totalFrames(script, FPS) : 0), [script]);
  const activeBeat = beatAtFrame(timeline, frame);

  // Keep ?frame in the URL in step with the scrubber (deep-link + render parity).
  useEffect(() => {
    const url = new URL(window.location.href);
    url.searchParams.set('frame', String(frame));
    window.history.replaceState({}, '', url);
  }, [frame]);

  // Headless render hook. scripts/render.js navigates ONCE, then drives frames
  // by calling window.__setFrame(n) per step (far faster than a page reload per
  // frame). Determinism is preserved: each frame is set explicitly and the
  // renderer waits for that frame to PAINT before screenshotting, never plays in
  // realtime. The ?frame= URL path remains the documented interface for
  // deep-linking / manual inspection; this is the same interface exposed as a
  // function for the capture loop.
  //
  // Barrier design: setFrame bumps a monotonic request id (reqRef) and stores it
  // in `view` alongside the frame number, then RETURNS that id. The layout effect
  // below (keyed on `view`) runs the instant React commits the DOM for that view
  // and writes window.__renderedReq = view.req. The renderer waits for
  // __renderedReq === the id __setFrame returned. Using a request id (not the
  // frame value) makes it robust even when a frame value repeats or the very
  // first requested frame equals the initial state.
  useEffect(() => {
    window.__renderedReq = -1;
    // Returns the request id it assigned; the renderer waits for
    // window.__renderedReq to reach that id.
    window.__setFrame = (n) => setFrame(n);
    window.__selectSlug = (slug) => {
      if (SCRIPTS[slug]) { setSelectedSlug(slug); }
    };
    return () => { delete window.__setFrame; delete window.__selectSlug; };
  }, [setFrame]);

  // Publish the request id SYNCHRONOUSLY once the DOM has committed for this
  // view. useLayoutEffect fires right after React mutates the DOM and before the
  // browser paints, so window.__renderedReq flips the instant the new frame's
  // markup is in the tree. Puppeteer's screenshot forces a fresh paint of that
  // committed DOM, so a static text frame captures correctly without waiting on
  // requestAnimationFrame (rAF is throttled in a headless/background tab, which
  // made the render crawl). Keyed on view.req so it re-runs for EVERY __setFrame
  // call, even one that repeats the frame number. Deterministic: one commit, one
  // published id, one capture.
  useLayoutEffect(() => {
    window.__renderedReq = view.req;
  }, [view]);

  // Clamp the frame when the selected script changes length.
  useEffect(() => {
    setFrame((f) => Math.min(f, Math.max(0, frameCount - 1)));
  }, [frameCount]);

  useLayoutEffect(() => {
    const el = previewRef.current;
    if (!el) return;
    const measure = () => setContainerSize({ w: el.clientWidth, h: el.clientHeight });
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const fitScale = useMemo(() => {
    if (!size || !containerSize.w || !containerSize.h) return 0.4;
    const availW = containerSize.w - PREVIEW_PAD * 2;
    const availH = containerSize.h - PREVIEW_PAD * 2;
    return Math.min(availW / size.width, availH / size.height, 1);
  }, [size, containerSize]);

  const scale = fitScale;
  const shootCommand = `npm run shoot ${selectedSlug}`;
  const copy = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedAt(Date.now());
    } catch (err) {
      console.error('Clipboard write failed:', err);
    }
  };
  const recentlyCopied = Date.now() - copiedAt < 1800;

  const Comp = resolved?.Component;

  return (
    <div style={{ display: 'flex', height: '100vh', background: PAGE_BG, fontFamily: FONT_BODY }}>

      {/* === LEFT SIDEBAR === */}
      <div style={{
        width: 320, borderRight: `1px solid ${BORDER}`, background: PANEL,
        display: 'flex', flexDirection: 'column', overflow: 'hidden',
      }}>
        <div style={{
          padding: '20px 22px', borderBottom: `1px solid ${BORDER}`,
          display: 'flex', alignItems: 'center', gap: 12,
        }}>
          <img src={LOGO_URL} alt={NAME} style={{ height: 28, width: 'auto', display: 'block' }} />
          <div style={{ fontSize: 14, fontWeight: 700, color: TEXT, letterSpacing: '-0.01em' }}>
            Video Studio
          </div>
        </div>

        <div style={{ padding: 14, flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: TEXT_MUTED, textTransform: 'uppercase', marginBottom: 10, letterSpacing: '0.08em' }}>
            Scripts · {slugs.length}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6, overflowY: 'auto', minHeight: 0 }}>
            {slugs.map((slug) => {
              const selected = slug === selectedSlug;
              const s = SCRIPTS[slug];
              return (
                <button
                  key={slug}
                  onClick={() => { setSelectedSlug(slug); setFrame(0); }}
                  style={{
                    background: selected ? `${PRIMARY}1a` : 'transparent',
                    border: selected ? `1px solid ${PRIMARY}` : `1px solid transparent`,
                    borderRadius: 10, padding: '10px 14px', textAlign: 'left', cursor: 'pointer',
                  }}
                >
                  <div style={{ fontSize: 13, fontWeight: 600, color: selected ? PRIMARY_DEEP : TEXT }}>{slug}</div>
                  <div style={{ fontSize: 11, color: TEXT_MUTED, marginTop: 2 }}>
                    {s?.meta?.aspect || '16:9'} · {s?.beats?.length || 0} beats
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* === MAIN AREA === */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <div style={{
          height: 52, borderBottom: `1px solid ${BORDER}`, background: PANEL,
          display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 22px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 12, color: TEXT_MUTED }}>
            <span style={{ fontWeight: 700, color: PRIMARY_DEEP, textTransform: 'uppercase', letterSpacing: '0.1em' }}>
              {activeBeat?.role || '—'}
            </span>
            <span style={{ fontFamily: FONT_MONO }}>
              frame {frame} / {Math.max(0, frameCount - 1)} · {fmtTime(frame / FPS)}
            </span>
          </div>
          <button
            onClick={() => copy(shootCommand)}
            title="Click to copy. Render the MP4 + timing.json locally."
            style={{
              background: recentlyCopied ? 'rgba(45,184,125,0.10)' : PANEL,
              border: `1px solid ${recentlyCopied ? 'rgba(45,184,125,0.40)' : BORDER}`,
              borderRadius: 8, padding: '6px 12px', cursor: 'pointer',
              fontFamily: FONT_MONO, fontSize: 12, color: recentlyCopied ? SUCCESS : TEXT,
              display: 'flex', gap: 8, alignItems: 'center',
            }}
          >
            <span>$ {shootCommand}</span>
            <span style={{ fontFamily: FONT_BODY, fontWeight: 600, color: recentlyCopied ? SUCCESS : TEXT_MUTED }}>
              {recentlyCopied ? 'COPIED' : 'COPY'}
            </span>
          </button>
        </div>

        {/* preview */}
        <div
          ref={previewRef}
          style={{
            flex: 1, overflow: 'auto', display: 'flex', alignItems: 'center', justifyContent: 'center',
            padding: PREVIEW_PAD, background: CANVAS_BG,
            backgroundImage: `radial-gradient(circle at 20% 0%, ${PRIMARY}10, transparent 40%), radial-gradient(circle at 80% 100%, ${ACCENT}10, transparent 40%)`,
          }}
        >
          {script && Comp ? (
            <div style={{
              width: size.width * scale, height: size.height * scale, flexShrink: 0, margin: 'auto',
              boxShadow: '0 0 0 1px rgba(0,0,0,0.06), 0 30px 60px -20px rgba(0,0,0,0.16)',
              borderRadius: 6, overflow: 'hidden', background: PANEL,
            }}>
              <div style={{ width: size.width, height: size.height, transform: `scale(${scale})`, transformOrigin: 'top left' }}>
                <Comp script={script} frame={frame} fps={FPS} />
              </div>
            </div>
          ) : (
            <div style={{ color: TEXT_MUTED, fontSize: 15, fontWeight: 500 }}>
              Add a data/&lt;slug&gt;.script.json to preview
            </div>
          )}
        </div>

        {/* scrubber */}
        <div style={{
          borderTop: `1px solid ${BORDER}`, background: PANEL, padding: '14px 22px',
          display: 'flex', alignItems: 'center', gap: 16,
        }}>
          <input
            type="range"
            min={0}
            max={Math.max(0, frameCount - 1)}
            value={frame}
            onChange={(e) => setFrame(parseInt(e.target.value, 10))}
            style={{ flex: 1, accentColor: PRIMARY }}
          />
          <span style={{ fontFamily: FONT_MONO, fontSize: 12, color: TEXT_MUTED, whiteSpace: 'nowrap' }}>
            {fmtTime(frameCount / FPS)} total
          </span>
        </div>
      </div>
    </div>
  );
};

#!/usr/bin/env node

// Headless Social Post Renderer
// Launches Puppeteer against the Vite dev server, navigates to each design,
// screenshots the .template-canvas element at native resolution, saves to output/.
//
// Usage:
//   npm run dev                   # start the dev server first (port 3216)
//   npm run render -- launch-square
//   npm run render -- --all       # render all designs from samples.json

import puppeteer from 'puppeteer';
import { readFileSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { outputFilenameFor } from './_filename.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = resolve(__dirname, '../output');
const SAMPLES_PATH = resolve(__dirname, '../src/data/samples.json');
const DEV_SERVER = 'http://localhost:3216';

const args = process.argv.slice(2);
const renderAll = args.includes('--all');
const designKeys = renderAll ? null : args.filter((a) => !a.startsWith('--'));

const samples = JSON.parse(readFileSync(SAMPLES_PATH, 'utf-8'));
const keysToRender = renderAll ? Object.keys(samples) : designKeys;

if (!keysToRender || keysToRender.length === 0) {
  console.log('Usage:');
  console.log('  npm run render -- <design-key>     Render a specific design');
  console.log('  npm run render -- --all             Render all designs');
  console.log('');
  console.log('Available designs:');
  Object.keys(samples).forEach((k) => console.log(`  ${k}`));
  process.exit(0);
}

// Template size lookup (duplicated here to avoid importing JSX in Node).
// One entry per social format — keep in lockstep with the templateMeta
// sizes declared in src/templates/SocialPost.jsx.
const TEMPLATE_SIZES = {
  'social-square':   { width: 1080, height: 1080 }, // Instagram square / feed
  'social-portrait': { width: 1080, height: 1350 }, // Instagram portrait / feed
  'social-linkedin': { width: 1200, height: 627 },  // LinkedIn link/feed image
  'social-x':        { width: 1600, height: 900 },  // X (Twitter) 16:9
  // FinalPiece rich posts (all Instagram portrait)
  'fp-platform': { width: 1080, height: 1350 },
  'fp-website':  { width: 1080, height: 1350 },
  'fp-crm':      { width: 1080, height: 1350 },
  'fp-agents':   { width: 1080, height: 1350 },
};

async function renderDesign(browser, key, sample) {
  const size = TEMPLATE_SIZES[sample.template];
  if (!size) {
    console.error(`  Unknown template: ${sample.template}`);
    return;
  }

  const page = await browser.newPage();
  // deviceScaleFactor 1 + the transform-neutralise below = exact native-pixel
  // output (1080×1080, 1600×900, …) regardless of the editor's preview zoom.
  await page.setViewport({ width: size.width + 400, height: size.height + 200, deviceScaleFactor: 1 });

  await page.goto(DEV_SERVER, { waitUntil: 'networkidle0', timeout: 15000 });

  // Click the design in the sidebar (find by text content match on the key)
  const clicked = await page.evaluate((designKey) => {
    const buttons = document.querySelectorAll('button');
    for (const btn of buttons) {
      // Use a strict-ish match on the visible label so we don't accidentally
      // click the folder header. The button's first child div carries the key.
      const labelDiv = btn.querySelector('div');
      if (labelDiv && labelDiv.textContent.trim() === designKey) {
        btn.click();
        return true;
      }
    }
    return false;
  }, key);

  if (!clicked) {
    console.error(`  Could not find design "${key}" in sidebar`);
    await page.close();
    return;
  }

  await page.waitForSelector('.template-canvas', { timeout: 5000 });
  await page.waitForNetworkIdle({ idleTime: 500, timeout: 10000 }).catch(() => {});

  // The editor previews the canvas inside a scaled wrapper (Fit mode / zoom %).
  // Neutralise that so we screenshot the canvas at its TRUE native size — the
  // render must be deterministic, never coupled to whatever zoom is on screen.
  await page.evaluate(() => {
    const c = document.querySelector('.template-canvas');
    if (!c) return;
    const inner = c.parentElement;            // the transform: scale() wrapper
    if (inner) { inner.style.transform = 'none'; inner.style.transformOrigin = 'top left'; }
    const outer = inner && inner.parentElement; // the sized + overflow:hidden box
    if (outer) { outer.style.width = 'auto'; outer.style.height = 'auto'; outer.style.overflow = 'visible'; }
  });
  await new Promise((r) => setTimeout(r, 500)); // reflow + fonts settle

  const canvas = await page.$('.template-canvas');
  if (!canvas) {
    console.error(`  No .template-canvas found for "${key}"`);
    await page.close();
    return;
  }

  const outputPath = resolve(OUTPUT_DIR, outputFilenameFor(key, sample));
  await canvas.screenshot({ path: outputPath, type: 'png' });
  console.log(`  Rendered: ${outputPath}`);
  await page.close();
}

async function main() {
  mkdirSync(OUTPUT_DIR, { recursive: true });

  console.log(`Rendering ${keysToRender.length} design(s)...`);
  console.log(`Dev server: ${DEV_SERVER}`);
  console.log('');

  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });

  for (const key of keysToRender) {
    const sample = samples[key];
    if (!sample) {
      console.error(`  Design "${key}" not found in samples.json`);
      continue;
    }
    console.log(`  ${key} (${sample.template})...`);
    await renderDesign(browser, key, sample);
  }

  await browser.close();
  console.log('');
  console.log('Done.');
}

main().catch((err) => {
  console.error('Render failed:', err);
  process.exit(1);
});

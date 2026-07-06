#!/usr/bin/env node

// Headless Image Renderer
// Launches Puppeteer against the Vite dev server, navigates to each design,
// screenshots the .template-canvas element at native resolution, saves to output/.
//
// Usage:
//   npm run dev                  # start the dev server first
//   npm run render -- social-post-launch
//   npm run render -- --all      # render all designs from samples.json
//
// Requires the dev server to be running on port 3210 (or $BOS_THUMBNAIL_PORT).

import puppeteer from 'puppeteer';
import { readFileSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { outputFilenameFor } from './_filename.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = resolve(__dirname, '../output');
const SAMPLES_PATH = resolve(__dirname, '../src/data/samples.json');
// Dev-server port defaults to 3210; override with BOS_THUMBNAIL_PORT (the same
// var vite.config.js and shoot.js read) when 3210 is already in use.
const DEV_PORT = Number(process.env.BOS_THUMBNAIL_PORT) || 3210;
const DEV_SERVER = `http://localhost:${DEV_PORT}`;

// Parse CLI args
const args = process.argv.slice(2);
const renderAll = args.includes('--all');
const designKeys = renderAll ? null : args.filter((a) => !a.startsWith('--'));

// Load samples
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

// Template size lookup (duplicated here to avoid importing JSX in Node)
const TEMPLATE_SIZES = {
  'youtube-thumbnail': { width: 1280, height: 720 },
};

async function renderDesign(browser, key, sample) {
  const size = TEMPLATE_SIZES[sample.template];
  if (!size) {
    console.error(`  Unknown template: ${sample.template}`);
    return;
  }

  const page = await browser.newPage();
  await page.setViewport({ width: size.width + 400, height: size.height + 200, deviceScaleFactor: 2 });

  // Navigate to the editor
  await page.goto(DEV_SERVER, { waitUntil: 'networkidle0', timeout: 15000 });

  // Click the design in the sidebar (find button by text content)
  const clicked = await page.evaluate((designKey) => {
    const buttons = document.querySelectorAll('button');
    for (const btn of buttons) {
      if (btn.textContent.includes(designKey)) {
        btn.click();
        return true;
      }
    }
    return false;
  }, key);

  if (!clicked) {
    console.error(`  Could not find design "${key}" in the studio sidebar.`);
    console.error(`  If "${key}" IS in src/data/samples.json, the dev server is`);
    console.error(`  serving a stale copy: stop npm run dev and start it again so it`);
    console.error(`  picks up your new entry, then re-run the shoot.`);
    await page.close();
    return;
  }

  // Wait for the canvas to render + external images to load
  await page.waitForSelector('.template-canvas', { timeout: 5000 });
  await page.waitForNetworkIdle({ idleTime: 500, timeout: 10000 }).catch(() => {});
  await new Promise((r) => setTimeout(r, 500)); // let fonts settle

  // Screenshot just the template canvas at native resolution
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

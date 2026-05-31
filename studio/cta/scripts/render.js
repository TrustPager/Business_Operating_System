#!/usr/bin/env node

// Headless CTA Renderer
// Launches Puppeteer against the Vite dev server, navigates to each design,
// screenshots the .template-canvas element at native resolution, saves to output/.
//
// Usage:
//   npm run dev                   # start the dev server first (port 3213)
//   npm run render -- welcome
//   npm run render -- --all       # render all designs from samples.json

import puppeteer from 'puppeteer';
import { readFileSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { outputFilenameFor } from './_filename.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = resolve(__dirname, '../output');
const SAMPLES_PATH = resolve(__dirname, '../src/data/samples.json');
const DEV_SERVER = 'http://localhost:3213';

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

// Template size lookup (duplicated here to avoid importing JSX in Node)
const TEMPLATE_SIZES = {
  'hero-card-cta': { width: 1200, height: 460 },
};

async function renderDesign(browser, key, sample) {
  const size = TEMPLATE_SIZES[sample.template];
  if (!size) {
    console.error(`  Unknown template: ${sample.template}`);
    return;
  }

  const page = await browser.newPage();
  await page.setViewport({ width: size.width + 400, height: size.height + 200, deviceScaleFactor: 2 });

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
  await new Promise((r) => setTimeout(r, 500)); // fonts settle

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

#!/usr/bin/env node

// Render thumbnail PNG(s) via puppeteer and auto-open them.
//
// Usage:
//   npm run shoot                    # render every design in samples.json
//   npm run shoot connect-claude     # render one specific design
//   npm run shoot --no-open          # render but skip auto-open
//
// This is the canonical export path - it uses puppeteer + real Chrome
// rendering, which correctly handles background-clip:text, backdrop-filter,
// and other modern CSS features that the in-studio Download PNG button
// (html2canvas-based) can struggle with.

import { spawn } from 'child_process';
import { existsSync, readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { exec } from 'child_process';
import { outputFilenameFor as buildFilename } from './_filename.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '..');
const OUTPUT_DIR = resolve(PROJECT_ROOT, 'output');
const SAMPLES_PATH = resolve(PROJECT_ROOT, 'src/data/samples.json');
const RENDER_SCRIPT = resolve(__dirname, 'render.js');
// Dev-server port defaults to 3210; override with BOS_THUMBNAIL_PORT (the same
// var vite.config.js and render.js read) when 3210 is already in use.
const DEV_PORT = Number(process.env.BOS_THUMBNAIL_PORT) || 3210;
const DEV_SERVER = `http://localhost:${DEV_PORT}`;

// Parse args
const args = process.argv.slice(2);
const skipOpen = args.includes('--no-open');
const designArgs = args.filter((a) => !a.startsWith('--'));

// Determine which keys to render + open
const samples = JSON.parse(readFileSync(SAMPLES_PATH, 'utf8'));
const allKeys = Object.keys(samples);
const keysToShoot = designArgs.length > 0 ? designArgs : allKeys;

// Validate keys
for (const k of keysToShoot) {
  if (!samples[k]) {
    console.error(`Design "${k}" not found in samples.json.`);
    console.error(`Available: ${allKeys.join(', ')}`);
    process.exit(1);
  }
}

// Check dev server is up
const checkServer = async () => {
  try {
    const res = await fetch(DEV_SERVER, { signal: AbortSignal.timeout(2000) });
    return res.ok;
  } catch {
    return false;
  }
};

// Local shim so the rest of this file can keep its single-arg signature.
// The shared helper takes (key, sample); we look up the sample here.
function outputFilenameFor(key) {
  return buildFilename(key, samples[key]);
}

const openPng = (key) => {
  const png = resolve(OUTPUT_DIR, outputFilenameFor(key));
  if (!existsSync(png)) {
    console.error(`  PNG not found: ${png}`);
    return;
  }
  const cmd =
    process.platform === 'win32' ? `start "" "${png}"` :
    process.platform === 'darwin' ? `open "${png}"` :
    `xdg-open "${png}"`;
  exec(cmd, (err) => {
    if (err) console.error(`  Could not auto-open ${png}: ${err.message}`);
  });
};

(async () => {
  if (!(await checkServer())) {
    console.error('');
    console.error(`Dev server not reachable at ${DEV_SERVER}.`);
    console.error('Start it first in another terminal:');
    console.error('');
    console.error('  npm run dev');
    console.error('');
    console.error(`Port ${DEV_PORT} may be in use by another session or a leftover`);
    console.error('dev server. If so, pick a free port with BOS_THUMBNAIL_PORT');
    console.error('(then restart npm run dev), e.g.:');
    console.error('');
    console.error('  BOS_THUMBNAIL_PORT=3211 npm run dev      # in one terminal');
    console.error('  BOS_THUMBNAIL_PORT=3211 npm run shoot     # in this one');
    console.error('');
    process.exit(1);
  }

  // Spawn render.js with the same args we received
  const renderArgs = designArgs.length > 0 ? designArgs : ['--all'];
  console.log('');
  console.log(`Rendering ${keysToShoot.length} design(s) via puppeteer...`);
  console.log('');

  const child = spawn('node', [RENDER_SCRIPT, ...renderArgs], {
    stdio: 'inherit',
    cwd: PROJECT_ROOT,
  });

  child.on('close', (code) => {
    if (code !== 0) {
      console.error('');
      console.error(`Render exited with code ${code}.`);
      process.exit(code);
    }

    if (skipOpen) {
      console.log('');
      console.log('Done. (Skipped auto-open due to --no-open.)');
      return;
    }

    console.log('');
    console.log('Opening PNG(s)...');
    keysToShoot.forEach(openPng);
  });
})();

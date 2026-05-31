#!/usr/bin/env node

// Render CTA PNG(s) via puppeteer and auto-open them.
//
// Usage:
//   npm run shoot                    # render every design in samples.json
//   npm run shoot connect-claude     # render one specific design
//   npm run shoot --no-open          # render but skip auto-open

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
const DEV_SERVER = 'http://localhost:3213';

const args = process.argv.slice(2);
const skipOpen = args.includes('--no-open');
const designArgs = args.filter((a) => !a.startsWith('--'));

const samples = JSON.parse(readFileSync(SAMPLES_PATH, 'utf8'));
const allKeys = Object.keys(samples);
const keysToShoot = designArgs.length > 0 ? designArgs : allKeys;

for (const k of keysToShoot) {
  if (!samples[k]) {
    console.error(`Design "${k}" not found in samples.json.`);
    console.error(`Available: ${allKeys.join(', ')}`);
    process.exit(1);
  }
}

const checkServer = async () => {
  try {
    const res = await fetch(DEV_SERVER, { signal: AbortSignal.timeout(2000) });
    return res.ok;
  } catch {
    return false;
  }
};

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
    process.exit(1);
  }

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

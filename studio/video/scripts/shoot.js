#!/usr/bin/env node

// Render a video via puppeteer frame-capture + ffmpeg stitch, then auto-open it.
// Thin wrapper over render.js (clone of studio/social/scripts/shoot.js, adapted
// for the video studio's output layout).
//
// Usage:
//   npm run dev                       # start the dev server first (port 3218)
//   npm run shoot <slug>              # render data/<slug>.script.json
//   npm run shoot <slug> --no-open    # render without auto-opening the MP4

import { spawn, exec } from 'child_process';
import { existsSync, readdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { safeSlug } from './_filename.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '..');
const OUTPUT_DIR = resolve(PROJECT_ROOT, 'output');
const DATA_DIR = resolve(PROJECT_ROOT, 'data');
const RENDER_SCRIPT = resolve(__dirname, 'render.js');
const DEV_SERVER = 'http://localhost:3218';

const args = process.argv.slice(2);
const skipOpen = args.includes('--no-open');
const slugArg = args.find((a) => !a.startsWith('--'));

if (!slugArg) {
  console.error('Usage: npm run shoot <slug>');
  console.error('Available fixtures in data/:');
  try {
    readdirSync(DATA_DIR)
      .filter((f) => f.endsWith('.script.json'))
      .forEach((f) => console.error(`  ${f.replace('.script.json', '')}`));
  } catch { /* no data dir */ }
  process.exit(1);
}

const checkServer = async () => {
  try {
    const res = await fetch(DEV_SERVER, { signal: AbortSignal.timeout(2000) });
    return res.ok;
  } catch {
    return false;
  }
};

const openFile = (file) => {
  if (!existsSync(file)) return;
  const cmd =
    process.platform === 'win32' ? `start "" "${file}"` :
    process.platform === 'darwin' ? `open "${file}"` :
    `xdg-open "${file}"`;
  exec(cmd, (err) => {
    if (err) console.error(`  Could not auto-open ${file}: ${err.message}`);
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

  console.log('');
  console.log(`Rendering "${slugArg}" via puppeteer frame-capture...`);
  console.log('');

  const child = spawn('node', [RENDER_SCRIPT, slugArg], { stdio: 'inherit', cwd: PROJECT_ROOT });

  child.on('close', (code) => {
    if (code !== 0) {
      console.error('');
      console.error(`Render exited with code ${code}.`);
      process.exit(code);
    }
    if (skipOpen) return;
    const slug = safeSlug(slugArg);
    openFile(resolve(OUTPUT_DIR, slug, `${slug}.mp4`));
  });
})();

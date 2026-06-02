#!/usr/bin/env node

// Render a social post PNG and upload it to YOUR TrustPager workspace's
// "Social Posts" folder. After upload, the API returns a hosted URL you
// can drop into a scheduler, a caption draft, or download to post by hand.
//
// Auth resolves from your BOS install (same order as the Python tools):
//   1. $TRUSTPAGER_API_KEY environment variable
//   2. ~/.claude/bos.json   →  { "api_key": "tp_live_..." }
//
// Usage:
//   npm run publish <design-key>             render + upload (skip if exists)
//   npm run publish -- --all                 render + upload every design
//   npm run publish <design-key> --replace   delete existing then re-upload

import { spawn } from 'child_process';
import { existsSync, readFileSync } from 'fs';
import { outputFilenameFor as buildFilename } from './_filename.js';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { homedir } from 'os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '..');
const OUTPUT_DIR = resolve(PROJECT_ROOT, 'output');
const SAMPLES_PATH = resolve(PROJECT_ROOT, 'src/data/samples.json');
const RENDER_SCRIPT = resolve(__dirname, 'render.js');

const DEV_SERVER = 'http://localhost:3216';
const API_BASE = 'https://api.trustpager.com/functions/v1/api/v1';
const BOS_CONFIG_PATH = resolve(homedir(), '.claude', 'bos.json');
const TARGET_FOLDER = 'Social Posts';
const TARGET_CATEGORY = 'image';

const args = process.argv.slice(2);
const all = args.includes('--all');
const replace = args.includes('--replace');
const keyArgs = args.filter((a) => !a.startsWith('--'));

const samples = JSON.parse(readFileSync(SAMPLES_PATH, 'utf8'));
const allKeys = Object.keys(samples);
const keysToPublish = all ? allKeys : keyArgs;

if (keysToPublish.length === 0) {
  console.error('');
  console.error('Usage:');
  console.error('  npm run publish <design-key>                 publish one design (skip if exists)');
  console.error('  npm run publish -- --all                     publish every design');
  console.error('  npm run publish <design-key> --replace       delete existing then re-upload');
  console.error('');
  console.error(`Available keys: ${allKeys.join(', ')}`);
  process.exit(1);
}
for (const k of keysToPublish) {
  if (!samples[k]) {
    console.error(`Design "${k}" not found. Available: ${allKeys.join(', ')}`);
    process.exit(1);
  }
}

// Same auth resolution as BOS Python tools: env var first, then the
// BOS config file. If neither is set, point at the setup tool.
function loadApiKey() {
  const fromEnv = (process.env.TRUSTPAGER_API_KEY || '').trim();
  if (fromEnv) return fromEnv;

  if (existsSync(BOS_CONFIG_PATH)) {
    try {
      const cfg = JSON.parse(readFileSync(BOS_CONFIG_PATH, 'utf8'));
      if (cfg?.api_key) return cfg.api_key;
    } catch (err) {
      console.error(`Could not parse ${BOS_CONFIG_PATH}: ${err.message}`);
    }
  }
  console.error('');
  console.error('No TrustPager API key found.');
  console.error('Run `python tools/setup.py` from the BOS root to install one, or set');
  console.error('  export TRUSTPAGER_API_KEY=tp_live_...');
  console.error('');
  process.exit(1);
}
const apiKey = loadApiKey();

async function devServerUp() {
  try {
    const res = await fetch(DEV_SERVER, { signal: AbortSignal.timeout(2000) });
    return res.ok;
  } catch {
    return false;
  }
}

function renderViaPuppeteer(keys) {
  return new Promise((res, rej) => {
    const renderArgs = keys.length === allKeys.length ? ['--all'] : keys;
    const child = spawn('node', [RENDER_SCRIPT, ...renderArgs], {
      stdio: 'inherit',
      cwd: PROJECT_ROOT,
    });
    child.on('close', (code) => (code === 0 ? res() : rej(new Error(`render exited ${code}`))));
  });
}

function outputFilenameFor(key) {
  return buildFilename(key, samples[key]);
}

function formatApiError(payload, fallbackText) {
  if (!payload) return fallbackText;
  if (payload.error && typeof payload.error === 'object') {
    return payload.error.message || payload.error.code || JSON.stringify(payload.error);
  }
  return payload.error || payload.message || payload.detail || fallbackText || JSON.stringify(payload);
}

async function listExistingFiles() {
  const params = new URLSearchParams({ type: TARGET_CATEGORY, category: 'images', limit: '500' });
  const res = await fetch(`${API_BASE}/files?${params.toString()}`, {
    headers: { 'Authorization': `Bearer ${apiKey}` },
  });
  const text = await res.text();
  let payload;
  try { payload = JSON.parse(text); } catch { payload = { raw: text }; }
  if (!res.ok) {
    throw new Error(`List failed (${res.status}): ${formatApiError(payload, text)}`);
  }
  const items = payload.data || payload.files || [];
  const byName = new Map();
  for (const f of items) {
    const folderName = f.folder_name || f.folder?.name || f.folder;
    if (folderName !== TARGET_FOLDER) continue;
    const name = f.name || f.filename;
    const id = f.id || f.file_id;
    if (name && id) byName.set(name, id);
  }
  return { byName };
}

async function deleteFile(id) {
  const res = await fetch(`${API_BASE}/files/${id}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${apiKey}` },
  });
  const text = await res.text();
  let payload;
  try { payload = JSON.parse(text); } catch { payload = { raw: text }; }
  if (!res.ok) {
    throw new Error(`Delete failed (${res.status}): ${formatApiError(payload, text)}`);
  }
  return payload;
}

async function uploadOne(key) {
  const filename = outputFilenameFor(key);
  const pngPath = resolve(OUTPUT_DIR, filename);
  if (!existsSync(pngPath)) throw new Error(`PNG not found: ${pngPath}`);
  const base64 = readFileSync(pngPath).toString('base64');
  const body = {
    base64,
    name: filename,
    type: TARGET_CATEGORY,
    category: 'images',
    folder: TARGET_FOLDER,
    mime_type: 'image/png',
    description: `Social post: ${samples[key].data?.headline?.split('\n')[0] || key}`,
  };
  const res = await fetch(`${API_BASE}/files/upload`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const text = await res.text();
  let payload;
  try { payload = JSON.parse(text); } catch { payload = { raw: text }; }
  if (!res.ok) {
    throw new Error(`Upload failed (${res.status}): ${formatApiError(payload, text)}`);
  }
  return payload;
}

(async () => {
  if (!(await devServerUp())) {
    console.error('');
    console.error(`Dev server not reachable at ${DEV_SERVER}.`);
    console.error('Start it first in another terminal: npm run dev');
    console.error('');
    process.exit(1);
  }

  console.log('');
  console.log(`Publishing ${keysToPublish.length} design(s) → TrustPager > Files > "${TARGET_FOLDER}"`);
  console.log('');

  try {
    await renderViaPuppeteer(keysToPublish);
  } catch (err) {
    console.error(`Render step failed: ${err.message}`);
    process.exit(1);
  }

  console.log('');
  console.log(`Checking existing files in "${TARGET_FOLDER}"...`);
  let existing;
  try {
    existing = await listExistingFiles();
    console.log(`  Found ${existing.byName.size} file(s) already in folder.`);
  } catch (err) {
    console.error(`Could not list existing files: ${err.message}`);
    process.exit(1);
  }

  console.log('');
  console.log(replace
    ? 'Publishing (--replace: deleting existing then re-uploading)...'
    : 'Publishing (skip-if-exists)...');
  console.log('');

  let uploaded = 0, skipped = 0, replaced = 0, failed = 0;

  for (const key of keysToPublish) {
    const filename = outputFilenameFor(key);
    process.stdout.write(`  ${filename} ... `);
    const existingId = existing.byName.get(filename);

    try {
      if (existingId && !replace) {
        console.log('SKIPPED (already exists)');
        skipped++;
        continue;
      }
      if (existingId && replace) {
        process.stdout.write('deleting old ... ');
        await deleteFile(existingId);
      }
      const result = await uploadOne(key);
      const fileId = result.id || result.file?.id || result.file_id;
      console.log(existingId && replace ? 'REPLACED' : 'UPLOADED');
      if (fileId) console.log(`    file_id: ${fileId}`);
      if (existingId && replace) replaced++;
      else uploaded++;
    } catch (err) {
      console.log('FAILED');
      console.log(`    ${err.message}`);
      failed++;
    }
  }

  console.log('');
  console.log(`Done. ${uploaded} new · ${replaced} replaced · ${skipped} skipped · ${failed} failed.`);
  console.log('');

  if (failed > 0) process.exit(1);
})();

#!/usr/bin/env node

// Render a thumbnail PNG and upload it to YOUR TrustPager workspace's
// "Tutorial Thumbnails" folder.
//
// Auth resolves from the $TRUSTPAGER_API_KEY environment variable.
//
// Usage:
//   npm run publish <design-key>             render + upload one design (skip if exists)
//   npm run publish -- --all                 render + upload every design (skip existing)
//   npm run publish <design-key> --replace   delete existing then re-upload
//   npm run publish -- --all --replace       wipe + re-upload every design
//
// Idempotency + rename detection (prevents duplicates):
//
//   For every thumbnail we know two stable identifiers:
//     - filename     `${order} - ${title}.png`  (changes when order or title changes)
//     - description  `YouTube thumbnail for: ${headline}`  (stable per thumbnail)
//
//   On each publish run we list every file in the target folder and build
//   two maps: filename->id and description->id. For each design:
//
//     a) filename match  -> SKIP (default) or DELETE+UPLOAD (--replace)
//     b) description match (filename miss)  -> RENAME existing file to the
//        new filename. This is what catches schema changes like the order-
//        prefix migration: the server still has "How to Manage Tasks in
//        TrustPager.png" but we now want "7 - How to Manage Tasks in
//        TrustPager.png" — we rename, not re-upload. Single source of
//        truth on disk.
//     c) neither matches -> fresh UPLOAD.
//
// Flow:
//   1. Render the PNG via puppeteer (same path as `npm run shoot`).
//   2. Read the PNG file, encode to base64.
//   3. List existing files in the Tutorial Thumbnails folder.
//   4. For each design: rename / skip / replace / upload per the logic above.
//   5. POST to TrustPager /v1/files/upload with category=images, folder=
//      "Tutorial Thumbnails". API key resolves from the $TRUSTPAGER_API_KEY
//      env var.
//
// This is the "finalize" step. `npm run shoot` stays local-only for iteration.

import { spawn } from 'child_process';
import { existsSync, readFileSync } from 'fs';
import { outputFilenameFor as buildFilename } from './_filename.js';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '..');
const OUTPUT_DIR = resolve(PROJECT_ROOT, 'output');
const SAMPLES_PATH = resolve(PROJECT_ROOT, 'src/data/samples.json');
const RENDER_SCRIPT = resolve(__dirname, 'render.js');

const DEV_SERVER = 'http://localhost:3210';
const API_BASE = 'https://api.trustpager.com/functions/v1/api/v1';
const TARGET_FOLDER = 'Tutorial Thumbnails';
// "image" puts the file in CDN-backed image storage so it surfaces in the
// Content > Files > Images tab (and any image-picker UI). Folders are
// referenced by NAME, so the existing "Tutorial Thumbnails" folder works
// across types - the API auto-creates the folder for the image category
// on first upload if it doesn't already exist there.
const TARGET_CATEGORY = 'image';

// --- Args ---
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
  console.error('  npm run publish -- --all                     publish every design (skip existing)');
  console.error('  npm run publish <design-key> --replace       delete existing then re-upload');
  console.error('  npm run publish -- --all --replace           wipe + re-upload every design');
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

// --- API key ---
// Resolves from the $TRUSTPAGER_API_KEY environment variable. If it's not
// set, tell the operator to set it.
function loadApiKey() {
  const fromEnv = (process.env.TRUSTPAGER_API_KEY || '').trim();
  if (fromEnv) return fromEnv;

  console.error('');
  console.error('No TrustPager API key found.');
  console.error('');
  console.error('Set the TRUSTPAGER_API_KEY environment variable:');
  console.error('  export TRUSTPAGER_API_KEY=tp_live_...');
  console.error('');
  process.exit(1);
}
const apiKey = loadApiKey();

// --- Dev server check ---
async function devServerUp() {
  try {
    const res = await fetch(DEV_SERVER, { signal: AbortSignal.timeout(2000) });
    return res.ok;
  } catch {
    return false;
  }
}

// --- Render ---
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

// Local shim around the shared helper. Keeps the single-arg signature used
// throughout this file; the shared helper takes (key, sample).
function outputFilenameFor(key) {
  return buildFilename(key, samples[key]);
}

// --- Surface a sensible error message regardless of where the API stashes it ---
function formatApiError(payload, fallbackText) {
  if (!payload) return fallbackText;
  // Nested error objects: { error: { message: '...', code: '...' } }
  if (payload.error && typeof payload.error === 'object') {
    return payload.error.message || payload.error.code || JSON.stringify(payload.error);
  }
  return payload.error || payload.message || payload.detail || fallbackText || JSON.stringify(payload);
}

// --- List existing files in Tutorial Thumbnails ---
// Returns { byName, byDescription } maps of { key -> file_id } for every
// file in the target folder. The two maps power the rename-detection logic
// in the main loop: filename is the unstable identity (changes when the
// order or title changes); description is the stable per-thumbnail identity
// (set to "YouTube thumbnail for: <headline>" on upload, and headlines are
// unique per thumbnail).
//
// Strategy: list files filtered to category=images (server-side filter),
// then narrow to TARGET_FOLDER client-side. We don't pass `folder` as a
// query param because the API expects a folder UUID there and we only know
// the folder NAME.
async function listExistingFiles() {
  // The list endpoint requires `type` (the storage backend, singular) — same
  // value we send when uploading. `category` is a UI filter and not required
  // for listing, but we pass it too so the response is already narrowed.
  const params = new URLSearchParams({
    type: TARGET_CATEGORY,    // 'image' (singular) — storage backend
    category: 'images',        // 'images' (plural) — UI filter
    limit: '500',
  });
  const url = `${API_BASE}/files?${params.toString()}`;
  const res = await fetch(url, {
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
  const byDescription = new Map();
  for (const f of items) {
    // Folder identity in the response shape can be folder_name OR a nested
    // folder.name. Accept either.
    const folderName = f.folder_name || f.folder?.name || f.folder;
    if (folderName !== TARGET_FOLDER) continue;
    const name = f.name || f.filename;
    const id = f.id || f.file_id;
    const desc = f.description;
    if (name && id) byName.set(name, id);
    if (desc && id) byDescription.set(desc, id);
  }
  return { byName, byDescription };
}

// --- Rename an existing file (used when description matches but filename doesn't) ---
async function renameFile(id, newName) {
  const res = await fetch(`${API_BASE}/files/${id}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name: newName }),
  });
  const text = await res.text();
  let payload;
  try { payload = JSON.parse(text); } catch { payload = { raw: text }; }
  if (!res.ok) {
    throw new Error(`Rename failed (${res.status}): ${formatApiError(payload, text)}`);
  }
  if (payload.approval_id) {
    throw new Error(`Rename queued for approval (id: ${payload.approval_id}). Approve at https://app.trustpager.com/settings/api?tab=approvals then re-run.`);
  }
  return payload;
}

// --- Delete an existing file (used by --replace) ---
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
  // If the delete needs approval (e.g. secure-category files), the API returns
  // 202 + an approval_id. For images in the Tutorial Thumbnails folder this
  // should be a straight 200 — flag the approval case so the user knows.
  if (payload.approval_id) {
    throw new Error(`Delete queued for approval (id: ${payload.approval_id}). Approve at https://app.trustpager.com/settings/api?tab=approvals then re-run with --replace.`);
  }
  return payload;
}

// --- Upload ---
async function uploadOne(key) {
  const filename = outputFilenameFor(key);
  const pngPath = resolve(OUTPUT_DIR, filename);
  if (!existsSync(pngPath)) {
    throw new Error(`PNG not found: ${pngPath}`);
  }
  const base64 = readFileSync(pngPath).toString('base64');
  // API contract for POST /files/upload:
  //   type:     "image" | "document" | "secure" (storage backend)
  //   category: UI filter tag - "images" (plural!) makes the file appear on
  //             /content/images. Without this the file lives in storage but
  //             is filtered out of the Images grid (the grid runs
  //             `.eq('category', 'images')` server-side).
  //   folder:   folder NAME within the storage backend (not UUID)
  //   name:     filename with extension (matches the YouTube video title
  //             so you can drag-drop straight to the upload page)
  //   base64:   file contents
  const body = {
    base64,
    name: filename,
    type: TARGET_CATEGORY,
    category: 'images',
    folder: TARGET_FOLDER,
    mime_type: 'image/png',
    description: `YouTube thumbnail for: ${samples[key].data.headline}`,
  };

  const res = await fetch(`${API_BASE}/files/upload`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
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

// --- Main ---
(async () => {
  if (!(await devServerUp())) {
    console.error('');
    console.error(`Dev server not reachable at ${DEV_SERVER}.`);
    console.error('Start it first in another terminal: npm run dev');
    console.error('');
    process.exit(1);
  }

  console.log('');
  console.log(`Publishing ${keysToPublish.length} design(s) to FinalPiece > Tutorial Thumbnails`);
  console.log('');

  try {
    await renderViaPuppeteer(keysToPublish);
  } catch (err) {
    console.error('');
    console.error(`Render step failed: ${err.message}`);
    process.exit(1);
  }

  // List existing files so we can skip duplicates (default), delete-then-
  // upload (--replace), or rename when the description matches but the
  // filename has changed (the order-prefix migration shape). One request
  // up-front instead of one per upload.
  console.log('');
  console.log(`Checking existing files in "${TARGET_FOLDER}"...`);
  let existing;
  try {
    existing = await listExistingFiles();
    console.log(`  Found ${existing.byName.size} file(s) already in folder.`);
  } catch (err) {
    console.error('');
    console.error(`Could not list existing files: ${err.message}`);
    console.error('Aborting — refusing to upload without knowing what is already there.');
    process.exit(1);
  }

  console.log('');
  console.log(replace
    ? 'Publishing to TrustPager (--replace: deleting existing then re-uploading)...'
    : 'Publishing to TrustPager (skip-if-exists, rename if description matches)...');
  console.log('');

  let uploaded = 0;
  let skipped = 0;
  let replaced = 0;
  let renamed = 0;
  let failed = 0;

  for (const key of keysToPublish) {
    const filename = outputFilenameFor(key);
    const headline = samples[key]?.data?.headline;
    const description = headline ? `YouTube thumbnail for: ${headline}` : null;
    process.stdout.write(`  ${filename} ... `);

    const existingIdByName = existing.byName.get(filename);
    const existingIdByDesc = description ? existing.byDescription.get(description) : undefined;

    try {
      // (a) exact filename match
      if (existingIdByName && !replace) {
        console.log('SKIPPED (already exists)');
        skipped++;
        continue;
      }

      // (b) description match, filename miss — rename in place
      if (!existingIdByName && existingIdByDesc && !replace) {
        process.stdout.write('renaming existing ... ');
        await renameFile(existingIdByDesc, filename);
        console.log('RENAMED (matched by description)');
        renamed++;
        continue;
      }

      // (c) --replace: nuke the existing then re-upload
      if (existingIdByName && replace) {
        process.stdout.write('deleting old ... ');
        await deleteFile(existingIdByName);
      } else if (existingIdByDesc && replace) {
        process.stdout.write('deleting old (matched by description) ... ');
        await deleteFile(existingIdByDesc);
      }

      const result = await uploadOne(key);
      const fileId = result.id || result.file?.id || result.file_id;
      if ((existingIdByName || existingIdByDesc) && replace) {
        console.log('REPLACED');
        replaced++;
      } else {
        console.log('UPLOADED');
        uploaded++;
      }
      if (fileId) console.log(`    file_id: ${fileId}`);
    } catch (err) {
      console.log('FAILED');
      console.log(`    ${err.message}`);
      failed++;
    }
  }

  console.log('');
  console.log(`Done. ${uploaded} new · ${renamed} renamed · ${replaced} replaced · ${skipped} skipped · ${failed} failed.`);
  console.log('Open in TrustPager: https://app.trustpager.com/content/files');
  if (skipped > 0 && !replace) {
    console.log('');
    console.log('To force re-upload of existing files: npm run publish -- --all --replace');
  }
  console.log('');

  if (failed > 0) process.exit(1);
})();

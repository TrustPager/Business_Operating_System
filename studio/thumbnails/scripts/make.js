#!/usr/bin/env node

// Interactive prompt to add a new thumbnail design to samples.json.
//
// Usage:
//   npm run make
//
// Prompts for and validates:
//   - Design key (kebab-case)
//   - Headline (4-8 words, on-thumbnail text)
//   - Accent word (must appear in headline)
//   - Composition id (Remotion comp this thumbnail belongs to)
//   - YouTube title (validated against YOUTUBE_TITLES.md rules)
//   - YouTube description hook (auto-wraps with the standard CTA close)
//
// Auto-assigns the next available `order` (max + 1). After adding, prints
// the next commands to render and ship.
//
// The full YouTube title + description rules live in YOUTUBE_TITLES.md.
// Headline / accent / hero rules live in README.md and CLAUDE.md.

import readline from 'readline';
import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SAMPLES_PATH = resolve(__dirname, '../src/data/samples.json');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise((r) => rl.question(q, r));

const KEBAB = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const REQUIRED_CTA = 'Try TrustPager free: https://trustpager.com';
const BANNED_TITLE_WORDS = [
  'Claude', 'Anthropic', 'OpenAI', 'ChatGPT',
  'Retell', 'Twilio', 'Postmark', 'Resend', 'Sendgrid',
  'Recall', 'Recall.ai',
  'Stripe', 'Cloudflare',
];

function lintTitle(title) {
  const issues = [];
  if (!title.toLowerCase().includes('trustpager')) {
    issues.push('Must include "TrustPager"');
  }
  for (const banned of BANNED_TITLE_WORDS) {
    const re = new RegExp(`\\b${banned.replace(/\./g, '\\.')}\\b`, 'i');
    if (re.test(title)) issues.push(`Banned vendor name: "${banned}"`);
  }
  const words = title.trim().split(/\s+/).length;
  if (words > 14) issues.push(`Too long (${words} words, max 14)`);
  if (words < 4) issues.push(`Too short (${words} words, min 4)`);
  return issues;
}

(async () => {
  console.log('');
  console.log('Make a new YouTube thumbnail');
  console.log('-----------------------------');
  console.log('See YOUTUBE_TITLES.md for the title + description rules.');
  console.log('See README.md / CLAUDE.md for headline + hero rules.');
  console.log('');

  // 1. Design key
  let key;
  while (true) {
    key = (await ask('Design key (kebab-case, e.g. "agent-hub"): ')).trim();
    if (!key) { console.log('  Required.'); continue; }
    if (!KEBAB.test(key)) {
      console.log('  Must be kebab-case: lowercase letters, digits, and dashes only.');
      continue;
    }
    break;
  }

  // 2. Headline (on-thumbnail text)
  let headline;
  while (true) {
    headline = (await ask('On-thumbnail headline (4-8 words): ')).trim();
    if (!headline) { console.log('  Required.'); continue; }
    const wordCount = headline.split(/\s+/).length;
    if (wordCount < 4 || wordCount > 8) {
      console.log(`  Should be 4-8 words. Got ${wordCount}. Try again.`);
      continue;
    }
    break;
  }

  // 3. Accent word
  let accentWord;
  while (true) {
    accentWord = (await ask('Accent word (must appear in headline): ')).trim();
    if (!accentWord) { console.log('  Required.'); continue; }
    const re = new RegExp(`\\b${accentWord.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i');
    if (!re.test(headline)) {
      console.log(`  "${accentWord}" not found in "${headline}".`);
      continue;
    }
    break;
  }

  // 4. Composition id
  const composition = (await ask('Remotion composition id (e.g. "Tutorial-EmailMarketing"): ')).trim();
  if (!composition) {
    console.log('  Warning: no composition linked. `npm run coverage` will flag this.');
  }

  // 5. YouTube title (validated against YOUTUBE_TITLES.md)
  let title;
  while (true) {
    title = (await ask('YouTube title (e.g. "How to ... in TrustPager"): ')).trim();
    if (!title) { console.log('  Required.'); continue; }
    const issues = lintTitle(title);
    if (issues.length > 0) {
      console.log('  Title issues — see YOUTUBE_TITLES.md:');
      for (const i of issues) console.log(`    - ${i}`);
      const retry = (await ask('  Retry? (Y/n): ')).trim().toLowerCase();
      if (retry === 'n' || retry === 'no') break;
      continue;
    }
    break;
  }

  // 6. YouTube description hook (single paragraph; CTA is auto-appended)
  console.log('');
  console.log('YouTube description body (one paragraph, then the CTA is auto-appended).');
  console.log('  Hook should lead with the outcome the viewer gets.');
  console.log('  See YOUTUBE_TITLES.md > "Description template" for examples.');
  const hook = (await ask('Description body: ')).trim();
  const description = hook ? `${hook}\n\n${REQUIRED_CTA}` : '';
  if (!description) {
    console.log('  Warning: empty description. `npm run coverage` will flag this.');
  }

  // 7. Load samples, handle overwrite, compute next order
  const samples = JSON.parse(readFileSync(SAMPLES_PATH, 'utf8'));
  if (samples[key]) {
    const overwrite = (await ask(`  Design "${key}" already exists. Overwrite? (y/N): `)).trim().toLowerCase();
    if (overwrite !== 'y' && overwrite !== 'yes') {
      console.log('Aborted.');
      rl.close();
      process.exit(0);
    }
  }

  const existingOrders = Object.values(samples)
    .map(e => e?.order)
    .filter(o => typeof o === 'number');
  const order = (samples[key]?.order)
    ?? (existingOrders.length > 0 ? Math.max(...existingOrders) + 1 : 1);

  // 8. Write
  const entry = {
    template: 'youtube-thumbnail',
    order,
  };
  if (composition) entry.composition = composition;
  entry.data = { headline, accentWord };
  if (title) entry.data.title = title;
  if (description) entry.data.description = description;
  samples[key] = entry;
  writeFileSync(SAMPLES_PATH, JSON.stringify(samples, null, 2) + '\n');

  rl.close();

  console.log('');
  console.log(`  Added "${key}" to samples.json (order ${order})`);
  console.log('');
  console.log('Next:');
  console.log(`  npm run dev               # live preview at http://localhost:3210`);
  console.log(`  npm run shoot ${key}      # render PNG`);
  console.log(`  npm run coverage          # lint the entry`);
  console.log(`  npm run publish ${key}    # upload to FinalPiece > Tutorial Thumbnails`);
  console.log('');
})();

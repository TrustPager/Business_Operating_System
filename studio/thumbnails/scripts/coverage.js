#!/usr/bin/env node

// Cross-reference Remotion compositions <-> thumbnail entries.
//
// Usage:
//   npm run coverage
//
// What it does:
//   1. Scans every <Composition id="..."> in ../src/compositions/ (the Remotion side)
//   2. Reads samples.json (the thumbnail side) and pulls each entry's
//      top-level "composition" field
//   3. Cross-references both directions and prints:
//        * Linked    -- composition has a thumbnail
//        * Missing   -- composition is a published tutorial with NO thumbnail
//        * Orphan    -- thumbnail entry points at a composition that doesn't exist
//   4. Regenerates COMPOSITION_MAP.md at the project root
//
// Required = composition id starts with Tutorial- or Email-. These are the
// published YouTube tutorial videos that need YouTube thumbnails. Everything
// else (Feature-, Promo-, Hybrid-, Claude-, SpecCheck-) is treated as
// optional / internal and surfaced only at the bottom of the report.

import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { resolve, dirname, join, relative } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '..');
const REMOTION_ROOT = resolve(PROJECT_ROOT, '..');
const REMOTION_SRC = resolve(REMOTION_ROOT, 'src/compositions');
const SAMPLES_PATH = resolve(PROJECT_ROOT, 'src/data/samples.json');
const MAP_PATH = resolve(PROJECT_ROOT, 'COMPOSITION_MAP.md');

const COMPOSITION_REGEX = /<Composition\s+id=["']([^"']+)["']/g;

// Non-prefixed published comps that still need thumbnails. Add to this list
// any composition that is a published YouTube video but doesn't follow the
// Tutorial-/Email- naming convention. Hybrid-LeadsPipeline-Build is the
// flagship 90-second demo and counts as published.
const PUBLISHED_NON_PREFIXED = new Set([
  'Hybrid-LeadsPipeline-Build',
]);

// Title lint rules — see YOUTUBE_TITLES.md for the full system.
// Words banned from YouTube titles (case-insensitive). Internal code is
// exempt. We use word boundaries so "Recall" only matches whole word, not
// e.g. "recalled". Replacements suggested in YOUTUBE_TITLES.md.
const BANNED_TITLE_WORDS = [
  'Claude', 'Anthropic', 'OpenAI', 'ChatGPT',
  'Retell', 'Twilio', 'Postmark', 'Resend', 'Sendgrid',
  'Recall', 'Recall.ai',
  'Stripe', 'Cloudflare',
];
const REQUIRED_TITLE_WORD = 'TrustPager';
const TITLE_MIN_WORDS = 4;
const TITLE_MAX_WORDS = 14;
const REQUIRED_CTA = 'Try TrustPager free: https://trustpager.com';

function lintTitle(title) {
  const issues = [];
  if (!title || typeof title !== 'string') {
    issues.push('Title missing or not a string');
    return issues;
  }
  if (!title.toLowerCase().includes(REQUIRED_TITLE_WORD.toLowerCase())) {
    issues.push(`Missing "${REQUIRED_TITLE_WORD}"`);
  }
  for (const banned of BANNED_TITLE_WORDS) {
    const re = new RegExp(`\\b${banned.replace(/\./g, '\\.')}\\b`, 'i');
    if (re.test(title)) {
      issues.push(`Banned vendor name: "${banned}" (see YOUTUBE_TITLES.md for replacement)`);
    }
  }
  const words = title.trim().split(/\s+/).length;
  if (words > TITLE_MAX_WORDS) issues.push(`Too long (${words} words, max ${TITLE_MAX_WORDS})`);
  if (words < TITLE_MIN_WORDS) issues.push(`Too short (${words} words, min ${TITLE_MIN_WORDS})`);
  return issues;
}

function lintDescription(desc) {
  const issues = [];
  if (!desc) { issues.push('No description'); return issues; }
  if (!desc.trimEnd().endsWith(REQUIRED_CTA)) {
    issues.push(`Missing CTA line at end ("${REQUIRED_CTA}")`);
  }
  return issues;
}

function isRequired(id) {
  // *-Test suffix = act-level test fixtures (Tutorial-ConnectClaude-v2-Act1-Test
  // etc.) used to render single acts during development. Not published videos.
  if (/-Test$/.test(id)) return false;
  if (PUBLISHED_NON_PREFIXED.has(id)) return true;
  return id.startsWith('Tutorial-') || id.startsWith('Email-');
}

function findAllCompositions(dir) {
  const results = [];
  function walk(d) {
    for (const entry of readdirSync(d)) {
      const full = join(d, entry);
      const stat = statSync(full);
      if (stat.isDirectory()) {
        walk(full);
        continue;
      }
      if (!full.endsWith('.tsx')) continue;
      const content = readFileSync(full, 'utf-8');
      let m;
      COMPOSITION_REGEX.lastIndex = 0;
      while ((m = COMPOSITION_REGEX.exec(content)) !== null) {
        results.push({
          id: m[1],
          file: relative(REMOTION_ROOT, full).replace(/\\/g, '/'),
        });
      }
    }
  }
  walk(dir);
  return results;
}

function pad(s, n) {
  if (s.length >= n) return s;
  return s + ' '.repeat(n - s.length);
}

function main() {
  const samples = JSON.parse(readFileSync(SAMPLES_PATH, 'utf-8'));
  const comps = findAllCompositions(REMOTION_SRC);

  // Build maps from samples.json
  const thumbToComp = {};
  const compToThumb = {};
  const thumbsWithNoComp = [];
  for (const [key, entry] of Object.entries(samples)) {
    const comp = entry.composition || entry?.data?.composition || null;
    if (comp) {
      thumbToComp[key] = comp;
      compToThumb[comp] = key;
    } else {
      thumbsWithNoComp.push(key);
    }
  }

  // Categorize compositions
  const allCompIds = new Set(comps.map((c) => c.id));
  const linked = [];
  const missing = [];
  const other = [];

  for (const c of comps) {
    if (!isRequired(c.id)) {
      other.push(c);
      continue;
    }
    if (compToThumb[c.id]) {
      const key = compToThumb[c.id];
      linked.push({
        ...c,
        key,
        title: samples[key]?.data?.title || '(no title)',
      });
    } else {
      missing.push(c);
    }
  }

  // Orphans: thumbnail entries pointing at non-existent comp ids
  const orphans = [];
  for (const [key, comp] of Object.entries(thumbToComp)) {
    if (!allCompIds.has(comp)) {
      orphans.push({ key, comp });
    }
  }

  // ---- Console output ----
  console.log('');
  console.log('TrustPager Thumbnail Coverage');
  console.log('=============================');
  console.log('');
  console.log(`  Linked:  ${linked.length}`);
  console.log(`  Missing: ${missing.length}  ${missing.length > 0 ? '  <- compositions without thumbnails' : ''}`);
  console.log(`  Orphan:  ${orphans.length}  ${orphans.length > 0 ? '  <- thumbnails pointing at deleted comps' : ''}`);
  console.log(`  Other:   ${other.length}   (non-Tutorial/Email compositions, no thumbnail required)`);
  console.log('');

  if (linked.length > 0) {
    console.log('Linked thumbnails:');
    linked.sort((a, b) => a.id.localeCompare(b.id));
    for (const l of linked) {
      console.log(`  [OK]   ${pad(l.id, 42)} -> ${l.key}`);
    }
    console.log('');
  }

  if (missing.length > 0) {
    console.log('Compositions MISSING thumbnails:');
    missing.sort((a, b) => a.id.localeCompare(b.id));
    for (const m of missing) {
      console.log(`  [MISS] ${pad(m.id, 42)}  (${m.file})`);
    }
    console.log('');
    console.log('  -> Run `npm run make` to add a thumbnail for each.');
    console.log('');
  }

  if (orphans.length > 0) {
    console.log('Orphan thumbnail entries (composition not found in Remotion):');
    for (const o of orphans) {
      console.log(`  [ORPH] ${pad(o.key, 30)} -> ${o.comp}`);
    }
    console.log('');
    console.log('  -> Either fix the composition field in samples.json or delete the entry.');
    console.log('');
  }

  if (thumbsWithNoComp.length > 0) {
    console.log('Thumbnail entries with NO composition field:');
    for (const k of thumbsWithNoComp) {
      console.log(`  [WARN] ${k}`);
    }
    console.log('');
    console.log('  -> Add a "composition" field linking it to a Remotion comp id.');
    console.log('');
  }

  // ---- Title + description lint ----
  // Validates every entry's title against YOUTUBE_TITLES.md. Non-blocking
  // (won't exit non-zero on lint issues alone) so legacy titles that haven't
  // been re-published yet stay visible without breaking the build.
  const lintIssues = [];
  for (const [key, entry] of Object.entries(samples)) {
    const t = entry?.data?.title;
    const d = entry?.data?.description;
    const titleIssues = lintTitle(t).map(msg => ({ key, kind: 'title', msg, value: t }));
    const descIssues = lintDescription(d).map(msg => ({ key, kind: 'description', msg, value: t }));
    lintIssues.push(...titleIssues, ...descIssues);
  }
  if (lintIssues.length > 0) {
    console.log('Title + description lint (see YOUTUBE_TITLES.md):');
    for (const i of lintIssues) {
      console.log(`  [WARN] ${pad(i.key, 22)} ${i.kind === 'title' ? 'TITLE' : 'DESC'} - ${i.msg}`);
      if (i.value && i.kind === 'title') console.log(`         "${i.value}"`);
    }
    console.log('');
  } else {
    console.log('Title + description lint: clean.');
    console.log('');
  }

  // ---- Write COMPOSITION_MAP.md ----
  const ts = new Date().toISOString();
  let md = '';
  md += '# TrustPager Thumbnail <-> Composition Map\n\n';
  md += 'Auto-generated by `npm run coverage`. Do not edit by hand.\n\n';
  md += `**Last run:** ${ts}\n\n`;
  md += `**Coverage:** ${linked.length} linked · ${missing.length} missing · ${orphans.length} orphans\n\n`;
  md += `**Title/description lint:** ${lintIssues.length === 0 ? 'clean' : lintIssues.length + ' warning(s) — see bottom of file'}\n\n`;
  md += '## How this file is used\n\n';
  md += 'Two ways to look up the mapping:\n\n';
  md += '- **From a Remotion composition** -> find its row in "Linked thumbnails" below to see which thumbnail it uses, or look in "Compositions missing thumbnails" to confirm it needs one built.\n';
  md += '- **From a thumbnail key** -> the `composition` field in [`src/data/samples.json`](src/data/samples.json) is the source of truth. This file is just a rendered view.\n\n';
  md += 'To regenerate: `npm run coverage` (also prints the report to the terminal).\n\n';

  md += '## Linked thumbnails\n\n';
  if (linked.length === 0) {
    md += '_None._\n\n';
  } else {
    md += '| Composition | Thumbnail key | YouTube title |\n';
    md += '|---|---|---|\n';
    linked.sort((a, b) => a.id.localeCompare(b.id));
    for (const l of linked) {
      md += `| \`${l.id}\` | \`${l.key}\` | ${l.title} |\n`;
    }
    md += '\n';
  }

  md += '## Compositions missing thumbnails\n\n';
  if (missing.length === 0) {
    md += '_None. Every required composition has a thumbnail._\n\n';
  } else {
    md += 'These published tutorial compositions have no entry in `samples.json`. Run `npm run make` to add one.\n\n';
    md += '| Composition | File |\n';
    md += '|---|---|\n';
    missing.sort((a, b) => a.id.localeCompare(b.id));
    for (const m of missing) {
      md += `| \`${m.id}\` | \`${m.file}\` |\n`;
    }
    md += '\n';
  }

  if (orphans.length > 0) {
    md += '## Orphan thumbnail entries\n\n';
    md += 'Thumbnail entries whose `composition` field points at a Remotion comp id that does not exist (renamed, deleted, or typo).\n\n';
    md += '| Thumbnail key | Points at | Status |\n';
    md += '|---|---|---|\n';
    for (const o of orphans) {
      md += `| \`${o.key}\` | \`${o.comp}\` | Not found |\n`;
    }
    md += '\n';
  }

  if (thumbsWithNoComp.length > 0) {
    md += '## Thumbnail entries with no `composition` field\n\n';
    for (const k of thumbsWithNoComp) {
      md += `- \`${k}\`\n`;
    }
    md += '\n';
  }

  if (other.length > 0) {
    md += '## Other compositions (no thumbnail required)\n\n';
    md += 'Non-Tutorial/Email compositions. Listed for awareness only.\n\n';
    md += '<details>\n<summary>Show ' + other.length + ' compositions</summary>\n\n';
    md += '| Composition | File |\n';
    md += '|---|---|\n';
    other.sort((a, b) => a.id.localeCompare(b.id));
    for (const o of other) {
      md += `| \`${o.id}\` | \`${o.file}\` |\n`;
    }
    md += '\n</details>\n\n';
  }

  if (lintIssues.length > 0) {
    md += `## Title + description lint warnings\n\n`;
    md += `See [YOUTUBE_TITLES.md](YOUTUBE_TITLES.md) for the rule set.\n\n`;
    md += `| Entry | Field | Issue |\n`;
    md += `|---|---|---|\n`;
    for (const i of lintIssues) {
      md += `| \`${i.key}\` | ${i.kind} | ${i.msg.replace(/\|/g, '\\|')} |\n`;
    }
    md += `\n`;
  }

  writeFileSync(MAP_PATH, md, 'utf-8');
  console.log(`Wrote ${relative(PROJECT_ROOT, MAP_PATH).replace(/\\/g, '/')}`);
  console.log('');

  // Exit non-zero only on orphans (genuinely broken state).
  // Missing thumbnails are todo items, not errors.
  if (orphans.length > 0) {
    process.exit(1);
  }
}

main();

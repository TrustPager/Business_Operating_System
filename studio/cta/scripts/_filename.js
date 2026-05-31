// Shared output-filename helper used by render.js, shoot.js, publish.js.
//
// Filename shape: `${sequence ?? 'cta'}-${key}.png`
// - `sequence`  optional top-level field on the sample. When set (e.g.
//                "welcome-trial"), the filename gets a prefix so all CTAs
//                for a given nurture sequence sort together in the output
//                folder + the TrustPager Files folder. Missing → "cta".
// - `key`       the design's key from samples.json (the slug Simon types
//                into `npm run shoot <key>`). Always present.
// - Strips characters Windows actually rejects (< > : " / \ | ? *).

export function outputFilenameFor(key, sample) {
  const sequence = sample?.sequence || 'cta';
  const raw = `${sequence}-${key}.png`;
  return raw.replace(/[<>:"/\\|?*]/g, '');
}

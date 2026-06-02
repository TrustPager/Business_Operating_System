// Shared output-filename helper used by render.js, shoot.js, publish.js.
//
// Filename shape: `${platform}-${key}.png`
// - `platform`  derived from the sample's template id (social-square →
//                "ig-square", social-linkedin → "linkedin", …). Prefixing by
//                platform keeps every variant of one campaign sorted together
//                in the output folder + the TrustPager Files folder, and makes
//                it obvious which size each PNG is when you go to post it.
// - `key`       the design's key from samples.json (the slug you type into
//                `npm run shoot <key>`). Always present.
// - Strips characters Windows actually rejects (< > : " / \ | ? *).

const PLATFORM_PREFIX = {
  'social-square':   'ig-square',
  'social-portrait': 'ig-portrait',
  'social-linkedin': 'linkedin',
  'social-x':        'x',
};

export function outputFilenameFor(key, sample) {
  const platform = PLATFORM_PREFIX[sample?.template] || 'social';
  const raw = `${platform}-${key}.png`;
  return raw.replace(/[<>:"/\\|?*]/g, '');
}

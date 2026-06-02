// Shared output-filename helper used by render.js, shoot.js, publish.js.
//
// OG images are deployed to a website's /og/ folder where the filename
// usually has to match the route it previews (e.g. docs-home.png →
// <meta og:image> on the home page). So a sample may declare an explicit
// `filename`; that wins. Otherwise we fall back to `${key}.png`.
//
// Strips characters Windows actually rejects (< > : " / \ | ? *).

export function outputFilenameFor(key, sample) {
  const raw = sample?.filename || `${key}.png`;
  const withExt = raw.endsWith('.png') ? raw : `${raw}.png`;
  return withExt.replace(/[<>:"/\\|?*]/g, '');
}

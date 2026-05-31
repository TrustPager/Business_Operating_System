// Shared output-filename helper used by render.js, shoot.js, publish.js.
//
// Filename shape: `${order} - ${title}.png`
// - `order`     comes from the top-level "order" field in samples.json. It's
//                a stable per-thumbnail integer (1, 2, 3, …) that lets you
//                find newly-added thumbnails in the output folder by looking
//                at the end of the numbered list. When missing, the order
//                prefix is omitted so legacy entries still render.
// - `title`     is the YouTube video title (sample.data.title). Strips only
//                the characters Windows actually rejects (< > : " / \ | ? *).
//                `&` is preserved because we want "Build & Send Forms".
// - Falls back to `key` if title is missing.

export function outputFilenameFor(key, sample) {
  const title = sample?.data?.title;
  const order = sample?.order;
  const safe = (title || key).replace(/[<>:"/\\|?*]/g, '');
  const prefix = (typeof order === 'number' && order > 0) ? `${order} - ` : '';
  return `${prefix}${safe}.png`;
}

// Shared output-naming helpers for the video studio, used by render.js + shoot.js.
//
// Everything for one script sorts together under output/<slug>/:
//   output/<slug>/frames/frame-000000.png   the captured frames
//   output/<slug>/<slug>.mp4                 the stitched video (silent stereo track)
//   output/<slug>/<slug>.gif                 a preview GIF
//   output/<slug>/<slug>.timing.json         the timing sidecar (spec §3 / Pin 1)
//
// Slugs come from the script's own `slug`; we still strip characters Windows
// rejects (< > : " / \ | ? *) defensively.

export function safeSlug(slug) {
  return String(slug || 'video').replace(/[<>:"/\\|?*]/g, '').trim() || 'video';
}

export function frameName(index) {
  return `frame-${String(index).padStart(6, '0')}.png`;
}

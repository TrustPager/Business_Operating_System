#!/usr/bin/env python3
"""Breakout engine for break-down-a-channel.

Turns a `yt-dlp --flat-playlist --dump-json` channel dump (view counts +
reverse-chronological order; NO dates in flat mode) into an upload-order outlier
series and a rank-based breakout inflection. Pure stdlib, deterministic, no
network. Reimplemented from the documented method; no third-party source.

Two distinct signals, two questions:

  * Outlier multiple = a video's views / the median of the previous `window`
    videos in upload order (a rolling trailing baseline by video count). This is
    the timeline y-axis and answers "which individual videos overperformed their
    neighbours" — the videos worth studying.

  * Breakout inflection = the durable upward step in the channel's own view
    level. Detected on log1p(view_count) (NOT on the self-normalising outlier —
    a rolling baseline turns a durable step into a transient bump, so a step
    detector can't see it there). Scan every candidate split with >= min_segment
    videos each side, score each with a Mann-Whitney U rank test (upward shifts
    only), take the most significant split above a z threshold. A rank test + a
    minimum segment length means one lone spike can never register as a step.

Honest caveat the skill must surface: a durable view step can reflect audience
growth as well as a packaging change, which is exactly why the skill reads *what
changed* at the inflection rather than trusting the number alone.
"""
import argparse
import json
import math
from statistics import median


def parse_flat_dump(entries):
    """entries: list of yt-dlp flat-playlist JSON objects (or {'entries': [...]}).
    Returns videos oldest->newest, dropping any with null view_count."""
    if isinstance(entries, dict):
        entries = entries.get("entries", entries.get("videos", []))
    kept = []
    for e in entries:
        vc = e.get("view_count")
        if vc is None:
            continue
        kept.append({
            "title": (e.get("title") or "").strip(),
            "view_count": int(vc),
            "url": e.get("url") or e.get("webpage_url") or e.get("id"),
            "playlist_index": e.get("playlist_index"),
        })
    # flat dump is reverse-chron (index 1 = newest). Oldest->newest:
    if kept and all(v["playlist_index"] is not None for v in kept):
        kept.sort(key=lambda v: v["playlist_index"], reverse=True)
    else:
        kept.reverse()
    return kept


def rolling_outlier(videos, window=10):
    """Attach 'outlier' = views / median(previous `window` views). Videos without
    at least 3 prior videos get outlier=None (not enough baseline)."""
    out = []
    for i, v in enumerate(videos):
        prior = [videos[j]["view_count"] for j in range(max(0, i - window), i)]
        w = dict(v)
        base = median(prior) if prior else 0
        w["outlier"] = (v["view_count"] / base) if len(prior) >= 3 and base > 0 else None
        out.append(w)
    return out


def _mann_whitney_z(a, b):
    """Normal-approximation z for U of sample b vs a (positive z => b ranks higher)."""
    n1, n2 = len(a), len(b)
    if n1 == 0 or n2 == 0:
        return 0.0
    combined = sorted([(x, 0) for x in a] + [(x, 1) for x in b])
    # average ranks for ties
    ranks = [0.0] * len(combined)
    i = 0
    while i < len(combined):
        j = i
        while j + 1 < len(combined) and combined[j + 1][0] == combined[i][0]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[k] = avg
        i = j + 1
    r2 = sum(ranks[k] for k in range(len(combined)) if combined[k][1] == 1)
    u2 = r2 - n2 * (n2 + 1) / 2.0
    mu = n1 * n2 / 2.0
    sigma = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12.0)
    return (u2 - mu) / sigma if sigma > 0 else 0.0


def detect_breakout(scored, min_segment=5, z_threshold=2.0):
    """Find the durable upward step in the channel's view level.

    Operates on log1p(view_count) across all videos oldest->newest (not the
    self-normalising outlier). Returns the most significant upward split, or
    no_upward_inflection. `scored` is rolling_outlier output (any list of dicts
    with view_count); the outlier field is used only to report the trigger's
    multiple, never for detection.
    """
    views = [v["view_count"] for v in scored]
    if len(views) < 2 * min_segment:
        return {"status": "no_upward_inflection", "reason": "too few videos"}
    vals = [math.log1p(v) for v in views]
    best = None
    for s in range(min_segment, len(vals) - min_segment + 1):
        pre, post = vals[:s], vals[s:]
        z = _mann_whitney_z(pre, post)
        if z > 0 and median(post) > median(pre):
            if best is None or z > best[1]:
                best = (s, z)
    if best is None or best[1] < z_threshold:
        return {"status": "no_upward_inflection"}
    split_pos, z = best
    trig = scored[split_pos]
    return {
        "status": "ok",
        "trigger_index": split_pos,
        "trigger_title": trig["title"],
        "trigger_url": trig.get("url"),
        "trigger_outlier": (round(trig["outlier"], 2) if trig.get("outlier") is not None else None),
        "z": round(z, 2),
        "pre_median_views": int(median(views[:split_pos])),
        "post_median_views": int(median(views[split_pos:])),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Breakout engine for break-down-a-channel")
    ap.add_argument("dump", help="yt-dlp --flat-playlist --dump-json output (json array or {entries:[]})")
    ap.add_argument("--window", type=int, default=10)
    ap.add_argument("--min-segment", type=int, default=5)
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    with open(a.dump, encoding="utf-8") as f:
        text = f.read().strip()
    entries = (json.loads(text) if text.startswith(("[", "{"))
               else [json.loads(l) for l in text.splitlines() if l.strip()])
    vids = parse_flat_dump(entries)
    scored = rolling_outlier(vids, window=a.window)
    report = {
        "video_count": len(vids),
        "timeline": [{"index": i, "title": v["title"], "views": v["view_count"],
                      "outlier": v.get("outlier"), "url": v.get("url")}
                     for i, v in enumerate(scored)],
        "breakout": detect_breakout(scored, min_segment=a.min_segment),
    }
    js = json.dumps(report, indent=2)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(js)
    else:
        print(js)


if __name__ == "__main__":
    main()

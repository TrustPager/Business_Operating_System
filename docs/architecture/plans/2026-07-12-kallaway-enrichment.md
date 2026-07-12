# Kallaway Enrichment Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Absorb the keyless, YouTube-scoped value from Kallaway's Sandcastles skills into BOS: (A) the bullseye audience model into `distribution-method.md` with anchors, (B) computed outlier scoring sharpened in `youtube-packaging-method.md` + `research-my-channel`, and (C) a new `break-down-a-channel` teardown skill on a reimplemented deterministic breakout engine.

**Architecture:** Two enrichments are pure authoring (one owner file + tight inline anchors, per the shared-rules doctrine). The new skill pairs a reasoning-heavy `SKILL.md` with one real code artifact — `tools/channel_breakdown.py`, a pure-stdlib deterministic engine that turns a `yt-dlp --flat-playlist` dump (view counts + reverse-chron order, no dates) into an upload-order outlier timeline and a rank-based breakout inflection. No Kallaway source enters the repo; methods are reimplemented and credited like `distribution-method.md` already does.

**Tech Stack:** Markdown (knowledge + skills), Python stdlib (the engine + unittest), `yt-dlp` (kind: local, keyless) for the channel dump, existing BOS tooling (`lint-skill`, `check-doctrine-voice`, `check-surface-budget`, `registry-generator`, `export-capabilities`).

**Spec:** docs/architecture/2026-07-12-kallaway-enrichment-design.md (approved 2026-07-12)

---

## Source-of-truth note on altitude

The spec and the two target method files own the *content* (the ring ladder, the 3/1/1 rule, the outlier definition, the breakout method). This plan owns the *mechanics* (exact files, edits, code, commands, gates). Where a task says "author per the spec," write the prose against the spec + method file, not against inlined copy here. The one place code is reproduced in full is Task C1 (the engine), because it is the load-bearing artifact and must be byte-complete so the implementer never guesses the math.

## Validation doctrine (from the codebase)

Reasoning-heavy surfaces (the two enrichments + `break-down-a-channel`'s body) are validated by `check-doctrine-voice` + a scripted **Sonnet dogfood** (the pass bar, as `get-found-online`/`youtube-studio` were). The one code artifact (`tools/channel_breakdown.py`) is validated by **TDD unittest fixtures** (offline, deterministic). The final acceptance gate is a **live end-to-end dogfood on the AI BOS channel** (Task D3) — not a fixture, not a replay.

## CI-order gates (run in Task D1; all must pass)

```bash
BOS_OFFLINE=1 python tools/check-no-secrets.py
BOS_OFFLINE=1 python tools/check-kernel-clean.py
BOS_OFFLINE=1 python tools/check-doctrine-voice.py
BOS_OFFLINE=1 python tools/check-connectors.py
BOS_OFFLINE=1 python tools/check-onboarding-binding.py
BOS_OFFLINE=1 python tools/check-surface-budget.py
BOS_OFFLINE=1 python tools/registry-generator.py --check
BOS_OFFLINE=1 python tools/export-capabilities.py --check
python tools/lint-skill.py skills/break-down-a-channel
BOS_OFFLINE=1 python -m unittest discover -s tests -v
```

---

## File map (lock decomposition before tasks)

**Modify (knowledge):**
- `knowledge/distribution-method.md` — new section "The audience bullseye" (ring ladder + 3/1/1 + sourcing rule); extend the existing Kallaway source note; add consumers to the consumer list. (Task A1)
- `knowledge/youtube-packaging-method.md` — sharpen the "Outlier analysis" section to a named, reported multiple with median-relative bands + caveats; add a Kallaway source note. (Task B1)

**Modify (skills — tight anchors only, no rule bodies):**
- `skills/build-social-strategy/SKILL.md` — Step 3 anchor: "audience spread" as the second axis. (Task A2)
- `skills/plan-my-content/SKILL.md` — batch allocated per 3/1/1; each post carries both a content-type tag and a ring tag. (Task A3)
- `skills/plan-my-youtube/SKILL.md` — ring ladder drives topic selection under the held avatar. (Task A4)
- `skills/research-my-channel/SKILL.md` — Step 1 reports the computed outlier multiple. (Task B2)

**Create (the new skill + engine):**
- `tools/channel_breakdown.py` — the deterministic breakout engine (parse → rolling outlier → rank-based inflection). (Task C1)
- `tests/test_channel_breakdown.py` — parse test (null view_count), detection test, lone-spike test. (Task C1)
- `skills/break-down-a-channel/SKILL.md` — the new teardown skill. (Task C3)
- `drivers/yt-dlp/README.md` — MODIFY: document the channel-history (`--flat-playlist`) use + the no-dates boundary. (Task C2)

**Modify (discovery / inventory — regenerated or hand-edited):**
- `knowledge/starter-projects.md` — discovery row for `break-down-a-channel`. (Task C4)
- `kernel/registry.json`, `docs/CAPABILITIES.md` — regenerated. (Task C4)

---

## Task A1: Bullseye section in distribution-method.md

**Files:**
- Modify: `knowledge/distribution-method.md`

- [ ] **Step 1:** Add a new section "## The audience bullseye — the ring ladder and the audience spread" after Lever 1 (it extends Lever 1's one-avatar principle). Write, per spec §Workstream A: the 5-level ring ladder (centre + 4 rings, one constraint relaxed per ring, size ~5-10x out, conversion decays out); the **3/1/1 audience spread** (3 centre / 1 Ring 1 / 1 Ring 2 per 5 videos, never past Ring 2 in phase one, plus the calibration loop); the **sourcing rule** (topics from centre/Ring 1 only, craft from anywhere, empty centre = the opening). Name it "audience spread," never a second "mix."
- [ ] **Step 2:** Extend the existing dev-facing Kallaway source note to cover the bullseye ("the ring ladder / 3/1/1 / sourcing rule synthesise Kallaway's Bullseye method").
- [ ] **Step 3:** Add `plan-my-content` and `plan-my-youtube` to the "Consumers that reference this file" list if not already complete for the bullseye anchor.
- [ ] **Step 4:** Run `BOS_OFFLINE=1 python tools/check-doctrine-voice.py`. Expected: PASS (no em dashes as sentence connectors, no banned framings).
- [ ] **Step 5:** Commit.
```bash
git add knowledge/distribution-method.md
git commit -m "feat(distribution-method): add the audience bullseye (ring ladder + 3/1/1 + sourcing)"
```

## Task A2: Anchor in build-social-strategy

**Files:**
- Modify: `skills/build-social-strategy/SKILL.md` (Step 3, near part 4 "The content mix")

- [ ] **Step 1:** Add a short anchor (2-4 sentences) introducing the **audience spread** as a *second, orthogonal axis* to the existing content-type mix: content mix = what a post is *about*; audience spread = who it's *aimed at* (the 3/1/1 across rings). Point to `distribution-method.md`'s bullseye section as the owner. Do NOT restate the ring ladder here and do NOT touch part 4's existing type-mix wording.
- [ ] **Step 2:** `python tools/lint-skill.py skills/build-social-strategy` and `BOS_OFFLINE=1 python tools/check-surface-budget.py`. Expected: PASS (description unchanged, still ≤400 chars).
- [ ] **Step 3:** Commit.
```bash
git add skills/build-social-strategy/SKILL.md
git commit -m "feat(build-social-strategy): anchor the audience-spread axis (bullseye)"
```

## Task A3: Anchor in plan-my-content

**Files:**
- Modify: `skills/plan-my-content/SKILL.md`

- [ ] **Step 1:** Read the skill to find where it lays out the calendar/batch. Add a tight anchor: the batch is allocated across rings per 3/1/1, and each planned post carries **both** its content-type tag and its ring tag (they compose, e.g. "proof × centre"). Reference `distribution-method.md` as the owner.
- [ ] **Step 2:** `python tools/lint-skill.py skills/plan-my-content`. Expected: PASS.
- [ ] **Step 3:** Commit.
```bash
git add skills/plan-my-content/SKILL.md
git commit -m "feat(plan-my-content): allocate the batch by audience spread (3/1/1)"
```

## Task A4: Anchor in plan-my-youtube

**Files:**
- Modify: `skills/plan-my-youtube/SKILL.md`

- [ ] **Step 1:** Add a tight anchor: the ring ladder drives topic selection under the one held avatar; ties to the virality formula already referenced there. Reference `distribution-method.md`. No rule body restated.
- [ ] **Step 2:** `python tools/lint-skill.py skills/plan-my-youtube`. Expected: PASS.
- [ ] **Step 3:** Commit.
```bash
git add skills/plan-my-youtube/SKILL.md
git commit -m "feat(plan-my-youtube): anchor the ring ladder for topic selection"
```

## Task B1: Computed outlier in youtube-packaging-method.md

**Files:**
- Modify: `knowledge/youtube-packaging-method.md` (the "Outlier analysis" section)

- [ ] **Step 1:** Rewrite the section to define the **outlier multiple = views ÷ the channel's trailing baseline** (median of the recent uploads within the window you can see), reported explicitly ("did 4.2x this channel's baseline"). Add the **median-relative** interpretation bands (`<1x` below this channel's typical — never "under-performing"; `~1-2x` solid; `2-5x` real outlier; `5x+` breakout) and the caveats (young video still compounding; tiny sample = noisy baseline; never compute from an unobserved number). Keep the existing "look across the niche" and table content.
- [ ] **Step 2:** Add a dev-facing Kallaway source note to the file (it currently has none): the outlier-multiple definition synthesises Kallaway's outlier-score.
- [ ] **Step 3:** `BOS_OFFLINE=1 python tools/check-doctrine-voice.py`. Expected: PASS.
- [ ] **Step 4:** Commit.
```bash
git add knowledge/youtube-packaging-method.md
git commit -m "feat(youtube-packaging-method): computed outlier multiple + median-relative bands"
```

## Task B2: research-my-channel reports the multiple

**Files:**
- Modify: `skills/research-my-channel/SKILL.md` (Step 1 "Competitor content scan")

- [ ] **Step 1:** Update Step 1's outlier bullet + the output so cited outliers report the **computed multiple** ("did ~4x this channel's baseline") instead of only "plainly outperformed", from the visible view counts, in-reasoning. Keep every existing hard rule (never invent an outlier or a number; real observed view counts only). Reference the sharpened `youtube-packaging-method.md` definition rather than restating the math.
- [ ] **Step 2:** `python tools/lint-skill.py skills/research-my-channel` and `BOS_OFFLINE=1 python tools/check-doctrine-voice.py`. Expected: PASS.
- [ ] **Step 3:** Commit.
```bash
git add skills/research-my-channel/SKILL.md
git commit -m "feat(research-my-channel): report the computed outlier multiple"
```

## Task C1: The breakout engine (TDD)

**Files:**
- Create: `tools/channel_breakdown.py`
- Test: `tests/test_channel_breakdown.py`

Reimplemented from the documented method (spec §Workstream C Engine). Pure stdlib. No Kallaway source.

- [ ] **Step 1: Write the failing tests.**
```python
# tests/test_channel_breakdown.py
"""Tests for tools/channel_breakdown.py — the breakout engine.
Offline, deterministic, no network. Run:
    BOS_OFFLINE=1 python -m unittest tests.test_channel_breakdown
"""
import unittest
from tools.channel_breakdown import parse_flat_dump, rolling_outlier, detect_breakout

class TestParse(unittest.TestCase):
    def test_skips_null_views_and_orders_oldest_first(self):
        # yt-dlp flat dump: playlist_index 1 = most recent (reverse-chron)
        entries = [
            {"playlist_index": 1, "title": "newest", "view_count": 50000},
            {"playlist_index": 2, "title": "shorts", "view_count": None},   # skipped
            {"playlist_index": 3, "title": "oldest", "view_count": 10000},
        ]
        vids = parse_flat_dump(entries)
        self.assertEqual([v["title"] for v in vids], ["oldest", "newest"])  # oldest->newest
        self.assertTrue(all(v["view_count"] is not None for v in vids))

class TestRollingOutlier(unittest.TestCase):
    def test_steady_channel_reads_near_1x(self):
        vids = [{"title": f"v{i}", "view_count": 10000} for i in range(20)]
        out = rolling_outlier(vids, window=5)
        # every video with enough history sits ~1.0x on a flat channel
        scored = [v for v in out if v.get("outlier") is not None]
        self.assertTrue(scored)
        for v in scored:
            self.assertAlmostEqual(v["outlier"], 1.0, delta=0.01)

class TestDetect(unittest.TestCase):
    def test_finds_a_real_step(self):
        # first 12 low, then a sustained ~5x step for 12 more
        vids = [{"title": f"v{i}", "view_count": 10000} for i in range(12)] + \
               [{"title": f"v{i}", "view_count": 50000} for i in range(12, 24)]
        out = rolling_outlier(vids, window=5)
        res = detect_breakout(out, min_segment=5)
        self.assertEqual(res["status"], "ok")
        self.assertGreaterEqual(res["trigger_index"], 11)
        self.assertLessEqual(res["trigger_index"], 14)

    def test_lone_spike_is_not_a_durable_step(self):
        # flat channel with a single 20x spike -> NOT an inflection
        vids = [{"title": f"v{i}", "view_count": 10000} for i in range(24)]
        vids[12]["view_count"] = 200000
        out = rolling_outlier(vids, window=5)
        res = detect_breakout(out, min_segment=5)
        self.assertEqual(res["status"], "no_upward_inflection")
```
- [ ] **Step 2: Run to verify they fail.** `BOS_OFFLINE=1 python -m unittest tests.test_channel_breakdown -v` → FAIL (module not found).
- [ ] **Step 3: Implement `tools/channel_breakdown.py`.**
```python
#!/usr/bin/env python3
"""Breakout engine for break-down-a-channel.

Turns a `yt-dlp --flat-playlist --dump-json` channel dump (view counts +
reverse-chronological order; NO dates in flat mode) into an upload-order outlier
series and a rank-based breakout inflection. Pure stdlib, deterministic, no
network. Reimplemented from the documented method; no third-party source.

Outlier multiple = a video's views / the median of the previous `window` videos
in upload order (a rolling trailing baseline by video count, so steady channel
growth reads ~1x throughout and the scan finds packaging step-changes).

Breakout detection: on log1p(outlier), scan candidate splits with >= min_segment
videos on each side, score each with a Mann-Whitney U rank test (upward shifts
only), take the most significant upward split above a z threshold. A rank test +
a minimum segment length means one lone spike can never register as a step.
"""
import argparse, json, math, sys
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
    if all(v["playlist_index"] is not None for v in kept):
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
        w["outlier"] = (v["view_count"] / median(prior)) if len(prior) >= 3 and median(prior) > 0 else None
        out.append(w)
    return out

def _mann_whitney_z(a, b):
    """Normal-approximation z for U of sample b vs a (positive z => b ranks higher)."""
    n1, n2 = len(a), len(b)
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
    """scored: rolling_outlier output. Returns the most significant upward split."""
    series = [(i, math.log1p(v["outlier"])) for i, v in enumerate(scored) if v.get("outlier") is not None]
    if len(series) < 2 * min_segment:
        return {"status": "no_upward_inflection", "reason": "too few scored videos"}
    vals = [x for _, x in series]
    best = None
    for s in range(min_segment, len(series) - min_segment + 1):
        pre, post = vals[:s], vals[s:]
        z = _mann_whitney_z(pre, post)
        if z > 0 and median(post) > median(pre):
            if best is None or z > best[1]:
                best = (s, z)
    if best is None or best[1] < z_threshold:
        return {"status": "no_upward_inflection"}
    split_pos, z = best
    trigger_series_idx = series[split_pos][0]
    pre_o = [scored[series[k][0]]["outlier"] for k in range(split_pos)]
    post_o = [scored[series[k][0]]["outlier"] for k in range(split_pos, len(series))]
    trig = scored[trigger_series_idx]
    return {
        "status": "ok",
        "trigger_index": trigger_series_idx,
        "trigger_title": trig["title"],
        "trigger_url": trig.get("url"),
        "z": round(z, 2),
        "pre_median_outlier": round(median(pre_o), 2),
        "post_median_outlier": round(median(post_o), 2),
    }

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("dump", help="yt-dlp --flat-playlist --dump-json output (json array or {entries:[]})")
    ap.add_argument("--window", type=int, default=10)
    ap.add_argument("--min-segment", type=int, default=5)
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    with open(a.dump, encoding="utf-8") as f:
        text = f.read().strip()
    entries = json.loads(text) if text.startswith(("[", "{")) else [json.loads(l) for l in text.splitlines() if l.strip()]
    vids = parse_flat_dump(entries)
    scored = rolling_outlier(vids, window=a.window)
    report = {
        "video_count": len(vids),
        "timeline": [{"index": i, "title": v["title"], "views": v["view_count"], "outlier": v.get("outlier"), "url": v.get("url")} for i, v in enumerate(scored)],
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
```
- [ ] **Step 4: Run tests to verify they pass.** `BOS_OFFLINE=1 python -m unittest tests.test_channel_breakdown -v` → PASS (4 tests).
- [ ] **Step 5: Commit.**
```bash
git add tools/channel_breakdown.py tests/test_channel_breakdown.py
git commit -m "feat(channel_breakdown): deterministic rank-based breakout engine + tests"
```

## Task C2: yt-dlp driver — document the channel-history use

**Files:**
- Modify: `drivers/yt-dlp/README.md`

- [ ] **Step 1:** Add a section documenting the **channel-history** use: `yt-dlp --flat-playlist --dump-json "<channel>/videos"` returns each video's `view_count` (rounded) and `playlist_index` (reverse-chron), and **no dates** in flat mode. State plainly it is still `kind: local`, keyless, read-only; Firecrawl remains the default surface read; this dump is `break-down-a-channel`'s specific need. Do not claim date fields.
- [ ] **Step 2:** `BOS_OFFLINE=1 python tools/check-connectors.py` and `BOS_OFFLINE=1 python tools/check-doctrine-voice.py`. Expected: PASS (yt-dlp still resolves as kind local; no activation path added).
- [ ] **Step 3:** Commit.
```bash
git add drivers/yt-dlp/README.md
git commit -m "docs(yt-dlp): document the keyless channel-history flat dump (no dates)"
```

## Task C3: The break-down-a-channel skill

**Files:**
- Create: `skills/break-down-a-channel/SKILL.md`

- [ ] **Step 1: Write the frontmatter.** `name: Break Down A Channel`; a description ≤400 chars, keyless, outcome-led, positive-only; `triggers` (break down a channel, how did this channel blow up, reverse-engineer a youtube channel, when did they take off, study a creator); `function_slot: research`; `requires_driver: yt-dlp`; `requires_credential: none`; `data_path: local`; `status: active`; `produces_customer_facing_copy: true`.
- [ ] **Step 2: Write the body** per spec §Workstream C: intake (one channel handle/URL) → pull the channel dump via `yt-dlp --flat-playlist --dump-json` (Bash) → run `tools/channel_breakdown.py` → read its JSON → write the teardown (`channel-breakdown-<handle>-<date>.md`): the upload-order outlier timeline (highlights inline), the breakout inflection (or "no durable step — a launch spike that reverted"), spike-vs-step, what changed at the inflection (read against `youtube-packaging-method.md`), and the one transferable, positive lesson. Hard rules: keyless, YouTube-only, real observed numbers only (never invent), no dates claimed from the flat dump, the funnel/monetization layer is out of v1, content-rules (no em dashes, no vendor leak). Credit nothing to a third-party vendor in customer-facing copy.
- [ ] **Step 3:** `python tools/lint-skill.py skills/break-down-a-channel`. Expected: PASS. If it rejects `data_path: local` for this shape, switch to the value the linter accepts and note it (spec's plan-time manifest check).
- [ ] **Step 4:** `BOS_OFFLINE=1 python tools/check-surface-budget.py` and `BOS_OFFLINE=1 python tools/check-onboarding-binding.py` and `BOS_OFFLINE=1 python tools/check-connectors.py`. Expected: PASS (≤400 chars; keyless-clean; yt-dlp resolves).
- [ ] **Step 5: Commit.**
```bash
git add skills/break-down-a-channel/SKILL.md
git commit -m "feat(break-down-a-channel): new keyless YouTube channel-teardown skill"
```

## Task C4: Discovery + inventory

**Files:**
- Modify: `knowledge/starter-projects.md`, `kernel/registry.json`, `docs/CAPABILITIES.md`

- [ ] **Step 1:** Add a `starter-projects.md` row for `break-down-a-channel` under the market/content group (keyless-tagged, outcome-led, skill-id in backticks), mirroring the youtube-studio Phase-1 rows.
- [ ] **Step 2:** Regenerate the registry + capabilities: `BOS_OFFLINE=1 python tools/registry-generator.py` then `BOS_OFFLINE=1 python tools/export-capabilities.py`.
- [ ] **Step 3:** Verify: `BOS_OFFLINE=1 python tools/registry-generator.py --check` and `BOS_OFFLINE=1 python tools/export-capabilities.py --check`. Expected: PASS (clean, no diff).
- [ ] **Step 4:** Commit.
```bash
git add knowledge/starter-projects.md kernel/registry.json docs/CAPABILITIES.md
git commit -m "feat(break-down-a-channel): register + surface in discovery and capabilities"
```

## Task D1: Full CI-order gate block

- [ ] **Step 1:** Run the full CI-order block (see top). Expected: every gate PASS, all unittests green.
- [ ] **Step 2:** Fix any failure at its source (not by loosening a gate). Re-run until green.
- [ ] **Step 3:** Commit any fixes.
```bash
git add -A
git commit -m "chore(kallaway-enrichment): green on the full CI-order gate block"
```

## Task D2: Scripted Sonnet dogfood

- [ ] **Step 1:** On Sonnet (the target client model), dry-run each touched surface against a realistic owner scenario: `build-social-strategy` (does the audience spread read as a second axis, not overwrite the type-mix?), `plan-my-content` (do posts carry both tags?), `plan-my-youtube` (ring ladder used?), `research-my-channel` (reports a computed multiple, invents nothing?), `break-down-a-channel` (produces a coherent teardown on fixture data?).
- [ ] **Step 2:** Note any place a rule was missed on Sonnet (the shared-rules field-incident risk). If an anchor was skipped, tighten the inline anchor (this is why anchors exist). Re-run.
- [ ] **Step 3:** Record the dogfood result (green/what changed) in the branch as a short note or commit message.

## Task D3: LIVE dogfood on the AI BOS channel (acceptance gate)

**Not done until this passes on real, fresh data.**

- [ ] **Step 1:** Pull a real channel history: `yt-dlp --flat-playlist --dump-json "<a live outlier-heavy channel in our space>/videos"` → run `tools/channel_breakdown.py` → confirm the timeline + inflection are sane against reality (spot-check the trigger video actually is a step, not a spike).
- [ ] **Step 2:** Run `break-down-a-channel` end-to-end on that channel and read the teardown for genuine, correct, useful insight (not fixture-shaped).
- [ ] **Step 3:** Exercise the Bullseye + computed-outlier enrichments in a real `build-social-strategy` / `research-my-channel` run **aimed at the AI BOS channel** — our own channel as the subject — on current live data.
- [ ] **Step 4:** Capture the live outputs, judge them honestly (do they hold up? anything invented? anything generic?), and write a short dogfood report. Only then is the cycle done.

## Finish

- [ ] Use superpowers:finishing-a-development-branch to decide merge to main. Push stays the founder's call (BOS repo is public; auto-mode false-blocks BOS pushes).
- [ ] Update the memory note for this project's state.

# Kallaway Enrichment — Design

**Status:** Approved 2026-07-12 (founder confirmed scope + funnel-trim + standalone-skill + live dogfood).
**Branch:** `feat/kallaway-enrichment`.

## Why this exists

Kane Kallaway's "Sandcastles" content-research skills were studied to find what BOS
can absorb. The headline finding: his `.skill` files are thin orchestration prompts;
the intelligence lives in the paid **Sandcastles** data engine (real per-video metrics
across YouTube/TikTok/IG, keyed on an **outlier score** = a video's views ÷ that
channel's trailing ~3-month average). Two of his four skills are useless without that
subscription. The value BOS can take, keylessly and YouTube-scoped, is:

1. The **operational audience model** (ring ladder + 3/1/1 mix + sourcing rule) that
   sits on top of the one-avatar principle BOS already teaches.
2. **Computed** outlier scoring, replacing the eyeballed read BOS already prescribes.
3. A one-channel **breakout teardown** — a genuinely new capability.

## Provenance and the public-repo rule (load-bearing)

The BOS repo is public. Kallaway's `.skill` / `.py` files are from his gated product.
**No line of his source enters this repo.** We reimplement the *methods* — all of which
are plainly described and are standard statistics — in BOS's own code and words, and we
credit him with a dev-facing source note exactly as
[`distribution-method.md`](../../knowledge/distribution-method.md) already does
("synthesises frameworks taught by Kallaway"). His files stay in the founder's local
`Skill research` folder, off-repo.

---

## Workstream A — Bullseye operational layer (enrichment)

**Home (one owner):** a new section in `knowledge/distribution-method.md`, which already
owns Lever 1 (one avatar, the darts metaphor). The bullseye is the operational extension
of that lever, so it belongs in the same file, not a new one.

New section content:
- **The ring ladder** — centre (exact ICP) + 4 rings, each relaxing exactly one constraint
  (industry → deal size → business model → profession). Each ring is a real, nameable
  audience. Size grows ~5-10x per ring out; conversion proximity decays outward.
- **The 3/1/1 batch mix** — for every 5 videos: 3 at centre (deep conversion), 1 at Ring 1
  (reach-with-conversion), 1 at Ring 2 (pure reach). Never past Ring 2 in phase one; the
  algorithm carries you to the outer rings after you earn it. Plus the **calibration loop**:
  run 3/1/1 for the first 2-3 batches, then bias future batches toward whichever ring
  actually converted (follows, DMs, enquiries) — the data decides.
- **The sourcing rule** — topics come from centre / Ring 1 only (drift broad and the
  fit score muddles); craft (hooks, formats, editing, pacing) can be studied from anywhere.
  If the centre is empty of creators, that is the opening: pull a Ring 1 topic and re-aim it.

**Anti-collision note (critical):** `build-social-strategy` Step 3 **part 4** already owns a
**content mix** on the *content-type* axis (educational / social-proof / promotional /
behind-the-scenes). The 3/1/1 is a **different axis — audience proximity**. Two things both
named "mix" in the same Step 3 is itself the drift risk, so **do not reuse the word "mix"
for the ring axis** — name it **"audience spread"** (or "reach allocation"). Every anchor
presents them as two orthogonal axes that *compose*: a planned post carries **both** tags at
once, e.g. "proof × centre" or "educational × Ring 2" (what it's *about* × who it's *aimed
at*). This makes orthogonality structural, not merely asserted, and never overwrites the
existing type-mix.

**Inline anchors (tight, per the shared-rules doctrine — referenced-only rules get missed
on Sonnet):**
- `skills/build-social-strategy/SKILL.md` — Step 3, alongside the existing content mix:
  a short anchor introducing the **audience spread** as the second axis (never a second
  "mix"), pointing to the distribution-method section as the owner.
- `skills/plan-my-content/SKILL.md` — the dated calendar allocates the batch across rings
  per 3/1/1, and each planned post carries **both** its content-type tag and its ring tag
  (they compose, e.g. "proof × centre").
- `skills/plan-my-youtube/SKILL.md` — the ring ladder drives topic selection under the one
  held avatar; ties to the virality formula already referenced there.

Each anchor is a few sentences that name the rule and cite the owner file. The full method
lives once, in `distribution-method.md`.

---

## Workstream B — Computed outlier scoring (enrichment, in-reasoning)

**Home (one owner):** the existing "Outlier analysis" section of
`knowledge/youtube-packaging-method.md`. It already says "median of the last 10-20 videos …
clears it by a clear multiple." Sharpen from vague to a **named, reported number**:

- **Outlier multiple = video views ÷ the channel's trailing baseline** (median of the
  channel's recent uploads within the window you can see; prefer a trailing ~3-month window
  when dates are visible, else the last ~10-20 uploads).
- Report it explicitly, e.g. "did **4.2x** this channel's baseline."
- **Interpretation bands** (directional): `< 1x` below the channel's own median, `~1-2x`
  solid, `2-5x` real outlier, `5x+` breakout — study hardest. **These describe relative
  position, not quality:** because the baseline is the channel's own median, roughly half a
  healthy channel sits `< 1x` by construction — say "below this channel's typical", never
  "under-performing", so the read doesn't scold half a good channel.
- **Caveats:** a very young video is still compounding (note it, don't over-read); a tiny
  visible sample makes the baseline noisy (say so); never compute from a number you did
  not actually observe.

**Consumer:** `skills/research-my-channel/SKILL.md` Step 1 reports the computed multiple per
cited outlier instead of "plainly outperformed." Stays keyless and in-reasoning from the
visible view counts; the optional `yt-dlp` deepener gives a fuller list for a steadier
baseline. Real numbers only — the existing "never invent an outlier or a number" rule holds.

No new code in this workstream. The math is done in-reasoning by the skill.

---

## Workstream C — New skill `break-down-a-channel` (youtube studio)

A bounded, keyless, one-channel teardown. Distinct from `research-my-channel`
("what should *I* make across a niche") — this answers "how did *this one* channel break
out, and what transfers?"

**Deliverable:** `channel-breakdown-<handle>-<date>.md` (+ inline highlights):
1. **Outlier-score timeline** — every video by **upload order** (x, oldest→newest) vs
   outlier multiple (y), the inflection and any spike cluster marked. The spine of the
   story. (Order, not calendar date — see the data-path note; exact dates are not in the
   flat dump and are fetched per-video only for the handful around the inflection, if wanted.)
2. **The breakout inflection** — the video where the channel's rolling performance
   step-changed upward (or "no durable step — a launch spike that reverted").
3. **Spike vs durable step** — did it level up, or fire one hit and mean-revert?
4. **What changed** at the inflection — topic / format / packaging shift (the transferable
   part), read against the packaging method.
5. **The transferable lesson** — one honest, positive "here is what to try on your channel."

**Scope trim (founder-approved):** **drop** Kallaway's ManyChat/comment-to-DM funnel and
offer/non-offer monetization-pillar layers for v1. They are pro-creator and largely
irrelevant to a service-business owner. Keep the packaging-transferable core.

**Data path — extends the yt-dlp driver (see below). VERIFIED EMPIRICALLY 2026-07-12.**
A breakout timeline needs a whole channel's video history, which the single-video deepener
does not provide and Firecrawl cannot reliably pull deep. Uses a `yt-dlp` channel
`--flat-playlist` dump — keyless, local, no account. **What the flat dump actually returns
(tested):** `view_count` (a *rounded* display figure, e.g. `27000`) and `playlist_index`
(reverse-chronological order). It does **NOT** return `upload_date` or `timestamp` — every
date field is null in flat mode. So the design uses **upload order as the x-axis and time
proxy**, never a calendar date, and a **rolling-by-count trailing baseline** (median of the
previous N videos in order), never a date-window baseline. Exact dates, if ever needed for
labelling around the inflection, cost one per-video network call each and are fetched only
for that handful — never for the whole channel. Firecrawl remains the default surface read;
the channel dump is this skill's specific need.

**Engine — a reimplemented deterministic helper.** This is the one place in-reasoning math
is unreliable over 100+ videos (which is exactly why Kallaway scripted it), so it earns a
script here — distinct from Workstream B. The helper:
- Parses the flat dump into `[{index, title, view_count}]`, oldest→newest (reverse the
  `playlist_index`). **Skips entries with `view_count: null`** (Shorts/live/members-only)
  and treats view counts as rounded/directional, not exact.
- Computes each video's outlier multiple = views ÷ a **rolling trailing-window baseline by
  video count** (median of the previous N in order). A rolling baseline means steady channel
  growth reads as ~1x throughout, so the scan finds packaging step-changes, not the growth
  trend.
- Detects the breakout inflection on `log1p(outlier)` with a **rank-based** two-sample
  statistic (Mann-Whitney U), not a difference-of-means — a mean statistic is *not* robust to
  a lone brand-deal spike, which would defeat the whole point; a rank test is. Requires a
  **minimum segment length of k consecutive videos** on each side, so a one-video spike can
  never register as a durable step (this is also what cleanly separates deliverable #3's
  spike vs step). Returns the trigger video + pre/post era **medians** (robust, matching the
  detection statistic).
- Pure Python stdlib, deterministic, no network. **Reimplemented from the documented method,
  in our own code** — not Kallaway's `.py`.
- Location: alongside the yt-dlp driver (e.g. `drivers/yt-dlp/` helpers) or a skill-local
  `scripts/` dir — final placement decided in the plan, consistent with how `studio/*` and
  existing skills structure code.

**Skill manifest (decided, not left to the implementer):** `requires_driver: yt-dlp` — the
channel dump is this skill's **mandatory** core data path, not an optional deepener as in
`research-my-channel`, so `none` would understate it. Still keyless: `yt-dlp` is
`kind: local` (not a connected kind), so it passes `check-connectors` and
`check-onboarding-binding` without an activation path. Also set `requires_credential: none`,
`function_slot: research`, `data_path: fetch_rest`. Description ≤ 400 chars
(`check-surface-budget`); passes `lint-skill`, `check-doctrine-voice`,
`registry-generator --check`, `export-capabilities --check`.

---

## yt-dlp driver expansion

`drivers/yt-dlp/README.md` today documents a **single-video** transcript/comments deepener.
This adds a **channel-history** use: a `--flat-playlist` dump of a channel's videos returning
**view counts and reverse-chronological order (no dates in flat mode)**, for the breakout
timeline. Update the README to document the new use, state the no-dates boundary plainly (so
it never claims a capability the tool lacks), and keep the honest boundary (still
`kind: local`, keyless, read-only; Firecrawl remains the default surface read). No new driver
kind; no activation path.

**Manifest verification (plan-time, not blocking):** confirm at lint time that
`tools/manifest.py` accepts `data_path: fetch_rest` for a `kind: local`-driver skill; if
`local` is the truer value for a skill whose data comes from a local binary invocation rather
than a hosted REST read, use that instead. Decide against the linter, not by copying
`research-my-channel` blindly.

---

## Inventory / doctrine updates (BOS standard)

- **Discovery surface** — add a `knowledge/starter-projects.md` row for `break-down-a-channel`
  under the market group (keyless-tagged, outcome-led, skill-id in backticks), mirroring the
  youtube-studio Phase-1 pattern. Without this row the skill exists but is undiscoverable in
  onboarding — a gap the live dogfood would hit. (There is **no root `CLAUDE.md`** in the BOS
  repo — verified; the real inventory/routing homes are `starter-projects.md`,
  `kernel/registry.json`, and `docs/CAPABILITIES.md`.)
- `kernel/registry.json` + `docs/CAPABILITIES.md` — regenerate via `registry-generator.py`
  and `export-capabilities.py` so the new skill and any regrouping land in the registry + tree.
- `distribution-method.md` and `youtube-packaging-method.md` consumer lists updated to name
  the new consumers/anchors.
- **Source-note credit to Kallaway** added where the bullseye lands in `distribution-method.md`
  (that file already carries one) **and** newly to `youtube-packaging-method.md`, since
  Workstream B ports Kallaway's specific "views ÷ trailing average" outlier-score definition
  and that file currently carries no source note.

## Validation (the pass bar)

**CI-order gates (all must pass):**
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
Plus a scripted **Sonnet dogfood** of the enriched skills and the new skill (the standard
BOS pass bar for reasoning-heavy skills), and offline fixture tests for the breakout helper:
(a) a **parse test** whose fixture includes a `view_count: null` entry (Shorts/live) to prove
the parser skips it and tolerates rounded counts, and (b) a **detection test** with a
deterministic ordered series → asserted inflection index, plus a lone-spike series that must
*not* register as a durable step (guards the rank-based + min-segment robustness).

**LIVE dogfood (founder-required acceptance gate):** after build + CI + Sonnet dogfood, run
the whole cycle **end-to-end on real, fresh YouTube data, framed for the AI BOS channel** —
our own channel as the subject. Concretely: pull a real channel history via `yt-dlp`, run
`break-down-a-channel` on a live outlier-heavy channel in our space, and exercise the
Bullseye + computed-outlier enrichments in a real `build-social-strategy` / `research-my-channel`
run aimed at the AI BOS channel. The cycle is not done until this live run produces a genuine,
correct, useful read on current data — not a fixture, not a replay.

## Out of scope (v1)

- TikTok / Instagram data (yt-dlp is YouTube; the others are hard and ToS-grey, keyless).
- The ManyChat/funnel-monetization teardown layer (trimmed above).
- Any Sandcastles integration or paid data source.
- An interactive HTML teardown report (v1 ships the markdown read; a rendered report can
  follow if the markdown proves its worth).

## Settled decisions

1. Scope = all three (2 enrichments + new skill). ✅
2. Outlier scoring = in-reasoning for the research read; a reimplemented deterministic engine
   only for the deep teardown. ✅
3. `break-down-a-channel` is a standalone youtube-studio skill, not a mode of
   `research-my-channel`. ✅
4. Funnel/monetization layer dropped from the teardown for v1. ✅
5. No Kallaway source verbatim in the public repo; methods reimplemented + credited. ✅
6. Live end-to-end dogfood on the AI BOS channel is the final acceptance gate. ✅
7. **The teardown is order-based, not date-based** — `yt-dlp --flat-playlist` returns view
   counts + reverse-chron order but no dates (verified 2026-07-12), so upload order is the
   x-axis and the baseline rolls by video count. Detection is rank-based (Mann-Whitney) with
   a minimum segment length, not a mean statistic. ✅ (Revised after spec review.)
8. New skill declares `requires_driver: yt-dlp` (mandatory core, still keyless kind local),
   not `none`. ✅ (Revised after spec review.)
9. The ring axis is named **"audience spread"**, never a second "mix"; posts carry both a
   content-type tag and a ring tag that compose. ✅ (Revised after spec review.)

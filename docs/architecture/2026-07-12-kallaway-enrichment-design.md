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

**Anti-collision note (critical):** `build-social-strategy` Step 3 part 4 already owns a
**content mix** on the *content-type* axis (educational / proof / promo / behind-the-scenes).
The 3/1/1 is a **different axis — audience proximity**. Every anchor must present them as
two orthogonal axes ("what the post is *about*" vs "who the post is *aimed at*"), never
overwrite or blur the existing type-mix.

**Inline anchors (tight, per the shared-rules doctrine — referenced-only rules get missed
on Sonnet):**
- `skills/build-social-strategy/SKILL.md` — Step 3, alongside the existing content mix:
  a short anchor introducing the audience-ring mix as the second axis, pointing to the
  distribution-method section as the owner.
- `skills/plan-my-content/SKILL.md` — the dated calendar allocates the batch across rings
  per 3/1/1, tagging each planned post with its ring.
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
- **Interpretation bands** (directional): `< 1x` under-performer, `~1-2x` solid,
  `2-5x` real outlier, `5x+` breakout — study hardest.
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
1. **Outlier-score timeline** — every video by publish date (x) vs outlier multiple (y),
   the inflection and any spike cluster marked. The spine of the story.
2. **The breakout inflection** — the video where the channel's rolling performance
   step-changed upward (or "no durable step — a launch spike that reverted").
3. **Spike vs durable step** — did it level up, or fire one hit and mean-revert?
4. **What changed** at the inflection — topic / format / packaging shift (the transferable
   part), read against the packaging method.
5. **The transferable lesson** — one honest, positive "here is what to try on your channel."

**Scope trim (founder-approved):** **drop** Kallaway's ManyChat/comment-to-DM funnel and
offer/non-offer monetization-pillar layers for v1. They are pro-creator and largely
irrelevant to a service-business owner. Keep the packaging-transferable core.

**Data path — extends the yt-dlp driver (see below).** A breakout timeline needs a whole
channel's video history (publish dates + view counts), which the single-video deepener does
not provide and Firecrawl cannot reliably pull deep. Uses a `yt-dlp` channel `--flat-playlist`
dump. Keyless, local, no account. Firecrawl remains the default for the surface read; the
channel dump is this skill's specific need.

**Engine — a reimplemented deterministic helper.** This is the one place in-reasoning math
is unreliable over 100+ videos (which is exactly why Kallaway scripted it), so it earns a
script here — distinct from Workstream B. The helper:
- Computes each video's outlier multiple (views ÷ trailing baseline) from the channel dump.
- Detects the breakout inflection via a step-change scan on `log1p(outlier)` (a difference-
  of-means / t-style score across candidate splits, upward shifts only — so one paid/brand
  spike cannot hijack the result), returning the trigger video + pre/post era medians.
- Pure Python stdlib, deterministic, no network. **Reimplemented from the documented method,
  in our own code** — not Kallaway's `.py`.
- Location: alongside the yt-dlp driver (e.g. `drivers/yt-dlp/` helpers) or a skill-local
  `scripts/` dir — final placement decided in the plan, consistent with how `studio/*` and
  existing skills structure code.

**Skill manifest constraints (from the codebase):** description ≤ 400 chars
(`check-surface-budget`), keyless-clean (not `needs_connection`), passes `lint-skill`,
`check-doctrine-voice`, `registry-generator --check`, `export-capabilities --check`.

---

## yt-dlp driver expansion

`drivers/yt-dlp/README.md` today documents a **single-video** transcript/comments deepener.
This adds a **channel-history** use: `--flat-playlist`-style dump of a channel's videos with
publish dates and view counts, for the breakout timeline. Update the README to document the
new use and keep the honest boundary (still `kind: local`, keyless, read-only; Firecrawl
remains the default surface read). No new driver kind; no activation path.

---

## Inventory / doctrine updates (BOS standard)

- `CLAUDE.md` (BOS root) — add `break-down-a-channel` to the youtube-studio inventory + routing.
- `docs/CAPABILITIES.md` / capability tree — regenerate via `export-capabilities.py` so the
  new skill and any regrouping land in the tree.
- `distribution-method.md` and `youtube-packaging-method.md` consumer lists updated to name
  the new consumers/anchors.
- Source-note credit to Kallaway added where the bullseye lands (matching distribution-method).

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
BOS pass bar for reasoning-heavy skills), and an offline fixture test for the breakout
helper (deterministic input → asserted inflection).

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

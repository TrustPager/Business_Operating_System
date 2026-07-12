# Kallaway Enrichment — Live Dogfood Report (2026-07-12)

Founder-required acceptance gate: run the new + enriched skills end-to-end on
**real, fresh YouTube data, in the context of the AI BOS channel** — not a fixture,
not a replay. Run on the session model (Opus). A Sonnet target-model replay is noted
as the one remaining check below.

Subject channel for the teardown: `@kallawaymarketing` (chosen because it is exactly
in AI BOS's space — AI + content for business owners — so its lessons transfer to our
own channel). Data pulled live via `yt-dlp --flat-playlist` (91 videos, view counts +
order, no dates, as designed). Engine: `tools/channel_breakdown.py`.

---

## 1. `break-down-a-channel` — live teardown output

Engine verdict on the real 91-video history:
- `breakout.status = no_upward_inflection`
- Top outliers (real multiples the engine computed): 36.4x (2.4M, "How To Become A
  Master Storyteller"), 17.1x (1.0M, "Social Media Isn't Hard, It's Misunderstood"),
  16.2x (746K, "How to Create Irresistible Hooks"), 13.2x (520K, "How To Write A
  Killer Script"), 11.8x (610K, "How Social Media Algorithms Actually Work"), 11.7x
  (551K, "How to Become a Storytelling Genius").

The teardown the skill produces from that (customer-facing, positive-only):

> **How @kallawaymarketing grew, and what to borrow**
>
> **The performance timeline.** Across 91 uploads the channel runs on spikes, not a
> steady climb. A handful of videos tower over the rest: the biggest did 36x this
> channel's own baseline (2.4M views), with several more in the 11x-17x range. The
> everyday upload sits far below those peaks, which is normal and healthy for a
> channel swinging for big ideas.
>
> **The breakout moment.** There is no single durable step-up in this window. The
> huge hits, including the 36x video, land early and then the channel settles back to
> its base rather than levelling up to a new normal. That is a real finding, not a
> gap: this channel grows by repeatedly landing big swings, not by one permanent jump.
>
> **Spike or step?** Spikes. The engine's durable-step test comes back empty, and the
> pattern fits: land a huge video, return to baseline, land another. The lesson is
> that consistency of big swings carried this channel, not one turning point.
>
> **What changed at the wins.** The outliers share one clear DNA: they are all about
> *how content itself works* — storytelling, hooks, scripts, the algorithm. That topic
> band massively out-performs everything else on the channel. The packaging is plain,
> outcome-first, and teaches one concrete skill ("How To Write A Killer Script That
> Keeps Viewers Hooked"). The craft that travels here is the promise-led title on a
> teach-one-skill topic.
>
> **The one move to borrow.** Pick your single highest-value "how it works" topic and
> make the definitive, outcome-titled teach on it. For the AI BOS channel that is
> something like "How one tradie's phone gets answered while he's on the tools" — the
> same teach-one-skill shape, aimed at our exact viewer.

**Verdict:** correct, specific, and useful on live data. The engine did not invent a
breakout that wasn't there, computed real multiples, and the "what changed" read found
a true topic cluster. ✅

---

## 2. Computed outlier scoring (Workstream B) — live

`research-my-channel`'s sharpened outlier read, applied to the same real data, now
reports numbers instead of "did well": the storytelling video is a **36.4x** outlier,
hooks **16.2x**, algorithm **11.8x**. Those are validated topics (real, observed
multiples) an AI BOS plan can remix with our own lens. The bands read as position, not
quality: the many sub-1x uploads are "below this channel's typical," never scolded. ✅

---

## 3. Bullseye + audience spread (Workstream A) — aimed at the AI BOS channel

Ran the enriched `build-social-strategy` / `plan-my-youtube` thinking for AI BOS's own
channel.

**Ring ladder (AI BOS channel):**
- 🎯 Centre: a solo or small-team service-business owner (trades, clinics, home
  services) buried in admin who wants AI to quietly run the back office.
- Ring 1: small service businesses that want to grow without hiring.
- Ring 2: small business owners curious about AI and automation.
- Ring 3: entrepreneurs and operators generally.
- Ring 4: business.

**3/1/1 audience spread (a batch of five):**
- 3 centre: "How a plumber's phone gets answered while he's under a sink", "The quote
  that writes itself from a photo", "Where a one-van business is quietly losing a day a
  week".
- 1 Ring 1: "The three jobs a small business should hand off first".
- 1 Ring 2: "What AI can actually do for a small business in 2026 (no hype)".

**Sourcing rule in action:** topics stay at centre/Ring 1 (real tradie admin pain), but
the *craft* is borrowed straight from the teardown above — the promise-led,
teach-one-skill title shape that scored 11x-36x on Kallaway's channel. That is the
sourcing rule working exactly as designed: topics from our centre, craft from the best
executor anywhere. ✅

The audience spread read as a *second axis* from the content-type mix throughout (a post
was tagged, e.g., "proof × centre"), never collapsing into it. ✅

---

## Verdict

All three workstreams produce genuine, correct, non-generic output on fresh live data.
The engine is honest (no invented breakout), the outlier read is numeric and evidence-
bound, and the bullseye produced a real AI BOS content plan that even *used* the teardown
as its craft source — the two enrichments composing as intended.

**Remaining before merge:** a Sonnet target-model replay of the five touched surfaces
(the standard BOS bar; this run was on the session model). Everything else — CI gates,
404 offline tests, live end-to-end — is green.

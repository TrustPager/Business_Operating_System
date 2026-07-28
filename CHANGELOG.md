# Changelog

All notable changes to Business Operating System are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added

- **`tools/api.py` — one command to call any TrustPager API endpoint.** A fixed, catalog-backed surface over the full REST API (by resource id or raw path, GET/POST/PATCH). Reads are free; writes require `--confirm`, are journaled, and surface a queued-for-approval (HTTP 202) response cleanly. This is the escape hatch for anything the named tools/skills don't wrap, and it sidesteps the MCP tool-manifest ranking limit entirely: a fixed command can never be "ranked out" of a chat client the way a deferred MCP tool can.
- **`tools/find-capability.py` — "can TrustPager do X?" search.** Ranks every endpoint in the public catalog against a plain-English goal and prints the matches with a ready-to-run `api.py` command for each. Turns endpoint discovery from "scan 60+ resources" into "ask, get the command." Read-only (reads only the public catalog).

- **The content-skill contract, enforced (`knowledge/content-rules.md` + `tools/lint-skill.py`).** Two obligations a skill now declares in its own frontmatter: a skill that writes customer-facing copy names its voice source inline, and a skill flagged with the new `engagement_copy` key routes `knowledge/storytelling-method.md` for the attention craft. `content-rules.md` gained the one home for where voice lives (`marketing-strategy/<BrandName>/voice.md` for marketing copy, `knowledge/communication-voice.md` for service messages, and `brand/brand.json` for identity only). Fifteen customer-facing skills that named no voice source were retrofitted, so the pack lints clean.
- **The findability check (`knowledge/youtube-packaging-method.md`).** A keyless, YouTube-specific way to learn which words viewers actually type, from YouTube's own public suggestion endpoint, seeded from several angles and clustered by intent. `research-my-channel` now reads the clusters into its research file and `plan-my-youtube` leads how-to and evergreen titles with real demand, keeping the owner's own outcome framing for the hook and description. Browse and story videos deliberately skip it.
- **A publish gate in `package-my-video`.** A pack reads `ready to upload` only after nine checks pass (title chosen, thumbnail and video present, chapters and a single call to action, no invented links, tags, one last content-guardrails read), plus two the owner confirms: the video ends on its rendered ending, and the audio is at a shipping level. A failing check is named plainly in the readme and holds the pack.
- **`knowledge/youtube-launch-method.md` — the launch layer of the YouTube floor.** Three things `youtube-packaging-method.md` deliberately does not cover: the branch tree and the idea filter (pillars are branches carrying unlimited leaves within the rings, and an idea earns a slot only by answering a real question on one of them), the MVP effort pyramid (idea, packaging, script, film, edit) written for BOTH production modes because the filmed and generated effort curves differ completely, and first-run discipline (about twenty videos, a one-week cap per video, no stockpiling, read against your own baseline). `plan-my-youtube`, `script-my-video`, `package-my-video`, and `what-worked` reference it.
- **The transformation and the point of view, as brand fields.** Two things a channel needs before it can be packaged, and neither existed anywhere in the pack: a transformation naming a specific audience and a specific outcome, and a point of view (the belief the owner stated about what their industry has wrong, plus what that belief argues against, aimed at a belief, a tactic, or an ideology and never at a person). They are brand-level, so they live in the brand strategy home beside `voice.md` and `build-brand-strategy` writes them in both modes; `knowledge/marketing-strategy-method.md` Layer 3 owns the definitions and the boundaries against the promise and against a case study's before→after. `plan-my-youtube` gained a gate that reads them first, tops up only a missing field, captures and writes them when the brand home has none, and never re-interviews an owner who already did positioning. What the point of view argues against is recorded exactly as the owner states it: how sharp it is, is their choice.
- **`knowledge/conversation-method.md` — how a long discovery conversation is actually run.** Six rules with one home, four of them new to the pack: each of its four consumers declares a backstop as a number a run can count, and takes a graceful exit at it (reflect, deliver with the gaps named, stop) instead of running away; an *engaged* owner whose answer goes vague or one-word gets two or three concrete options to react to rather than the same open question again, which is the fix for a non-technical owner who cannot answer an open question about their own business; an insight is reflected back before every next ask and a turn that is only "Great!" is banned; every field of an artifact is re-read against its own pass/fail test before it ships (grounding, not polish, so a staged rough co-build still ships its guesses labelled); a stuck owner gets three ways in offered once, then a labelled best guess rather than a grinding; and a pasted prior output switches the run to refinement without ever flipping the cold-start gate. `start-here`, `learn-my-business`, `grill-me-on-this-decision`, and `build-my-voice` reference it, and the copies they each carried inline were trimmed to pointers.
- **`what-worked` — read your OWN channel after a publish.** The mirror of `break-down-a-channel`: same keyless local `yt-dlp` dump and the same deterministic engine, pointed at the owner's own uploads. It scores each upload against the owner's own trailing baseline, walks the effort pyramid from the top to name what was different about the ones that moved (idea, packaging, script, film, edit, mode-aware at the film and edit rungs), and closes on one concrete next video: keep the style, change the job. Never manufactures a cause for an on-baseline video.
- **The cross-channel outlier board (`research-my-channel` Step 4b).** `research-my-channel` Step 1 reads outliers by eye, from whatever counts a page happened to show. The board is the tool-scored wide version: the same keyless local `yt-dlp` flat dump and the same deterministic engine the two teardown skills run, fanned across up to ten niche channels at once, scoring every recent upload against its own channel's baseline and ranking the pooled multiples (never raw views) into one shortlist of the angles the niche is already rewarding. Offered as a plain choice, never a prerequisite, with its limits stated up front rather than buried: rounded view counts, no dates in flat mode, no baseline on the oldest rows of a truncated pull. Every scored row is kept and carries its channel; which ideas actually earn a slot stays `plan-my-youtube`'s call, once its pillars are set.

### Changed

- **Comment-mining is standard research, not an upsell.** `yt-dlp` is keyless and reaches YouTube comment threads across the platform; what cannot reach them is the web-SCRAPE read specifically (they load through a separate client-side call). The pack had collapsed that into "the keyless read cannot reach comments", which demoted the richest demand signal on the floor to an optional ask. `research-my-channel` now checks once, silently, whether `yt-dlp` is already installed: if it is, comments mine as part of the standard read with no asking; if it is not, the read still completes from search and public discussion and the one-time install is recommended rather than the capability being described as out of reach. Full transcripts and the cross-channel outlier board stay genuinely optional. `drivers/yt-dlp/README.md` and `plan-my-youtube` carry the same correction.
- **The franchise loop-out is produced, not just prescribed.** `youtube-packaging-method.md` told owners to end a franchise video on its own metaphor left visibly incomplete, but no step on the floor produced one, and `package-my-video`'s publish gate asked the owner to confirm it anyway. `script-my-video`'s `cta` beat and `design-my-scenes` now carry the guidance (the latter naming honestly that no dedicated visual device exists yet). The gate splits in two: a truncated render still holds the pack, and the loop-out is advisory only, because how an owner ends their own video is their call.
- **`<slug>.script.json` now has a stated bridge between its three read points.** `script-my-video` writes it into the owner's own workspace; `voice-my-video`, `design-my-scenes`, and both render studios read from their own studio-local `data/`. Each intake step now says how the file gets there (copy it in, or `studio/video`'s existing `--script <path>` flag), instead of assuming it already had.
- **The unlicensed video path is now a real option instead of dormant code.** `studio/video` (a headless browser plus ffmpeg, no licence obligation of any kind) sat in the repo unreachable: no skill mentioned it, so an owner who did not want the render engine's licence obligation had no path to it. `make-my-video` now offers it, but only when the owner raises the licence, and states the trade plainly: it renders branded text-on-screen video from the script plus the timing sidecar, and it does not do voiceover, talking-head overlay, captions, or the product-demo add-on. Its beat-role label is now derived rather than hardcoded, so a role added to the script schema (as `subscribe` was) renders sensibly here without a matching change: that drift had already happened silently, unnoticed because nothing drives or tests this studio.
- **The render engine's licence is a one-time courtesy note, not a gate (founder ruling).** Remotion is free for an individual or a small team and a company of four or more needs to buy its own licence. `make-my-video` mentions that once, on the first render, in plain language, and never again. Nothing checks it, nothing blocks a render, no acknowledgement is recorded, and BOS never asserts a licence status on the owner's behalf: it is their call and their responsibility. The position is recorded in `studio/motion/CLAUDE.md` so no future change builds the gate that was originally designed.

- **Video scripting reads the owner's real writing voice.** `script-my-video` and `voice-my-video` were the only content skills pointed at `brand/brand.json` for voice, a file whose schema carries none, so every video was scripted in a voice the skill never read. Both now read `marketing-strategy/<BrandName>/voice.md` (identity still from `brand.json`), with a plain fallback when no voice doc exists. `make-my-video` and `make-product-demo` carried the same mistake and were corrected too.
- **The video hook is scored, not felt.** The six hook power words in `knowledge/storytelling-method.md` were documented as a fallback for when a hook would not land, so hooks got written by ear and never checked. They are now the scoring gate: `script-my-video` quotes the words carrying each of the four core pieces before a hook is locked, re-scores after any structural rewrite, and shows the owner the score.
- **The two meanings of "packaging" are routed, not conflated.** `package-my-video` is collation (a finished video into a publish-ready folder); ideation is `plan-my-youtube` and the owner's title pick now happens in `script-my-video`, which offers three to five options and scripts against the one they choose. The routing table lives in `knowledge/youtube-packaging-method.md`.
- **`make-thumbnail` resolves its studio and brand explicitly** when a working directory holds more than one thumbnail studio or brand kit, instead of rendering into the first one it finds.
- **Onboarding (`/start-here`) redirected to consultation-first (founder-ruled 2026-07-03).** The Day-1 win is now the collaborative consultative conversation (reflect understanding, draw out the goal and the owner's own theory of the blocker, then think alongside them with the reasoning shown), decided by an engagement gauge, rather than a built artifact handed over on the spot. Any build is deferred to a recommendation-with-alternatives at the end; a terse owner still gets a fast tangible win. The assistant now mirrors the owner's register. See `docs/architecture/2026-07-03-collaborative-consultation-design.md`.

---

## [1.0.0] - 2026-06-29

### Initial public release

**Keyless day-one floor**

The following categories of skill work with no account, no key, and no setup beyond cloning the repo (or installing the plugin):

- **Pricing and money:** price a job from costs and margin, produce a priced breakdown any customer can interrogate.
- **Proposals:** write a finished proposal from a brain-dump; the pricing engine feeds the numbers directly.
- **Research:** competitor reads, market context, and business-model analysis from a URL or a plain description.
- **Documents:** draft policies, contracts, and operating procedures from a description of what you need.
- **Content and brand:** build a brand brief, author copy in your voice, draft social content and email sequences.
- **Decisions and strategy:** think through a decision with structured reasoning; build a one-page operating strategy.

Every floor skill uses `requires_driver: none`, `requires_credential: none`, and `data_path: reasoning_only` in its manifest. No outbound calls are made.

**Conversational cross-platform install**

Install by telling Claude to get the Business Operating System (it clones the repo and runs setup for you), or clone and run `python tools/setup.py` yourself. The `tools/setup.py` installer and `tools/check-install.py` health-check run the same way on Mac, Windows, and Linux. The `~/.claude/bos-run.py` signpost launcher means skills work from any directory without hardcoded paths.

**TrustPager as the optional connected layer**

Operators who connect a TrustPager workspace unlock CRM-backed skills: morning briefings, follow-up radars, pipeline management, lead triage, automated reporting, invoice tracking, form and document workflows, and voice-call tooling. The connected layer is additive; the keyless floor is unchanged for operators who do not connect.

**Platform-agnostic design**

BOS is not a TrustPager product. It is an open-source Claude Code plugin that works on any platform and connects to TrustPager as one optional driver. The manifest schema (`requires_driver`, `requires_credential`, `data_path`) is designed to accommodate other drivers and integrations. Contributions of new keyless skills and new drivers are welcome.

**Testing and gates**

An offline test suite (`BOS_OFFLINE=1 python -m unittest discover -s tests`), a secret scanner (`tools/check-no-secrets.py`), manifest linting (`tools/lint-skill.py`), and freshness checks for the registry and capabilities doc run on every push and pull request via GitHub Actions. No real API key ever enters CI or the test environment.

**License:** MIT

---

[1.0.0]: https://github.com/TrustPager/Business_Operating_System/releases/tag/v1.0.0

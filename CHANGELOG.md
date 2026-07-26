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

### Changed

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

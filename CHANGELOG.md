# Changelog

All notable changes to Business Operating System are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow [Semantic Versioning](https://semver.org/).

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

A 310-test offline suite (`BOS_OFFLINE=1 python -m unittest discover -s tests`), a secret scanner (`tools/check-no-secrets.py`), manifest linting (`tools/lint-skill.py`), and freshness checks for the registry and capabilities doc run on every push and pull request via GitHub Actions. No real API key ever enters CI or the test environment.

**License:** MIT

---

[1.0.0]: https://github.com/TrustPager/Business_Operating_System/releases/tag/v1.0.0

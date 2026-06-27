# The Floor Roster — definition-of-done for the keyless floor

> **Founder-ruled (2026-06-27, see [D9](founder-decisions.md)):** the floor is **defined by the set of tangible first-win projects we offer a brand-new owner**, not by whatever skills happen to exist. This roster IS the floor spec. A win is "on the floor" only when it is genuinely keyless (zero accounts, zero files), produces a real artifact, is finishable in one sitting, and is token-frugal. TrustPager enrichment is always the *connected deepener*, never a floor requirement.
>
> **Bound to reality:** every app this roster (and the onboarding surface) names must pass the onboarding-binding check — it exists in `kernel/registry.json`, is `status: active`, and any app offered as a keyless win is `requires_credential: none` with a keyless driver (`none`/`markitdown`/`render`/`firecrawl`). See [the guardrail](#the-guardrail-anti-recurrence). The registry is the single source of truth; this roster is curation on top of it.

## The first-win roster (≈19 wins)

Status legend: ✅ ships keyless today · 🟡 partly built · 🔁 needs decouple from TrustPager · 🆕 not built.

| # | First win (the artifact the owner walks away with) | Vertical fit | Relief | Required components | Status |
|---|---|---|---|---|---|
| 1 | A line-itemed quote from a photo + 30s voice note | Trades | win-work | quote-from-photo, price-my-work, doc-lib-set | 🔁 |
| 2 | A defensible price for one common job (margin shown) | Trades, mfg, consulting | get-paid | price-my-work, doc-lib-set | 🆕 |
| 3 | An on-brand proposal/SOW in the owner's voice (.docx) | Consulting, property | win-work | write-a-proposal, price-my-work, build-brand-strategy, doc-lib-set | 🆕 |
| 4 | A one-page read of one competitor's site | All; consulting/property | decide-well | research-a-competitor, firecrawl-keyless | 🆕 |
| 5 | A pre-meeting brief + 3 sharp questions | Consulting, broking, property | win-work | research-before-call, research-a-competitor, firecrawl-keyless | 🆕 |
| 6 | A 2-week multi-channel content plan + first captions | Consulting, wellness, hospitality | market | plan-my-content, write-post-copy, build-brand-strategy | 🆕 |
| 7 | One on-brand graphic + caption for this week | Wellness, hospitality, property | market | make-social-post, write-post-copy, build-brand-strategy | 🟡 |
| 8 | A 15-30s branded promo video | Hospitality, wellness, property | market | make-brand-video, creative-render-driver, build-brand-strategy | 🆕 |
| 9 | A publish-ready folder (brief + caption + asset) | All running socials | save-time | assemble-content-pack, make-social-post, write-post-copy | 🟡 |
| 10 | Any messy file → clean usable data | Broking, mfg, admin-heavy | save-time | extract-document, compare-documents, markitdown-driver | ✅ |
| 11 | An intake/fact-find pack read in seconds + what's-missing | Broking, allied health | save-time | extract-document, template-from-document, markitdown-driver | ✅ |
| 12 | A structured spreadsheet that runs one slice | Trades, mfg, property | save-time | build-spreadsheet, doc-lib-set | 🔁 |
| 13 | A scattered customer list → one clean normalized file | All pre-CRM | save-time | import-from-anywhere, markitdown-driver, build-spreadsheet, doc-lib-set | 🔁 |
| 14 | A call/meeting → clean summary + actions (paste a transcript) | Consulting, allied health | save-time | transcript-summary, markitdown-driver | 🔁 |
| 15 | A grilling on the owner's next big decision | All; consulting/trades | decide-well | grill-me-on-this-decision, write-prompt | 🆕 |
| 16 | A job ad + screening questions in the owner's voice | Trades, hospitality, wellness | save-time | write-a-job-ad, onboard-team-member, build-brand-strategy | 🟡 |
| 17 | On-brand policies + FAQ answers (deposits, cancellations, privacy) | Wellness, hospitality, allied health | market | write-a-policy, build-brand-strategy | 🆕 |
| 18 | The brand written down → brand.json that reskins everything | All | market | build-brand-strategy, build-customer-voice, brand-my-workspace | 🔁 |
| 19 | Throw-me-any-file structuring into a reusable template spec | Broking, mfg, allied health | save-time | template-from-document, markitdown-driver | ✅ |

## Derived build set — priority by unlock count

Build in this order (each "unlocks" = number of roster wins it enables). Reasoning-only/local wins are `BOS_OFFLINE`-green; Firecrawl + video are network/heavy and noted.

| Order | Component | Unlocks | Effort | Keyless path | Note |
|---|---|---|---|---|---|
| 1 | **doc-lib-set** driver (openpyxl/python-docx/pdfplumber/reportlab) | 5 | small | local | Keyless WRITE side: .xlsx/.docx/PDF. Thin Bash wrappers mirroring `markitdown_convert.py`. MIT/BSD/MPL clean. OCRmyPDF gated behind preflight; python-pptx on-demand. |
| 2 | **markitdown-driver** (promote to first-class) | 4 | trivial | local | Keyless READ side. `tools/markitdown_convert.py` exists; name it a `requires_credential:none` driver. Unblocks transcript-summary + import keyless paths. |
| 3 | **price-my-work** | 3 | small | reasoning_only | Top win-work/get-paid job + the keyless pricing fallback quote-from-photo & write-a-proposal need. |
| 4 | **build-customer-voice** (decouple) | 3 | small | reasoning_only/local | Documented prerequisite of floor `build-brand-strategy`; accept owner-pasted notes instead of `mcp list_transcripts`. |
| 5 | **write-post-copy** | 3 | small | reasoning_only | Studios render only the on-image headline; nothing drafts the caption/body. Positive-only enforced. |
| 6 | **grill-me-on-this-decision** | 1 | small | reasoning_only | Locked floor app (D6); the reasoning anchor. Routed by start-here Step 6. |
| 7 | **write-a-proposal** | 1 | medium | reasoning_only + doc-lib-set | Closes price→proposal. Becomes the live signing template on connect. Positive-only. |
| 8 | **plan-my-content** | 1 | medium | reasoning_only | THE missing hinge: content-pillars → dated multi-channel plan. Horizon clamped to 1-2 weeks. |
| 9 | **build-spreadsheet** (decouple) | 2 | small | local | Keyless standalone .xlsx via doc-lib-set; live workspace sheet is the deepener. |
| 10 | **import-from-anywhere** (decouple) | 1 | medium | local | MarkItDown read → normalized local file; CRM seed only on connect. The natural connect on-ramp. |
| 11 | **transcript-summary** (fix: keyless paste/local path) | 1 | small | local | Correctness gap: floor's zero-account claim isn't literally true until this lands. |
| 12 | **quote-from-photo** (decouple: drop list_products) | 1 | trivial | reasoning_only | Lean on price-my-work for pricing; remove the contradictory `mcp` tool. |
| 13 | **write-a-job-ad** | 1 | small | reasoning_only | Completes the team cluster's before-hire gap. Positive-only. |
| 14 | **write-a-policy** | 1 | small | reasoning_only | High day-one demand; pre-feeds build-knowledge-base-from-docs on connect. Positive-only. |
| 15 | **assemble-content-pack** | 1 | small | local | Publish-ready terminus of the MAKE cluster; pure orchestration, no generation. |
| 16 | **research-a-competitor** | 2 | medium | fetch_rest (Firecrawl) | Floor's KNOW dimension. **Network — not `BOS_OFFLINE`-green; harness mocks/skips the fetch.** scrape/search/interact only, never crawl/map/agent/extract. |
| 17 | **research-before-call** | 1 | medium | fetch_rest (Firecrawl) | Builds on research-a-competitor. Network. |
| 18 | **firecrawl-keyless** driver (wire scrape/search/interact) | 2 | trivial | fetch_rest | Already active in `.mcp.json`. Wired not vendored. Manifest must NOT advertise crawl/map/agent/extract as keyless. |
| — | **make-brand-video + creative-render-driver** | 1 | large | local render | Founder priority but **P6** (Remotion bridge, cross-repo, pin-on, heavy install). Genericise the RVS promo layer first. Voiceover OFF to stay keyless. |

## The guardrail (anti-recurrence)

The drift that shipped in P3 (onboarding routing to apps that don't exist / aren't keyless) is structurally prevented by binding the onboarding surface to the registry, both ways:

1. **CI binding check** (`tools/check-onboarding-binding.py`, run after `registry-generator`): every app-id referenced in `skills/start-here`, `skills/whats-possible`, and `knowledge/starter-projects.md` (A) is an active registry key; (B) anything offered as a keyless win is `requires_credential:none` + keyless driver; (C) no `requires_credential:none` skill body contains a TrustPager tool/script/curl.
2. **Manifest rule:** a `requires_credential:none` skill may not declare `mcp__` in `uses_tools`.
3. **Runtime binding:** `start-here` may only *route* to apps in the registry keyless set. The curated library proposes vertical-tailored projects; the registry validates; CI enforces.

This makes "onboarding only ever offers real, keyless wins" a checked invariant, not a convention.

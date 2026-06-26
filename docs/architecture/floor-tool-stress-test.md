All claims in the verdicts are verified against the repo. The verdicts are internally consistent with the locked docs. Now I'll produce the final ruling, re-challenging the two INCLUDEs for redundancy against each other and against native CC.

The two survivors are `firecrawl-keyless` (KNOW) and `doc-lib-set` (PAPERWORK & DATA + MONEY write-side). They occupy different clusters and the read/write boundary is clean (MarkItDown+pypdf = read/fill-AcroForm; doc-lib-set = generate + flat-fill + OCR + precision-extract). No overlap to collapse between the two. The only genuine overlap risk is *within* doc-lib-set (python-pptx low ICP value; OCRmyPDF heavy install) and *within* firecrawl (search vs native WebSearch) — both already scoped correctly in the verdicts.

---

# BOS Floor Tool Stress-Test — Final Ruling

Lead architect's verdict on the adopt-to-harden layer. Two candidates survive; eight are cut. I re-challenged both survivors for redundancy against each other and against native Claude Code — they hold, with two scope-clamps applied.

## 1. Included — the adopt-to-harden layer

| Tool | Keyless? | License | Where it plugs into the floor | Integration cost | The one-line reason it earned its place |
|---|---|---|---|---|---|
| **firecrawl-keyless** — Firecrawl hosted MCP, **scope: `scrape`/`search`/`interact` only** | Yes (these 3 tools) | Wrapper MIT / engine AGPL-3.0 → **consume-as-service, never vendor engine** | KNOW cluster — the keyless web-data driver behind `research-a-competitor` + `research-before-call` (default-on) and `scan-the-market` + `enrich-this-lead` (pinnable) | S — already in `.mcp.json`, nothing to build to keep | It is the *only* thing that makes the KNOW dimension exist at zero accounts: ranked-search-with-full-page-content + robust batch JS scraping that native WebSearch (US-only, snippets) and WebFetch (single-URL, no-JS) genuinely lack. |
| **doc-lib-set** — openpyxl, python-docx, pdfplumber, reportlab (+ OCRmyPDF, python-pptx) | Yes (local `pip`) | MIT / BSD / MPL-2.0 — all vendor-clean | PAPERWORK & DATA + MONEY clusters — the keyless **write side**: powers `build-spreadsheet` (standalone .xlsx), `write-a-proposal` (.docx), `price-my-work`, and flat-PDF fill / precision extraction for `update-pdf` | S — thin Bash wrappers mirroring `tools/markitdown_convert.py` | It is the missing *generate* half of the doc loop: MarkItDown+pypdf only read and fill AcroForms — nothing in the floor can emit a native xlsx/docx, OCR a scanned PDF, or fill a flat PDF, so multiple already-locked MUST apps are broken promises without it. |

**Scope-clamps carried into the implementation plan (these are the conditions of inclusion, not optional):**
- **firecrawl-keyless:** the floor manifest must wire only `scrape`/`search`/`interact` and must NOT advertise `crawl`/`map`/`agent`/`extract` as keyless — those need a free `FIRECRAWL_API_KEY` and belong in the opt-in tier.
- **doc-lib-set:** `openpyxl + python-docx + pdfplumber + reportlab` are default-on core. **OCRmyPDF is default-on but gated behind a one-time Tesseract+Ghostscript preflight** (same friction model as MarkItDown[all]). **python-pptx is adopt-on-demand, NOT default-installed** — low ICP value for trades/broking/allied-health/consulting.

## 2. Cut

| Tool | The single reason |
|---|---|
| **playwright-mcp** | Redundant-with-native-CC in the strongest form — it *is* the in-session environment (`mcp__playwright__*` is live right now). "Including" a tool the floor already possesses is a no-op; the research skills should *call* it as the hard-case fallback, not adopt it. |
| **mcp-video-ffmpeg** (KyaniteLabs) | Redundant-with-native-CC — stateless FFmpeg, which Bash runs directly; the CLI/lib-vs-MCP rule forbids importing a 119-tool MCP to wrap ~4 verbs. Immature (57★, effectively solo) → blueprint a thin BOS-owned FFmpeg post-production skill instead. |
| **duckduckgo-mcp** | Redundant — adds a *third* keyless search path (native WebSearch + Firecrawl `search` + DDG) into one cluster; the AU-geo gap it claims is already closed by Firecrawl's global `search`. Fragile unofficial-HTML endpoint → blueprint the one-file fallback, don't depend. |
| **marketing:\* plugin** | Redundant-with-native-CC (generic copy/strategy the session model already does) **and** license-unclean (first-party, not MIT-vendorable). Routing floor content apps to it would strip brand spine, evidence, AU framing, and the positive-only language rule — degrading the MAKE cluster, not completing it. |
| **claude-seo** | Not-keyless at the load-bearing tier (rankings/volume/backlinks sit behind PageSpeed/GSC/GA4/DataForSEO keys) **and** grab-bag — SEO opens a *new* search-visibility cluster the floor never scoped, the opposite of cheaply completing an existing one. Blueprint its parallel-sub-agent + GEO/AEO structure if a keyed SEO app is ever built. |
| **bamboohr-blueprint** | Redundant — the "one driver + many plain-language role-apps" pattern is already proven in-repo and the scan already names the firecrawl-* skills as its canonical blueprint; BambooHR's flat single-API US-centric shape under-models BOS's known ≥3-driver-kind reality. Also fails the floor bar (account+key). |
| **video-toolkit-blueprint** (wilwaldon) | Immature / nothing-to-adopt — verified to be a README-only link directory (3 commits, no skill code); the lifecycle lesson it's credited with belongs to a *different* repo and is already harvested into `floor-completion-plan.md` §4. A README cannot be a floor tool. |
| **au-gov-data** (Fair Work MAPD + ABN Lookup) | Not-keyless — both require free-registration credentials (FWC API key, ABR GUID), failing the gating bar of this test and the `BOS_OFFLINE` zero-credential DoD. It deepens an app the floor already ships keylessly (reasoning + versioned ATO/Fair-Work constants) → opt-in driver, not floor. |

## 3. Adopt vs blueprint

**Adopt (vendor/wire directly):**
- **doc-lib-set** — vendored as thin Bash-invoked wrappers in `tools/`, named as the "write side" in `document-tools-method.md`. Fully ours to ship (MIT/BSD/MPL).
- **firecrawl-keyless** — *wired, not vendored.* We consume the hosted endpoint (already in `.mcp.json`); the AGPL-3.0 engine is never copied into the MIT tree. The boundary is the integration, and it's already correct.

**Blueprint only (lift the pattern, from the CUT pile):**
- **mcp-video-ffmpeg** → blueprint a `make-vertical`/`add-subtitles`/`make-a-gif` skill over Bash+FFmpeg, brand.json-aware (the MAKE post-production gap Remotion doesn't cover).
- **claude-seo** → if/when a keyed SEO app is built, model its parallel-sub-agent + GEO/AEO + local-SEO structure.
- **bamboohr-blueprint** / **duckduckgo-mcp** / **video-toolkit-blueprint** → lessons already banked in the scan; no new action.
- **au-gov-data** → adopt later as opt-in MONEY/people-ops drivers; meanwhile bake a versioned ATO/Fair-Work constants file into the floor so the keyless pay app is award-aware with no live call.

## 4. Coherence check

**Does the included set complete clusters without overlap? Yes — and the two survivors do not touch each other.**

- **No overlap between survivors.** firecrawl-keyless lives entirely in KNOW (inbound web data); doc-lib-set lives entirely in PAPERWORK & DATA + MONEY (outbound file generation). Different clusters, different verbs, zero shared surface. Nothing to collapse between them.
- **No overlap with already-adopted floor tools.** The read/write boundary is clean: MarkItDown (read any file) + pypdf (read/fill AcroForm) own *ingest*; doc-lib-set owns *generate + flat-fill + OCR + precision-extract*. pdfplumber's table extraction is a genuine delta over MarkItDown's lossy markdown, not a duplicate.
- **The one redundancy I re-challenged and cleared:** Firecrawl `search` vs native WebSearch. They overlap on "find sources," but WebSearch is US-only snippets and Firecrawl returns ranked results *with* full-page markdown in one call — a real capability delta for an AU ICP. Kept, because the cluster genuinely lacks the global-ranked-with-content path; the *redundant third* path (DDG) was correctly cut.
- **Internal-overlap risks neutralised by the scope-clamps:** python-pptx (low ICP overlap with docx/xlsx) demoted to on-demand; OCRmyPDF's heavy install gated behind preflight so it never bloats the default load.
- **Gaps the survivors leave (by design, not omission):** generative media (no honestly-keyless path), live calendar/comms send, AU pay-correctness live data — all correctly past the floor as opt-in drivers. The MAKE *video* gap is closed by building the already-designed Remotion bridge, not by any candidate here. No survivor leaves a cluster half-open.

**TrustPager check:** neither survivor depends on or is justified by TrustPager. Both stand alone at zero accounts. The verdicts that leaned on TrustPager-native equivalents (marketing:*, claude-seo, e-sign) were all in the CUT pile and cut for *other* reasons too — the floor does not rely on TrustPager for anything in this layer.

## 5. Net effect on the floor build

Adopting these two — and only these two — hardens the two clusters that were literally broken at zero accounts: KNOW gains its only keyless outbound-intelligence engine (firecrawl `scrape`/`search`/`interact`), and PAPERWORK/MONEY gains the keyless *generate* half of the document loop (xlsx/docx out, flat-PDF fill, OCR, precision extraction), turning already-locked MUST apps like `build-spreadsheet`, `write-a-proposal`, and `price-my-work` from promises into working paths. We no longer build a web-scraper, a search backend, or a document-generation engine ourselves — those are now assembly over mature, license-clean dependencies, leaving the genuine build surface as the kernel/driver-abstraction, the reasoning floor apps, and the plain-language app layer. Everything else was cut as redundant-with-native-CC (playwright, FFmpeg-MCP, DDG, marketing:*), not-keyless (claude-seo, au-gov-data), or immature/already-blueprinted (bamboohr, video-toolkit). **The floor stands fully with zero TrustPager: both survivors are platform-agnostic, keyless at their adopted scope, and complete their clusters without leaning on the connect-tier.**
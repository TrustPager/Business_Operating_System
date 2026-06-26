Important corrections surfaced: Carbone MCP is real and official but Apache-2.0 with only 3 stars (not the maturity the native lens implied), and it needs a Carbone API key (free tier 100 renders/mo) — it is NOT keyless, contradicting the native lens's "covered/keyless" framing. The document floor is actually better served by the keyless Python libraries the document domain scan verified. That's a meaningful flag.

I have enough verified anchors plus the two detailed domain scans (finance, documents) that already did first-hand verification. I also have the TrustPager tool list in-context, which directly confirms native AI creative/SEO/document/comms tools the domain scans largely missed. Let me write the consolidated plan.

# BOS — Native Capability + Ecosystem: Decisive Build Plan

**Scope note:** This consolidates the native Claude Code lens + six domain scans into one build decision per capability. Where the high-level "native lens" JSON conflicts with a hands-on domain scan, I trust the domain scan (it verified repos first-hand) and flag the conflict. I re-verified four load-bearing claims live this session (Xero AU-payroll exclusion, Firecrawl license/keyless, Carbone MCP, and read the connected TrustPager tool surface) — corrections are in §6.

A theme the native-lens JSON missed and the tool surface makes undeniable: **TrustPager is not just the CRM driver — it already ships native AI tools for image gen/edit/upscale, document/form generation, e-sign, SEO (full suite), reputation/reviews, referrals, lead-gen, email/SMS/WhatsApp, scheduling, invoicing, and voice.** For a TrustPager-connected owner, BOS's "driver" layer for half these domains is *already connected*. The build job is the **floor (zero-account)** and a thin **driver-abstraction interface**, not reimplementing functions TrustPager or native CC already perform.

---

## 1. Don't build it — Claude Code already does

Delete these from the build list. Each is native, keyless, zero-account.

| Capability | Native CC feature (the specific thing) |
|---|---|
| Search the web + read a public page | `WebSearch` (keyless, ranked results; US-only) + `WebFetch` (URL→markdown, 15-min cache). Covers the entire floor "find sources / read a page" loop. *(domain-1 native)* |
| Browser interaction / JS-rendered / authenticated scraping, screenshots | `playwright` MCP already in-session (Apache-2.0, keyless): navigate, click, fill, screenshot, evaluate JS. *(domain-1)* |
| All marketing **drafting** — ad copy, captions, emails, nurture sequences, SEO titles/meta/outlines, campaign plans, competitive briefs, review-reply drafts, referral scripts | First-party `marketing:*` skills already loaded (draft-content, content-creation, campaign-plan, brand-review, competitive-brief, performance-report, seo-audit, email-sequence). *(domain-5)* |
| Read any text file; create/edit text files (.md/.csv/.json/.html) | `Read` (incl. born-digital PDFs + images) / `Write` / `Edit`. *(domain-4)* |
| Run any local lib/CLI (the real doc/finance/creative engine) | `Bash` — drives MarkItDown, pypdf, openpyxl, FFmpeg, ImageMagick. These are "capabilities" only because Bash runs them. *(domain-4)* |
| Brand graphics / logos / social-card layouts / diagrams (vector) | Native SVG authoring (powers `show_widget`). Keyless. *(domain-2)* |
| Render HTML/Vite → PNG/MP4 | `playwright` screenshot/record — validates the Vite/Puppeteer studio approach as native-adjacent. *(domain-2)* |
| Recurring cadences (weekly post draft, nurture send, weekly report, review nudges) | `scheduled-tasks` MCP + `schedule` skill. No third-party scheduler needed to *trigger* work. *(domain-5)* |
| Site analytics / CRO / funnels / session recordings | `clarity-finalpiece` MCP + `microsoft-clarity:*` skills (token already configured). *(domain-5)* |
| Audit trail / versioning / secrets | Git history + `.env` + the installed pre-push secret-scan hook. *(native lens)* |
| All financial **math** — GST (10%, ÷11), super (12% SG from 1 Jul 2025), PAYG estimates, margin, Simpler-BAS G1/1A/1B mapping | Pure model reasoning. Do **not** adopt a "GST library" (npm/pip ones are India/NZ GST or toys). *(domain-3)* |
| All people-ops **thinking** — roster optimization, timesheet math, leave balances, review drafting, hiring scorecards | Reasoning + docx/xlsx artifacts + connected Google Calendar MCP. *(domain-4)* |

**Native, but account-gated (already connected in this workspace — use, don't build):**
- **Scheduling/calendar:** Google Calendar MCP (`adaba9ef-…`: list/create/update events, suggest_time). *(domain-6)*
- **CRM + far more:** TrustPager MCP (`2ab2957b-…`). Confirmed tool surface includes `ai_generate_image / ai_edit_image / ai_upscale_image / ai_generate_speech / ai_generate_music`, `ai_generate_document / ai_generate_form / ai_fill_form / render_document_template / convert_form_submission_to_pdf`, `send_for_signing` (+ envelope lifecycle), full `seo_*` suite (keyword research, SERP, backlinks, site/local audit, AI-visibility, competitor gap), `create_reputation_review / request_reputation_review / get_reputation_stats`, `create_referral / referral_link / leaderboard`, `lead_gen_search / enrich`, `send_email / send_sms / send_whatsapp`, `create_invoice / payment_link / sync_receivables`. **This is the single biggest "don't build" in the whole plan.**

---

## 2. Adopt — include directly

Keyless, license-clean (MIT/BSD/Apache-2.0/MPL), well-reviewed. These complete the **floor**; account-gated ones are opt-in drivers.

| Tool | Source | Keyless? | License | Replaces in our build |
|---|---|---|---|---|
| **MarkItDown** (already adopted) | github.com/microsoft/markitdown | Yes | MIT | "Read any file" ingest — keep as-is. *(domain-4)* |
| **pypdf** (already adopted) | pypi.org/project/pypdf | Yes | BSD-3 | Fillable-PDF (AcroForm) read/fill/merge — keep `/update-pdf`. *(domain-4)* |
| **openpyxl** | pypi.org/project/openpyxl | Yes | MIT | xlsx generation/edit. Use the **library directly** — do NOT build on Anthropic's proprietary xlsx skill. *(domain-4)* |
| **python-docx** | pypi.org/project/python-docx | Yes | MIT | docx generation (quotes, agreements, onboarding letters). Library, not the proprietary docx skill. *(domain-4)* |
| **pdfplumber** | pypi.org/project/pdfplumber | Yes | MIT | Precision table/line-item extraction + flat-form field mapping (invoice/statement parsing). *(domain-4)* |
| **OCRmyPDF** | github.com/ocrmypdf/ocrmypdf | Yes | MPL-2.0 | Scanned/photographed PDFs (lender forms) → searchable. Closes the one real read-gap for the AU trades/broking ICP. Needs Tesseract+Ghostscript (one-time install, same model as MarkItDown). *(domain-4)* |
| **python-pptx** | pypi.org/project/python-pptx | Yes | MIT | pptx generation. Adopt-on-demand (low ICP need). *(domain-4)* |
| **`playwright` MCP** | github.com/microsoft/playwright-mcp | Yes | Apache-2.0 | Hard/JS/authenticated scraping + visual competitive snapshots. Already in-session. *(domain-1)* |
| **Firecrawl hosted MCP** (already adopted) | mcp.firecrawl.dev/v2/mcp · github.com/firecrawl/firecrawl-mcp-server | Partial (scrape/search/interact keyless; crawl/map/agent/extract = free key) | MIT (wrapper) | Default web-data driver. Keep. **Engine is AGPL-3.0 — consume as a service, never vendor engine code.** ✓ re-verified this session. *(domain-1)* |
| **Anthropic `marketing:*` plugin** | claude.com/plugins/marketing | Yes | First-party | The marketing "apps" baseline — route to it; don't rebuild copy/strategy. *(domain-5)* |

**Adopt as opt-in DRIVERS (account-gated — past the floor):**

| Tool | Source | License | Replaces |
|---|---|---|---|
| **Xero MCP** (official) | github.com/XeroAPI/xero-mcp-server | MIT | Deepest AU accounting driver (GST/BAS-aware). ✓ re-verified MIT/315★. **⚠ Payroll tools NZ/UK ONLY — not AU** (verified quote in §6). Use for accounting; AU payroll handled elsewhere. *(domain-3)* |
| **Stripe hosted MCP** | docs.stripe.com/mcp | (hosted) | Lowest-friction "get paid" — payment links/invoices for owners with no accounting suite. *(domain-3)* |
| **Resend MCP** (official) | github.com/resend/resend-mcp | MIT | Floor-friendly email/nurture **send** driver (broadcasts+contacts+templates). Default for owners with no ESP. *(domain-5)* |
| **Pipeboard Meta-Ads MCP** | github.com/pipeboard-co/meta-ads-mcp | BSL-1.1 → Apache-2029 | The Meta paid-ads driver (write w/ confirmation pattern). Free to *call*; can't resell as hosted. ICP is Meta-heavy → prioritise. *(domain-5)* |
| **Google Ads MCP** (official) | github.com/googleads/google-ads-mcp | Apache-2.0 | Google-ads reporting/analysis driver. Below Meta for this ICP. *(domain-5)* |
| **DataForSEO MCP** (official) | github.com/dataforseo/mcp-server-typescript | Apache-2.0 | Paid SEO/reviews **data** driver behind the floor SEO app (pay-as-you-go, no subscription floor). Prefer over Ahrefs for the ICP. *(domain-5)* |
| **Deel MCP** (official) | developer.deel.com/mcp | (vendor) | Adopt-as-is *only* when a client already runs Deel (contractors/EOR). Read-write OAuth. *(domain-4)* |
| **QuickBooks Online MCP** (official) | github.com/intuit/quickbooks-online-mcp-server | Apache-2.0 | Alt accounting driver (#2 in AU). Same driver interface as Xero. *(domain-3)* |

---

## 3. Blueprint — model our own on these (one design lesson each)

| Tool / source | License | The one lesson to lift |
|---|---|---|
| **Fair Work Modern Awards Pay DB API** — fwc.gov.au/.../modern-awards-pay-database-api | Gov (free, registration) | **Build an "AU pay-correctness" floor app over it.** This is the highest-leverage AU-specific finding: award rates/penalties/overtime as authoritative data, no payroll vendor. *(domain-4)* |
| **ATO published rates** (SG 12%, PAYG tables, MCB $62,500, GST 10%) | Gov data | Ship a **versioned "AU constants" data file**, updated each FY (bake in Payday Super from 1 Jul 2026). Model does the math. *(domain-3)* |
| **Beancount** — github.com/beancount/beancount | **GPL-2.0** | The data model for a **keyless plaintext double-entry "books" floor app**. **Blueprint only — GPL-2.0; do not vendor.** Model our own MIT ledger on its proven structure. *(domain-3)* |
| **ABN Lookup web service** — abr.business.gov.au | Gov (free GUID) | Thin **ABN/GST-registration verify driver** before invoicing — decides whether to charge/claim GST. *(domain-3)* |
| **Exa MCP** company/competitor/people tools — exa.ai/mcp | MIT (wrapper); keyed | Shape of an **enrichment app**: entity in → structured profile + competitors + news out. Offer as optional BYOK driver. *(domain-1)* |
| **PDL / Apollo APIs** (best free enrichment tiers) | Commercial APIs | **Build a thin multi-provider BYOK enrichment driver** — don't depend on the dead "Lead Enrichment MCP" Apify actor (≈1 user). The pattern is sound; the package isn't. *(domain-1)* |
| **claude-seo** — github.com/AgriciDaniel/claude-seo (9.8k★) | MIT | Parallel sub-agent + GEO/AEO + local-SEO/GBP structure for the **SEO app**. (Could adopt, but its *structure* is the higher-leverage take; depth-tier above native `seo-audit`.) *(domain-5)* |
| **acalder BambooHR MCP** (74 tools + 30 role skills) | MIT | **"One driver + many role skills"** = exactly BOS's driver+apps shape. Mine the structure, don't ship it (US-leaning, low adoption). *(domain-4)* |
| **wilwaldon Claude-Code-Video-Toolkit** (53★) | MIT | Reference for a **lifecycle-phased creative skill** (plan→assets→review→audio→edit→render) — validates the Remotion-bridge approach. *(domain-2)* |
| **KyaniteLabs/mcp-video** (Apache-2.0, keyless) | Apache-2.0 | Best **blueprint (or low-risk adopt) for a keyless FFmpeg post-production driver** — GIF/vertical/social repurposing + subtitle burn, the layer Remotion doesn't cover. *(domain-2)* |
| **Anthropic document skills** (docx/pdf/pptx/xlsx) | **Proprietary** | The **unpack→edit-XML→repack** pattern + LibreOffice-headless for render/recalc/convert. **Read to learn, build from scratch on the OSS libs.** ⚠ License forbids derivatives/redistribution (see §6). *(domain-4)* |
| **KeyPay/Employment Hero + Deputy REST APIs** | Commercial | If/when a client runs them, **blueprint a thin AU payroll/rostering driver** (award interpretation, STP, super, rosters) over the REST API rather than depend on Zapier MCP middlemen. *(domain-4)* |
| **DuckDuckGo MCP** (1.3k★, MIT, keyless) | MIT | Single-file pattern for a **keyless SERP fallback** (global, vs WebSearch US-only) — model it, don't add it as a dependency. *(domain-1)* |

---

## 4. Build (genuine gaps no one fills well)

These are where BOS earns its keep. Everything else is assembly.

1. **The KERNEL + driver-abstraction interface.** No one ships a "swap Xero/QBO/Stripe/TrustPager behind one `accounting` interface; swap Resend/Klaviyo/AC behind one `email` interface" abstraction. **This is the product** — the one thing that's genuinely ours. TrustPager must be the *default implementation* of most interfaces, with the OSS/keyed tools as swap-ins.
2. **The zero-account FLOOR apps (reasoning + OSS libs only).** Simpler-BAS prep (G1/1A/1B), GST/super/PAYG calc off versioned ATO constants, 13-week cash-flow forecast (xlsx), expense categorisation, aged-receivables aging; keyless books ledger (Beancount-model); rostering/timesheet/leave (xlsx + Calendar + Fair Work rates); JD/interview-kit/onboarding/review/handbook (skill-pack-modeled, **AU-framed**: Fair Work, NES, super, positive-language rule).
3. **AU pay-correctness app** over the Fair Work API + ATO constants — award-correct pay, the thing US-centric tools (Gusto/Rippling/BambooHR) get wrong for this ICP.
4. **Multi-provider BYOK enrichment driver** (PDL/Apollo) — genuine gap, no maintained keyless option.
5. **Plain-language "app" surface over every driver.** The existing `firecrawl-*` slash-skills are the proven blueprint: owners say "enrich this lead" / "prep my BAS," not "call MCP tool X." This *framing layer* is part of the product, not the drivers.
6. **A human-approval gate on every write-driver call** (invoices, payments, ledger postings, live sends) — mirror the workspace pattern that already correctly blocked an unrequested live invoice read. Generic MCP servers don't enforce this; BOS must.

**Explicitly NOT build:** generative pixel models (adopt fal.ai BYOK), CRM (TrustPager), copy/strategy generators (native marketing plugin), GST libraries, an SBR2/ATO direct-lodgement engine (DSP accreditation — incompatible with an MIT floor; **prepare figures, owner lodges via Xero/QBO/myGov**).

---

## 5. Per-capability verdict table

| Need | Native? | Verdict | The specific pick |
|---|---|---|---|
| Web search + read public page | **Yes** (WebSearch/WebFetch) | Native | Delete from build |
| JS/auth scraping, screenshots | Yes (playwright MCP) | Adopt | `playwright` MCP (Apache-2.0, in-session) |
| Web-data driver | Partial (Firecrawl) | Adopt (have it) | Firecrawl hosted MCP (MIT wrapper; AGPL engine = service only) |
| Semantic search / competitive intel | No | Blueprint/opt-in | Exa MCP (BYOK) + public FB Ads Library tool surface |
| Lead enrichment | No | **Build** (blueprint pattern) | BYOK driver over PDL/Apollo |
| Brand vector graphics | Yes (SVG) | Native | Delete |
| Generative images/video/music | No | Adopt (BYOK) | fal.ai MCP primary; TrustPager `ai_generate_image` native when connected |
| Branded/deterministic video+GIF | Yes (Remotion sibling repo) | Blueprint | Remotion bridge (⚠ source-available, paid @4+ staff — external tool, never vendor) |
| Video post-production / GIF/social | No (FFmpeg via Bash) | Adopt/blueprint | KyaniteLabs/mcp-video (Apache-2.0, keyless) |
| Design assets (owner-editable) | Connector present | Adopt | Canva connector (`plugin_marketing_canva`, free plan works) |
| Read any file | Partial | Adopt (have it) | MarkItDown (MIT) |
| Fill PDFs (AcroForm) | No | Adopt (have it) | pypdf (BSD-3) |
| Fill flat PDFs / generate PDF | No | Watch/on-demand | reportlab (BSD — ⚠ confirm license before bundling) |
| Generate docx/xlsx/pptx | No | Adopt libs | python-docx / openpyxl / python-pptx (MIT) |
| Precision extraction | No | Adopt | pdfplumber (MIT) |
| OCR scanned PDFs | No | Adopt | OCRmyPDF (MPL-2.0) |
| E-signing | Yes (TrustPager) | Native | TrustPager `send_for_signing`; DocuSign MCP = watch-only |
| Invoicing / receivables | Yes (TrustPager) | Native + drivers | TrustPager default; Stripe/Xero/QBO swap-ins |
| Accounting (Xero/QBO) | No | Adopt (opt-in) | Xero MCP (MIT) primary; QBO MCP (Apache-2.0) alt |
| AU GST/BAS prep | **Yes** (reasoning) | **Build floor app** | Simpler-BAS G1/1A/1B + ATO constants; owner lodges via Xero/myGov |
| AU super/PAYG calc | **Yes** (reasoning) | **Build floor app** | Versioned ATO constants (SG 12%, Payday Super 1 Jul 2026) |
| Cash-flow forecast / budgeting | Yes (xlsx) | Build floor app | 13-week rolling model |
| Keyless books ledger | No | **Build** (Beancount-model) | MIT plaintext ledger, GST-tagged |
| ABN/GST verify | No | Blueprint driver | ABN Lookup (free GUID) |
| Rostering / timesheets / leave | Yes (reasoning+cal) | Build floor; opt-in driver | xlsx + Calendar + Fair Work rates; Deputy/KeyPay blueprint |
| AU pay-correctness | No | **Build** | Fair Work Pay DB API app |
| Payroll run (AU) | No | Blueprint driver | KeyPay/Employment Hero REST (⚠ Xero MCP payroll excludes AU) |
| Payroll (contractor/EOR) | No | Adopt opt-in | Deel MCP |
| Hiring/onboarding/perf docs | Yes (reasoning) | Build floor (blueprint) | AU-framed skills (corporate-skill-pack model) |
| Social posting | No | Adopt | Postiz (self-host, AGPL — run as service) default; Ayrshare hosted fallback |
| Paid ads (Meta) | No | Adopt | Pipeboard Meta-Ads MCP (BSL-1.1) |
| Paid ads (Google) | No | Adopt | Google Ads MCP (Apache-2.0) |
| Email/nurture **send** | Partial (TrustPager) | Native + adopt | TrustPager native; Resend MCP (MIT) for no-ESP; AC/Klaviyo BYO |
| Marketing **drafting** | **Yes** (marketing:*) | Native | Delete — route to plugin |
| SEO data | Yes (TrustPager `seo_*`) | Native + adopt | TrustPager SEO suite native; DataForSEO (Apache-2.0) deeper data; claude-seo structure |
| Reputation/reviews | Yes (TrustPager) | Native | TrustPager `reputation_*`; route GBP via Ayrshare if needed |
| Referrals | Yes (TrustPager) | Native | TrustPager `referral_*` |
| Scheduling/calendar | Yes (connected) | Native | Google Calendar MCP |
| CRM | Yes (TrustPager) | Native | TrustPager — do not research alternatives |
| Recurring automation | Yes | Native | scheduled-tasks MCP + schedule skill |
| Audit/secrets | Yes | Native | Git + .env + pre-push hook |
| Driver-abstraction kernel | No | **Build** | The product |
| Plain-language app layer | No | **Build** | firecrawl-skill pattern over every driver |
| Write-action approval gate | No | **Build** | Mirror existing block-on-write pattern |

---

## 6. Risks & flags

**Verified-wrong / corrected this session (honesty rule):**
- **Carbone MCP — native-lens claim is misleading.** Native lens calls it "covered / production-ready / handles 100+ formats" implying a keyless doc-generation answer. Verified: it is official but **Apache-2.0, only 3 stars, and requires a Carbone API key (free 100 renders/mo) — NOT keyless.** No domain scan corroborated it. **Do not adopt for the floor; the keyless Python libs (python-docx/openpyxl/pypdf, all verified) are the correct doc-generation floor.** Carbone is at best a watch-only hosted convenience driver. (github.com/carboneio/carbone-mcp)
- **Xero MCP payroll excludes Australia.** Re-verified live: README states *"To use Payroll-specific queries, the region should be either NZ or UK."* The native-lens "Finance: covered incl. superannuation via Xero" and its invented "Lightning Ventures Xero fork (AU/NZ, Payday Super)" are **wrong/unverified** — I could not confirm any "Lightning Ventures" fork exists; **treat as fabricated until proven.** AU payroll/super must come from the Fair Work API + ATO constants + (blueprinted) KeyPay, not Xero MCP.

**Unverified findings in the source material — do not rely on without checking (flagged, not adopted):**
- Native-lens-only names with no domain-scan corroboration and no source I could confirm: *Zernio, Socialync, Sequenzy, Money Forward MCP, Digits MCP, CrawlForge, SyncGTM Enrichment MCP, Check Payroll MCP, Outscraper MCP.* Several read as plausible-but-unconfirmed; the domain scans (which verified repos first-hand) did not list them. **Treat the native-lens "findings" with skepticism — that JSON asserted maturity it didn't verify.** The six domain scans are the trustworthy tier.
- Gusto consumer data-connector (403 on fetch) — domain-4 correctly flagged UNVERIFIED. Gusto is US-only regardless → skip.
- reportlab license (stated BSD from memory, not re-fetched) — **confirm on PyPI before bundling.** fpdf2 alternative is LGPL-3.0 (mild copyleft) — prefer reportlab if license-clean matters.
- Dead package: "Lead Enrichment MCP Server" (Apify, ~1 user) — verified to exist, **do not adopt**; blueprint the pattern only.

**License traps (MIT repo):**
- **AGPL-3.0:** Firecrawl *engine* (consume as hosted service only) · **Postiz** (run as separate self-hosted service the driver calls — never vendor source).
- **GPL-2.0:** Beancount — blueprint only, external tool, do not link/bundle.
- **Source-available / paid:** Remotion (paid @4+ employees — external tool, never vendor; document the boundary for adopters).
- **Proprietary:** Anthropic document skills — **forbid derivatives/redistribution** ("demonstration/educational only"). Usable at runtime inside CC; build BOS skills from scratch on the OSS libs.
- **BSL-1.1:** Pipeboard Meta-Ads (fine to call; can't resell as hosted product; converts Apache-2029).
- **Clean to vendor:** MIT (MarkItDown, openpyxl, python-docx, python-pptx, pdfplumber, Resend, claude-seo, Xero/QBO-Apache, DuckDuckGo, Exa/Tavily/Apify wrappers) · BSD (pypdf) · Apache-2.0 (playwright, KyaniteLabs/mcp-video, Google Ads, DataForSEO, QBO) · MPL-2.0 (OCRmyPDF — only changes to OCRmyPDF itself must be shared).

**Keyless-vs-key surprises:**
- Firecrawl: scrape/search/interact keyless; **crawl/map/agent/extract need a free key** — don't promise full Firecrawl on the floor.
- Fair Work + ABN Lookup: "keyless-ish" but **need free registration GUID/key** — low-friction, not zero-friction.
- Canva: free-plan login works, but **Resize=paid, Autofill/Brand Templates=Enterprise.**
- Every generative-media MCP (fal.ai/Replicate/Higgsfield) and every accounting/ads/SEO-data driver is **keyed** — all sit *past* the floor by design.

**Maintenance concerns:** single-maintainer / low-star repos to blueprint-not-depend: GBP review MCPs (solo, early), facebook-ads-library-mcp (39★), beanquery-mcp (experimental), Claude-Code-Video-Toolkit (53★), Ayrshare MCP wrapper (community over a paid API).

**Environment caveat across all six scans:** the MCP registry tools (`search_mcp_registry`, `list_connectors`, `suggest_connectors`) returned **empty for every query** this session — so *nothing* was registry-verified; everything rests on live GitHub/vendor/gov URLs. Re-confirm stars/licenses/versions at adoption time.

---

## 7. Net effect on the build

This scan **removes roughly half the planned build outright** and **de-risks most of the rest into assembly.** Web research, all marketing/SEO/reputation/referral drafting, scheduling, CRM, e-sign, generative media, and the entire document *read* path are native or already-connected (Claude Code + the loaded marketing plugin + the TrustPager and Google Calendar MCPs) — and the document *write* floor needs only four keyless, license-clean Python libraries we can adopt today. What's genuinely left to **build** is small and is the actual product: the **kernel + driver-abstraction interface**, the **zero-account floor apps** (AU GST/BAS/super/cash-flow + keyless books + rostering/people-ops), the **AU pay-correctness app** over the Fair Work API, a **BYOK enrichment driver**, the **plain-language app layer**, and a **write-approval gate**. The biggest landmine to design around is **Australian payroll** — the obvious driver (Xero MCP) explicitly excludes AU and the native lens's "covered" verdict (plus its invented Lightning Ventures fork) is not trustworthy; treat AU super/payroll as a build-and-blueprint problem, not an adopt.
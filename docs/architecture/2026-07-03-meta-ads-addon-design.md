# Meta Ads addon — plan-my-ads (floor) + run-my-ads (library), and the first connected-MCP driver

**Status:** Approved design (founder-approved 2026-07-03, decisions #1–#6),
revised 2026-07-03 after spec review (all blocker + major findings resolved). This
is the build spec for two new apps (`plan-my-ads`, `run-my-ads`), the first
`claude_mcp`-type driver (`meta-ads`), its connect walkthrough, a per-user ads
profile, and the layered spend-safety model. The method throughout is Evelyn
Weiss's, generalized off her Skool-specific workflow to any business shape.
Nothing in the kernel changes. `plan-my-ads` is a keyless floor win day one;
`run-my-ads` ships in-repo but stays dark until the owner connects their own Meta
Ads account.

---

## 1. Summary

Owners want ads that work, not an ads degree. This addon gives them two apps that
split cleanly along the plan/run seam already used elsewhere in the BOS:

- **`plan-my-ads`** is the thinking. Keyless, reasoning-only, works at zero
  accounts. It runs Evelyn Weiss's ad method as a live consultation and hands back
  one written **ad plan** — the objective to optimize for, the diagnostic offer
  ad, the creative brief, the six-part copy draft, the budget and KPIs, the
  scaling ladder, and the retargeting plan. It is useful even if the owner never
  connects Meta (it applies just as well to Google, TikTok, or a manual setup),
  and it **feeds** `run-my-ads`.
- **`run-my-ads`** is the doing. It connects to the owner's own Meta Ads account
  through the official Meta Ads MCP, runs Evelyn's pre-flight checks, and builds
  **paused** campaign, ad set, and ad shells to the plan. It never spends a cent:
  everything ships paused, every write is confirmed and journaled, and it never
  turns an ad on. The owner reviews in Ads Manager and switches it on themselves.

The `meta-ads` driver is the first of a new kind — a **connected OAuth MCP the
owner hosts**, not a keyed-REST adapter or a keyless hosted MCP. This addon
defines that reusable shape so every future connected tool (Google Ads, and the
like) drops in the same way.

This is the highest-stakes write surface in the BOS. The spend-safety model (§8)
is layered accordingly.

---

## 2. Goals and non-goals

### Goals

- Ship Evelyn Weiss's ad method as a keyless floor win (`plan-my-ads`) that any
  owner can run on Day 1 with no account and no key.
- Ship a connected companion (`run-my-ads`) that turns that plan into real,
  **paused** Meta campaign shells safely, over the owner's own OAuth connection.
- Define the reusable `claude_mcp` driver contract, using `meta-ads` as the first
  instance, so future connected tools cost no kernel change.
- Keep personalization in DATA, not in forked skill files: one central skill body
  for everyone, a per-user ads profile written by an init walkthrough.
- Make spend safety absolute: paused-by-construction, confirmed, journaled, and
  never activated by the BOS — including never setting a status field to ACTIVE.

### Non-goals (YAGNI)

- **No kernel change.** The driver is introduced purely as the `requires_driver`
  string on skills plus one small additive `run.py` journal-write branch (§8).
  `manifest.py`, `registry-generator.py`, and `kernel/*` need no edits.
- **No new library subsystem.** The D13 off-the-shelf library is decided but not
  built; `run-my-ads` is gated dark by the *existing* mechanism (a non-keyless
  `requires_driver` + registry activation/pinning), exactly as the TrustPager
  skills already are.
- **No ad activation, ever.** BOS creates paused shells and stops. It never calls
  `ads_activate_entity` and never sets a `status` field to ACTIVE via any tool
  (§8).
- **No file uploads to Meta** (the MCP cannot upload media). The owner adds real
  images, video, and final copy in Ads Manager.
- **No landing-page/VSL authoring here.** `plan-my-ads` points at the offer page
  the ad sends people to; authoring that page belongs to a site/offer skill.
- **No `requires_region`.** Neither ads skill sets it; ad-account currency comes
  from Meta directly, not from the BOS region.

### How this honors each non-negotiable

| Non-negotiable | How this design honors it |
|---|---|
| **Kernel unchanged when a driver/app is added** | The `meta-ads` driver is `requires_driver: meta-ads` (a free-form id, validated only as non-empty). No BOS mechanism reads a driver folder for a `claude_mcp` driver (§3): `manifest.py` and `registry-generator.py` never open `drivers/`, so the registry regenerates with zero generator edits. The only tooling delta is one additive branch in `tools/run.py` (journal-write, §8) — no `kernel/` change. |
| **Floor works at zero accounts and zero credentials** | `plan-my-ads` is `requires_driver: none`, `requires_credential: none`, `data_path: reasoning_only`. It runs to a finished ad plan with no network, no key, no tools — green under `BOS_OFFLINE`. |
| **Owners never see kernel/driver/app/MCP** | `connect.md` and both skill bodies are plain language ("connect your ad account", "I'll set it up paused"). The words kernel, driver, app, MCP never appear in owner-facing text. |
| **Token-frugal per turn (D10)** | `setup.py` does NOT register the Meta MCP (unlike keyless Firecrawl). It is connected on demand, and Claude Code defers its tool schemas — names only per turn until a tool is called. The connect heads-up reassures on exactly this. |
| **Anti-drift, one home per fact** | The connect detail (exact commands, the callback-port fallback) lives once in `drivers/meta-ads/connect.md`; §3d and `knowledge/connectors.md` both carry short pointers to it, never a restated procedure. The Evelyn method lives once in `plan-my-ads` (thinking) and once in `run-my-ads` (execution). Brand identity is read from `brand/brand.json`, never copied into the ads profile. The future-library-home fact is stated once (§7). |
| **Positive-only, method attributed to Evelyn Weiss** | All owner-facing copy is outcome-led (name the win first). The diagnostic internal vocabulary (flatline/heartbeat) is dev-facing only and never shown to the end customer. Both skill bodies attribute the method to Evelyn Weiss. |
| **MIT-clean** | No vendored code. The Meta MCP is the owner's own connection over OAuth; BOS ships only plain-language docs and skill bodies. |

---

## 3. The reusable `claude_mcp` driver contract [NEW]

Existing drivers come in shapes that split into two physical realities:

- **A driver folder exists** only for `trustpager` (a keyed-REST `DriverConfig`
  over `kernel.runtime.transport`, with `auth.py` + `catalog.py`) and the
  `regional/au` data pack.
- **No driver folder at all** for `firecrawl` (keyless hosted MCP, registered by
  `setup.py` straight into `~/.claude.json`), `markitdown`, `render`, and `doclib`
  — these exist purely as `requires_driver` manifest strings on skills.

`meta-ads` is the first "connect this OAuth MCP the owner hosts" driver. It defines
that shape, and it follows the **folderless** precedent, not the trustpager one.

**Defining property:** a `claude_mcp` driver has **no Python transport**. The
Claude Code client hosts the MCP; the owner connects it over OAuth; BOS skills
call the `mcp__<id>__*` tools directly. There is no `DriverConfig`, no `auth.py`,
no key to resolve. `drivers/__init__.py` already states "The kernel never imports a
driver" — a `claude_mcp` driver has nothing for the kernel to import anyway.

### 3a. What is actually load-bearing (and what is documentation)

For a `claude_mcp` driver, **no BOS mechanism reads a driver folder.** The only
load-bearing artifacts are exactly the ones firecrawl uses:

1. The **`requires_driver: meta-ads` string** on `run-my-ads`'s manifest (drives
   registry classification and the dark-gate, §7).
2. The **connect walkthrough** (`drivers/meta-ads/connect.md`) — read by the
   `run-my-ads` init and pointed at from the connectors card.
3. The **`## Meta Ads` card** in `knowledge/connectors.md` (§6f) — the catalog
   surface `connect-a-tool` and `whats-possible` read.

We DO ship a `drivers/meta-ads/` folder, but purely as the deliberate
reusable-shape reference doc for the next connected driver. Everything in it is
**non-enforced documentation**: nothing in `manifest.py`, `registry-generator.py`,
`lint-skill.py`, or the kernel opens it today. This is stated plainly so a builder
does not go hunting for a loader that does not exist.

```
drivers/meta-ads/
├── __init__.py            # declarative metadata — documentation only, NOT read by anything
├── OPERATING-CONTEXT.md   # source text run-my-ads init folds into ./CLAUDE.md (§3c)
├── connect.md             # the plain-language connect walkthrough (single home; §6e)
└── README.md              # documents the reusable claude_mcp driver shape [NEW]
```

Do **not** create `auth.py` or a `DriverConfig`. Do **not** add `meta-ads` to
`_KEYLESS_DRIVERS` in `check-onboarding-binding.py` — it is connected-tier, not
keyless.

### 3b. Driver manifest — `drivers/meta-ads/__init__.py` [NEW, documentation only]

Declarative metadata, offered as the template a future connected-MCP driver could
copy and as the machine-readable form of this spec's spend-safety facts.
**Nothing reads this file today** (there is no driver-metadata loader). It is not a
contract the runtime enforces; the real enforcement lives in the skill manifest,
the skill body, and the CI check (§8). Ship it as reference, labelled as such in
its own docstring.

```python
# drivers/meta-ads/__init__.py
"""Meta Ads driver — the first claude_mcp-type driver.

DOCUMENTATION ONLY. No BOS mechanism imports or reads this module today; there is
no driver-metadata loader. The load-bearing artifacts are the requires_driver
string on run-my-ads, connect.md, and the connectors.md card (see spec §3a). This
file records the reusable shape for the next connected-MCP driver (Google Ads,
etc.) and the machine-readable spend-safety facts a future loader could consume.

Unlike keyed-REST drivers (trustpager), a claude_mcp driver has NO Python
transport. The Claude Code client hosts the MCP (connected by the owner via
OAuth); BOS skills call the mcp__meta-ads__* tools directly. Method attributed to
Evelyn Weiss.
"""

DRIVER = {
    "id": "meta-ads",
    "kind": "claude_mcp",              # keyed_rest | keyless_mcp | local | data_pack | claude_mcp
    "display_name": "Meta Ads",
    "server_url": "https://mcp.facebook.com/ads",
    "tool_prefix": "mcp__meta-ads__",
    "connect_doc": "connect.md",
    "credential": "mcp",               # OAuth, no key paste
    "read_only_scope_first": True,     # grant the read-only scope tier first (§8)
    # Spend-safety hard lines (see §8). Documentation of intent; the live guard is
    # the CI check in tools/check-ads-safety.py, not this dict.
    "never_call": ["mcp__meta-ads__ads_activate_entity"],
    "never_set": {"mcp__meta-ads__ads_update_entity": ["status"]},
}
```

**The `claude_mcp` driver-manifest schema (the documented contract):**

| Field | Meaning |
|---|---|
| `id` | the `requires_driver` string skills reference |
| `kind` | `claude_mcp` for this class |
| `display_name` | plain-language name owners see |
| `server_url` | the hosted MCP endpoint the owner connects to |
| `tool_prefix` | the `mcp__<id>__` namespace all its tools share |
| `connect_doc` | the driver-owned connect walkthrough filename |
| `credential` | `mcp` (OAuth); never `key` for this class |
| `read_only_scope_first` | grant the read scope tier first for safety |
| `never_call` | tool names BOS must never invoke (spend/irreversible surface) |
| `never_set` | per-tool field names BOS must never write (e.g. `status` on `ads_update_entity` — the second, subtler activation path; §8) |

### 3c. `drivers/meta-ads/OPERATING-CONTEXT.md` outline [NEW]

Modeled on `drivers/trustpager/OPERATING-CONTEXT.md`. **`run-my-ads` init folds it
in itself** — it does NOT call `learn-my-business`. `learn-my-business` is
`requires_driver: trustpager` and its Step 2b hardcodes the trustpager path, so a
Meta-only owner never triggers it. `run-my-ads` init therefore implements its own
read-and-merge as independently-authored steps, reusing the SAME no-clobber
pattern Step 2b uses (read the source, show the diff, ask before overwriting; if
`./CLAUDE.md` already carries a Meta Ads section, merge, never clobber). Sections:

- **Header note** — "loaded into your profile only once you connect your Meta Ads
  account; until then none of this applies."
- **How the connection works** — it is the owner's own ad account over their
  sign-in; reads are free, so look around freely; creating anything is always
  paused and always confirmed first; we start on the read-only access tier and
  widen only when the owner is ready to launch.
- **What lives in the ad account** — ad accounts, Pages and Instagram accounts,
  the pixel/dataset that tracks conversions, campaigns → ad sets → ads, past ads
  and their results.
- **Things that change how you behave (spend safety)** — everything ships
  **paused**; every create is confirmed with the owner and journaled; the BOS
  **never** turns an ad on (`ads_activate_entity` is off-limits) and **never**
  sets a status field to ACTIVE on any edit; budgets are shown in the ad account's
  own currency; the owner activates in Ads Manager.
- **Tools you lean on** — the read/pre-flight tools (`ads_get_ad_accounts`,
  `ads_get_ad_account_pages`, `ads_get_datasets`, `ads_get_dataset_stats`) and the
  create tools (`ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad`),
  described in plain language.

### 3d. The connect walkthrough — pointer only (one home)

The exact connect commands and the callback-port fallback live in **exactly one
place**: `drivers/meta-ads/connect.md` (full content in §6e). This section does
not restate them — that would create the second documented procedure the one-home
rule forbids. If the endpoint URL or the fallback ever changes, connect.md is the
single file to edit.

**Connect model — a deliberate, labelled override of `connect-a-tool`.** The
shipped `connect-a-tool` doctrine is *owner-drives-in-app*: its Claude Code step is
"run `/mcp`, choose add/connect, follow the sign-in," and its hard rule is "no
'go run this' handoffs." Meta Ads is different: the official Meta MCP is added by
the two `claude mcp` CLI commands, which BOS can run on the owner's machine while
the owner still performs the one step only they can — the Meta OAuth sign-in in the
browser. **This overrides `connect-a-tool` for the Meta Ads case, and it must be
labelled as an override so the two do not silently diverge:**

- `connect-a-tool`'s Claude Code step and its hard rules get one added, labelled
  line: "Exception — Meta Ads: added via the `claude mcp` CLI, walked in
  `drivers/meta-ads/connect.md`. The owner still does the sign-in; see that file."
- `knowledge/connectors.md`'s Meta Ads card and `connect.md` carry the SAME CLI
  path, so no reader can drift onto the `/mcp` model for Meta.

This keeps the owner-authorizes-the-sign-in boundary intact (BOS never sees a
password or token) while acknowledging, out loud, that the add mechanism differs
from every other connector.

---

## 4. `plan-my-ads` — the floor skill

Keyless. Evelyn Weiss's ad method as thinking, generalized to any business shape.
Produces a written ad plan. Feeds `run-my-ads`. Works with no account connected.

### 4a. Exact manifest frontmatter

`skills/plan-my-ads/SKILL.md`:

```yaml
---
name: Plan My Ads
description: Turn what you sell into a clear, ready-to-run ad plan — the one result to optimize for, the offer ad that proves demand, the creative brief, the copy, the budget and the numbers to watch. Built on Evelyn Weiss's ad method. Works with no ad account connected, and applies to Facebook, Google, TikTok, or a manual setup.
triggers:
  - plan my ads
  - plan a facebook ad
  - plan an ad campaign
  - help me plan meta ads
  - write an ad plan
  - map out my ads
function_slot: ads
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
reads_for_profile:
  - offer
  - audience
  - budget_appetite
---
```

**`function_slot: ads` is shared with `run-my-ads` on purpose.** `function_slot`
is a category label, not a uniqueness key: multiple skills already share a slot in
the registry, and nothing in the surfacing logic assumes one skill per slot. The
plan/run pair both sitting in `ads` is intended.

**Body constraints:** no `mcp__*` tool reference anywhere in the body (keeps
assertion C clean — the check greps for `mcp__trustpager__` specifically, but
keeping the body free of ALL `mcp__*` also keeps the plan genuinely portable to
Google/TikTok/manual); no `unlocks` (the plan→run handoff is a body-level pointer,
not a driver unlock); positive-only, no em dash.

### 4b. Trigger phrases

The six above. Aim is 5+ (lint WARNs under 3). They cover the plain asks: "plan
my ads", "plan a facebook ad", "write an ad plan", "map out my ads".

### 4c. The numbered-gate flow

Authored as numbered gates before defaults (target model is Sonnet). The method
is Evelyn Weiss's; attribute it in the opening beat.

- **Step 1 — Read what we already know (silent).** Read `brand/brand.json` (name,
  voice, tagline, colors) and the `./CLAUDE.md` business profile (shape, offer,
  goal, the diagnosed constraint). If a `meta-ads-profile.json` exists, read only
  its **non-account** fields (budget, objective, geo) to sharpen the plan — never
  account IDs. Never require any of it; the plan works from a cold start.
- **Step 2 — Pick the one result to optimize for.** The single most important
  decision. Map the owner's goal to the real conversion event, never traffic or
  clicks:

  | Owner's goal | Optimize for | Typical shapes |
  |---|---|---|
  | Sell something now | Purchase | ecommerce/retail, low-ticket service, paid access, product |
  | Free signup / opt-in | CompleteRegistration | free community, lead magnet, freemium |
  | Enquiry / quote | Lead | trades, professional services, B2B |
  | Booking / appointment | Schedule / Booking | clinic, hospitality, consultant, call-funnel service |

  (This is the plain-language plan layer. The exact Meta enum spellings and which
  optimization goal is actually valid for each objective are `run-my-ads`'s job,
  read live from Meta at build time — see §5b. The plan never hardcodes a Meta enum.)

- **Step 3 — Design the diagnostic offer ad.** The first ad for any new offer is
  the plain "here's exactly what you get" ad — the thing itself, shown as cleanly
  and as close to the real thing as possible. No gloss, no lifestyle angle. Its
  job is to return a definite answer about the offer. State, for THIS business,
  what that ad shows, and the read the owner will make from it (internal
  vocabulary, dev-facing only): no conversions in the test window = fix the offer;
  one or more conversions, ideally about one a day = the offer has demand, worth
  more budget. Never enhance the ad past what the offer truly is to manufacture a
  positive read.
- **Step 4 — Creative brief (image-first).** Every ad is a product image or a
  product video. Choose format(s) for this business, image-first:
  - Product image: a real photo of the actual thing (the finished job, the
    product in use, the plate/room, the space/result); or a mockup of the digital
    thing (worksheets, a dashboard, a portal view); or a deliberate founder photo
    when the owner IS the product.
  - Product video: a dictated screen/subject walkthrough (front-load the same
    walkthrough that lives on the offer page for full ad-to-page congruency); or a
    lightly-edited explainer when resources allow.
  - Note plainly: start image-first (lowest-cost, fastest, most scalable); raw and
    relatable often beats polished.
- **Step 5 — Ad copy draft (the six-part formula, positive-only).** Fill in:
  1. Hook that names the result the audience wants (outcome-led — never a pain
     hook like "Tired of X?").
  2. Who you are / relevant truthful background, stated so it implies no specific
     results for others.
  3. "I created [X] for [audience] who want [outcome]."
  4. "Here's exactly what you get: 1, 2, 3, 4, 5." — the concrete deliverables.
  5. "You can get started here [price] [link]."
  6. A final CTA on its own line below the link.

  Then run the draft through the compliance rails and list any flags:
  truthful/substantiable claims only; no implied-earnings claims; no false
  scarcity; positive and outcome-led throughout. Reserve any "even if" line to
  reassure ("even if today is day one"), never to name a lack.
- **Step 6 — Budget and KPIs.** Daily test budget ≈ 1–3× the offer price, or
  ≈ 2× target CPA (target CPA derived from customer LTV). Run window 48–72 hours;
  a conversion within ~48h then about one a day is the cadence that says demand is
  real. Deliberately small — learn cheaply. Include shape benchmarks as
  **illustrative, market-dependent** (e.g. free signup roughly under $2.50–$3;
  low-ticket profitable at a low price point; higher-ticket judged against target
  CPA from LTV) — never as promises.
- **Step 7 — Scaling ladder.** Once demand is proven, the job shifts to improving
  economics so budget can rise without cost rising: lift CTR/ad quality (CPM
  falls), raise funnel conversion rate, add average order value. Only then test
  new angles/formats. Productize standalone pieces and validate each the same way
  (image first, then video) to open more paid pathways in.
- **Step 8 — Retargeting plan (the most profitable ad type).** Prerequisite:
  conversion tracking live. Audience: a 180-day custom audience from the pixel,
  filtered to the key offer page. Tiny budget (~$2–$5/day for most). Creative: an
  image ad to the exact offer-page URL, reusing landing-page elements for
  congruency. Copy: the landing-page copy re-angled for a return visitor, positive
  opener ("You checked out [X] and it stayed with you — here's why now's a good
  time"). Build five variations; compliance-check; run many creatives at high
  overall frequency for the "illusion of omnipresence." If they run nothing else,
  run retargeting.
- **Step 9 — Write the ad plan artifact and point at the run layer.** Save the
  plan (below) and close with the handoff (§4e).

### 4d. The written ad-plan artifact

`plan-my-ads` writes one plain-language markdown document to the owner's working
directory (positive-only, method attributed to Evelyn Weiss). Sections:

1. **Goal and objective** — the one conversion event to optimize for.
2. **The diagnostic offer ad** — what the plain "here's exactly what you get" ad
   is for this business, and the read criteria.
3. **Creative brief** — chosen format(s), image-first, with the specific
   shots/mockups/walkthrough to make; raw-beats-polished note.
4. **Ad copy draft** — the six-part formula filled in, with the compliance flags
   listed.
5. **Budget and KPIs** — the daily test budget with its math, the 48–72h window,
   the cadence, the shape benchmark (illustrative).
6. **Scaling ladder** — the three economic levers + productize-and-validate.
7. **Retargeting plan** — audience, tiny budget, congruent creative, five copy
   variations.
8. **What's next** — the handoff to `run-my-ads`.

The plan references "your offer page should say X" but never authors the VSL.

### 4e. How it feeds `run-my-ads`

The plan is the input `run-my-ads` reads at setup time. The close-out is prose,
not a routed keyless offer (so it never trips the keyless-honesty gate, §7):

> "That's your ad plan. When you're ready to actually launch this on Facebook and
> Instagram, I can set the campaigns up for you — built to this plan, created
> paused and safe for you to review and switch on yourself. That needs a one-time
> connection to your ad account, and I'll walk you through it."

---

## 5. `run-my-ads` — the library skill

Connected. Evelyn Weiss's guided campaign-shell setup, ported to the official Meta
Ads MCP. Creates paused shells only. The highest-stakes write surface in the BOS.

### 5a. Exact manifest frontmatter

`skills/run-my-ads/SKILL.md`:

```yaml
---
name: Run My Ads
description: Once your Meta Ads account is connected, turn your ad plan into ready-to-launch Facebook and Instagram campaigns — built to Evelyn Weiss's method, created paused and safe, checked over first, and handed back with a clear checklist and the 72-hour rule. You review and switch them on yourself; I never spend a cent without showing you first.
triggers:
  - run my ads
  - set up my meta ads
  - launch my facebook ads
  - build my ad campaign
  - create my meta campaign
  - set up a facebook ad campaign
function_slot: ads
requires_driver: meta-ads
requires_credential: mcp
data_path: mcp_tools
status: active
uses_tools:
  - mcp__meta-ads__ads_get_ad_accounts
  - mcp__meta-ads__ads_get_ad_account_pages
  - mcp__meta-ads__ads_get_datasets
  - mcp__meta-ads__ads_get_dataset_stats
  - mcp__meta-ads__ads_get_dataset_quality
  - mcp__meta-ads__ads_get_ad_entities
  - mcp__meta-ads__ads_get_creatives
  - mcp__meta-ads__ads_get_field_context
  - mcp__meta-ads__ads_get_ig_accounts
  - mcp__meta-ads__ads_get_ad_preview
  - mcp__meta-ads__ads_insights_industry_benchmark
  - mcp__meta-ads__ads_create_campaign
  - mcp__meta-ads__ads_create_ad_set
  - mcp__meta-ads__ads_create_ad
  - mcp__meta-ads__ads_update_entity
---
```

**`ads_activate_entity` is deliberately absent from `uses_tools`** — so any body
reference to it would fail lint, making an explicit activation build-failing.
`ads_update_entity` IS present (it is legitimately used to rename or fix an
integer budget/bid on a still-PAUSED shell), but it carries a hard body rule and a
CI check that it must never carry a `status` field (§8) — because
`ads_update_entity` with `{"status":"ACTIVE"}` is a second, subtler activation
path the live schema permits. Every listed value is a real tool name (verified
from the connected MCP). All tools share the `mcp__meta-ads__` substring, so the
driver-owns-tool check passes; the list is documentation of intent.

### 5b. The campaign decision tree

Owner-facing questions in plain language; the tree resolves to a `campaign_type`.

1. **Validate or scale?**
   - **Validate** — test whether the offer converts before spending more → the
     diagnostic offer-ad shell. `campaign_type: validation`.
   - **Scale** — offer already proven, want to grow.
2. **If scaling — new creative test or revive proven winners?**
   - **Creative test → High Volume vs Target Cost:**
     - **High Volume** (CBO, `LOWEST_COST_WITHOUT_CAP`) — Meta finds the most
       conversions at lowest cost. The simple, reliable start.
       `campaign_type: scale_high_volume`.
     - **Target Cost** (ABO, `COST_CAP`) — set a max cost-per-result so a higher
       daily budget won't overspend the target. Risk: too low and it may not spend.
       `campaign_type: scale_target_cost`.
   - **Revive proven winners → Bid Cap** (ABO, `LOWEST_COST_WITH_BID_CAP`) —
     advanced; set the absolute max auction bid on proven ads. Risk: too low for
     the auction and it won't deliver. `campaign_type: scale_bid_cap`.

Community/offer type maps to the optimization event (generalized from Evelyn's
paid-vs-free framing). **The optimization_goal values below are the default and
must be verified live, never hardcoded blindly** — `run-my-ads` always reads
`recommended_optimization_goal` / `valid_optimization_goals` from the
create-campaign response and picks the recommended goal before creating the ad set
(§5f). The table is the *starting default*, not the authoritative wire value:

| Owner's answer | optimization_goal (default) | promoted_object custom_event_type | campaign objective | source |
|---|---|---|---|---|
| Sell now (product/service/paid access) | `OFFSITE_CONVERSIONS` | `PURCHASE` | `OUTCOME_SALES` | attested (Evelyn) |
| Free signup / opt-in | `OFFSITE_CONVERSIONS` | `COMPLETE_REGISTRATION` | `OUTCOME_SALES` | attested (Evelyn) |
| Enquiry / quote | `OFFSITE_CONVERSIONS` | `LEAD` | `OUTCOME_LEADS` | **verified live 2026-07-03: recommended goal `LEAD_GENERATION`** |
| Booking / appointment | `OFFSITE_CONVERSIONS` | `SCHEDULE` | `OUTCOME_LEADS` | **verified live 2026-07-03: recommended goal `LEAD_GENERATION`** |

Notes carried by the body:

- **`OFFSITE_CONVERSIONS` is the "sell now" default, NOT `VALUE`.** The live
  `ads_create_ad_set` schema lists `OFFSITE_CONVERSIONS` as the first/recommended
  goal for `OUTCOME_SALES`; `VALUE` is value-optimization that requires a
  value-configured dataset (a Purchase event carrying reliable value) and usually
  a min-ROAS bid strategy. Evelyn used `VALUE` only for paid communities that pass
  purchase value. `VALUE` is a **confirmed-only upgrade**: use it only when the
  init / pre-flight has confirmed the dataset receives valued Purchase events
  (check via `ads_get_dataset_stats` / `ads_get_dataset_quality`). Default to
  `OFFSITE_CONVERSIONS` + `{"pixel_id":..,"custom_event_type":"PURCHASE"}`
  otherwise, or a VALUE ad set risks "Performance goal isn't available" rejection
  or poor delivery.
- The **PURCHASE** and **COMPLETE_REGISTRATION / OUTCOME_SALES** rows are attested
  by Evelyn's doc. The **LEAD** and **SCHEDULE / OUTCOME_LEADS** rows are the
  spec's generalization and are **not** attested by any source; the live enum
  spelling (Meta lists `LEAD_GENERATION` / `QUALITY_LEAD` as the OUTCOME_LEADS
  goals, and `OFFSITE_CONVERSIONS` as the default) must be confirmed via
  `ads_get_field_context` and the create-campaign response before the ad-set
  create. Treat these two rows as "resolve live," not settled.
- `billing_event` is `IMPRESSIONS` throughout.
- Confirm the exact `custom_event_type` enum spelling with `ads_get_field_context`
  at init/build time (Evelyn's doc writes `COMPLETE_REGISTRATION`).

### 5c. Budget and bid math

All amounts in **cents** (× 100). Read the account currency and
`min_daily_budget_cents` from `ads_get_ad_accounts` first; sub-minimum budgets are
rejected.

- **Validation / High Volume:** daily budget = 1–2× offer price (recommend 1.5× to
  start); free/lead default ~$10/day local. CBO → budget on the **campaign**
  (`campaign_daily_budget`).
- **Target Cost:** cost cap = `target_cpp × 0.7 × 100` (30% below target, giving
  Meta room). Daily budget is a ceiling, not a commitment. ABO → budget + cap on
  the **ad set**.
- **Bid Cap:** bid = `LTV ÷ target_return`, i.e. `bid_cap × 100`. Daily budget just
  sets volume. ABO → budget + bid on the **ad set**.

### 5d. Location logic (Step: choose reach)

Offer the choice: single country; their home country; a region cluster; or all
Tier-1 (recommended to start — most room for the algorithm). For AU-region owners
default the home-country path to `["AU"]` and still offer Tier-1.

- Tier-1 set (compile once, reuse):
  `["AU","AT","BE","CA","CZ","DK","FI","FR","DE","IS","IE","IT","LU","NL","NZ","NO","PL","PT","SI","ES","SE","CH","GB","US","HU"]`
- Region cluster example (DACH): `["DE","AT","CH"]`
- Targeting is **broad only**: `{"geo_locations":{"countries":[...]}}` and nothing
  else.
  - **Do not pass `age_min`/`age_max` or interests at all in the paused shell.**
    Advantage+ Audience is ON by default; with it on, any age fields are treated
    as *suggestions, not caps*, and can broaden who the ad reaches (and therefore
    who it can spend against) contrary to what the owner expects. Omitting them is
    what makes the "broad only" guarantee real.
  - Never invent interest IDs (they require real numeric IDs from a targeting
    search; placeholders are rejected).
  - If the owner explicitly asks for a hard age cap, set
    `targeting_automation.advantage_audience: 0` in the SAME call, and surface in
    the confirmation that this narrows the audience.

### 5e. Pre-flight checks (run automatically before any create)

Implemented as in-body reasoning + MCP read calls (there is no `tools/preflight.py`
and none is built). Always pass explicit ids + date ranges on reads.

1. **Ad account** — `ads_get_ad_accounts`. If several, confirm which. Check
   `is_ads_mcp_enabled` (false → stop, send them to manual Ads Manager setup);
   check `is_queryable` (false → the bid-cap revive path is unavailable; surface
   `not_queryable_reason`); read currency + `min_daily_budget_cents`. `ad_account_id`
   is numeric, no `act_` prefix. None found → stop, tell them to set up an ad
   account first.
2. **Pixel / dataset events** — `ads_get_datasets` (scope with exactly one of
   `ad_account_id` OR `business_id`), then `ads_get_dataset_stats` to verify the
   right event is firing (Purchase / CompleteRegistration / Lead / Schedule).
   `start_time`/`end_time` are Unix-timestamp strings, 28-day max lookback. Zero
   volume on the event the campaign will optimize for → warn plainly ("your
   tracking may not be connected yet"); proceed only if they confirm the pixel is
   new. `ads_get_dataset_quality` is available for a deeper look, and is the check
   that decides whether a `VALUE` "sell now" upgrade is safe (§5b).
3. **Page** — `ads_get_ad_account_pages`. Multiple → ask which; none → stop,
   connect a Page first. **Lead-gen gate:** for an `OUTCOME_LEADS` ad set whose
   optimization goal resolves to a lead-form goal (`LEAD_GENERATION` /
   `QUALITY_LEAD`), the Page must have `leadgen_tos_accepted: true`; if false, send
   them to `https://www.facebook.com/legal/leadgen/tos` before creating the ad set.
4. **Offer URL** — collect and sanity-check it points at the exact offer page, not
   a root that redirects and loses people.

### 5f. The exact `mcp__meta-ads__` call playbook (verified params)

Everything created **paused by construction** — no status flag is needed; the
create tools return entities in PAUSED state. Order: campaign → ad set → ad.

**`ads_create_campaign`** (required: `ad_account_id`, `campaign_name`,
`objective`, `buying_type`):
- `objective` — ODAX outcome values only (`OUTCOME_SALES`, `OUTCOME_LEADS`, etc.).
  Legacy names (`CONVERSIONS`, `LEAD_GENERATION` as an objective, `LINK_CLICKS`)
  are rejected as objectives.
- `buying_type` — **always pass `"AUCTION"` explicitly** (the schema requires it;
  Evelyn's doc omits it).
- `special_ad_categories` — default `"[]"`.
- **CBO** (Validation, High Volume): set `campaign_daily_budget` (cents) here;
  leave `campaign_bid_strategy` default (`LOWEST_COST_WITHOUT_CAP`).
- **ABO** (Target Cost, Bid Cap): leave ALL of `campaign_daily_budget`,
  `campaign_lifetime_budget`, `campaign_bid_strategy` **unset** — any campaign
  budget field implicitly switches to CBO and the ad-set-level bidding call is then
  rejected ("Must Use Campaign Bid Strategy").
- Campaign name convention: `[Type] - [Goal] - [BusinessName] - [Date]`.
- **Read the response's `valid_optimization_goals` /
  `recommended_optimization_goal` and treat them as authoritative** for the ad-set
  call. Pick the recommended goal; never hardcode a goal (especially never blindly
  `VALUE`, §5b). An invalid goal is auto-corrected server-side to the recommended
  default anyway — resolving it explicitly avoids surprises.

**`ads_create_ad_set`** (required: `ad_account_id`, `campaign_id`, `ad_set_name`,
`billing_event`, `optimization_goal`, `targeting`):
- `billing_event: "IMPRESSIONS"`.
- `optimization_goal` — use the value from the create-campaign response's
  `recommended_optimization_goal` (fallback: the default in the §5b table). Must be
  valid for the parent objective. Default for both `OUTCOME_SALES` and
  `OUTCOME_LEADS` is `OFFSITE_CONVERSIONS`.
- `promoted_object` (JSON string) — **required** for `OFFSITE_CONVERSIONS` /
  `VALUE` / lead-form goals. Key is **`pixel_id`**. Examples:
  `{"pixel_id":"<id>","custom_event_type":"PURCHASE"}` (paid, default),
  `{"pixel_id":"<id>","custom_event_type":"COMPLETE_REGISTRATION"}` (free). Also
  required for an `OUTCOME_SALES` + WEBSITE combination even without a custom event
  (a bare `{"pixel_id":"<id>"}`), or the create is rejected with "Performance goal
  isn't available."
- `targeting: {"geo_locations":{"countries":[...]}}` — broad only, no age/interest
  fields (§5d).
- **ABO budget/bid (only when the parent campaign carries no budget):**
  - Target Cost: `daily_budget` (cents), `bid_strategy: "COST_CAP"`,
    `bid_amount = target_cpp × 0.7 × 100`.
  - Bid Cap: `daily_budget` (cents), `bid_strategy: "LOWEST_COST_WITH_BID_CAP"`,
    `bid_amount = bid_cap × 100`.
  - Passing any of these under a CBO parent is rejected server-side.
- EU/DSA: if `geo_locations.countries` includes an EU country, `dsa_beneficiary`
  and `dsa_payor` are required; they auto-fill from the business name if omitted
  (fine).

**`ads_create_ad`** (required: `ad_account_id`, `ad_set_id`, `ad_name`,
`creative`):
- `creative` — JSON string with exactly one source:
  - New ad (default): `{"object_story_spec":{"page_id":"<PAGE_ID>","link_data":{"link":"<offer_url>","message":"<placeholder copy>"}}}`.
    `page_id` is mandatory inside `object_story_spec` (omitting it → "Facebook Page
    is Missing").
  - Bid-cap revival: `{"object_story_id":"<pageId_postId>"}`.
- The MCP cannot upload media; the owner adds the real image/video and final copy
  in Ads Manager.

**Bid-cap revival read path** (only when `is_queryable: true`):
`ads_get_ad_entities` at `level: "ad"`, `date_preset: "maximum"`, filtered to
prior spend > 0 and prior results (validate field names via `ads_get_field_context`
first — do not trust a static field list). Then `ads_get_creatives` re-called with
`creative_ids` or `fields` to get `object_story_id` (a bare listing returns only
`id`/`name`/`account_id`/`status`). A creative with no `object_story_id` cannot be
revived this way; no old ads → suggest a creative test instead.

**Never call `ads_activate_entity`, and never set `status` via
`ads_update_entity`.** These are the two live-money switches. See §8.

### 5g. PAUSED-shell creation, by campaign type

- **Validation (CBO):** campaign with `campaign_daily_budget`; ad set per §5b;
  **three ad shells** — a product-image ad, a mockup ad, a walkthrough-video ad —
  each a minimal `object_story_spec` with `page_id` + `link_data.link` +
  placeholder message.
- **High Volume (CBO):** as validation, **one ad shell**.
- **Target Cost (ABO):** campaign with no budget; ad set with `daily_budget` +
  `COST_CAP` + `bid_amount`; one ad shell. Then offer the **dual campaign** — a
  matching High Volume campaign with the same ads for comparison.
- **Bid Cap Revival (ABO):** pull old ads (above); campaign with no budget; ad set
  with `LOWEST_COST_WITH_BID_CAP` + `bid_amount`; recreate ads with
  `{"object_story_id":"pageId_postId"}`.

### 5h. Post-setup checklist + the 72-hour rule

After all creates, hand back a plain checklist (the closing beat, owner-facing,
positive-led):

- **Upload your creatives** — image or video per ad (I can't upload files, so this
  bit's yours).
- **Add your ad copy** (the six-part copy from your plan) + 2–3 short headlines.
- **Turn off enhancements** — Site Links off, Branding off, Promotions off.
- **Check the link** points to your exact offer page.
- **Validation only:** optionally duplicate the image ad with banner variations;
  save a creative folder.
- **Scale only:** duplicate the ad and swap creatives to test variations.
- **Bid cap only:** preview each revived ad, re-check the bid cap, watch it daily
  for the first few days.
- **Review everything yourself** — budget, targeting, the result you're
  optimizing for, every setting.
- **Switch it on yourself** — here's your Ads Manager link; give it a final look
  and flip it on when you're happy. I built it paused so nothing spends until you
  do.
- **Then wait 72 hours** — that's the learning phase. Leave it alone; changing
  anything resets the learning.

---

## 6. "Make it yours" init + the meta-ads profile [NEW]

**One central skill, personalization is DATA.** The `run-my-ads` body is identical
for every owner; per-user detail lives in a JSON profile written by an init
walkthrough. Never template or fork the skill file per user — a fork would either
be clobbered by `update-bos` or block updates, and it causes drift. This is stated
once as a hard rule in the body.

### 6a. Where the profile lives

```
~/.claude/bos-cache/meta-ads-profile.json
```

Per-user runtime state already lives under `~/.claude/bos-cache/` (e.g.
`follow-up-radar-state.json`). It is untracked, per-machine, owner-only. **Because
it is outside the repo tree entirely, `git pull` / `update-bos` / `setup.py` can
never touch it — no `.gitignore` entry, no protected-list entry, and no special
handling is needed** (see §7e; `update-bos` has no protected-list data structure
in any case — it protects work via git-untracked files + stash/pop, and this path
is neither tracked nor in the repo). It is NOT `brand.json`: brand identity flows
automatically because the ads skills read `brand/brand.json`; this file is the
ads-specific layer only (one home per fact — no brand fields duplicated here).

### 6b. The init walkthrough (Step 1 of `run-my-ads`, at connect time)

If the profile is absent, run init first. Init also folds
`drivers/meta-ads/OPERATING-CONTEXT.md` into `./CLAUDE.md` via `run-my-ads`'s OWN
read-and-merge step (§3c) — it does not call `learn-my-business` (which is
TrustPager-gated and never runs for a Meta-only owner). Init is a
fill-in-the-blank journey: it only *asks* for the ads-specific bucket; everything
else is auto-filled and confirmed.

### 6c. The profile schema (field-by-field, with source)

**Source A — from the brand kit (`brand/brand.json`), read, never asked:**

| field | from | used for |
|---|---|---|
| `business_name` | brand.json name | campaign naming |
| `brand_colors`, `logo_path` | brand.json | creative direction (not written to Meta by BOS) |
| `voice` | brand.json voice / `build-my-voice` output | ad copy sounds like them |
| `tagline` | brand.json tagline | copy |

**Source B — from the business profile (`./CLAUDE.md`), read, never asked:**

| field | from |
|---|---|
| `business_shape` | the profile's shape (service/trades/ecommerce/hospitality/clinic) |
| `offer` | what they sell |
| `region` | the explicit `Region:` line only if set — never inferred |
| `diagnosed_constraint` | the diagnosed pressure point → validate-vs-scale posture |
| `goal` | the owner's stated goal |

**Source C — new ads-specific asks (the ONLY interview, a few plain questions):**

| field | question (positive-led) |
|---|---|
| `monthly_ad_budget` | "Roughly what would you like to put behind ads each month to start?" |
| `primary_objective` | "What's the one result you want — more enquiries, more sales, more bookings, or more reach?" → maps to the Meta objective |
| `optimization_event` | derived from objective + shape; confirmed in words |
| `geo_targeting` | "Which areas do you want your ads to reach?" |
| `spend_ceiling_confirmed` | the owner-confirmed hard monthly ceiling BOS will never exceed without re-asking (§8) |

**Source D — auto-detected from one live read at init (confirm, don't ask):**

| field | tool (read-only) |
|---|---|
| `ad_account_id` | `ads_get_ad_accounts` (if several, ask which) |
| `page_id`, `ig_account_id` | `ads_get_ad_account_pages`, `ads_get_ig_accounts` |
| `pixel_id` / `dataset` + health + value-readiness | `ads_get_datasets`, `ads_get_dataset_quality` (also decides VALUE eligibility, §5b) |
| `past_ads_summary` | `ads_get_ad_entities` + `ads_insights_industry_benchmark` |
| `currency`, `timezone` | the ad account's own settings (Meta's currency, NOT inferred from BOS region) |

### 6d. How both skills read the profile

- **`run-my-ads`** reads `~/.claude/bos-cache/meta-ads-profile.json` at the top of
  its flow **directly with the Read tool** — it is plain JSON at a fixed path, so
  no launcher is needed. (The `bos-run.py` launcher only dispatches a skill's
  `fetch.py` or an allowlisted `tool`; `run-my-ads` ships no `fetch.py`, so the
  follow-up-radar `fetch.py` pattern does not apply here.) Absent → run init first.
- **`plan-my-ads`** (keyless) reads only the brand kit + business profile — never
  account IDs. If the ads profile happens to exist, it may read only the
  non-account fields (budget, objective, geo) to sharpen the plan; it never
  requires it and never reads account IDs, so the plan stays portable.

### 6e. `connect.md` content (the walkthrough — single home for the connect steps)

```markdown
# Connect Meta Ads (Facebook & Instagram ads)

## What this unlocks
Once connected, I can set up your Facebook and Instagram ad campaigns for you —
built to your plan, created paused and safe, ready for you to review and switch
on yourself. Reads are free; I never spend a cent without showing you first.

## The honest boundary
There's one sign-in only you can do (it's your ad account). I do everything
else: the exact steps, the safety thinking, the check that it worked, and the
setup. I'll never ask for a password or a code. This loads the ad tools, but
Claude Code keeps them out of the way until I actually use one, so it won't slow
your other work.

(For the builder: this connector is added via the `claude mcp` CLI, which is a
deliberate, labelled exception to connect-a-tool's usual "/mcp in the app" flow.
The owner still performs the sign-in themselves; BOS only runs the add/login
commands. See spec §3d.)

## Step 1 — I add the connection for you (permission first)
"To set up your ads I need to add the Meta Ads connection. It's a one-time,
free sign-in with your Facebook account. Want me to get it ready?"
On yes, I run (on your machine, so I do it, not you):
    claude mcp add --transport http --scope user meta-ads https://mcp.facebook.com/ads
It must be user scope so it's available everywhere, not just this folder.

## Step 2 — You sign in (the one step that's yours)
I run:
    claude mcp login meta-ads
This opens Meta's sign-in in your browser. Sign in with the Facebook account
that manages your ads and approve the access.
- Grant the read-only access first. We start read-only so nothing can spend by
  accident; we widen it only when you're ready to actually launch.
- If the browser sign-in seems to hang (the little local page never returns), no
  problem — I re-add it on a fixed port and we try again:
    claude mcp add --transport http --scope user meta-ads https://mcp.facebook.com/ads --callback-port 8080

## Step 3 — Restart so it loads
The connection only wakes up when Claude Code starts fresh. So: close and reopen
Claude Code once. (Before the restart it won't show in /mcp yet — that's
expected, not a problem.)

## Step 4 — I verify it worked
Back after the restart, I do one small read to prove it's live — I list your ad
accounts. If I can see them, you're connected. If not, we check you signed into
the right Facebook account and try the sign-in once more.

## Step 5 — Make it yours, then put it to use
The moment it verifies, I run the quick "make it yours" setup (I read your brand
and business, take a look at your account, and ask a couple of ads questions),
then we're ready to launch your plan — created paused, for your review.
```

### 6f. The `## Meta Ads` card in `knowledge/connectors.md` [NEW]

A short catalog card following the existing schema; the detail lives in
`connect.md` (one home).

- **What it is:** the owner's Facebook and Instagram ad account, so the system can
  build campaigns to their plan — paused and safe.
- **Fits businesses that:** want more enquiries, sales, or bookings from paid ads;
  have an offer to put in front of a cold or warm audience; already run (or want to
  start) Facebook/Instagram ads.
- **Unlocks:** `run-my-ads` — pre-flight checks and paused campaign/ad-set/ad
  shells built to your ad plan, with a post-setup checklist and the 72-hour rule.
  (Hands off to `run-my-ads`, the way TrustPager hands off to its connected tier.)
- **Connect it:** the steps live in
  [drivers/meta-ads/connect.md](../drivers/meta-ads/connect.md) — user-scope
  `claude mcp add`, `claude mcp login meta-ads`, grant the read-only tier first,
  restart, verify with one read. Fallback `--callback-port 8080` if the callback
  stalls. (This connector uses the `claude mcp` CLI, a labelled exception to the
  usual in-app `/mcp` connect flow — see connect.md.)
- **Keep it lean:** connect it when the owner is ready to launch ads, not "just in
  case." The tools stay deferred (names only) until one is used, so it won't slow
  other work.
- **Heads-up:** ads spend real money — but the system only ever creates campaigns
  **paused**, shows every setting first, and never turns anything on. The owner
  reviews in Ads Manager and switches it on themselves. No cost to connect.
- **Verify:** ask the system to list your ad accounts. If it can see them, the
  connection is live, and it'll run the "make it yours" setup next.

---

## 7. Packaging and gating

### 7a. In-repo, gated dark today (no library subsystem)

The D13 off-the-shelf library is decided but not built. Everything `run-my-ads`
needs to stay dark until Meta is connected already exists:

1. **`requires_driver: meta-ads` is the hard gate.** `whats-possible` reads
   `kernel/registry.json` and splits apps by credential/driver; anything with a
   non-keyless driver renders in the "switches on when you connect a tool" half,
   never the "works right now" half — exactly how the TrustPager MCP skills sit
   dark until TrustPager is connected. `run-my-ads` inherits that for free.
2. **Registry activation + pinning (D6)** is the surfacing control: un-pinned
   connected apps stay out of the always-loaded trigger surface; connecting Meta
   pins/activates `run-my-ads`. The pin does the job the library would eventually
   do — no "install from library" step needed.
3. **The onboarding-binding check keeps it honest.** Because `run-my-ads` is
   `requires_credential: mcp` + `requires_driver: meta-ads` (not keyless),
   assertion B fails the build if any onboarding surface offers it as a keyless
   win.

### 7b. The future home (stated once, no drift)

Document in this spec and in a one-line comment in `run-my-ads`'s body:

> When the D13 off-the-shelf library subsystem ships, `run-my-ads` (and the
> `meta-ads` driver) become a tier-1 library module — grab-and-go alongside the
> Remotion creative studio. Until then it ships in-repo, gated dark by
> `requires_driver: meta-ads` + registry pinning.

### 7c. Install

- **Nothing new at install time.** `setup.py` already copies `skills/*` into
  `~/.claude/skills/` for auto-discovery and records ownership in `bos.json`.
  `plan-my-ads` is live keyless immediately; `run-my-ads` is present but dark.
- **The Meta MCP is NOT registered by `setup.py`** (unlike keyless Firecrawl). It
  is connected on demand via `connect.md` when the owner chooses to launch ads.
  This keeps the floor at zero connected-driver tools (D10).
- **Regenerate the registry** — after adding the two `SKILL.md` files, run
  `python tools/registry-generator.py` and commit `kernel/registry.json`, or the
  `--check` CI gate fails STALE. The generator auto-includes both (any valid
  manifest is picked up), with zero generator edits.
- A restart is required for the skills to load; both close-outs say so.

### 7d. Onboarding-surface safety (assertion B)

`start-here` must never advertise `run-my-ads` as a keyless win. It may mention the
ad-plan outcome (routing to keyless `plan-my-ads`); the plan→run pointer is prose,
not a routed keyless offer, so it does not trip B. Two options for surfacing
`run-my-ads` elsewhere (pick one at build time):

- **Minimal (no tooling change):** only name `run-my-ads` in `whats-possible`
  (existence-checked, not keyless-asserted) and in a `starter-projects.md` row
  under a "switches on when connected" heading. Works today, zero code change.
- **Cleaner (recommended):** add a generic `needs_connection` tag to
  `_CONNECTED_TIER_TAGS` in `tools/check-onboarding-binding.py` (currently
  `{better_with_crm, needs_crm}`) so ads/other-driver apps can be flagged
  honestly without a CRM-specific word. Small, additive, vendor-neutral.

### 7e. `update-bos` safety

- **The ads profile needs no `update-bos` change.** `~/.claude/bos-cache/
  meta-ads-profile.json` lives outside the repo tree, so `git pull` / `git stash` /
  `setup.py` never see it. `update-bos` has no "protected list" data structure to
  add it to (it protects work via git-untracked files + `git stash`/`pop`), and
  none is needed here. If any belt-and-suspenders is ever wanted, the only real
  hook is a one-line note in `update-bos` Step 2's "protect their work" prose that
  `bos-cache` is owner state — but even that is redundant given the path is
  untracked and non-repo.
- The `meta-ads` MCP connection lives in the owner's Claude Code user config
  (`~/.claude.json`), outside the repo — `update-bos` doesn't touch it, and a repo
  update never disconnects them.
- Because personalization is DATA, refreshing the shared skill files is safe and
  desirable — the owner gets improved ad logic while keeping their account IDs,
  budget, and ceiling.

---

## 8. Spend-safety model (layered) + journal integration

Meta writes spend real money. This is the highest-stakes write surface in the BOS
(higher than TrustPager credits). Four layers, three added by BOS on top of the
official MCP. **There are TWO activation paths, not one** — an explicit activate
call, and a status write on update — and every layer covers both.

**Layer 0 — the official MCP.** Every `ads_create_*` tool creates its entity in
**PAUSED state by construction** and confirms every write. BOS relies on this but
does not trust it as the only guard.

**Layer 1 — BOS explicit confirmation gate (in the `run-my-ads` body). This is the
spend gate.** Before ANY `ads_create_*` or `ads_update_entity` call, show the owner
exactly what will be created or changed — objective, budget, audience, geo,
creative — plus the per-day and monthly spend implication (in the ad account's own
currency), and require an explicit yes. Mirrors the shipped `send-email` "show and
approve" pattern, raised to spend-money stakes. The confirmation is positive-led:
"I'll create this **paused** — nothing spends until you review it in Ads Manager
and switch it on yourself." For an `ads_update_entity` edit, the confirmation must
re-assert the entity remains PAUSED after the change.

**Layer 2 — journal every write (after-the-fact record, NOT a gate) [NEW].** A
`claude_mcp` driver has no Python transport, so writes do not auto-journal through
the kernel. The `run-my-ads` body journals explicitly after each confirmed create
via a small new `journal-write` mode on `tools/run.py` that calls
`kernel.runtime.journal.record_write` directly:

```
python ~/.claude/bos-run.py journal-write \
  --method mcp__meta-ads__ads_create_campaign \
  --path meta-ads/act_<id>/campaigns \
  --status ok --result-id <returned campaign id> \
  --body '{"objective":"...","daily_budget":"...","status":"PAUSED"}'
```

Implementation notes for the builder:
- `journal-write` is a **new `elif` branch in `run.py`'s `main()`**, parallel to
  the `argv[0] == "tool"` branch. It is **NOT** an entry in `_ALLOWED_TOOLS` —
  that frozenset dispatches files in `tools/`, and there is no `tools/journal-write.py`.
  The branch imports `kernel.runtime.journal.record_write` and passes `--body` as a
  parsed JSON dict. (The test asserting every skill-invoked *tool* is in
  `_ALLOWED_TOOLS` does not cover subcommands, so add a small dedicated test for
  this branch — §9.)
- `record_write`'s real signature (`method, path, body, *, status, result_id,
  approval_id, error, journal_dir`) maps cleanly to the `--method / --path /
  --status / --result-id / --body` CLI. It runs everything through `redact()`, so
  no token can leak, and writes to the same append-only
  `~/.claude/bos-journal/YYYY-MM-DD.jsonl` CRM writes land in.

**Journaling is best-effort by design and is NOT a spend gate.** `record_write`
wraps its body in `except Exception: pass` and returns early when journaling is
disabled (`BOS_JOURNAL=0`), so a create can succeed while its journal line silently
fails to write (disabled env, disk error, bad path). Layer 1 confirmation is the
gate; Layer 2 is an after-the-fact record only. To keep the audit trail honest, the
`run-my-ads` body **verifies the journal line landed** after each confirmed create
(re-read today's `bos-journal/*.jsonl` for the returned `result_id`) and tells the
owner plainly if the record could not be written, rather than assuming success.
This changes nothing in the kernel.

**Layer 3 — NEVER activate: no `ads_activate_entity`, and no `status` write.** BOS
creates paused shells and stops; it never un-pauses by any route. There are two
activation paths and both are closed:
1. `ads_activate_entity` — the obvious live-money switch.
2. `ads_update_entity` with a `status` field set to ACTIVE — the live schema
   accepts a free-form `fields` JSON object of ANY field-name to value, including
   `{"status":"ACTIVE"}`. The tool's own description only *advises* against it; it
   does not enforce it. So this is a real second path and is treated as equally
   off-limits.

Enforced at three levels, both paths covered:
1. **Driver metadata (documentation of intent):**
   `"never_call": ["mcp__meta-ads__ads_activate_entity"]` and
   `"never_set": {"mcp__meta-ads__ads_update_entity": ["status"]}` in
   `drivers/meta-ads/__init__.py`.
2. **Skill body hard rules + manifest omission.** The "Hard rules" section states
   plainly: "I never turn ads on. I build them paused and hand them to you to
   review in Ads Manager and switch on yourself. `ads_activate_entity` is
   off-limits. `ads_update_entity` is used ONLY to rename or set an integer
   budget/bid on a still-PAUSED shell; it must NEVER carry a `status` field.
   Setting status to ACTIVE is a spend action and is off-limits by the same rule as
   `ads_activate_entity`." `ads_activate_entity` is deliberately absent from
   `uses_tools`, so referencing it in the body fails lint. (`ads_update_entity`
   stays in `uses_tools` because it has a legitimate paused-only use; the status
   rule is enforced by the CI check below, not by omission.)
3. **A cheap CI assertion (`tools/check-ads-safety.py`, recommended):** assert
   that (a) no skill body references `ads_activate_entity`, AND (b) no skill body
   passes `ads_update_entity` a `fields` payload containing a status set to ACTIVE
   — grep for the co-occurrence of `ads_update_entity` with a
   `"status"\s*:\s*"ACTIVE"` (or any `status` key inside an update `fields` blob).
   Belt-and-suspenders, mirroring how assertion C forbids TrustPager coupling
   tokens. Easy to extend to future `never_call` / `never_set` entries from driver
   metadata.

**Spend-ceiling honesty.** If a requested campaign's budget × schedule would exceed
`spend_ceiling_confirmed`, `run-my-ads` re-asks before creating — a confirm, not a
dismissible heads-up, because it is real money.

**Currency safety.** The confirmation shows the ad account's own currency
(auto-detected at init), never a currency inferred from the BOS region. `Region:`
stays explicit-opt-in and is never inferred.

---

## 9. Test plan

### `plan-my-ads` — keyless / offline (the floor bar)

- **Lint clean:** `python tools/lint-skill.py skills/plan-my-ads` — no undeclared
  tools, no unknown manifest keys, no vendor literals.
- **`BOS_OFFLINE` green:** runs to a finished ad-plan artifact with zero network,
  zero key, zero tools (`test-skill.py` under `BOS_OFFLINE=1`).
- **Binding check green:** `check-onboarding-binding.py` — passes A (exists +
  active in the regenerated registry), B (registry-keyless), C (no TrustPager
  coupling token, and no `mcp__meta-ads__*` reference anywhere in the body).
- **Business-shape coverage:** run the plan for each shape (service, trades,
  ecommerce, hospitality, clinic) and confirm the method generalizes off the Skool
  base — no Skool-specific assumption (paid-vs-free community, `/about` URL, Skool
  pixel setup, LT/LTH prefixes, the reverse-organic loop) leaks into, say, a
  plumber's plan.
- **Content-rule guard:** the ad plan is customer-adjacent copy → positive-led, no
  em dash (the em-dash normalizer + `check-doctrine-voice.py`).

### `run-my-ads` — tested without spending

- **Manifest + lint:** `uses_tools` matches the tools the body calls;
  `ads_activate_entity` is absent from both manifest and body.
- **Ads-safety check:** `tools/check-ads-safety.py` proves (a) no body references
  `ads_activate_entity`, and (b) no body sets `status` ACTIVE via `ads_update_entity`
  (both activation paths, §8 Layer 3.3).
- **Registry classification test:** assert `run-my-ads` lands in the connected
  half — `requires_credential == "mcp"` and `requires_driver == "meta-ads"` in
  `kernel/registry.json`, and `_is_keyless()` returns False for it. Pure JSON
  assertion, no network.
- **Binding-check negative test:** a fixture that offers `run-my-ads` as a keyless
  win on a surface → assert `check-onboarding-binding.py` FAILs it (proves the
  dark-gate bites).
- **Journal-write mode test:** call the new `run.py journal-write` branch with a
  fake `ads_create_campaign` record → assert a redacted line lands in a temp
  `bos-journal/` dir (the journal's `journal_dir` param is the test seam). No Meta
  call needed. Also assert the branch is reachable WITHOUT touching `_ALLOWED_TOOLS`.
- **Init walkthrough test (offline):** feed a fixture `brand.json` + fixture
  `./CLAUDE.md` + a fixture account-read JSON → assert init writes a correct
  `meta-ads-profile.json` with fields correctly sourced (A/B/C/D buckets), and that
  account IDs never bleed into anything `plan-my-ads` reads.
- **Live paused-shell test (no spend), gated behind an explicit test flag, run once
  manually:** against a real or sandbox ad account, create a paused campaign that
  spends $0 until manually activated, then delete it. **Exercise a lead-objective
  shell (`OUTCOME_LEADS`), not only a sales one**, so the inferred LEAD/SCHEDULE
  rows (§5b) are proven once against the live API before ship. Not in `BOS_OFFLINE`
  CI. The offline CI proves everything except the live create; the live create is
  proven once, on a paused shell, and torn down.

**Gates to run before declaring done:**
`python tools/lint-skill.py skills/plan-my-ads skills/run-my-ads`;
`python tools/registry-generator.py --check`;
`python tools/check-onboarding-binding.py`;
`python tools/check-no-secrets.py`;
`python tools/check-ads-safety.py`.

---

## 10. Open decisions for the founder + phased build order

### Open decisions

1. **Onboarding-surface tagging (§7d):** minimal (name `run-my-ads` only in
   `whats-possible` + a "switches on when connected" `starter-projects.md` row,
   zero code change) vs cleaner (add a `needs_connection` tag to
   `_CONNECTED_TIER_TAGS`). Recommendation: cleaner — one additive, vendor-neutral
   line that serves every future connected driver.
2. **Ads-safety CI check (§8 Layer 3.3):** a dedicated `tools/check-ads-safety.py`
   vs extending `check-onboarding-binding.py`. Recommendation: a small dedicated
   check — clearer intent, and it must assert BOTH activation paths (activate call
   + status-via-update), so a dedicated file keeps that logic self-contained and
   easy to extend to future `never_call` / `never_set` tools.
3. **`ads_get_dataset_quality` in pre-flight:** required every run, or offered as a
   deeper look on request. Recommendation: run it whenever a `VALUE` "sell now"
   upgrade is under consideration (it is the check that decides VALUE eligibility,
   §5b); otherwise offer on request and keep the default pre-flight to Evelyn's
   pixel-firing check (`ads_get_dataset_stats`).
4. **Dual-campaign default for Target Cost (§5g):** always offer the matching High
   Volume comparison campaign, or only on request. Recommendation: offer, don't
   impose (it doubles the shells).

### Phased build order (driver-first)

1. **Driver first.** Create `drivers/meta-ads/` — `__init__.py` (declarative
   metadata, labelled documentation-only), `OPERATING-CONTEXT.md`, `connect.md`
   (the single home for the connect steps), and `README.md` (the reusable-shape
   doc). Add the `## Meta Ads` card to `knowledge/connectors.md`, and add the
   labelled Meta-Ads exception line to `connect-a-tool/SKILL.md` (§3d). This is the
   foundation both skills and the connect flow lean on; nothing spends.
2. **Floor skill.** `skills/plan-my-ads/SKILL.md` — the keyless plan layer. Lint,
   regenerate the registry, prove `BOS_OFFLINE` green + binding-check green across
   all five business shapes. Ship this first as a standalone floor win even before
   `run-my-ads`.
3. **Tooling deltas (small, additive).** Add the `journal-write` branch to
   `tools/run.py` (a new `elif` in `main()`, NOT an `_ALLOWED_TOOLS` entry); add
   `tools/check-ads-safety.py` (both activation paths); (if chosen) add
   `needs_connection` to `_CONNECTED_TIER_TAGS`. No `update-bos` change and no
   `.gitignore` change — the profile is outside the repo tree (§6a, §7e).
4. **Connected skill.** `skills/run-my-ads/SKILL.md` — init walkthrough as Step 1
   (with its own OPERATING-CONTEXT fold-in, not a call into learn-my-business),
   pre-flight, the paused-shell playbook, the spend-safety hard rules (both
   activation paths), the post-setup checklist + 72h rule. Regenerate the registry.
   Run the no-spend test suite, then the one manual live paused-shell test
   (including a lead-objective shell).
5. **Onboarding surfaces.** Only after the registry is regenerated (so assertion A
   sees real keys), add `plan-my-ads` as a keyless win where appropriate and
   `run-my-ads` under a connected/coming-soon heading per §7d. Run the full gate
   set.

**Doctrine check:** kernel unchanged (only an additive `run.py` branch; no
`kernel/` edit) ✓; floor works at zero accounts (`plan-my-ads` keyless) ✓; owner
never sees kernel/driver/MCP (plain-language `connect.md` + bodies) ✓; token-frugal
(Meta MCP connected on demand, schemas deferred) ✓; anti-drift one-home (connect
steps in `connect.md` only, §3d + card point to it; connect-model override
labelled; future-library-home stated once; brand read, not copied) ✓; positive-only,
method attributed to Evelyn Weiss ✓; spend safety layered with a hard never-activate
line covering BOTH activation paths ✓; MIT-clean (the MCP is the owner's own
connection, no vendored code) ✓.

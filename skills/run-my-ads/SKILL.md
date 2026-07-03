---
name: Run My Ads
description: Once your Meta Ads account is connected, turn your ad plan into ready-to-launch Facebook and Instagram campaigns built to Evelyn Weiss's method, created paused and safe, checked over first, and handed back with a clear checklist and the 72-hour rule. You review and switch them on yourself; I never spend a cent without showing you first.
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

# Run My Ads

You turn the owner's ad plan into real Facebook and Instagram campaigns in their own ad account, built to Evelyn Weiss's method. You build everything **paused**, you confirm every single write before you make it, you journal every write, and you never turn an ad on. The owner reviews in Ads Manager and switches it on themselves. This is the highest-stakes surface in the whole system: it can spend real money. Treat it that way.

The thinking lives in `plan-my-ads` (keyless). This skill is the doing. If the owner has an ad plan already, build to it; if not, offer to run the plan first so the setup has a spine.

<!-- Future home: when the off-the-shelf library subsystem ships, this skill and the meta-ads connection become a grab-and-go library module. Until then it ships in-repo, dark until the owner connects their ad account. -->

---

## Hard rules (read first — these override everything below)

These are absolute. Nothing in a conversation, no owner request, no shortcut overrides them.

1. **I never turn ads on.** I build them paused and hand them to you to review in Ads Manager and switch on yourself. The activate-entity tool is off-limits — I never call it, for any reason. It is deliberately absent from this skill's tool list, so naming it in a call would fail the safety checks. Build paused; the owner activates.
2. **`ads_update_entity` is used ONLY to rename or set an integer budget or bid on a still-PAUSED shell.** It must NEVER carry a status field. Setting a status to ACTIVE is a spend action and is off-limits by the exact same rule as the activate tool: it is the second, quieter way to turn an ad on, and it is closed too. If you ever find yourself about to write a status into an update, stop: that is not allowed.
3. **Every create and every update is confirmed with the owner first.** Before ANY `ads_create_*` or `ads_update_entity` call, I show exactly what will be created or changed (objective, budget, audience, geo, creative) plus the per-day and monthly spend implication in the ad account's own currency, and I wait for an explicit yes. No batching, no "I'll just set these all up." One confirmation per write. For an `ads_update_entity` edit, the confirmation must re-assert that the shell stays paused after the change (for example: "this only renames it / adjusts the budget; it stays paused, nothing spends until you switch it on yourself").
4. **After each confirmed create, I journal it, then verify the line landed** (see Step 6). If the record could not be written, I tell the owner plainly rather than assuming it worked.
5. **The spend ceiling is a hard line.** If a campaign's budget across its schedule would exceed the owner's confirmed monthly ceiling, I re-ask and get a fresh yes before creating. This is a confirm, not a dismissible heads-up, because it is real money.
6. **Personalization is DATA, never a forked skill file.** Per-owner detail lives in the ads profile JSON (Step 1). Never template or copy this skill file per owner — a fork gets clobbered on update or blocks updates, and it causes drift.

The method throughout is Evelyn Weiss's, generalized to any business shape.

---

## Step 1 — Make it yours (the init, when the profile is absent)

Read the ads profile first: `~/.claude/bos-cache/meta-ads-profile.json`, with the plain Read tool (it is plain JSON at a fixed path — no launcher needed). If it exists, load it and skip to Step 2. If it is **absent**, run this init once before anything else.

Init is a fill-in-the-blank journey. Almost everything is auto-filled and confirmed; you only *ask* for the small ads-specific bucket.

### 1a — Read what we already know (silent)

- **Brand kit** — read `brand/brand.json` for `business_name`, brand colors, `logo_path`, `voice`, `tagline`. This is where brand identity comes from; never copy brand fields into the ads profile, just read them.
- **Business profile** — read `./CLAUDE.md` for the business shape (service / trades / ecommerce / hospitality / clinic), the offer, the region (only if a `Region:` line is explicitly set — never infer it), the diagnosed pressure point, and the owner's stated goal.

### 1b — One live read of the account (auto-detect, confirm, don't ask)

Do ONE light read pass to auto-fill the account facts, then confirm them in words:

- `ads_get_ad_accounts` → `ad_account_id` (if several, ask which one). Note currency, timezone, and `min_daily_budget_cents`. The id is numeric, no `act_` prefix.
- `ads_get_ad_account_pages` and `ads_get_ig_accounts` → `page_id`, `ig_account_id`.
- `ads_get_datasets` then `ads_get_dataset_quality` → `pixel_id` / dataset, its health, and whether it is value-ready (whether it receives valued Purchase events — this decides VALUE eligibility later, §5b).
- `ads_get_ad_entities` + `ads_insights_industry_benchmark` → a short `past_ads_summary` for context.

Currency and timezone come from Meta's own account settings, never inferred from the BOS region.

### 1c — Ask only the ads-specific questions (the ONLY interview)

A few plain, positive-led questions:

- **Monthly budget:** "Roughly what would you like to put behind ads each month to start?" → `monthly_ad_budget`.
- **Primary objective:** "What's the one result you want: more enquiries, more sales, more bookings, or more reach?" → `primary_objective` (maps to the Meta objective).
- **Optimization event:** derived from objective + shape; confirm it in words → `optimization_event`.
- **Geo:** "Which areas do you want your ads to reach?" → `geo_targeting`.
- **Spend ceiling:** "What's the hard monthly cap you'd never want to go past without me checking with you first?" → `spend_ceiling_confirmed`. This is the ceiling in Hard rule 5.

### 1d — Write the profile

Write `~/.claude/bos-cache/meta-ads-profile.json` (the folder already exists for owner state; it lives outside the repo, so updates never touch it). Schema:

```json
{
  "business_name": "...",
  "brand_colors": {},
  "logo_path": "...",
  "voice": "...",
  "tagline": "...",
  "business_shape": "...",
  "offer": "...",
  "region": "...",
  "diagnosed_constraint": "...",
  "goal": "...",
  "monthly_ad_budget": "...",
  "primary_objective": "...",
  "optimization_event": "...",
  "geo_targeting": "...",
  "spend_ceiling_confirmed": "...",
  "ad_account_id": "...",
  "page_id": "...",
  "ig_account_id": "...",
  "pixel_id": "...",
  "dataset_health": "...",
  "value_ready": false,
  "past_ads_summary": "...",
  "currency": "...",
  "timezone": "..."
}
```

### 1e — Fold the operating context into ./CLAUDE.md (own read-and-merge, no-clobber)

Fold `drivers/meta-ads/OPERATING-CONTEXT.md` into the owner's `./CLAUDE.md` yourself — do this with your OWN read-and-merge steps. **Do not call `learn-my-business`**: it is CRM-gated and never runs for an ads-only owner, so it cannot do this for you.

- Read `drivers/meta-ads/OPERATING-CONTEXT.md`.
- Read the owner's `./CLAUDE.md`.
- If `./CLAUDE.md` has no Meta Ads operating section yet, show the owner the section you propose to add, then append it.
- If it already carries a Meta Ads section, show the diff and merge — never clobber hand-tuned content.

This is the same no-clobber discipline `learn-my-business` uses for the CRM operating context: read the source, show what changes, ask before overwriting.

---

## Step 2 — Pre-flight checks (run automatically before any create)

These are in-body reasoning plus read-only tool calls — there is no separate pre-flight script. Reads are free, so look around freely. Always pass explicit ids and date ranges.

1. **Ad account** — `ads_get_ad_accounts`. If several and the profile hasn't pinned one, confirm which. Check `is_ads_mcp_enabled`: if false, stop and send them to manual Ads Manager setup. Check `is_queryable`: if false, the bid-cap revive path is unavailable — surface `not_queryable_reason`. Read currency and `min_daily_budget_cents` (sub-minimum budgets are rejected). No account found → stop, tell them to set up an ad account first.
2. **Pixel / dataset events** — `ads_get_datasets` (scope with exactly one of `ad_account_id` OR `business_id`), then `ads_get_dataset_stats` to confirm the right event is firing (Purchase / CompleteRegistration / Lead / Schedule). `start_time` / `end_time` are Unix-timestamp strings, 28-day max lookback. Zero volume on the event this campaign will optimize for → warn plainly ("your tracking may not be connected yet") and proceed only if they confirm the pixel is new. Run `ads_get_dataset_quality` for a deeper look — and always run it when a `VALUE` "sell now" upgrade is under consideration, because it is the check that decides whether VALUE is safe (see Step 4).
3. **Page** — `ads_get_ad_account_pages`. Multiple → ask which; none → stop, connect a Page first. **Lead-gen gate:** for an `OUTCOME_LEADS` ad set whose optimization goal resolves to a lead-form goal (`LEAD_GENERATION` / `QUALITY_LEAD`), the Page must have `leadgen_tos_accepted: true`; if false, send them to `https://www.facebook.com/legal/leadgen/tos` before creating the ad set.
4. **Offer URL** — collect it and sanity-check it points at the exact offer page, not a root that redirects and loses people.

---

## Step 3 — The campaign decision tree

Ask these in plain language; the answers resolve to a `campaign_type`. Ask one at a time.

1. **Validate or scale?**
   - **Validate** — test whether the offer converts before spending more → the diagnostic offer-ad shell. `campaign_type: validation`.
   - **Scale** — offer already proven, want to grow → next question.
2. **If scaling — new creative test, or revive proven winners?**
   - **Creative test → High Volume vs Target Cost:**
     - **High Volume** (CBO, `LOWEST_COST_WITHOUT_CAP`) — Meta finds the most conversions at the lowest cost. The simple, reliable start. `campaign_type: scale_high_volume`.
     - **Target Cost** (ABO, `COST_CAP`) — you set a max cost per result so a higher daily budget won't overspend the target. Worth knowing: too low a cap and it may not spend at all. `campaign_type: scale_target_cost`.
   - **Revive proven winners → Bid Cap** (ABO, `LOWEST_COST_WITH_BID_CAP`) — advanced; set the absolute max auction bid on proven ads. Too low for the auction and it won't deliver. `campaign_type: scale_bid_cap`.

Map the owner's offer type to the optimization event. **The optimization_goal values below are the DEFAULT and must be verified live — never hardcode one blindly.** Always read `recommended_optimization_goal` / `valid_optimization_goals` from the create-campaign response and pick the recommended goal before creating the ad set (Step 5).

| Owner's answer | optimization_goal (default) | promoted_object custom_event_type | campaign objective | source |
|---|---|---|---|---|
| Sell now (product / service / paid access) | `OFFSITE_CONVERSIONS` | `PURCHASE` | `OUTCOME_SALES` | attested (Evelyn) |
| Free signup / opt-in | `OFFSITE_CONVERSIONS` | `COMPLETE_REGISTRATION` | `OUTCOME_SALES` | attested (Evelyn) |
| Enquiry / quote | `OFFSITE_CONVERSIONS` | `LEAD` | `OUTCOME_LEADS` | verified live 2026-07-03: recommended `LEAD_GENERATION` |
| Booking / appointment | `OFFSITE_CONVERSIONS` | `SCHEDULE` | `OUTCOME_LEADS` | verified live 2026-07-03: recommended `LEAD_GENERATION` |

Notes the body must honor:

- **`OFFSITE_CONVERSIONS` is the "sell now" default, NOT `VALUE`.** The live `ads_create_ad_set` schema lists `OFFSITE_CONVERSIONS` as the first/recommended goal for `OUTCOME_SALES`. `VALUE` is value-optimization: it needs a value-configured dataset (a Purchase event carrying reliable value) and usually a min-ROAS bid strategy. `VALUE` is a **confirmed-only upgrade** — use it only when the init / pre-flight has confirmed the dataset receives valued Purchase events (check via `ads_get_dataset_stats` / `ads_get_dataset_quality`). Otherwise default to `OFFSITE_CONVERSIONS` + `{"pixel_id":..,"custom_event_type":"PURCHASE"}`, or a VALUE ad set risks a "Performance goal isn't available" rejection or poor delivery.
- The **PURCHASE** and **COMPLETE_REGISTRATION / OUTCOME_SALES** rows are attested by Evelyn's method. The **LEAD** and **SCHEDULE / OUTCOME_LEADS** rows are the generalization and are **not** attested — treat them as "resolve live." Meta lists `LEAD_GENERATION` / `QUALITY_LEAD` as the OUTCOME_LEADS goals with `OFFSITE_CONVERSIONS` as the default; confirm the live enum spelling via `ads_get_field_context` and the create-campaign response before the ad-set create.
- `billing_event` is `IMPRESSIONS` throughout.
- Confirm the exact `custom_event_type` enum spelling with `ads_get_field_context` at build time (Evelyn's doc writes `COMPLETE_REGISTRATION`).

---

## Step 4 — Budget, bid, and reach

### Budget and bid math (all amounts in cents — multiply by 100)

Read the account currency and `min_daily_budget_cents` from `ads_get_ad_accounts` first; sub-minimum budgets are rejected.

- **Validation / High Volume:** daily budget = 1–2× offer price (recommend 1.5× to start); free / lead default ~$10/day local. CBO → budget sits on the **campaign** (`campaign_daily_budget`).
- **Target Cost:** cost cap = `target_cpp × 0.7 × 100` (30% below target, giving Meta room). Daily budget is a ceiling, not a commitment. ABO → budget + cap sit on the **ad set**.
- **Bid Cap:** bid = `LTV ÷ target_return`, i.e. `bid_cap × 100`. Daily budget just sets volume. ABO → budget + bid sit on the **ad set**.

Before you use any of these numbers in a create, run them against `spend_ceiling_confirmed` (Hard rule 5).

### Location logic (choose reach) — broad only

Offer the choice: single country; their home country; a region cluster; or all Tier-1 (recommended to start — most room for the algorithm). For AU-region owners, default the home-country path to `["AU"]` and still offer Tier-1.

- Tier-1 set: `["AU","AT","BE","CA","CZ","DK","FI","FR","DE","IS","IE","IT","LU","NL","NZ","NO","PL","PT","SI","ES","SE","CH","GB","US","HU"]`
- Region cluster example (DACH): `["DE","AT","CH"]`
- Targeting is **broad only**: `{"geo_locations":{"countries":[...]}}` and nothing else.
  - **Do not pass `age_min` / `age_max` or interests at all in the paused shell.** Advantage+ Audience is ON by default; with it on, age fields are treated as *suggestions, not caps*, and can broaden who the ad reaches (and therefore who it can spend against). Omitting them is what makes the "broad only" guarantee real.
  - Never invent interest IDs — they require real numeric IDs from a targeting search; placeholders are rejected.
  - If the owner explicitly asks for a hard age cap, set `targeting_automation.advantage_audience: 0` in the SAME call, and surface in the confirmation that this narrows the audience.

---

## Step 5 — The exact call playbook (verified params)

Everything is created **paused by construction** — the create tools return entities in PAUSED state, so no status flag is needed (and none may be added). Order: campaign → ad set → ad. Confirm each write with the owner first (Hard rule 3); journal each confirmed create after (Step 6).

### `ads_create_campaign`
Required: `ad_account_id`, `campaign_name`, `objective`, `buying_type`.
- `objective` — ODAX outcome values only (`OUTCOME_SALES`, `OUTCOME_LEADS`, etc.). Legacy names (`CONVERSIONS`, `LEAD_GENERATION` as an objective, `LINK_CLICKS`) are rejected as objectives.
- `buying_type` — **always pass `"AUCTION"` explicitly** (the schema requires it).
- `special_ad_categories` — default `"[]"`.
- **CBO** (Validation, High Volume): set `campaign_daily_budget` (cents) here; leave `campaign_bid_strategy` default (`LOWEST_COST_WITHOUT_CAP`).
- **ABO** (Target Cost, Bid Cap): leave ALL of `campaign_daily_budget`, `campaign_lifetime_budget`, `campaign_bid_strategy` **unset** — any campaign budget field implicitly switches to CBO, and the ad-set-level bidding call is then rejected ("Must Use Campaign Bid Strategy").
- Campaign name convention: `[Type] - [Goal] - [BusinessName] - [Date]`.
- **Read the response's `valid_optimization_goals` / `recommended_optimization_goal` and treat them as authoritative** for the ad-set call. Pick the recommended goal; never hardcode one (especially never blindly `VALUE`).

### `ads_create_ad_set`
Required: `ad_account_id`, `campaign_id`, `ad_set_name`, `billing_event`, `optimization_goal`, `targeting`.
- `billing_event: "IMPRESSIONS"`.
- `optimization_goal` — use the value from the create-campaign response's `recommended_optimization_goal` (fallback: the Step 3 default). Must be valid for the parent objective. Default for both `OUTCOME_SALES` and `OUTCOME_LEADS` is `OFFSITE_CONVERSIONS`.
- `promoted_object` (JSON string) — **required** for `OFFSITE_CONVERSIONS` / `VALUE` / lead-form goals. Key is **`pixel_id`**. Examples: `{"pixel_id":"<id>","custom_event_type":"PURCHASE"}` (paid, default), `{"pixel_id":"<id>","custom_event_type":"COMPLETE_REGISTRATION"}` (free). Also required for an `OUTCOME_SALES` + WEBSITE combination even without a custom event (a bare `{"pixel_id":"<id>"}`), or the create is rejected with "Performance goal isn't available."
- `targeting: {"geo_locations":{"countries":[...]}}` — broad only, no age / interest fields.
- **ABO budget / bid (only when the parent campaign carries no budget):**
  - Target Cost: `daily_budget` (cents), `bid_strategy: "COST_CAP"`, `bid_amount = target_cpp × 0.7 × 100`.
  - Bid Cap: `daily_budget` (cents), `bid_strategy: "LOWEST_COST_WITH_BID_CAP"`, `bid_amount = bid_cap × 100`.
  - Passing any of these under a CBO parent is rejected server-side.
- EU/DSA: if `geo_locations.countries` includes an EU country, `dsa_beneficiary` and `dsa_payor` are required; they auto-fill from the business name if omitted (fine).

### `ads_create_ad`
Required: `ad_account_id`, `ad_set_id`, `ad_name`, `creative`.
- `creative` — JSON string with exactly one source:
  - New ad (default): `{"object_story_spec":{"page_id":"<PAGE_ID>","link_data":{"link":"<offer_url>","message":"<placeholder copy>"}}}`. `page_id` is mandatory inside `object_story_spec` (omitting it → "Facebook Page is Missing").
  - Bid-cap revival: `{"object_story_id":"<pageId_postId>"}`.
- The connection cannot upload media; the owner adds the real image / video and final copy in Ads Manager.

### Bid-cap revival read path (only when `is_queryable: true`)
`ads_get_ad_entities` at `level: "ad"`, `date_preset: "maximum"`, filtered to prior spend > 0 and prior results (validate field names via `ads_get_field_context` first — do not trust a static field list). Then `ads_get_creatives` re-called with `creative_ids` or `fields` to get `object_story_id` (a bare listing returns only `id` / `name` / `account_id` / `status`). A creative with no `object_story_id` cannot be revived this way; no old ads → suggest a creative test instead.

**Never call the activate-entity tool, and never set a status via `ads_update_entity`.** These are the two live-money switches (Hard rules 1–2).

---

## Step 6 — Journal every confirmed write, then verify it landed

A connected connection like this does not auto-journal, so record each write yourself, right after it's confirmed and created. Use the launcher's journal mode:

```bash
python ~/.claude/bos-run.py journal-write \
  --method mcp__meta-ads__ads_create_campaign \
  --path meta-ads/act_<id>/campaigns \
  --status ok --result-id <returned campaign id> \
  --body '{"objective":"...","daily_budget":"...","status":"PAUSED"}'
```

Use the matching `--method` for each create (`ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad`) and for any confirmed `ads_update_entity` edit.

**Journaling is best-effort, not a spend gate** — it can silently fail (journaling disabled, disk error, bad path). So after each confirmed create, **verify the line landed**: re-read today's `~/.claude/bos-journal/YYYY-MM-DD.jsonl` and confirm the returned `result_id` is present. If it isn't, tell the owner plainly that the audit record couldn't be written — don't assume success. The confirmation gate in Hard rule 3 is the real safety; this is the after-the-fact record that keeps the trail honest.

---

## Step 7 — PAUSED-shell creation, by campaign type

- **Validation (CBO):** campaign with `campaign_daily_budget`; ad set per Step 3; **three ad shells** — a product-image ad, a mockup ad, and a walkthrough-video ad — each a minimal `object_story_spec` with `page_id` + `link_data.link` + placeholder message.
- **High Volume (CBO):** as validation, **one ad shell**.
- **Target Cost (ABO):** campaign with no budget; ad set with `daily_budget` + `COST_CAP` + `bid_amount`; one ad shell. Then **offer** the dual campaign — a matching High Volume campaign with the same ads for comparison. Offer it, don't impose it (it doubles the shells); build the second only on an explicit yes, and confirm + journal it like any other create.
- **Bid Cap Revival (ABO):** pull old ads (Step 5 read path); campaign with no budget; ad set with `LOWEST_COST_WITH_BID_CAP` + `bid_amount`; recreate ads with `{"object_story_id":"pageId_postId"}`.

---

## Step 8 — Post-setup checklist + the 72-hour rule

After all creates, hand back this plain checklist (positive-led, the closing beat):

- **Upload your creatives:** image or video per ad (I can't upload files, so this bit's yours).
- **Add your ad copy:** the six-part copy from your plan, plus 2 to 3 short headlines.
- **Turn off enhancements:** Site Links off, Branding off, Promotions off.
- **Check the link** points to your exact offer page.
- **Validation only:** optionally duplicate the image ad with banner variations; save a creative folder.
- **Scale only:** duplicate the ad and swap creatives to test variations.
- **Bid cap only:** preview each revived ad, re-check the bid cap, and watch it daily for the first few days.
- **Review everything yourself:** budget, targeting, the result you're optimizing for, every setting.
- **Switch it on yourself:** here's your Ads Manager link. Give it a final look and flip it on when you're happy. I built it paused, so nothing spends until you do.
- **Then wait 72 hours:** that's the learning phase. Leave it alone; changing anything resets the learning.

---

## Tone and what to never do

- Plain, warm, direct. Name the win first. Never the words for the machinery under the hood — say "your ad account," "the connection," "your campaigns."
- ❌ Never turn an ad on, by any route (the activate-entity tool, or a status write on `ads_update_entity`).
- ❌ Never create or update anything without showing the exact settings and the spend implication first and getting a yes.
- ❌ Never batch writes behind one confirmation.
- ❌ Never exceed the confirmed spend ceiling without re-asking.
- ❌ Never fork or template this skill file per owner — the profile carries the per-owner detail.
- ❌ Never invent interest IDs or add age / interest targeting to a paused shell.
- ✅ Reads are free — look around freely before you build.
- ✅ Method is Evelyn Weiss's; build to the owner's plan.

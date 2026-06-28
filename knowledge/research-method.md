# Research method — the keyless web-research convention

**The standard keyless way BOS reads the live web is the hosted Firecrawl MCP.** It is already configured in `.mcp.json` (`https://mcp.firecrawl.dev/v2/mcp`) and needs **no API key** for `scrape`, `search`, and `interact`. That makes web research a genuine keyless capability: a brand-new owner can have a competitor read or a pre-call brief at zero accounts, no key.

This doc is the convention for every Increment-3 research app (e.g. `research-a-competitor`, `research-before-call`). No app is built here — this is the contract those apps follow so they pass the manifest rule and the onboarding binding check.

## The firecrawl driver id
A web-research app declares:

```yaml
function_slot: research
requires_credential: none
requires_driver: firecrawl
data_path: fetch_rest
```

`firecrawl` is in the onboarding binding check's keyless set (`tools/check-onboarding-binding.py` `_KEYLESS_DRIVERS`), so a firecrawl app counts as a real keyless instant-win. `data_path: fetch_rest` says it reaches a keyless hosted REST endpoint (not local reasoning, not a connected MCP).

## The keyless-MCP reconciliation (the one rule that looks contradictory)
There is a deliberate tension to resolve cleanly:

- The manifest rule (`tools/manifest.py`) **forbids** any `mcp__…` tool in the `uses_tools` of a `requires_credential: none` skill. A keyless skill that *declares* an MCP tool is lying about being keyless — that rule is what caught quote-from-photo quietly reaching into TrustPager.
- But the Firecrawl MCP genuinely **is** keyless. We want to use it from a keyless app.

**Resolution:** a firecrawl app does **NOT** list `mcp__firecrawl__…` in `uses_tools`. It calls the firecrawl MCP tools in the **body** of the SKILL.md instead (the same way `build-brand-strategy` and `start-here` already reference `firecrawl-scrape` / `firecrawl-search` in their prose). This is safe because:

- The manifest rule only inspects the declared `uses_tools` list — an empty/driver-only list passes.
- The binding check's **assertion C** (no hidden coupling in a `credential:none` body) only forbids **TrustPager** coupling tokens (`mcp__trustpager__*`, `dump-crm-bundle`, `dump-transcripts`, `api.trustpager.com`). A `firecrawl` body reference is **not** a coupling token, so it passes C cleanly.

So: **driver in the manifest, tools in the body.** `uses_tools` stays free of `mcp__firecrawl__…`; the skill body invokes the firecrawl skills/MCP tools directly.

## Scope clamp — HARD
Keyless covers **only** these three operations. Use nothing else in a floor research app:

- ✅ `scrape` — one URL → clean content
- ✅ `search` — a query → results (+ optional page content)
- ✅ `interact` — click / fill / navigate a live page

**OUT of floor scope (these need a paid `FIRECRAWL_API_KEY`):**

- ❌ `crawl` — bulk multi-page extraction
- ❌ `map` — list every URL on a domain
- ❌ `agent` — autonomous structured extraction
- ❌ `extract` — schema-driven structured extraction

A floor research app that needs `crawl`/`map`/`agent`/`extract` is not keyless and does not belong on the floor. Keep research apps to `scrape`/`search`/`interact`.

## Offline (`BOS_OFFLINE`) accommodation
Firecrawl apps are **network** — they reach a live REST endpoint, unlike the reasoning-only and local (doclib/markitdown) apps. So the offline suite cannot fetch. The accommodation for a firecrawl app's unit tests:

- **Mock or skip the fetch.** Never make a real network call in a test.
- **Test the synthesis / shape logic**, not the network: feed the synthesis step a canned/fixture page payload and assert the app produces the right structured output (the one-page competitor read, the pre-call brief shape).
- **Flag the network dependency in the SKILL.md** so it is honest about needing connectivity at runtime (keyless ≠ offline; it is keyless-but-online).

This keeps `BOS_OFFLINE=1 python -m unittest discover -s tests` green even though the live capability is network-bound.

## Positive-only outputs
Like every floor app, the customer-facing OUTPUT a research app produces (the competitor read, the brief) follows the positive-only rule and uses no em dashes. Naming a rival's gap is fine as a sharp-operator observation; framing the owner's own position by what they lack is not.

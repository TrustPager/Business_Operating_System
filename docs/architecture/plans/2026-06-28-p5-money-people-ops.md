# P5 — MONEY + People-Ops Floor Implementation Plan

> **For agentic workers:** Execute via superpowers:subagent-driven-development (fresh subagent per task + spec review + quality review). Run in a `p5-money` worktree. **Every task's gate:** the relevant skill lints clean + manifest valid (`python tools/manifest.py skills/<name>/SKILL.md`), `python tools/registry-generator.py --check` is fresh, `python tools/check-onboarding-binding.py` exits 0, `python tools/check-no-secrets.py` passes, and `BOS_OFFLINE=1 python -m unittest discover -s tests` is green. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the keyless MONEY floor as a correctness step-change over plain Claude Code: universal business-math apps backed by a tested financial-calculation library, plus an Australia-only regional pack (BAS, GST, super) compiled from official published data and locked behind an explicit, owner-confirmed `region: AU` gate. People-ops is already shipped (`write-a-job-ad`, `write-a-policy`); this plan adds the money cluster and `renewal-tracker`.

**Architecture:** Three correctness pillars, none of which plain Claude can do: (1) `numpy-financial` (BSD, local pip) as a thin `tools/` calc wrapper so loan, depreciation, NPV/IRR math is library-correct, not arithmetic-in-the-head; (2) a versioned AU constants data module compiled from gazetted ATO and Fair Work sources, each value carrying its source URL and effective date, so the partner cites the real figure instead of guessing; (3) `tools/write_xlsx.py` (already built) so each money app produces a living spreadsheet, not a chat answer. Region is modelled exactly like a driver: a new optional `requires_region` manifest key plus a runtime/binding gate, defaulting absent. The universal core works at any region with no region set; the AU pack stays fully dark until the owner explicitly confirms Australia.

**Tech stack:** Python stdlib (kernel/tools), `numpy-financial` (BSD, install-on-first-use like the doc libs), the existing doc-lib-set wrappers (`tools/write_xlsx.py`, `tools/make_pdf.py`), Markdown skills + flat manifests, the offline harness (`BOS_OFFLINE`, `lint-skill.py`, `manifest.py`, `check-onboarding-binding.py`).

**Source specs (locked):** [`founder-decisions.md`](../founder-decisions.md) D7 (location-agnostic core + opt-in regional pack), D9 (registry-bound onboarding), D10 (token-frugal connected tier), D13 (lean zero-state, heavy/optional in a library); [`implementation-roadmap.md`](../implementation-roadmap.md) P5; [`floor-roster.md`](../floor-roster.md); [`manifest-schema.md`](../manifest-schema.md). The reshape and the keyless-tool search that justify this plan are recorded in the session that produced it.

---

## Cross-cutting rules (apply to every task)

- **The bar:** every app must give the owner something Claude Code alone cannot: a gazetted figure with an effective date, library-correct financial math, or a maintainable `.xlsx`. A pure reasoning restatement of arithmetic does not ship.
- **Strict AU gate (founder directive):** nothing AU-specific is reachable unless the owner has **explicitly confirmed** their business is in Australia. Region is never inferred from language, timezone, currency, or address. It is set only by an explicit yes to a direct question and recorded in the profile. The constants module never loads, and AU apps never surface, until that flag is set. **`Region: AU` is the ONLY signal any AU code path, skill, or onboarding surface may key on.** The pre-existing free-text "I'm based in `<<< city, country >>>`" line in `templates/CLAUDE.md` is NOT a region signal and must never be read to infer region, even if it names an Australian city. A profile that says "based in Sydney" but has no `Region: AU` line keeps every AU tool off.
- **Never invent a rate or a rule.** Every AU constant is copied from an official ATO or Fair Work page and stored with its source URL and last-updated date. If a figure cannot be sourced, it is left out and flagged, never guessed. The same discipline `price-my-work` applies to costs applies here to statutory figures.
- **We prepare figures, the owner lodges.** No app files, lodges, or submits anything to a tax authority. `estimate-my-bas` prepares the numbers for the owner to enter themselves (D7).
- **Positive-only language** on every customer-facing OUTPUT (pain-naming is fine inside the app's own discovery prompts). **No em dashes** in any content (the mechanical guard enforces this on doc-write output; keep skill bodies clean too).
- **Keyless + offline:** every app here is `reasoning_only` or `local` and must be `BOS_OFFLINE`-green. No network, no key, no account.
- **MIT/BSD/MPL only:** `numpy-financial` is BSD-3-Clause. Record the license boundary. No AGPL/GPL.
- After any manifest/skill/constants change, **regenerate `kernel/registry.json` in the same commit** (the drift guard fails otherwise) and **update `floor-roster.md` statuses**.

---

## Increment 1 — Infrastructure (build first; everything rides on these)

> Sequential. These touch `tools/`, the manifest contract, the binding check, and `registry.json`. Each is its own task + two-stage review.

### Task 1.1 — `requires_region` manifest key (the gate, data-driven)

**Files:**
- Modify: `tools/manifest.py` (add the optional key + validation)
- Modify: `docs/architecture/manifest-schema.md` (document it)
- Test: `tests/test_manifest_region.py` (create)

- [ ] **Step 1: Write the failing tests.** A manifest with `requires_region: AU` validates clean; `requires_region: none` (or absent) validates clean; `requires_region: xx` (not an allowed region) returns an error; the value must be a scalar, not a list.

```python
# tests/test_manifest_region.py
from tools.manifest import validate_manifest

BASE = {
    "function_slot": "money", "requires_driver": "none",
    "requires_credential": "none", "data_path": "reasoning_only",
}

def test_region_au_ok():
    assert validate_manifest({**BASE, "requires_region": "AU"}) == []

def test_region_absent_ok():
    assert validate_manifest(BASE) == []

def test_region_unknown_rejected():
    assert validate_manifest({**BASE, "requires_region": "xx"})
```

- [ ] **Step 2: Run to verify failure.** `python -m unittest tests.test_manifest_region -v` → FAIL (`requires_region` is treated as an unknown key today).
- [ ] **Step 3: Implement.** In `tools/manifest.py`: add `requires_region` to the allowed optional keys; allowed values are a small region set `{"AU"}` plus the absent/`none` default (start with AU only — YAGNI; the set extends when a second region ships). Validate it is a scalar in the allowed set when present.
- [ ] **Step 4: Run to verify pass.** `python -m unittest tests.test_manifest_region -v` → PASS.
- [ ] **Step 5: Document.** Add a `requires_region` row to the `manifest-schema.md` contract table (optional; allowed values `AU` or absent; "region is modelled like a driver per D7; an app with `requires_region` only surfaces once the profile confirms that region").
- [ ] **Step 6: Commit.** `feat(p5): add requires_region manifest key (the AU gate, data-driven)`

### Task 1.2 — binding-check region honesty + registry passthrough

**Files:**
- Modify: `tools/registry-generator.py` (carry `requires_region` into `registry.json`)
- Modify: `tools/check-onboarding-binding.py` (a region-gated app may not be offered as a universal keyless cold win)
- Test: `tests/test_binding_region.py` (create)

- [ ] **Step 1: Write the failing test.** An app with `requires_region: AU` that is referenced as a plain keyless cold-win offer in `start-here`/`starter-projects` is a binding error; the same app referenced under an explicitly AU-gated section is fine. (Model this on the existing keyless-honesty assertion in `_check_keyless_honesty`.)
- [ ] **Step 2: Run to verify failure.** `python -m unittest tests.test_binding_region -v` → FAIL.
- [ ] **Step 3: Implement.** (a) In `registry-generator.py`, pass `requires_region` through to each registry entry (default omitted/`none`). (b) In `check-onboarding-binding.py`, add assertion D with a **concrete, recognizable marker** mirroring the existing `_CONNECTED_TIER_TAGS` / `_PLANNED_HEADING_RE` machinery: define an `_AU_GATED_HEADING_RE` (the AU-gated subsection heading in `starter-projects.md`) and/or a `requires_region:au` row tag. Assertion D: an app whose registry entry has `requires_region` set is valid **only** when every reference to it sits inside an AU-gated marked context; a `requires_region` app referenced in any unmarked keyless-offer context **fails D**. **D must override B** (`estimate-my-bas` is technically keyless under `_is_keyless()` since it is `credential:none` + `requires_driver:none`, so without the override B would wave it through anywhere) — a `requires_region` app is rejected from any unmarked keyless offer even though it is keyless. Keep the existing A/B/C assertions intact.
- [ ] **Step 4: Run to verify pass + regenerate.** Tests PASS; `python tools/registry-generator.py` then `--check` is fresh.
- [ ] **Step 5: Commit.** `feat(p5): region-gated apps carry into registry and pass binding only when AU-gated`

### Task 1.3 — `finance_calc` tool over numpy-financial (library-correct math)

**Files:**
- Create: `tools/finance_calc.py` (argparse CLI mirroring `tools/markitdown_convert.py`'s shape: subcommands, `INSTALL_HINT`, clean exit codes)
- Modify: `tools/README.md` (document the new tool + its license boundary)
- Test: `tests/test_finance_calc.py` (create)

- [ ] **Step 1: Write the failing tests.** Cover only the functions a shipping P5 app actually consumes, with known-answer fixtures: `pmt` (loan/equipment repayment) and depreciation `sln` (prime-cost) + `ddb`/`db` (diminishing-value). Also assert the missing-library path prints the BSD `pip install numpy-financial` hint and exits 2. **`npv`/`irr` are deliberately OUT of P5 scope** (no P5 app consumes them per the over-build rule in Step 5); they are deferred to the future multi-month investment-view app, where they belong. Do not build them here.

```python
# tests/test_finance_calc.py — illustrative known-answer
def test_pmt_known_value():
    # $30,000 over 60 months at 7.5% p.a. -> ~ -601.07/month
    from tools.finance_calc import pmt
    assert round(pmt(0.075/12, 60, 30000), 2) == -601.07
```

- [ ] **Step 2: Run to verify failure.** `python -m unittest tests.test_finance_calc -v` → FAIL.
- [ ] **Step 3: Implement.** Thin wrappers over `numpy_financial.{pmt,ipmt,ppmt}` and depreciation (`sln`, `db`, `ddb`) — the set `profit-per-job` consumes. (`npv`/`irr` deferred per Step 1.) Install-on-first-use: if the import fails, print the one-line hint and exit 2 (the SKILL layer turns that into the detect→offer→do-on-yes→verify loop per D11). No network at runtime → `local`/`BOS_OFFLINE`-green once installed. Expose both a Python API (for tests) and a CLI (for skills).
- [ ] **Step 4: Run to verify pass.** Tests PASS (install `numpy-financial` locally for the run).
- [ ] **Step 5: License note + load-bearing check.** Record in `tools/README.md` that `numpy-financial` is BSD-3-Clause (MIT/BSD/MPL-clean). Confirm at least one shipped app exercises `finance_calc` on a known-answer path so the wrapper is demonstrably load-bearing, not built for show: the concrete consumers are `profit-per-job`'s equipment-finance `pmt` + depreciation (Task 2.1), where library-correct math genuinely beats LLM arithmetic. If no app reaches it, the wrapper is over-built and should be cut back.
- [ ] **Step 6: Commit.** `feat(p5): finance_calc wrapper over numpy-financial (pmt/npv/irr/depreciation)`

### Task 1.4 — AU regional constants module (versioned, sourced, gated)

**Files:**
- Create: `drivers/regional/au/constants-FY2026-27.json` (the data; FY-versioned filename)
- Create: `drivers/regional/au/README.md` (provenance: every value's source URL + effective date + the update procedure)
- Create: `tools/regional.py` (a tiny loader: `load_au_constants()` returns the parsed module; refuses to load unless called with an explicit `region="AU"` argument — defence in depth so nothing loads it by accident)
- Test: `tests/test_regional_au.py` (create)

- [ ] **Step 1: Decide and document the scope (in the README first).** Bundle only what is small, stable enough to version, and genuinely authoritative:
  - GST rate; the Simpler-BAS field map (G1 total sales, 1A GST on sales, 1B GST on purchases) and the calc method.
  - Super guarantee rate (current FY) + key super thresholds.
  - Resident income-tax brackets + Medicare levy rate; FBT rate.
  - National minimum wage + casual loading (full per-award rates are 122 awards and are NOT bundled — they are the connected-tier FWC API deepener, Increment 4).
  Each entry stores `value`, `effective_from`, `source_url`, `retrieved_on`. PAYG withholding schedules are NOT embedded (too large/volatile); reference the ATO tax-withheld calculator instead. **Labelled divergence from roadmap P5 (line 104, which names PAYG as part of a "complete" AU pack):** embedding full PAYG schedules is an intentional narrowing for honesty and size; the pack ships GST/super/BAS/income-tax-brackets complete and points to the official ATO calculator for PAYG withholding. The live FWC/ABS APIs (Increment 4) are the path to award-accurate and PAYG-live data on connect.
- [ ] **Step 2: Write the failing tests.** The JSON parses; every entry has the four provenance fields; `gst_rate` is present; the BAS field map has G1/1A/1B; `tools.regional.load_au_constants(region="AU")` returns the module and **raises/returns empty for any other region** (the gate at the data layer).
- [ ] **Step 3: Run to verify failure.** `python -m unittest tests.test_regional_au -v` → FAIL.
- [ ] **Step 4: Compile the data from official sources.** Pull each figure from the gazetted ATO / Fair Work pages (e.g. ATO "Key super rates and thresholds", individual income tax rates, GST; Fair Work national minimum wage). Record the source URL + retrieved date for each. **Do not invent or approximate any value.** If FY2026-27 figures are not yet published for an item, store the current published FY and note it.
- [ ] **Step 5: Implement the loader + run tests.** `tools/regional.py` loads the JSON only when `region="AU"`. Tests PASS.
- [ ] **Step 6: Secret scan + commit.** `python tools/check-no-secrets.py` passes (it is open public data, no secrets). `feat(p5): AU regional constants module (FY-versioned, sourced, region-gated loader)`

---

## Increment 2 — Universal money apps (any region; no region set required)

> Each is a new skill `skills/<name>/SKILL.md` with `function_slot: money`, `requires_driver: none`, `requires_credential: none`, `data_path: reasoning_only`, no `requires_region`. Mirror `skills/price-my-work/SKILL.md` for shape (read-back-before-compute, assumptions written down, hard rules, positive-only). Each MAY call `tools/finance_calc.py` for exact math and `tools/write_xlsx.py` for the artifact. After building, promote in `knowledge/starter-projects.md` + route from `start-here`, regenerate the registry, update the roster.
>
> **Labelled divergence from roadmap P5 (line 103, which lists `cash-flow-forecast`, `profit-per-job`, `expense-sense`, budgeting/margin):** "margin" folds into `profit-per-job` (Task 2.1) and "budgeting" folds into `cash-flow-forecast` (Task 2.2). **`expense-sense` is cut**, not built: as a `reasoning_only` "categorize and trim my expenses" app it is the closest thing in P5 to a vanilla-Claude restatement and fails the bar. Expense categorisation worth shipping is AU-deduction-aware, which belongs in the AU pack on the constants module, not the universal core; revisit it there only if a real gap appears. This keeps the universal core to the two apps that clear the bar via a living `.xlsx` + library-correct math.

### Task 2.1 — profit-per-job (slot: money)

The owner picks one job type and their typical revenue, direct costs, and a share of overheads; the app returns true profit per job and the margin, with an overhead-recovery method stated (not buried), and offers a reusable `.xlsx` model pre-filled from the figures (and from `price-my-work` rates when present). Folds in the "margin" concern so no separate margin app is needed. **This is the load-bearing consumer of `finance_calc` (Task 1.3):** when a job depends on financed equipment, it computes the per-job equipment cost from `pmt` (loan/equipment repayment) and a depreciation schedule (`sln` prime-cost / `ddb` diminishing-value), which is exactly where library-correct math beats LLM arithmetic. **Clears the bar via:** a maintainable spreadsheet model + a consistent overhead-recovery method + correct finance/depreciation math, not a one-off chat sum. **Acceptance:** a defensible per-job profit with the equipment-finance/depreciation path exercised via `finance_calc` + an optional `.xlsx`, keyless; positive-only; gates green.

### Task 2.2 — cash-flow-forecast (slot: money)

Opening balance + expected inflows and outflows over a clamped 4-13 week horizon → a week-by-week running-balance forecast that flags the tightest week, output as a live `.xlsx` with formulas the owner maintains (not a static table). Folds in "budgeting". **No NPV here** (discounting over a sub-3-month horizon is near-noise and would be numpy-financial used for show, not correctness; NPV/IRR belong in a multi-month investment view, not a 13-week running balance). **Clears the bar via:** a living formula-driven spreadsheet the owner keeps and updates, well beyond a chat estimate. **Acceptance:** a week-by-week `.xlsx` forecast (real formulas, not a static table) with the tight week called out, keyless; positive-only; gates green.

### Task 2.3 — renewal-tracker (slot: documents)

Licenses, insurances, certifications, and registrations the owner lists → a clean `.xlsx` tracker. **The `.xlsx` is the required deliverable here (not optional, unlike profit-per-job): the win IS the file, never a chat table** — otherwise this app is a reasoning restatement and fails the bar. The sheet is a living model: a formula-driven "days until renewal" column and a conditional sort so the soonest renewal floats to the top and stays correct every time the owner opens it. Honest split: the keyless win is the maintainable tracker file; the connect tier (a CRM/calendar driver) is what actually *fires* the reminders, described as the deepener, never oversold. **Acceptance:** a formula-driven `.xlsx` renewal tracker (days-until-renewal + soonest-first sort) as the required output, keyless; the reminder-firing deepener is described as connect-time; gates green.

---

## Increment 3 — AU regional pack (gated behind explicitly-confirmed region: AU)

### Task 3.1 — estimate-my-bas (slot: accounting; requires_region: AU)

**Manifest:** `function_slot: accounting`, `requires_driver: none`, `requires_credential: none`, `data_path: reasoning_only`, `requires_region: AU`, `status: active`.
The owner provides their quarter's sales and purchases (or points at a `cash-flow`/spreadsheet output); the app uses `drivers/regional/au` (loaded only because region is AU) to prepare Simpler-BAS G1/1A/1B figures with the GST method shown, and an optional `.xlsx`. **Body gate (the skill-body layer of the gate, not just prose):** the skill's first step reads the `Region:` line from the profile and, if it is not `AU`, politely declines and stops (no constants loaded), even if the profile's free-text city/country names an Australian place. The data-loader gate (`load_au_constants(region="AU")`, Task 1.4) is the hard backstop so even a body slip cannot load AU figures for a non-AU caller. **Other hard rules in the body:** prepare-only, never lodge; cite the GST rate's source + effective date from the constants module; if the figures look out of FY range, say so. **Clears the bar via:** gazetted GST + the official BAS field mapping, which the model cannot reliably reproduce from memory. **Tests:** a fixture asserting the body refuses for a non-AU (and a missing-`Region:`) profile, and prepares correctly for `Region: AU`. **Acceptance:** correct G1/1A/1B preparation from typed figures, sourced + dated, prepare-only, keyless; the body refuses without `Region: AU`; gates green; the app does NOT surface for a non-AU profile.

### Task 3.2 — region confirmation + AU-gated onboarding wiring

**Files:** `skills/start-here/SKILL.md` (add the explicit region question + the gate), `templates/CLAUDE.md` (a clear `Region:` profile line), `knowledge/starter-projects.md` (an AU-gated subsection), `knowledge/industry-notes.md` if a shape reference needs it.

- The region question is **explicit and opt-in**: a plain "Is your business based in Australia? (I only turn on Australian tax tools if you say yes.)" Never inferred. Recorded as a `Region:` line in the owner's `./CLAUDE.md`.
- **Neutralize the pre-existing inference leak (review issue 1):** `templates/CLAUDE.md` line 21 captures location as free text ("I'm based in `<<< city, country >>>`"). Add a one-line note next to it that this is descriptive only and does NOT switch on any region-specific tools, and add an explicit `Region:` line (default unset) as the single machine-read region field. `start-here` and every AU skill body must key on `Region:` ONLY, never the city/country prose. State this in the task so no reader treats "Sydney" as consent.
- Universal money apps (Increment 2) are offered to everyone from the start. `estimate-my-bas` and any future AU app are offered **only** in the AU-gated subsection, surfaced only once `Region: AU` is confirmed.
- The binding check (Task 1.2 assertion D) enforces that the AU app is never listed as a universal cold win. **Acceptance:** a fresh non-AU owner never sees an AU app; confirming AU reveals `estimate-my-bas`; binding check green.

---

## Increment 4 — Connected-tier deepeners (named, deferred; do NOT build here)

These are real upgrades but require accounts/keys, so they are out of the keyless floor and gated behind both `region: AU` and a connection. Named so the design is on record; they ride on the P7/P8 connection work and the D10 token investigation.

- **Fair Work MAPD API** (registration + subscription key): live per-award rates, allowances, penalties, and change notifications. Turns the bundled national-minimum-wage snapshot into self-updating award-accurate data. Connect-tier refresh for the wage side of the constants module.
- **ABS Indicator API** (API key): live economic indicators (e.g. CPI) for indexing and benchmarks. Optional connect-tier enrichment for `cash-flow-forecast`.

---

## Definition of done (P5)

- [ ] `requires_region` is a validated optional manifest key; it carries into `registry.json`; the binding check forbids a region-gated app from being offered as a universal keyless win.
- [ ] `tools/finance_calc.py` wraps numpy-financial (pmt + depreciation; `npv`/`irr` deferred to the future investment-view app) with known-answer tests and a graceful missing-library path; BSD license recorded; every wrapped function is consumed by a shipping P5 app.
- [ ] The AU constants module exists, FY-versioned, with every value carrying a source URL + effective date; its loader refuses any non-AU region; no value was invented.
- [ ] `profit-per-job`, `cash-flow-forecast`, and `renewal-tracker` ship keyless, each producing a real `.xlsx`, each offered to all owners; positive-only; `BOS_OFFLINE`-green.
- [ ] `estimate-my-bas` ships keyless and prepare-only, sourced + dated, and surfaces only for an explicitly-confirmed AU profile; its body refuses without `Region: AU`.
- [ ] The AU gate is enforced at every layer: manifest (`requires_region`), registry passthrough, binding check (assertion D, overriding B, with a concrete marker), onboarding surface (AU-gated subsection only), skill body (reads `Region:` only), and the data loader (`region="AU"` backstop). The free-text city/country line is neutralized as an inference source.
- [ ] `start-here` asks the region question explicitly (never inferred) and records `Region:` in the profile; AU apps live only in the AU-gated onboarding subsection.
- [ ] Roadmap-P5 divergences are labelled, not silent: "margin" folded into profit-per-job, "budgeting" into cash-flow-forecast, `expense-sense` cut (fails the bar), PAYG schedules referenced to the ATO calculator rather than embedded.
- [ ] People-ops confirmed already complete (`write-a-job-ad`, `write-a-policy`); no new build there.
- [ ] `floor-roster.md` updated; registry fresh; every skill lints clean; secrets + kernel-clean + binding + offline suite all green.
- [ ] Connect-tier deepeners (FWC MAPD, ABS Indicator) recorded for P7/P8, not built here.

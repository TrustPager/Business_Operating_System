# Tier-1 Connected Add-on Kit — the reusable system for building connected add-ons

**Status:** Draft for review. Design direction founder-approved in brainstorming
(2026-07-03): full kit (recipe + generalized gate + conformance check +
templates), structure enforced by a conformance check, pre-existing drivers
grandfathered. Pending the spec-review loop and a founder read before planning.

**One-line:** Turn the shipped Meta Ads add-on from a one-off into a reusable,
safe-by-construction system: a codified recipe, a driver-kind taxonomy, one
CI-enforced gate that reads each connected driver's own declarations for both
safety and structural conformance, and copyable templates, so every future
connected add-on (Vercel next) is near-mechanical to build and cannot ship
half-wired or unsafe.

Grounded in the 2026-07-03 four-agent review of the Meta Ads add-on
([2026-07-03-meta-ads-addon-design.md](2026-07-03-meta-ads-addon-design.md)),
which distilled the reusable pattern and found the safety gate had shipped
orphaned. Sibling of the existing reusable-recipe precedent
[trustpager-to-floor-extraction.md](trustpager-to-floor-extraction.md).

---

## 1. Why

The Meta Ads add-on ([`plan-my-ads`](../../skills/plan-my-ads/SKILL.md) floor +
[`run-my-ads`](../../skills/run-my-ads/SKILL.md) connected, over the folderless
`meta-ads` `claude_mcp` driver) is a strong, convention-aligned reference for a
connected add-on. But it is a *reference*, not a *system*: the next add-on author
has to reverse-engineer the pattern from it, and two review findings show the
one-off is fragile:

- **The safety gate shipped orphaned.** `tools/check-ads-safety.py` was absent
  from CI, tests, and the pre-push hook, so the never-activate guarantee was
  documentation-only. (Wired into CI on `feat/meta-ads-addon` as commit
  `508c16a`; this kit generalizes it.)
- **`never_call`/`never_set` live in two homes** (the driver `DRIVER` dict AND
  the checker), with nothing syncing them, an anti-drift violation.
- **`requires_driver` is unvalidated**, so a typo'd driver id passes manifest
  validation silently and only fails at runtime.

Goal: make a connected add-on **near-mechanical to build and safe by
construction**. An author copies a template, fills a checklist, and one gate
proves both the structure and the safety before it can ship.

## 2. What ships (four artifacts)

1. **The recipe** — `docs/architecture/tier-1-addon-kit.md`, the one home for how
   to build a connected add-on.
2. **The driver-kind taxonomy** — five kinds, declared in each driver's `DRIVER`
   dict `kind` field and documented in the recipe.
3. **The gate** — `tools/check-connectors.py` (generalized from
   `check-ads-safety.py`): one CI check that reads each opted-in connected
   driver's `DRIVER` dict and enforces both safety and structural conformance.
4. **The templates** — `drivers/_template/` (docs-only driver skeleton) plus the
   two skill-frontmatter contracts and the connectors-card snippet embedded in
   the recipe.

## 3. The recipe (`docs/architecture/tier-1-addon-kit.md`)

Codifies, as a mechanical checklist, exactly what the review distilled. It
*points at* the meta-ads add-on as the worked example and at the owning docs
rather than restating them (one home per fact):

- **Plan/run seam:** a keyless floor "thinking" skill (writes a portable
  artifact, works under `BOS_OFFLINE`) + a connected "doing" skill (reads that
  artifact, calls the driver's tools). Split purely by manifest.
- **The two frontmatter contracts.** Floor: `requires_driver: none` /
  `requires_credential: none` / `data_path: reasoning_only` (or `local`), no
  `uses_tools`, no `mcp__*` in the body. Connected: `requires_driver: <id>` /
  `requires_credential: mcp` or `key` / `data_path: mcp_tools` or `local`, with
  an exhaustive `uses_tools`, and any irreversible tool **deliberately omitted**
  from `uses_tools` so lint fails the build if the body names it.
- **The folderless documentation-only driver** (for `claude_mcp`): `DRIVER` dict
  + docstring stating nothing reads it. Load-bearing artifacts are only the
  `requires_driver` string, `connect.md`, and the `connectors.md` card.
- **`connect.md`** = single home for connect steps (fixed shape). **The
  `connectors.md` card** (fixed schema). **The labelled `connect-a-tool`
  override** when the add-mechanism differs from the default in-app `/mcp` flow.
- **The guided intake** (Source A/B/C/D): read `brand.json` (A) + `./CLAUDE.md`
  (B) silently, ask only the small add-on-specific bucket (C), auto-fill and
  confirm from one live read (D); write a `~/.claude/bos-cache/<addon>-profile.json`;
  fold the driver's `OPERATING-CONTEXT.md` into `./CLAUDE.md` with the skill's own
  no-clobber merge (does not call `learn-my-business`, which is CRM-gated).
- **Personalization is DATA, never a forked skill file.**
- **Layered write-safety** (confirm-before-every-write is the real gate; journal
  + verify; never-do declarations), carried *only* when the driver has a money or
  irreversible surface.

## 4. The driver-kind taxonomy

Every driver that opts into the kit declares a `kind` in its `DRIVER` dict:

| kind | What it is | Example | Shape |
|---|---|---|---|
| `claude_mcp` | Owner-hosted OAuth MCP the Claude client hosts | `meta-ads` | Folderless docs-only; connect.md; no Python transport |
| `keyed_cli` | A keyed local CLI invoked via Bash | Vercel (planned) | Docs-only `DRIVER` dict + `secret_pattern`; connect.md; no DriverConfig |
| `keyed_rest` | Keyed REST API with a Python transport | `trustpager` | `DriverConfig` + auth/catalog (the CRM core; grandfathered, see §7) |
| `keyless` | No account, runs locally or reads the open web | `firecrawl`, `render` | Grandfathered, see §7 |
| `data_pack` | Region/data bundle, no connection | `regional/au` | Grandfathered, see §7 |

The recipe documents all five so an author picks one. The gate (§5/§6) only
enforces on drivers that ship a `DRIVER` dict; connected kinds (`claude_mcp`,
`keyed_cli`) get the full structural checks.

## 5. The gate — `tools/check-connectors.py` (safety, generalized)

Generalize `check-ads-safety.py` into `tools/check-connectors.py`. Instead of
hard-coding `NEVER_CALL_TOOLS` / `NEVER_SET_ACTIVE`, it:

- Discovers each `drivers/*/__init__.py`, **`ast`-parses** the top-level `DRIVER`
  dict literal (static parse, no import, so the gate still runs anywhere with
  stdlib only and pulls in no vendor code).
- For every `DRIVER` dict carrying `never_call` / `never_set`, greps all skill
  bodies for a violation (a forbidden tool call, or a status-ish field set to a
  live value), exactly the current ads logic but data-driven.

**Meta-ads retrofit (the only legacy touch):** delete the redeclared
`NEVER_CALL_TOOLS` / `NEVER_SET_ACTIVE` from the checker; the values already exist
in `drivers/meta-ads/__init__.py`'s `DRIVER` dict, which becomes the single
source. Kills the two-homes duplication.

The CI step added in `508c16a` stays, its `run:` line pointing at the generalized
tool (renamed step: "Connector safety + conformance").

## 6. The gate — conformance (same tool)

`check-connectors.py` also validates each driver that ships a `DRIVER` dict:

- `kind` is present and in the taxonomy (§4).
- `requires_driver` on any skill resolves to a real `drivers/<id>/` (closes the
  typo-passes-silently hole). Reported per offending skill.
- For **connected** kinds (`claude_mcp`, `keyed_cli`): a `connect.md` exists in
  the driver folder, and a `## <display_name>` card exists in
  `knowledge/connectors.md`.
- The floor/connected **frontmatter contracts** hold for the add-on's skill pair
  (floor is keyless-clean; connected declares its driver + an exhaustive
  `uses_tools`).

A half-built connected add-on fails CI. Keyless/data-pack kinds that later adopt
a `DRIVER` dict are validated for `kind` + docstring only (they do not connect,
so connect.md/card are not required of them).

## 7. Scope / grandfathering (founder-ruled 2026-07-03)

The gate keys off the presence of a new-style `DRIVER` dict. Today only
`meta-ads` has one, so **only meta-ads is in scope**; Vercel joins when it ships
its `DRIVER` dict. **The pre-existing drivers are grandfathered:**

- `trustpager` (the CRM core) keeps its `DriverConfig` + auth/catalog shape. It is
  the platform, not a "tier-1 add-on", and is explicitly out of the add-on kit.
- `firecrawl` / `render` / `markitdown` (keyless) and `regional` (data pack) and
  `_noop` keep their current shapes. Forcing them into the connected-add-on
  template would be a category error (they do not connect) and a needless sweep.

The taxonomy documents their kinds for completeness; the gate does not require
them to adopt a `DRIVER` dict. (A future full normalization is a non-goal, §10.)

## 8. Templates

- `drivers/_template/` — a docs-only skeleton (the `_` prefix matching `_noop`):
  `__init__.py` with a fully-commented `DRIVER` dict (id, kind, display_name,
  server_url/cli, tool_prefix, connect_doc, credential, read_only_scope_first,
  and optional `never_call`/`never_set`), plus `connect.md`, `OPERATING-CONTEXT.md`,
  and `README.md` stubs following the meta-ads shapes.
- The two skill-frontmatter contracts and the connectors-card snippet live in the
  recipe doc (one home), not as separate stub files.

## 9. Wiring + validation

- **CI:** the `508c16a` step's `run:` becomes `python tools/check-connectors.py`;
  rename the step. No other `.github/workflows/test.yml` change.
- **Offline tests** (`tests/test_check_connectors.py`, `BOS_OFFLINE=1`, unittest):
  fixtures under `tests/fixtures/connectors/` for a good add-on (passes) and
  broken ones that each fail exactly one rule: invalid `kind`, unresolved
  `requires_driver`, missing `connect.md`, missing card, a `never_call` tool named
  in a body, a `never_set` field set live. Assert the checker reports each.
- **Dogfood:** `check-connectors.py` passes clean against the real `meta-ads`
  add-on, and fails against a deliberately-broken fixture with a clear message.
- **Retrofit safety:** after deleting the checker's hard-coded lists, re-run
  against meta-ads to confirm the `DRIVER`-dict-sourced values still catch the
  same violations (parity with `508c16a`).
- **Branch:** built on `feat/tier1-addon-kit`, stacked off `feat/meta-ads-addon`
  (it depends on the meta-ads driver + the `508c16a` CI wiring). Vic merges the
  chain: `feat/meta-ads-addon` first, then this.

## 10. Non-goals (YAGNI)

- No full sweep of the legacy drivers into the taxonomy (founder-ruled; §7).
- No scaffolding/codegen script (the template + recipe are copied by hand).
- Not the D13 off-the-shelf library subsystem, and not the D10 connected-tier
  token investigation (both separate follow-ups).
- No change to `kernel/*`, `manifest.py`, or `registry-generator.py` beyond
  (optionally) validating `requires_driver` resolution, which the new gate does
  externally rather than in the manifest validator.

## 11. Open questions for the plan

- Whether `requires_driver` resolution should also be enforced in
  `tools/manifest.py` (belt-and-suspenders) or only in `check-connectors.py`. Lean
  gate-only to keep the manifest validator lean; confirm during planning.
- Exact home for the connect-doorway articulation ("here is X keyless, enhanced by
  Y, unlocked with Z") if not already single-homed by the meta-ads work in
  `knowledge/connectors.md` (reconcile with the site-builder's Task 2.5).
- Whether the recipe supersedes or cross-links `trustpager-to-floor-extraction.md`
  (they are adjacent: one is floor-extraction, one is connected-add-on authoring).

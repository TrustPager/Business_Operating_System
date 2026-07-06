# Tier-1 Connected Add-on Kit — how to build a connected add-on

The recipe for taking a business capability that needs a live outside account
(ad platform, deploy host, and the like) and shipping it as a connected add-on
that is safe by construction and near-mechanical to build. Fill the checklist,
copy the shapes, and one gate (`tools/check-connectors.py`) proves both the
structure and the safety before it can ship.

This is the sibling of [`trustpager-to-floor-extraction.md`](trustpager-to-floor-extraction.md).
That recipe is about giving the keyless floor a genuine version of a paid
capability. This one is the other half of the same story: how the *connected*
version of a capability is built once the owner is ready to plug their own
account in. The two meet at the plan/run seam below.

**Worked example (built), pointed at throughout, never restated:** the Meta Ads
add-on. Keyless floor [`plan-my-ads`](../../skills/plan-my-ads/SKILL.md) +
connected [`run-my-ads`](../../skills/run-my-ads/SKILL.md), over the folderless
`claude_mcp` driver [`drivers/meta-ads/`](../../drivers/meta-ads/). Read it
alongside this recipe; every step here is realized there.

Full design rationale: [`2026-07-03-tier-1-addon-kit-design.md`](2026-07-03-tier-1-addon-kit-design.md)
(§3 recipe, §4 taxonomy, §5–§6 the gate). This doc is the human-facing build
checklist; that doc is the why.

---

## The core shape

A connected add-on is a **plan/run seam** plus **one driver** plus **three
catalog artifacts**, and nothing else:

1. A keyless **floor "thinking" skill** that writes a portable plan artifact,
   works with no account, and runs under `BOS_OFFLINE`.
2. A connected **"doing" skill** that reads that plan and calls the driver's
   tools against the owner's live account.
3. A **driver** that declares the add-on's shape and (if it can spend or do
   anything irreversible) its safety hard lines.
4. **`connect.md`**, the **`connectors.md` card**, and the **`starter-projects.md`
   row** — the three surfaces that make the add-on connectable and discoverable.

The split between the two skills is **purely a manifest split**: the floor skill
carries no driver, the connected skill carries the driver. Same capability,
two altitudes. `plan-my-ads` is the thinking, `run-my-ads` is the doing, and
`plan-my-ads` hands off to `run-my-ads` by outcome, never as a routed offer.

---

## The recipe (a mechanical checklist)

### 1. Build the plan/run seam

- **Floor skill** (the thinking): keyless, finishable in one sitting, writes one
  portable plan artifact to the owner's working directory. It names outcomes in
  plain language and never hardcodes a platform's internal setting names or enum
  spellings — that belongs to the run skill, read live at build time. See
  `plan-my-ads`'s nine gates and its "written ad-plan artifact" section for the
  worked shape.
- **Connected skill** (the doing): reads the plan artifact as its input and
  builds to it against the live account. If the plan is absent, it offers to run
  the floor skill first so the doing has a spine.
- The plan artifact is the contract between them. Keep it plain-language and
  portable (the ad plan applies to any ad platform), so the floor skill stays
  genuinely useful on its own and the connected skill has a clean input.

### 2. Write the two frontmatter contracts

The gate enforces the **connected** half mechanically (see "What the gate
checks"); the floor half is a checklist item here, already covered by the
existing lint + onboarding-binding checks.

**Floor skill frontmatter (the keyless contract):**

```yaml
requires_driver: none
requires_credential: none
data_path: reasoning_only    # or 'local' if it reads/writes local files
# no uses_tools key at all
```

- No `uses_tools` key, and **no `mcp__*` token anywhere in the body.** A floor
  skill that names a connected tool would couple the floor to a paid surface —
  the thing the extraction recipe forbids.

**Connected skill frontmatter (the connected contract):**

```yaml
requires_driver: <driver-id>       # e.g. meta-ads — must resolve (see gate)
requires_credential: mcp           # or 'key' for a keyed driver
data_path: mcp_tools               # or 'local'
uses_tools:                        # EXHAUSTIVE — every tool the body calls
  - mcp__<driver-id>__<read_tool>
  - mcp__<driver-id>__<create_tool>
  - mcp__<driver-id>__<update_tool>
  # ... and so on
```

- `uses_tools` is exhaustive: **every** driver tool the body calls is listed,
  and every entry is driver-owned (contains the driver id). See `run-my-ads`'s
  fifteen-entry `uses_tools` list.
- **Any irreversible / spend tool is DELIBERATELY OMITTED from `uses_tools`.**
  The activate tool is not in `run-my-ads`'s list on purpose, so if a body ever
  named it, lint would fail the build. Omission is the guard for the loud switch.
  (The quiet switch — a status field set live via an update tool that legitimately
  stays in `uses_tools` — is guarded by the safety value-scan instead; see §7.)

### 3. Write the folderless documentation-only driver (`claude_mcp`)

For a `claude_mcp` driver there is **no Python transport** — the Claude client
hosts the MCP, the owner connects it over OAuth, and skills call the
`mcp__<id>__*` tools directly. The driver folder is documentation only. See
[`drivers/meta-ads/README.md`](../../drivers/meta-ads/README.md) for the full
"what a `claude_mcp` driver is" write-up and the four-file clone steps.

- **`__init__.py`** carries a top-level `DRIVER` dict and a docstring that states
  plainly **nothing reads this module** (no driver-metadata loader exists). The
  `DRIVER` dict fields: `id`, `kind`, `display_name`, `server_url` (or a CLI for
  a `keyed_cli` driver), `tool_prefix`, `connect_doc`, `credential`,
  `read_only_scope_first`, and — only if the tool can spend or do anything
  irreversible — `never_call` / `never_set` (see §7).
- The three **load-bearing** artifacts are only: the `requires_driver` string on
  the connected skill, `connect.md`, and the `connectors.md` card. Everything in
  the driver folder is a reference shape, not a runtime dependency.
- Do NOT add `auth.py` or a `DriverConfig`, and do NOT add the driver to
  `_KEYLESS_DRIVERS` — it is connected-tier, not keyless.

### 4. Write `connect.md` (the single home for connect steps)

The connect steps have exactly **one home**: `drivers/<id>/connect.md`. Every
other surface (the connectors card, the spec) carries a short pointer to it,
never a restated procedure. Its fixed shape, per [`drivers/meta-ads/connect.md`](../../drivers/meta-ads/connect.md):

- **What this unlocks** — the win, in the owner's terms.
- **The honest boundary** — the one sign-in only the owner can do; the system
  does everything else. No password or code is ever asked for.
- **Step 1: add the connection** (permission first).
- **Step 2: the owner signs in** — grant the read-only scope tier first.
- **Step 3: restart** so the connection loads.
- **Step 4: verify** with one lightweight read.
- **Step 5: make it yours, then put it to use** — hands to the "make it yours"
  intake (§6), then to the doing.

### 5. Write the `connectors.md` card

Add one card to [`knowledge/connectors.md`](../../knowledge/connectors.md)
following the fixed schema at the top of that file. The heading is
`## <display_name> (<plain parenthetical>)` — the gate matches the card to the
driver by **prefix** on `display_name`, so the parenthetical suffix is fine.
The card's fields:

- **What it is** — one plain line.
- **Fits businesses that** — the business-need tags (found by "what do I want to
  do", not by product name).
- **Unlocks** — the connected skill it switches on.
- **Connect it** — a pointer to `drivers/<id>/connect.md` (not a restated
  procedure), plus the labelled `connect-a-tool` exception if one applies (§8).
  A locally-registered MCP server connects at **local (this-folder) scope** by
  default (see the Connection Scoping Doctrine below); the card names that scope,
  the doctrine owns the rule.
- **Keep it lean** — connect it when ready, not "just in case"; the tools stay
  deferred (names only) until used.
- **Heads-up** — any cost, credit, or spend note said out loud first.
- **Verify** — the one read that proves it is live.

See the `## Meta Ads (Facebook & Instagram ads)` card for the worked shape.

### 6. Wire the guided intake (Source A/B/C/D), profile as DATA

The connected skill's "make it yours" init fills a per-owner profile from four
sources, asking the owner as little as possible. See `run-my-ads` Step 1 for the
worked version.

- **Source A — read `brand/brand.json` silently:** business name, colors, logo,
  voice, tagline. Read, never copy brand fields into the add-on profile.
- **Source B — read `./CLAUDE.md` silently:** business shape, offer, region (only
  if a `Region:` line is explicitly set, never inferred), diagnosed constraint,
  goal.
- **Source C — ask only the small add-on-specific bucket:** the handful of
  questions unique to this capability (for ads: monthly budget, objective, geo,
  spend ceiling). This is the ONLY interview.
- **Source D — one live read of the account, auto-fill and confirm, don't ask:**
  read the account facts once (ids, currency, health) and confirm them in words
  rather than making the owner type what the account already knows.
- **Write** the profile to `~/.claude/bos-cache/<addon>-profile.json` (outside
  the repo, so updates never touch it).
- **Fold the driver's `OPERATING-CONTEXT.md` into `./CLAUDE.md`** with the
  skill's **own** read-and-merge, no-clobber steps: read the source, read the
  owner's `./CLAUDE.md`, show the section or the diff, append or merge, never
  clobber hand-tuned content. **Do NOT call `learn-my-business`** — it is
  CRM-gated and never runs for an add-on-only owner. See `run-my-ads` Step 1e.

**Personalization is DATA, never a forked skill file.** Per-owner detail lives
in the profile JSON. Never template or copy the skill file per owner — a fork
gets clobbered on update (or blocks updates) and it causes drift.

### 7. Carry layered write-safety — only for a money / irreversible surface

If the driver can spend money or do anything irreversible, carry the full safety
stack. If it cannot, skip this section entirely (a read-only or purely additive
add-on does not need it). See `run-my-ads`'s "Hard rules" and Step 6 for the
worked stack.

- **Confirm-before-every-write is the real gate.** Show the owner exactly what
  will be created or changed, plus the spend implication in the account's own
  currency, and wait for an explicit yes. One confirmation per write, no batching.
- **Journal every confirmed write, then verify the line landed.** Journaling is
  best-effort, not a spend gate — so after each write, re-read the journal and
  confirm the record is there; if it isn't, say so plainly.
- **Never-do declarations live in the `DRIVER` dict**, as `never_call` (the loud
  switch — a tool BOS must never call) and `never_set` (the quiet switch — an
  update tool that must never carry a listed field set to a live value). List
  **every** interchangeable field: Meta forbids all three of `status`,
  `configured_status`, `effective_status`, because any one of them un-pauses a
  shell. The truncated one-field version is unsafe; copy the exhaustive one.
- The gate reads these declarations and scans every skill body for a violation
  (see below). The confirmation gate is the real safety; the gate is the
  belt-and-suspenders that makes the never-do lines un-bypassable.

### 8. The labelled `connect-a-tool` override

The default connect mechanism is the in-app `/mcp` (Connectors) flow. When an
add-on's connect mechanism differs — Meta Ads is added via the `claude mcp` CLI,
which the system runs for the owner — that difference must be a **labelled
exception** in both [`skills/connect-a-tool/SKILL.md`](../../skills/connect-a-tool/SKILL.md)
and the driver's `connect.md`, so the two do not silently diverge. Label it as
"this overrides the usual in-app `/mcp` flow because …" and point at `connect.md`
as the single home for the steps. The owner still performs the one sign-in only
they can. Whichever add mechanism is used, a locally-registered MCP server
registers at **local (this-folder) scope** in the owner's BOS workspace by
default — that choice is owned by the Connection Scoping Doctrine above, not by
the exception.

### 9. The `needs_connection` onboarding tag (DONE)

A connected add-on's row in [`knowledge/starter-projects.md`](../../knowledge/starter-projects.md)
uses the vendor-neutral **`needs_connection`** tag. This tag already exists in
`_CONNECTED_TIER_TAGS` in `tools/check-onboarding-binding.py` (landed with the
meta-ads work), so treat it as done, not pending. **Never `keyless`** (the add-on
needs an account) and **never a CRM-coupling tag** (it is not the CRM).

---

## The Connection Scoping Doctrine (the owning statement)

This is the **single home** for two rules every driver author follows so an
owner gets a fast, lean system without ever having to understand why. Every
other surface that touches connections (the `connectors.md` cards, the
`connect-a-tool` skill, a driver's `connect.md`) points here rather than
restating these rules.

**Why it matters, in one line:** a registered local MCP server loads its tool
surface into every session that can see it, used or not, and it only attaches at
session start (there is no hot-loading). So the only lever an author has is
*scope* — which sessions ever see the server. Get the scope right at authoring
time and the owner never pays for a tool they aren't using.

### Primitive 1 — CLI-first drivers (the default)

When a capability's outside service is **stateless** (a key goes in, JSON comes
back), ship it as a **CLI the skill calls**, not as a registered MCP server. A
CLI has **zero standing cost**: nothing loads into a session until the skill
shells out to it. This is the native BOS pattern — BOS already installs
`~/.claude/bos-run.py` as the signpost skills use to find their tools, so a
CLI-first driver slots straight into it. The `keyed_cli` kind in the taxonomy
below is exactly this shape (Vercel is the worked example).

Reserve a registered MCP server for the cases where a CLI genuinely can't do the
job: the tool needs an **OAuth sign-in flow**, a **persistent connection**, or
**real-time subscriptions**. Those are the connected kinds (`claude_mcp`); Meta
Ads is the worked example. If a stateless API is being wrapped as an MCP server
"because it's easier", that is the wrong call — make it a CLI.

### Primitive 2 — Scoped connections (never user scope for a driver)

When a driver **must** be a locally-registered MCP server, it registers at
**local (this-folder) scope in the owner's BOS workspace folder** — that is
`claude mcp add --scope local` (the CLI default), run from the workspace folder
— never user scope. Local scope is directory-scoped and **private to the
owner**: only sessions opened in that folder ever attach the server, so their
other projects stay fast, and the registration lives in the owner's own
`~/.claude.json`, never in a git-tracked file — so it cannot be accidentally
committed, pushed, or tangled up in an `update-bos` pull. This is the default
for every connected driver.

- **Why not `--scope project` (labelled, so the distinction reads as policy):**
  project scope writes a shared `.mcp.json` at the repo root — a git-tracked
  file in a BOS workspace, which is a clone of the public repo. That form is
  reserved for teams that *deliberately* want to share a connection via version
  control; it is never the BOS default, because an owner's connection must not
  land in `git status` or a push.
- **The one labelled exception:** the keyless **firecrawl** server, which
  `tools/setup.py` registers at **user scope on purpose** — it is a universal,
  keyless web-research utility that every session legitimately benefits from, and
  this is existing, deliberate behavior. It is labelled here so the divergence
  reads as policy, not drift. No other driver gets user scope.
- **The room escape hatch (optional, for very heavy servers):** if a single
  server is heavy enough that even the main workspace shouldn't pay for it, give
  it its **own subfolder ("room") and register it at local scope from inside
  that room**, so only sessions opened *in that room* pay for it. The skill's
  connect doorway then tells the owner, in plain language, "open Claude Code in
  your `<X>` folder" — they never hear the word "scope".
- **Out of BOS's hands:** claude.ai **connectors** (the sign-in type, like
  TrustPager, Gmail, or Calendar) are **account-level** and cannot be scoped by a
  local config file. This doctrine governs **local MCP registrations only**
  (`claude mcp add` / `.mcp.json`). For a claude.ai connector, the lever the owner
  has is the same "keep it lean, connect only what you'll use now" guidance the
  connector cards already carry.

### The deferral note — keep Claude Code current

Current Claude Code defers a server's tool schemas behind tool-search: only the
tool **names** load until one is actually fetched, which softens the standing
cost of a registered server considerably. Older versions load every full schema
up front (tens of thousands of tokens for a large server). So the standing
advice, everywhere it surfaces to an owner, is simply **keep Claude Code
current** — newer versions load connected tools far more token-efficiently. This
is a softener on Primitive 2, never a replacement for it: scope is still the real
lever, because deferral shrinks the per-session cost but does not remove it.

---

## The driver-kind taxonomy (the canonical six)

Every driver that opts into the kit declares a `kind` in its `DRIVER` dict. The
gate validates against **exactly this set** (the "kind is in the taxonomy"
check); anything else, or a missing kind, fails conformance.

| kind | What it is | Example | Shape |
|---|---|---|---|
| `claude_mcp` | Owner-hosted OAuth MCP the Claude client hosts | `meta-ads` | Folderless docs-only; `connect.md`; no Python transport |
| `keyed_cli` | A keyed local CLI invoked via Bash | Vercel (planned) | Docs-only `DRIVER` dict + `secret_pattern`; `connect.md`; no `DriverConfig` |
| `keyed_rest` | Keyed REST API with a Python transport | `trustpager` | `DriverConfig` + auth/catalog (the CRM core; grandfathered) |
| `keyless_mcp` | Keyless hosted MCP, no account | `firecrawl` | Grandfathered |
| `local` | Runs locally, no account | `render`, `markitdown`, `doclib` | Grandfathered |
| `data_pack` | Region/data bundle, no connection | `regional/au` | Grandfathered |

The two **connected** kinds — `claude_mcp` and `keyed_cli` — get the full
structural checks (connect.md + card). The other four do not connect, so those
checks are not required of them.

**Grandfathering:** the gate only enforces on drivers that ship a new-style
`DRIVER` dict. Today that is `meta-ads` alone; Vercel joins when it ships its
dict. The pre-existing drivers (`trustpager`, `firecrawl`, `render`,
`markitdown`, `regional`, `_noop`) keep their current shapes — forcing them into
the connected-add-on template would be a category error, since they do not
connect. The taxonomy documents their kinds for completeness only.

---

## What the gate checks (`tools/check-connectors.py`)

The single CI gate reads each opted-in driver's `DRIVER` dict (static `ast`
parse, never an import) and enforces both safety and structure. A half-built or
unsafe connected add-on fails CI. Build to this and it passes near-mechanically:

**Safety** (only when the driver declares `never_call` / `never_set`):

- No `never_call` tool name appears in ANY skill body (the loud switch).
- No `never_set` field is set to a live value via its update tool in any body
  (the quiet switch), scanned across line boundaries. Both the fully-qualified
  and the bare tool name are searched, for breadth.

**Conformance** (for every driver that ships a `DRIVER` dict):

- `kind` is present and in the canonical six.
- **`requires_driver` on every skill resolves** — threefold: it is `none`, OR a
  known keyless driver id (folderless by design), OR a real `drivers/<id>/`
  folder exists. This closes the typo-passes-silently hole.
- **Connected kinds** (`claude_mcp`, `keyed_cli`): a `connect.md` exists in the
  driver folder, AND a `connectors.md` heading **begins with** the `display_name`
  (prefix match — the parenthetical suffix is fine).
- **The connected frontmatter contract** holds for each skill whose
  `requires_driver` is an opted-in driver: `requires_credential` in `{mcp, key}`,
  `data_path` in `{mcp_tools, local}`, and every `uses_tools` entry is
  driver-owned.

The gate enforces only the connected half of the frontmatter contract, because a
floor skill (`requires_driver: none`) is not mechanically linked to the driver;
the floor keyless-clean contract stays a recipe checklist item (§2), already
covered by lint + onboarding-binding.

---

## Guardrails (what NOT to do)

- Don't put the connected tool on the floor. The floor skill carries no driver
  and no `mcp__*` token — if it needs the live account, it belongs in the
  connected skill (this is the extraction recipe's `reasoning_only`-stays-keyless
  rule).
- Don't fork or template the skill file per owner. Per-owner detail is DATA in
  the profile JSON (§6).
- Don't restate the connect steps anywhere but `connect.md`. One home; every
  other surface points at it.
- Don't add a Python transport (`auth.py`, `DriverConfig`) to a `claude_mcp`
  driver, and don't add it to `_KEYLESS_DRIVERS`.
- Don't list an irreversible / spend tool in the connected skill's `uses_tools`.
  Omit it so lint fails if the body ever names it (§2).
- Don't call `learn-my-business` from the add-on intake — fold the operating
  context with the skill's own no-clobber merge (§6).
- Don't ship the truncated one-field `never_set` example. List every
  interchangeable status field, so the pattern an author copies is the safe one.

---

## Ship checklist + validation

- Floor skill: keyless frontmatter, no `mcp__*` in the body, writes a portable
  plan artifact, registered in `kernel/registry.json`, a `starter-projects.md`
  row.
- Connected skill: connected frontmatter, exhaustive `uses_tools` with the
  irreversible tool omitted, reads the plan, runs the Source A/B/C/D intake,
  carries the write-safety stack if the surface spends, `needs_connection` row.
- Driver: `DRIVER` dict with a canonical `kind`, a "documentation only"
  docstring, `never_call` / `never_set` if it can spend, plus `connect.md`,
  `OPERATING-CONTEXT.md`, and `README.md`.
- Catalog: a `connectors.md` card (heading begins with `display_name`), a
  labelled `connect-a-tool` exception if the add-mechanism differs.
- Regenerate `docs/CAPABILITIES.md` (`python tools/export-capabilities.py`) and
  commit it.
- **Run `python tools/check-connectors.py`** — it must print OK. Then dogfood the
  add-on on Sonnet (the client run-tier) with a realistic owner: the floor skill
  does its slice well and stays keyless, the connected skill builds safely (paused
  / confirmed / journaled if it spends), and every line of customer-facing output
  is positive-only with no em dashes.

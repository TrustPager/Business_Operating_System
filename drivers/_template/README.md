# The connected-driver TEMPLATE

<!-- TEMPLATE — documentation only. This folder is the copyable skeleton for the
     next connected add-on. The underscore prefix (`_template`) tells the connector
     gate to SKIP it, so its <placeholder> values never fail CI. When you clone it,
     drop the underscore, fill every placeholder, and replace this README with one
     that explains YOUR driver (modeled on drivers/meta-ads/README.md). -->

This folder is the reusable **shape** for a connected `claude_mcp` (or `keyed_cli`)
driver. Copy it to `drivers/<your-id>/`, fill the `<placeholder>` markers, and you
have the safe, conformant four-file shape by default. The worked, shipping example
this mirrors is [`drivers/meta-ads/`](../meta-ads/); read it alongside this
template. The full build recipe is
[`docs/architecture/tier-1-addon-kit.md`](../../docs/architecture/tier-1-addon-kit.md).

## What a connected driver is

A connected driver declares a **business capability that needs a live outside
account** (an ad platform, a deploy host, and the like) as an add-on that is safe
by construction. The default and worked kind is `claude_mcp`: a **connected OAuth
MCP that the owner hosts** — the Claude Code client runs the MCP, the owner
authorizes it over their own sign-in, and BOS skills call the `mcp__<id>__*` tools
directly. The owner's credential never passes through BOS; there is no key to
paste, resolve, or redact.

Its **defining property is that it has no Python transport.** There is no
`DriverConfig`, no `auth.py`, no `catalog.py`, no key resolver — the folder is
documentation only. `drivers/__init__.py` already says "The kernel never imports a
driver"; a `claude_mcp` driver has nothing for the kernel to import in the first
place.

## The four files (what to fill)

- **`__init__.py`** — the declarative `DRIVER` dict (id, kind, `server_url`/`cli`,
  `tool_prefix`, `connect_doc`, `credential`, `read_only_scope_first`, and the
  `never_call` / `never_set` spend-safety lines if the tool can spend or do
  anything irreversible). Its docstring states plainly that nothing reads it; there
  is no driver-metadata loader.
- **`connect.md`** — the single home for the connect steps (the fixed seven-part
  shape: what this unlocks, the honest boundary, add / sign-in / restart / verify /
  make-it-yours). Every other surface points here; none restates it.
- **`OPERATING-CONTEXT.md`** — the plain-language source text the connected skill's
  "make it yours" setup folds into the owner's `./CLAUDE.md` on connect (modeled on
  `drivers/trustpager/OPERATING-CONTEXT.md`).
- **`README.md`** — this file; replace it with the shape write-up for your driver.

## The three load-bearing artifacts (outside this folder)

For a `claude_mcp` driver, **no BOS mechanism reads a driver folder.** The
load-bearing artifacts live elsewhere and are exactly the ones the worked example
uses:

1. The **`requires_driver: <id>` string** on the connected skill's manifest — what
   drives registry classification and the dark-gate.
2. The **connect walkthrough** at `connect.md` — read by the connected skill's
   "make it yours" setup and pointed at from the connectors card.
3. The **`## <Display Name>` card** in `knowledge/connectors.md` — the catalog
   surface that `connect-a-tool` and `whats-possible` read.

## What NOT to add

Do **not** add `auth.py` or a `DriverConfig` here, and do **not** add the driver to
`_KEYLESS_DRIVERS` in `check-onboarding-binding.py` — it is connected tier, not
keyless. A builder should not go hunting for a loader that does not exist; there
isn't one. Do not restate the connect steps anywhere but `connect.md`, and do not
ship the truncated one-field `never_set` example — list every interchangeable
status field so the pattern you copy is the safe one.

## Cloning this shape

1. Copy `drivers/_template/` to `drivers/<id>/` (drop the underscore).
2. Fill `__init__.py`: set `id`, `display_name`, `server_url` (or `cli`),
   `tool_prefix`, and the `never_call` / `never_set` spend-safety lines if the tool
   has an irreversible or money surface. Delete the fields your kind does not use.
3. Write `OPERATING-CONTEXT.md` for how the assistant behaves once that tool is
   connected, and `connect.md` for the one-home connect steps.
4. On the connected skill, set `requires_driver: <id>` and list its `uses_tools`
   (the irreversible tool DELIBERATELY omitted). Add a card to
   `knowledge/connectors.md` whose heading begins with the `display_name`.
5. Regenerate the registry. No kernel change, no generator edit — the folder stays
   documentation, and the `requires_driver` string does the real work.
6. Run `python tools/check-connectors.py` — it must print OK.

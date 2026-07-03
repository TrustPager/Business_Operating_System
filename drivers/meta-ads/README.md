# The `claude_mcp` driver shape

This folder is the first `claude_mcp`-type driver (`meta-ads`), and it exists to
**document the reusable shape** for the next connected tool of the same kind
(Google Ads, and the like). It is a reference, not a runtime dependency.

## What a `claude_mcp` driver is

A `claude_mcp` driver is a **connected OAuth MCP that the owner hosts** — the
Claude Code client runs the MCP, the owner authorizes it over their own sign-in,
and BOS skills call the `mcp__<id>__*` tools directly. The owner's credential
never passes through BOS; there is no key to paste, resolve, or redact.

Its **defining property is that it has no Python transport.** There is no
`DriverConfig`, no `auth.py`, no `catalog.py`, no key resolver. `drivers/__init__.py`
already says "The kernel never imports a driver" — a `claude_mcp` driver has
nothing for the kernel to import in the first place.

## How it differs from the other driver shapes

The existing drivers split into three physical realities. A `claude_mcp` driver
is a fourth, and it follows the **folderless** precedent, not the trustpager one.

| Shape | Example | Transport | Credential | Folder on disk |
|---|---|---|---|---|
| **keyed-REST** | `trustpager` | Python `DriverConfig` over `kernel.runtime.transport`, with `auth.py` + `catalog.py` | an API key BOS resolves and redacts | yes — real, load-bearing Python |
| **keyless hosted MCP** | `firecrawl` | none in BOS; `setup.py` registers the hosted MCP into `~/.claude.json` | none | no folder — just a `requires_driver` string |
| **data pack** | `regional/au` | none; a loader (`tools/regional.py`) reads versioned JSON | none | yes — data + a README, no transport |
| **`claude_mcp`** (this) | `meta-ads` | **none**; the Claude Code client hosts the MCP, the owner connects it over OAuth | OAuth, held by the owner, never by BOS | this folder — **documentation only** |

The nearest neighbour is `firecrawl`: both are MCPs with no Python transport. The
difference is **who connects and when**. Firecrawl is keyless and hosted, so
`setup.py` registers it once for everyone at install time. `meta-ads` is the
owner's own account over OAuth, so it is connected **on demand** via `connect.md`
when the owner is ready to launch ads — never auto-registered, which keeps the
floor at zero connected-driver tools and the per-turn token cost low (the tools
stay deferred, names only, until one is actually called).

## The folderless / no-transport property

For a `claude_mcp` driver, **no BOS mechanism reads a driver folder.**
`manifest.py`, `registry-generator.py`, `lint-skill.py`, and the kernel never
open `drivers/meta-ads/`. The load-bearing artifacts live elsewhere and are
exactly the ones firecrawl uses:

1. The **`requires_driver: meta-ads` string** on `run-my-ads`'s manifest — this is
   what drives registry classification and the dark-gate.
2. The **connect walkthrough** at `connect.md` — read by the `run-my-ads` "make it
   yours" setup and pointed at from the connectors card.
3. The **`## Meta Ads` card** in `knowledge/connectors.md` — the catalog surface
   that `connect-a-tool` and `whats-possible` read.

The connect steps themselves have exactly **one home**: `connect.md`. Every other
file (the connectors card, the spec) carries a short pointer to it, never a
restated procedure. If the endpoint URL or the callback-port fallback ever
changes, `connect.md` is the single file to edit.

## Why this folder exists at all, then

Purely as the deliberate reusable-shape reference for the next connected driver.
Everything in it is **non-enforced documentation**:

- **`__init__.py`** — declarative `DRIVER` metadata (id, kind, `server_url`,
  `tool_prefix`, `connect_doc`, credential, and the spend-safety hard lines). Its
  own docstring says plainly that nothing reads it today; there is no
  driver-metadata loader. It is the template a future connected-MCP driver copies,
  and the machine-readable form of the spend-safety facts a future loader could
  consume.
- **`OPERATING-CONTEXT.md`** — the plain-language source text that `run-my-ads`'s
  setup folds into the owner's `./CLAUDE.md` on connect (modeled on
  `drivers/trustpager/OPERATING-CONTEXT.md`).
- **`connect.md`** — the single-home connect walkthrough.
- **`README.md`** — this file.

Do **not** add `auth.py` or a `DriverConfig` here, and do **not** add `meta-ads`
to `_KEYLESS_DRIVERS` in `check-onboarding-binding.py` — it is connected-tier, not
keyless. A builder should not go hunting for a loader that does not exist; there
isn't one.

## Cloning this shape for the next connected driver

1. Create `drivers/<id>/` with the same four files.
2. Copy `__init__.py`, set `id`, `display_name`, `server_url`, `tool_prefix`, and
   the `never_call` / `never_set` spend-safety lines if the tool has an
   irreversible or money surface.
3. Write `OPERATING-CONTEXT.md` for how the assistant behaves once that tool is
   connected, and `connect.md` for the one-home connect steps.
4. On the connected skill, set `requires_driver: <id>` and list its `uses_tools`.
   Add a card to `knowledge/connectors.md` pointing at the new `connect.md`.
5. Regenerate the registry. No kernel change, no generator edit — the folder stays
   documentation, and the `requires_driver` string does the real work.

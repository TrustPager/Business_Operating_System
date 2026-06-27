# Skill manifest schema

Every skill's `SKILL.md` frontmatter carries a small, flat **manifest** that
describes what the skill needs and what it does. This is the data-driven
capability contract: a generator (P1 Task 2) reads each skill's manifest into
`kernel/registry.json`, and the runtime decides — from that data, not from
hardcoded logic — which skills are available given the configured driver and
credentials. Lint (P1 Task 3) enforces the contract so manifests can't drift
out of sync with the schema. The schema, parser, and validator all live in
`tools/manifest.py` (stdlib only — the frontmatter is flat by design, so no
PyYAML).

## The contract

Frontmatter keys are flat scalar values and simple `  - ` string lists only —
no nesting. The enum values below are authoritative in `tools/manifest.py`;
this table is the human-readable mirror, so if the two ever disagree the code
wins.

| Key | Required | Allowed values |
|---|---|---|
| `function_slot` | yes | `crm` `accounting` `ads` `social` `creative` `comms` `documents` `money` `people` `strategy` `research` `floor` |
| `requires_driver` | yes | a driver id (e.g. `trustpager`) or `none` |
| `requires_credential` | yes | `none` \| `mcp` \| `key` |
| `data_path` | yes | `reasoning_only` \| `mcp_tools` \| `fetch_rest` \| `local` |
| `uses_tools` | optional | list of `mcp__*` tool names |
| `unlocks` | optional | list of strings |
| `reads_for_profile` | optional | list of strings |
| `status` | optional (default `active`) | `active` \| `deprecated` \| `removed` |

These enums encode founder decision **D8**: TrustPager apps run on the MCP data
path (`data_path: mcp_tools`, `requires_credential: mcp`); floor apps are
reasoning-only (`data_path: reasoning_only`, `requires_credential: none`,
`requires_driver: none`).

### `data_path` values

- `reasoning_only` — the skill works purely from the model's reasoning over the
  operator's input. No driver, no I/O.
- `mcp_tools` — the skill reads/writes through a connected MCP (e.g. TrustPager
  over OAuth). Pairs with `requires_credential: mcp`.
- `fetch_rest` — the skill fans out to a keyed third-party REST API (the kernel's
  keyed-REST transport). Pairs with `requires_credential: key`.
- `local` — the skill reads **local files the operator provides** — e.g.
  MarkItDown converting a dropped-in PDF/DOCX, or a render driver writing output
  to disk. Nothing leaves the machine and no account is involved, so it pairs
  with a keyless driver and `requires_credential: none`.

### The keyless-driver model

`requires_driver` names the driver a skill runs on, but naming a driver does
**not** imply a credential. Some drivers are **keyless** — they ship in the
floor and need no account, no key, and no OAuth connection:

| Driver id | Keyless? | Typical `data_path` | `requires_credential` |
|---|---|---|---|
| `markitdown` | yes (keyless) | `local` | `none` |
| `firecrawl` | yes (keyless) | `fetch_rest` | `none` |
| `render` | yes (keyless) | `local` | `none` |
| `trustpager` | no — connect via MCP | `mcp_tools` | `mcp` |
| third-party REST APIs | no — paste a key | `fetch_rest` | `key` |

Keyless drivers (`markitdown`, `firecrawl`, `render`) document-convert, scrape,
or render entirely from what the operator already has, so they declare
`requires_credential: none`. Only drivers that reach an authed account —
`trustpager` and other keyed REST APIs — declare `mcp` or `key`. This keeps the
install "anyone can run it" honest: the keyless floor works day one.

## Manifest keys vs passthrough keys

A `SKILL.md` frontmatter block mixes two concerns, and the validator treats them
differently:

- **Manifest keys** — the capability contract above. Required:
  `function_slot`, `requires_driver`, `requires_credential`, `data_path`.
  Optional: `uses_tools`, `unlocks`, `reads_for_profile`, `status`.
- **Passthrough keys** — pre-existing non-manifest frontmatter that skills
  legitimately carry and that other tooling reads (Claude Code skill loading,
  `tools/lint-skill.py`): `name`, `description`, `triggers`. These are
  **allowed** and are **not** treated as "unknown" — but they are not validated
  by `validate_manifest()` either; that's `lint-skill.py`'s job.

Any key that is neither a manifest key nor a passthrough key is **unknown** and
is reported as an error, so typos and stray keys get caught.

`validate_manifest(meta)` returns a list of human-readable error strings (empty
== valid). It checks: all required keys present; each enum field's value is in
its allowed set; `uses_tools` / `unlocks` / `reads_for_profile` are lists if
present; `status` is a valid enum if present; and no unknown keys.

## Exemplars

### Floor skill — `skills/write-prompt/SKILL.md`

A reasoning-only skill: no driver, no credential, no tools. It works purely from
the model's reasoning over the operator's input.

```yaml
---
name: Write Prompt
description: Turn a rough ask into a complete, explicit prompt ...
triggers:
  - write a prompt
  - sharpen this prompt
  - turn this into a proper prompt
  - help me brief this
  - make this prompt explicit
  - improve this prompt
function_slot: floor
requires_driver: none
requires_credential: none
data_path: reasoning_only
---
```

### CRM skill — `skills/sweep-my-day/SKILL.md`

A TrustPager-backed skill: it reads the operator's workspace over the MCP data
path, so it requires the `trustpager` driver and an `mcp` credential. `uses_tools`
lists the `mcp__trustpager__*` tools the SKILL.md body documents as its MCP
fallback path (the body otherwise prefers the consolidated `fetch.py` helper).

```yaml
---
name: Sweep My Day
description: Morning briefing ...
triggers:
  - sweep my day
  - what needs my attention
  - ...
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__list_email_threads
  - mcp__trustpager__list_sms_conversations
  - mcp__trustpager__list_phone_call_logs
  - mcp__trustpager__list_form_submissions
  - mcp__trustpager__list_whatsapp_conversations
  - mcp__trustpager__list_tasks
  - mcp__trustpager__list_work_orders
  - mcp__trustpager__list_scheduled_communications
  - mcp__trustpager__list_opportunities
  - mcp__trustpager__get_opportunity_activities
  - mcp__trustpager__list_transcripts
  - mcp__trustpager__list_bookings
  - mcp__trustpager__get_pipeline_summary
---
```

## Checking a manifest

```bash
python tools/manifest.py skills/sweep-my-day/SKILL.md
```

Prints `OK` if valid, or the list of problems with a non-zero exit code.

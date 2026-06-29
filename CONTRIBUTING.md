# Contributing to Business Operating System

Thanks for taking the time to improve BOS. This document covers how a skill is structured, how to write one, how to invoke the tools, and what every pull request must pass before it can merge.

---

## How a skill is structured

Each skill lives in its own folder under `skills/`:

```
skills/<skill-name>/
  SKILL.md           # the skill definition (frontmatter + body)
  fetch.py           # optional: data-fetch helper for connected skills
  test-fixture.json  # required if fetch.py exists
```

`SKILL.md` has two parts:

1. **Frontmatter** (between `---` fences at the top of the file): the flat manifest that describes what the skill needs and what it does. This is the capability contract the runtime reads.
2. **Body** (everything after the frontmatter): the skill instructions, in plain Markdown, written for Claude to follow when the skill activates.

### The manifest keys

| Key | Required | Purpose |
|---|---|---|
| `name` | yes | Human-readable display name |
| `description` | yes | One-line description for the registry |
| `triggers` | yes | List of natural-language phrases that activate the skill |
| `function_slot` | yes | The category this skill belongs to (see below) |
| `requires_driver` | yes | The driver this skill uses (e.g. `trustpager`) or `none` |
| `requires_credential` | yes | `none`, `mcp`, or `key` |
| `data_path` | yes | How the skill gets its data (see below) |
| `uses_tools` | optional | List of `mcp__*` tool names the skill calls |
| `unlocks` | optional | Other skills this skill gates or enables |
| `reads_for_profile` | optional | Data fields this skill reads to build the operator profile |
| `status` | optional | `active` (default), `deprecated`, or `removed` |
| `requires_region` | optional | `AU` if the skill only applies to a specific region |

Full schema with allowed enum values: [`docs/architecture/manifest-schema.md`](docs/architecture/manifest-schema.md). The code in `tools/manifest.py` is authoritative; the schema doc is the human-readable mirror.

### Keyless vs connected skills

Skills are either **keyless** (floor skills) or **connected** (TrustPager or keyed-REST skills). The manifest declares which:

**Keyless floor skill** (works for anyone, day one, no accounts):
```yaml
function_slot: floor       # or money, strategy, research, creative, etc.
requires_driver: none
requires_credential: none
data_path: reasoning_only
```

**TrustPager-connected skill** (requires a TrustPager workspace and MCP connection):
```yaml
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__list_opportunities
```

**Keyed REST skill** (requires a third-party API key):
```yaml
requires_driver: <driver-name>
requires_credential: key
data_path: fetch_rest
```

Some drivers are keyless by design (`markitdown`, `firecrawl`, `render`). See the manifest schema doc for the full driver table.

### The gold-standard skill to study

`skills/sweep-my-day/SKILL.md` is the reference implementation for a connected CRM skill. `skills/price-my-work/SKILL.md` is the reference for a keyless floor skill. Read both before writing your own.

---

## How to invoke tools

Skills that call Python helper tools use the **signpost launcher**, which resolves the install location automatically:

```bash
python ~/.claude/bos-run.py tool <tool-name>
```

For example, a skill's `fetch.py` is invoked internally as:

```bash
python ~/.claude/bos-run.py <skill-name>
```

The signpost launcher is created by `python tools/setup.py`. If it is missing, run setup again.

Do not hardcode absolute paths to `tools/` or `skills/` in skill bodies. Use the signpost so the skill works whether BOS was installed as a plugin or as a clone.

---

## Gates every PR must pass

Run all of these locally before opening a PR. CI runs the same sequence and will block the merge if any step fails.

### 1. Offline unit tests (no key, no network)

```bash
BOS_OFFLINE=1 python -m unittest discover -s tests
```

310 tests, all must pass. `BOS_OFFLINE=1` is mandatory: it prevents any live API call from reaching the TrustPager servers, which means a real key can never accidentally leave your machine during the test run.

### 2. Secret scan

```bash
python tools/check-no-secrets.py
```

Scans every tracked file for real credential tokens (TrustPager, Anthropic, AWS, private-key blocks) and a stray `bos.json`. Must return clean. See [`TESTING.md`](TESTING.md) for what the scanner matches and how it avoids false positives on legitimate documentation.

### 3. Lint the skill

```bash
python tools/lint-skill.py skills/<your-skill-name>
```

Checks frontmatter against the manifest schema, verifies no hardcoded `tp_live_` key or raw `supabase.co` URL in `fetch.py`, and confirms `resolve_path()` is used for all file references. Fix all reported errors.

### 4. Onboarding binding check

```bash
python tools/check-onboarding-binding.py
```

Verifies that the onboarding surface only offers skills that are genuinely keyless (i.e. `requires_credential: none`). A connected skill that sneaks into the keyless floor breaks the "works day one" promise.

### 5. Registry freshness check

```bash
python tools/registry-generator.py --check
```

Verifies that `kernel/registry.json` matches the current manifests. If you added or changed a skill, regenerate first:

```bash
python tools/registry-generator.py
```

Then run `--check` again to confirm the output is clean.

### 6. Capabilities freshness check

```bash
python tools/export-capabilities.py --check
```

Verifies that the generated capabilities doc matches the registry. If you changed the registry, regenerate:

```bash
python tools/export-capabilities.py
```

Then run `--check` again.

---

## Content rules (applies to all shipped content)

These rules apply to any text that a user or customer reads: skill bodies, `SKILL.md` descriptions, trigger phrases, templates, knowledge files, and docs.

**No em dashes.** Never use em dashes in shipped content. Break the thought into two sentences, or use a comma, a colon, or parentheses instead. Hyphens in compound words are fine.

**Positive-only copy.** Frame value by what the skill delivers, not by the pain it eliminates. "Your priced quote, ready to send" is correct. "Stop guessing what to charge" is not. See the content rules in the project [README](./README.md) for background.

These two rules are enforced by the unit tests (`test_lint_sequence.py`) and reviewed on every PR.

---

## Adding a skill: end-to-end checklist

1. Create `skills/<skill-name>/SKILL.md` with valid frontmatter and a clear body.
2. If the skill fetches live data, add `fetch.py` and `test-fixture.json`.
3. Run `python tools/lint-skill.py skills/<skill-name>` and fix any errors.
4. Regenerate the registry: `python tools/registry-generator.py`.
5. Regenerate capabilities: `python tools/export-capabilities.py`.
6. Run the full gate suite (all six steps above).
7. Open a PR with the checklist from `.github/PULL_REQUEST_TEMPLATE.md` completed.

---

## PR expectations

- The PR description should explain what changed and why.
- The PR checklist (in `.github/PULL_REQUEST_TEMPLATE.md`) must be completed, not just ticked.
- For skill additions, include a brief description of what the skill does and whether it is keyless or connected.
- Keep changes focused: one skill or one fix per PR. Large refactors should be discussed in an issue first.

---

## Questions?

Open a GitHub issue or reach the maintainers at the TrustPager team via [trustpager.com](https://trustpager.com).

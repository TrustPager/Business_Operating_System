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

### Write for the lightest model that will run it

Most operators run Claude Code on a Pro plan, which means a lighter-tier model executes your skill, not the strongest one. Dense prose with conditions buried mid-paragraph gets skimmed; explicit structure gets followed. Concretely:

- Prefer **numbered decision procedures** ("pick in this order, stop at the first rule that applies") over conditional prose.
- Put **gates before defaults**. A lighter model grabs the first strong instruction it sees; if the default is stated first, the conditions after it lose.
- State hard rules as **short imperative bullets**, one behaviour each.
- Test-read your skill asking: "could this be skimmed into the wrong action?" If a sentence carries two behaviours, split it.

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

Every test must pass. `BOS_OFFLINE=1` is mandatory: it prevents any live API call from reaching the TrustPager servers, which means a real key can never accidentally leave your machine during the test run.

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

### 7. Doctrine voice check

```bash
python tools/check-doctrine-voice.py
```

The BOS business doctrine (`knowledge/business-method.md`) carries a hard rule: the owner never hears a source's coined framework name or a guru's name — every concept surfaces under the BOS's own vocabulary. This gate scans for the source coinages and fails with the BOS-native replacement to use. Source names are allowed only in the doctrine's provenance spots and `docs/architecture/research/`.

### 8. Private-data sweep

```bash
python _scripts/sweep.py --fail-only
```

This repo is public. The sweep scans every tracked file for identities and paths that must never ship: real customer business names and personal names, internal persona and team names, internal UUIDs and infrastructure hostnames, personal contact details, and local dev paths (`C:\Users\<name>\` and client-folder paths). It is the gate that catches a real client's name left in a docstring, a README example, or sample data.

`--fail-only` is what CI runs and what you must pass. The plain `python _scripts/sweep.py` also prints the WARN tier, which flags every internal first name in the architecture docs. WARN is a review aid, not a gate, on purpose: gating on it would make the whole check noise people learn to skip. Read it by hand before a release.

The deny list carries no plaintext identities — this repo is public, so names live only as SHA-256 hashes. To add one: `python _scripts/sweep.py --hash "The Name"`, then paste only the printed hash entry.

Enable the pre-push gate once per clone (covers every worktree):

```bash
git config core.hooksPath .githooks
```

Two rules when the sweep blocks you:

- **Fix the content, not the deny list.** Deleting an entry to get green defeats the check. The only legitimate edit to `_scripts/sweep.py`'s list is adding a new identity hash.
- **When you need an example identity, invent one.** Real names cannot be pattern-matched into safety, so the convention is that every example name, mockup name, and sample-data name is fictional. One that matches a real person or client is a defect.

---

## Content rules (applies to customer- and owner-facing surfaces)

These rules apply to any text a **customer or owner reads as a finished surface**: content skills generate for customers (documents, quotes, proposals, emails, SMS, nurture sequences, social copy), the owner-facing docs (`README.md`, `INSTALL.md`, `docs/CAPABILITIES.md`), and the templates that become the owner's own files (`templates/`).

They do **not** apply to maintainer-facing text: skill bodies and knowledge files (instructions Claude reads, not the customer), `TESTING.md`, `tools/README.md`, architecture docs, and code comments. Write those clearly in whatever punctuation serves.

**No em dashes.** Never use em dashes in in-scope content. Break the thought into two sentences, or use a comma, a colon, or parentheses instead. Hyphens in compound words are fine.

**Positive-only copy.** Frame value by what the skill delivers, not by the pain it eliminates. "Your priced quote, ready to send" is correct. "Stop guessing what to charge" is not. See the content rules in the project [README](./README.md) for background.

Enforcement: the document writers (`write_docx`, `write_xlsx`, `make_pdf`) reject em dashes at the output boundary (`tools/_content_rules.py`), sequence copy is checked by `test_lint_sequence.py`, and skills that draft customer copy carry the rule as a hard requirement in their body. PR review covers the rest.

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

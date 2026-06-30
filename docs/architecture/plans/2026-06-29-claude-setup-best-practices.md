# Claude Setup Best-Practices Module Implementation Plan

> **For agentic workers:** Execute via superpowers:subagent-driven-development (fresh subagent per task + review). Run in a `track2-claude-setup` worktree. **Every task's gate:** `BOS_OFFLINE=1 python -m unittest discover -s tests` green; `python tools/check-no-secrets.py` OK; and for any skill/manifest change, `python tools/registry-generator.py --check` + `python tools/check-onboarding-binding.py` + `python tools/export-capabilities.py --check` all green in the same commit. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Ship an opt-in keyless BOS module that sets up the user's global `~/.claude/CLAUDE.md` best-practices block and merges the recommended `~/.claude/settings.json` permissions, in either a recommended or guided Q&A mode, additive and reversible, teaching as it sets up.

**Architecture:** A small keyless helper tool (`tools/setup_claude_config.py`) does the safe, idempotent, collision-defended file edits (additive JSON merge + delimited-block update under `~/.claude/`), invoked through the existing signpost (`python ~/.claude/bos-run.py tool setup_claude_config`). A keyless skill (`skills/tune-my-setup/`) drives the two modes over that tool and teaches the why. Content sources are bundled (`settings/recommended-settings.json` exists; add a recommended global-CLAUDE.md block + a knowledge method doc). It is discoverable via `/whats-possible`, NOT routed from `start-here`.

**Tech Stack:** Python stdlib (the helper), Markdown (skill, command, content, knowledge doc), JSON (settings), the signpost launcher (`run.py` `tool` mode + `_ALLOWED_TOOLS`), the offline harness + temp-home test pattern (mirror `tests/test_setup_skill_install.py`).

**Source spec (approved):** [`docs/architecture/2026-06-29-claude-setup-best-practices-design.md`](../2026-06-29-claude-setup-best-practices-design.md).

**Cross-cutting rules (every task):**
- Keyless: pure local file edits under `~/.claude/`, no account/key/network. `BOS_OFFLINE`-green.
- Cross-OS: resolve home via `Path.home()` (honors `USERPROFILE` on Windows); never touch anything outside `~/.claude/`.
- **Zero em dashes** in shipped content (the skill, command, content block, knowledge doc, any user-facing string the helper prints). Positive-only, outcome-led copy.
- Additive + reversible + show-and-ask: never clobber the user's existing global config; BOS-managed CLAUDE.md content lives in delimited markers; the module always tells the user nothing is permanent and how to change it.
- Tests touch only a TEMP home, never the real `~/.claude/` (mirror the install tests' temp-home redirection).

---

## Task 1 — the safe-config helper tool (build first; everything rides on it)
**Files:** create `tools/setup_claude_config.py`; modify `tools/run.py` (`_ALLOWED_TOOLS`); test `tests/test_setup_claude_config.py` (create).

**Build (TDD):** a stdlib CLI exposing two operations, both defended and idempotent:
- **`merge-settings`**: additively merge given `permissions.allow` / `permissions.deny` entries into `~/.claude/settings.json` (create if absent), de-duplicating, NEVER removing the user's existing entries, preserving all other keys. If the existing file is unreadable or not valid JSON, REFUSE (exit non-zero, clear message), never overwrite.
- **`merge-claude-md`**: insert-or-replace a BOS-managed block delimited by `<!-- bos:best-practices:start -->` ... `<!-- bos:best-practices:end -->` in `~/.claude/CLAUDE.md` (create if absent). Defenses (spec Issue 5): if the file is unreadable / non-UTF-8, refuse and report; if a `start` marker exists without a matching `end` (corrupted prior run), refuse and tell the user to fix it manually; only insert (zero markers) or replace-in-place (exactly one well-formed pair).
- A `--home <dir>` (or env) override so tests can point at a temp home; default `Path.home()`.
- Add `setup_claude_config` to `_ALLOWED_TOOLS` in `tools/run.py` (the signpost drift-guard `test_every_invoked_tool_is_allowlisted` requires this once a skill references it). The tool FILENAME must be exactly `tools/setup_claude_config.py` (underscores) so the allowlist entry, the skill-body `tool setup_claude_config` reference, and the file all match.

**Tests (temp home, offline):**
- merge into a NON-existent settings.json creates it with the given permissions.
- merge into an EXISTING settings.json with the user's own allow entries keeps them and adds the new ones, de-duped, other keys preserved.
- merge into a settings.json with invalid JSON REFUSES (non-zero, no overwrite).
- merge-claude-md into a non-existent file creates it with the delimited block.
- re-running merge-claude-md REPLACES only the block, leaving surrounding user content intact (idempotent).
- a file with a `start` marker and no `end` REFUSES and reports.
- (allowlist) `setup_claude_config` is in `_ALLOWED_TOOLS`.

**Acceptance:** both ops additive/idempotent/defended; refuses rather than corrupts; temp-home only; in the allowlist; suite green; no secrets; no em dashes in the tool's user-facing strings.

---

## Task 2 — recommended content sources
**Files:** create `settings/recommended-global-claude.md` (the best-practices block body); create `knowledge/claude-setup-method.md` (the why, the course reading); confirm `settings/recommended-settings.json` is the permission source (exists, no change unless a gap).

**Build:**
- **`settings/recommended-global-claude.md`**: the content that goes inside the BOS-managed block in the user's global CLAUDE.md. Best-practice, opt-in working-style + safety defaults, written positive and plain: e.g. plain-language partner, one action at a time, confirm before customer-facing sends, and the content rules (positive-only, no em dashes) offered as opt-ins. NO em dashes. Keep it tight (this lands in the user's global config, so it must be lean and high-signal).
- **`knowledge/claude-setup-method.md`**: explains the best practices and the why (the "module as course" reading the skill references). Covers: what global vs project CLAUDE.md are for, why the recommended permissions posture (pre-allow safe reads, keep writes prompting, deny destructive), and that everything is reversible. Plain, no em dashes.
- The TrustPager-permissions split per the spec: general entries always; TP read pre-allows merged with a plain explanation (harmless until connected); guided mode asks. (This is enforced in the skill body / how it calls the tool; document the intent here.)

**Acceptance:** both content files exist, lean, accurate, zero em dashes, positive-only.

---

## Task 3 — the module skill + command + wiring
**Files:** create `skills/tune-my-setup/SKILL.md`; create `commands/tune-my-setup.md`; modify `knowledge/starter-projects.md` (promote as an opt-in module); regenerate `kernel/registry.json` + `docs/CAPABILITIES.md`; confirm `/whats-possible` surfaces it.

**Build (mirror an existing keyless skill for shape, e.g. `skills/build-customer-voice/SKILL.md`):**
- Manifest: `function_slot: floor`, `requires_driver: none`, `requires_credential: none`, `data_path: local`, `status: active`. Put the "writes the user's GLOBAL `~/.claude/` config, not project files" note in the SKILL BODY, NOT the frontmatter: the manifest parser is a flat `key: value` reader that raises on a `#` comment line and would skip the skill. (Per the spec's `data_path` note.)
- Body: open by explaining what it does and that everything is reversible; offer the two modes.
  - **Recommended:** preview the global CLAUDE.md block (from `settings/recommended-global-claude.md`) and the settings.json permission merge (from `settings/recommended-settings.json`), explain each briefly (teach as it sets up), ask for a yes, then apply via `python ~/.claude/bos-run.py tool setup_claude_config merge-claude-md ...` and `... merge-settings ...`.
  - **Guided (Q&A):** ask short plain questions (how do you like Claude to work; want the positive-only / no-em-dash content rules on; do you use or plan to use TrustPager so its safe reads are pre-allowed; keep all writes prompting), explaining the why behind each, then build the same files from the answers.
  - **Project pointer:** check whether `./CLAUDE.md` exists; if not, point to `/start-here` (do NOT write the business profile here).
  - Close with the "nothing is permanent, here is how to change it" reassurance + a pointer to `knowledge/claude-setup-method.md` to explore further.
  - Keyless, positive-only, no em dashes. Carry the standard launcher note (if the signpost is missing, run setup once).
- `commands/tune-my-setup.md`: a slash-command shim (mirror `commands/price-my-work.md`), no em dashes.
- Promote in `knowledge/starter-projects.md` as a recommended OPT-IN module (tag it `keyless` so binding assertion B passes; it is a real keyless skill). Do NOT add it to `start-here` routing.
- Run `python tools/registry-generator.py` and `python tools/export-capabilities.py` to register it + refresh CAPABILITIES (add a one-liner in `export-capabilities.py` if the fallback description is poor).

**Acceptance:** the skill offers both modes, teaches the why, applies changes only via the helper with show-and-ask, points (not writes) for the project file; registry + CAPABILITIES fresh; binding check green (the app exists + is honestly keyless-tagged); lint clean; no em dashes; suite green.

---

## Task 4 — end-to-end verification
**Files:** none authored; a verification + fixes if drift found.
**Checklist (all green):**
- `BOS_OFFLINE=1 python -m unittest discover -s tests` green (the new helper tests included).
- `python tools/check-onboarding-binding.py` exits 0 (no phantom; `tune-my-setup` is registered + keyless-tagged; the drift-guard `test_every_invoked_tool_is_allowlisted` passes because `setup_claude_config` is allowlisted and the SKILL references it).
- `python tools/registry-generator.py --check` + `python tools/export-capabilities.py --check` up to date.
- `python tools/check-no-secrets.py` OK.
- Em-dash scan: zero in `skills/tune-my-setup/SKILL.md`, `commands/tune-my-setup.md`, `settings/recommended-global-claude.md`, `knowledge/claude-setup-method.md`, and any user-facing string in `tools/setup_claude_config.py`.
- **Offline end-to-end smoke** (extend the helper test or add a small one): from a temp home, run the recommended-mode operations through the signpost-equivalent (`python tools/run.py tool setup_claude_config merge-settings ...` and `merge-claude-md ...`), then assert the temp `~/.claude/settings.json` has the merged permissions and the temp `~/.claude/CLAUDE.md` has the delimited block, and that a second run is idempotent.
**Acceptance:** every check green; the module installs the global best practices safely and reversibly, keyless, cross-OS, and never corrupts an existing file.

---

## Definition of done
- [ ] `tools/setup_claude_config.py` merges settings + CLAUDE.md block additively, idempotently, refusing rather than corrupting; in `_ALLOWED_TOOLS`; temp-home tested.
- [ ] `settings/recommended-global-claude.md` + `knowledge/claude-setup-method.md` exist, lean, em-dash-free.
- [ ] `skills/tune-my-setup/` + `commands/tune-my-setup.md` ship: two modes, teaches-by-doing, additive/reversible, project-file pointer only, keyless.
- [ ] Registered in the registry + CAPABILITIES; promoted in starter-projects as an opt-in module; surfaced by `/whats-possible`; NOT routed from `start-here`.
- [ ] All gates green; zero em dashes in the module's shipped content; offline + cross-OS; the real `~/.claude/` is never touched by tests.
- [ ] Out of scope confirmed untouched: hooks/MCP-install, the project business profile (start-here's job), any Skool/course-delivery system, auto-run in onboarding.

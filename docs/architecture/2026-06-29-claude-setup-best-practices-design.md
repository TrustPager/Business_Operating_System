# Claude Setup Best-Practices Module — Design Spec

**Status:** Approved in brainstorming (2026-06-29). Next step: implementation plan via superpowers:writing-plans.

**Goal:** A keyless, opt-in BOS module that helps a user set up their Claude Code environment following best practices: a global `~/.claude/CLAUDE.md` block of cross-project preferences, the recommended `~/.claude/settings.json` permissions, and a light pointer to the project `./CLAUDE.md`. It runs in either a recommended-out-of-the-box mode or a guided Q&A mode, always additive and reversible, and it teaches as it sets up.

**Why:** BOS already ships a sensible `settings/recommended-settings.json` (pre-allow safe reads, keep writes prompting, deny destructive) but nothing applies or explains it, and nothing helps a user set up their global `~/.claude/CLAUDE.md`. `start-here` writes the project business profile only. This module closes that gap and promotes good Claude Code hygiene to every BOS user.

## Strategic framing (the "module as course" model)

This is the first instance of how BOS learning/onboarding modules should work, and it sets the template. Skool (the community) is NOT where intensive coursework lives. Skool is a lightweight signpost: *"ask your BOS about X, because Y, and go explore Z."* The real learning happens inside Claude, by doing. So this module is written to **teach as it acts**: it explains why each best practice matters (especially in guided mode), so activating the module IS the lesson. Future "courses" (e.g. "research an MCP server or CLI you find interesting and see how you'd integrate it", "explore tier-1 upgrades") follow the same shape: a short Skool pointer into a BOS module or conversation, not a PDF curriculum.

Practical consequence for this build: the module's prose is exploratory and explanatory, not just procedural. It surfaces the "why" and reassures the user that nothing is permanent and everything is changeable.

## Locked decisions (brainstorming, 2026-06-29)

1. **Standalone, opt-in module, NOT a `start-here` beat.** The keyless cold-start floor stays lean. This module is recommended and activated on demand: discoverable via `/whats-possible`, pointed to from Skool, re-runnable anytime. It is not auto-run during onboarding.
2. **Two modes:** (a) **Recommended** applies the curated best-practice build-out directly; (b) **Guided (Q&A)** asks a short series of plain questions so the user understands and chooses each setting. Both are offered up front; the user picks.
3. **Additive and reversible, always.** BOS shows what it will write and asks before writing. It never clobbers the user's existing content. BOS-managed sections live in clearly-delimited blocks so a re-run updates only those. Both modes end by telling the user plainly that nothing is permanent and exactly how to change it later.
4. **Content rules are offered as opt-ins, not imposed.** The positive-only and no-em-dash house rules are presented as recommended options the user can accept or skip (they are BOS's house style, not everyone's).

## Design

### Component A — the module skill (e.g. `skills/tune-my-setup/`)
A keyless skill: `function_slot: floor` (or `strategy`), `requires_driver: none`, `requires_credential: none`, `data_path: local` (it writes local files via a tool). Its body:
- Opens by explaining what it does and that everything is reversible, then offers the two modes (Recommended vs Guided).
- **Recommended mode:** previews the global `~/.claude/CLAUDE.md` best-practices block and the `~/.claude/settings.json` permission merge, asks for a yes, then applies them via the helper tool. Briefly explains each thing it added and how to change it.
- **Guided mode:** asks a short series of plain questions (how do you like Claude to work? do you want the positive-only / no-em-dash content rules on? which safe read actions should run without asking, keeping all writes prompting?), explaining the why behind each, then builds the same two files from the answers.
- **Project pointer:** confirms whether a project `./CLAUDE.md` exists; if not, points the user to `/start-here` (does NOT write the business profile itself — no overlap with start-here).
- Closes with the "nothing is permanent, here is how to change it" reassurance and a pointer to explore further.
- Keyless, positive-only output, no em dashes.

### Component B — the safe-config helper (`tools/`, signpost-invoked)
A keyless Python tool (e.g. `tools/setup_claude_config.py`) the skill calls via `python ~/.claude/bos-run.py tool setup_claude_config ...` (and added to the launcher allowlist). It performs the actual file edits safely:
- **`~/.claude/settings.json` merge:** additively merge a given set of `permissions.allow`/`deny` entries into the existing file (create if absent), de-duplicating, NEVER removing the user's existing entries, preserving all other keys. Valid-JSON in, valid-JSON out.
- **`~/.claude/CLAUDE.md` block:** insert or update a BOS-managed block delimited by clear markers (e.g. `<!-- bos:best-practices:start -->` ... `<!-- bos:best-practices:end -->`) so a re-run replaces only that block and leaves the rest of the user's global CLAUDE.md untouched. Create the file if absent.
- Idempotent; cross-OS (`Path.home()` / `%USERPROFILE%`); never touches anything outside `~/.claude/`.
- Takes its content/permissions input as arguments or from a bundled recommended-content source, so the skill drives both modes through the same tool.

### Source content
- Settings: reuse `settings/recommended-settings.json` (the permission allow/deny set) as the source of the recommended merge.
- Global CLAUDE.md block: author a recommended best-practices block (working-style + opt-in content rules + safety defaults), bundled in the repo (e.g. `settings/recommended-global-claude.md` or inline in the skill/tool), so both modes draw from one source.
- A `knowledge/` method doc (e.g. `knowledge/claude-setup-method.md`) explaining the best practices and the why, that the skill references and that doubles as the "course" reading.

### Wiring + discovery
- Promote in `knowledge/starter-projects.md` (as an opt-in module, NOT a cold keyless win offered by start-here) and ensure `/whats-possible` surfaces it.
- A `commands/tune-my-setup.md` slash-command shim.
- Do NOT route it from `start-here`.

## Out of scope (YAGNI)
- Hooks setup, MCP-server installation, or deep settings beyond permissions + the CLAUDE.md block.
- Writing the project business profile (that is `start-here`'s job; this only points to it).
- A Skool integration or any course-delivery system. The "module as course" model is the framing; this build ships one module, not a platform.
- Auto-running in onboarding.

## Success criteria
- A user can activate the module on demand and, in either mode, end up with a sensible global `~/.claude/CLAUDE.md` best-practices block and the recommended `~/.claude/settings.json` permissions merged in, with their pre-existing content untouched.
- Re-running updates only the BOS-managed block / re-merges permissions idempotently; never clobbers user content.
- The module explains the why and reassures reversibility (teaches as it sets up).
- It is opt-in and discoverable via `/whats-possible`, not run by `start-here`.
- Keyless and `BOS_OFFLINE`-green; the helper tool is tested against a temp home (no real `~/.claude` touched); cross-OS.
- No em dashes in shipped content; positive-only; the content rules are offered, not imposed.

## Risks
- **Editing the user's global config is sensitive.** The additive-merge + delimited-block + show-diff-and-ask discipline is the mitigation; the helper tool must be collision-safe and idempotent, tested like the install (`_install_skills`) tests.
- **Overlap with `start-here`** on the project CLAUDE.md: avoided by making this module a light pointer, not a writer, for the project file.
- **Windows path/JSON correctness:** `Path.home()` resolves via `USERPROFILE`; the install tests already exercise temp-home redirection, reuse that pattern.

# Testing & checks

BOS is a **no-code, no-Python** pack: skills and commands are Markdown that Claude reads, the studios are Node. There's no fetch layer to unit-test anymore, so "testing" here means two things — keep secrets out of the repo, and keep the pack pure-MCP. Both run in CI ([.github/workflows/test.yml](.github/workflows/test.yml)) and need no key and no network.

## What CI checks

1. **Secret scan.** [gitleaks](https://github.com/gitleaks/gitleaks-action) scans tracked files for real credentials. No `tp_live_`/`tp_test_` key (or any other secret) may ever land in the repo. The only place a key belongs is the operator's own `trustpager` MCP connection, which is never committed.

2. **No-Python guard.** The Python data-fetch runtime was removed on purpose. CI fails if any `.py` file is tracked, or if a skill/command/doc references the removed runtime (`python tools/…`, `bos-run.py`, `fetch.py`, `trustpager_api`). This is what stops the pack quietly regrowing a Python dependency.

3. **Skill frontmatter sanity.** Every `skills/*/SKILL.md` must exist and carry `name:` + `description:` frontmatter.

## Sanity-checking a skill by hand

There's no fixture harness — a skill is just instructions. To verify one:

1. **Read it.** Does Step 1 pull data via named `trustpager` MCP read tools (no `python`)? Is the digest logic spelled out as explicit rules? Are the tool names real (`list_deals`, not `list_opportunities`)?
2. **Dry-run it** against a demo workspace: trigger the skill in Claude Code with the `trustpager` MCP connected and watch the tool calls. Reads are free; any write should pause for your approval and get logged to `.bos-journal.md` (see [knowledge/safeguards.md](knowledge/safeguards.md)).
3. **Check the rails.** Anything that sends/creates/updates must draft-then-confirm, journal the write, and search-first rather than blind-retry.

## Before opening a PR

- No key anywhere (gitleaks will catch it, but check).
- No `.py` files, and no `python …` invocations in any skill, command, agent, or doc.
- New skills follow [skills/sweep-my-day/SKILL.md](skills/sweep-my-day/SKILL.md) as the gold standard.

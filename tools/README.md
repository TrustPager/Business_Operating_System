# tools/

Every file in this folder is a single-purpose Python script. Stdlib only — no `pip install` needed. Each script is named for the goal it serves, so when Claude (or you) types `ls tools/` or greps for "setup", "config", "catalog", "lint", etc., the right file shows up on the first match.

## Quick reference (intent → tool)

### Foundations

| When you want to… | Run |
|---|---|
| Set up TrustPager API access for the first time | `python tools/setup.py` |
| See what API key is stored / clear it / clear the cache | `python tools/config.py` |
| Verify your install is healthy (after setup, or when something breaks) | `python tools/check-install.py` |
| Browse all TrustPager API resources and their endpoints | `python tools/list-endpoints.py` |
| See the full schema of one endpoint (params, scopes, doc URL) | `python tools/inspect-endpoint.py <resource>` |
| Validate a Claude Code skill folder before committing | `python tools/lint-skill.py skills/<name>` |
| Run a skill against a mock fixture (offline, no credits) | `python tools/test-skill.py <name>` |

### Business audits (read-only — useful by themselves, also called by skills)

| When you want to… | Run |
|---|---|
| Audit pipeline health — stuck deals, drop-offs, value by stage | `python tools/audit-pipeline.py` |
| Audit contact data quality — duplicates, missing emails, dormant | `python tools/audit-contacts.py` |
| Find data gaps — opps without contacts, overdue tasks, etc. | `python tools/find-gaps.py` |

## How they work together

```
First run:
  setup.py            (one-time auth bootstrap)
   └─→ check-install.py   (confirm everything's connected)

Day-to-day:
  Any skill in skills/<name>/ imports from trustpager_api.py.

Building / debugging skills:
  list-endpoints.py   →  find the API surface you need
  inspect-endpoint.py →  pin down the exact params + scopes
  lint-skill.py       →  sanity-check the skill folder
  test-skill.py       →  run it against a fixture, no API calls

Maintenance:
  config.py           →  show or clear stored API key / catalog cache
```

## The shared library

`trustpager_api.py` is the one file every script (and every skill) imports. It owns:

- **Auth + HTTP** — `api_get`, `api_post`, `api_patch`, `idempotent_post`, key resolution, friendly errors for 401 / 402 / 403 / 422 / 429 / 5xx.
- **Reads at scale** — `paginate(path)` (auto-follows `next_cursor`), `parallel_get([...])` (concurrent fan-out).
- **Writes at scale** — `bulk_apply(write_fn, items)` with per-item error collection and a queued-approval bucket.
- **202 / approval queue** — POSTs that need your approval return `ApprovalPending(approval_id, body)`, not an error. Skills can `.poll()` for execution.
- **Catalog** — `get_catalog()` (24h cached), `resolve_path(resource_id, method, action, path_contains)`, `inspect_endpoint(...)`. So skill code never hardcodes a path that might drift.
- **Helpers** — `now_utc`, `parse_iso`, `days_since`, `group_count`, `top_n_by`, `log`, `emit_json`, `emit_error_and_exit`.

Skills add this once at the top:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import api_get, paginate, parallel_get, BOSError, ...
```

## Naming conventions

- **Lower-kebab-case** filenames (`list-endpoints.py`, not `listEndpoints.py`). Easier to grep and read in `ls`.
- **Verb-noun** order (`list-endpoints`, `inspect-endpoint`, `check-install`). Reads like an imperative — what the script *does*.
- **No vendor / project prefixes** (no `tp-`, no `bos-`). The folder is the namespace.
- The shared library is **snake_case** (`trustpager_api`) because Python imports it as a module — kebab-case wouldn't import.

## Adding a new tool

1. Create `tools/<verb>-<noun>.py`.
2. First 12 lines of the file = a top-of-file docstring with:
   - One-line summary (becomes the script's `argparse` description).
   - "When to use" — bullet list of scenarios.
   - "What it does" — bullet list of effects.
   - "Usage" — exact invocation examples.
3. Import `trustpager_api` if you need API access; otherwise pure stdlib.
4. Add a row to the table above.
5. If it's a domain-specific tool (works with one type of data — opportunities, contacts, etc.), say so in the docstring so AI greps land here.

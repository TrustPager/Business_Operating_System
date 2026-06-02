# Testing — and how we keep the API key out of it

The one rule: **a real `tp_live_…` key never enters a test, a fixture, CI, or
the repo.** The key is read only at runtime, by the operator, from
`~/.claude/bos.json`. Everything in the test suite runs offline against canned
data. This document is the strategy and the guard-rails that enforce it.

## The kill-switch: `BOS_OFFLINE`

Set `BOS_OFFLINE=1` and the shared library
([`tools/trustpager_api.py`](tools/trustpager_api.py)) refuses every
**authenticated** call — `_request` raises **before** it even reads the API
key. (The public, unauthenticated API catalog can still load — fetching it
can't leak a key — so `_use_live` fixtures still work in CI.) A key leak is
impossible *by construction*, not just by convention. Run anything under it:

```
BOS_OFFLINE=1 python tools/test-skill.py nurture-health
BOS_OFFLINE=1 python -m unittest discover -s tests
```

## Three layers of test

1. **Static lint** — `python tools/lint-skill.py skills/<name>` checks every
   skill's frontmatter and (for any `fetch.py`) that there's no hardcoded
   `tp_live_` key, no hardcoded `supabase.co` URL, and that paths come from
   `resolve_path()`.

2. **Offline fixture tests** — `python tools/test-skill.py <name>` monkeypatches
   `api_get` + the catalog with the skill's `test-fixture.json` and runs the
   real `fetch.py` end to end. **No key, no network.** Fixtures are *input*
   shape:

   ```json
   {
     "catalog":  { "resources": [ { "id": "...", "endpoints": [ {"method":"GET","path":"/..."} ] } ] },
     "responses": { "<resolved-path>": { "data": [ ... ], "pagination": {"has_more": false} } }
   }
   ```

   (`{"_use_live": true}` fetches the public catalog instead of inlining one —
   fine under `BOS_OFFLINE` since the catalog needs no key. Prefer inline
   catalogs for new skills so the test has zero network dependency.)

3. **Unit tests** — `tests/` holds pure-logic tests with no I/O:
   - `test_lint_sequence.py` — the house-style linter (CTA-above-image, mixed-set
     failure, em-dash, negative subjects).
   - `test_safety.py` — the offline guard actually blocks GET/POST/catalog, the
     guard fires before the key is read, and the journal redacts keys.

   Run: `python -m unittest discover -s tests -v`.

## The secret scanner

`python tools/check-no-secrets.py` scans tracked files for real credential
tokens (TrustPager / Anthropic / AWS / private-key blocks) and a stray
`bos.json`. It matches a *real* key (long token after the prefix), not the bare
`tp_live_` prefix that legitimately appears in docs — so prose is never a false
positive. **Run it before every push**; CI runs it first.

Wire it as a pre-commit hook:

```
# .git/hooks/pre-commit
#!/bin/sh
python tools/check-no-secrets.py || exit 1
```

## CI

[`.github/workflows/test.yml`](.github/workflows/test.yml) runs all of the
above on every push/PR with `BOS_OFFLINE: "1"` and **no secrets referenced
anywhere** in the workflow. Order: secret scan → lint every skill → offline
fixture tests → unit tests → linter self-check.

## The only place a real key is allowed: opt-in live smoke

Sometimes you need to confirm a `fetch.py` works against the real API. That is
**manual, local, and never the production key**:

- Use a **dedicated read-only key for the Demo workspace**, exported for the
  one command: `TRUSTPAGER_API_KEY=tp_live_<demo> python skills/<name>/fetch.py`.
- Never the production key. Never committed. Never in CI. Never echoed.
- Writes during a smoke go to the Demo workspace with controlled recipients
  only — the same boundary the rest of the platform's testing follows.

If you're unsure whether something is safe to run live, it isn't — make a
fixture instead.

## Redaction (defence in depth)

Even though a key should never appear in a write body, the journal
([`tools/journal.py`](tools/journal.py)) redacts any `tp_live_`/`tp_test_`
token from what it writes, and library error messages never print the key
(they reference the prefix only). `config.py` masks the stored key when it
shows it.

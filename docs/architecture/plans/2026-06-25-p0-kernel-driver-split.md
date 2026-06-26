# P0 — Kernel / Driver Split Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking. Run in a dedicated worktree.

**Goal:** Split the monolithic `tools/trustpager_api.py` into a vendor-neutral `kernel/runtime/` and a `drivers/trustpager/`, leaving a re-export shim so nothing downstream breaks — and prove the boundary with a no-op second driver that journals through the kernel without importing TrustPager.

**Architecture:** The kernel owns the *mechanism* (offline guard, a transport-neutral `request(driver_cfg, …)`, journaling, redaction, the 202/approval contract, paginate/parallel/bulk helpers). A **driver** is a `DriverConfig` (base_url, key_resolver, secret_pattern, error_map, approval_url, catalog/path-resolver) plus its data. TrustPager becomes the first driver; `tools/trustpager_api.py` becomes a thin re-export shim for backward compatibility.

**Tech Stack:** Python 3.12 stdlib only · `unittest` · the offline harness (`BOS_OFFLINE`, `tools/test-skill.py`, `tools/check-no-secrets.py`).

**Source spec:** `docs/architecture/bos-rearchitecture-review.md` (P0 #1, §2 kernel spec, migration Steps 0–1); `docs/architecture/implementation-roadmap.md` (P0).

**Refactor note:** This MOVES existing, working implementations — it does not rewrite them. Where a step says "move X," lift the current body from `tools/trustpager_api.py` (read it first) and re-home it; only the parameterization points below are genuinely new code.

---

## File Structure

- Create: `kernel/runtime/__init__.py` — public kernel API surface (re-exports)
- Create: `kernel/runtime/errors.py` — `BOSError`
- Create: `kernel/runtime/redaction.py` — redaction mechanism + a pattern registry (drivers register their secret regex)
- Create: `kernel/runtime/offline.py` — `is_offline()` (the `BOS_OFFLINE` guard)
- Create: `kernel/runtime/transport.py` — `DriverConfig` dataclass + `request()` (parameterized HTTP), `ApprovalPending`
- Create: `kernel/runtime/journal.py` — `record_write()` / `journaled()` (vendor-neutral)
- Create: `kernel/runtime/reads.py` — `parallel_get`, `paginate`, `bulk_apply` (driver-agnostic, take a bound get/write fn)
- Create: `kernel/runtime/helpers.py` — `now_utc`, `parse_iso`, `days_since`, `group_count`, `top_n_by`, `log`, `emit_json`, `emit_error_and_exit`, `force_utf8_stdout`
- Create: `kernel/runtime/paths.py` — `plugin_root()` (resolves `CLAUDE_PLUGIN_ROOT`, falls back to repo dir)
- Create: `drivers/trustpager/__init__.py` — the TrustPager `DriverConfig` + bound `api_get/api_post/api_patch/idempotent_post`
- Create: `drivers/trustpager/auth.py` — `get_api_key()` (env `TRUSTPAGER_API_KEY` / `~/.claude/bos.json`), the `tp_(live|test)_…` secret pattern, the 401/402/403/422 error map (with `app.trustpager.com` URLs)
- Create: `drivers/trustpager/catalog.py` — `get_catalog`, `resolve_path`, `inspect_endpoint`, `PATH_OVERRIDES`, the cross-catalog bridge, `API_BASE`, `CATALOG_URL`
- Create: `drivers/_noop/__init__.py` — the boundary-proof second driver (fake base_url, env key_resolver, own secret pattern)
- Modify: `tools/trustpager_api.py` → thin shim re-exporting `kernel.runtime` + `drivers.trustpager` (keeps all 22 `fetch.py` + `bos-run.py` working)
- Test: `tests/test_kernel_vendor_neutral.py`, `tests/test_transport_offline.py`, `tests/test_journal_redaction.py`, `tests/test_driver_boundary.py`, `tests/test_shim_compat.py`

---

## Task 0: Freeze the substrate + tag

**Files:**
- Modify: `tools/trustpager_api.py:68-73` (PATH_OVERRIDES) and `:699-714` (cross-catalog bridge) — convert the "delete ~48h post-cutover" TODO into a dated, tested guard OR delete if the upstream docs cutover has shipped (verify against `https://docs.trustpager.com/api-index.json`).
- Create: `kernel/runtime/paths.py`

- [ ] **Step 1: Tag the pre-refactor release.** `git tag pre-kernel-split && git log --oneline -1` — this is the rollback anchor; pin INSTALL.md's update step to it.
- [ ] **Step 2: Write failing test for `plugin_root()`.** `tests/test_paths.py`: assert `plugin_root()` returns the dir containing `.claude-plugin/` when `CLAUDE_PLUGIN_ROOT` is unset, and honours it when set.
- [ ] **Step 3: Run it — expect FAIL** (`python -m unittest tests.test_paths -v` → ImportError).
- [ ] **Step 4: Implement `kernel/runtime/paths.py`** with `plugin_root()` (env first, then walk up for `.claude-plugin/`).
- [ ] **Step 5: Run it — expect PASS.**
- [ ] **Step 6: Decide the PATH_OVERRIDES guard** (delete-if-shipped or dated-guard); keep `resolve_path` behaviour identical (the existing tests must still pass).
- [ ] **Step 7: Commit.** `git add -A && git commit -m "chore(p0): freeze substrate, add plugin_root(), tag pre-kernel-split"`

---

## Task 1: Kernel primitives (errors, offline, redaction, helpers)

**Files:** Create `kernel/runtime/{errors,offline,redaction,helpers}.py`; Test `tests/test_kernel_vendor_neutral.py`, `tests/test_journal_redaction.py`

- [ ] **Step 1: Write the failing vendor-neutrality test.**

```python
# tests/test_kernel_vendor_neutral.py
import pathlib, re
def test_kernel_has_no_vendor_literals():
    root = pathlib.Path(__file__).resolve().parent.parent / "kernel"
    bad = re.compile(r"tp_(live|test)_|api\.trustpager\.com|bos\.json|trustpager", re.I)
    offenders = [p for p in root.rglob("*.py") if bad.search(p.read_text(encoding="utf-8"))]
    assert offenders == [], f"vendor literals leaked into kernel: {offenders}"
```

- [ ] **Step 2: Run it — expect FAIL** (kernel/ doesn't exist yet).
- [ ] **Step 3: Implement the primitives.** Move from `tools/trustpager_api.py`: `BOSError` → `errors.py`; `_is_offline` → `offline.py` as `is_offline()`; the date/digest/log/emit helpers (`now_utc`/`parse_iso`/`days_since`/`group_count`/`top_n_by`/`log`/`emit_json`/`emit_error_and_exit`/`force_utf8_stdout`) → `helpers.py`. For `redaction.py`: move `_redact` as the *mechanism* but make the pattern a **registry** — `register_secret_pattern(regex)` + `redact(text)` applies all registered patterns. Do NOT hardcode `tp_live_` here (that registers from the driver).
- [ ] **Step 4: Run vendor-neutrality test — expect PASS.**
- [ ] **Step 5: Write + run the redaction test** (`tests/test_journal_redaction.py`): register a sample pattern, assert `redact()` masks it; assert an unregistered token is left intact.
- [ ] **Step 6: Commit.** `git commit -am "feat(kernel): vendor-neutral errors/offline/redaction/helpers"`

---

## Task 2: The transport seam — `DriverConfig` + `request()`

**Files:** Create `kernel/runtime/transport.py`, `kernel/runtime/journal.py`, `kernel/runtime/reads.py`; Test `tests/test_transport_offline.py`

- [ ] **Step 1: Write the failing offline-guard test.**

```python
# tests/test_transport_offline.py
import os, unittest
from kernel.runtime.transport import request, DriverConfig
class T(unittest.TestCase):
    def test_offline_blocks_before_key_read(self):
        os.environ["BOS_OFFLINE"] = "1"
        called = {"key": False}
        cfg = DriverConfig(base_url="https://x", key_resolver=lambda: called.__setitem__("key", True) or "k",
                           secret_pattern=r"k", error_map={}, approval_url="https://x/appr")
        with self.assertRaises(Exception):
            request(cfg, "GET", "ping")
        self.assertFalse(called["key"], "offline guard must fire BEFORE the key resolver runs")
```

- [ ] **Step 2: Run it — expect FAIL** (transport doesn't exist).
- [ ] **Step 3: Implement `transport.py`.** Define `DriverConfig` (dataclass: `base_url`, `key_resolver: Callable[[],str]`, `secret_pattern: str`, `error_map: dict[int,Callable]`, `approval_url: str`, optional `extra_headers`). Move `_build_url`, `_request`, `ApprovalPending` from the monolith — but: (a) `is_offline()` check fires FIRST (before `key_resolver()`); (b) auth header uses `cfg.key_resolver()`; (c) base URL is `cfg.base_url`; (d) HTTP-error branches call `cfg.error_map.get(code)` for vendor messaging, with a generic fallback; (e) `ApprovalPending.approval_url` defaults from `cfg.approval_url`. On import, register `cfg.secret_pattern` with the redaction registry.
- [ ] **Step 4: Run offline test — expect PASS.**
- [ ] **Step 5: Move journaling → `journal.py`** (`record_write`/`journaled`, using `redact()` from the registry; `JOURNAL_DIR` under `plugin_root()`-independent `~/.claude/bos-journal`). Move `parallel_get`/`paginate`/`bulk_apply` → `reads.py` (they take a bound `get`/`write` callable, no vendor coupling).
- [ ] **Step 6: Re-run the full offline suite** (`BOS_OFFLINE=1 python -m unittest discover -s tests -v`) — expect PASS.
- [ ] **Step 7: Commit.** `git commit -am "feat(kernel): transport seam (DriverConfig+request), journal, reads"`

---

## Task 3: The TrustPager driver

**Files:** Create `drivers/trustpager/{__init__,auth,catalog}.py`; Test `tests/test_trustpager_driver.py`

- [ ] **Step 1: Write the failing test** — `resolve_path("scheduling", path_contains="bookings")` returns `"scheduling/bookings"` against an inline fixture catalog (offline), and `get_api_key()` reads `TRUSTPAGER_API_KEY`.
- [ ] **Step 2: Run it — expect FAIL.**
- [ ] **Step 3: Implement the driver.** Move into `auth.py`: `get_api_key()` (env → `~/.claude/bos.json`), the `tp_(live|test)_[A-Za-z0-9_\-]{16,}` secret pattern, and the 401/402/403/422 error map (the `app.trustpager.com` messages). Move into `catalog.py`: `API_BASE`, `CATALOG_URL`, `get_catalog`, `resolve_path`, `inspect_endpoint`, `PATH_OVERRIDES`, the cross-catalog bridge. In `__init__.py`: build the TrustPager `DriverConfig` and expose bound `api_get/api_post/api_patch/idempotent_post` (each calls `kernel.runtime.request(TP_CONFIG, …)`, writes journaled).
- [ ] **Step 4: Run driver test — expect PASS.**
- [ ] **Step 5: Re-run the existing offline fixture tests** for two representative skills: `BOS_OFFLINE=1 python tools/test-skill.py sweep-my-day` and `… nurture-health` — expect PASS (they exercise the catalog + reads paths through the new driver).
- [ ] **Step 6: Commit.** `git commit -am "feat(drivers): trustpager driver over the kernel seam"`

---

## Task 4: The backward-compat shim

**Files:** Modify `tools/trustpager_api.py`; Test `tests/test_shim_compat.py`

- [ ] **Step 1: Write the failing import-compat test.**

```python
# tests/test_shim_compat.py
def test_shim_reexports_everything_fetch_scripts_use():
    import importlib
    m = importlib.import_module("trustpager_api")  # via the sys.path insert fetch.py uses
    for name in ["api_get","api_post","api_patch","idempotent_post","parallel_get",
                 "paginate","bulk_apply","resolve_path","get_catalog","inspect_endpoint",
                 "BOSError","ApprovalPending","now_utc","parse_iso","days_since",
                 "group_count","top_n_by","log","emit_json","emit_error_and_exit"]:
        assert hasattr(m, name), f"shim missing {name}"
```

- [ ] **Step 2: Run it — expect FAIL** (names moved out).
- [ ] **Step 3: Rewrite `tools/trustpager_api.py` as a shim** — `from kernel.runtime import *` + `from drivers.trustpager import *` (explicit re-exports of the public names above). Keep `API_BASE`/`CATALOG_URL` re-exported for any caller that referenced them. Add a module docstring: "Compatibility shim — real homes are kernel/runtime and drivers/trustpager."
- [ ] **Step 4: Run shim test — expect PASS.**
- [ ] **Step 5: Smoke every fetch script imports.** `for d in skills/*/fetch.py; do BOS_OFFLINE=1 python -c "import ast,sys; ast.parse(open('$d').read())"; done` then run the full offline fixture suite (`for d in skills/*/; do [ -f "$d/test-fixture.json" ] && python tools/test-skill.py "$(basename $d)"; done`) — expect all PASS.
- [ ] **Step 6: Commit.** `git commit -am "refactor: trustpager_api.py becomes a kernel+driver shim (no behaviour change)"`

---

## Task 5: The boundary proof — no-op second driver (THE GATE)

**Files:** Create `drivers/_noop/__init__.py`; Test `tests/test_driver_boundary.py`

- [ ] **Step 1: Write the failing boundary test.**

```python
# tests/test_driver_boundary.py
import sys, unittest
from unittest import mock
class Boundary(unittest.TestCase):
    def test_noop_driver_journals_through_kernel_without_trustpager(self):
        # import the no-op driver fresh; assert NO trustpager module loaded by it
        for m in list(sys.modules):
            if "trustpager" in m: del sys.modules[m]
        from drivers._noop import write_ping
        with mock.patch("kernel.runtime.transport._http", return_value={"data": {"id": "ok"}}):
            with mock.patch("kernel.runtime.journal.record_write") as rec:
                write_ping({"hello": "world"})
                rec.assert_called_once()          # it journaled THROUGH the kernel
        assert not any("trustpager" in m for m in sys.modules), \
            "no-op driver pulled in TrustPager — the kernel is not vendor-neutral"
```

- [ ] **Step 2: Run it — expect FAIL** (no `_noop` driver).
- [ ] **Step 3: Implement `drivers/_noop/__init__.py`** — its own `DriverConfig` (`base_url="https://example.invalid"`, `key_resolver=lambda: os.environ.get("NOOP_KEY","noop")`, `secret_pattern=r"noop_[a-z0-9]+"`, `error_map={}`, `approval_url="https://example.invalid/appr"`) and a `write_ping(body)` that calls `kernel.runtime.request(NOOP_CONFIG,"POST","ping",body=body)` via the journaled write path. It imports ONLY from `kernel.runtime` — never `drivers.trustpager`, never `trustpager_api`. (Refactor `_request` so the network call is an injectable `_http` for the test mock.)
- [ ] **Step 4: Run the boundary test — expect PASS. This is the P0 gate.**
- [ ] **Step 5: Commit.** `git commit -am "test(p0): no-op driver proves the kernel is vendor-neutral"`

---

## Task 6: Lint the boundary + full green

**Files:** Modify `tools/lint-skill.py` (or add `tools/check-kernel-clean.py`); CI `.github/workflows/test.yml`

- [ ] **Step 1: Write/extend the failing lint check** — a vendor-literal scan of `kernel/` (same regex as Task 1) wired as a FAIL, runnable standalone: `python tools/check-kernel-clean.py`.
- [ ] **Step 2: Run it — expect PASS now** (Task 1 already cleared kernel/), and prove it FAILS by temporarily planting `tp_live_x` in a kernel file, re-running, then reverting.
- [ ] **Step 3: Add the check to CI** — new step in `.github/workflows/test.yml` after the secret scan: `python tools/check-kernel-clean.py`.
- [ ] **Step 4: Full green gate.** Run the whole offline suite as CI does: secret scan → `check-kernel-clean` → lint every skill → offline fixture tests → unit tests. Expect all green.
- [ ] **Step 5: Commit + open PR.** `git commit -am "ci(p0): enforce vendor-neutral kernel"` then push the worktree branch and open a PR titled "P0: kernel/driver split".

---

## Definition of done (the P0 gate)
- [ ] `drivers/_noop` journals a write through `kernel.runtime` with **zero** TrustPager imports (Task 5 test passes).
- [ ] All 22 `fetch.py` + `bos-run.py` run unchanged (shim test + offline fixture suite green).
- [ ] `kernel/` contains no vendor literals (CI-enforced).
- [ ] No behaviour change for any existing skill (offline fixtures identical).
- [ ] `tools/trustpager_api.py` is a thin shim; the real homes are `kernel/runtime/` + `drivers/trustpager/`.

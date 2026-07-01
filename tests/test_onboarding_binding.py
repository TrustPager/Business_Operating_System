"""Tests for tools/check-onboarding-binding.py — the onboarding↔registry binding guard.

Floor Wave 0 Task 1. The shipped onboarding surface (start-here / whats-possible /
starter-projects) must only ever advertise apps that (A) actually exist in the
registry as ``status: active``, (B) are honestly keyless when offered as a cold
keyless / ``[live]`` instant-win, and (C) carry no hidden TrustPager coupling in a
``requires_credential: none`` skill body. This module proves the checker enforces
all three, plus the manifest rule that a ``credential:none`` skill may not list an
``mcp__`` tool in ``uses_tools``.

Every case builds a tiny synthetic surface (sample registry dict + sample markdown)
in a temp dir, so unit correctness never depends on the live repo tree. Offline-safe:
no network, no key.

    python -m unittest tests.test_onboarding_binding
"""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

# check-onboarding-binding.py has a hyphen, so import it by file path (the same
# trick test_registry_fresh.py uses for registry-generator.py).
_CHK_PATH = REPO / "tools" / "check-onboarding-binding.py"
_spec = importlib.util.spec_from_file_location("check_onboarding_binding", _CHK_PATH)
chk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(chk)  # type: ignore[union-attr]

# tools/manifest.py for the manifest-rule case.
from manifest import validate_manifest  # noqa: E402


# --- Sample registry ------------------------------------------------------
#
# A small, honest registry: a keyless floor app, a keyless local-driver app, and
# an mcp/trustpager app. The surface fixtures reference these by key.
_SAMPLE_REGISTRY = {
    "build-brand-strategy": {
        "requires_credential": "none",
        "requires_driver": "none",
        "data_path": "local",
        "status": "active",
    },
    "extract-document": {
        "requires_credential": "none",
        "requires_driver": "markitdown",
        "data_path": "local",
        "status": "active",
    },
    "make-social-post": {
        "requires_credential": "none",
        "requires_driver": "render",
        "data_path": "local",
        "status": "active",
    },
    "import-from-anywhere": {
        "requires_credential": "mcp",
        "requires_driver": "trustpager",
        "data_path": "mcp_tools",
        "status": "active",
    },
    "outstanding-invoices": {
        "requires_credential": "mcp",
        "requires_driver": "trustpager",
        "data_path": "mcp_tools",
        "status": "active",
    },
}


def _write_surface(tmp: Path, start_here: str = "", whats_possible: str = "",
                   starter_projects: str = "", five_day_challenge: str = "") -> None:
    """Materialise the onboarding-surface files under a temp tree.

    Mirrors the real layout: skills/start-here/SKILL.md, skills/whats-possible/
    SKILL.md, knowledge/starter-projects.md, skills/five-day-challenge/SKILL.md.
    The challenge file is always created (empty by default) so the path exists.
    """
    sh = tmp / "skills" / "start-here"
    wp = tmp / "skills" / "whats-possible"
    fd = tmp / "skills" / "five-day-challenge"
    kn = tmp / "knowledge"
    for d in (sh, wp, fd, kn):
        d.mkdir(parents=True, exist_ok=True)
    (sh / "SKILL.md").write_text(start_here, encoding="utf-8")
    (wp / "SKILL.md").write_text(whats_possible, encoding="utf-8")
    (fd / "SKILL.md").write_text(five_day_challenge, encoding="utf-8")
    (kn / "starter-projects.md").write_text(starter_projects, encoding="utf-8")


# A minimal, fully-clean start-here body: routes only to real keyless apps.
_CLEAN_START_HERE = """\
---
name: Start Here
---
# Start Here
Default `build-brand-strategy`; route by signal (doc→`extract-document`,
post→`make-social-post`).
"""

# A clean whats-possible: reads the registry, names no specific app-id.
_CLEAN_WHATS_POSSIBLE = """\
---
name: What's Possible
---
# What's Possible
Read `kernel/registry.json` and split into keyless vs connect-only. Outcomes only.
"""

# A clean starter-projects: a keyless [live] row + an honestly-tagged connected
# row + a non-routable Planned block.
_CLEAN_STARTER_PROJECTS = """\
# Starter Projects

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Brand written down | `build-brand-strategy` `[live]` | keyless |
| A branded post today | `make-social-post` `[live]` | keyless |
| Throw me any file | `extract-document` `[live]` | keyless |
| Get your list clean | `import-from-anywhere` `[live]` | better_with_crm |
| Spot uninvoiced jobs | `outstanding-invoices` `[live]` | needs_crm |

## Planned / coming soon (not buildable yet — non-routable)

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Price this job | `price-my-work` `[floor-new]` | keyless |
"""


def _run(tmp: Path, registry: dict | None = None):
    """Run the checker against a temp surface; return the list of failure strings."""
    return chk.check_onboarding_binding(
        registry=_SAMPLE_REGISTRY if registry is None else registry,
        start_here_path=tmp / "skills" / "start-here" / "SKILL.md",
        whats_possible_path=tmp / "skills" / "whats-possible" / "SKILL.md",
        starter_projects_path=tmp / "knowledge" / "starter-projects.md",
        five_day_challenge_path=tmp / "skills" / "five-day-challenge" / "SKILL.md",
        skills_dir=tmp / "skills",
    )


class TestAExists(unittest.TestCase):
    """A — every referenced app-id must be an active registry key."""

    def test_phantom_reference_fails_A(self):
        # start-here routes to `research-a-competitor`, which is NOT in the registry.
        start_here = (
            "---\nname: Start Here\n---\n# Start Here\n"
            "Default `build-brand-strategy`; route competitor→`research-a-competitor`.\n"
        )
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, start_here, _CLEAN_WHATS_POSSIBLE, _CLEAN_STARTER_PROJECTS)
            failures = _run(tmp)
            self.assertTrue(failures, "phantom reference should produce failures")
            joined = "\n".join(failures)
            self.assertIn("A", joined)
            self.assertIn("research-a-competitor", joined)

    def test_phantom_in_bullet_nonplanned_fails_A(self):
        # A phantom app named as buildable in a BULLET line (no `|`) in a NON-Planned
        # section must not evade A — the bullet-line evasion gap. `phantom-bullet-app`
        # is not in the registry and the bullet carries no Planned / [floor-new] flag.
        starter = """\
# Starter Projects

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Brand written down | `build-brand-strategy` `[live]` | keyless |

### Win work

- **Spin me up a thing** today — `phantom-bullet-app` does it cold, no setup.
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp)
            a_failures = [f for f in failures if f.startswith("A")]
            self.assertTrue(a_failures, f"bullet-line phantom should fail A: {failures}")
            joined = "\n".join(a_failures)
            self.assertIn("phantom-bullet-app", joined)

    def test_phantom_in_bullet_under_planned_heading_passes_A(self):
        # The same phantom in a BULLET under a `## Planned` heading is EXEMPT from A —
        # honestly flagged unbuilt, same exemption a Planned table row gets.
        starter = """\
# Starter Projects

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Brand written down | `build-brand-strategy` `[live]` | keyless |

## Planned / coming soon (not buildable yet — non-routable)

- **Spin me up a thing** — `phantom-bullet-app`, on the way.
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp)
            self.assertEqual(
                failures, [],
                f"bullet phantom under a Planned heading should be exempt: {failures}")


class TestBKeylessHonesty(unittest.TestCase):
    """B — a [live]/keyless-offered app the registry marks mcp/trustpager FAILS."""

    def test_live_keyless_mcp_app_fails_B(self):
        # starter-projects offers import-from-anywhere as `[live]` + keyless, but
        # the registry marks it mcp/trustpager — a dishonest keyless offer.
        starter = """\
# Starter Projects

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Brand written down | `build-brand-strategy` `[live]` | keyless |
| Get your list clean | `import-from-anywhere` `[live]` | keyless |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp)
            self.assertTrue(failures, "dishonest keyless offer should fail")
            joined = "\n".join(failures)
            self.assertIn("B", joined)
            self.assertIn("import-from-anywhere", joined)

    def test_live_mcp_app_tagged_better_with_crm_passes_B(self):
        # Same mcp app, but honestly tagged better_with_crm — EXEMPT from B.
        starter = """\
# Starter Projects

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Brand written down | `build-brand-strategy` `[live]` | keyless |
| Get your list clean | `import-from-anywhere` `[live]` | better_with_crm |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp)
            b_failures = [f for f in failures if f.startswith("B")]
            self.assertEqual(b_failures, [], f"better_with_crm should be exempt from B: {failures}")

    def test_phantom_in_planned_block_passes_A_and_B(self):
        # A [floor-new] phantom placed in the non-routable Planned block is EXEMPT
        # from both A (not routable) and B (not offered as buildable now).
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE,
                           _CLEAN_STARTER_PROJECTS)  # has price-my-work in Planned
            failures = _run(tmp)
            self.assertEqual(failures, [], f"clean surface w/ Planned block should pass: {failures}")


class TestCNoHiddenCoupling(unittest.TestCase):
    """C — a credential:none skill body with a TrustPager coupling token FAILS."""

    def test_keyless_body_with_tp_token_fails_C(self):
        # start-here is a credential:none registry skill; its body smuggles a TP tool.
        start_here = (
            "---\nname: Start Here\n---\n# Start Here\n"
            "Default `build-brand-strategy`.\n"
            "Pull the catalogue via `mcp__trustpager__list_products` quietly.\n"
        )
        registry = dict(_SAMPLE_REGISTRY)
        registry["start-here"] = {
            "requires_credential": "none",
            "requires_driver": "none",
            "data_path": "reasoning_only",
            "status": "active",
        }
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, start_here, _CLEAN_WHATS_POSSIBLE, _CLEAN_STARTER_PROJECTS)
            failures = _run(tmp, registry=registry)
            joined = "\n".join(failures)
            self.assertTrue(any(f.startswith("C") for f in failures),
                            f"hidden coupling should fail C: {failures}")
            self.assertIn("mcp__trustpager__list_products", joined)
            self.assertIn("start-here", joined)


class TestManifestRule(unittest.TestCase):
    """credential:none manifest with an mcp__ uses_tools entry must FAIL validation."""

    def test_credential_none_with_mcp_uses_tool_fails(self):
        meta = {
            "name": "Quote From Photo",
            "description": "x",
            "triggers": ["a", "b", "c"],
            "function_slot": "documents",
            "requires_driver": "none",
            "requires_credential": "none",
            "data_path": "reasoning_only",
            "uses_tools": ["mcp__trustpager__list_products"],
            "status": "active",
        }
        errors = validate_manifest(meta)
        self.assertTrue(errors, "credential:none + mcp__ uses_tools should error")
        self.assertTrue(any("uses_tools" in e and "credential" in e.lower() for e in errors),
                        f"error should name the credential:none⇒no-mcp rule: {errors}")

    def test_credential_none_without_mcp_uses_tool_passes(self):
        meta = {
            "name": "Compare Documents",
            "description": "x",
            "triggers": ["a", "b", "c"],
            "function_slot": "documents",
            "requires_driver": "markitdown",
            "requires_credential": "none",
            "data_path": "local",
            "status": "active",
        }
        self.assertEqual(validate_manifest(meta), [])

    def test_mcp_credential_with_mcp_uses_tool_still_passes(self):
        # An mcp-credential skill may legitimately list mcp__ tools.
        meta = {
            "name": "Sweep My Day",
            "description": "x",
            "triggers": ["a", "b", "c"],
            "function_slot": "crm",
            "requires_driver": "trustpager",
            "requires_credential": "mcp",
            "data_path": "mcp_tools",
            "uses_tools": ["mcp__trustpager__list_tasks"],
            "status": "active",
        }
        self.assertEqual(validate_manifest(meta), [])


class TestCleanSurfacePasses(unittest.TestCase):
    """A fully-clean surface passes A, B, and C (exit 0, no failures)."""

    def test_clean_surface_passes_everything(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE,
                           _CLEAN_STARTER_PROJECTS)
            failures = _run(tmp)
            self.assertEqual(failures, [], f"clean surface should pass: {failures}")


class TestWave1Drivers(unittest.TestCase):
    """Floor Wave 1 Increment 1: the new keyless drivers are recognised.

    - ``doclib`` (doc-lib-set keyless WRITE) counts as keyless in assertion B.
    - the firecrawl convention reconciles cleanly: a credential:none /
      requires_driver:firecrawl skill that references firecrawl in its BODY but
      lists no ``mcp__firecrawl__`` in uses_tools passes BOTH the manifest rule
      and assertion C (which only forbids TrustPager coupling).
    """

    def test_doclib_app_offered_keyless_passes_B(self):
        # A [live] + keyless app whose registry entry uses requires_driver: doclib
        # is an honest keyless offer (doclib is in _KEYLESS_DRIVERS) → B passes.
        registry = dict(_SAMPLE_REGISTRY)
        registry["write-a-proposal"] = {
            "requires_credential": "none",
            "requires_driver": "doclib",
            "data_path": "local",
            "status": "active",
        }
        starter = """\
# Starter Projects

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Brand written down | `build-brand-strategy` `[live]` | keyless |
| A real proposal | `write-a-proposal` `[live]` | keyless |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp, registry=registry)
            self.assertEqual(failures, [], f"doclib app should be keyless-honest: {failures}")

    def test_firecrawl_body_reference_passes_C(self):
        # A keyless firecrawl skill: driver in the manifest, firecrawl tools in the
        # BODY, no mcp__firecrawl__ in uses_tools. C only forbids TrustPager → passes.
        body = (
            "---\nname: Research A Competitor\n---\n# Research A Competitor\n"
            "Use `firecrawl-scrape` on the rival URL and `firecrawl-search` their "
            "name, then synthesise a one-page read.\n"
        )
        registry = dict(_SAMPLE_REGISTRY)
        registry["research-a-competitor"] = {
            "requires_credential": "none",
            "requires_driver": "firecrawl",
            "data_path": "fetch_rest",
            "status": "active",
        }
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE,
                           _CLEAN_STARTER_PROJECTS)
            (tmp / "skills" / "research-a-competitor").mkdir(parents=True, exist_ok=True)
            (tmp / "skills" / "research-a-competitor" / "SKILL.md").write_text(
                body, encoding="utf-8")
            failures = _run(tmp, registry=registry)
            self.assertEqual([f for f in failures if f.startswith("C")], [],
                             f"firecrawl body reference must not trip C: {failures}")

    def test_firecrawl_manifest_no_mcp_in_uses_tools_passes(self):
        # The manifest rule: a keyless firecrawl app declares the driver, NOT the
        # mcp__firecrawl__ tools, in uses_tools → validates clean.
        meta = {
            "name": "Research A Competitor",
            "description": "x",
            "triggers": ["a", "b", "c"],
            "function_slot": "research",
            "requires_driver": "firecrawl",
            "requires_credential": "none",
            "data_path": "fetch_rest",
            "status": "active",
        }
        self.assertEqual(validate_manifest(meta), [])


class TestChallengeBinding(unittest.TestCase):
    """The five-day-challenge orchestrator is a bound surface: every app it names
    must exist (A). It spans tiers (keyless Days 1-4 + a connected Day-5 finale),
    so naming an mcp app is fine (existence-checked, not asserted keyless)."""

    def test_phantom_app_in_challenge_fails_A(self):
        challenge = """\
---
name: Five Day Challenge
---
# Challenge
### Day 1
Run `build-brand-strategy`.
### Day 5
Run `totally-fake-app` to finish.
"""
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE,
                           _CLEAN_STARTER_PROJECTS, five_day_challenge=challenge)
            failures = _run(tmp)
            self.assertTrue(any("totally-fake-app" in f for f in failures),
                            f"phantom in challenge should fail A; got {failures}")

    def test_clean_challenge_spanning_tiers_passes(self):
        # Day 1-4 keyless app + a Day-5 connected (mcp) app: both real, so it passes.
        # The mcp app must NOT trip B, because the challenge does not assert keyless.
        challenge = """\
---
name: Five Day Challenge
---
# Challenge
### Day 1
Run `build-brand-strategy`.
### Day 5
Connect a tool, then run `outstanding-invoices` (connected).
"""
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE,
                           _CLEAN_STARTER_PROJECTS, five_day_challenge=challenge)
            self.assertEqual(_run(tmp), [])


if __name__ == "__main__":
    unittest.main()

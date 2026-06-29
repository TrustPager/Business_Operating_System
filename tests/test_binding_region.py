"""Tests for assertion D (region honesty) in tools/check-onboarding-binding.py.

Assertion D: any app whose registry entry has ``requires_region`` set must ONLY
be referenced inside an explicitly AU-gated context on the onboarding surface.
An AU app in any unmarked section (including a plain keyless offer) fails D. D
overrides B: technical keylessness does not waive the region gate.

All cases use SYNTHETIC fixtures (no real AU app exists in the registry yet;
``estimate-my-bas`` arrives in a later increment). We build in-memory registry
dicts and crafted onboarding markdown, and call the assertion function and
extractor functions directly so no filesystem layout is required for the core
assertion cases. A full end-to-end run through ``check_onboarding_binding`` is
also included to confirm D is wired into the orchestrator.

Offline-safe: no network, no key.

    python -m unittest tests.test_binding_region
"""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

# Load check-onboarding-binding.py by file path (hyphen in name).
_CHK_PATH = REPO / "tools" / "check-onboarding-binding.py"
_spec = importlib.util.spec_from_file_location("check_onboarding_binding_mod", _CHK_PATH)
chk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(chk)  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# Synthetic registries
# ---------------------------------------------------------------------------

# A keyless AU-only app (the first of its kind; ``estimate-my-bas`` is the real
# one, but it hasn't shipped yet so we use a synthetic stand-in here).
_AU_APP_ENTRY = {
    "requires_credential": "none",
    "requires_driver": "none",
    "data_path": "reasoning_only",
    "status": "active",
    "requires_region": "AU",
}

# A normal (non-region) keyless app for false-positive checks.
_PLAIN_APP_ENTRY = {
    "requires_credential": "none",
    "requires_driver": "none",
    "data_path": "reasoning_only",
    "status": "active",
}

# Registry with the AU app and a plain app.
_REGISTRY_WITH_AU = {
    "estimate-my-bas": _AU_APP_ENTRY,
    "build-brand-strategy": _PLAIN_APP_ENTRY,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_surface(tmp: Path, start_here: str = "", whats_possible: str = "",
                   starter_projects: str = "") -> None:
    sh = tmp / "skills" / "start-here"
    wp = tmp / "skills" / "whats-possible"
    kn = tmp / "knowledge"
    for d in (sh, wp, kn):
        d.mkdir(parents=True, exist_ok=True)
    (sh / "SKILL.md").write_text(start_here, encoding="utf-8")
    (wp / "SKILL.md").write_text(whats_possible, encoding="utf-8")
    (kn / "starter-projects.md").write_text(starter_projects, encoding="utf-8")


def _run(tmp: Path, registry: dict):
    return chk.check_onboarding_binding(
        registry=registry,
        start_here_path=tmp / "skills" / "start-here" / "SKILL.md",
        whats_possible_path=tmp / "skills" / "whats-possible" / "SKILL.md",
        starter_projects_path=tmp / "knowledge" / "starter-projects.md",
        skills_dir=tmp / "skills",
    )


# A minimal clean start-here that references only the plain app.
_CLEAN_START_HERE = """\
---
name: Start Here
---
# Start Here
Default `build-brand-strategy` for any owner.
"""

# A clean whats-possible with no specific app-ids.
_CLEAN_WHATS_POSSIBLE = """\
---
name: What's Possible
---
# What's Possible
Read `kernel/registry.json` and list apps.
"""


# ---------------------------------------------------------------------------
# Direct unit tests for _check_region_honesty
# ---------------------------------------------------------------------------

class TestCheckRegionHonestyDirect(unittest.TestCase):
    """Test assertion D directly via _check_region_honesty, using crafted References."""

    def _make_ref(self, app_id, *, au_gated, offered_keyless=True, planned=False):
        return chk.Reference(
            app_id,
            "starter-projects",
            offered_keyless=offered_keyless,
            connected_tier=False,
            planned=planned,
            au_gated=au_gated,
        )

    def test_au_app_in_unmarked_context_fails_D(self):
        # An AU app referenced without any AU gate fails D.
        ref = self._make_ref("estimate-my-bas", au_gated=False, offered_keyless=True)
        failures = chk._check_region_honesty(_REGISTRY_WITH_AU, [ref])
        self.assertTrue(failures, "AU app in unmarked context should fail D")
        self.assertTrue(any(f.startswith("D") for f in failures), f"failure must be tagged D: {failures}")
        self.assertIn("estimate-my-bas", failures[0])
        self.assertIn("requires_region", failures[0])

    def test_au_app_in_au_gated_context_passes_D(self):
        # The same AU app with au_gated=True passes D.
        ref = self._make_ref("estimate-my-bas", au_gated=True, offered_keyless=True)
        failures = chk._check_region_honesty(_REGISTRY_WITH_AU, [ref])
        self.assertEqual(failures, [], f"AU app inside AU-gated context should pass D: {failures}")

    def test_plain_app_in_unmarked_context_passes_D(self):
        # A normal (non-region) app in any context is not subject to D.
        ref = self._make_ref("build-brand-strategy", au_gated=False, offered_keyless=True)
        failures = chk._check_region_honesty(_REGISTRY_WITH_AU, [ref])
        self.assertEqual(failures, [], f"plain app should not trigger D: {failures}")

    def test_planned_au_app_is_exempt_from_D(self):
        # A planned/unbuilt reference is not offered; D does not apply.
        ref = self._make_ref("estimate-my-bas", au_gated=False, offered_keyless=False,
                             planned=True)
        failures = chk._check_region_honesty(_REGISTRY_WITH_AU, [ref])
        self.assertEqual(failures, [], f"planned AU app should be exempt from D: {failures}")

    def test_au_app_not_in_registry_is_exempt_from_D(self):
        # A phantom AU app (not in registry) is already caught by A; D skips it.
        ref = self._make_ref("phantom-au-app", au_gated=False, offered_keyless=True)
        failures = chk._check_region_honesty(_REGISTRY_WITH_AU, [ref])
        self.assertEqual(failures, [], f"phantom not in registry should not double-report in D: {failures}")


# ---------------------------------------------------------------------------
# Extractor: AU-gated heading detection in extract_starter_projects_refs
# ---------------------------------------------------------------------------

class TestExtractorAuGatedHeading(unittest.TestCase):
    """Verify that extract_starter_projects_refs sets au_gated correctly."""

    def test_row_under_au_heading_is_au_gated(self):
        text = """\
## Australia only

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Lodge my BAS | `estimate-my-bas` `[live]` | keyless |
"""
        refs = chk.extract_starter_projects_refs(text)
        au_refs = [r for r in refs if r.app_id == "estimate-my-bas"]
        self.assertTrue(au_refs, "should extract estimate-my-bas")
        self.assertTrue(all(r.au_gated for r in au_refs),
                        "row under AU heading must be au_gated=True")

    def test_row_under_non_au_heading_is_not_au_gated(self):
        text = """\
## Win work

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Build my brand | `build-brand-strategy` `[live]` | keyless |
"""
        refs = chk.extract_starter_projects_refs(text)
        plain_refs = [r for r in refs if r.app_id == "build-brand-strategy"]
        self.assertTrue(plain_refs, "should extract build-brand-strategy")
        self.assertTrue(all(not r.au_gated for r in plain_refs),
                        "row under non-AU heading must be au_gated=False")

    def test_row_with_inline_au_tag_is_au_gated(self):
        text = """\
## Tax and compliance

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Lodge my BAS | `estimate-my-bas` `[live]` | keyless requires_region:au |
"""
        refs = chk.extract_starter_projects_refs(text)
        au_refs = [r for r in refs if r.app_id == "estimate-my-bas"]
        self.assertTrue(au_refs, "should extract estimate-my-bas")
        self.assertTrue(all(r.au_gated for r in au_refs),
                        "row with requires_region:au tag must be au_gated=True")

    def test_row_without_inline_tag_under_generic_heading_is_not_au_gated(self):
        text = """\
## Tax and compliance

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Lodge my BAS | `estimate-my-bas` `[live]` | keyless |
"""
        refs = chk.extract_starter_projects_refs(text)
        au_refs = [r for r in refs if r.app_id == "estimate-my-bas"]
        self.assertTrue(au_refs)
        self.assertTrue(all(not r.au_gated for r in au_refs),
                        "generic heading, no inline tag => au_gated=False")

    def test_au_gated_heading_resets_after_next_non_au_heading(self):
        # After an AU-gated section, a subsequent plain heading must clear the flag.
        text = """\
## Australian businesses

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Lodge my BAS | `estimate-my-bas` `[live]` | keyless |

## Win work

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Build my brand | `build-brand-strategy` `[live]` | keyless |
"""
        refs = chk.extract_starter_projects_refs(text)
        au_refs = [r for r in refs if r.app_id == "estimate-my-bas"]
        plain_refs = [r for r in refs if r.app_id == "build-brand-strategy"]
        self.assertTrue(all(r.au_gated for r in au_refs), "AU section rows should be au_gated")
        self.assertTrue(all(not r.au_gated for r in plain_refs),
                        "subsequent plain section rows must NOT be au_gated")


# ---------------------------------------------------------------------------
# End-to-end: D wired into check_onboarding_binding
# ---------------------------------------------------------------------------

class TestAssertionDEndToEnd(unittest.TestCase):
    """Full surface + registry runs that exercise D through the orchestrator."""

    def test_au_app_as_plain_keyless_offer_in_starter_projects_fails_D(self):
        # The AU app appears as a plain [live]+keyless row with no AU-gated heading
        # and no inline tag. D must fail; B must NOT also fire (D takes priority by
        # design, but both could fire; we just assert D is present).
        starter = """\
# Starter Projects

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Build my brand | `build-brand-strategy` `[live]` | keyless |
| Lodge my BAS | `estimate-my-bas` `[live]` | keyless |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp, _REGISTRY_WITH_AU)
            d_failures = [f for f in failures if f.startswith("D")]
            self.assertTrue(d_failures,
                            f"AU app in unmarked keyless offer should fail D: {failures}")
            self.assertIn("estimate-my-bas", "\n".join(d_failures))

    def test_au_app_under_au_gated_heading_passes_D(self):
        # The AU app is in a clearly AU-gated section. D passes.
        starter = """\
# Starter Projects

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Build my brand | `build-brand-strategy` `[live]` | keyless |

## Australia only

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Lodge my BAS | `estimate-my-bas` `[live]` | keyless |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp, _REGISTRY_WITH_AU)
            d_failures = [f for f in failures if f.startswith("D")]
            self.assertEqual(d_failures, [],
                             f"AU app inside AU-gated section should pass D: {failures}")

    def test_au_app_with_inline_tag_passes_D(self):
        # The AU app has the requires_region:au inline tag on the same row. D passes.
        starter = """\
# Starter Projects

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Build my brand | `build-brand-strategy` `[live]` | keyless |
| Lodge my BAS | `estimate-my-bas` `[live]` | keyless requires_region:au |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp, _REGISTRY_WITH_AU)
            d_failures = [f for f in failures if f.startswith("D")]
            self.assertEqual(d_failures, [],
                             f"AU app with requires_region:au tag should pass D: {failures}")

    def test_normal_app_in_keyless_offer_is_not_affected_by_D(self):
        # A non-region app in a plain keyless offer does not trigger D (no false positive).
        starter = """\
# Starter Projects

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Build my brand | `build-brand-strategy` `[live]` | keyless |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp, _REGISTRY_WITH_AU)
            d_failures = [f for f in failures if f.startswith("D")]
            self.assertEqual(d_failures, [],
                             f"plain app in keyless offer should not trigger D: {failures}")

    def test_au_app_in_start_here_without_tag_fails_D(self):
        # An AU app routed via start-here with no inline requires_region:au tag fails D.
        start_here = """\
---
name: Start Here
---
# Start Here
Default `build-brand-strategy`; AU owners route to `estimate-my-bas`.
"""
        starter = """\
# Starter Projects

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Build my brand | `build-brand-strategy` `[live]` | keyless |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, start_here, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp, _REGISTRY_WITH_AU)
            d_failures = [f for f in failures if f.startswith("D")]
            self.assertTrue(d_failures,
                            f"AU app routed from start-here without tag should fail D: {failures}")

    def test_au_app_in_start_here_with_inline_tag_passes_D(self):
        # An AU app routed via start-here WITH the inline requires_region:au tag passes D.
        start_here = """\
---
name: Start Here
---
# Start Here
Default `build-brand-strategy`; route AU owners to `estimate-my-bas` requires_region:au.
"""
        starter = """\
# Starter Projects

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Build my brand | `build-brand-strategy` `[live]` | keyless |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, start_here, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp, _REGISTRY_WITH_AU)
            d_failures = [f for f in failures if f.startswith("D")]
            self.assertEqual(d_failures, [],
                             f"AU app with inline tag in start-here should pass D: {failures}")


# ---------------------------------------------------------------------------
# Strict AU-gate heading regex (the bare lowercase "au" must NOT gate)
# ---------------------------------------------------------------------------

class TestAuGateHeadingStrictness(unittest.TestCase):
    """is_au_gated_heading must gate only on Australia/Australian or uppercase AU.

    A bare lowercase word "au" (au revoir, review au integrations) must NEVER gate,
    or a region-restricted app could leak through a heading that only coincidentally
    contains the letters a-u.
    """

    def test_bare_lowercase_au_revoir_does_not_gate(self):
        self.assertFalse(chk.is_au_gated_heading("au revoir"),
                         "'au revoir' must NOT be AU-gated")

    def test_bare_lowercase_au_in_prose_does_not_gate(self):
        self.assertFalse(chk.is_au_gated_heading("review au integrations"),
                         "'review au integrations' must NOT be AU-gated")

    def test_uppercase_AU_token_gates(self):
        self.assertTrue(chk.is_au_gated_heading("AU"), "'AU' must be AU-gated")

    def test_australia_word_gates(self):
        self.assertTrue(chk.is_au_gated_heading("Australia"), "'Australia' must gate")

    def test_australian_tax_tools_gates(self):
        self.assertTrue(chk.is_au_gated_heading("Australian tax tools"),
                        "'Australian tax tools' must gate")

    def test_lowercase_australia_word_still_gates(self):
        # The geographic word matches case-insensitively, so lowercase prose gates.
        self.assertTrue(chk.is_au_gated_heading("for australia only"),
                        "lowercase 'australia' word must still gate (case-insensitive)")

    def test_lowercase_acronym_au_does_not_gate_even_with_suffix(self):
        # Even "au only" must not gate: the bare lowercase acronym is not a real gate.
        self.assertFalse(chk.is_au_gated_heading("au only"),
                         "'au only' (lowercase acronym) must NOT gate")

    def test_au_app_under_au_revoir_heading_fails_D(self):
        # End-to-end: an AU app under a `## au revoir` heading is NOT gated, fails D.
        starter = """\
# Starter Projects

## au revoir

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Lodge my BAS | `estimate-my-bas` `[live]` | keyless |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp, _REGISTRY_WITH_AU)
            d_failures = [f for f in failures if f.startswith("D")]
            self.assertTrue(d_failures,
                            f"AU app under 'au revoir' must fail D: {failures}")

    def test_au_app_under_review_au_integrations_heading_fails_D(self):
        starter = """\
# Starter Projects

## review au integrations

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Lodge my BAS | `estimate-my-bas` `[live]` | keyless |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp, _REGISTRY_WITH_AU)
            d_failures = [f for f in failures if f.startswith("D")]
            self.assertTrue(d_failures,
                            f"AU app under 'review au integrations' must fail D: {failures}")

    def test_au_app_under_uppercase_AU_heading_passes_D(self):
        starter = """\
# Starter Projects

## AU

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Lodge my BAS | `estimate-my-bas` `[live]` | keyless |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp, _REGISTRY_WITH_AU)
            d_failures = [f for f in failures if f.startswith("D")]
            self.assertEqual(d_failures, [],
                             f"AU app under '## AU' must pass D: {failures}")

    def test_au_app_under_australian_tax_tools_heading_passes_D(self):
        starter = """\
# Starter Projects

## Australian tax tools

| Project | Builds on | Keyless/CRM |
|---|---|---|
| Lodge my BAS | `estimate-my-bas` `[live]` | keyless |
"""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            _write_surface(tmp, _CLEAN_START_HERE, _CLEAN_WHATS_POSSIBLE, starter)
            failures = _run(tmp, _REGISTRY_WITH_AU)
            d_failures = [f for f in failures if f.startswith("D")]
            self.assertEqual(d_failures, [],
                             f"AU app under '## Australian tax tools' must pass D: {failures}")


# ---------------------------------------------------------------------------
# D overrides B: au_only app is keyless but still fails D when unmarked
# ---------------------------------------------------------------------------

class TestAssertionDOverridesB(unittest.TestCase):
    """D must fire for an AU-only app in an unmarked keyless offer even if B would pass.

    The AU app is genuinely keyless (requires_credential: none, requires_driver: none),
    so B alone would let it through. D must still catch it when au_gated is False.
    """

    def test_au_keyless_app_unmarked_fails_D_not_just_B(self):
        # Build a Reference that is keyless-honest for B (would pass B) but is not
        # AU-gated. D must fire.
        ref = chk.Reference(
            "estimate-my-bas",
            "starter-projects",
            offered_keyless=True,
            connected_tier=False,
            planned=False,
            au_gated=False,
        )
        registry = {"estimate-my-bas": _AU_APP_ENTRY}

        b_failures = chk._check_keyless_honesty(registry, [ref])
        d_failures = chk._check_region_honesty(registry, [ref])

        # B passes (app IS keyless).
        self.assertEqual(b_failures, [],
                         f"AU keyless app should pass B (it IS keyless): {b_failures}")
        # D fails (app is AU-only but not gated).
        self.assertTrue(d_failures,
                        "AU keyless app in unmarked context must fail D even though B passes")
        self.assertTrue(any(f.startswith("D") for f in d_failures))


if __name__ == "__main__":
    unittest.main()

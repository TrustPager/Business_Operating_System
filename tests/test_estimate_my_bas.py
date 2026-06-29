"""Tests for the estimate-my-bas AU pack activation (P5 final increment).

estimate-my-bas is the first real Australia-only floor app. It is reachable ONLY
when the owner has explicitly confirmed their business is in Australia
(``Region: AU`` in the profile). The gate must hold at every layer; these tests
lock the ones that are checkable offline:

  1. Registry honesty: the generated registry entry carries
     ``requires_region: "AU"`` and is otherwise keyless (credential none, keyless
     driver, reasoning-only). This is the manifest-layer gate, frozen.

  2. Binding (assertion D): the SHIPPED onboarding surface passes the
     onboarding-binding check WITH estimate-my-bas present, i.e. it is referenced
     only inside AU-gated context. A guard case (mirroring tests/test_binding_region.py)
     proves the gate is live for THIS real app: a synthetic reference to
     estimate-my-bas OUTSIDE an AU-gated context is flagged by assertion D.

  3. Skill-body gate: the SKILL.md body contains the Region-gate refusal
     instruction, so the "decline unless Region: AU" step cannot be silently
     removed.

The data-loader layer (``load_au_constants`` refusing any non-"AU" region) is
already covered by its own tests; we do not duplicate it here.

Offline-safe: no network, no key.

    python -m unittest tests.test_estimate_my_bas
"""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

APP_ID = "estimate-my-bas"

# Keyless drivers, mirroring the contract in check-onboarding-binding.py.
_KEYLESS_DRIVERS = frozenset({"none", "markitdown", "render", "firecrawl", "doclib"})

# Load check-onboarding-binding.py by file path (hyphen in name).
_CHK_PATH = REPO / "tools" / "check-onboarding-binding.py"
_spec = importlib.util.spec_from_file_location("check_onboarding_binding_mod", _CHK_PATH)
chk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(chk)  # type: ignore[union-attr]


def _load_registry() -> dict:
    return json.loads((REPO / "kernel" / "registry.json").read_text(encoding="utf-8"))


def _skill_body() -> str:
    text = (REPO / "skills" / APP_ID / "SKILL.md").read_text(encoding="utf-8")
    return chk._split_body(text)


# ---------------------------------------------------------------------------
# 1. Registry: requires_region AU + otherwise keyless
# ---------------------------------------------------------------------------

class TestRegistryEntry(unittest.TestCase):
    """The generated registry entry is AU-gated and otherwise keyless."""

    def setUp(self):
        self.registry = _load_registry()

    def test_app_is_in_registry_and_active(self):
        self.assertIn(APP_ID, self.registry, "estimate-my-bas must be in the registry")
        self.assertEqual(self.registry[APP_ID].get("status", "active"), "active",
                         "estimate-my-bas must be status: active")

    def test_requires_region_is_AU(self):
        entry = self.registry[APP_ID]
        self.assertEqual(entry.get("requires_region"), "AU",
                         "estimate-my-bas must carry requires_region: AU")

    def test_otherwise_keyless(self):
        # The region gate is the ONLY restriction: no credential, keyless driver,
        # reasoning-only data path. (D will still gate it on the surface.)
        entry = self.registry[APP_ID]
        self.assertEqual(entry.get("requires_credential"), "none",
                         "estimate-my-bas must be requires_credential: none")
        self.assertIn(entry.get("requires_driver"), _KEYLESS_DRIVERS,
                      "estimate-my-bas must use a keyless driver")
        self.assertEqual(entry.get("data_path"), "reasoning_only",
                         "estimate-my-bas must be reasoning_only")

    def test_accounting_slot(self):
        self.assertEqual(self.registry[APP_ID].get("function_slot"), "accounting",
                         "estimate-my-bas must be function_slot: accounting")


# ---------------------------------------------------------------------------
# 2. Binding: the SHIPPED surface passes assertion D with the app present
# ---------------------------------------------------------------------------

class TestShippedSurfacePassesAssertionD(unittest.TestCase):
    """The real onboarding surface must satisfy assertion D with estimate-my-bas live."""

    def test_full_binding_check_passes(self):
        registry = _load_registry()
        paths = {
            "start_here_path": REPO / "skills" / "start-here" / "SKILL.md",
            "whats_possible_path": REPO / "skills" / "whats-possible" / "SKILL.md",
            "starter_projects_path": REPO / "knowledge" / "starter-projects.md",
            "skills_dir": REPO / "skills",
        }
        failures = chk.check_onboarding_binding(registry=registry, **paths)
        self.assertEqual(failures, [],
                         f"shipped onboarding surface must pass A/B/C/D with "
                         f"estimate-my-bas present: {failures}")

    def test_estimate_my_bas_is_only_referenced_au_gated(self):
        # Specifically: no D failure mentioning estimate-my-bas anywhere on the surface.
        registry = _load_registry()
        paths = {
            "start_here_path": REPO / "skills" / "start-here" / "SKILL.md",
            "whats_possible_path": REPO / "skills" / "whats-possible" / "SKILL.md",
            "starter_projects_path": REPO / "knowledge" / "starter-projects.md",
            "skills_dir": REPO / "skills",
        }
        failures = chk.check_onboarding_binding(registry=registry, **paths)
        d_about_bas = [f for f in failures if f.startswith("D") and APP_ID in f]
        self.assertEqual(d_about_bas, [],
                         f"estimate-my-bas must never trip assertion D on the shipped "
                         f"surface: {d_about_bas}")


class TestAssertionDProtectsThisRealApp(unittest.TestCase):
    """Guard: the region gate is LIVE for estimate-my-bas specifically.

    Mirrors tests/test_binding_region.py style: construct a synthetic reference
    to the REAL app outside an AU-gated context, against the REAL registry entry,
    and assert assertion D flags it. This proves the gate protects this app, not
    just the earlier synthetic stand-in.
    """

    def test_reference_outside_au_context_is_flagged(self):
        registry = _load_registry()
        # A reference with au_gated=False, exactly as the surface would produce for
        # an un-gated row/line that names estimate-my-bas.
        ref = chk.Reference(
            APP_ID,
            "starter-projects",
            offered_keyless=True,
            connected_tier=False,
            planned=False,
            au_gated=False,
        )
        failures = chk._check_region_honesty(registry, [ref])
        self.assertTrue(failures,
                        "estimate-my-bas referenced outside an AU-gated context must fail D")
        self.assertTrue(any(f.startswith("D") for f in failures),
                        f"failure must be tagged D: {failures}")
        self.assertIn(APP_ID, failures[0])

    def test_reference_inside_au_context_passes(self):
        registry = _load_registry()
        ref = chk.Reference(
            APP_ID,
            "starter-projects",
            offered_keyless=True,
            connected_tier=False,
            planned=False,
            au_gated=True,
        )
        failures = chk._check_region_honesty(registry, [ref])
        self.assertEqual(failures, [],
                         f"estimate-my-bas inside an AU-gated context must pass D: {failures}")

    def test_starter_projects_extracts_bas_as_au_gated(self):
        # The actual starter-projects.md row for estimate-my-bas must extract as au_gated.
        text = (REPO / "knowledge" / "starter-projects.md").read_text(encoding="utf-8")
        refs = chk.extract_starter_projects_refs(text)
        bas_refs = [r for r in refs if r.app_id == APP_ID]
        self.assertTrue(bas_refs, "starter-projects.md must reference estimate-my-bas")
        self.assertTrue(all(r.au_gated for r in bas_refs),
                        "every estimate-my-bas reference in starter-projects.md must be au_gated")


# ---------------------------------------------------------------------------
# 3. Skill body: the Region-gate refusal instruction is present
# ---------------------------------------------------------------------------

class TestSkillBodyRegionGate(unittest.TestCase):
    """The SKILL body must instruct reading Region: and declining unless it is AU."""

    def setUp(self):
        self.body = _skill_body()
        self.low = self.body.lower()

    def test_body_references_reading_region_line(self):
        self.assertIn("region:", self.low,
                      "SKILL body must reference the profile Region: line")
        self.assertIn("./claude.md", self.low,
                      "SKILL body must point at the owner's profile (./CLAUDE.md)")

    def test_body_declines_when_not_AU(self):
        # The body must state it declines / stops when Region is not exactly AU.
        self.assertIn("AU", self.body,
                      "SKILL body must name the AU region value")
        declines = any(word in self.low for word in ("decline", "stop", "switched off", "switch it on"))
        self.assertTrue(declines,
                        "SKILL body must instruct declining/stopping when Region is not AU")
        self.assertTrue("exactly" in self.low and "au" in self.low,
                        "SKILL body must require Region to be exactly AU")

    def test_body_refuses_to_infer_from_free_text_city(self):
        # The non-inference rule must be explicit in the body.
        self.assertTrue(
            ("never infer" in self.low) or ("does not open the gate" in self.low)
            or ("not open the gate" in self.low),
            "SKILL body must state Region is never inferred from a free-text city/address",
        )

    def test_body_states_prepare_only_never_lodge(self):
        # The prepare-only / never-lodge hard rule must be in the body.
        self.assertIn("lodge", self.low, "SKILL body must address lodging")
        self.assertTrue(
            ("never lodge" in self.low) or ("never file" in self.low)
            or ("prepare-only" in self.low) or ("prepare only" in self.low),
            "SKILL body must state it prepares figures only and never lodges",
        )


if __name__ == "__main__":
    unittest.main()

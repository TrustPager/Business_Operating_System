"""Regression tests for tools/check-doctrine-voice.py.

A voice gate with no teeth is worse than none: it would read as "the
vocabulary is enforced" while drift walks straight past it. These tests plant
known coined terms and assert the scanner flags them, assert clean BOS
vocabulary passes, and assert the live repo is currently clean outside the
allowed provenance locations.

Offline-safe: no network, no key. Run:
    python -m unittest tests.test_doctrine_voice
"""

import importlib.util
import pathlib
import unittest

_CHECKER_PATH = (
    pathlib.Path(__file__).resolve().parent.parent
    / "tools" / "check-doctrine-voice.py"
)
_spec = importlib.util.spec_from_file_location("check_doctrine_voice", _CHECKER_PATH)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


class TestPlantedCoinedTerms(unittest.TestCase):
    """Every coined term the rule bans must be caught when planted."""

    PLANTED = [
        "Let's build your Grand Slam Offer today.",
        "As Hormozi says, volume wins.",
        "Name it with the MAGIC formula.",
        "Run the CLOSER framework on the call.",
        "Commit to the Rule of 100 first.",
        "Pick one of the Core Four channels.",
        "Keep the Silent Sixth running.",
        "Redesign with the Delivery Cube.",
        "Install the Five Horsemen of retention.",
        "Find a starving crowd before you build.",
        "Don't let the niche slap get you.",
        "BAMFAM: never leave without the next booking.",
        "Beware the woman in the red dress.",
        "That's one of the Seven Deadly Growth Sins.",
        "Aim for client-financed acquisition.",
        "Score the Dream Outcome first.",
        "Raise the Perceived Likelihood with proof.",
        "Cut the Time Delay to a first win.",
        "Reduce Effort & Sacrifice to near zero.",
        "This mirrors $100M Offers chapter three.",
        "April Dunford's ladder applies here.",
        "Gerber's E-Myth covers this.",
        "Use the Triple-A loop on objections.",
        "The Gym Launch playbook covers this.",
    ]

    def test_each_planted_term_is_flagged(self):
        for snippet in self.PLANTED:
            with self.subTest(snippet=snippet):
                findings = _mod.scan_text(snippet)
                self.assertTrue(
                    findings,
                    f"planted coined term not flagged: {snippet!r}",
                )

    def test_bos_vocabulary_passes(self):
        clean = "\n".join([
            "Build the Category-of-One offer using the five naming parts.",
            "Score the Arrival, the Belief, the Wait, and the Work.",
            "Run the discovery arc on the call; keep the standing engine on.",
            "Hold the volume floor on one of the four doors.",
            "Check the self-funding bar and the market gate first.",
            "The retention cadence and the delivery grid handle the rest.",
            "The shiny-object rule and the seven stuck-points apply.",
            "That's the Day 1 magic: a closer look at their real business.",
        ])
        self.assertEqual(_mod.scan_text(clean), [],
                         "clean BOS vocabulary must not be flagged")

    def test_common_prose_does_not_false_positive(self):
        prose = "\n".join([
            "Move a step closer to the goal and keep the magic alive.",
            "There was some delay in time before the effort paid off.",
            "The core team met four times; the rule was simple.",
        ])
        self.assertEqual(_mod.scan_text(prose), [],
                         "ordinary prose must not trip the coined-term scan")


class TestAllowedLocations(unittest.TestCase):
    def test_doctrine_and_research_are_allowed(self):
        self.assertTrue(_mod._is_allowed("knowledge/business-method.md"))
        self.assertTrue(_mod._is_allowed(
            "docs/architecture/research/business-doctrine/report-1-offers-value.md"))
        self.assertTrue(_mod._is_allowed(
            "docs\\architecture\\research\\business-doctrine\\critic-rulings.md"))

    def test_owner_facing_surfaces_are_not_allowed(self):
        for rel in ["skills/price-my-work/SKILL.md", "README.md",
                    "knowledge/industry-notes.md", "commands/start-here.md",
                    "docs/CAPABILITIES.md", "templates/CLAUDE.md"]:
            with self.subTest(rel=rel):
                self.assertFalse(_mod._is_allowed(rel))


class TestProvenanceLinesMayNameASource(unittest.TestCase):
    """Crediting a source on a labelled provenance line is the point of those lines."""

    def test_labelled_provenance_line_is_exempt(self):
        line = ("> Source note (dev-facing): the outlier multiple synthesises "
                "Kallaway's outlier-score framework, rewritten for a service business.")
        self.assertEqual(_mod.scan_text(line), [],
                         "a labelled provenance line may name its source")

    def test_the_same_name_in_ordinary_prose_is_caught(self):
        line = "Use Kallaway's bullseye when planning the channel."
        found = _mod.scan_text(line)
        self.assertTrue(any("Kallaway" in what for _, what, _ in found),
                        "an unlabelled mention must still be caught")


class TestVendorSurfacesCarryTheOwnersBrand(unittest.TestCase):
    """A surface an owner's own brand fills must not ship someone else's."""

    def test_owner_brand_surfaces_are_scanned(self):
        for rel in ["studio/thumbnails/src/templates/heroes/Hero.jsx",
                    "studio/social/src/templates/index.js",
                    "studio/social/src/data/samples.json"]:
            with self.subTest(rel=rel):
                self.assertTrue(_mod._is_vendor_surface(rel))

    def test_connected_driver_and_its_tooling_are_not_scanned(self):
        """Naming the connected platform where it IS the platform is legitimate."""
        for rel in ["drivers/trustpager/README.md", "tools/trustpager_api.py",
                    "skills/design-nurture-sequence/SKILL.md",
                    "knowledge/connectors.md", "studio/social/scripts/publish.js"]:
            with self.subTest(rel=rel):
                self.assertFalse(_mod._is_vendor_surface(rel))

    def test_the_gate_carries_no_exceptions(self):
        """The two it briefly carved out were moved out of the pack instead."""
        self.assertFalse(hasattr(_mod, "VENDOR_SURFACE_EXCEPTIONS"),
                         "an exception list is how a brand-agnosticism rule rots")

    def test_a_vendor_brand_on_an_owner_surface_is_caught(self):
        found = _mod.scan_text("// TrustPager Thumbnail Studio tokens.",
                               vendor_surface=True)
        self.assertTrue(any("TrustPager" in what for _, what, _ in found))

    def test_the_same_line_off_that_surface_is_clean(self):
        self.assertEqual(
            _mod.scan_text("// TrustPager Thumbnail Studio tokens.",
                           vendor_surface=False), [],
            "off an owner-brand surface, naming the connected platform is fine")


class TestLiveRepoIsClean(unittest.TestCase):
    def test_tracked_files_pass_the_gate(self):
        self.assertEqual(_mod.scan(scan_all=False), 0,
                         "coined terms found outside the allowed provenance "
                         "locations — run: python tools/check-doctrine-voice.py")


if __name__ == "__main__":
    unittest.main()

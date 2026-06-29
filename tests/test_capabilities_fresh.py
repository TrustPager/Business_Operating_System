"""Drift guard: the committed docs/CAPABILITIES.md must be FRESH vs the registry.

docs/CAPABILITIES.md is the GTM-facing capability doc, GENERATED from
kernel/registry.json (plus each skill's SKILL.md name/description) by
tools/export-capabilities.py. The risk is silent drift: someone adds, removes,
or re-tiers a skill — so the registry changes — but forgets to re-export, and
the GTM doc the AI-BOS project cites no longer reflects what the plugin does.
This test is the unit-level guard against that: it rebuilds the doc in memory
from the committed registry + skills and asserts it is byte-for-byte identical
to the committed docs/CAPABILITIES.md.

If this test fails, the fix is NOT to edit this test — it is to run
``python tools/export-capabilities.py`` and commit the regenerated doc.

Offline-safe: no network, no key. Run:
    python -m unittest tests.test_capabilities_fresh
    python -m unittest discover -s tests
"""

import importlib.util
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# kebab-case filename can't be `import`ed directly — load by path, the same
# trick test_registry_fresh.py uses for the registry generator.
_GEN_PATH = REPO / "tools" / "export-capabilities.py"
_spec = importlib.util.spec_from_file_location("export_capabilities", _GEN_PATH)
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)  # type: ignore[union-attr]

_SKILLS_DIR = REPO / "skills"
_REGISTRY_PATH = REPO / "kernel" / "registry.json"
_CAPABILITIES_PATH = REPO / "docs" / "CAPABILITIES.md"

# Heavy render-studio apps (D13): must appear under the heavier-setup subgroup,
# not the cold-day-one "Works now (keyless)" block.
_HEAVY_RENDER_APPS = gen._HEAVY_RENDER_APPS

# The subgroup labels as they appear in the generated doc.
_COLD_WIN_LABEL = "**Works now (keyless)**"
_HEAVY_LABEL = "**Keyless, heavier setup (optional studios)**"


class TestCapabilitiesFresh(unittest.TestCase):
    def test_committed_capabilities_matches_fresh_export(self):
        """The committed CAPABILITIES.md equals a fresh build from the registry.

        Built the SAME way the writer builds it (build_capabilities over the
        committed registry + skills), compared byte-for-byte against the
        committed file's exact text.
        """
        registry = json.loads(_REGISTRY_PATH.read_text(encoding="utf-8"))
        fresh = gen.build_capabilities(registry, _SKILLS_DIR)
        committed = _CAPABILITIES_PATH.read_text(encoding="utf-8")
        self.assertEqual(
            fresh,
            committed,
            "docs/CAPABILITIES.md is STALE — it drifted from "
            "kernel/registry.json. Regenerate it: "
            "`python tools/export-capabilities.py` and commit the result. "
            "(Do not edit this test to make it pass.)",
        )

    def test_heavy_render_apps_not_in_cold_keyless_block(self):
        """Heavy render-studio apps must not appear in the cold "Works now (keyless)" block.

        D13: make-social-post and make-thumbnail (and any future entry in
        _HEAVY_RENDER_APPS) require the bundled browser/puppeteer render stack.
        They are keyless but NOT instant day-one wins, so they must appear in
        the "Keyless, heavier setup (optional studios)" subgroup rather than
        the cold-win block that a README reader would interpret as zero-setup.

        This test parses the committed CAPABILITIES.md line by line to find
        which bullet-point block each heavy app lands in, asserting it is never
        the cold-win block.
        """
        committed = _CAPABILITIES_PATH.read_text(encoding="utf-8")
        registry = json.loads(_REGISTRY_PATH.read_text(encoding="utf-8"))

        # Build a map of plain-name -> app_id for heavy apps so we can match
        # bullet lines in the doc regardless of display capitalisation.
        heavy_plain_names: dict[str, str] = {}
        for app_id in _HEAVY_RENDER_APPS:
            entry = registry.get(app_id, {})
            if entry.get("status") != "active":
                continue
            meta = gen._read_meta(_SKILLS_DIR / app_id / "SKILL.md", app_id)
            heavy_plain_names[gen._plain_name(app_id, meta).lower()] = app_id

        # Walk lines tracking the current subgroup label.
        current_subgroup: str = ""
        for line in committed.splitlines():
            stripped = line.strip()
            if stripped in (_COLD_WIN_LABEL, _HEAVY_LABEL, "**Switches on when you connect a tool**"):
                current_subgroup = stripped
                continue

            if not stripped.startswith("- **"):
                continue

            # Extract display name from "- **Name**: ..." bullet.
            name_part = stripped[4:]  # drop "- **"
            close = name_part.find("**")
            if close == -1:
                continue
            display_name = name_part[:close].lower()

            if display_name in heavy_plain_names:
                app_id = heavy_plain_names[display_name]
                self.assertNotEqual(
                    current_subgroup,
                    _COLD_WIN_LABEL,
                    f"{app_id} ({display_name!r}) appeared under "
                    f"{_COLD_WIN_LABEL!r} — heavy render-studio apps must be "
                    f"under {_HEAVY_LABEL!r} instead (D13). "
                    "Re-add it to _HEAVY_RENDER_APPS in export-capabilities.py.",
                )

    def test_heavy_render_apps_appear_in_heavier_setup_block(self):
        """Heavy render-studio apps must appear in the heavier-setup subgroup.

        The doc must contain the "Keyless, heavier setup (optional studios)"
        label, and every active heavy app must have a bullet under it.
        """
        committed = _CAPABILITIES_PATH.read_text(encoding="utf-8")
        registry = json.loads(_REGISTRY_PATH.read_text(encoding="utf-8"))

        # Collect active heavy apps.
        active_heavy: dict[str, str] = {}  # plain_name.lower() -> app_id
        for app_id in _HEAVY_RENDER_APPS:
            entry = registry.get(app_id, {})
            if entry.get("status") != "active":
                continue
            meta = gen._read_meta(_SKILLS_DIR / app_id / "SKILL.md", app_id)
            active_heavy[gen._plain_name(app_id, meta).lower()] = app_id

        if not active_heavy:
            self.skipTest("No active heavy render apps in the registry.")

        self.assertIn(
            _HEAVY_LABEL,
            committed,
            f"The subgroup label {_HEAVY_LABEL!r} is missing from "
            "docs/CAPABILITIES.md. Regenerate it after updating "
            "export-capabilities.py.",
        )

        # Collect names that appear under the heavier-setup subgroup.
        found_under_heavy: set[str] = set()
        current_subgroup: str = ""
        for line in committed.splitlines():
            stripped = line.strip()
            if stripped in (_COLD_WIN_LABEL, _HEAVY_LABEL, "**Switches on when you connect a tool**"):
                current_subgroup = stripped
                continue
            if not stripped.startswith("- **") or current_subgroup != _HEAVY_LABEL:
                continue
            name_part = stripped[4:]
            close = name_part.find("**")
            if close != -1:
                found_under_heavy.add(name_part[:close].lower())

        for plain_lower, app_id in active_heavy.items():
            self.assertIn(
                plain_lower,
                found_under_heavy,
                f"{app_id} is in _HEAVY_RENDER_APPS but did not appear under "
                f"{_HEAVY_LABEL!r} in docs/CAPABILITIES.md. Regenerate the doc.",
            )


if __name__ == "__main__":
    unittest.main()

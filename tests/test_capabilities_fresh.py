"""Drift guard: the committed docs/CAPABILITIES.md must be FRESH vs the registry.

docs/CAPABILITIES.md is the GTM-facing capability doc, GENERATED from
kernel/registry.json (plus each skill's SKILL.md name/description) by
tools/export-capabilities.py. The risk is silent drift: someone adds, removes,
or re-tiers a skill — so the registry changes — but forgets to re-export, and
the GTM doc the AI-BOS project cites no longer reflects what the plugin does.
This test is the unit-level guard against that: it rebuilds the doc in memory
from the committed registry + skills and asserts it is byte-for-byte identical
to the committed docs/CAPABILITIES.md.

If this test fails, the fix is NOT to edit this test — it's to run
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


if __name__ == "__main__":
    unittest.main()

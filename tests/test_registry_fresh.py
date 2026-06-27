"""Drift guard: the committed kernel/registry.json must be FRESH (P1 Task 6).

kernel/registry.json is GENERATED from the 58 skills' manifests by
tools/registry-generator.py. The risk is silent drift: someone edits a skill's
SKILL.md manifest but forgets to regenerate, so the committed registry no longer
reflects reality. This test is the unit-level guard against that — it regenerates
the registry from skills/ (in memory, serialized exactly as the writer serializes
it) and asserts it is byte-for-byte identical to the committed kernel/registry.json.

If this test fails, the fix is NOT to edit this test — it's to run
``python tools/registry-generator.py`` and commit the regenerated registry.

Offline-safe: no network, no key. Run:
    python -m unittest tests.test_registry_fresh
    python -m unittest discover -s tests
"""

import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# kebab-case filename can't be `import`ed directly — load by path, the same
# trick the rest of the suite uses for tools/.
_GEN_PATH = REPO / "tools" / "registry-generator.py"
_spec = importlib.util.spec_from_file_location("registry_generator", _GEN_PATH)
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)  # type: ignore[union-attr]

_SKILLS_DIR = REPO / "skills"
_REGISTRY_PATH = REPO / "kernel" / "registry.json"


class TestRegistryFresh(unittest.TestCase):
    def test_committed_registry_matches_fresh_generation(self):
        """The committed registry equals a fresh generate + serialize.

        Serialized the SAME way the writer serializes (serialize_registry),
        compared byte-for-byte against the committed file's exact text.
        """
        fresh = gen.serialize_registry(gen.generate_registry(_SKILLS_DIR))
        committed = _REGISTRY_PATH.read_text(encoding="utf-8")
        self.assertEqual(
            fresh,
            committed,
            "kernel/registry.json is STALE — it drifted from the skill "
            "manifests. Regenerate it: `python tools/registry-generator.py` "
            "and commit the result. (Do not edit this test to make it pass.)",
        )


if __name__ == "__main__":
    unittest.main()

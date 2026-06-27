"""Offline unit tests for tools/registry-generator.py (P1 Task 2).

The registry generator walks skills/*/SKILL.md, lifts each manifest with the
shared parser (tools/manifest.py — NOT a third parser), validates it, and emits
a deterministic kernel/registry.json keyed by skill folder name. A skill with
no manifest, or a malformed/invalid one, is SKIPPED with a stderr warning — it
must never crash the whole registry.

These tests build a throwaway skills/ tree in a temp dir and exercise:
  - the two valid manifests are included, sorted by skill name;
  - the no-manifest skill is skipped (absent, no exception);
  - a malformed/invalid manifest is skipped (absent, no exception);
  - output is byte-identical across two runs (determinism).

Offline-safe: no network, no key. Run:
    python -m unittest tests.test_registry_generator
    python -m unittest discover -s tests
"""

import importlib.util
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

REPO = Path(__file__).resolve().parent.parent
# kebab-case filename can't be `import`ed directly — load by path, the same
# trick the rest of the suite uses for tools/.
_GEN_PATH = REPO / "tools" / "registry-generator.py"
_spec = importlib.util.spec_from_file_location("registry_generator", _GEN_PATH)
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)  # type: ignore[union-attr]


# --- SKILL.md fixtures ---------------------------------------------------

FLOOR_SKILL = """\
---
name: Write Prompt
description: Turn a rough ask into a complete prompt.
triggers:
  - write a prompt
  - sharpen this prompt
function_slot: floor
requires_driver: none
requires_credential: none
data_path: reasoning_only
---

# Write Prompt

Body text that is not part of the manifest.
"""

MCP_SKILL = """\
---
name: Sweep My Day
description: Morning briefing across the workspace.
triggers:
  - sweep my day
  - morning briefing
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__list_tasks
  - mcp__trustpager__list_opportunities
unlocks:
  - daily-roundup
status: active
---

# Sweep My Day

Body text.
"""

NO_MANIFEST_SKILL = """\
---
name: Just A Skill
description: Has frontmatter but no manifest keys.
triggers:
  - do the thing
---

# Just A Skill

This skill predates the manifest contract — no manifest keys at all.
"""

MALFORMED_SKILL = """\
---
name: Broken Skill
description: Declares manifest keys but with a bad enum + missing key.
triggers:
  - break it
function_slot: not_a_real_slot
requires_driver: trustpager
requires_credential: mcp
---

# Broken Skill

Invalid: function_slot is not in the enum and data_path is missing.
"""


def _write_skill(skills_dir: Path, name: str, body: str) -> None:
    """Create skills/<name>/SKILL.md with the given content."""
    folder = skills_dir / name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "SKILL.md").write_text(body, encoding="utf-8")


class TestGenerateRegistry(unittest.TestCase):
    def _build_tree(self, skills_dir: Path) -> None:
        # Intentionally create folders out of alphabetical order so we can
        # prove the generator sorts.
        _write_skill(skills_dir, "sweep-my-day", MCP_SKILL)
        _write_skill(skills_dir, "write-prompt", FLOOR_SKILL)
        _write_skill(skills_dir, "legacy-skill", NO_MANIFEST_SKILL)

    def test_valid_manifests_included_and_sorted(self):
        with TemporaryDirectory() as tmp:
            skills_dir = Path(tmp) / "skills"
            self._build_tree(skills_dir)
            reg = gen.generate_registry(skills_dir)

            # Both valid skills present; keyed by folder name.
            self.assertIn("sweep-my-day", reg)
            self.assertIn("write-prompt", reg)
            # Sorted by skill name (insertion order is the sort order).
            self.assertEqual(
                list(reg.keys()),
                sorted(["sweep-my-day", "write-prompt"]),
            )

    def test_no_manifest_skill_is_skipped(self):
        with TemporaryDirectory() as tmp:
            skills_dir = Path(tmp) / "skills"
            self._build_tree(skills_dir)
            reg = gen.generate_registry(skills_dir)
            self.assertNotIn("legacy-skill", reg)
            self.assertEqual(len(reg), 2)

    def test_manifest_fields_carried_through(self):
        with TemporaryDirectory() as tmp:
            skills_dir = Path(tmp) / "skills"
            self._build_tree(skills_dir)
            reg = gen.generate_registry(skills_dir)

            floor = reg["write-prompt"]
            self.assertEqual(floor["function_slot"], "floor")
            self.assertEqual(floor["requires_driver"], "none")
            self.assertEqual(floor["requires_credential"], "none")
            self.assertEqual(floor["data_path"], "reasoning_only")
            # status defaults to "active" when not declared.
            self.assertEqual(floor["status"], "active")

            mcp = reg["sweep-my-day"]
            self.assertEqual(mcp["function_slot"], "crm")
            self.assertEqual(mcp["requires_driver"], "trustpager")
            self.assertEqual(mcp["requires_credential"], "mcp")
            self.assertEqual(mcp["data_path"], "mcp_tools")
            self.assertEqual(
                mcp["uses_tools"],
                ["mcp__trustpager__list_tasks", "mcp__trustpager__list_opportunities"],
            )
            self.assertEqual(mcp["unlocks"], ["daily-roundup"])
            self.assertEqual(mcp["status"], "active")
            # Passthrough frontmatter (name/description/triggers) is NOT
            # carried into the registry — only manifest fields.
            self.assertNotIn("name", mcp)
            self.assertNotIn("description", mcp)
            self.assertNotIn("triggers", mcp)

    def test_malformed_manifest_is_skipped_not_raised(self):
        with TemporaryDirectory() as tmp:
            skills_dir = Path(tmp) / "skills"
            _write_skill(skills_dir, "write-prompt", FLOOR_SKILL)
            _write_skill(skills_dir, "broken-skill", MALFORMED_SKILL)
            # Must not raise even though one manifest is invalid.
            reg = gen.generate_registry(skills_dir)
            self.assertIn("write-prompt", reg)
            self.assertNotIn("broken-skill", reg)
            self.assertEqual(len(reg), 1)

    def test_empty_skills_dir_yields_empty_registry(self):
        with TemporaryDirectory() as tmp:
            skills_dir = Path(tmp) / "skills"
            skills_dir.mkdir(parents=True)
            self.assertEqual(gen.generate_registry(skills_dir), {})

    def test_missing_skills_dir_yields_empty_registry(self):
        with TemporaryDirectory() as tmp:
            skills_dir = Path(tmp) / "does-not-exist"
            # Robustness: a missing dir is empty, not a crash.
            self.assertEqual(gen.generate_registry(skills_dir), {})


class TestDeterminism(unittest.TestCase):
    def test_two_runs_produce_identical_json(self):
        with TemporaryDirectory() as tmp:
            skills_dir = Path(tmp) / "skills"
            _write_skill(skills_dir, "sweep-my-day", MCP_SKILL)
            _write_skill(skills_dir, "write-prompt", FLOOR_SKILL)
            _write_skill(skills_dir, "legacy-skill", NO_MANIFEST_SKILL)

            first = gen.serialize_registry(gen.generate_registry(skills_dir))
            second = gen.serialize_registry(gen.generate_registry(skills_dir))
            self.assertEqual(first, second)
            # Deterministic contract: indent=2, sort_keys, trailing newline.
            self.assertTrue(first.endswith("\n"))
            self.assertEqual(json.loads(first), json.loads(second))
            # sort_keys means top-level keys are alphabetical in the text.
            self.assertLess(
                first.index("sweep-my-day"), first.index("write-prompt")
            )


if __name__ == "__main__":
    unittest.main()

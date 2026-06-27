"""Tests for tools/manifest.py — manifest schema parser + validator (P1 Task 1).

The manifest is the data-driven capability contract carried in each skill's
SKILL.md frontmatter. parse_frontmatter() lifts the YAML-ish block into a dict;
validate_manifest() returns a list of human-readable errors (empty == valid).

Offline-safe: no network, no key. Run:
    python -m unittest tests.test_manifest
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
from manifest import parse_frontmatter, validate_manifest  # noqa: E402


def _floor_manifest() -> dict:
    """A minimal valid 'floor' manifest (reasoning-only, no driver/credential)."""
    return {
        "name": "Write Prompt",
        "description": "Turn a rough ask into a complete prompt.",
        "triggers": ["write a prompt", "sharpen this prompt", "make it explicit"],
        "function_slot": "floor",
        "requires_driver": "none",
        "requires_credential": "none",
        "data_path": "reasoning_only",
    }


class TestValidateManifest(unittest.TestCase):
    def test_valid_floor_manifest_has_no_errors(self):
        self.assertEqual(validate_manifest(_floor_manifest()), [])

    def test_valid_mcp_manifest_has_no_errors(self):
        meta = {
            "name": "Sweep My Day",
            "description": "Morning briefing.",
            "triggers": ["sweep my day", "morning briefing", "what's hot"],
            "function_slot": "crm",
            "requires_driver": "trustpager",
            "requires_credential": "mcp",
            "data_path": "mcp_tools",
            "uses_tools": ["mcp__trustpager__list_tasks"],
            "status": "active",
        }
        self.assertEqual(validate_manifest(meta), [])

    def test_missing_required_key_is_an_error(self):
        meta = _floor_manifest()
        del meta["data_path"]
        errors = validate_manifest(meta)
        self.assertTrue(errors)
        self.assertTrue(any("data_path" in e for e in errors))

    def test_bad_enum_value_is_an_error(self):
        meta = _floor_manifest()
        meta["data_path"] = "nope"
        errors = validate_manifest(meta)
        self.assertTrue(errors)
        self.assertTrue(any("data_path" in e and "nope" in e for e in errors))

    def test_data_path_local_validates(self):
        # 'local' is a valid data_path: skill reads local files the operator
        # provides (e.g. MarkItDown over a dropped-in PDF). Keyless driver,
        # no credential.
        meta = _floor_manifest()
        meta["requires_driver"] = "markitdown"
        meta["data_path"] = "local"
        self.assertEqual(validate_manifest(meta), [])

    def test_bogus_data_path_still_fails(self):
        meta = _floor_manifest()
        meta["data_path"] = "bogus"
        errors = validate_manifest(meta)
        self.assertTrue(errors)
        self.assertTrue(any("data_path" in e and "bogus" in e for e in errors))

    def test_unknown_key_is_an_error(self):
        meta = _floor_manifest()
        meta["wibble"] = "anything"
        errors = validate_manifest(meta)
        self.assertTrue(errors)
        self.assertTrue(any("wibble" in e for e in errors))

    def test_passthrough_keys_are_not_unknown(self):
        # name / description / triggers are legitimate non-manifest frontmatter.
        meta = _floor_manifest()
        self.assertIn("name", meta)
        self.assertIn("description", meta)
        self.assertIn("triggers", meta)
        self.assertEqual(validate_manifest(meta), [])

    def test_list_field_given_a_scalar_is_an_error(self):
        meta = _floor_manifest()
        meta["uses_tools"] = "mcp__trustpager__list_tasks"  # should be a list
        errors = validate_manifest(meta)
        self.assertTrue(errors)
        self.assertTrue(any("uses_tools" in e for e in errors))

    def test_status_defaults_when_absent(self):
        # status is optional; absence must NOT be an error.
        meta = _floor_manifest()
        self.assertNotIn("status", meta)
        self.assertEqual(validate_manifest(meta), [])

    def test_bad_status_enum_is_an_error(self):
        meta = _floor_manifest()
        meta["status"] = "retired"  # not in {active, deprecated, removed}
        errors = validate_manifest(meta)
        self.assertTrue(any("status" in e for e in errors))

    def test_optional_list_fields_accept_lists(self):
        meta = _floor_manifest()
        meta["unlocks"] = ["something"]
        meta["reads_for_profile"] = ["business name"]
        self.assertEqual(validate_manifest(meta), [])


class TestParseFrontmatter(unittest.TestCase):
    def test_parses_scalars_and_lists(self):
        text = (
            "---\n"
            "name: Demo\n"
            "function_slot: floor\n"
            "triggers:\n"
            "  - one\n"
            "  - two\n"
            "---\n\n"
            "# Body\n"
        )
        meta = parse_frontmatter(text)
        self.assertEqual(meta["name"], "Demo")
        self.assertEqual(meta["function_slot"], "floor")
        self.assertEqual(meta["triggers"], ["one", "two"])

    def test_no_frontmatter_returns_empty_dict(self):
        self.assertEqual(parse_frontmatter("# just a heading\n"), {})


class TestExemplarsValidate(unittest.TestCase):
    def _check(self, skill_name: str) -> None:
        path = REPO / "skills" / skill_name / "SKILL.md"
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        errors = validate_manifest(meta)
        self.assertEqual(errors, [], f"{skill_name} manifest invalid: {errors}")

    def test_write_prompt_exemplar_validates_clean(self):
        self._check("write-prompt")

    def test_sweep_my_day_exemplar_validates_clean(self):
        self._check("sweep-my-day")


if __name__ == "__main__":
    unittest.main()

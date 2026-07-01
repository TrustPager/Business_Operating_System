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

    def test_keyless_skill_listing_foreign_mcp_tool_is_an_error(self):
        # Rule 4b: a keyless skill (requires_credential: none) that lists an
        # mcp__ tool it could only reach through a connection is a contradiction.
        # This is the leak guard (e.g. quote-from-photo reaching into TrustPager).
        meta = _floor_manifest()
        meta["uses_tools"] = ["mcp__trustpager__list_products"]
        errors = validate_manifest(meta)
        self.assertTrue(errors)
        self.assertTrue(any("mcp__trustpager__list_products" in e for e in errors))

    def test_keyless_firecrawl_skill_may_list_its_own_driver_tools(self):
        # A keyless HOSTED driver (firecrawl) is credential-free but IS an MCP.
        # A firecrawl app may honestly declare its own driver's tools without
        # tripping rule 4b — mirrors lint-skill.py's _driver_owns_tool exception.
        meta = _floor_manifest()
        meta["function_slot"] = "research"
        meta["requires_driver"] = "firecrawl"
        meta["data_path"] = "fetch_rest"
        meta["uses_tools"] = ["mcp__firecrawl__firecrawl_scrape"]
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


class TestParseFrontmatterHardened(unittest.TestCase):
    """Round-trip coverage for the single hardened parser (P1 Task 5).

    Each case is one shape the flat frontmatter contract must handle:
    scalar, quoted-with-special-chars, a list, an empty list, an empty
    value (distinguishable from absent), and a nested/over-indented value
    (now rejected with an error rather than silently dropped).
    """

    def _fm(self, body: str) -> str:
        return "---\n" + body + "---\n\n# Body\n"

    # --- scalar ---------------------------------------------------------
    def test_plain_scalar(self):
        meta = parse_frontmatter(self._fm("function_slot: floor\n"))
        self.assertEqual(meta["function_slot"], "floor")

    # --- quoted scalar with special chars (incl. a colon) ---------------
    def test_quoted_scalar_with_colon_keeps_inner_colon(self):
        # A double-quoted value containing a ': ' must survive intact; the
        # surrounding quotes are stripped, the inner colon is preserved.
        meta = parse_frontmatter(self._fm('description: "Stage: intake, then review"\n'))
        self.assertEqual(meta["description"], "Stage: intake, then review")

    def test_single_quoted_scalar_strips_quotes(self):
        meta = parse_frontmatter(self._fm("name: 'Sweep My Day'\n"))
        self.assertEqual(meta["name"], "Sweep My Day")

    def test_unquoted_value_with_colon_is_preserved(self):
        # Real descriptions carry prose; an unquoted value containing a colon
        # must keep everything after the FIRST 'key:' delimiter.
        meta = parse_frontmatter(self._fm("description: Does X: then Y.\n"))
        self.assertEqual(meta["description"], "Does X: then Y.")

    # --- list -----------------------------------------------------------
    def test_dash_list(self):
        meta = parse_frontmatter(self._fm("triggers:\n  - one\n  - two\n  - three\n"))
        self.assertEqual(meta["triggers"], ["one", "two", "three"])

    # --- empty list -----------------------------------------------------
    def test_empty_inline_list(self):
        # `key: []` is an explicit empty list, distinct from a missing key.
        meta = parse_frontmatter(self._fm("uses_tools: []\n"))
        self.assertIn("uses_tools", meta)
        self.assertEqual(meta["uses_tools"], [])

    # --- empty value: present-but-empty, distinct from absent -----------
    def test_empty_value_is_present_not_absent(self):
        # A value-less line with nothing following must be representable as an
        # empty value (empty string), so validate_manifest can say "empty"
        # rather than "missing".
        meta = parse_frontmatter(self._fm("function_slot:\nrequires_driver: none\n"))
        self.assertIn("function_slot", meta)          # present...
        self.assertEqual(meta["function_slot"], "")   # ...but empty

    def test_empty_value_still_fails_validation_via_enum(self):
        meta = parse_frontmatter(self._fm(
            "function_slot:\n"
            "requires_driver: none\n"
            "requires_credential: none\n"
            "data_path: reasoning_only\n"
        ))
        errors = validate_manifest(meta)
        # function_slot is present-but-empty -> enum rejects '' (NOT "missing").
        self.assertTrue(any("function_slot" in e for e in errors))
        self.assertFalse(any("missing required key: function_slot" in e for e in errors))

    def test_absent_value_reports_missing_not_empty(self):
        # Contrast: a genuinely absent required key reports "missing".
        meta = parse_frontmatter(self._fm(
            "requires_driver: none\n"
            "requires_credential: none\n"
            "data_path: reasoning_only\n"
        ))
        errors = validate_manifest(meta)
        self.assertTrue(any("missing required key: function_slot" in e for e in errors))

    # --- nested / over-indented value: rejected, not silently dropped ---
    def test_over_indented_list_item_raises(self):
        # A 4-space-indented list item used to be silently dropped (false pass).
        with self.assertRaises(ValueError):
            parse_frontmatter(self._fm("triggers:\n    - one\n"))

    def test_nested_mapping_raises(self):
        # An indented `key: value` (a nested map) is not part of the flat
        # contract and must surface an error, not vanish.
        with self.assertRaises(ValueError):
            parse_frontmatter(self._fm("function_slot: crm\n  nested: oops\n"))

    def test_dash_item_without_open_list_raises(self):
        # A list item with no preceding `key:` opener is structurally broken.
        with self.assertRaises(ValueError):
            parse_frontmatter(self._fm("  - orphan\n"))

    def test_blank_line_splitting_a_list_raises(self):
        # A blank line closes the open list; a list item after it is now an
        # orphan and raises (the old parser silently dropped the tail items).
        with self.assertRaises(ValueError):
            parse_frontmatter(self._fm("triggers:\n  - one\n\n  - two\n"))

    # --- regression: existing clean shapes still parse ------------------
    def test_mixed_scalars_then_list_then_scalar(self):
        meta = parse_frontmatter(self._fm(
            "name: Demo\n"
            "triggers:\n"
            "  - a\n"
            "  - b\n"
            "status: active\n"
        ))
        self.assertEqual(meta["name"], "Demo")
        self.assertEqual(meta["triggers"], ["a", "b"])
        self.assertEqual(meta["status"], "active")


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

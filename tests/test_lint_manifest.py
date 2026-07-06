"""Tests for tools/lint-skill.py manifest-contract enforcement (P1 Task 3).

Task 3 hardens the linter with three enforcement upgrades:
  (a) Manifest validation -> FAIL  — invalid manifest (per validate_manifest) fails lint.
  (b) resolve_path WARN -> FAIL    — fetch.py calling api_get() without resolve_path() fails.
  (c) Undeclared mcp__ tool        — an mcp__ tool referenced in the SKILL.md body that is
                                      neither in uses_tools nor belongs to the skill's
                                      requires_driver is a violation (FAIL).

These tests build synthetic skills in temp dirs so the negative cases never depend on
real skills. Offline-safe: no network, no key.

    python -m unittest tests.test_lint_manifest
"""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

# lint-skill.py has a hyphen, so import it by file path.
_spec = importlib.util.spec_from_file_location("lint_skill", REPO / "tools" / "lint-skill.py")
lint_skill = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lint_skill)


# --- Fixtures -------------------------------------------------------------

_VALID_FLOOR_FM = """\
name: Synth Floor
description: A synthetic reasoning-only skill for tests.
triggers:
  - do the synthetic thing
  - run synth
  - synth floor please
function_slot: floor
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
"""

_VALID_MCP_FM = """\
name: Synth Crm
description: A synthetic mcp-backed skill for tests.
triggers:
  - synth crm
  - run the crm synth
  - do crm synth thing
function_slot: crm
requires_driver: trustpager
requires_credential: mcp
data_path: mcp_tools
uses_tools:
  - mcp__trustpager__list_tasks
status: active
"""


def _write_skill(root: Path, frontmatter: str, body: str = "\n# Synth\n\nBody.\n",
                 fetch_py: str | None = None) -> Path:
    d = root / "synth-skill"
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"---\n{frontmatter}---\n{body}", encoding="utf-8")
    if fetch_py is not None:
        (d / "fetch.py").write_text(fetch_py, encoding="utf-8")
    return d


def _severities(issues):
    return [sev for sev, _ in issues]


class TestCleanSkillPasses(unittest.TestCase):
    def test_clean_floor_skill_has_no_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_skill(Path(tmp), _VALID_FLOOR_FM)
            issues = lint_skill.lint_skill(d)
            self.assertNotIn("FAIL", _severities(issues),
                             f"clean floor skill should not FAIL: {issues}")

    def test_clean_mcp_skill_referencing_declared_tool_passes(self):
        body = "\n# Synth\n\nUse `mcp__trustpager__list_tasks` to read tasks.\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_skill(Path(tmp), _VALID_MCP_FM, body=body)
            issues = lint_skill.lint_skill(d)
            self.assertNotIn("FAIL", _severities(issues),
                             f"declared tool reference should pass: {issues}")


class TestManifestValidationFails(unittest.TestCase):
    """(a) invalid manifest -> FAIL."""

    def test_invalid_enum_value_fails(self):
        fm = _VALID_FLOOR_FM.replace("data_path: reasoning_only", "data_path: nope")
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_skill(Path(tmp), fm)
            issues = lint_skill.lint_skill(d)
            self.assertIn("FAIL", _severities(issues))
            self.assertTrue(any("data_path" in m for _, m in issues), issues)

    def test_missing_required_manifest_key_fails(self):
        fm = _VALID_FLOOR_FM.replace("function_slot: floor\n", "")
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_skill(Path(tmp), fm)
            issues = lint_skill.lint_skill(d)
            self.assertIn("FAIL", _severities(issues))
            self.assertTrue(any("function_slot" in m for _, m in issues), issues)

    def test_unknown_manifest_key_fails(self):
        fm = _VALID_FLOOR_FM + "bogus_key: whatever\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_skill(Path(tmp), fm)
            issues = lint_skill.lint_skill(d)
            self.assertIn("FAIL", _severities(issues))


class TestResolvePathFails(unittest.TestCase):
    """(b) fetch.py api_get() without resolve_path() -> FAIL (was WARN)."""

    def test_api_get_without_resolve_path_fails(self):
        fetch = (
            "from trustpager_api import api_get\n"
            "def fetch():\n"
            "    return api_get('/rest/v1/opportunities')\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_skill(Path(tmp), _VALID_MCP_FM, fetch_py=fetch)
            issues = lint_skill.lint_skill(d)
            self.assertIn("FAIL", _severities(issues))
            self.assertTrue(any("resolve_path" in m for _, m in issues), issues)

    def test_api_get_with_resolve_path_passes(self):
        fetch = (
            "from trustpager_api import api_get, resolve_path\n"
            "def fetch():\n"
            "    return api_get(resolve_path('opportunities'))\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_skill(Path(tmp), _VALID_MCP_FM, fetch_py=fetch)
            issues = lint_skill.lint_skill(d)
            self.assertNotIn("FAIL", _severities(issues), issues)


class TestUndeclaredToolCheck(unittest.TestCase):
    """(c) mcp__ tool in body not in uses_tools and not the skill's driver -> FAIL."""

    def test_undeclared_non_driver_tool_in_body_fails(self):
        # Floor skill (driver=none) mentioning a trustpager tool it never declares.
        body = "\n# Synth\n\nThis quietly calls `mcp__trustpager__list_products`.\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_skill(Path(tmp), _VALID_FLOOR_FM, body=body)
            issues = lint_skill.lint_skill(d)
            self.assertIn("FAIL", _severities(issues),
                          f"undeclared non-driver tool should FAIL: {issues}")
            self.assertTrue(any("mcp__trustpager__list_products" in m for _, m in issues), issues)

    def test_driver_owned_tool_in_body_is_exempt(self):
        # mcp-backed trustpager skill may reference any mcp__*trustpager* tool freely.
        body = "\n# Synth\n\nCalls `mcp__trustpager__create_opportunity` and "
        body += "`mcp__trustpager__send_email` without declaring each.\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_skill(Path(tmp), _VALID_MCP_FM, body=body)
            issues = lint_skill.lint_skill(d)
            self.assertNotIn("FAIL", _severities(issues),
                             f"driver-owned tools should be exempt: {issues}")

    def test_declared_tool_in_body_passes(self):
        body = "\n# Synth\n\nUses declared `mcp__trustpager__list_tasks`.\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_skill(Path(tmp), _VALID_MCP_FM, body=body)
            issues = lint_skill.lint_skill(d)
            self.assertNotIn("FAIL", _severities(issues), issues)


class TestCustomerFacingCopyKeyAllowed(unittest.TestCase):
    """produces_customer_facing_copy is an accepted passthrough key (content-doctrine layer)."""

    def test_produces_customer_facing_copy_is_a_known_key(self):
        fm = _VALID_FLOOR_FM + "produces_customer_facing_copy: true\n"
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_skill(Path(tmp), fm)
            issues = lint_skill.lint_skill(d)
            self.assertFalse(
                any("unknown key" in m for _, m in issues),
                f"produces_customer_facing_copy must be an accepted key: {issues}",
            )


if __name__ == "__main__":
    unittest.main()

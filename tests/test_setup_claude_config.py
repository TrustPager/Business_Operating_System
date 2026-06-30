"""Tests for tools/setup_claude_config.py.

Covers:
  merge-settings:
    - creates settings.json when absent
    - merges additively into existing file (user entries kept, new ones added,
      de-duped, other keys preserved)
    - idempotent (run twice -> no duplicate entries)
    - refuses (non-zero, no overwrite) when settings.json is invalid JSON

  merge-claude-md:
    - creates CLAUDE.md when absent
    - appends block to existing CLAUDE.md with no markers
    - idempotent (run twice -> replaces block, surrounding content byte-identical)
    - refuses when start marker present but no matching end marker

  allowlist:
    - setup_claude_config is in tools/run.py's _ALLOWED_TOOLS

All tests use a temp home so they never touch the real ~/.claude directory.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


# ---------------------------------------------------------------------------
# Load the module under test
# ---------------------------------------------------------------------------

def _load_module(name: str, rel_path: str):
    repo_root = Path(__file__).resolve().parent.parent
    path = repo_root / rel_path
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_MOD = _load_module("setup_claude_config", "tools/setup_claude_config.py")


def _run(args: list[str], tmp_home: Path) -> int:
    """Call the module's main() with a --home pointing at tmp_home."""
    return _MOD.main(["--home", str(tmp_home), *args])


# ---------------------------------------------------------------------------
# Helper: build a minimal source settings file in a temp dir
# ---------------------------------------------------------------------------

def _make_source_settings(tmp: Path, allow: list[str] | None = None,
                           deny: list[str] | None = None) -> Path:
    data: dict = {"permissions": {}}
    if allow is not None:
        data["permissions"]["allow"] = allow
    if deny is not None:
        data["permissions"]["deny"] = deny
    p = tmp / "source-settings.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def _make_source_md(tmp: Path, content: str = "# BOS best practices\n") -> Path:
    p = tmp / "source.md"
    p.write_text(content, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# merge-settings tests
# ---------------------------------------------------------------------------

class TestMergeSettingsCreate(unittest.TestCase):
    """merge-settings creates settings.json when it does not exist."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.claude_dir = self.home / ".claude"
        self.settings_path = self.claude_dir / "settings.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_creates_settings_json(self):
        src = _make_source_settings(self.tmp, allow=["Read", "Glob"], deny=["WebSearch"])
        rc = _run(["merge-settings", "--from", str(src)], self.home)
        self.assertEqual(rc, 0)
        self.assertTrue(self.settings_path.exists(), "settings.json must be created")

    def test_allow_entries_written(self):
        src = _make_source_settings(self.tmp, allow=["Read", "Glob"])
        _run(["merge-settings", "--from", str(src)], self.home)
        data = json.loads(self.settings_path.read_text(encoding="utf-8"))
        perms = data.get("permissions", {})
        self.assertIn("Read", perms.get("allow", []))
        self.assertIn("Glob", perms.get("allow", []))

    def test_deny_entries_written(self):
        src = _make_source_settings(self.tmp, deny=["WebSearch"])
        _run(["merge-settings", "--from", str(src)], self.home)
        data = json.loads(self.settings_path.read_text(encoding="utf-8"))
        perms = data.get("permissions", {})
        self.assertIn("WebSearch", perms.get("deny", []))

    def test_output_is_valid_json(self):
        src = _make_source_settings(self.tmp, allow=["Read"])
        _run(["merge-settings", "--from", str(src)], self.home)
        text = self.settings_path.read_text(encoding="utf-8")
        try:
            json.loads(text)
        except json.JSONDecodeError as e:
            self.fail(f"settings.json is not valid JSON: {e}")


class TestMergeSettingsMerge(unittest.TestCase):
    """merge-settings merges additively into an existing settings.json."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.claude_dir = self.home / ".claude"
        self.claude_dir.mkdir()
        self.settings_path = self.claude_dir / "settings.json"

    def tearDown(self):
        self._tmp.cleanup()

    def _write_existing(self, data: dict):
        self.settings_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def test_user_allow_entries_kept(self):
        self._write_existing({
            "permissions": {"allow": ["UserTool"], "deny": []},
            "someOtherKey": "preserved",
        })
        src = _make_source_settings(self.tmp, allow=["Read"])
        _run(["merge-settings", "--from", str(src)], self.home)
        data = json.loads(self.settings_path.read_text(encoding="utf-8"))
        self.assertIn("UserTool", data["permissions"]["allow"])
        self.assertIn("Read", data["permissions"]["allow"])

    def test_new_allow_entries_added(self):
        self._write_existing({"permissions": {"allow": ["Existing"]}})
        src = _make_source_settings(self.tmp, allow=["NewEntry"])
        _run(["merge-settings", "--from", str(src)], self.home)
        data = json.loads(self.settings_path.read_text(encoding="utf-8"))
        self.assertIn("NewEntry", data["permissions"]["allow"])

    def test_other_top_level_keys_preserved(self):
        self._write_existing({
            "permissions": {"allow": []},
            "env": {"MY_VAR": "hello"},
            "model": "claude-opus",
        })
        src = _make_source_settings(self.tmp, allow=["Read"])
        _run(["merge-settings", "--from", str(src)], self.home)
        data = json.loads(self.settings_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("env", {}).get("MY_VAR"), "hello")
        self.assertEqual(data.get("model"), "claude-opus")

    def test_deny_entries_merged(self):
        self._write_existing({"permissions": {"allow": [], "deny": ["OldDeny"]}})
        src = _make_source_settings(self.tmp, deny=["NewDeny"])
        _run(["merge-settings", "--from", str(src)], self.home)
        data = json.loads(self.settings_path.read_text(encoding="utf-8"))
        deny = data["permissions"].get("deny", [])
        self.assertIn("OldDeny", deny)
        self.assertIn("NewDeny", deny)

    def test_no_duplicates_after_merge(self):
        self._write_existing({"permissions": {"allow": ["Read", "Glob"]}})
        src = _make_source_settings(self.tmp, allow=["Read", "NewTool"])
        _run(["merge-settings", "--from", str(src)], self.home)
        data = json.loads(self.settings_path.read_text(encoding="utf-8"))
        allow = data["permissions"].get("allow", [])
        self.assertEqual(allow.count("Read"), 1, "Read must appear exactly once")


class TestMergeSettingsIdempotent(unittest.TestCase):
    """Running merge-settings twice produces no duplicates."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.settings_path = self.home / ".claude" / "settings.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_idempotent_no_duplicate_allow(self):
        src = _make_source_settings(self.tmp, allow=["Read", "Glob"], deny=["WebSearch"])
        _run(["merge-settings", "--from", str(src)], self.home)
        _run(["merge-settings", "--from", str(src)], self.home)
        data = json.loads(self.settings_path.read_text(encoding="utf-8"))
        allow = data["permissions"].get("allow", [])
        self.assertEqual(len(allow), len(set(allow)), "No duplicate allow entries")

    def test_idempotent_no_duplicate_deny(self):
        src = _make_source_settings(self.tmp, allow=["Read"], deny=["WebSearch"])
        _run(["merge-settings", "--from", str(src)], self.home)
        _run(["merge-settings", "--from", str(src)], self.home)
        data = json.loads(self.settings_path.read_text(encoding="utf-8"))
        deny = data["permissions"].get("deny", [])
        self.assertEqual(len(deny), len(set(deny)), "No duplicate deny entries")


class TestMergeSettingsRefuse(unittest.TestCase):
    """merge-settings refuses (non-zero exit, no overwrite) on invalid JSON."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.claude_dir = self.home / ".claude"
        self.claude_dir.mkdir()
        self.settings_path = self.claude_dir / "settings.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_refuses_on_invalid_json(self):
        self.settings_path.write_text("{ this is not json }", encoding="utf-8")
        src = _make_source_settings(self.tmp, allow=["Read"])
        rc = _run(["merge-settings", "--from", str(src)], self.home)
        self.assertNotEqual(rc, 0, "Must exit non-zero on invalid settings.json")

    def test_does_not_overwrite_on_invalid_json(self):
        original_content = "{ this is not json }"
        self.settings_path.write_text(original_content, encoding="utf-8")
        src = _make_source_settings(self.tmp, allow=["Read"])
        _run(["merge-settings", "--from", str(src)], self.home)
        # File must remain untouched
        actual = self.settings_path.read_text(encoding="utf-8")
        self.assertEqual(actual, original_content,
                         "Invalid settings.json must not be overwritten")


# ---------------------------------------------------------------------------
# merge-claude-md tests
# ---------------------------------------------------------------------------

START = "<!-- bos:best-practices:start -->"
END = "<!-- bos:best-practices:end -->"


class TestMergeClaudeMdCreate(unittest.TestCase):
    """merge-claude-md creates CLAUDE.md when absent."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.claude_dir = self.home / ".claude"
        self.md_path = self.claude_dir / "CLAUDE.md"

    def tearDown(self):
        self._tmp.cleanup()

    def test_creates_claude_md(self):
        src = _make_source_md(self.tmp, "# BOS block content\n")
        rc = _run(["merge-claude-md", "--from", str(src)], self.home)
        self.assertEqual(rc, 0)
        self.assertTrue(self.md_path.exists(), "CLAUDE.md must be created")

    def test_created_file_contains_start_marker(self):
        src = _make_source_md(self.tmp, "# BOS block content\n")
        _run(["merge-claude-md", "--from", str(src)], self.home)
        text = self.md_path.read_text(encoding="utf-8")
        self.assertIn(START, text)

    def test_created_file_contains_end_marker(self):
        src = _make_source_md(self.tmp, "# BOS block content\n")
        _run(["merge-claude-md", "--from", str(src)], self.home)
        text = self.md_path.read_text(encoding="utf-8")
        self.assertIn(END, text)

    def test_created_file_contains_block_content(self):
        src = _make_source_md(self.tmp, "# BOS block content\n")
        _run(["merge-claude-md", "--from", str(src)], self.home)
        text = self.md_path.read_text(encoding="utf-8")
        self.assertIn("BOS block content", text)


class TestMergeClaudeMdAppend(unittest.TestCase):
    """merge-claude-md appends to existing CLAUDE.md with no markers."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.claude_dir = self.home / ".claude"
        self.claude_dir.mkdir()
        self.md_path = self.claude_dir / "CLAUDE.md"

    def tearDown(self):
        self._tmp.cleanup()

    def test_user_prose_intact_after_append(self):
        user_prose = "# My CLAUDE.md\n\nDo not remove this.\n"
        self.md_path.write_text(user_prose, encoding="utf-8")
        src = _make_source_md(self.tmp, "# BOS stuff\n")
        _run(["merge-claude-md", "--from", str(src)], self.home)
        text = self.md_path.read_text(encoding="utf-8")
        self.assertIn("Do not remove this.", text)

    def test_block_appended_after_user_prose(self):
        user_prose = "# My CLAUDE.md\n\nSome user content.\n"
        self.md_path.write_text(user_prose, encoding="utf-8")
        src = _make_source_md(self.tmp, "# BOS block\n")
        _run(["merge-claude-md", "--from", str(src)], self.home)
        text = self.md_path.read_text(encoding="utf-8")
        self.assertIn(START, text)
        self.assertIn("BOS block", text)
        # User prose must come before the appended block
        self.assertLess(text.index("Some user content."), text.index(START))

    def test_returns_zero(self):
        self.md_path.write_text("# Existing\n", encoding="utf-8")
        src = _make_source_md(self.tmp)
        rc = _run(["merge-claude-md", "--from", str(src)], self.home)
        self.assertEqual(rc, 0)


class TestMergeClaudeMdIdempotent(unittest.TestCase):
    """Running merge-claude-md twice replaces only the block; surrounding content stays."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.claude_dir = self.home / ".claude"
        self.claude_dir.mkdir()
        self.md_path = self.claude_dir / "CLAUDE.md"

    def tearDown(self):
        self._tmp.cleanup()

    def test_user_content_before_block_unchanged(self):
        user_prose = "# Header\n\nUser prose before.\n"
        self.md_path.write_text(user_prose, encoding="utf-8")
        src = _make_source_md(self.tmp, "# BOS v1\n")
        _run(["merge-claude-md", "--from", str(src)], self.home)
        _run(["merge-claude-md", "--from", str(src)], self.home)
        text = self.md_path.read_text(encoding="utf-8")
        self.assertIn("User prose before.", text)

    def test_user_content_after_block_unchanged(self):
        # Build a file with markers already in place + trailing user content
        existing = (
            "# Header\n\n"
            f"{START}\n# Old block\n{END}\n\n"
            "Trailing user note.\n"
        )
        self.md_path.write_text(existing, encoding="utf-8")
        src = _make_source_md(self.tmp, "# BOS v2\n")
        _run(["merge-claude-md", "--from", str(src)], self.home)
        text = self.md_path.read_text(encoding="utf-8")
        self.assertIn("Trailing user note.", text)

    def test_block_content_replaced_not_doubled(self):
        user_prose = "# Header\n"
        self.md_path.write_text(user_prose, encoding="utf-8")
        src = _make_source_md(self.tmp, "# BOS content\n")
        _run(["merge-claude-md", "--from", str(src)], self.home)
        _run(["merge-claude-md", "--from", str(src)], self.home)
        text = self.md_path.read_text(encoding="utf-8")
        # There should be exactly ONE start marker and ONE end marker
        self.assertEqual(text.count(START), 1, "Exactly one start marker")
        self.assertEqual(text.count(END), 1, "Exactly one end marker")

    def test_updated_block_content_written(self):
        user_prose = "# Header\n"
        self.md_path.write_text(user_prose, encoding="utf-8")
        src_v1 = _make_source_md(self.tmp / "v1.md" if False else self.tmp, "# BOS v1\n")
        # Use separate source files for v1 vs v2
        src_v1_path = self.tmp / "v1.md"
        src_v1_path.write_text("# BOS v1\n", encoding="utf-8")
        src_v2_path = self.tmp / "v2.md"
        src_v2_path.write_text("# BOS v2 updated\n", encoding="utf-8")

        _run(["merge-claude-md", "--from", str(src_v1_path)], self.home)
        _run(["merge-claude-md", "--from", str(src_v2_path)], self.home)
        text = self.md_path.read_text(encoding="utf-8")
        self.assertIn("BOS v2 updated", text)
        self.assertNotIn("BOS v1", text)


class TestMergeClaudeMdRefuse(unittest.TestCase):
    """merge-claude-md refuses on unbalanced markers."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.claude_dir = self.home / ".claude"
        self.claude_dir.mkdir()
        self.md_path = self.claude_dir / "CLAUDE.md"

    def tearDown(self):
        self._tmp.cleanup()

    def test_refuses_start_without_end(self):
        broken = f"# Header\n\n{START}\n# Dangling block, no end marker.\n"
        self.md_path.write_text(broken, encoding="utf-8")
        src = _make_source_md(self.tmp)
        rc = _run(["merge-claude-md", "--from", str(src)], self.home)
        self.assertNotEqual(rc, 0, "Must refuse when start has no matching end")

    def test_does_not_overwrite_on_unbalanced_markers(self):
        broken = f"# Header\n\n{START}\n# Dangling.\n"
        self.md_path.write_text(broken, encoding="utf-8")
        src = _make_source_md(self.tmp)
        _run(["merge-claude-md", "--from", str(src)], self.home)
        actual = self.md_path.read_text(encoding="utf-8")
        self.assertEqual(actual, broken, "File must be untouched on refusal")

    def test_refuses_end_without_start(self):
        broken = f"# Header\n\n# Some content\n{END}\n"
        self.md_path.write_text(broken, encoding="utf-8")
        src = _make_source_md(self.tmp)
        rc = _run(["merge-claude-md", "--from", str(src)], self.home)
        self.assertNotEqual(rc, 0, "Must refuse when end has no matching start")

    def test_refuses_multiple_start_markers(self):
        broken = f"{START}\nBlock1\n{END}\n{START}\nBlock2\n"
        self.md_path.write_text(broken, encoding="utf-8")
        src = _make_source_md(self.tmp)
        rc = _run(["merge-claude-md", "--from", str(src)], self.home)
        self.assertNotEqual(rc, 0, "Must refuse on multiple unbalanced starts")


# ---------------------------------------------------------------------------
# Allowlist test
# ---------------------------------------------------------------------------

class TestAllowlist(unittest.TestCase):
    """setup_claude_config must be in run.py's _ALLOWED_TOOLS."""

    def test_setup_claude_config_in_allowed_tools(self):
        run_mod = _load_module("run_module", "tools/run.py")
        self.assertIn(
            "setup_claude_config",
            run_mod._ALLOWED_TOOLS,
            "'setup_claude_config' must be in _ALLOWED_TOOLS in tools/run.py",
        )


if __name__ == "__main__":
    unittest.main()

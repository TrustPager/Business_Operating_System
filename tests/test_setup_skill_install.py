"""Tests for _install_skills() in tools/setup.py.

Covers:
  - Skills and commands are copied into <temphome>/.claude/ after a call.
  - Idempotent: calling twice does not error or duplicate entries.
  - Collision safety: a pre-existing non-BOS skill/command is NOT overwritten
    and a warning is printed.
  - bos.json records installed_skills and installed_commands.

All tests use a temp HOME so they never touch the real ~/.claude directory.
The fixture bos_home is a small temp tree with one skill dir and one command.
"""

from __future__ import annotations

import importlib
import importlib.util
import json
import sys
import types
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch
import tempfile


# ---------------------------------------------------------------------------
# Module loader (mirrors test_setup_keyskip.py pattern)
# ---------------------------------------------------------------------------

def _load_setup_module():
    """Load tools/setup.py without triggering the real trustpager_api import."""
    repo_root = Path(__file__).resolve().parent.parent
    setup_path = repo_root / "tools" / "setup.py"

    fake_tp = types.ModuleType("trustpager_api")
    # CONFIG_PATH will be overridden per test; this placeholder keeps the import
    # from crashing before we patch it.
    fake_tp.CONFIG_PATH = Path("/tmp/bos-test-placeholder.json")
    # Use setdefault so we don't clobber a real module if tests run together.
    sys.modules.setdefault("trustpager_api", fake_tp)

    tools_dir = str(repo_root / "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)

    spec = importlib.util.spec_from_file_location("setup_module_skill", setup_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_SETUP = _load_setup_module()


# ---------------------------------------------------------------------------
# Fixture builder
# ---------------------------------------------------------------------------

def _make_bos_home(tmp: Path) -> Path:
    """Create a minimal bos_home fixture with one skill and one command."""
    bos = tmp / "bos_home"
    skill_dir = bos / "skills" / "demo-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# demo-skill\n", encoding="utf-8")

    cmd_dir = bos / "commands"
    cmd_dir.mkdir(parents=True)
    (cmd_dir / "demo-cmd.md").write_text("# demo-cmd\n", encoding="utf-8")

    return bos


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestInstallSkillsBasic(unittest.TestCase):
    """Skills and commands land in the right places after _install_skills()."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.bos = _make_bos_home(self.tmp)
        self.claude_dir = self.tmp / ".claude"
        self.config_path = self.claude_dir / "bos.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_skill_md_is_copied(self):
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
        skill_md = self.claude_dir / "skills" / "demo-skill" / "SKILL.md"
        self.assertTrue(skill_md.exists(),
                        "SKILL.md must exist at ~/.claude/skills/demo-skill/SKILL.md")

    def test_command_md_is_copied(self):
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
        cmd_md = self.claude_dir / "commands" / "demo-cmd.md"
        self.assertTrue(cmd_md.exists(),
                        "demo-cmd.md must exist at ~/.claude/commands/demo-cmd.md")

    def test_skill_content_is_correct(self):
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
        skill_md = self.claude_dir / "skills" / "demo-skill" / "SKILL.md"
        self.assertIn("demo-skill", skill_md.read_text(encoding="utf-8"))

    def test_returns_correct_counts(self):
        with patch("sys.stdout", new_callable=StringIO):
            n_skills, n_cmds = _SETUP._install_skills(str(self.bos), self.config_path)
        self.assertEqual(n_skills, 1)
        self.assertEqual(n_cmds, 1)


class TestInstallSkillsBosJson(unittest.TestCase):
    """bos.json records installed_skills and installed_commands."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.bos = _make_bos_home(self.tmp)
        self.claude_dir = self.tmp / ".claude"
        self.config_path = self.claude_dir / "bos.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_installed_skills_recorded(self):
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
        cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.assertIn("demo-skill", cfg.get("installed_skills", []))

    def test_installed_commands_recorded(self):
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
        cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.assertIn("demo-cmd", cfg.get("installed_commands", []))

    def test_existing_bos_json_keys_preserved(self):
        """Other bos.json keys (bos_home, api_key) must not be clobbered."""
        self.claude_dir.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(
            json.dumps({"bos_home": "/some/path", "api_key": "preserved"}),
            encoding="utf-8",
        )
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
        cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.assertEqual(cfg.get("bos_home"), "/some/path")
        self.assertEqual(cfg.get("api_key"), "preserved")


class TestInstallSkillsIdempotent(unittest.TestCase):
    """Running _install_skills() twice must not error or duplicate list entries."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.bos = _make_bos_home(self.tmp)
        self.claude_dir = self.tmp / ".claude"
        self.config_path = self.claude_dir / "bos.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_second_run_does_not_raise(self):
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
        try:
            with patch("sys.stdout", new_callable=StringIO):
                _SETUP._install_skills(str(self.bos), self.config_path)
        except Exception as exc:
            self.fail(f"Second call raised: {exc}")

    def test_second_run_no_duplicate_skills_in_bos_json(self):
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
            _SETUP._install_skills(str(self.bos), self.config_path)
        cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
        installed = cfg.get("installed_skills", [])
        self.assertEqual(len(installed), len(set(installed)),
                         "installed_skills must not contain duplicates")

    def test_second_run_no_duplicate_commands_in_bos_json(self):
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
            _SETUP._install_skills(str(self.bos), self.config_path)
        cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
        installed = cfg.get("installed_commands", [])
        self.assertEqual(len(installed), len(set(installed)),
                         "installed_commands must not contain duplicates")

    def test_second_run_file_still_exists_and_readable(self):
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
            _SETUP._install_skills(str(self.bos), self.config_path)
        skill_md = self.claude_dir / "skills" / "demo-skill" / "SKILL.md"
        self.assertTrue(skill_md.exists())
        self.assertIn("demo-skill", skill_md.read_text(encoding="utf-8"))


class TestInstallSkillsCollision(unittest.TestCase):
    """Pre-existing non-BOS skills/commands must NOT be overwritten."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.bos = _make_bos_home(self.tmp)
        self.claude_dir = self.tmp / ".claude"
        self.config_path = self.claude_dir / "bos.json"

    def tearDown(self):
        self._tmp.cleanup()

    def _pre_create_user_skill(self) -> Path:
        """Put a user-authored SKILL.md in demo-skill BEFORE BOS runs."""
        skill_dir = self.claude_dir / "skills" / "demo-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("# USER VERSION\n", encoding="utf-8")
        # bos.json does NOT list demo-skill as BOS-owned (simulates a user file).
        self.claude_dir.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(
            json.dumps({"installed_skills": [], "installed_commands": []}),
            encoding="utf-8",
        )
        return skill_md

    def _pre_create_user_command(self) -> Path:
        """Put a user-authored demo-cmd.md BEFORE BOS runs."""
        cmd_dir = self.claude_dir / "commands"
        cmd_dir.mkdir(parents=True, exist_ok=True)
        cmd_file = cmd_dir / "demo-cmd.md"
        cmd_file.write_text("# USER COMMAND\n", encoding="utf-8")
        self.claude_dir.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(
            json.dumps({"installed_skills": [], "installed_commands": []}),
            encoding="utf-8",
        )
        return cmd_file

    def test_user_skill_not_overwritten(self):
        skill_md = self._pre_create_user_skill()
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("USER VERSION", content,
                      "User's SKILL.md must not be overwritten by BOS")

    def test_user_skill_collision_prints_warning(self):
        self._pre_create_user_skill()
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            _SETUP._install_skills(str(self.bos), self.config_path)
        output = mock_out.getvalue()
        self.assertIn("skip", output.lower(),
                      "A collision warning must be printed for the skipped skill")
        self.assertIn("demo-skill", output,
                      "Warning must name the colliding skill")

    def test_user_skill_not_added_to_installed_list(self):
        self._pre_create_user_skill()
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
        cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.assertNotIn("demo-skill", cfg.get("installed_skills", []),
                         "A skipped (collision) skill must not appear in installed_skills")

    def test_user_command_not_overwritten(self):
        cmd_file = self._pre_create_user_command()
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)
        content = cmd_file.read_text(encoding="utf-8")
        self.assertIn("USER COMMAND", content,
                      "User's command file must not be overwritten by BOS")

    def test_user_command_collision_prints_warning(self):
        self._pre_create_user_command()
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            _SETUP._install_skills(str(self.bos), self.config_path)
        output = mock_out.getvalue()
        self.assertIn("skip", output.lower(),
                      "A collision warning must be printed for the skipped command")
        self.assertIn("demo-cmd", output,
                      "Warning must name the colliding command")

    def test_bos_owned_skill_is_refreshed(self):
        """If BOS owns the skill, it must be refreshed (overwritten) on re-run."""
        # First install: BOS places it and records ownership.
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)

        # Tamper with the installed file to simulate stale copy.
        skill_md = self.claude_dir / "skills" / "demo-skill" / "SKILL.md"
        skill_md.write_text("# STALE\n", encoding="utf-8")

        # Second run: BOS should overwrite because it owns the name.
        with patch("sys.stdout", new_callable=StringIO):
            _SETUP._install_skills(str(self.bos), self.config_path)

        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("demo-skill", content,
                      "BOS-owned stale copy should be refreshed with repo content")
        self.assertNotIn("STALE", content,
                         "Stale content must be replaced on refresh")


class TestInstallSkillsNoSourceDirs(unittest.TestCase):
    """If the repo has no skills/ or commands/ dir, the function runs without error."""

    def test_empty_bos_home_no_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            bos = Path(tmp) / "bos_home"
            bos.mkdir()
            claude_dir = Path(tmp) / ".claude"
            config_path = claude_dir / "bos.json"
            with patch("sys.stdout", new_callable=StringIO):
                try:
                    n_skills, n_cmds = _SETUP._install_skills(str(bos), config_path)
                except Exception as exc:
                    self.fail(f"Empty bos_home raised: {exc}")
            self.assertEqual(n_skills, 0)
            self.assertEqual(n_cmds, 0)


if __name__ == "__main__":
    unittest.main()

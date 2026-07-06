"""Tests for tools/check-surface-budget.py — the session-start surface cap.

The gate fails if any skills/*/SKILL.md description exceeds 400 chars or any
commands/*.md description exceeds 150 chars. These tests lock both the real-tree
pass (parity with CI) and the failure behaviour against a synthetic tree, so a
future fat description can never slip the cap silently.

Offline-safe: no network, no key. Run:
    BOS_OFFLINE=1 python -m unittest tests.test_check_surface_budget
"""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _load_gate():
    """Load tools/check-surface-budget.py (hyphenated) as a module by path."""
    spec = importlib.util.spec_from_file_location(
        "check_surface_budget", REPO / "tools" / "check-surface-budget.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _skill_md(desc: str) -> str:
    return f"---\nname: X\ndescription: {desc}\n---\n\nBody.\n"


def _command_md(desc: str) -> str:
    return f"---\ndescription: {desc}\n---\n\nRun the skill.\n"


class TestRealTreeParity(unittest.TestCase):
    def test_gate_passes_on_real_tree(self):
        r = subprocess.run(
            [sys.executable, "tools/check-surface-budget.py"],
            cwd=REPO, capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_every_committed_description_is_within_cap(self):
        gate = _load_gate()
        for p in (REPO / "skills").glob("*/SKILL.md"):
            self.assertLessEqual(
                len(gate._description(p)), gate.SKILL_CAP,
                f"{p} skill description exceeds {gate.SKILL_CAP}",
            )
        for p in (REPO / "commands").glob("*.md"):
            self.assertLessEqual(
                len(gate._description(p)), gate.COMMAND_CAP,
                f"{p} command description exceeds {gate.COMMAND_CAP}",
            )


class TestFailsOverCap(unittest.TestCase):
    """Point the gate's REPO_ROOT at a synthetic tree and assert it flags fat ones."""

    def _scan_over(self, skills: dict, commands: dict) -> tuple[int, str]:
        gate = _load_gate()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, desc in skills.items():
                d = root / "skills" / name
                d.mkdir(parents=True)
                (d / "SKILL.md").write_text(_skill_md(desc), encoding="utf-8")
            (root / "commands").mkdir(parents=True, exist_ok=True)
            for name, desc in commands.items():
                (root / "commands" / f"{name}.md").write_text(
                    _command_md(desc), encoding="utf-8")
            gate.REPO_ROOT = root
            import io
            from contextlib import redirect_stdout
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = gate.scan()
            return rc, buf.getvalue()

    def test_clean_synthetic_tree_passes(self):
        rc, out = self._scan_over(
            skills={"ok": "short skill description"},
            commands={"ok": "short command label"},
        )
        self.assertEqual(rc, 0, out)

    def test_fat_skill_fails(self):
        rc, out = self._scan_over(
            skills={"fat": "x" * 401, "ok": "fine"},
            commands={},
        )
        self.assertEqual(rc, 2, out)
        self.assertIn("skills/fat/SKILL.md", out)
        self.assertNotIn("skills/ok/SKILL.md", out)

    def test_skill_at_cap_passes(self):
        rc, out = self._scan_over(skills={"edge": "x" * 400}, commands={})
        self.assertEqual(rc, 0, out)

    def test_fat_command_fails(self):
        rc, out = self._scan_over(
            skills={},
            commands={"fat": "x" * 151, "ok": "fine"},
        )
        self.assertEqual(rc, 2, out)
        self.assertIn("commands/fat.md", out)
        self.assertNotIn("commands/ok.md", out)

    def test_command_at_cap_passes(self):
        rc, out = self._scan_over(skills={}, commands={"edge": "x" * 150})
        self.assertEqual(rc, 0, out)


if __name__ == "__main__":
    unittest.main()

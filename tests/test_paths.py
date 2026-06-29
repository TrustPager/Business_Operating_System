"""Tests for kernel.runtime.paths.plugin_root().

The kernel needs ONE reliable way to find the plugin root so skills can
locate tools/, the registry, etc. on a plugin install. plugin_root() adopts
the documented CLAUDE_PLUGIN_ROOT anchor (referenced nowhere before this) and
falls back to walking up for the directory that owns .claude-plugin/.

Offline-safe: no network, no key. Run:
    python -m unittest tests.test_paths
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from kernel.runtime.paths import data_path, plugin_root, tool_path  # noqa: E402


class TestPluginRoot(unittest.TestCase):
    def setUp(self):
        self._prev = os.environ.get("CLAUDE_PLUGIN_ROOT")

    def tearDown(self):
        if self._prev is None:
            os.environ.pop("CLAUDE_PLUGIN_ROOT", None)
        else:
            os.environ["CLAUDE_PLUGIN_ROOT"] = self._prev

    def test_honours_env_var_when_set(self):
        with tempfile.TemporaryDirectory() as d:
            os.environ["CLAUDE_PLUGIN_ROOT"] = d
            self.assertEqual(plugin_root(), Path(d))

    def test_empty_env_var_falls_back(self):
        # An empty/blank env var must NOT win — fall back to the walk-up.
        os.environ["CLAUDE_PLUGIN_ROOT"] = ""
        root = plugin_root()
        self.assertTrue((root / ".claude-plugin").is_dir())

    def test_walks_up_to_claude_plugin_dir_when_unset(self):
        os.environ.pop("CLAUDE_PLUGIN_ROOT", None)
        root = plugin_root()
        # The discovered root is the directory that owns .claude-plugin/.
        self.assertTrue((root / ".claude-plugin").is_dir())
        # In this repo that is the repo root.
        self.assertEqual(root, REPO)

    def test_cwd_independent_when_env_unset(self):
        # Prove plugin_root() does not depend on the process working directory.
        os.environ.pop("CLAUDE_PLUGIN_ROOT", None)
        original_cwd = os.getcwd()
        tmp = tempfile.mkdtemp()
        try:
            os.chdir(tmp)
            root = plugin_root()
            # Must still find the real repo, not the temp dir.
            self.assertTrue((root / "kernel").is_dir(), "kernel/ not found under resolved root")
            self.assertTrue((root / "tools").is_dir(), "tools/ not found under resolved root")
        finally:
            os.chdir(original_cwd)
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)

    def test_tool_path_resolves_under_plugin_root(self):
        os.environ.pop("CLAUDE_PLUGIN_ROOT", None)
        expected = plugin_root() / "tools" / "check-no-secrets.py"
        self.assertEqual(tool_path("check-no-secrets.py"), expected)

    def test_tool_path_with_env_var(self):
        with tempfile.TemporaryDirectory() as d:
            os.environ["CLAUDE_PLUGIN_ROOT"] = d
            result = tool_path("my-tool.py")
            self.assertEqual(result, Path(d) / "tools" / "my-tool.py")

    def test_data_path_single_part(self):
        os.environ.pop("CLAUDE_PLUGIN_ROOT", None)
        expected = plugin_root() / "registry"
        self.assertEqual(data_path("registry"), expected)

    def test_data_path_multiple_parts(self):
        os.environ.pop("CLAUDE_PLUGIN_ROOT", None)
        expected = plugin_root() / "registry" / "skills.json"
        self.assertEqual(data_path("registry", "skills.json"), expected)

    def test_data_path_with_env_var(self):
        with tempfile.TemporaryDirectory() as d:
            os.environ["CLAUDE_PLUGIN_ROOT"] = d
            result = data_path("registry", "skills.json")
            self.assertEqual(result, Path(d) / "registry" / "skills.json")


if __name__ == "__main__":
    unittest.main()

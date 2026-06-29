"""Tests for the clean keyless-skip path in tools/setup.py.

Covers:
  - Blank key input -> exit 0, keyless message shown, no api_key written.
  - Valid tp_live_ key pasted -> key stored, exit 0 (keyed path preserved).
  - Already-configured key in bos.json -> reused without prompting, exit 0.

All I/O (input, getpass, subprocess) and filesystem writes are mocked so the
suite runs fully offline and never touches real files.
"""

from __future__ import annotations

import importlib
import json
import sys
import types
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, call, patch


# ---------------------------------------------------------------------------
# Helpers to load tools/setup.py cleanly (it lives outside the package root).
# ---------------------------------------------------------------------------

def _load_setup_module():
    """Import tools/setup.py as a module, patching the trustpager_api import."""
    repo_root = Path(__file__).resolve().parent.parent
    setup_path = repo_root / "tools" / "setup.py"

    # Provide a minimal stub for trustpager_api so the import doesn't need the
    # real package installed.
    fake_tp = types.ModuleType("trustpager_api")
    fake_tp.CONFIG_PATH = Path("/tmp/bos-test-bos.json")  # overridden per test
    sys.modules.setdefault("trustpager_api", fake_tp)

    spec = importlib.util.spec_from_file_location("setup_module", setup_path)
    mod = importlib.util.module_from_spec(spec)
    # Make sys.path include tools/ so the relative import inside setup.py works.
    tools_dir = str(repo_root / "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    spec.loader.exec_module(mod)
    return mod


_SETUP = _load_setup_module()

FAKE_KEY = "tp_live_TESTONLY_aaabbbccc"


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

class TestKeylessSkip(unittest.TestCase):
    """Blank key input should exit 0, print keyless message, write no api_key."""

    def _run_main(self, tmp_path: Path):
        config_path = tmp_path / "bos.json"
        with (
            patch.object(_SETUP, "CONFIG_PATH", config_path),
            patch.object(_SETUP, "_install_doc_stack", return_value=0),
            patch.object(_SETUP, "_find_key_in_mcp_config", return_value=None),
            patch("builtins.input", return_value=""),  # blank key
            patch("sys.stdout", new_callable=StringIO) as mock_out,
            patch("sys.argv", ["setup.py", "--skip-deps"]),
        ):
            rc = _SETUP.main()
        return rc, config_path, mock_out.getvalue()

    def test_blank_key_exits_zero(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            rc, _, _ = self._run_main(Path(tmp))
        self.assertEqual(rc, 0)

    def test_blank_key_no_api_key_written(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            _, config_path, _ = self._run_main(Path(tmp))
        if config_path.exists():
            cfg = json.loads(config_path.read_text())
            self.assertNotIn("api_key", cfg,
                             "api_key must NOT be written on keyless skip")

    def test_blank_key_bos_home_written(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            _, config_path, _ = self._run_main(Path(tmp))
            self.assertTrue(config_path.exists(), "bos.json should be created")
            cfg = json.loads(config_path.read_text())
            self.assertIn("bos_home", cfg, "bos_home must be set on keyless skip")

    def test_blank_key_keyless_message_shown(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            _, _, output = self._run_main(Path(tmp))
        self.assertIn("keyless floor is ready", output,
                      "Friendly keyless message must appear in stdout")

    def test_blank_key_no_error_text(self):
        """The word ERROR must not appear in stdout or stderr on blank key."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "bos.json"
            with (
                patch.object(_SETUP, "CONFIG_PATH", config_path),
                patch.object(_SETUP, "_install_doc_stack", return_value=0),
                patch.object(_SETUP, "_find_key_in_mcp_config", return_value=None),
                patch("builtins.input", return_value=""),
                patch("sys.stdout", new_callable=StringIO) as mock_out,
                patch("sys.stderr", new_callable=StringIO) as mock_err,
                patch("sys.argv", ["setup.py", "--skip-deps"]),
            ):
                _SETUP.main()
        self.assertNotIn("ERROR", mock_out.getvalue())
        self.assertNotIn("ERROR", mock_err.getvalue())


class TestKeyedPath(unittest.TestCase):
    """Pasting a valid tp_live_ key stores it exactly and exits 0."""

    def test_valid_key_stored(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "bos.json"
            # _write_launcher_shim needs a real parent dir to write into.
            shim_dir = Path(tmp)
            with (
                patch.object(_SETUP, "CONFIG_PATH", config_path),
                patch.object(_SETUP, "_install_doc_stack", return_value=0),
                patch.object(_SETUP, "_find_key_in_mcp_config", return_value=None),
                patch.object(_SETUP, "_write_launcher_shim",
                             return_value=shim_dir / "bos-run.py"),
                patch("builtins.input", return_value=FAKE_KEY),
                patch("sys.stdout", new_callable=StringIO),
                patch("sys.argv", ["setup.py", "--skip-deps"]),
            ):
                rc = _SETUP.main()

            self.assertEqual(rc, 0)
            self.assertTrue(config_path.exists())
            cfg = json.loads(config_path.read_text())
            self.assertEqual(cfg.get("api_key"), FAKE_KEY,
                             "The pasted key must be stored verbatim")

    def test_valid_key_exits_zero(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "bos.json"
            shim_dir = Path(tmp)
            with (
                patch.object(_SETUP, "CONFIG_PATH", config_path),
                patch.object(_SETUP, "_install_doc_stack", return_value=0),
                patch.object(_SETUP, "_find_key_in_mcp_config", return_value=None),
                patch.object(_SETUP, "_write_launcher_shim",
                             return_value=shim_dir / "bos-run.py"),
                patch("builtins.input", return_value=FAKE_KEY),
                patch("sys.stdout", new_callable=StringIO),
                patch("sys.argv", ["setup.py", "--skip-deps"]),
            ):
                rc = _SETUP.main()
        self.assertEqual(rc, 0)


class TestExistingKeyReuse(unittest.TestCase):
    """A key already in bos.json is reused without prompting."""

    def test_existing_key_no_prompt(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "bos.json"
            # Pre-write a config with an existing key.
            config_path.write_text(
                json.dumps({"api_key": FAKE_KEY, "bos_home": str(tmp)}),
                encoding="utf-8",
            )
            shim_dir = Path(tmp)
            mock_input = MagicMock()
            with (
                patch.object(_SETUP, "CONFIG_PATH", config_path),
                patch.object(_SETUP, "_install_doc_stack", return_value=0),
                patch.object(_SETUP, "_write_launcher_shim",
                             return_value=shim_dir / "bos-run.py"),
                patch("builtins.input", mock_input),
                patch("sys.stdout", new_callable=StringIO),
                patch("sys.argv", ["setup.py", "--skip-deps"]),
            ):
                rc = _SETUP.main()

        self.assertEqual(rc, 0)
        # input() must NOT have been called with the key-paste prompt.
        paste_calls = [
            c for c in mock_input.call_args_list
            if "tp_live_" in str(c)
        ]
        self.assertEqual(paste_calls, [],
                         "Key-paste prompt must not appear when key already set")


if __name__ == "__main__":
    unittest.main()

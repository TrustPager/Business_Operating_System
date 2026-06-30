"""Tests for the keyless firecrawl MCP registration in tools/setup.py.

Covers the JSON-merge fallback (_register_firecrawl_via_json) and the
idempotency guard (_firecrawl_already_registered):
  - Fresh machine (no ~/.claude.json): the file is created with the firecrawl
    server under mcpServers, shaped as a user-scope HTTP server.
  - Preserve everything: an existing config with other top-level keys AND other
    mcpServers entries keeps all of them; only firecrawl is added.
  - Idempotent: a second register is a no-op (already-registered is detected;
    no duplicate, the firecrawl entry is unchanged).
  - Never clobber an unreadable file: a corrupt ~/.claude.json is left byte-for-
    byte intact and the merge reports failure rather than overwriting it.

All tests point the module's _CLAUDE_JSON at a temp file, so they never touch
the real ~/.claude.json. Offline-safe: no network, no CLI, no key. Run:
    python -m unittest tests.test_setup_firecrawl
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path

from unittest.mock import patch


def _load_setup_module():
    """Load tools/setup.py without triggering the real trustpager_api import."""
    repo_root = Path(__file__).resolve().parent.parent
    setup_path = repo_root / "tools" / "setup.py"

    fake_tp = types.ModuleType("trustpager_api")
    fake_tp.CONFIG_PATH = Path(tempfile.gettempdir()) / "bos-test-placeholder.json"
    sys.modules.setdefault("trustpager_api", fake_tp)

    tools_dir = str(repo_root / "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)

    spec = importlib.util.spec_from_file_location("setup_module_firecrawl", setup_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_SETUP = _load_setup_module()


class TestFirecrawlRegistration(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.claude_json = Path(self._tmp.name) / ".claude.json"
        # Redirect the module-level constant at the temp file for every test.
        self._patcher = patch.object(_SETUP, "_CLAUDE_JSON", self.claude_json)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()
        self._tmp.cleanup()

    def _read(self) -> dict:
        return json.loads(self.claude_json.read_text(encoding="utf-8"))

    def test_fresh_machine_creates_user_scope_http_server(self):
        self.assertFalse(self.claude_json.exists())
        self.assertFalse(_SETUP._firecrawl_already_registered())

        ok = _SETUP._register_firecrawl_via_json()
        self.assertTrue(ok)

        data = self._read()
        self.assertIn("firecrawl", data["mcpServers"])
        self.assertEqual(
            data["mcpServers"]["firecrawl"],
            {"type": "http", "url": "https://mcp.firecrawl.dev/v2/mcp"},
        )
        self.assertTrue(_SETUP._firecrawl_already_registered())

    def test_preserves_existing_keys_and_other_servers(self):
        original = {
            "numStartups": 7,
            "projects": {"/some/path": {"history": ["a", "b"]}},
            "mcpServers": {
                "trustpager": {"type": "http", "url": "https://example.invalid"},
            },
        }
        self.claude_json.write_text(json.dumps(original, indent=2), encoding="utf-8")

        ok = _SETUP._register_firecrawl_via_json()
        self.assertTrue(ok)

        data = self._read()
        # Everything that was there is still there, untouched.
        self.assertEqual(data["numStartups"], 7)
        self.assertEqual(data["projects"], {"/some/path": {"history": ["a", "b"]}})
        self.assertEqual(
            data["mcpServers"]["trustpager"],
            {"type": "http", "url": "https://example.invalid"},
        )
        # And firecrawl was added alongside.
        self.assertIn("firecrawl", data["mcpServers"])

    def test_idempotent_second_call_is_noop(self):
        _SETUP._register_firecrawl_via_json()
        self.assertTrue(_SETUP._firecrawl_already_registered())
        first = self.claude_json.read_text(encoding="utf-8")

        # Re-registering must not duplicate or alter the firecrawl entry.
        _SETUP._register_firecrawl_via_json()
        data = self._read()
        servers = data["mcpServers"]
        self.assertEqual(
            list(servers.keys()).count("firecrawl"), 1,
            "firecrawl must appear exactly once",
        )
        self.assertEqual(
            servers["firecrawl"],
            {"type": "http", "url": "https://mcp.firecrawl.dev/v2/mcp"},
        )
        # Content is stable across a redundant register.
        self.assertEqual(self.claude_json.read_text(encoding="utf-8"), first)

    def test_unreadable_config_is_not_clobbered(self):
        corrupt = "{ this is not valid json "
        self.claude_json.write_text(corrupt, encoding="utf-8")

        ok = _SETUP._register_firecrawl_via_json()
        self.assertFalse(ok, "must report failure rather than overwrite")
        # The original bytes are left exactly intact.
        self.assertEqual(self.claude_json.read_text(encoding="utf-8"), corrupt)
        self.assertFalse(_SETUP._firecrawl_already_registered())


if __name__ == "__main__":
    unittest.main()

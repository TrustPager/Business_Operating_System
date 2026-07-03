# drivers/deploy-cli/__init__.py — fixture: a good keyed_cli connected driver.
"""Fixture driver for the conformance gate's good-path (keyed_cli).

Documentation-only. A keyed_cli driver is invoked via a local CLI (no Python
transport). Exercises the connected structural checks against the second
connected kind, and the connected frontmatter contract's data_path: local branch.
"""

DRIVER = {
    "id": "deploy-cli",
    "kind": "keyed_cli",
    "display_name": "Deploy CLI",
    "cli": "deploy",
    "tool_prefix": "mcp__deploy-cli__",
    "connect_doc": "connect.md",
    "credential": "key",
    "secret_pattern": "dpl_[A-Za-z0-9]{24}",
}

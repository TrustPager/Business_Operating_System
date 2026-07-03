# drivers/widget-ads/__init__.py — fixture: connected driver, card heading absent.
"""Fixture: a well-formed connected (claude_mcp) DRIVER dict with connect.md
present, but knowledge/connectors.md has NO heading beginning with the
display_name, so the gate must FAIL the card rule (the only defect)."""

DRIVER = {
    "id": "widget-ads",
    "kind": "claude_mcp",
    "display_name": "Widget Ads",
    "server_url": "https://mcp.example.com/widget",
    "tool_prefix": "mcp__widget-ads__",
    "connect_doc": "connect.md",
    "credential": "mcp",
}

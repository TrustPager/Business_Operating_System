# drivers/widget-ads/__init__.py — fixture: connected driver, NO connect.md.
"""Fixture: a well-formed connected (claude_mcp) DRIVER dict whose driver folder
is missing connect.md, so the gate must FAIL the connect.md rule. The card is
present so connect.md is the only defect."""

DRIVER = {
    "id": "widget-ads",
    "kind": "claude_mcp",
    "display_name": "Widget Ads",
    "server_url": "https://mcp.example.com/widget",
    "tool_prefix": "mcp__widget-ads__",
    "connect_doc": "connect.md",
    "credential": "mcp",
}

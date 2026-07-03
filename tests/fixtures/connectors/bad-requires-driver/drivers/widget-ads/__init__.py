# drivers/widget-ads/__init__.py — fixture: valid driver; a skill typos its id.
"""Fixture: the driver is well-formed, but the connected skill's requires_driver
is a typo that resolves to nothing (no `none`, not a keyless driver, no
drivers/<id>/ folder), so the gate must FAIL the requires_driver resolution rule."""

DRIVER = {
    "id": "widget-ads",
    "kind": "claude_mcp",
    "display_name": "Widget Ads",
    "server_url": "https://mcp.example.com/widget",
    "tool_prefix": "mcp__widget-ads__",
    "connect_doc": "connect.md",
    "credential": "mcp",
}

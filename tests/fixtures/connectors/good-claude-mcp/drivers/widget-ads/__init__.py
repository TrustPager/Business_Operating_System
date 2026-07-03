# drivers/widget-ads/__init__.py — fixture: a good claude_mcp connected driver.
"""Fixture driver for the conformance gate's good-path (claude_mcp).

Documentation-only shape mirroring drivers/meta-ads. Exercises the connected
structural checks: kind in taxonomy, connect.md present, a connectors.md card
whose heading begins with display_name, and a connected skill honoring the
frontmatter contract with data_path: mcp_tools.
"""

DRIVER = {
    "id": "widget-ads",
    "kind": "claude_mcp",
    "display_name": "Widget Ads",
    "server_url": "https://mcp.example.com/widget",
    "tool_prefix": "mcp__widget-ads__",
    "connect_doc": "connect.md",
    "credential": "mcp",
    "never_call": ["mcp__widget-ads__widget_activate"],
    "never_set": {
        "mcp__widget-ads__widget_update": ["status", "configured_status"],
    },
}

# drivers/widget-ads/__init__.py — fixture: valid driver; connected skill has an
# invalid requires_credential.
"""Fixture: driver, connect.md, and card are all well-formed, so the ONLY defect is
the connected skill's requires_credential being outside {mcp, key}. Isolates the
credential sub-rule of the connected frontmatter contract (data_path and uses_tools
are deliberately valid here), complementing bad-frontmatter."""

DRIVER = {
    "id": "widget-ads",
    "kind": "claude_mcp",
    "display_name": "Widget Ads",
    "server_url": "https://mcp.example.com/widget",
    "tool_prefix": "mcp__widget-ads__",
    "connect_doc": "connect.md",
    "credential": "mcp",
}

# drivers/widget-ads/__init__.py — fixture: valid driver; connected skill breaks
# the frontmatter contract.
"""Fixture: driver, connect.md, and card are all well-formed, so the ONLY defects
are in the connected skill's frontmatter: requires_credential not in {mcp,key},
data_path not in {mcp_tools,local}, and a uses_tools entry that is not
driver-owned. The gate must FAIL the connected frontmatter contract."""

DRIVER = {
    "id": "widget-ads",
    "kind": "claude_mcp",
    "display_name": "Widget Ads",
    "server_url": "https://mcp.example.com/widget",
    "tool_prefix": "mcp__widget-ads__",
    "connect_doc": "connect.md",
    "credential": "mcp",
}

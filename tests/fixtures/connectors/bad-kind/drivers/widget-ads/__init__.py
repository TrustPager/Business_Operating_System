# drivers/widget-ads/__init__.py — fixture: BROKEN, kind not in the taxonomy.
"""Fixture: the DRIVER dict declares a kind outside the canonical set, so the
conformance gate must FAIL on the `kind` rule."""

DRIVER = {
    "id": "widget-ads",
    "kind": "mystery_kind",              # not in CANONICAL_KINDS
    "display_name": "Widget Ads",
    "server_url": "https://mcp.example.com/widget",
    "tool_prefix": "mcp__widget-ads__",
    "connect_doc": "connect.md",
    "credential": "mcp",
}

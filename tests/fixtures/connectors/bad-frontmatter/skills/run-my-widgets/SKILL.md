---
name: Run My Widgets
description: Fixture connected skill that violates the connected frontmatter contract three ways.
triggers:
  - run my widgets
function_slot: ads
requires_driver: widget-ads
requires_credential: key
data_path: reasoning_only
status: active
uses_tools:
  - mcp__widget-ads__widget_get_accounts
  - mcp__some-other-driver__foreign_tool
---

# Run My Widgets

Fixture body. data_path is reasoning_only (not mcp_tools/local) and uses_tools
lists a foreign, non-driver-owned tool. requires_credential is a valid value so
that rule alone passes; the other two fail.

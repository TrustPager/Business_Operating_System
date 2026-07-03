---
name: Run My Widgets
description: Fixture connected skill; frontmatter is valid so only the driver kind fails.
triggers:
  - run my widgets
function_slot: ads
requires_driver: widget-ads
requires_credential: mcp
data_path: mcp_tools
status: active
uses_tools:
  - mcp__widget-ads__widget_get_accounts
  - mcp__widget-ads__widget_create_campaign
---

# Run My Widgets

Fixture body.

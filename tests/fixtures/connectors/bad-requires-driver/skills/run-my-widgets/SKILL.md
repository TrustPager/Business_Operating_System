---
name: Run My Widgets
description: Fixture connected skill whose requires_driver is a typo (widget-adz) that resolves to nothing.
triggers:
  - run my widgets
function_slot: ads
requires_driver: widget-adz
requires_credential: mcp
data_path: mcp_tools
status: active
uses_tools:
  - mcp__widget-ads__widget_get_accounts
---

# Run My Widgets

Fixture body. The typo'd requires_driver is the only defect.

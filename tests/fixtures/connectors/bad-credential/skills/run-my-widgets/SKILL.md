---
name: Run My Widgets
description: Fixture connected skill whose requires_credential is 'none' (invalid for a connected add-on).
triggers:
  - run my widgets
function_slot: ads
requires_driver: widget-ads
requires_credential: none
data_path: mcp_tools
status: active
uses_tools:
  - mcp__widget-ads__widget_get_accounts
---

# Run My Widgets

Fixture body. requires_credential 'none' is the only defect; data_path and the
single driver-owned tool are valid so the credential sub-rule fires alone.

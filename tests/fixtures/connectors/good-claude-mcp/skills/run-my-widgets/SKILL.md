---
name: Run My Widgets
description: Once your Widget Ads account is connected, turn your plan into ready-to-launch widget campaigns, created paused and safe.
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
  - mcp__widget-ads__widget_update
---

# Run My Widgets

You turn the owner's plan into real widget campaigns, built paused. You confirm
every write, journal it, and never turn a widget on. The activate tool is
deliberately absent from uses_tools, so naming it in a call would fail the safety
checks.

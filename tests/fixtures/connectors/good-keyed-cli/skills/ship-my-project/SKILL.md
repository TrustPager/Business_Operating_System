---
name: Ship My Project
description: Once your Deploy CLI is connected, take your project live with one command, checked over first.
triggers:
  - ship my project
function_slot: creative
requires_driver: deploy-cli
requires_credential: key
data_path: local
status: active
uses_tools:
  - mcp__deploy-cli__deploy_list_projects
  - mcp__deploy-cli__deploy_create_deployment
---

# Ship My Project

You take the owner's project live via the deploy CLI, confirming each step first.

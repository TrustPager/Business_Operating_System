# drivers/meta-ads/__init__.py
"""Meta Ads driver — the first claude_mcp-type driver.

DOCUMENTATION ONLY. No BOS mechanism imports or reads this module today; there is
no driver-metadata loader. The load-bearing artifacts are the requires_driver
string on run-my-ads, connect.md, and the connectors.md card (see spec §3a). This
file records the reusable shape for the next connected-MCP driver (Google Ads,
etc.) and the machine-readable spend-safety facts a future loader could consume.

Unlike keyed-REST drivers (trustpager), a claude_mcp driver has NO Python
transport. The Claude Code client hosts the MCP (connected by the owner via
OAuth); BOS skills call the mcp__meta-ads__* tools directly. Method attributed to
Evelyn Weiss.
"""

DRIVER = {
    "id": "meta-ads",
    "kind": "claude_mcp",              # keyed_rest | keyed_cli | keyless_mcp | local | data_pack | claude_mcp
    "display_name": "Meta Ads",
    "server_url": "https://mcp.facebook.com/ads",
    "tool_prefix": "mcp__meta-ads__",
    "connect_doc": "connect.md",
    "credential": "mcp",               # OAuth, no key paste
    "read_only_scope_first": True,     # grant the read-only scope tier first (§8)
    # Spend-safety hard lines (see §8). Documentation of intent; the live guard is
    # the CI check in tools/check-connectors.py, not this dict.
    "never_call": ["mcp__meta-ads__ads_activate_entity"],
    # All three interchangeable status fields Meta exposes on an entity —
    # setting any of them to ACTIVE un-pauses a shell just as an activate call would.
    "never_set": {
        "mcp__meta-ads__ads_update_entity": [
            "status", "configured_status", "effective_status",
        ]
    },
}

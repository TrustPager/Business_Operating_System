# drivers/vercel/__init__.py
"""Vercel driver — the reference keyed_cli-type driver.

DOCUMENTATION ONLY. No BOS mechanism imports or reads this module today; there is
no driver-metadata loader. The load-bearing artifacts are the requires_driver
string on launch-my-site, connect.md, and the connectors.md card (see the Tier-1
Connected Add-on Kit §3). This file records the reusable shape the kit's taxonomy
names for a keyed local CLI, so the next keyed_cli driver gets the safe shape by
default.

Unlike a claude_mcp driver (meta-ads), a keyed_cli driver is NOT a hosted MCP:
there is no server_url and no mcp__* tool surface in play. The owner installs the
CLI and authorizes it once (a browser sign-in via ``vercel login``, or a
``VERCEL_TOKEN``); BOS skills shell the ``vercel`` CLI via Bash. And unlike a
keyed-REST driver (trustpager), it has NO Python transport: no DriverConfig, no
auth.py, no catalog.py, no key resolver, no import of kernel.runtime.*.

No ``never_call`` / ``never_set``: a CLI deploy has no quiet live-switch. The one
explicit switch — a production deploy (``vercel --prod``) — is guarded by
launch-my-site's Hard rules, not by this driver, so the connector gate's safety
scan is a no-op for vercel by construction.
"""

DRIVER = {
    "id": "vercel",
    "kind": "keyed_cli",               # keyed_rest | keyed_cli | keyless_mcp | local | data_pack | claude_mcp
    "display_name": "Vercel",
    "cli": "vercel",                   # the local CLI invoked via Bash (NOT a server_url)
    "tool_prefix": "mcp__vercel__",    # unused (the skill shells the CLI); kept for shape parity
    "connect_doc": "connect.md",
    "credential": "key",               # a token/sign-in the owner supplies (not OAuth-into-MCP)
    "read_only_scope_first": True,     # verify with a read (`vercel whoami`) and preview before any prod deploy
    # secret_pattern: for redaction of a leaked token in logs/output. A Vercel token
    # is 24 alphanumeric characters (bounded on word edges so it doesn't over-match).
    "secret_pattern": r"\b[A-Za-z0-9]{24}\b",
}

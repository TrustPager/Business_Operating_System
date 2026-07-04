# drivers/_template/__init__.py
"""Connected-driver TEMPLATE — the copyable shape for the next connected add-on.

DOCUMENTATION ONLY. Nothing in BOS imports or reads this module. There is no
driver-metadata loader, and the connector gate (tools/check-connectors.py) SKIPS
every underscore-prefixed driver dir — so this ``_template`` folder is never
validated and its ``<placeholder>`` values can never fail CI. It exists purely so
an author cloning the next connected driver (Google Ads, a deploy host, and the
like) gets the safe, conformant shape by default instead of authoring it cold.

To use it: copy this whole folder to ``drivers/<your-id>/`` (drop the underscore),
fill every ``<placeholder>``, delete the fields that do not apply to your kind, and
follow the four-file clone steps in ``drivers/meta-ads/README.md`` and the recipe
at ``docs/architecture/tier-1-addon-kit.md``. The worked, shipping example this
mirrors is ``drivers/meta-ads/`` — read it alongside this template.

Like ``drivers/meta-ads/__init__.py``, a ``claude_mcp`` driver has NO Python
transport: no ``DriverConfig``, no ``auth.py``, no ``catalog.py``, no key resolver.
The Claude Code client hosts the MCP (the owner connects it over OAuth), and BOS
skills call the ``mcp__<id>__*`` tools directly. Do NOT add a transport here, and
do NOT add the driver to ``_KEYLESS_DRIVERS`` — a connected add-on is connected
tier, not keyless.
"""

# The top-level ``DRIVER`` dict — the machine-readable shape a future loader could
# consume, and the declarative record of the add-on's spend-safety hard lines.
# Every field is explained below. Fill each ``<placeholder>``; delete the fields
# that do not apply to your driver's ``kind`` (see the per-field notes).
DRIVER = {
    # id: the driver's folder id (``drivers/<id>/``). Lowercase, hyphen-free segment
    # that appears inside every one of its tool names (``mcp__<id>__*``). This is the
    # value skills carry as ``requires_driver: <id>`` — it MUST match the folder name.
    "id": "<driver-id>",

    # kind: the driver's taxonomy slot. MUST be one of the canonical six, or the gate
    # fails conformance. Pick the one that matches your driver's physical reality:
    #   keyed_rest | keyed_cli | keyless_mcp | local | data_pack | claude_mcp
    # This template is written for the two CONNECTED kinds (claude_mcp, keyed_cli);
    # a claude_mcp OAuth MCP is the worked default (mirrors meta-ads).
    "kind": "claude_mcp",

    # display_name: the human name shown to the owner. The gate matches this driver to
    # its knowledge/connectors.md card by PREFIX, so the card heading must BEGIN with
    # this exact string (a parenthetical suffix on the heading is fine — e.g. heading
    # "## <Display Name> (<plain parenthetical>)" matches display_name "<Display Name>").
    "display_name": "<Display Name>",

    # server_url / cli: the connect endpoint — use exactly ONE, matching your kind, and
    # DELETE the other line.
    #   - claude_mcp: keep ``server_url`` (the hosted MCP URL the owner OAuths into).
    #   - keyed_cli:  delete ``server_url`` and keep ``cli`` (the local CLI invoked via
    #     Bash, e.g. "vercel"); a keyed_cli driver also carries a ``secret_pattern``.
    "server_url": "https://<your-mcp-endpoint>",   # claude_mcp: the hosted MCP URL
    # "cli": "<cli-command>",                       # keyed_cli: use this INSTEAD of server_url

    # tool_prefix: the shared prefix of every tool this driver owns. Always
    # ``mcp__<id>__`` for an MCP-hosted driver; keep it consistent with ``id`` above.
    "tool_prefix": "mcp__<driver-id>__",

    # connect_doc: the filename of the single-home connect walkthrough in this folder.
    # Always "connect.md" — the connect steps live there and nowhere else.
    "connect_doc": "connect.md",

    # credential: how the owner authorizes. "mcp" for a claude_mcp OAuth MCP (no key
    # paste — the owner signs in). "key" for a keyed_cli / keyed driver (an API key or
    # token the owner supplies). It must be one of {mcp, key} for a connected add-on.
    "credential": "mcp",

    # read_only_scope_first: grant the read-only access tier first, then widen only when
    # the owner is ready to act (spend/deploy/write). Keep True for any driver that can
    # do something irreversible; it keeps accidental live actions impossible on connect.
    "read_only_scope_first": True,

    # --- Spend-safety hard lines (OPTIONAL) --------------------------------------
    # Include ``never_call`` and ``never_set`` ONLY if this driver can spend money or do
    # anything irreversible. A read-only or purely additive add-on omits both entirely.
    # These are documentation of intent; the live guard is the CI scan in
    # tools/check-connectors.py, which reads these declarations and fails on any skill
    # body that names a never_call tool or sets a never_set field to a live value.

    # never_call — "the loud switch": tools BOS must NEVER call because calling one is
    # itself the irreversible/live-money action (e.g. an "activate"/"turn on" tool).
    # List the fully-qualified name(s); the gate also searches the bare form.
    "never_call": ["mcp__<driver-id>__<activate_tool>"],

    # never_set — "the quiet switch": an update-style tool that legitimately STAYS in a
    # skill's uses_tools (it edits a still-safe/paused shell), paired with the field(s)
    # that must never be set to a live/ACTIVE value through it.
    #
    # List ALL interchangeable status fields, not just one. A platform often exposes
    # several fields that each un-pause a shell on their own — meta-ads exposes THREE
    # (``status``, ``configured_status``, ``effective_status``), and setting ANY ONE of
    # them to ACTIVE turns the shell live just as an activate call would. A one-field
    # example would look safe while leaving the other paths open, so copy the exhaustive
    # form below and replace with your platform's real interchangeable set.
    "never_set": {
        "mcp__<driver-id>__<update_tool>": [
            "<status_field>", "<configured_status_field>", "<effective_status_field>",
        ]
    },
}

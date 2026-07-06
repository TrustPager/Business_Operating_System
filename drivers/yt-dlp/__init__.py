# drivers/yt-dlp/__init__.py
"""yt-dlp driver — an OPTIONAL keyless local-CLI deepener for research-my-channel.

DOCUMENTATION ONLY. No BOS mechanism imports or reads this module; there is no
driver-metadata loader. The load-bearing artifacts are the DRIVER dict (so
check-connectors.py validates the kind) and this file + README.md documenting the
honest Firecrawl-vs-yt-dlp boundary. It is NOT a connected driver: kind is
``local`` (a local binary, no account, keyless), so it ships neither connect.md nor
a connectors.md card, and it carries no ``never_call``/``never_set`` (a read-only
scrape has no irreversible/live action). It stays on the keyless floor.
"""

DRIVER = {
    "id": "yt-dlp",
    "kind": "local",                 # keyed_rest | keyed_cli | keyless_mcp | local | data_pack | claude_mcp
    "display_name": "yt-dlp",
    "cli": "yt-dlp",                 # the local CLI invoked via Bash; keyless, no account
    "connect_doc": None,             # local driver: no connect flow, no connect.md
    "credential": "none",            # keyless local binary
    "read_only_scope_first": True,   # read-only scrape; never a write
}

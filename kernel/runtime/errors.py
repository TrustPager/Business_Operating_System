"""Errors — the vendor-neutral base exception for the BOS kernel.

`BOSError` carries a friendly, user-facing message. Drivers and tools raise it
for any failure that an end user (not just a developer) should read.
"""

from __future__ import annotations


class BOSError(Exception):
    """Friendly, user-facing error. The message is intended for end users."""

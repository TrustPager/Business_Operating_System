"""tools/regional.py - Region-gated loader for AU constants.

load_au_constants(region) returns the parsed AU constants dict ONLY when
region == "AU" (exact, case-sensitive). Any other value raises ValueError.

This is a defence-in-depth backstop so AU tax/wage data can never load
for a non-AU caller even if upstream logic mis-routes.

Usage:
    from tools.regional import load_au_constants
    constants = load_au_constants("AU")
    gst_rate = constants["gst"]["rate"]["value"]  # 0.10

Offline-safe: reads the bundled JSON file; never fetches from the network.
"""

import json
from pathlib import Path

_DRIVERS_DIR = Path(__file__).resolve().parent.parent / "drivers" / "regional"


def load_au_constants(region: str) -> dict:
    """Return the parsed AU constants dict.

    Parameters
    ----------
    region : str
        Must be exactly "AU". Any other value (including "au", "", None,
        "US", etc.) raises ValueError.

    Returns
    -------
    dict
        Parsed contents of drivers/regional/au/constants-FY*.json.

    Raises
    ------
    ValueError
        If region is not exactly "AU".
    FileNotFoundError
        If no constants-FY*.json file exists in the au driver directory.
    """
    if region != "AU":
        raise ValueError(
            f"load_au_constants requires region='AU'; got {region!r}. "
            "This loader is AU-only. For other regions, build a separate loader."
        )

    au_dir = _DRIVERS_DIR / "au"
    candidates = sorted(au_dir.glob("constants-*.json"))
    if not candidates:
        raise FileNotFoundError(
            f"No constants-*.json file found in {au_dir}. "
            "Run the update procedure in drivers/regional/au/README.md."
        )

    # Use the most recent file (sorted lexicographically; FY names sort correctly)
    constants_path = candidates[-1]
    with open(constants_path, encoding="utf-8") as f:
        return json.load(f)

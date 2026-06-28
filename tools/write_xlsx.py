#!/usr/bin/env python3
"""write_xlsx.py — the doc-lib-set WRITE side for Excel (.xlsx).

The keyless WRITE counterpart to markitdown_convert.py (the READ side). Where
MarkItDown turns any document into Markdown for Claude to read, this turns
structured data Claude produced into a real .xlsx an owner can open — no
account, no network, one local install.

Usage:
    # rows as JSON on the command line (a list of row-lists):
    python tools/write_xlsx.py --out pricing.xlsx --rows '[["Item","Qty","Price"],["Site visit",1,120]]'

    # or pipe the JSON in on stdin:
    cat rows.json | python tools/write_xlsx.py --out pricing.xlsx

    # optional sheet title and a bold header row:
    python tools/write_xlsx.py --out q.xlsx --rows '[...]' --sheet "Quote" --header

Input shape: a JSON array of rows, each row a JSON array of cell values
(strings / numbers / booleans / null). The first row is treated as the header
when --header is passed (it is rendered bold).

This is part of the doc-lib-set keyless WRITE driver (`doclib`). See
knowledge/document-tools-method.md. No network at runtime.
"""
import sys
import json
import argparse


# The pip spec the BOS installs when this lib is missing.
MISSING_DEP_SPEC = "openpyxl"

# Machine-readable + human missing-dependency signal (D11). The leading
# BOS_MISSING_DEP: line is what the SKILL layer keys off to run a detect ->
# offer -> install-on-yes -> verify loop; the second line recommends
# `python -m pip install` (never bare `pip`, a churn trap on multi-Python Windows).
INSTALL_HINT = (
    f"BOS_MISSING_DEP: {MISSING_DEP_SPEC}\n"
    "openpyxl isn't installed (the doc-lib-set tool for writing .xlsx files).\n"
    f"Install it with: python -m pip install {MISSING_DEP_SPEC}\n"
)


def _load_rows(rows_arg: str | None) -> list[list]:
    """Load the rows JSON from --rows or stdin; validate it is a list of lists."""
    if rows_arg is not None:
        raw = rows_arg
    else:
        raw = sys.stdin.read()
    if not raw.strip():
        sys.stderr.write("No rows provided (pass --rows '<json>' or pipe JSON on stdin).\n")
        sys.exit(1)
    try:
        rows = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Could not parse rows JSON: {e}\n")
        sys.exit(1)
    if not isinstance(rows, list) or not all(isinstance(r, list) for r in rows):
        sys.stderr.write("Rows must be a JSON array of arrays, e.g. [[\"A\",\"B\"],[1,2]].\n")
        sys.exit(1)
    return rows


def write_xlsx(path: str, rows: list[list], *, sheet: str | None = None,
               header: bool = False) -> None:
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
    except ImportError:
        sys.stderr.write(INSTALL_HINT)
        sys.exit(2)

    wb = Workbook()
    ws = wb.active
    if sheet:
        ws.title = sheet[:31]  # Excel caps sheet titles at 31 chars

    try:
        for r_idx, row in enumerate(rows, start=1):
            for c_idx, value in enumerate(row, start=1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                if header and r_idx == 1:
                    cell.font = Font(bold=True)
        wb.save(path)
    except Exception as e:  # noqa: BLE001 — surface the real reason to the operator
        sys.stderr.write(f"Could not write {path}: {e}\n")
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description="Write a real .xlsx from JSON rows (openpyxl).")
    ap.add_argument("--out", required=True, help="Path to write the .xlsx file to.")
    ap.add_argument("--rows", help="Rows as a JSON array of arrays. Omit to read JSON from stdin.")
    ap.add_argument("--sheet", help="Optional sheet title.")
    ap.add_argument("--header", action="store_true", help="Render the first row bold (header).")
    args = ap.parse_args()

    rows = _load_rows(args.rows)
    write_xlsx(args.out, rows, sheet=args.sheet, header=args.header)
    sys.stderr.write(f"Wrote {len(rows)} row(s) to {args.out}\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""pdf_tables.py — precise table/text extraction from a PDF (doc-lib-set READ-precise).

MarkItDown (tools/markitdown_convert.py) is the standard READ path: any document
to clean Markdown. But Markdown flattens a PDF's table grid, which loses cell
structure when you need the actual rows and columns (a statement, an invoice, a
priced schedule). This wrapper uses pdfplumber to pull tables out as structured
rows — and, with --text, the raw page text — so a skill that needs the grid
gets the grid, not a flattened approximation.

Usage:
    python tools/pdf_tables.py statement.pdf                 # tables -> JSON on stdout
    python tools/pdf_tables.py statement.pdf --out tables.json
    python tools/pdf_tables.py statement.pdf --text          # extract page text instead
    python tools/pdf_tables.py statement.pdf --pages 1-3      # limit to a page range

Output (default, tables): JSON of the form
    {"pages": [{"page": 1, "tables": [[["A","B"],["1","2"]], ...]}, ...]}
Output (--text): JSON of the form
    {"pages": [{"page": 1, "text": "..."}, ...]}

This is part of the doc-lib-set keyless driver (`doclib`). See
knowledge/document-tools-method.md. No network at runtime.
"""
import sys
import json
import argparse


INSTALL_HINT = (
    "pdfplumber isn't installed. It's the doc-lib-set tool for precise PDF "
    "table/text extraction.\n"
    "Install it once:\n"
    "    pip install pdfplumber\n"
)


def _parse_pages(spec: str | None, total: int) -> list[int]:
    """Resolve a 1-based page spec ('1', '1-3', '2,4') to 0-based indices.

    None means all pages. Out-of-range indices are clamped/dropped.
    """
    if spec is None:
        return list(range(total))
    wanted: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo_s, _, hi_s = part.partition("-")
            try:
                lo, hi = int(lo_s), int(hi_s)
            except ValueError:
                sys.stderr.write(f"Bad page range: {part!r}\n")
                sys.exit(1)
            for n in range(lo, hi + 1):
                wanted.add(n - 1)
        else:
            try:
                wanted.add(int(part) - 1)
            except ValueError:
                sys.stderr.write(f"Bad page number: {part!r}\n")
                sys.exit(1)
    return [i for i in sorted(wanted) if 0 <= i < total]


def extract(path: str, *, want_text: bool = False, pages: str | None = None) -> dict:
    try:
        import pdfplumber
    except ImportError:
        sys.stderr.write(INSTALL_HINT)
        sys.exit(2)

    out_pages: list[dict] = []
    try:
        with pdfplumber.open(path) as pdf:
            indices = _parse_pages(pages, len(pdf.pages))
            for i in indices:
                page = pdf.pages[i]
                if want_text:
                    out_pages.append({"page": i + 1, "text": page.extract_text() or ""})
                else:
                    tables = page.extract_tables() or []
                    out_pages.append({"page": i + 1, "tables": tables})
    except FileNotFoundError:
        sys.stderr.write(f"File not found: {path}\n")
        sys.exit(1)
    except Exception as e:  # noqa: BLE001 — surface the real reason to the operator
        sys.stderr.write(f"Could not extract from {path}: {e}\n")
        sys.exit(1)
    return {"pages": out_pages}


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Extract tables (or text) from a PDF as JSON (pdfplumber)."
    )
    ap.add_argument("path", help="Path to the PDF file.")
    ap.add_argument("--out", help="Write JSON to this file instead of stdout.")
    ap.add_argument("--text", action="store_true",
                    help="Extract page text instead of tables.")
    ap.add_argument("--pages", help="Page range to limit to, e.g. '1', '1-3', '2,4'.")
    args = ap.parse_args()

    result = extract(args.path, want_text=args.text, pages=args.pages)
    payload = json.dumps(result, ensure_ascii=False, indent=2)

    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(payload)
        except OSError as e:
            sys.stderr.write(f"Could not write {args.out}: {e}\n")
            sys.exit(1)
        sys.stderr.write(f"Wrote extraction to {args.out}\n")
    else:
        sys.stdout.write(payload)


if __name__ == "__main__":
    main()

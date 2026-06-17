#!/usr/bin/env python3
"""
markitdown_convert.py — the standard BOS document-to-Markdown converter.

Wraps Microsoft MarkItDown so every "read a document" skill has one consistent
path: any file (PDF, Word, Excel, PowerPoint, image, HTML, CSV, JSON, ZIP, ...)
-> clean Markdown that Claude can work on.

Usage:
    python tools/markitdown_convert.py <path-to-file>            # Markdown -> stdout
    python tools/markitdown_convert.py <path-to-file> --out out.md

This is the EXTRACT/READ side only. Writing into a PDF (form fill) is a
different tool — see knowledge/document-tools-method.md and /update-pdf.
"""
import sys
import argparse


INSTALL_HINT = (
    "MarkItDown isn't installed. It's the standard BOS document converter.\n"
    "Install it once:\n"
    "    pip install markitdown          # core formats (pdf, docx, xlsx, pptx, html, csv)\n"
    "    pip install 'markitdown[all]'   # + image OCR / audio extras\n"
)


def convert(path: str) -> str:
    try:
        from markitdown import MarkItDown
    except ImportError:
        sys.stderr.write(INSTALL_HINT)
        sys.exit(2)

    md = MarkItDown()
    try:
        result = md.convert(path)
    except FileNotFoundError:
        sys.stderr.write(f"File not found: {path}\n")
        sys.exit(1)
    except Exception as e:  # noqa: BLE001 — surface the real reason to the operator
        sys.stderr.write(f"Could not convert {path}: {e}\n")
        sys.exit(1)
    return result.text_content


def main() -> None:
    ap = argparse.ArgumentParser(description="Convert any document to Markdown (MarkItDown).")
    ap.add_argument("path", help="Path to the file to convert.")
    ap.add_argument("--out", help="Write Markdown to this file instead of stdout.")
    args = ap.parse_args()

    markdown = convert(args.path)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(markdown)
        sys.stderr.write(f"Wrote Markdown to {args.out}\n")
    else:
        sys.stdout.write(markdown)


if __name__ == "__main__":
    main()

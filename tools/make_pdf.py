#!/usr/bin/env python3
"""make_pdf.py — the doc-lib-set WRITE side for generating a PDF.

The keyless WRITE counterpart to markitdown_convert.py (the READ side). Turns a
small structured document spec Claude produced into a finished PDF an owner can
send or print — a quote, a one-pager, a summary — no account, no network, one
local install.

Usage:
    python tools/make_pdf.py --out brief.pdf --blocks \
        '[{"type":"heading","text":"Pre-call brief"},
          {"type":"paragraph","text":"Acme Pty Ltd — plumbing, Geelong."},
          {"type":"bullet","text":"Ask about their current response time."}]'

    cat doc.json | python tools/make_pdf.py --out brief.pdf

Input shape: a JSON array of blocks. Each block is an object with a "type":
    {"type":"heading","text":"...","level":1}   # level 1-3, default 1
    {"type":"paragraph","text":"..."}            # a body paragraph
    {"type":"bullet","text":"..."}               # a bulleted item

This is part of the doc-lib-set keyless WRITE driver (`doclib`). See
knowledge/document-tools-method.md. No network at runtime.

NOTE: this GENERATES a fresh PDF from data. Filling an existing PDF's form
fields is the READ-then-write path documented under /update-pdf; precise table
extraction FROM a PDF is tools/pdf_tables.py.
"""
import sys
import json
import argparse


INSTALL_HINT = (
    "reportlab isn't installed. It's the doc-lib-set tool for generating PDFs.\n"
    "Install it once:\n"
    "    pip install reportlab\n"
)


def _load_blocks(blocks_arg: str | None) -> list[dict]:
    """Load the blocks JSON from --blocks or stdin; validate it is a list of objects."""
    if blocks_arg is not None:
        raw = blocks_arg
    else:
        raw = sys.stdin.read()
    if not raw.strip():
        sys.stderr.write("No blocks provided (pass --blocks '<json>' or pipe JSON on stdin).\n")
        sys.exit(1)
    try:
        blocks = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Could not parse blocks JSON: {e}\n")
        sys.exit(1)
    if not isinstance(blocks, list) or not all(isinstance(b, dict) for b in blocks):
        sys.stderr.write(
            "Blocks must be a JSON array of objects, e.g. "
            "[{\"type\":\"paragraph\",\"text\":\"...\"}].\n"
        )
        sys.exit(1)
    return blocks


def make_pdf(path: str, blocks: list[dict]) -> None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
        from reportlab.lib.units import mm
    except ImportError:
        sys.stderr.write(INSTALL_HINT)
        sys.exit(2)

    styles = getSampleStyleSheet()
    heading_styles = {1: styles["Heading1"], 2: styles["Heading2"], 3: styles["Heading3"]}

    try:
        story = []
        for block in blocks:
            btype = block.get("type", "paragraph")
            text = block.get("text", "")
            if btype == "heading":
                level = block.get("level", 1)
                try:
                    level = int(level)
                except (TypeError, ValueError):
                    level = 1
                level = max(1, min(level, 3))
                story.append(Paragraph(text, heading_styles[level]))
                story.append(Spacer(1, 2 * mm))
            elif btype == "bullet":
                story.append(
                    ListFlowable(
                        [ListItem(Paragraph(text, styles["Normal"]))],
                        bulletType="bullet",
                    )
                )
            elif btype == "paragraph":
                story.append(Paragraph(text, styles["Normal"]))
                story.append(Spacer(1, 2 * mm))
            else:
                sys.stderr.write(
                    f"Unknown block type {btype!r} (expected heading/paragraph/bullet).\n"
                )
                sys.exit(1)
        doc = SimpleDocTemplate(path, pagesize=A4)
        doc.build(story)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 — surface the real reason to the operator
        sys.stderr.write(f"Could not write {path}: {e}\n")
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate a PDF from JSON blocks (reportlab).")
    ap.add_argument("--out", required=True, help="Path to write the .pdf file to.")
    ap.add_argument("--blocks", help="Blocks as a JSON array of objects. Omit to read JSON from stdin.")
    args = ap.parse_args()

    blocks = _load_blocks(args.blocks)
    make_pdf(args.out, blocks)
    sys.stderr.write(f"Wrote {len(blocks)} block(s) to {args.out}\n")


if __name__ == "__main__":
    main()

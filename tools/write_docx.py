#!/usr/bin/env python3
"""write_docx.py — the doc-lib-set WRITE side for Word (.docx).

The keyless WRITE counterpart to markitdown_convert.py (the READ side). Turns a
small structured document spec Claude produced into a real .docx an owner can
open and send — proposals, policies, job ads, letters — no account, no network,
one local install.

Usage:
    # blocks as JSON on the command line:
    python tools/write_docx.py --out proposal.docx --blocks \
        '[{"type":"heading","text":"Proposal","level":1},
          {"type":"paragraph","text":"Thanks for the opportunity."}]'

    # or pipe the JSON in on stdin:
    cat doc.json | python tools/write_docx.py --out proposal.docx

Input shape: a JSON array of blocks. Each block is an object with a "type":
    {"type":"heading","text":"...","level":1}   # level 0-9, default 1
    {"type":"paragraph","text":"..."}            # a body paragraph
    {"type":"bullet","text":"..."}               # a bulleted list item

This is part of the doc-lib-set keyless WRITE driver (`doclib`). See
knowledge/document-tools-method.md. No network at runtime.
"""
import sys
import json
import argparse


INSTALL_HINT = (
    "python-docx isn't installed. It's the doc-lib-set tool for writing .docx files.\n"
    "Install it once:\n"
    "    pip install python-docx\n"
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


def write_docx(path: str, blocks: list[dict]) -> None:
    try:
        from docx import Document
    except ImportError:
        sys.stderr.write(INSTALL_HINT)
        sys.exit(2)

    doc = Document()
    try:
        for block in blocks:
            btype = block.get("type", "paragraph")
            text = block.get("text", "")
            if btype == "heading":
                level = block.get("level", 1)
                try:
                    level = int(level)
                except (TypeError, ValueError):
                    level = 1
                level = max(0, min(level, 9))
                doc.add_heading(text, level=level)
            elif btype == "bullet":
                doc.add_paragraph(text, style="List Bullet")
            elif btype == "paragraph":
                doc.add_paragraph(text)
            else:
                sys.stderr.write(
                    f"Unknown block type {btype!r} (expected heading/paragraph/bullet).\n"
                )
                sys.exit(1)
        doc.save(path)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 — surface the real reason to the operator
        sys.stderr.write(f"Could not write {path}: {e}\n")
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description="Write a real .docx from JSON blocks (python-docx).")
    ap.add_argument("--out", required=True, help="Path to write the .docx file to.")
    ap.add_argument("--blocks", help="Blocks as a JSON array of objects. Omit to read JSON from stdin.")
    args = ap.parse_args()

    blocks = _load_blocks(args.blocks)
    write_docx(args.out, blocks)
    sys.stderr.write(f"Wrote {len(blocks)} block(s) to {args.out}\n")


if __name__ == "__main__":
    main()

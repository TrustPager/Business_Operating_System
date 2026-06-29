#!/usr/bin/env python3
"""Shared content-rule guards for customer-facing artifacts (doc-lib-set WRITE side).

Enforces the no-em-dash rule MECHANICALLY at the artifact boundary. The write tools
(write_docx / write_xlsx / make_pdf) call assert_no_em_dash() before they build the
file, so a quote, proposal, letter, or spreadsheet can never be written with an em
dash (U+2014) in its content. The 10-persona field test found the model reliably
self-catches em dashes only on a QA re-read; this guard makes the rule self-enforcing
instead of discipline-dependent. On a hit the tool exits non-zero and names the
offending text, so the assistant rewrites that line with a comma, a colon,
parentheses, or separate sentences (better grammar than a blunt auto-replace, and
nothing slips through to a sent document).

Only the em dash is banned. Hyphens (-) in compound words and en dashes in numeric
ranges are fine, so this guard targets U+2014 only and will not false-positive on them.

Pure stdlib, no third-party imports, so the check runs even when the doc library
itself is not installed.
"""
from __future__ import annotations

import sys
from typing import Iterable

EM_DASH = "—"  # the banned sentence-connector character
EXIT_CONTENT_RULE = 3  # distinct from missing-dependency (2) and generic error (1)


def _snippet(text: str, idx: int, pad: int = 30) -> str:
    """A short, single-line context window around the offending character."""
    start = max(0, idx - pad)
    end = min(len(text), idx + pad + 1)
    lead = "..." if start > 0 else ""
    tail = "..." if end < len(text) else ""
    return (lead + text[start:end] + tail).replace("\n", " ").strip()


def find_em_dashes(texts: Iterable[object]) -> list[str]:
    """Return a context snippet for each string value that contains an em dash."""
    offenders: list[str] = []
    for t in texts:
        if not isinstance(t, str):
            continue
        idx = t.find(EM_DASH)
        if idx != -1:
            offenders.append(_snippet(t, idx))
    return offenders


def assert_no_em_dash(texts: Iterable[object], *, source: str = "this output") -> None:
    """Exit non-zero (EXIT_CONTENT_RULE) with a clear, fixable message on any em dash.

    Non-string values are ignored, so callers can pass mixed cell payloads directly.
    Returns cleanly when there are no offenders.
    """
    offenders = find_em_dashes(texts)
    if not offenders:
        return
    sys.stderr.write(
        f"BOS_CONTENT_RULE: em dash found in {source}. Customer-facing output must not "
        "use em dashes. Rewrite the line with a comma, a colon, parentheses, or separate "
        "sentences (hyphens and en-dash number ranges are fine), then write it again. "
        "Offending text:\n"
    )
    for o in offenders:
        sys.stderr.write(f"  - {o}\n")
    sys.exit(EXIT_CONTENT_RULE)

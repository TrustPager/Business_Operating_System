#!/usr/bin/env python3
"""
markitdown_convert.py: the standard BOS document-to-Markdown converter.

Wraps Microsoft MarkItDown so every "read a document" skill has one consistent
path: any file (PDF, Word, Excel, PowerPoint, image, HTML, CSV, JSON, ZIP, ...)
-> clean Markdown that Claude can work on.

Usage:
    python tools/markitdown_convert.py <path-to-file>            # Markdown -> stdout
    python tools/markitdown_convert.py <path-to-file> --out out.md

This is the EXTRACT/READ side only. Writing into a PDF (form fill) is a
different tool (see knowledge/document-tools-method.md and /update-pdf).

Missing-dependency contract (D11, brain-dead self-sufficiency):
On a missing dependency this prints a machine-readable line
``BOS_MISSING_DEP: <pip-spec>`` plus a human line recommending
``python -m pip install <pip-spec>`` (never bare ``pip``), and exits non-zero.
The SKILL layer turns that signal into a detect -> offer -> install-on-yes ->
verify loop; it never tells the owner to run a command. markitdown reads the
common office formats only when the right extra is installed
(``markitdown[docx]`` etc.); without it, the converter silently degrades to a
raw-XML fallback, so we detect the missing extra up front and fail honestly
rather than hand back an unreliable read.
"""
import sys
import argparse
import os


# Map a file extension to the markitdown extra that backs its reader. When the
# extra is absent, markitdown either raises MissingDependencyException or
# silently degrades to a generic ZIP/text fallback. Both are unacceptable for a
# "read this document" workflow, so we detect the missing extra and fail loudly.
_EXT_TO_EXTRA: dict[str, str] = {
    ".docx": "docx",
    ".pdf": "pdf",
    ".xlsx": "xlsx",
    ".xls": "xls",
    ".pptx": "pptx",
}

# The python module each extra installs, used to probe whether the extra is
# really present (markitdown[docx] -> python-docx -> import docx, etc.).
_EXTRA_TO_MODULE: dict[str, str] = {
    "docx": "docx",
    "pdf": "pdfminer",
    "xlsx": "openpyxl",
    "xls": "xlrd",
    "pptx": "pptx",
}


def _missing_dep(spec: str, *, human: str | None = None) -> None:
    """Emit the structured + human missing-dependency signal and exit non-zero.

    ``spec`` is the exact pip spec to install (e.g. ``markitdown[docx]``). The
    SKILL layer keys off the ``BOS_MISSING_DEP:`` prefix.
    """
    sys.stderr.write(f"BOS_MISSING_DEP: {spec}\n")
    detail = human or f"To read this I need {spec}."
    sys.stderr.write(f"{detail} Install it with: python -m pip install {spec}\n")
    sys.exit(2)


def _extra_for(path: str) -> str | None:
    """The markitdown extra needed to read ``path`` by extension, if any."""
    return _EXT_TO_EXTRA.get(os.path.splitext(path)[1].lower())


def _module_present(module: str) -> bool:
    from importlib import util as importutil
    try:
        return importutil.find_spec(module) is not None
    except (ImportError, ValueError):
        return False


def convert(path: str) -> str:
    try:
        from markitdown import MarkItDown
    except ImportError:
        _missing_dep(
            "markitdown[all]",
            human="MarkItDown isn't installed (the standard BOS document reader).",
        )

    # Proactive per-format check: markitdown's office readers need the matching
    # extra. If the file is a known structured format and its extra is missing,
    # fail with the exact spec rather than return a degraded fallback read.
    extra = _extra_for(path)
    if extra is not None:
        module = _EXTRA_TO_MODULE.get(extra)
        if module and not _module_present(module):
            _missing_dep(
                f"markitdown[{extra}]",
                human=f"To read this {os.path.splitext(path)[1]} file I need the "
                      f"document reader (markitdown[{extra}]).",
            )

    md = MarkItDown()
    try:
        result = md.convert(path)
    except FileNotFoundError:
        sys.stderr.write(f"File not found: {path}\n")
        sys.exit(1)
    except Exception as e:  # noqa: BLE001 (inspect for a wrapped missing-dep first)
        spec = _missing_dep_spec_from_exc(e)
        if spec is not None:
            _missing_dep(
                spec,
                human=f"To read this file I need the document reader ({spec}).",
            )
        sys.stderr.write(f"Could not convert {path}: {e}\n")
        sys.exit(1)
    return result.text_content


def _missing_dep_spec_from_exc(exc: Exception) -> str | None:
    """If ``exc`` (a markitdown error) was caused by a missing per-format
    dependency, return the exact ``markitdown[extra]`` spec; else None.

    markitdown catches a converter's MissingDependencyException internally and
    re-raises it wrapped in a FileConversionException whose ``attempts`` carry
    the original exc_info. We dig that out so we can name the precise extra.
    """
    try:
        from markitdown import MissingDependencyException
    except ImportError:
        return None

    # Direct hit (some markitdown versions raise it straight through).
    if isinstance(exc, MissingDependencyException):
        return _spec_from_dep_message(str(exc))

    # Wrapped in FileConversionException.attempts[*].exc_info.
    attempts = getattr(exc, "attempts", None) or []
    for attempt in attempts:
        info = getattr(attempt, "exc_info", None)
        if not info:
            continue
        exc_type, exc_val = info[0], info[1]
        if exc_type is not None and issubclass(exc_type, MissingDependencyException):
            spec = _spec_from_dep_message(str(exc_val))
            if spec:
                return spec
    return None


def _spec_from_dep_message(message: str) -> str | None:
    """Pull the ``markitdown[<extra>]`` spec out of markitdown's missing-dep text.

    markitdown's message reads '... include the optional dependency [<feature>]
    or [all] ...'. We map the feature back to a clean pip spec.
    """
    import re
    m = re.search(r"pip install markitdown\[([a-z0-9]+)\]", message)
    if m:
        return f"markitdown[{m.group(1)}]"
    # Fallback: the message names the feature in brackets near "optional dependency".
    m = re.search(r"optional dependency \[([a-z0-9]+)\]", message)
    if m:
        return f"markitdown[{m.group(1)}]"
    return None


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

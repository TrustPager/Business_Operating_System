#!/usr/bin/env python3
"""Find .map()-rendered content in an Astro site that the website editor
can't select or edit.

When to use:
  - Before doing an "editor pass" on a client website repo (TrustPager's
    click-to-edit bridge script only selects elements carrying a literal
    data-tp-id="...", one per element in the SOURCE FILE).
  - After adding new .map()-driven sections to a site, to catch the gap
    before a client notices "why can't I edit this card".

What it does:
  - Walks every .astro file under <site>/src/.
  - Finds each .map( ... ) call and inspects its callback body for three
    known-broken shapes: a computed data-tp-id (data-tp-id={...} — never
    matches the editor's literal string search, so clicking selects it but
    saving the edit fails with "could not find element"), a literal
    data-tp-id INSIDE the loop (renders the same id on every iteration —
    only the first instance is ever editable), or no data-tp-id at all
    (nothing in the loop is selectable).
  - Prints one line per finding: file, loop line number, and the verdict.
    Does NOT auto-fix — unrolling a loop into individual literal blocks
    needs a human/AI judgement call per site (naming, which nested spans
    to tag), same as was done for BOS-Design.

Usage:
  python tools/check-editable-elements.py "[local-path]/Websites/[client]-Design"
  python tools/check-editable-elements.py "[local-path]/Websites/[client]-Design" --json
  python tools/check-editable-elements.py --all "[local-path]/Websites"
"""
import argparse
import json
import re
import sys
from pathlib import Path

COMPUTED_ID_RE = re.compile(r'data-tp-id\s*=\s*\{')
LITERAL_ID_RE = re.compile(r'data-tp-id\s*=\s*"[^"]*"')
MAP_CALL_RE = re.compile(r'\.map\s*\(')


def find_matching_paren(text, open_paren_index):
    """Given the index of a '(' , return the index of its matching ')'
    (the char right after it), skipping brackets found inside string/
    template literals so a stray '(' or ')' in copy text doesn't desync
    the count. Heuristic, not a real parser — good enough to bound a
    .map(...) call for a regex pass on its contents."""
    depth = 0
    i = open_paren_index
    in_string = None  # None, or the quote char currently inside
    n = len(text)
    while i < n:
        ch = text[i]
        if in_string:
            if ch == '\\':
                i += 2
                continue
            if ch == in_string:
                in_string = None
        elif ch in ('"', "'", '`'):
            in_string = ch
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n  # unbalanced — return end of file rather than crash


JSX_COMMENT_RE = re.compile(r'\{/\*.*?\*/\}', re.DOTALL)
HTML_COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)


def strip_comments(text):
    """Blank out (not remove — keeps line numbers accurate) JSX {/* ... */}
    and HTML <!-- ... --> comments so prose mentioning ".map()" or
    "data-tp-id" inside a comment doesn't get mistaken for real markup."""
    def blank(m):
        return re.sub(r'[^\n]', ' ', m.group(0))
    text = JSX_COMMENT_RE.sub(blank, text)
    text = HTML_COMMENT_RE.sub(blank, text)
    return text


def check_file(path):
    text = strip_comments(path.read_text(encoding='utf-8'))
    findings = []
    for m in MAP_CALL_RE.finditer(text):
        call_start = m.start()
        open_paren = m.end() - 1
        call_end = find_matching_paren(text, open_paren)
        body = text[open_paren:call_end]
        line_no = text.count('\n', 0, call_start) + 1

        has_computed = bool(COMPUTED_ID_RE.search(body))
        has_literal = bool(LITERAL_ID_RE.search(body))

        if has_computed:
            verdict = 'BROKEN: computed data-tp-id (data-tp-id={...}) — never matches the editor\'s literal string search; clicking selects it but saving an edit fails'
        elif has_literal:
            verdict = 'BROKEN: literal data-tp-id written inside the loop — renders the same id on every iteration, only the first card is ever editable'
        else:
            verdict = 'GAP: no data-tp-id anywhere in this loop — nothing rendered here is selectable'

        # Best-effort snippet: the array/expression the loop is over, e.g.
        # "steps" in "steps.map(...)" — read backwards from call_start.
        j = call_start - 1
        while j >= 0 and (text[j].isalnum() or text[j] in '_.[]'):
            j -= 1
        source_expr = text[j + 1:call_start].strip()

        findings.append({
            'file': str(path),
            'line': line_no,
            'source': source_expr or '(unknown)',
            'verdict': verdict,
        })
    return findings


def scan_site(site_root):
    site_root = Path(site_root)
    src = site_root / 'src'
    if not src.exists():
        return None
    all_findings = []
    for astro_file in sorted(src.rglob('*.astro')):
        all_findings.extend(check_file(astro_file))
    return all_findings


def main():
    parser = argparse.ArgumentParser(description='Find .map()-rendered content an Astro site\'s editor can\'t select.')
    parser.add_argument('path', help='Path to a single site repo, or (with --all) a parent folder of site repos')
    parser.add_argument('--all', action='store_true', help='Treat <path> as a parent folder and scan every immediate subfolder that has a src/ dir')
    parser.add_argument('--json', action='store_true', help='Emit JSON instead of a human-readable report')
    args = parser.parse_args()

    root = Path(args.path)
    sites = [d for d in sorted(root.iterdir()) if d.is_dir()] if args.all else [root]

    report = {}
    for site in sites:
        findings = scan_site(site)
        if findings is None:
            continue
        report[site.name] = findings

    if args.json:
        print(json.dumps(report, indent=2))
        return

    total = 0
    for site_name, findings in report.items():
        print(f'\n=== {site_name} ===')
        if not findings:
            print('  No .map() loops found (or none under src/).')
            continue
        for f in findings:
            rel = Path(f['file']).name
            print(f"  {rel}:{f['line']}  {f['source']}.map(...)")
            print(f"    -> {f['verdict']}")
            total += 1
    print(f'\n{total} loop(s) flagged across {len(report)} site(s).')


if __name__ == '__main__':
    main()

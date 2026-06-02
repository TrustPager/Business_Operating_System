#!/usr/bin/env python3
"""Show the BOS write journal — the audit trail of every change BOS made.

Every write BOS issues to your TrustPager workspace (create / update / send /
trigger, and anything queued for approval) is appended to a local journal at
~/.claude/bos-journal/YYYY-MM-DD.jsonl by the shared API library. Reads are
NOT journaled. This is what makes the "BOS logs what it did" promise real and
inspectable — nothing leaves your machine, and you can always see the trail.

When to use:
- "What did BOS change today / this week?"
- "Did that send actually go out, or is it waiting on approval?"
- Reviewing what a skill did before you trust it with more.
- Handing a clean change-list to a teammate or your own records.

What each line records:
    ts, method (POST/PATCH), path, status (ok | approval_pending | error),
    result_id, approval_id, error (if any), body_summary (truncated payload).

Usage:
    python tools/journal.py                 # today's writes
    python tools/journal.py --today         # today's writes (explicit)
    python tools/journal.py --since 2026-06-01
    python tools/journal.py --tail 20       # last N entries across all days
    python tools/journal.py --grep send_    # only paths containing a string
    python tools/journal.py --errors        # only failed writes
    python tools/journal.py --path          # print the journal directory and exit

Disable journaling entirely by setting BOS_JOURNAL=0 in your environment.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import JOURNAL_DIR, force_utf8_stdout  # noqa: E402


STATUS_GLYPH = {"ok": "✓", "approval_pending": "⧗", "error": "✗"}


def _iter_files(since: str | None) -> list[Path]:
    """Return journal files (oldest first), optionally filtered to >= since (YYYY-MM-DD)."""
    if not JOURNAL_DIR.exists():
        return []
    files = sorted(JOURNAL_DIR.glob("*.jsonl"))
    if since:
        files = [f for f in files if f.stem >= since]
    return files


def _read_entries(files: list[Path]) -> list[dict]:
    out: list[dict] = []
    for f in files:
        try:
            for line in f.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        except OSError:
            continue
    return out


def _fmt(entry: dict) -> str:
    glyph = STATUS_GLYPH.get(entry.get("status", ""), "?")
    ts = entry.get("ts", "")
    # Trim to HH:MM:SS for readability
    when = ts[11:19] if len(ts) >= 19 else ts
    method = (entry.get("method") or "").ljust(5)
    path = entry.get("path") or ""
    tail = ""
    if entry.get("status") == "approval_pending":
        tail = f"  → approval {entry.get('approval_id')}"
    elif entry.get("status") == "error":
        tail = f"  → {(entry.get('error') or '').splitlines()[0][:80]}"
    elif entry.get("result_id"):
        tail = f"  → id {entry.get('result_id')}"
    return f"{glyph} {when}  {method} {path}{tail}"


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--today", action="store_true", help="Show today's writes (default)")
    parser.add_argument("--since", metavar="YYYY-MM-DD", help="Show writes on/after this date")
    parser.add_argument("--tail", type=int, metavar="N", help="Show the last N entries across all days")
    parser.add_argument("--grep", metavar="STR", help="Only entries whose path contains STR")
    parser.add_argument("--errors", action="store_true", help="Only failed writes")
    parser.add_argument("--path", action="store_true", help="Print the journal directory and exit")
    args = parser.parse_args()

    if args.path:
        print(JOURNAL_DIR)
        return 0

    if args.since:
        files = _iter_files(args.since)
    elif args.tail:
        files = _iter_files(None)
    else:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        files = _iter_files(today)

    entries = _read_entries(files)
    if args.grep:
        entries = [e for e in entries if args.grep in (e.get("path") or "")]
    if args.errors:
        entries = [e for e in entries if e.get("status") == "error"]
    entries.sort(key=lambda e: e.get("ts") or "")
    if args.tail:
        entries = entries[-args.tail:]

    if not entries:
        where = "today" if not (args.since or args.tail) else "the selected range"
        print(f"No BOS writes journaled for {where}.")
        print(f"(Journal dir: {JOURNAL_DIR} — set BOS_JOURNAL=0 to disable journaling.)")
        return 0

    ok = sum(1 for e in entries if e.get("status") == "ok")
    pend = sum(1 for e in entries if e.get("status") == "approval_pending")
    err = sum(1 for e in entries if e.get("status") == "error")
    print(f"BOS write journal — {len(entries)} writes  "
          f"({ok} done, {pend} awaiting approval, {err} failed)\n")
    for e in entries:
        print(_fmt(e))
    return 0


if __name__ == "__main__":
    sys.exit(main())

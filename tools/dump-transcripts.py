#!/usr/bin/env python3
"""Dump ≥5-minute call & meeting transcripts as readable Markdown.

When to use:
- You're building a brand voice / nurture sequence / positioning doc and
  want to mine what your customers actually say (verbatim) instead of
  inventing language for them.
- You want a frozen Markdown snapshot of recent customer conversations
  that an AI can read offline.
- You want to audit which prospects talked about what, in their words.

What it dumps:
- Markdown files per transcript: `<date>_<duration>min_<who>_<id8>.md`
- Calls go to `<out>/calls/`, meetings go to `<out>/meetings/`.
- Each file has YAML frontmatter (id, type, occurred_at, duration_minutes,
  title, participants, linked deal + contact) and a cleaned transcript body.
- `_index.json` summarising everything dumped.

WebVTT timestamps + cue numbers are stripped; speaker lines are preserved.
Most Twilio phone calls between humans are NOT auto-transcribed — only
Recall AI Notetaker meetings and Retell voice-agent calls have rich text
to dump. The tool silently skips transcripts with empty bodies.

Usage:
    python tools/dump-transcripts.py
    python tools/dump-transcripts.py --min-duration 600   # 10 minutes+
    python tools/dump-transcripts.py --target 20
    python tools/dump-transcripts.py --out ./conversations
    python tools/dump-transcripts.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, force_utf8_stdout,
)


SKILL = "dump-transcripts"

# Map API `type` value -> output folder bucket.
CALL_TYPES = {"phone_call", "call"}
MEETING_TYPES = {"meeting"}


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def list_complete_transcripts(page_size: int, max_pages: int) -> Iterable[dict]:
    """Yield every `transcription_status=complete` transcript, newest first.
    Lightweight list rows — no transcript_text included."""
    cursor: str | None = None
    pages = 0
    while pages < max_pages:
        params: dict[str, Any] = {
            "limit": page_size,
            "transcription_status": "complete",
        }
        if cursor:
            params["after"] = cursor
        body = api_get("transcripts", **params)
        if not isinstance(body, dict):
            return
        items = body.get("data") or []
        if not items:
            return
        yield from items
        pagination = body.get("pagination") or {}
        if not pagination.get("has_more"):
            return
        cursor = pagination.get("next_cursor")
        if not cursor:
            return
        pages += 1


def fetch_detail(t_id: str) -> dict:
    body = api_get(f"transcripts/{t_id}")
    if isinstance(body, dict) and "data" in body and isinstance(body["data"], dict):
        return body["data"]
    return body if isinstance(body, dict) else {}


def slugify(s: str, max_len: int = 40) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return (s or "untitled")[:max_len]


def vtt_to_markdown(vtt_text: str) -> str:
    """Strip WebVTT cue numbers + timestamps. Keep speaker lines.
    Output is plain Markdown — readable as a play script."""
    if not vtt_text:
        return ""
    out: list[str] = []
    for line in vtt_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped == "WEBVTT":
            continue
        if stripped.startswith("NOTE"):
            continue
        if stripped.isdigit():
            continue
        if "-->" in stripped and re.match(r"^\d{2}:\d{2}", stripped):
            continue
        out.append(stripped)
    deduped: list[str] = []
    for line in out:
        if deduped and deduped[-1] == line:
            continue
        deduped.append(line)
    return "\n\n".join(deduped)


def extract_body(detail: dict) -> tuple[str, str | None]:
    """Returns (markdown_body, summary_or_None).
    `transcript_text` is usually a JSON-encoded blob:
        {"type": "...", "transcript_vtt": "WEBVTT...", "summary": "..."}
    Some sources may store plain text instead."""
    raw = detail.get("transcript_text") or ""
    if not raw:
        return "", None
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            vtt = parsed.get("transcript_vtt") or parsed.get("vtt") or ""
            summary = parsed.get("summary")
            if vtt:
                return vtt_to_markdown(vtt), summary
            plain = parsed.get("transcript") or parsed.get("text") or ""
            if plain:
                return plain.strip(), summary
            return "", summary
    except (json.JSONDecodeError, TypeError):
        pass
    if "WEBVTT" in raw or "-->" in raw:
        return vtt_to_markdown(raw), None
    return raw.strip(), None


def yaml_frontmatter(d: dict) -> str:
    """Minimal hand-rolled YAML — quotes anything with special chars."""

    def fmt(v: Any) -> str:
        if v is None:
            return "null"
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, (int, float)):
            return str(v)
        if isinstance(v, (list, dict)):
            return json.dumps(v, ensure_ascii=False, default=str)
        s = str(v)
        if any(c in s for c in (':', '#', '\n', '"', '\\')):
            return json.dumps(s, ensure_ascii=False)
        return s

    lines = ["---"]
    for k, v in d.items():
        lines.append(f"{k}: {fmt(v)}")
    lines.append("---")
    return "\n".join(lines)


def build_filename(t: dict) -> str:
    occurred = t.get("occurred_at") or ""
    date_part = occurred[:10] if occurred else "0000-00-00"
    dur = t.get("duration_seconds") or 0
    mins = dur // 60
    linked = t.get("linked_entities") or {}
    deals = linked.get("deals") or []
    contacts = linked.get("contacts") or []
    who = ""
    if deals and deals[0].get("name"):
        who = deals[0]["name"]
    elif contacts:
        c = contacts[0]
        who = (
            " ".join(filter(None, [c.get("first_name"), c.get("last_name")])).strip()
            or c.get("email")
            or ""
        )
    if not who:
        who = t.get("title") or ""
    return f"{date_part}_{mins:02d}min_{slugify(who)}_{t['id'][:8]}.md"


def main() -> None:
    force_utf8_stdout()
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--out", help="Output folder (default: ./transcripts/<UTC-date>/)")
    ap.add_argument(
        "--min-duration",
        type=int,
        default=300,
        help="Min duration in seconds (default: 300 = 5 min)",
    )
    ap.add_argument(
        "--target",
        type=int,
        default=30,
        help="Target count per bucket (calls / meetings). Default: 30.",
    )
    ap.add_argument(
        "--max-pages",
        type=int,
        default=20,
        help="Max list pages to scan (100 transcripts each, default: 20 = up to 2000).",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Show resolved plan + output paths, then exit",
    )
    args = ap.parse_args()

    out_root = (
        Path(args.out)
        if args.out
        else Path("transcripts") / datetime.now(timezone.utc).strftime("%Y-%m-%d")
    )
    calls_dir = out_root / "calls"
    meetings_dir = out_root / "meetings"

    log(f"out:    {out_root}")
    log(f"filter: duration_seconds >= {args.min_duration}")
    log(f"target: up to {args.target} calls + {args.target} meetings")

    if args.dry_run:
        log("(dry-run — no writes)")
        print(str(out_root))
        return

    started_at = datetime.now(timezone.utc).isoformat()

    log("\n[1/2] scanning list endpoint...")
    calls: list[dict] = []
    meetings: list[dict] = []
    scanned = 0
    try:
        for item in list_complete_transcripts(
            page_size=100, max_pages=args.max_pages
        ):
            scanned += 1
            dur = item.get("duration_seconds") or 0
            if dur < args.min_duration:
                continue
            ttype = item.get("type")
            if ttype in CALL_TYPES and len(calls) < args.target:
                calls.append(item)
            elif ttype in MEETING_TYPES and len(meetings) < args.target:
                meetings.append(item)
            if len(calls) >= args.target and len(meetings) >= args.target:
                break
    except BOSError as err:
        emit_error_and_exit(str(err), skill=SKILL)

    log(
        f"  scanned {scanned} transcripts -> {len(calls)} calls, {len(meetings)} meetings ≥ min duration"
    )

    calls_dir.mkdir(parents=True, exist_ok=True)
    meetings_dir.mkdir(parents=True, exist_ok=True)

    log("\n[2/2] fetching detail + writing markdown...")
    index: list[dict[str, Any]] = []
    skipped_empty = 0

    def process(group: list[dict], folder: Path, label: str) -> None:
        nonlocal skipped_empty
        for i, light in enumerate(group, 1):
            tid = light["id"]
            try:
                detail = fetch_detail(tid)
            except BOSError as e:
                log(f"  [{label} {i}/{len(group)}] FAILED {tid}: {e}")
                continue
            body, summary = extract_body(detail)
            if not body.strip():
                skipped_empty += 1
                log(f"  [{label} {i}/{len(group)}] empty transcript_text — skip {tid[:8]}")
                continue
            linked = detail.get("linked_entities") or {}
            fm = {
                "id": detail["id"],
                "type": detail.get("type"),
                "source": detail.get("source"),
                "occurred_at": detail.get("occurred_at"),
                "duration_seconds": detail.get("duration_seconds"),
                "duration_minutes": round((detail.get("duration_seconds") or 0) / 60, 1),
                "title": detail.get("title"),
                "participants": detail.get("participants") or [],
                "linked_deals": [d.get("name") for d in (linked.get("deals") or [])],
                "linked_contacts": [
                    " ".join(filter(None, [c.get("first_name"), c.get("last_name")])).strip()
                    or c.get("email")
                    for c in (linked.get("contacts") or [])
                ],
                "recording_url": detail.get("recording_url"),
                "booking_id": detail.get("booking_id"),
            }
            outpath = folder / build_filename(detail)
            parts = [yaml_frontmatter(fm), ""]
            if summary:
                parts += [f"## Summary (auto-generated)", "", summary, ""]
            parts += [f"## Transcript", "", body, ""]
            outpath.write_text("\n".join(parts), encoding="utf-8")
            rel = outpath.relative_to(out_root)
            index.append(
                {
                    "file": str(rel).replace("\\", "/"),
                    "id": detail["id"],
                    "type": detail.get("type"),
                    "occurred_at": detail.get("occurred_at"),
                    "duration_seconds": detail.get("duration_seconds"),
                    "title": detail.get("title"),
                    "linked_deals": fm["linked_deals"],
                    "linked_contacts": fm["linked_contacts"],
                }
            )
            if i % 5 == 0 or i == len(group):
                log(f"  [{label}] {i}/{len(group)}")

    process(calls, calls_dir, "calls")
    process(meetings, meetings_dir, "meetings")

    index_path = out_root / "_index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(
        json.dumps(
            {
                "skill": SKILL,
                "started_at": started_at,
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "min_duration_seconds": args.min_duration,
                "counts": {
                    "calls": sum(1 for x in index if x["type"] in CALL_TYPES),
                    "meetings": sum(1 for x in index if x["type"] in MEETING_TYPES),
                    "skipped_empty": skipped_empty,
                    "scanned_list_items": scanned,
                },
                "transcripts": index,
            },
            indent=2,
            default=str,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    log(f"\nWrote {len(index)} transcripts ({skipped_empty} skipped — empty text).")
    print(str(out_root))


if __name__ == "__main__":
    main()

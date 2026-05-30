#!/usr/bin/env python3
"""Lead triage — find new inbound leads + score by fit + propose category.

Pulls every new lead from the last N hours across all inbound sources:
- Form submissions (new ones, not yet processed)
- Inbound email threads (first message, not yet replied)
- Inbound SMS conversations (no outbound response yet)
- Opportunities created in window with status "lead" / "new"

For each lead, computes a fit score 0-100 based on:
- Has phone number          (+25)
- Has email                 (+15)
- Has company / job title   (+15)
- Message length ≥ 80 chars (+20)
- Source quality (form > email > sms > unknown)  (0-25)

Returns one record per lead, ranked by score descending.

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/lead-triage/fetch.py
    python skills/lead-triage/fetch.py --hours 24
"""

from __future__ import annotations

import argparse
import sys
from datetime import timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, parallel_get, parse_iso, resolve_path,
)


SKILL = "lead-triage"


def _score(lead: dict[str, Any]) -> int:
    s = 0
    if lead.get("phone"):
        s += 25
    if lead.get("email"):
        s += 15
    if lead.get("company") or lead.get("job_title"):
        s += 15
    msg = lead.get("message") or ""
    if len(msg) >= 80:
        s += 20
    elif len(msg) >= 30:
        s += 10
    src = lead.get("source") or ""
    src_quality = {"form": 25, "email": 18, "sms": 10, "call": 8, "manual": 5}.get(src, 0)
    s += src_quality
    return min(s, 100)


def _category(score: int, msg: str) -> str:
    msg_lower = (msg or "").lower()
    spam_signals = [
        "seo services", "web design", "partnership opportunity",
        "increase your traffic", "guest post", "backlink",
    ]
    if any(sig in msg_lower for sig in spam_signals):
        return "disqualify"
    if score >= 70:
        return "fast_track"
    if score >= 40:
        return "nurture"
    return "cold"


def fetch_and_digest(hours: int, quiet: bool) -> dict[str, Any]:
    now = now_utc()
    cutoff = now - timedelta(hours=hours)
    cutoff_iso = cutoff.isoformat()

    log(SKILL, f"fetching inbound leads from last {hours}h...", quiet=quiet)

    paths = {
        "form_submissions": resolve_path("forms", path_contains="submissions"),
        "email_threads":    resolve_path("email", path_contains="threads"),
        "sms_convos":       resolve_path("sms", path_contains="conversations"),
        "opportunities":    resolve_path("opportunities"),
    }

    calls = [
        (paths["form_submissions"], {"limit": 100, "after": cutoff_iso}),
        (paths["email_threads"],    {"limit": 100, "after": cutoff_iso, "direction": "inbound"}),
        (paths["sms_convos"],       {"limit": 100, "after": cutoff_iso}),
        (paths["opportunities"],    {"limit": 100, "after": cutoff_iso, "status": "open"}),
    ]
    results = parallel_get(calls)

    leads: list[dict[str, Any]] = []

    # Form submissions
    for fs in results.get(paths["form_submissions"], {}).get("data", []):
        data = fs.get("form_data") or fs.get("submission_data") or {}
        # Build a flat message from any "message", "notes", "comments" fields
        message_keys = ["message", "notes", "comments", "enquiry", "details", "description"]
        msg = ""
        for k in message_keys:
            if data.get(k):
                msg = str(data[k])
                break
        leads.append({
            "kind": "form_submission",
            "source": "form",
            "id": fs.get("id"),
            "received_at": fs.get("created_at"),
            "first_name": data.get("first_name") or data.get("name") or "",
            "last_name": data.get("last_name") or "",
            "email": data.get("email") or fs.get("contact_email"),
            "phone": data.get("phone") or fs.get("contact_phone"),
            "company": data.get("company") or "",
            "job_title": data.get("job_title") or "",
            "message": msg,
            "form_name": fs.get("form_name") or fs.get("template_name"),
            "contact_id": fs.get("contact_id"),
            "opportunity_id": fs.get("deal_id") or fs.get("opportunity_id"),
        })

    # Email threads — inbound, no reply yet
    for et in results.get(paths["email_threads"], {}).get("data", []):
        replied = et.get("replied") or et.get("we_replied")
        if replied:
            continue
        latest = et.get("latest_message") or {}
        leads.append({
            "kind": "email_thread",
            "source": "email",
            "id": et.get("id"),
            "received_at": et.get("created_at") or et.get("last_inbound_at"),
            "first_name": (et.get("contact") or {}).get("first_name", ""),
            "last_name": (et.get("contact") or {}).get("last_name", ""),
            "email": (et.get("contact") or {}).get("email") or et.get("from_email"),
            "phone": (et.get("contact") or {}).get("phone"),
            "company": (et.get("contact") or {}).get("company_name", ""),
            "job_title": "",
            "message": latest.get("plain_text") or latest.get("subject") or "",
            "subject": et.get("subject"),
            "contact_id": (et.get("contact") or {}).get("id"),
            "opportunity_id": et.get("deal_id"),
        })

    # SMS conversations — inbound, no outbound yet
    for sc in results.get(paths["sms_convos"], {}).get("data", []):
        if sc.get("we_replied") or (sc.get("outbound_count") or 0) > 0:
            continue
        leads.append({
            "kind": "sms_conversation",
            "source": "sms",
            "id": sc.get("id"),
            "received_at": sc.get("created_at") or sc.get("last_inbound_at"),
            "first_name": (sc.get("contact") or {}).get("first_name", ""),
            "last_name": (sc.get("contact") or {}).get("last_name", ""),
            "email": (sc.get("contact") or {}).get("email"),
            "phone": (sc.get("contact") or {}).get("phone") or sc.get("from_phone"),
            "company": "",
            "job_title": "",
            "message": sc.get("first_message_body") or sc.get("last_inbound_body") or "",
            "contact_id": (sc.get("contact") or {}).get("id"),
            "opportunity_id": sc.get("deal_id"),
        })

    # Opportunities created in window without prior contact — handled as "manual" leads
    for op in results.get(paths["opportunities"], {}).get("data", []):
        created = parse_iso(op.get("created_at"))
        if not created or created < cutoff:
            continue
        if op.get("contact_id"):
            # Skip if a form/email/sms above already captured this opp
            if any(l.get("opportunity_id") == op.get("id") for l in leads):
                continue
        leads.append({
            "kind": "opportunity",
            "source": "manual",
            "id": op.get("id"),
            "received_at": op.get("created_at"),
            "first_name": "",
            "last_name": op.get("name") or "",
            "email": None,
            "phone": None,
            "company": "",
            "job_title": "",
            "message": op.get("description") or "",
            "contact_id": op.get("contact_id"),
            "opportunity_id": op.get("id"),
        })

    # Score + categorize
    for lead in leads:
        lead["score"] = _score(lead)
        lead["category"] = _category(lead["score"], lead.get("message", ""))

    leads.sort(key=lambda l: (l["score"], l.get("received_at") or ""), reverse=True)

    by_category: dict[str, int] = {"fast_track": 0, "nurture": 0, "cold": 0, "disqualify": 0}
    for l in leads:
        by_category[l["category"]] = by_category.get(l["category"], 0) + 1

    return {
        "generated_at": now.isoformat(),
        "window_hours": hours,
        "headline": {
            "total_leads": len(leads),
            "by_category": by_category,
            "by_source": {
                "form":   sum(1 for l in leads if l["source"] == "form"),
                "email":  sum(1 for l in leads if l["source"] == "email"),
                "sms":    sum(1 for l in leads if l["source"] == "sms"),
                "manual": sum(1 for l in leads if l["source"] == "manual"),
            },
            "with_opportunity": sum(1 for l in leads if l.get("opportunity_id")),
            "without_opportunity": sum(1 for l in leads if not l.get("opportunity_id")),
        },
        "items": leads,
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--hours", type=int, default=48,
                        help="How far back to look (default 48 hours)")
    parser.add_argument("--json-only", action="store_true",
                        help="Suppress stderr progress logs")
    args = parser.parse_args()

    try:
        digest = fetch_and_digest(args.hours, quiet=args.json_only)
        emit_json(digest)
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())

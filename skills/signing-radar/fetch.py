#!/usr/bin/env python3
"""signing-radar — pull every signing envelope into one funnel + follow-up digest.

Owners send documents for signing and then lose track of who's where. This
fetcher returns a single JSON document Claude turns into a follow-up report:
the sent → opened → signed funnel, plus the two follow-up-gold buckets —
"opened but not signed" (engaged, holding) and "sent but never opened, going
stale" (chase or it dies).

All read-only (list_signing_envelopes). Auth: TRUSTPAGER_API_KEY env var or
~/.claude/bos.json.

Usage:
    python skills/signing-radar/fetch.py
    python skills/signing-radar/fetch.py --stale-days 5
    python skills/signing-radar/fetch.py --json-only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, paginate, parse_iso, days_since, resolve_path,
)

SKILL = "signing-radar"

# Envelope/recipient statuses we treat as "opened but not yet signed" — the
# hottest follow-up set. Workspaces vary on the exact label, so match a set.
OPENED_NOT_SIGNED = {"viewed", "opened"}
DONE = {"completed", "signed"}
DEAD = {"voided", "declined", "expired"}


def _age_days(env: dict, now) -> float | None:
    """Days since the envelope was sent (fallback: created)."""
    ts = env.get("sent_at") or env.get("created_at") or env.get("updated_at")
    dt = parse_iso(ts) if ts else None
    return days_since(dt, now) if dt else None


def fetch(stale_days: int, quiet: bool) -> dict:
    now = now_utc()
    log(SKILL, "listing signing envelopes...", quiet=quiet)

    envelopes = list(paginate(resolve_path("signing/envelopes"), limit=100, max_pages=20))

    funnel = {"sent": 0, "opened": 0, "signed": 0, "completed": 0,
              "declined": 0, "voided": 0, "expired": 0, "other": 0}
    opened_not_signed: list[dict] = []
    sent_never_opened_stale: list[dict] = []
    declined: list[dict] = []
    recently_completed: list[dict] = []

    for env in envelopes:
        status = (env.get("status") or "").lower()
        age = _age_days(env, now)
        row = {
            "envelope_id": env.get("id"),
            "document_title": env.get("document_title") or env.get("template_name") or "(untitled)",
            "deal_id": env.get("deal_id"),
            "status": status,
            "age_days": round(age, 1) if age is not None else None,
            "signer_email": env.get("signer_email"),
            "signer_name": env.get("signer_name"),
        }

        # Funnel tally (coarse — envelope-level).
        if status in OPENED_NOT_SIGNED:
            funnel["opened"] += 1
            opened_not_signed.append(row)
        elif status == "signed":
            funnel["signed"] += 1
        elif status == "completed":
            funnel["completed"] += 1
            if age is not None and age <= 7:
                recently_completed.append(row)
        elif status == "declined":
            funnel["declined"] += 1
            row["decline_reason"] = env.get("decline_reason")
            declined.append(row)
        elif status == "voided":
            funnel["voided"] += 1
        elif status == "expired":
            funnel["expired"] += 1
        elif status == "sent":
            funnel["sent"] += 1
            if age is not None and age >= stale_days:
                sent_never_opened_stale.append(row)
        else:
            funnel["other"] += 1

    # Sort the follow-up buckets oldest-first (most urgent).
    opened_not_signed.sort(key=lambda r: r["age_days"] or 0, reverse=True)
    sent_never_opened_stale.sort(key=lambda r: r["age_days"] or 0, reverse=True)

    return {
        "skill": SKILL,
        "generated_at": now.isoformat(),
        "stale_days_threshold": stale_days,
        "total_envelopes": len(envelopes),
        "funnel": funnel,
        "opened_not_signed": opened_not_signed,            # follow-up GOLD
        "sent_never_opened_stale": sent_never_opened_stale,  # chase or it dies
        "declined": declined,
        "recently_completed": recently_completed,
    }


def main() -> None:
    force_utf8_stdout()
    ap = argparse.ArgumentParser(description="Signing envelope funnel + follow-up digest")
    ap.add_argument("--stale-days", type=int, default=5,
                    help="Flag 'sent but never opened' once older than this many days (default 5)")
    ap.add_argument("--json-only", action="store_true", help="Suppress progress logs")
    args = ap.parse_args()
    try:
        emit_json(fetch(args.stale_days, quiet=args.json_only))
    except BOSError as e:
        emit_error_and_exit(e)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Dump your TrustPager workspace as JSON — for marketing-strategy analysis.

When to use:
- You're about to build a brand voice / nurture sequence / positioning doc
  and want a frozen snapshot of your CRM to work from.
- An AI is going to read your workspace state and you want it pre-fetched
  to a folder so the AI can read files instead of poking the API live.
- You want to audit what's in your workspace (pipelines, automations, auto
  queues, opportunities, companies, contacts) in one offline session.

What it dumps (one JSON file per resource):
- `pipelines.json`             — every pipeline (id, name, position, etc).
- `pipeline_stages.json`       — every stage, grouped by pipeline_id.
- `automations.json`           — every automation WITH inline triggers + actions
                                 (so you can see actual email body, subject,
                                 SMS body, task templates, etc. — not just names).
- `auto_queues.json`           — every auto queue WITH inline steps.
- `opportunities.json`         — every opportunity with `expand=contact`.
- `companies.json`             — every company.
- `companies-customers.json`   — same list filtered to is_customer=true.
- `contacts.json`              — most recent N contacts (configurable, default 500).
- `_manifest.json`             — counts + timestamps for the dump itself.

All read-only. No writes, no approvals queue, no API credits charged.

Output folder defaults to `./crm-bundle/<UTC-date>/` so re-running creates a
new timestamped snapshot instead of overwriting the last one.

Usage:
    python tools/dump-crm-bundle.py
    python tools/dump-crm-bundle.py --out ./my-bundle
    python tools/dump-crm-bundle.py --resources opportunities,automations
    python tools/dump-crm-bundle.py --contacts-limit 200
    python tools/dump-crm-bundle.py --dry-run        # print plan, don't fetch
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, force_utf8_stdout, paginate,
)


SKILL = "dump-crm-bundle"
DEFAULT_RESOURCES = [
    "pipelines",
    "automations",
    "auto_queues",
    "opportunities",
    "companies",
    "contacts",
]


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, default=str, ensure_ascii=False),
        encoding="utf-8",
    )


def fetch_pipelines() -> tuple[list[dict], dict[str, list[dict]]]:
    """List every pipeline, then fetch stages for each."""
    log("- pipelines + stages...")
    pipelines = paginate("pipelines")
    stages_by_pipeline: dict[str, list[dict]] = {}
    for p in pipelines:
        pid = p["id"]
        body = api_get(f"pipelines/{pid}/stages")
        if isinstance(body, dict) and "data" in body and isinstance(body["data"], list):
            stages_by_pipeline[pid] = body["data"]
        elif isinstance(body, list):
            stages_by_pipeline[pid] = body
        else:
            stages_by_pipeline[pid] = []
    return pipelines, stages_by_pipeline


def fetch_automations(deep: bool = True) -> list[dict]:
    """List every automation. If deep=True (default), follow up with
    GET /automations/{id} per row so the inline triggers + actions
    (with full email/SMS body, task templates, etc.) are included."""
    log("- automations (deep)..." if deep else "- automations (list only)...")
    listing = paginate("automations")
    if not deep:
        return listing
    detailed: list[dict] = []
    for i, a in enumerate(listing, 1):
        body = api_get(f"automations/{a['id']}")
        if isinstance(body, dict) and "data" in body and isinstance(body["data"], dict):
            detailed.append(body["data"])
        else:
            detailed.append(body if isinstance(body, dict) else a)
        if i % 25 == 0 or i == len(listing):
            log(f"    ... {i}/{len(listing)}")
    return detailed


def fetch_auto_queues() -> list[dict]:
    """List every auto queue and fetch each one in detail so the inline
    step list (automation_event_queue_steps with delays + linked automation
    IDs) is included."""
    log("- auto queues (with steps)...")
    queues = paginate("auto-queues")
    detailed: list[dict] = []
    for q in queues:
        body = api_get(f"auto-queues/{q['id']}")
        if isinstance(body, dict) and "data" in body and isinstance(body["data"], dict):
            detailed.append(body["data"])
        else:
            detailed.append(body if isinstance(body, dict) else q)
    return detailed


def fetch_opportunities() -> list[dict]:
    log("- opportunities (expand=contact)...")
    return paginate("opportunities", expand="contact")


def fetch_companies() -> list[dict]:
    log("- companies (all)...")
    return paginate("companies")


def fetch_contacts(cap: int) -> list[dict]:
    log(f"- contacts (most recent {cap})...")
    items: list[dict] = []
    cursor: str | None = None
    page_size = min(100, cap)
    while len(items) < cap:
        params: dict[str, Any] = {
            "limit": page_size,
            "sort": "created_at",
            "order": "desc",
        }
        if cursor:
            params["after"] = cursor
        body = api_get("contacts", **params)
        if not isinstance(body, dict):
            break
        page = body.get("data") or []
        items.extend(page)
        pagination = body.get("pagination") or {}
        if not pagination.get("has_more"):
            break
        cursor = pagination.get("next_cursor")
        if not cursor:
            break
    return items[:cap]


def main() -> None:
    force_utf8_stdout()
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--out",
        help="Output folder (default: ./crm-bundle/<UTC-date>/)",
    )
    ap.add_argument(
        "--resources",
        default="all",
        help="Comma-list of resources to fetch. Options: "
        + ",".join(DEFAULT_RESOURCES)
        + " (default: all)",
    )
    ap.add_argument(
        "--contacts-limit",
        type=int,
        default=500,
        help="How many recent contacts to dump (default: 500)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print resolved plan + output folder, then exit (no API calls)",
    )
    args = ap.parse_args()

    if args.out:
        out_dir = Path(args.out)
    else:
        out_dir = Path("crm-bundle") / datetime.now(timezone.utc).strftime("%Y-%m-%d")

    log(f"out: {out_dir}")

    if args.resources == "all":
        requested = set(DEFAULT_RESOURCES)
    else:
        requested = {r.strip() for r in args.resources.split(",") if r.strip()}
        unknown = requested - set(DEFAULT_RESOURCES)
        if unknown:
            emit_error_and_exit(
                f"Unknown resources: {sorted(unknown)}. Valid: {DEFAULT_RESOURCES}",
                skill=SKILL,
            )

    log(f"plan: {sorted(requested)}")

    if args.dry_run:
        log("(dry-run — no writes)")
        print(str(out_dir))
        return

    started_at = datetime.now(timezone.utc).isoformat()
    written: list[dict[str, Any]] = []

    try:
        if "pipelines" in requested:
            pipelines, stages = fetch_pipelines()
            write_json(out_dir / "pipelines.json", pipelines)
            write_json(out_dir / "pipeline_stages.json", stages)
            n_stages = sum(len(s) for s in stages.values())
            written += [
                {"file": "pipelines.json", "count": len(pipelines)},
                {"file": "pipeline_stages.json", "count": n_stages},
            ]
            log(f"  -> {len(pipelines)} pipelines, {n_stages} stages")

        if "automations" in requested:
            automations = fetch_automations(deep=True)
            write_json(out_dir / "automations.json", automations)
            written.append({"file": "automations.json", "count": len(automations)})
            log(f"  -> {len(automations)} automations")

        if "auto_queues" in requested:
            queues = fetch_auto_queues()
            write_json(out_dir / "auto_queues.json", queues)
            n_steps = sum(
                len(q.get("automation_event_queue_steps") or q.get("steps") or [])
                for q in queues
            )
            written.append(
                {"file": "auto_queues.json", "count": len(queues), "steps": n_steps}
            )
            log(f"  -> {len(queues)} queues, {n_steps} steps total")

        if "opportunities" in requested:
            opps = fetch_opportunities()
            write_json(out_dir / "opportunities.json", opps)
            written.append({"file": "opportunities.json", "count": len(opps)})
            log(f"  -> {len(opps)} opportunities")

        if "companies" in requested:
            all_co = fetch_companies()
            write_json(out_dir / "companies.json", all_co)
            customers = [c for c in all_co if c.get("is_customer")]
            write_json(out_dir / "companies-customers.json", customers)
            written += [
                {"file": "companies.json", "count": len(all_co)},
                {"file": "companies-customers.json", "count": len(customers)},
            ]
            log(f"  -> {len(all_co)} companies total ({len(customers)} customers)")

        if "contacts" in requested:
            contacts = fetch_contacts(cap=args.contacts_limit)
            write_json(out_dir / "contacts.json", contacts)
            written.append({"file": "contacts.json", "count": len(contacts)})
            log(f"  -> {len(contacts)} recent contacts")

    except BOSError as err:
        emit_error_and_exit(str(err), skill=SKILL)

    write_json(
        out_dir / "_manifest.json",
        {
            "skill": SKILL,
            "started_at": started_at,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "files": written,
        },
    )

    print(str(out_dir))


if __name__ == "__main__":
    main()

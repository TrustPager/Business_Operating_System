#!/usr/bin/env python3
"""learn-my-business — read the shape of the operator's workspace into one digest.

Instead of asking a non-technical operator to pick an industry template and
hand-fill the <<< ... >>> blanks, this reads the live workspace and returns the
real shapes Claude needs to WRITE their CLAUDE.md for them: company profile +
brand, pipelines and their stages, products, lead sources, opportunity types,
lost/won reasons, and rough record counts.

Read-only. Every section is best-effort — the company-profile and crm-settings
endpoints vary by workspace, so anything unreachable lands in `warnings` and
`_sources`, and the digest is emitted with the rest.

Auth: TRUSTPAGER_API_KEY env var or ~/.claude/bos.json.

Usage:
    python skills/learn-my-business/fetch.py
    python skills/learn-my-business/fetch.py --json-only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_error_and_exit, emit_json, force_utf8_stdout,
    log, now_utc, paginate, parallel_get, resolve_path,
)

SKILL = "learn-my-business"

COMPANY_RESOURCE_CANDIDATES = ["company-profile", "company", "companies", "workspace"]
SETTINGS_RESOURCE_CANDIDATES = ["crm-settings", "settings", "crm_settings"]


def _resolve_any(candidates: list[str], **kw: Any) -> str | None:
    for rid in candidates:
        try:
            return resolve_path(rid, **kw)
        except BOSError:
            continue
    return None


def _stages_of(pipeline: dict[str, Any]) -> list[str]:
    stages = (pipeline.get("crm_pipeline_stages") or pipeline.get("stages") or [])
    stages = sorted(stages, key=lambda s: s.get("position") or s.get("step_order") or 0)
    return [s.get("name") for s in stages if s.get("name")]


def _approx_count(path: str) -> int | str | None:
    """Rough size of a list endpoint. The API uses cursor pagination with no
    `total`, so we read one page (100) and report an exact count, or "100+" if
    there's more. Returns None if the endpoint can't be read."""
    try:
        resp = api_get(path, limit=100)
    except BOSError:
        return None
    if not isinstance(resp, dict):
        return None
    n = len(resp.get("data", []) or [])
    has_more = (resp.get("pagination") or {}).get("has_more")
    return f"{n}+" if has_more else n


def fetch(quiet: bool) -> dict[str, Any]:
    now = now_utc()
    warnings: list[str] = []
    sources: dict[str, str] = {}

    # ---- company profile + brand ----
    company: dict[str, Any] = {}
    cpath = _resolve_any(COMPANY_RESOURCE_CANDIDATES, action="list")
    if cpath:
        try:
            resp = api_get(cpath)
            data = resp.get("data", resp)
            row = data[0] if isinstance(data, list) and data else (data if isinstance(data, dict) else {})
            company = {
                "name": row.get("name") or row.get("company_name"),
                "industry": row.get("industry"),
                "website": row.get("website") or row.get("website_url"),
                "city": row.get("city"),
                "country": row.get("country"),
                "brand_primary": (row.get("brand") or {}).get("primary_color") if isinstance(row.get("brand"), dict) else row.get("primary_color"),
                "description": row.get("description") or row.get("about"),
            }
            sources["company"] = "ok"
        except BOSError as e:
            sources["company"] = "unavailable"
            warnings.append(f"company profile not readable: {str(e).splitlines()[0]}")
    else:
        sources["company"] = "unavailable"
        warnings.append("no company-profile endpoint in the catalog — ask the operator for name/industry")

    # ---- pipelines + stages ----
    # Stages are NOT inline on the pipeline list/detail — they live at the
    # sub-endpoint GET /pipelines/:id/stages. Fetch them in parallel per pipeline.
    pipelines: list[dict[str, Any]] = []
    try:
        ppath = resolve_path("pipelines")
        listed = list(paginate(ppath, limit=100, max_pages=3))
        ids = [p["id"] for p in listed if p.get("id")]
        stage_resp = parallel_get([(f"{ppath}/{i}/stages", {}) for i in ids]) if ids else {}
        for p in listed:
            pid = p.get("id")
            stages = _stages_of(p)  # use inline stages if the API ever provides them
            if not stages and pid:
                sr = stage_resp.get(f"{ppath}/{pid}/stages", {})
                rows = sr.get("data", []) if isinstance(sr, dict) and "error" not in sr else []
                rows = sorted(rows, key=lambda s: s.get("position") or 0)
                stages = [s.get("name") for s in rows if s.get("name")]
            pipelines.append({
                "id": pid,
                "name": p.get("name"),
                "is_default": bool(p.get("is_default") or p.get("is_primary")),
                "stages": stages,
            })
        sources["pipelines"] = "ok"
    except BOSError as e:
        sources["pipelines"] = "unavailable"
        warnings.append(f"pipelines not readable: {str(e).splitlines()[0]}")

    # ---- products ----
    products: list[dict[str, Any]] = []
    try:
        for p in paginate(resolve_path("products"), limit=100, max_pages=2):
            products.append({
                "name": p.get("name"),
                "price": p.get("price") or p.get("unit_price"),
                "currency": p.get("currency"),
                "billing": p.get("billing_interval") or p.get("pricing_model"),
            })
        sources["products"] = "ok"
    except BOSError as e:
        sources["products"] = "unavailable"
        warnings.append(f"products not readable: {str(e).splitlines()[0]}")

    # ---- crm settings (lead sources, types, reasons) ----
    settings: dict[str, Any] = {}
    spath = _resolve_any(SETTINGS_RESOURCE_CANDIDATES, action="list")
    if spath:
        try:
            resp = api_get(spath)
            s = resp.get("data", resp) if isinstance(resp, dict) else {}
            if isinstance(s, list) and s:
                s = s[0]
            settings = {
                "lead_sources": s.get("lead_sources") or s.get("lead_source_options"),
                "opportunity_types": s.get("opportunity_type_options") or s.get("deal_types"),
                "lost_reasons": s.get("lost_reasons") or s.get("lost_reason_options"),
                "won_reasons": s.get("won_reasons") or s.get("won_reason_options"),
            }
            sources["settings"] = "ok"
        except BOSError as e:
            sources["settings"] = "unavailable"
            warnings.append(f"crm settings not readable: {str(e).splitlines()[0]}")
    else:
        sources["settings"] = "unavailable"

    # ---- rough counts (cursor pagination has no total — approximate) ----
    counts: dict[str, int | str | None] = {}
    for label, rid in (("opportunities", "opportunities"), ("contacts", "contacts"),
                       ("companies", "companies"), ("automations", "automations")):
        try:
            counts[label] = _approx_count(resolve_path(rid))
        except BOSError:
            counts[label] = None
    sources["counts"] = "ok"

    return {
        "generated_at": now.isoformat(),
        "company": company,
        "pipelines": pipelines,
        "products": products[:25],
        "settings": settings,
        "counts": counts,
        "warnings": warnings,
        "_sources": sources,
    }


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--json-only", action="store_true", help="Suppress stderr progress logs")
    args = parser.parse_args()
    try:
        log(SKILL, "reading workspace shape...", quiet=args.json_only)
        emit_json(fetch(quiet=args.json_only))
        return 0
    except BOSError as e:
        emit_error_and_exit(str(e), code=1)


if __name__ == "__main__":
    sys.exit(main())


# =============================================================================
# Output shape — what Claude reads from stdout
# =============================================================================
#
# {
#   "generated_at": "...",
#   "company": {"name": "...", "industry": "...", "website": "...",
#               "city": "...", "country": "...", "brand_primary": "#...",
#               "description": "..."},
#   "pipelines": [{"id": "...", "name": "Sales", "is_default": true,
#                  "stages": ["New lead", "Qualified", "Quote sent", "Won"]}],
#   "products": [{"name": "CRM Suite", "price": 129, "currency": "AUD",
#                 "billing": "monthly"}],
#   "settings": {"lead_sources": [...], "opportunity_types": [...],
#                "lost_reasons": [...], "won_reasons": [...]},
#   "counts": {"opportunities": 240, "contacts": 1800, "companies": 320,
#              "automations": 18},
#   "warnings": [...],
#   "_sources": {"company": "ok", "pipelines": "ok", "products": "ok",
#                "settings": "ok", "counts": "ok"}
# }

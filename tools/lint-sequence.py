#!/usr/bin/env python3
"""Lint a nurture sequence against the house style — before it ships, or to
catch drift in a live queue.

This is the deterministic check behind `/lint-nurture-sequence`. It reads a set
of sequence emails (from a live auto queue, or from a local drafts file) and
flags, per email, the things that quietly degrade a drip: a missing clickable
text CTA above the image, an inconsistent sign-off, a negative subject line, an
em dash, a missing greeting. Then it checks the set is internally CONSISTENT —
the single biggest cause of a sequence that "feels half-built" is some emails
following the pattern and others not.

What it checks per email:
  - greeting present (Hi {{contact.first_name}} / a {{contact.*}} near the top)
  - a link exists at all
  - a bold clickable TEXT link appears ABOVE the first image (so image-blocked
    clients still have a CTA) — the exact gap that makes drips underperform
  - HTML <p> structure (plain-text bodies render badly in Gmail)
  - sign-off block present (default "Warmest regards"; set with --signoff)
  - subject is positive / forward-looking (no leading negation)
  - no em dash (house style; relax with --allow-em-dash)
  - subject present and not absurdly long

Across the set:
  - sign-offs match
  - CTA-above-image is all-or-nothing (not mixed)
  - P.S. presence is consistent (informational)

Exit codes (mirrors tools/lint-skill.py):
    0 — clean
    1 — warnings only
    2 — at least one FAIL

Usage:
    python tools/lint-sequence.py --queue <auto_queue_id>
    python tools/lint-sequence.py --drafts path/to/drafts.json
    python tools/lint-sequence.py --queue <id> --json          # machine-readable
    python tools/lint-sequence.py --drafts d.json --signoff "Cheers, Sam" --allow-em-dash

Drafts file shape (either form):
    [{"label": "Day 0", "subject": "...", "body": "<p>...</p>"}, ...]
    {"emails": [ {...}, ... ]}
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trustpager_api import (  # noqa: E402
    BOSError, api_get, emit_json, force_utf8_stdout, log, paginate, resolve_path,
)

TOOL = "lint-sequence"

SEND_ACTION_TYPES = {"send_gmail_email", "send_custom_email", "send_marketing_email"}
QUEUE_RESOURCE_CANDIDATES = ["event-queues", "auto-queues", "auto_queues", "event_queues"]
DEFAULT_SIGNOFF = "Warmest regards"

# Subject openers / tokens that read as negative framing.
NEGATION_PATTERNS = [
    r"^\s*don'?t\b", r"^\s*do not\b", r"^\s*stop\b", r"^\s*never\b",
    r"^\s*no\b", r"\bisn'?t\b", r"\bwon'?t\b", r"\bcan'?t\b", r"\bdon'?t\b",
    r"\bnever\b", r"\bstop\b",
]

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"


# ---------------------------------------------------------------------------
# Source loaders
# ---------------------------------------------------------------------------

def _resolve_any(candidates: list[str], **kw: Any) -> str:
    last: Exception | None = None
    for rid in candidates:
        try:
            return resolve_path(rid, **kw)
        except BOSError as e:
            last = e
    raise BOSError(f"None of {candidates} resolve. Last: {last}")


def _emails_from_queue(queue_id: str, quiet: bool) -> list[dict[str, str]]:
    """Pull each step's email (subject + body) from a live auto queue, in order."""
    get_path = _resolve_any(QUEUE_RESOURCE_CANDIDATES, action="get")
    concrete = get_path.replace(":id", queue_id).replace(":queue_id", queue_id)
    resp = api_get(concrete)
    detail = resp.get("data", resp) if isinstance(resp, dict) else {}
    steps = (detail.get("automation_event_queue_steps") or detail.get("steps") or [])
    steps = sorted(steps, key=lambda s: s.get("step_order") or 0)

    emails: list[dict[str, str]] = []
    for s in steps:
        aid = s.get("automation_id")
        label = (s.get("description") or f"Step {s.get('step_order')}")
        if "—" in label:
            label = label.split("—")[0].strip()
        if not aid:
            emails.append({"label": label, "subject": "", "body": "", "_note": "no automation linked"})
            continue
        try:
            actions_resp = api_get(f"automations/{aid}/actions")
            actions = actions_resp.get("data", actions_resp) if isinstance(actions_resp, dict) else []
        except BOSError:
            actions = []
        send = next((a for a in actions if a.get("action_type") in SEND_ACTION_TYPES), None)
        cfg = (send or {}).get("config", {}) if send else {}
        emails.append({
            "label": label,
            "subject": cfg.get("subject") or "",
            "body": cfg.get("body") or "",
            "_note": "" if send else "no send action on this step",
        })
    return emails


def _emails_from_drafts(path: str) -> list[dict[str, str]]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    items = raw.get("emails", raw) if isinstance(raw, dict) else raw
    out: list[dict[str, str]] = []
    for i, e in enumerate(items):
        out.append({
            "label": e.get("label") or e.get("day") or f"Email {i + 1}",
            "subject": e.get("subject") or "",
            "body": e.get("body") or e.get("html") or "",
            "_note": "",
        })
    return out


# ---------------------------------------------------------------------------
# Per-email checks
# ---------------------------------------------------------------------------

def _first_img_index(body: str) -> int:
    m = re.search(r"<img\b", body, re.IGNORECASE)
    return m.start() if m else -1


def _has_text_cta_before_image(body: str, img_idx: int) -> bool:
    """True if a TEXT link closes before the first image — i.e. an anchor with
    visible text content, not the anchor that merely wraps the image itself.
    That wrapping anchor doesn't help readers whose client blocks images."""
    for m in re.finditer(r"<a\b[^>]*href=[^>]*>(.*?)</a>", body, re.IGNORECASE | re.DOTALL):
        if m.start() >= img_idx:
            break
        inner = m.group(1)
        if "<img" in inner.lower():
            continue  # anchor just wraps an image — not a clickable text CTA
        if re.sub(r"<[^>]+>", "", inner).strip():
            return True
    return False


def _check_email(email: dict[str, str], signoff: str, allow_em_dash: bool) -> list[dict[str, str]]:
    subject = email.get("subject", "") or ""
    body = email.get("body", "") or ""
    checks: list[dict[str, str]] = []

    def add(name: str, level: str, msg: str) -> None:
        checks.append({"check": name, "level": level, "message": msg})

    # subject present
    if not subject.strip():
        add("subject", FAIL, "no subject line")
    elif len(subject) > 90:
        add("subject", WARN, f"subject is long ({len(subject)} chars) — front-load the hook")
    else:
        add("subject", PASS, "subject present")

    # greeting
    head = body[:240].lower()
    if "{{contact." in head or re.search(r"\bhi\b|\bhello\b|\bhey\b", head):
        add("greeting", PASS, "greeting present")
    else:
        add("greeting", WARN, "no greeting near the top (expected 'Hi {{contact.first_name}}')")

    # html structure
    if "<p" in body.lower():
        add("html", PASS, "uses <p> structure")
    elif body.strip():
        add("html", WARN, "body is not HTML <p> — plain text renders poorly in Gmail")

    # link exists
    has_any_link = bool(re.search(r"<a\b[^>]*href=", body, re.IGNORECASE))
    img_idx = _first_img_index(body)
    if not has_any_link:
        add("link", FAIL, "no link in the email at all — there's nothing to click")
    else:
        add("link", PASS, "has a link")

    # CTA text link ABOVE the image
    if img_idx >= 0:
        if _has_text_cta_before_image(body, img_idx):
            add("cta_above_image", PASS, "clickable text CTA appears above the image")
        else:
            add("cta_above_image", FAIL,
                "image has no text link above it — readers who block images get no CTA")
    else:
        add("cta_above_image", PASS, "no image (text-only email — n/a)")

    # sign-off
    if signoff.lower() in body.lower():
        add("signoff", PASS, f"sign-off present ('{signoff}')")
    else:
        add("signoff", WARN, f"sign-off '{signoff}' not found — sequence sign-offs should match")

    # positive subject
    subj_l = subject.lower()
    if subject and any(re.search(p, subj_l) for p in NEGATION_PATTERNS):
        add("positive_subject", WARN, "subject reads as negative framing — prefer a positive, forward-looking line")
    elif subject:
        add("positive_subject", PASS, "subject is positively framed")

    # em dash
    if not allow_em_dash and ("—" in subject or "—" in body):
        add("no_em_dash", WARN, "contains an em dash (—) — house style avoids them (use --allow-em-dash to permit)")
    else:
        add("no_em_dash", PASS, "no em dash" if not allow_em_dash else "em dash allowed")

    if email.get("_note"):
        add("source", WARN, email["_note"])

    return checks


# ---------------------------------------------------------------------------
# Cross-set consistency
# ---------------------------------------------------------------------------

def _consistency(emails: list[dict[str, str]], per_email: list[dict[str, Any]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []

    # CTA-above-image should be all-or-nothing
    cta_states = []
    for e in per_email:
        cta = next((c for c in e["checks"] if c["check"] == "cta_above_image"), None)
        if cta and "n/a" not in cta["message"]:
            cta_states.append(cta["level"] == PASS)
    if cta_states and len(set(cta_states)) > 1:
        out.append({"level": FAIL,
                    "message": "MIXED: some emails have a text CTA above the image and some don't — "
                               "this is the #1 cause of a drip feeling half-built. Make it consistent."})

    # P.S. presence consistency (informational)
    ps_flags = ["p.s." in (e.get("body", "") or "").lower() for e in emails]
    if ps_flags and 0 < sum(ps_flags) < len(ps_flags):
        out.append({"level": WARN,
                    "message": f"P.S. line present on {sum(ps_flags)}/{len(ps_flags)} emails — "
                               "fine if intentional, worth aligning if not."})

    # sign-off consistency
    signoff_flags = [
        next((c["level"] for c in e["checks"] if c["check"] == "signoff"), PASS) == PASS
        for e in per_email
    ]
    if signoff_flags and 0 < sum(signoff_flags) < len(signoff_flags):
        out.append({"level": WARN,
                    "message": "sign-off block is inconsistent across the set — every email should close the same way."})

    return out


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def _worst(level_a: str, level_b: str) -> str:
    order = {PASS: 0, WARN: 1, FAIL: 2}
    return level_a if order[level_a] >= order[level_b] else level_b


def lint(emails: list[dict[str, str]], signoff: str, allow_em_dash: bool) -> dict[str, Any]:
    per_email: list[dict[str, Any]] = []
    for e in emails:
        checks = _check_email(e, signoff, allow_em_dash)
        worst = PASS
        for c in checks:
            worst = _worst(worst, c["level"])
        per_email.append({"label": e.get("label"), "subject": e.get("subject"),
                          "worst": worst, "checks": checks})
    consistency = _consistency(emails, per_email)

    overall = PASS
    for e in per_email:
        overall = _worst(overall, e["worst"])
    for c in consistency:
        overall = _worst(overall, c["level"])

    fails = sum(1 for e in per_email for c in e["checks"] if c["level"] == FAIL)
    fails += sum(1 for c in consistency if c["level"] == FAIL)
    warns = sum(1 for e in per_email for c in e["checks"] if c["level"] == WARN)
    warns += sum(1 for c in consistency if c["level"] == WARN)

    return {
        "overall": overall,
        "email_count": len(emails),
        "fail_count": fails,
        "warn_count": warns,
        "emails": per_email,
        "consistency": consistency,
    }


GLYPH = {PASS: "✓", WARN: "⚠", FAIL: "✗"}


def _print_human(report: dict[str, Any]) -> None:
    print(f"Sequence lint — {report['email_count']} emails: "
          f"{report['fail_count']} fail, {report['warn_count']} warn  "
          f"[{report['overall']}]\n")
    for e in report["emails"]:
        print(f"{GLYPH[e['worst']]} {e['label']}  —  {e['subject'] or '(no subject)'}")
        for c in e["checks"]:
            if c["level"] != PASS:
                print(f"     {GLYPH[c['level']]} {c['check']}: {c['message']}")
    if report["consistency"]:
        print("\nAcross the set:")
        for c in report["consistency"]:
            print(f"  {GLYPH[c['level']]} {c['message']}")
    print()


def main() -> int:
    force_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--queue", metavar="ID", help="Lint a live auto queue's emails")
    src.add_argument("--drafts", metavar="FILE", help="Lint a local drafts JSON file")
    parser.add_argument("--signoff", default=DEFAULT_SIGNOFF, help=f"Expected sign-off (default: '{DEFAULT_SIGNOFF}')")
    parser.add_argument("--allow-em-dash", action="store_true", help="Permit em dashes")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a human report")
    parser.add_argument("--json-only", action="store_true", help="Alias for --json")
    args = parser.parse_args()

    try:
        if args.queue:
            log(TOOL, f"reading queue {args.queue}...", quiet=args.json or args.json_only)
            emails = _emails_from_queue(args.queue, quiet=args.json or args.json_only)
        else:
            emails = _emails_from_drafts(args.drafts)
    except (BOSError, OSError, json.JSONDecodeError) as e:
        sys.stderr.write(f"ERROR: {e}\n")
        return 2

    if not emails:
        sys.stderr.write("No emails found to lint.\n")
        return 2

    report = lint(emails, signoff=args.signoff, allow_em_dash=args.allow_em_dash)
    if args.json or args.json_only:
        emit_json(report)
    else:
        _print_human(report)

    return 2 if report["overall"] == FAIL else (1 if report["overall"] == WARN else 0)


if __name__ == "__main__":
    sys.exit(main())

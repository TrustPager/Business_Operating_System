#!/usr/bin/env python3
"""Generate docs/CAPABILITIES.md — the GTM-facing capability doc (registry-derived).

The go-to-market project needs to cite what the plugin *actually* does today
without hand-listing features that drift. This tool turns the live capability
registry into one plain-language, owner-facing capability doc so GTM references
a single true artifact that stays honest as the system grows.

Design rules this module upholds (mirroring tools/registry-generator.py):

- **The registry is the source of truth for WHAT appears.** We read
  ``kernel/registry.json`` for the set of capabilities, their ``status``,
  ``function_slot``, ``requires_driver``, and ``requires_credential``. Only
  ``status: active`` capabilities are listed. The plain name and one-liner come
  from each skill's SKILL.md frontmatter (``name`` / ``description``), lifted
  with the SHARED parser in ``tools/manifest.py`` — we do NOT write a second
  parser, and we do NOT copy prose into the registry.

- **Pure deterministic function of the registry + manifests.** No git commit,
  no timestamp, no machine state is embedded. Two runs over the same inputs
  produce byte-identical output, so ``--check`` is a stable drift guard.
  (Cross-repo provenance is stamped later by the downstream sync step, not here.)

- **One broken skill can't dark the doc.** A capability listed in the registry
  whose SKILL.md is missing or unreadable falls back to a name derived from its
  id and a one-liner condensed from the description (or empty), with a warning
  to stderr — it never crashes the run.

- **Plain language, owner-facing, no jargon.** Each one-liner is an authored,
  owner-facing sentence: no tool names (TrustPager, MCP, app-ids, "skill",
  "driver", "registry", "kernel"), no cross-reference tails, framed by the
  outcome. The authored copy lives in a static map keyed by capability id; what
  actually *appears* is still gated entirely by the registry's active set and
  classification, so the doc stays a deterministic function of the registry.

The six job groups and the keyless-vs-connect split mirror skills/whats-possible
exactly:

- 🏆 Win work · 💰 Get paid · 📞 Stay on top of customers ·
  🎨 Look professional & market · 🗂️ Handle paperwork · 🧭 Plan & decide
- **Keyless** = ``requires_credential: none`` AND ``requires_driver`` in
  {none, markitdown, render, doclib, firecrawl}; everything else is connect-tier.

CLI:
    python tools/export-capabilities.py            # write docs/CAPABILITIES.md
    python tools/export-capabilities.py --out PATH # write somewhere else
    python tools/export-capabilities.py --check    # verify, NEVER write (CI gate)

In ``--check`` mode it regenerates the doc IN MEMORY, compares it byte-for-byte
to the committed ``docs/CAPABILITIES.md``, and NEVER touches the file: identical
→ prints "CAPABILITIES.md up to date" and exits 0; different (or missing) →
prints a "regenerate it" message and exits 1. This is the drift guard that fails
CI when the registry changes without re-exporting.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Reuse the single source of truth for the manifest parser. tools/manifest.py
# has an import-safe name (no hyphen), so add tools/ to sys.path and import it
# directly rather than re-loading by path — this guarantees one parser.
_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from manifest import parse_frontmatter  # noqa: E402  (path set above)

# --- The keyless floor definition (mirrors skills/whats-possible) --------
#
# A capability "works right now (keyless)" when it needs zero accounts: no
# credential AND only a local-or-keyless driver. Everything else "switches on
# when you connect a tool". This is the exact split whats-possible uses.
_KEYLESS_DRIVERS: frozenset[str] = frozenset(
    {"none", "markitdown", "render", "doclib", "firecrawl"}
)

# --- Heavy render-studio apps (D13) ----------------------------------------
#
# These are keyless (no credential, render driver counts as keyless) but they
# require the bundled browser/puppeteer render stack to actually execute. They
# are NOT cold day-one instant wins and must not appear in the plain "Works now
# (keyless)" instant-win block. They get their own clearly-labelled subgroup:
# "Keyless, heavier setup (optional studios)".
#
# Rule: only apps whose SKILL.md describes a browser/puppeteer render pipeline
# belong here. Keyless apps that merely write files or read a website do NOT
# belong here even if they touch a studio (e.g. brand-my-workspace just writes
# JSON; assemble-content-pack just collects files).
_HEAVY_RENDER_APPS: frozenset[str] = frozenset(
    {"make-social-post", "make-thumbnail"}
)

# --- The six owner-facing job groups (mirrors skills/whats-possible) ------
#
# Order is the presentation order in the doc. Each is (emoji+title, intro line).
_GROUPS: tuple[tuple[str, str, str], ...] = (
    (
        "win_work",
        "🏆 Win work",
        "Quoting, proposals, positioning, sizing up a competitor, "
        "researching a prospect before a call.",
    ),
    (
        "get_paid",
        "💰 Get paid",
        "Spotting unbilled or unpaid work and chasing what you're owed.",
    ),
    (
        "stay_on_top",
        "🤝 Stay on top of customers",
        "Follow-ups, missed-call recovery, turning a call into notes and next "
        "steps, and keeping your customer list clean.",
    ),
    (
        "look_professional",
        "🎨 Look professional & market",
        "Your brand and voice, branded posts, content plans, and a workspace "
        "that looks like you.",
    ),
    (
        "handle_paperwork",
        "🗂️ Handle paperwork",
        "Reading any file and structuring it, forms, documents, e-signing, "
        "spreadsheets, and intake packs.",
    ),
    (
        "plan_and_decide",
        "🧭 Plan & decide",
        "Stress-testing a decision, writing a sharp brief or prompt, hiring "
        "and onboarding, and building the playbook your business runs on.",
    ),
)

# Default group for each function_slot, used when a capability is not given an
# explicit placement below. Mirrors whats-possible Step 2's slot hints.
_SLOT_DEFAULT_GROUP: dict[str, str] = {
    "crm": "stay_on_top",
    "comms": "stay_on_top",
    "money": "get_paid",
    "accounting": "get_paid",
    "social": "look_professional",
    "creative": "look_professional",
    "ads": "look_professional",
    "documents": "handle_paperwork",
    "research": "win_work",
    "strategy": "plan_and_decide",
    "people": "plan_and_decide",
    "floor": "plan_and_decide",
}

# Explicit per-capability placement, for capabilities whose best job-group is
# not simply their slot's default (whats-possible: "a capability can sit in the
# group that best fits the job it does for them, not just its slot"). Anything
# not listed here folds into _SLOT_DEFAULT_GROUP[slot].
_GROUP_OVERRIDES: dict[str, str] = {
    # Quoting / proposals / product copy are how you WIN work, regardless of slot.
    "price-my-work": "win_work",
    "quote-from-photo": "win_work",
    "write-a-proposal": "win_work",
    "describe-a-product": "win_work",
    # Brand strategy is the "look professional & market" foundation.
    "build-brand-strategy": "look_professional",
    "build-customer-voice": "look_professional",
    # Voice lock-in is brand/marketing, not planning, despite its strategy slot.
    "build-my-voice": "look_professional",
}


def _plain_name(app_id: str, meta: dict[str, Any]) -> str:
    """The owner-facing display name.

    Prefer the SKILL.md ``name`` when it reads like a real title (not just the
    kebab-case id echoed back). Otherwise derive a Title Case name from the id.
    """
    name = meta.get("name")
    if isinstance(name, str) and name.strip():
        # Some skills set name to the bare id (e.g. "draft-reply"). If the name
        # is just the id, Title-Case the id instead so the doc never shows a
        # kebab-case token.
        if name.strip().lower() != app_id.lower():
            return name.strip()
    return _titlecase_id(app_id)


def _titlecase_id(app_id: str) -> str:
    """``draft-reply`` -> ``Draft Reply`` (small joiners stay lowercase)."""
    small = {"a", "an", "and", "for", "from", "of", "on", "the", "to"}
    parts = app_id.replace("_", "-").split("-")
    words: list[str] = []
    for i, part in enumerate(parts):
        if not part:
            continue
        if i != 0 and part.lower() in small:
            words.append(part.lower())
        else:
            words.append(part[:1].upper() + part[1:])
    return " ".join(words)


# Authored, owner-facing one-liners — one per capability id. These are the
# plain-English "what it does for you" lines that ship to GTM: outcome-led,
# positive, no tool names, no em dashes, no cross-references. They distil each
# skill's intent without the internal/dev framing the SKILL.md descriptions
# carry. The registry still gates WHAT appears; this map only supplies HOW each
# active capability is described.
_ONE_LINERS: dict[str, str] = {
    # 🏆 Win work
    "describe-a-product": "Turn a photo or a few notes into an on-brand product "
    "description ready for your store, a listing, or a catalogue.",
    "price-my-work": "Turn the cost of a job into a priced breakdown you can "
    "stand behind, with your margin shown and the assumptions written down.",
    "quote-from-photo": "Turn a site photo and a few notes into a drafted quote "
    "or proposal in about a minute, ready for you to review.",
    "write-a-proposal": "Turn a priced scope and your voice into the proposal "
    "that wins the job, written out as a document you can send.",
    "research-a-competitor": "Read a rival's page and turn it into a sharp "
    "one-page read: how they position, what they charge, and your openings.",
    "research-before-call": "Walk into any meeting prepared, with a one-page "
    "brief on the person or company plus three questions that open the room.",
    # 💰 Get paid
    "profit-per-job": "Find out what one job type actually earns you after every "
    "cost is counted, with your margin shown as a dollar figure.",
    "cash-flow-forecast": "See your cash position week by week, with a live "
    "spreadsheet where the running balance updates when you change any number.",
    "estimate-my-bas": "Prepare your quarterly Simpler-BAS GST figures (G1, 1A, "
    "1B) with the calculation shown and the ATO source cited, ready to enter on "
    "your own BAS. Australian businesses only.",
    "outstanding-invoices": "Show who owes you money as an aged summary, and "
    "optionally email it to you on a schedule.",
    "sync-from-xero": "Pull your customer, invoice, and payment data from Xero "
    "so your deals reflect what has actually been paid.",
    # 📞 Stay on top of customers
    "renewal-tracker": "A live tracker spreadsheet for licenses, insurances, "
    "certifications, and memberships, where the days-until-renewal column "
    "recalculates every time you open the file.",
    "transcript-summary": "Turn a recorded call or meeting into a clean "
    "write-up with the decisions and the action list.",
    "write-a-letter": "Turn what happened, in your own words, into a firm, "
    "professional letter that holds the line and stays factual.",
    "add-a-field": "Add a custom field to your records and surface it where you "
    "need it, on the card and in your spreadsheets.",
    "audit-my-automations": "Health-check every automation: which are firing, "
    "stale, erroring, or overlapping, with a one-line fix for each.",
    "audit-my-data": "Find the gaps in your records: missing fields, likely "
    "duplicates, dormant records, and a fix checklist worst-first.",
    "automate-this": "Describe a repetitive task and get a working automation "
    "built for you: triggers, conditions, and ordered actions.",
    "build-work-order-process": "Set up the statuses your jobs move through and "
    "the details captured at each step.",
    "design-nurture-sequence": "Draft a multi-step email follow-up sequence in "
    "your voice, ready for you to review.",
    "draft-reply": "Draft a reply to an email or text in your tone, with the "
    "context pulled in, ready for your approval.",
    "follow-up-radar": "Surface the deals that have gone quiet and draft a "
    "personalised re-engagement message for each, for you to approve.",
    "form-radar": "Show where every form you sent stands, and who to nudge or "
    "chase, hottest follow-ups first.",
    "lead-triage": "Sort new leads by fit and draft the right first response "
    "for each: fast-track, slow burn, or pass.",
    "lint-nurture-sequence": "Check a follow-up sequence against your house "
    "style before it ships, and catch drift across the set.",
    "log-this-call": "Log the call you just had: capture the recap, update the "
    "deal, and schedule the next step.",
    "make-it-happen": "Describe what you want done in plain English and have it "
    "carried out, with your approval at each important step.",
    "missed-call-recovery": "Find recent missed calls and draft a recovery text "
    "or callback message for each, ready to send.",
    "nurture-health": "See whether your live follow-up sequences are working: "
    "the funnel, where people drop off, and per-step open and click rates.",
    "prep-for-call": "Build the brief before a customer call: who they are, the "
    "deal, the history, and the one outcome to drive.",
    "report-an-issue": "File a clean bug report or feature request to the "
    "platform team without leaving your assistant.",
    "review-team-draft": "Review a teammate's customer-facing draft before it "
    "ships: on-voice and verified, then approve it or send it back.",
    "send-email": "Send an email that drafts the body in your tone, attaches "
    "what is relevant, and gets your approval before it goes.",
    "sweep-my-day": "Get a morning briefing of everything that needs your "
    "attention today across deals, tasks, and messages.",
    "test-form": "Safely test a form or client portal before any real customer "
    "sees it, confirming answers land on the record.",
    "why-didnt-it-fire": "Find the one real reason an automation did not do "
    "what you expected, plus the fix.",
    "wire-nurture-sequence": "Push an approved set of follow-up drafts live in "
    "the right order so the sequence runs on its own.",
    "work-order-radar": "Show the state of every job: what has stalled too "
    "long and what completed recently, stalls first.",
    # 🎨 Look professional & market
    "assemble-content-pack": "Gather the pieces of one finished social post "
    "into a single, clean, ready-to-publish folder.",
    "brand-my-workspace": "Point this at your website to detect your colours, "
    "fonts, name, and logo, and brand every studio in one shot.",
    "build-brand-strategy": "Turn how you talk about your work into a sharp "
    "brand brief: positioning, a promise, and content angles, in your words.",
    "build-customer-voice": "Turn the words your customers actually use into a "
    "customer-voice doc that grounds all your marketing.",
    "build-my-voice": "Lock in how you sound so every content app writes as you, "
    "from a file of your own emails and posts: your company voice and your "
    "personal voice, both from your own words.",
    "build-social-strategy": "Turn your goal into a tailored social plan: the "
    "platforms, a realistic cadence, content pillars, and the first move.",
    "make-social-post": "Design and render branded social posts for Instagram, "
    "LinkedIn, and X, ready to publish.",
    "make-thumbnail": "Design and render a polished, on-brand YouTube thumbnail "
    "for any video.",
    "plan-my-content": "Turn your content pillars and voice into a dated, "
    "ready-to-post calendar for the next week or two.",
    "write-post-copy": "Draft the publish-ready words for a social post in your "
    "own voice, ready to go out with the graphic.",
    # 🗂️ Handle paperwork
    "build-spreadsheet": "Build a real spreadsheet you can open and fill today: "
    "a job tracker, a simple cashflow, or a lead log.",
    "compare-documents": "Compare two documents and show what actually changed, "
    "in plain language: added, removed, and changed.",
    "extract-document": "Pull the data out of any file and use it: answer a "
    "question, summarise it, or map it onto a record.",
    "import-from-anywhere": "Turn a messy source, like a screenshot or a broken "
    "export, into one tidy customer list you can use.",
    "template-from-document": "Turn an existing paper or PDF form or contract "
    "into a reusable digital template.",
    "assemble-pack": "Combine a record's filled forms and uploaded files into "
    "one ordered PDF pack, ready to send onward.",
    "build-document": "Design a reusable signing document template with "
    "sections, merge fields, and the inputs the signer fills.",
    "build-form": "Design a form template with the fields, types, and order "
    "you need.",
    "build-knowledge-base-from-docs": "Turn your policy, FAQ, and product docs "
    "into answerable knowledge so the assistant and voice agents use them.",
    "lint-document": "Pre-flight a signing template before it goes out: every "
    "signer has a signature, no broken merge fields, nothing missing.",
    "lint-form": "Pre-flight a form before it ships: every field wired, "
    "required fields set, and no leftover placeholders.",
    "outstanding-documents": "Show, per client, what you asked for versus what "
    "has arrived, so you chase exactly the right thing.",
    "send-for-signing": "Send a document to signers with the safeguards: "
    "confirm signers, preview the merge, and track who has signed.",
    "signing-radar": "Show where every document you sent for signing stands, "
    "and who to follow up or chase, hottest first.",
    "update-pdf": "Fill a PDF with data from a record so you never retype it, "
    "then show you the filled copy to review.",
    "wire-form": "Connect a form's fields to the right record so answers land "
    "where they should, then hook it into how it is used.",
    # 🧭 Plan & decide
    "grill-me-on-this-decision": "Pressure-test a real decision before you "
    "commit: the assumptions, both cases at full strength, and a recommendation.",
    "find-my-next-move": "Get the straight operator's read of your business: the "
    "one thing most in your way, the highest-leverage move to clear it shown from "
    "your own numbers, and a kept one-page plan.",
    "plan-my-roadmap": "See what to connect next: the tools and add-ons that "
    "would move you fastest toward your goal, in priority order, as a kept "
    "one-page roadmap.",
    "onboard-team-member": "Set a new hire up with your team's standards baked "
    "in, so they follow the same process from day one.",
    "start-here": "Get your assistant up to speed on your business in one short "
    "conversation where it thinks alongside you toward your goal, then recommends "
    "the first thing to build together.",
    "sync-team-standards": "Push a change to your team's standards out to "
    "everyone, with a per-person preview before it updates.",
    "whats-possible": "Show everything your system can already do for you, "
    "grouped by the job it gets done.",
    "write-a-job-ad": "Turn a role and its must-haves into a ready-to-post job "
    "ad in your voice, with screening questions that filter applicants.",
    "write-a-policy": "Turn how you actually handle something into clean, "
    "on-brand policy or FAQ text ready for your website, emails, or staff.",
    "write-prompt": "Turn a rough ask into a complete, explicit prompt ready to "
    "hand to a person or to your assistant.",
    "delegate-this-work": "Hand a piece of work to a specific team member, with "
    "a follow-up set so it does not fall through the cracks.",
    "email-me-a-report": "Deliver any report as a recurring email digest that "
    "lands in the right inboxes on a schedule.",
    "learn-my-business": "Read your live workspace and write your business "
    "profile from real data: your pipeline, products, and brand.",
    "show-me-how": "Describe what you want to do and get a step-by-step "
    "walkthrough, with the right pages and the gotchas.",
    "team-review": "Get a weekly rollup for managers: who shipped what, which "
    "deals moved, and where work is stuck.",
    "weekly-review": "Get the Friday rollup: what shipped, what stalled, and "
    "where the pipeline sits now.",
    "tune-my-setup": "Set up Claude Code with sensible working-style defaults "
    "and safe-read permissions, additive and reversible at any time.",
}


def _one_liner(app_id: str, meta: dict[str, Any]) -> str:
    """The owner-facing one-line description for a capability.

    Prefers the authored line in ``_ONE_LINERS`` (clean, no jargon, no em
    dashes). If a capability has no authored line (e.g. a brand-new skill added
    to the registry before this map is updated), fall back to a condensed first
    clause of its SKILL.md description so the doc still has *something* honest,
    rather than a blank line. Returns "" only when neither is available.
    """
    authored = _ONE_LINERS.get(app_id)
    if authored:
        return authored

    desc = meta.get("description")
    if not isinstance(desc, str) or not desc.strip():
        return ""
    text = _lead_clause(desc.strip())
    text = " ".join(text.split()).strip(" ,;:-")
    if not text:
        return ""
    return text[:1].upper() + text[1:]


def _lead_clause(text: str) -> str:
    """Return the leading clause: the first sentence, trimmed at an aside dash.

    Splits on the first sentence-ending period and on the em dash skills use to
    introduce examples / asides, whichever comes first, so a fallback line stays
    a single clean statement. (Used only for the rare no-authored-line case.)
    """
    cut = len(text)
    i = text.find(". ")
    if i != -1:
        cut = min(cut, i)
    if text.endswith(".") and len(text) - 1 < cut:
        cut = len(text) - 1
    dash = text.find("—")  # em dash introduces an aside
    if dash != -1:
        cut = min(cut, dash)
    return text[:cut].strip()


def _is_keyless(entry: dict[str, Any]) -> bool:
    """True when the capability works at zero accounts (keyless floor).

    Both light keyless and heavy-render keyless apps satisfy this check;
    use ``_is_heavy_render`` to further distinguish them within the keyless
    tier.
    """
    return (
        entry.get("requires_credential") == "none"
        and entry.get("requires_driver") in _KEYLESS_DRIVERS
    )


def _is_heavy_render(app_id: str) -> bool:
    """True when the capability is keyless but requires the render studio.

    These are listed separately under "Keyless, heavier setup (optional
    studios)" rather than the cold-day-one "Works now (keyless)" block so
    readers are not misled into expecting instant zero-setup wins. The set is
    defined explicitly in ``_HEAVY_RENDER_APPS`` (data-driven, not prose).
    """
    return app_id in _HEAVY_RENDER_APPS


def _group_for(app_id: str, entry: dict[str, Any]) -> str:
    """The owner-facing job group key for a capability.

    Explicit override first; otherwise the slot's default group; if a slot is
    somehow unknown, fold into "plan_and_decide" (the catch-all) rather than
    invent a new bucket — exactly as whats-possible instructs.
    """
    if app_id in _GROUP_OVERRIDES:
        return _GROUP_OVERRIDES[app_id]
    slot = entry.get("function_slot")
    return _SLOT_DEFAULT_GROUP.get(slot, "plan_and_decide")


def build_capabilities(registry: dict[str, Any], skills_dir: Path) -> str:
    """Build the full CAPABILITIES.md text from the registry + skill manifests.

    Deterministic: depends only on the registry contents and the SKILL.md
    frontmatter. No timestamp, commit, or machine state is read or embedded.
    """
    # Collect active capabilities, resolve name + one-liner from SKILL.md.
    # rows: group_key -> list of (plain_name, one_liner, is_keyless,
    # is_heavy_render), each list sorted by plain_name for a stable, scannable
    # order.
    #
    # is_keyless=True + is_heavy_render=False  -> "Works now (keyless)" block
    # is_keyless=True + is_heavy_render=True   -> "Keyless, heavier setup" block
    # is_keyless=False                         -> "Switches on when you connect" block
    rows: dict[str, list[tuple[str, str, bool, bool]]] = {key: [] for key, _, _ in _GROUPS}

    for app_id in sorted(registry):
        entry = registry[app_id]
        if entry.get("status") != "active":
            continue

        meta = _read_meta(skills_dir / app_id / "SKILL.md", app_id)
        plain = _plain_name(app_id, meta)
        liner = _one_liner(app_id, meta)
        keyless = _is_keyless(entry)
        heavy = _is_heavy_render(app_id)
        group_key = _group_for(app_id, entry)
        rows[group_key].append((plain, liner, keyless, heavy))

    for key in rows:
        rows[key].sort(key=lambda r: r[0].lower())

    return _render(rows)  # type: ignore[arg-type]


def _read_meta(skill_md: Path, app_id: str) -> dict[str, Any]:
    """Lift a skill's frontmatter; never crash on a missing/bad file."""
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError as exc:
        print(
            f"[capabilities] {app_id}: cannot read SKILL.md ({exc}); "
            "falling back to id-derived name",
            file=sys.stderr,
        )
        return {}
    try:
        return parse_frontmatter(text)
    except Exception as exc:  # defensive: a parse hiccup can't dark the run
        print(
            f"[capabilities] {app_id}: frontmatter parse failed ({exc}); "
            "falling back to id-derived name",
            file=sys.stderr,
        )
        return {}


_HEADER = (
    "<!--\n"
    "  GENERATED FILE. DO NOT HAND-EDIT.\n"
    "  Generated from kernel/registry.json by tools/export-capabilities.py.\n"
    "  The registry is the source of truth; re-run after changing skills:\n"
    "      python tools/export-capabilities.py\n"
    "-->\n"
)

_INTRO = (
    "# What your Business Operating System can do\n"
    "\n"
    "This is the plain-language list of everything your system can do for you, "
    "grouped by the job it gets done. The **keyless floor** works on day one at "
    "zero accounts and no setup. Connecting a tool **deepens** it: the same "
    "assistant, now reaching into your live business.\n"
)


def _render(rows: dict[str, list[tuple[str, str, bool, bool]]]) -> str:
    """Render the grouped rows into the final Markdown body.

    Each row is (plain_name, one_liner, is_keyless, is_heavy_render).
    Three subgroups per job section:
      - "Works now (keyless)": keyless AND not heavy render — cold day-one wins.
      - "Keyless, heavier setup (optional studios)": keyless but require the
        bundled render stack. Still no accounts needed, but not instant.
      - "Switches on when you connect a tool": requires a credential or
        non-keyless driver.
    """
    parts: list[str] = [_HEADER, "\n", _INTRO]

    for key, title, intro in _GROUPS:
        group_rows = rows.get(key, [])
        if not group_rows:
            continue

        # Three-way split: light keyless | heavy keyless | connect-tier
        keyless_light = [r for r in group_rows if r[2] and not r[3]]
        keyless_heavy = [r for r in group_rows if r[2] and r[3]]
        connect = [r for r in group_rows if not r[2]]

        parts.append("\n")
        parts.append(f"## {title}\n")
        parts.append("\n")
        parts.append(f"{intro}\n")

        if keyless_light:
            parts.append("\n")
            parts.append("**Works now (keyless)**\n")
            parts.append("\n")
            for plain, liner, _kl, _hr in keyless_light:
                parts.append(_bullet(plain, liner))

        if keyless_heavy:
            parts.append("\n")
            parts.append(
                "**Keyless, heavier setup (optional studios)**\n"
            )
            parts.append("\n")
            for plain, liner, _kl, _hr in keyless_heavy:
                parts.append(_bullet(plain, liner))

        if connect:
            parts.append("\n")
            parts.append("**Switches on when you connect a tool**\n")
            parts.append("\n")
            for plain, liner, _kl, _hr in connect:
                parts.append(_bullet(plain, liner))

    return "".join(parts)


def _bullet(plain: str, liner: str) -> str:
    """One capability line: ``- **Plain Name**: one-line what-it-does``.

    A colon (not an em dash) joins the name to the one-liner: this doc is
    GTM-facing copy, and the house content rule bans em dashes as connectors.
    """
    if liner:
        return f"- **{plain}**: {liner}\n"
    return f"- **{plain}**\n"


def _default_repo_root() -> Path:
    """The repo root, resolved via plugin_root() when available."""
    try:
        sys.path.insert(0, str(_TOOLS_DIR.parent))
        from kernel.runtime.paths import plugin_root  # noqa: E402

        return plugin_root()
    except Exception:
        return _TOOLS_DIR.parent


def _default_skills_dir() -> Path:
    return _default_repo_root() / "skills"


def _default_registry_path() -> Path:
    return _default_repo_root() / "kernel" / "registry.json"


def _default_out_path() -> Path:
    return _default_repo_root() / "docs" / "CAPABILITIES.md"


def _load_registry(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate docs/CAPABILITIES.md from kernel/registry.json."
    )
    parser.add_argument(
        "--registry",
        default=None,
        help="Path to registry.json (default: <repo>/kernel/registry.json).",
    )
    parser.add_argument(
        "--skills-dir",
        default=None,
        help="Directory containing skill folders (default: <repo>/skills).",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output path (default: <repo>/docs/CAPABILITIES.md).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the committed CAPABILITIES.md is fresh WITHOUT writing it; "
        "exit non-zero if it has drifted from the registry.",
    )
    args = parser.parse_args(argv)

    registry_path = Path(args.registry) if args.registry else _default_registry_path()
    skills_dir = Path(args.skills_dir) if args.skills_dir else _default_skills_dir()
    out_path = Path(args.out) if args.out else _default_out_path()

    try:
        registry = _load_registry(registry_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(
            f"[capabilities] FAIL: cannot read {registry_path} ({exc})",
            file=sys.stderr,
        )
        return 1

    text = build_capabilities(registry, skills_dir)

    if args.check:
        # Read-only verification. NEVER write the file in --check mode.
        if not out_path.is_file():
            print(
                f"[capabilities] FAIL: {out_path} is missing — run "
                "`python tools/export-capabilities.py` to create it.",
                file=sys.stderr,
            )
            return 1
        committed = out_path.read_text(encoding="utf-8")
        if committed == text:
            print("CAPABILITIES.md up to date", file=sys.stderr)
            return 0
        print(
            f"[capabilities] FAIL: {out_path} is STALE — it drifted from "
            "kernel/registry.json. Fix: run "
            "`python tools/export-capabilities.py` and commit the regenerated "
            "docs/CAPABILITIES.md.",
            file=sys.stderr,
        )
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    active = sum(1 for a in registry if registry[a].get("status") == "active")
    print(
        f"[capabilities] wrote {out_path} — {active} active capabilities",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Team Standards: Starter

> **The single source for how your team operates through Claude Code.** The owner
> (or a manager) edits this ONE file. `/onboard-team-member` reads it and generates
> each teammate's `CLAUDE.md` + memory pack from it, so everyone runs the same
> standards without anyone re-explaining them. When you change something here,
> re-run `/onboard-team-member` for each person to refresh their setup (it shows a
> diff before overwriting).
>
> Edit anything in `<<< ... >>>`. The defaults below already encode the disciplines
> that keep a team consistent: one voice, verify before a customer sees anything,
> clear roles. Keep them unless you have a reason not to.

---

## 1. Team voice (how everyone sounds to customers)

Every customer-facing message (email, SMS, portal note) from anyone on the team uses ONE voice, so the business sounds like one company, not five people. Full spec: `knowledge/communication-voice.md`.

- Plain, warm, reassuring, short. Lead with the outcome, one human sentence on what we did, one clear next step, then stop.
- No jargon, no technical explanations of what went wrong, no internal system detail.
- A customer USES the product; they never "test" or "debug" it. Hand them one clean instruction on how to use it, never a list of things to try.
- One message, not five. Fix the thing, then send one clear note. Multiple emails overwhelm a customer who has less context than you do.
- No hedging ("should work now"). Say what is true.

`<<< Add any voice rules specific to your business, e.g. always sign off with the rep's first name; never quote a price without checking the product catalogue. >>>`

## 2. Verify before a customer hears it (the quality gate)

Nothing customer-facing goes out until the exact thing it is about has been confirmed working. Order, every time:

1. **Claude smoke-tests first** in the workspace (exercise the exact thing; use a test contact so no real customer is notified).
2. **A human confirms** the result by hand.
3. **Only then** does the customer get a short note + one clean instruction on how to use it.

If a teammate drafts something customer-facing that hasn't been verified, it goes to a manager to confirm first. Never tell a customer something is fixed or working before someone has seen it work. Full rail: `knowledge/safeguards.md`.

## 3. Roles and what each can do

Define who is on the team and what they are allowed to do in Claude. `/onboard-team-member` uses the role to scope which commands a person gets and which need manager approval.

| Role | Can read | Can draft | Can send to customers | Can change pipeline / opportunities | Can build/enable automations | Can delete / disable |
|------|----------|-----------|------------------------|--------------------------------------|------------------------------|----------------------|
| `manager` / owner | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `ae` (account exec) | ✅ | ✅ | ✅ (per approval rules below) | ✅ | ❌ | ❌ |
| `sdr` / rep | ✅ | ✅ | drafts only (manager approves) | ❌ | ❌ | ❌ |
| `ops` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

`<<< Adjust the roles and permissions to match your team. Add or remove rows. >>>`

## 4. Approval rules (what needs a manager's OK before it ships)

- `<<< Customer email/SMS on an opportunity over $<<<amount>>> → manager approves before sending. >>>`
- `<<< Anything that disables or deletes a live automation, contact, or deal → manager only. >>>`
- `<<< Drafts from anyone in an "approval-only" role → manager reviews before sending. >>>`

(Platform writes that come back "queued for approval", HTTP 202, are a separate, built-in gate: see `knowledge/safeguards.md`. These rules are your team's human approvals on top of that.)

## 5. Team members

| Name | Email | Role |
|------|-------|------|
| `<<< Owner name >>>` | `<<< owner@business.com >>>` | `manager` |
| `<<< Sarah >>>` | `<<< sarah@business.com >>>` | `sdr` |
| `<<< Bob >>>` | `<<< bob@business.com >>>` | `ae` |

## 6. Escalation + handoffs

- Who do people escalate a stuck deal or an unhappy customer to? `<<< name / role >>>`
- When a deal changes hands, the person handing off logs a short note on the opportunity (what was discussed, commitments made, open questions) so the next person has full context. Claude reads the opportunity's full history on `/prep-for-call`, so the record is the source of truth.

## 7. Team playbooks (optional, Phase 3)

Point to the team's process docs (e.g. "lead qualification", "demo prep", "onboarding a new client") so Claude can follow them when acting for a teammate. `<<< list playbook names / links, or leave blank for now >>>`

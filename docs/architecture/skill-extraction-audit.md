# BOS Skill Extraction Audit

**The question:** strip away TrustPager — does each skill still deliver meaningful standalone value to a business owner with nothing connected? That tells us what the *platform-agnostic* product actually is, and what lives behind the optional "connect TrustPager" section.

> **Provenance / confidence note.** 45 of 58 skills were classified by a dedicated analyst agent each (high confidence; many also passed an adversarial verify pass). The run hit the account session limit before finishing, so the remaining 13 were classified in-thread against the same rubric (the borderline six were read directly). The adversarial *verify* pass did **not** run on ~21 of the "extractable" skills (the agents failed mid-run), so the **extractable bucket is the optimistic read** — a tightening pass would likely demote a few borderline ones (flagged in §6). The headline split is robust; the exact membership of a handful of borderline calls is not yet hardened.

---

## 1. Headline

**35 of 58 skills (≈60%) are standalone-usable** without TrustPager — **11** work with *zero* setup (the floor), **24** work once we swap the data source. Only **23** are genuinely TrustPager-native (live-CRM operations). That validates the pivot hard: BOS can be a genuinely useful business operating system for someone who has never heard of TrustPager — and gets materially deeper when they connect it. TrustPager stops being the product and becomes the most powerful driver in it.

| Bucket | Count | What it means |
|---|---|---|
| 🟢 **general_floor** | 11 | Works minute-one, nothing connected. The "feel powerful immediately" set. |
| 🟡 **extractable** | 24 | Ship a standalone version now; TrustPager deepens it when present. |
| 🔵 **trustpager_native** | 23 | Lives behind "connect TrustPager — here's everything it unlocks." |

---

## 2. The three buckets

### 🟢 Floor — works with zero tools connected (11)
`write-prompt` · `transcript-summary` · `extract-document` · `compare-documents` · `quote-from-photo` · `build-brand-strategy` · `brand-my-workspace` · `make-social-post` · `make-thumbnail` · `onboard-team-member` · `sync-team-standards`

### 🟡 Extractable — standalone with a swapped data source (24)
`learn-my-business` · `audit-my-data` · `build-document` · `build-form` · `template-from-document` · `update-pdf` · `assemble-pack` · `build-knowledge-base-from-docs` · `build-spreadsheet` · `build-customer-voice` · `design-nurture-sequence` · `lint-document` · `lint-form` · `lint-nurture-sequence` · `draft-reply` · `send-email` · `prep-for-call` · `lead-triage` · `follow-up-radar` · `outstanding-invoices` · `outstanding-documents` · `import-from-anywhere` · `delegate-this-work` · `review-team-draft`

### 🔵 TrustPager-native — collapses without the live CRM (23)
`sweep-my-day` · `weekly-review` · `team-review` · `make-it-happen` · `log-this-call` · `missed-call-recovery` · `add-a-field` · `automate-this` · `audit-my-automations` · `why-didnt-it-fire` · `form-radar` · `wire-form` · `test-form` · `build-work-order-process` · `work-order-radar` · `send-for-signing` · `signing-radar` · `nurture-health` · `wire-nurture-sequence` · `email-me-a-report` · `sync-from-xero` · `show-me-how` · `report-an-issue`

---

## 3. The standalone product surface (floor + extractable), grouped by job

What a no-TrustPager owner actually gets — the platform-agnostic product:

- **📄 Documents & paperwork** — extract data from any file (`extract-document`), compare two versions (`compare-documents`), fill a PDF from data you give it (`update-pdf`), merge files into one pack (`assemble-pack`), digitize a paper form/contract into a structured spec (`template-from-document`, `build-form`, `build-document`), build a knowledge base from your docs (`build-knowledge-base-from-docs`), QA a form/doc (`lint-form`, `lint-document`)
- **🎨 Content & brand** — build your brand strategy and voice (`build-brand-strategy`, `build-customer-voice`, `brand-my-workspace`), make social posts and thumbnails (`make-social-post`, `make-thumbnail`), draft a nurture sequence and lint it (`design-nurture-sequence`, `lint-nurture-sequence`)
- **💬 Comms & sales prep** — draft a reply or email (`draft-reply`, `send-email`), prep for a call (`prep-for-call`), triage leads (`lead-triage`), spot quiet follow-ups (`follow-up-radar`), turn a site photo into a quote (`quote-from-photo`), summarize a call/meeting (`transcript-summary`)
- **📊 Data & money** — audit data quality (`audit-my-data`), build a spreadsheet (`build-spreadsheet`), normalize messy imports (`import-from-anywhere`), age receivables (`outstanding-invoices`), chase missing client docs (`outstanding-documents`), hand off work (`delegate-this-work`)
- **🧭 Strategy & team** — write a perfect prompt (`write-prompt`), get set up as a business partner (`learn-my-business` — the onboarding itself), onboard a teammate and keep standards in sync (`onboard-team-member`, `sync-team-standards`), review a teammate's draft (`review-team-draft`)

---

## 4. Extraction specs — how each extractable skill stands alone (and what TrustPager adds)

| Skill | Standalone data source | What TrustPager adds when connected |
|---|---|---|
| learn-my-business | owner describes the business (dictation) | reads the live workspace to enrich + verify the profile |
| audit-my-data | exported contacts/deals/tasks (CSV/XLSX) | live data, real field names, *applies* the fixes in place |
| build-document | owner-described doc / paste | creates the live signing template + merge fields |
| build-form | description or paper form | creates the live form template + fields |
| template-from-document | a local paper/PDF/contract | creates the actual TrustPager form/signing template |
| update-pdf | local blank PDF + data you provide | auto-fills the field values from the live record |
| assemble-pack | a local folder of files | auto-gathers the record's filed forms + uploads, saves pack back |
| build-knowledge-base-from-docs | local policy/FAQ/product docs | publishes into TrustPager AI Knowledge for the assistant/voice agents |
| build-spreadsheet | a standalone sheet / imported Excel | a live "workspace" sheet that pulls from the CRM + auto-creates monthly |
| build-customer-voice | transcripts/notes you provide | pulls every ≥5-min call/meeting transcript automatically |
| design-nurture-sequence | the brand docs + your voice | maps your real help-center videos; feeds `wire-nurture-sequence` |
| lint-document / lint-form / lint-nurture-sequence | a local draft | lints the *live* template/queue in place |
| draft-reply | the message you paste | pulls the full thread + contact history from the record |
| send-email | the content you write | sends via TrustPager Mail with the quality rails + logs it |
| prep-for-call | who you're meeting (paste) | builds the brief from the live opportunity + history |
| lead-triage | a pasted/exported lead list | classifies live inbound + drafts the first response on the record |
| follow-up-radar | an exported pipeline/activity log | live "gone quiet" detection from real `last_activity_at` |
| outstanding-invoices | an exported receivables ledger | live aged receivables from the accounting integration + dashboard email |
| outstanding-documents | a checklist + a folder of received files | tracks asked-vs-arrived against the live record |
| import-from-anywhere | the file/paste you give it | writes the normalized records straight into the workspace |
| delegate-this-work | the business profile (who does what) | creates the assigned task, notifies them, sets your follow-up |
| review-team-draft | a local draft + team standards | pulls the draft from the workspace + checks against the live record |

---

## 5. The "connect TrustPager — here's everything it unlocks" set (23)

These are pure live-CRM operations — they have no standalone meaning and belong behind the optional, non-pushy unlock section:

- **Daily/weekly rhythm:** `sweep-my-day`, `weekly-review`, `team-review`
- **Live CRM actions:** `make-it-happen`, `log-this-call`, `missed-call-recovery`, `add-a-field`
- **Automations:** `automate-this`, `audit-my-automations`, `why-didnt-it-fire`
- **Forms / signing / work orders (live):** `form-radar`, `wire-form`, `test-form`, `build-work-order-process`, `work-order-radar`, `send-for-signing`, `signing-radar`
- **Nurture (live):** `wire-nurture-sequence`, `nurture-health`
- **Reporting / integration / meta:** `email-me-a-report`, `sync-from-xero`, `show-me-how`, `report-an-issue`

---

## 6. Borderline calls & the verify caveat

The verify pass didn't run on most extractables, so these are the ones a tightening pass should re-examine — and my call if forced:

- **`build-form` / `template-from-document`** — standalone they produce a *form spec*, not a working form (no host to collect responses). Real but thinner value (digitizing a paper form for any tool). *Keep extractable, low-confidence.*
- **`send-email`** — only truly standalone once an email-sending driver exists; otherwise it's "draft an email." *Extractable but dependent on a comms driver.*
- **`delegate-this-work`** — standalone "delegate" = draft the assignment + set a reminder; thin without a task system. *Borderline; keep extractable.*
- **`outstanding-invoices` / `outstanding-documents` / `follow-up-radar`** — extractable only if the owner can produce a decent export; "gone quiet" needs activity dates an export may lack. *Keep extractable, watch.*
- **`weekly-review` / `team-review` / `sweep-my-day`** — classified native; in the OS vision these become cross-driver rhythm apps (review across calendar/tasks/email/CRM). *Native today; revisit once non-CRM drivers exist.*

A short re-run of just the verify stage (when the session limit resets) would harden the extractable membership.

---

## 7. Recommended v1 floor — the minute-one win

Smallest set that makes a brand-new owner feel powerful in their first session, before connecting anything. Lead with a **visible artifact** straight off the 60-second info-dump:

1. **`build-brand-strategy`** — turn their dump into positioning + voice. Feels like magic, zero setup.
2. **`write-prompt`** — instant, universal, obviously useful.
3. **`extract-document` / `compare-documents`** — "throw me any file."
4. **`transcript-summary`** — "paste a call, get notes + action items."
5. **`quote-from-photo`** — huge relief for trades; photo + memo → draft quote.
6. **`make-social-post` / `make-thumbnail`** — a shareable, branded image they can post.

`learn-my-business` (the onboarding interview itself) is the spine that runs first and feeds all of the above from the profile.

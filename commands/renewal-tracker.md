---
description: A live renewal tracker .xlsx where the days-until-renewal column is a live formula that recalculates every time the file is opened. Licenses, insurances, certifications, registrations, and memberships in, rows sorted soonest-first, status flags on what is inside the lead window. Keyless, works from what the owner types in.
---

Run the **Renewal Tracker** skill.

Invoke the skill at `skills/renewal-tracker/SKILL.md`. Follow it exactly: take
in each renewable item (name, category, renewal date, optional lead-time), read
the items back in one compact list and get a yes before writing, sort them
soonest-renewal-first, and build the live `.xlsx` tracker via `tools/write_xlsx.py`.

The `.xlsx` IS the required deliverable for this app. Build it. A chat table
alone does not clear the bar.

The days-until-renewal column MUST use a live formula: `=DATE(yyyy,m,d)-TODAY()`
for each row (substituting the year, month, and day from the owner's data), so
the column recalculates from the actual open date every time the owner opens
the file. A static pre-computed number does not clear the bar.

Rows are written soonest-renewal-first (nearest date at row 2, furthest at the
bottom). Include a status flag column using a formula keyed to the days-until
and lead-time columns: "Act now" when inside the lead window, "On track" when
outside, "Renew now" when at or past zero.

Never invent a renewal date. If a date is missing, ask one plain question or
leave the item out and say so.

Handle `BOS_MISSING_DEP:` from `tools/write_xlsx.py` with the
detect-offer-install loop: offer the one-time setup in plain language, run
`python -m pip install openpyxl` on a yes, confirm it worked, then re-run.
Never tell the owner to run a command.

Close with the honest connect-tier split in one line: the keyless file keeps
the tracker current every time it is opened; connecting a CRM or calendar is
what turns the list into reminders that actually fire. Never imply the keyless
file notifies anyone.

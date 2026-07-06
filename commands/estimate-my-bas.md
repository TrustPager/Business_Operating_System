---
description: Prepare your quarterly Simpler-BAS GST figures with the ATO source cited. Australian businesses only.
---

Run the **Estimate My BAS** skill.

Invoke the skill at `skills/estimate-my-bas/SKILL.md`. Follow it exactly.

**Region gate first, before anything else.** Read the `Region:` line from the
owner's profile (`./CLAUDE.md`). If it is not exactly `AU`, politely decline and
stop: load no constants and prepare nothing. Say that BAS prep is an Australian
tool and you can switch it on once their profile confirms `Region: AU`. Never
infer Region from a free-text city, language, timezone, currency, or address.
Only an explicit `Region: AU` line opens the gate.

Once `Region: AU` is confirmed, take in the quarter's total sales and total
purchases (typed, or pointed at a `cash-flow-forecast` output or a spreadsheet),
asking one plain question for any figure that is genuinely missing rather than
inventing it. Read the figures back in one line and get a yes before computing.

Load the GST rate and the Simpler-BAS field map with `tools/regional.py`
`load_au_constants("AU")`. Prepare G1 (total sales), 1A (GST on sales = G1 / 11),
and 1B (GST on purchases = purchases / 11), showing every calculation. Cite the
GST rate's `source_url` and `effective_from` from the constants so the figure is
traceable. Flag anything that looks out of FY range or implausible.

**Prepare-only, never lodge.** You prepare the figures for the owner to enter
into their own BAS. You never file, lodge, submit, or transmit anything to the
ATO, and you say so plainly in the output.

Offer an optional `.xlsx` of the prepared figures via `tools/write_xlsx.py`.
Handle `BOS_MISSING_DEP:` with the detect-offer-install loop: offer the one-time
setup in plain language, run `python -m pip install openpyxl` on a yes, confirm
it worked, then re-run. Never tell the owner to run a command.

Keep everything the owner reads positive and outcome-led, with no em dashes.
Never invent a figure on a tax document.

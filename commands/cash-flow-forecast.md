---
description: A week-by-week cash flow forecast with a live .xlsx where the running balance recalculates when you change a number. Opening balance in, expected inflows and outflows by week out, and you see the tightest week coming so you can plan ahead. Clamped to 4-13 weeks. Folds in basic budgeting (planned vs expected). Keyless, works from what you type in.
---

Run the **Cash Flow Forecast** skill.

Invoke the skill at `skills/cash-flow-forecast/SKILL.md`. Follow it exactly: take
in the opening balance, the horizon (clamped to 4-13 weeks), and the expected
inflows and outflows by week, asking one plain question for any figure that is
genuinely missing rather than inventing it. Read the figures back in one line and
get a yes before computing.

Build the week-by-week running-balance forecast (opening balance + inflows minus
outflows each week, chained forward). Find the tightest week (the lowest closing
balance) and name it as the one to plan cash for. Frame the forecast positively
and outcome-led: the signal is where to plan, not where to worry.

The live `.xlsx` IS the deliverable that separates this from a chat table. Build
it with `tools/write_xlsx.py` where the Net column (=inflows minus outflows) and
the Closing Balance column (=prior balance plus net) are FORMULA cells, not
pre-computed values, so the owner can change any inflow or outflow and every
balance downstream recalculates instantly. Never write a values-only spreadsheet
for this app.

If the owner has planned or budgeted figures alongside expected, include variance
columns. No NPV, no discounting. No separate budgeting app needed.

Handle `BOS_MISSING_DEP:` from `tools/write_xlsx.py` with the detect-offer-install
loop: offer the one-time setup in plain language, run `python -m pip install
openpyxl` on a yes, confirm it worked, then re-run. Never tell the owner to run
a command.

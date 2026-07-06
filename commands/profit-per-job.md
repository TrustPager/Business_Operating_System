---
description: Find out what one job type actually earns you after every cost, with your margin as a dollar figure.
---

Run the **Profit Per Job** skill.

Invoke the skill at `skills/profit-per-job/SKILL.md`. Follow it exactly: pick one
job type and take in its revenue and true costs (materials, labour hours and
rate, a share of overheads, and any financed or depreciating equipment), asking
one plain question for any figure that's missing rather than inventing it. State
the overhead-recovery method openly (percentage of revenue, per-hour, or
per-job). When the job leans on financed or depreciating gear, compute the
real per-job equipment cost with `tools/finance_calc.py` (`pmt` for the finance
repayment, `sln` or `ddb` for depreciation), apportioned to one job, with the
method named. Then take the true cost base off revenue and lay out the result:
the true profit per job, the margin shown as a dollar figure on its own line, the
overhead-recovery method, the equipment math, and the assumptions every number
rests on.

One job type per run. Never invent a cost. The typed read is the win; if they
want a reusable model they can re-cost any time, offer to build a real `.xlsx`
with the document tools (`tools/write_xlsx.py`), pre-filled from their figures
(and from a prior `price-my-work` run when available), but don't make that the
price of the win. This folds in margin, so no separate margin app is needed.

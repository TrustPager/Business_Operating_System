---
name: Profit Per Job
description: Find out what one job type actually makes you, not what it bills. Revenue in, true costs out (materials, labour, a fair share of overheads, and the real per-job cost of any financed or depreciating gear), and you get the profit per job with the margin shown openly as a dollar figure and the overhead-recovery method stated in plain words. Keyless, works from what you type in, with an optional reusable .xlsx model. Folds in margin, so no separate margin app is needed.
triggers:
  - profit per job
  - what does this job actually make me
  - true profit on a job
  - am i making money on this job
  - work out my real margin
  - profit after overheads
  - what's left after costs
  - real profit per job
function_slot: money
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---

# Profit Per Job

An owner picks one job type they do all the time, types in what it brings in and
what it truly costs, and walks away knowing the real number: the profit that job
leaves in their pocket once materials, labour, a fair slice of overheads, and the
genuine per-job cost of any financed or depreciating equipment are all counted.
The margin is shown openly as its own dollar figure, and the overhead-recovery
method is named out loud rather than buried in a total.

This is the partner to `price-my-work`. Where that app builds the price you
charge, this one tells you what one job type actually earns you after everything.
It runs cold on day one, on typed inputs alone. Two things make it real, not a
chat sum:

1. **Library-correct equipment-finance and depreciation math** via
   `tools/finance_calc.py`. When a job leans on financed or depreciating gear,
   the per-job equipment cost comes from `pmt` (the finance repayment) and a
   depreciation figure from `sln` (prime-cost) or `ddb` (diminishing-value), not
   from arithmetic in the head.
2. **An optional reusable `.xlsx` model** via `tools/write_xlsx.py`, pre-filled
   from the owner's figures (and from a prior `price-my-work` run when one is to
   hand), so the same job can be re-costed any time without starting over.

## Step 1: Pick one job type and take in the numbers

The owner names one job type (this app does one per run: if they hand you a few,
do the first and offer the rest one at a time). Gather what you need, and ask
only for the pieces that are genuinely missing:

- **The job type** in their words ("a standard bathroom reseal", "a half-day
  garden tidy", "one custom cabinet build").
- **Revenue** for that job: what it typically brings in (the price, before tax).
- **Direct costs** that belong to the job itself:
  - **Materials** at the owner's cost (what they pay, not what they charge).
  - **Labour**: hours and the rate per hour. A crew works as total crew-hours,
    or hours per head.
- **Overheads**: the share of fixed running costs this job should carry. Don't
  assume one. Ask which method the owner wants (Step 2 names the choices) and
  take the figure or the rate they give.
- **Equipment** (only if the job uses financed or depreciating gear): the asset,
  what it cost, how it's paid for (financed at a rate over a term, or owned and
  depreciating), and how many jobs of this type it serves over the relevant
  period. This drives the finance_calc path in Step 3.

If a number is missing, ask one plain question for it rather than inventing it.
If the owner genuinely doesn't track something (say, overheads), compute what you
can and say plainly that it isn't included, never slip a made-up figure in.

## Step 1b: Read the figures back before you compute (one line)

A wrong figure here flows straight into a profit number the owner may bank a
decision on. Before any maths, play the numbers back in one tight line and get a
yes:

> Here's what I've got for one [job type]: brings in $X, materials $Y, labour Z
> hrs at $R/hr, overheads recovered by [method], and [equipment, if any]. That
> right?

If they correct one, take it and read it back once more so you're both sure.
Only once the inputs are confirmed do you compute.

## Step 2: State the overhead-recovery method openly

Overheads are the part owners most often wave at, so name the method you're using
in plain words rather than folding it silently into a total. Pick the one that
fits how the owner thinks, and say which:

- **Percentage of revenue**: overheads = revenue x overhead%. Simple when the
  owner knows roughly what share of every dollar goes to running the business.
- **Per-hour (overhead rate x job hours)**: overheads = job hours x an hourly
  overhead rate. Fits when fixed costs track with time on the tools.
- **Per-job (a flat slice)**: overheads = a fixed dollar amount per job. Fits
  when each job carries a similar share of fixed costs regardless of size.

Whichever they choose, restate it as one line in the output so the recovered
overhead is legible, not a mystery number. If the owner has no overhead figure at
all, say so openly and compute profit before overheads, labelled as such.

## Step 3: The equipment-finance / depreciation path (finance_calc)

When the job uses financed or depreciating equipment, the per-job equipment cost
is computed with `tools/finance_calc.py`, not estimated. Shell the tool and read
the `{"result": ...}` JSON it prints. Use the periodic finance repayment from
`pmt`, and a depreciation figure from `sln` (prime-cost) or `ddb`
(diminishing-value), then apportion to one job.

**Financed equipment (the per-job slice of the repayment).** Get the periodic
repayment with `pmt`, then divide by the number of jobs of this type the
equipment serves in that same period:

```bash
# Equipment financed at 7.2% per year over 5 years (60 monthly payments) on a $24,000 principal.
# rate is the PERIODIC rate: 0.072 / 12 per month. nper is the number of periods.
python "${CLAUDE_PLUGIN_ROOT}/tools/finance_calc.py" pmt --rate 0.006 --nper 60 --pv 24000
# -> {"result": 477.42...}  (the monthly repayment)
```

Then apportion: if that gear does, say, 40 jobs of this type a month, the per-job
finance cost is monthly repayment / 40. State the apportionment in the output
("$477.42/month over 40 jobs = $11.94 per job").

**Depreciating equipment (the per-job slice of the depreciation).** For owned
gear that wears out, get a periodic depreciation figure, then apportion the same
way. Prime-cost (straight-line) with `sln`, or diminishing-value with `ddb`:

```bash
# Prime-cost: $24,000 asset, $4,000 salvage, 5-year life -> depreciation per YEAR.
python "${CLAUDE_PLUGIN_ROOT}/tools/finance_calc.py" sln --cost 24000 --salvage 4000 --life 5
# -> {"result": 4000.0}  (per year; divide by jobs/year for the per-job slice)

# Diminishing-value (double-declining), first year of a 5-year life:
python "${CLAUDE_PLUGIN_ROOT}/tools/finance_calc.py" ddb --cost 24000 --salvage 4000 --life 5 --period 1
# -> {"result": 9600.0}  (year-1 depreciation; ddb front-loads it)
```

Pick the method the owner uses (prime-cost vs diminishing-value), name it in the
output, apportion the periodic figure across the jobs that period, and show the
per-job number. Use either the finance repayment OR the depreciation figure for a
given asset, not both: financed gear carries the repayment, owned gear carries
the depreciation. If the owner is unsure which method, prime-cost (`sln`) is the
plain default; say you used it.

**If the library is missing.** `finance_calc.py` needs `numpy-financial`. If it
prints a line starting `BOS_MISSING_DEP:` and exits, that's the signal the math
library isn't installed yet. Don't hand-compute the finance or depreciation math
as a workaround. Offer the one-time setup in plain language:

> To work out the true per-job cost of that gear properly, I need to add the
> finance-math tool-kit, a quick free one-time setup on your machine. Want me to
> sort it?

On a yes, run `python -m pip install numpy-financial` yourself, confirm it
worked, then re-run the calc. Never tell the owner to run a command.

## Step 4: Compute the true profit, margin shown openly

Add up the true cost base, then take it off revenue. Show every line so nothing
is a black box.

**True cost base** = materials + labour (hours x rate) + recovered overheads
(by the Step 2 method) + the per-job equipment cost (the finance or depreciation
slice from Step 3, if any).

**True profit per job** = revenue − true cost base.

**Margin, shown openly as money.** Margin is profit as a share of the revenue
(price), and it goes on its own line as a dollar figure AND a percent, never
buried in the total:

- **Margin** (profit as a share of revenue): margin% = profit / revenue.
- Keep the `price-my-work` discipline: margin and markup are different sums.
  Margin is against revenue; markup would be against cost. This app reports the
  margin against revenue, and says so in one line.

Round to sensible money (whole dollars) and say you rounded.

## Step 5: Lay out the result

Present it as a clean read the owner can act on. Outcome-led and plain:

```
## What one [job type] actually makes you

| Line | Detail | Amount |
|------|--------|--------|
| Revenue | what the job brings in | $… |
| Materials | <items> | $… |
| Labour | <hours> hrs x $<rate>/hr | $… |
| Overheads | recovered by <method> | $… |
| Equipment (per job) | <pmt repayment / sln or ddb depreciation>, apportioned | $… |
| **True cost base** | | **$…** |
| **True profit per job** | revenue minus all costs | **$…** |

**Your margin:** you keep **$… (n%)** of revenue on this job once everything is counted.

**Overhead-recovery method:** <percentage of revenue / per-hour / per-job>, stated so it's legible.

**Equipment math:** <e.g. "pmt: $477.42/month over 40 jobs = $11.94/job" or
"sln: $4,000/year over 480 jobs = $8.33/job">, computed with the finance tool.

**Assumptions** (the numbers this rests on):
- <each figure the owner gave, restated for the record>
- <overhead-recovery method used>
- <equipment method used: financed repayment, or prime-cost / diminishing-value depreciation>
- <rounding applied>
- <anything left out, e.g. "overheads not included: none given">
```

Frame it forward: this is the number the owner can trust when they decide which
jobs to chase more of.

## Step 6: Offer the reusable .xlsx model (optional, never the win)

The read above IS the win: complete and usable as text. If the owner wants a
model they can keep and re-cost any time, offer to build a real `.xlsx` with
`tools/write_xlsx.py`, pre-filled from their figures:

> Want this as a reusable spreadsheet model? I can build the same breakdown as a
> real `.xlsx` you can open, save, and re-run for the next job, pre-filled with
> your numbers.

Build the rows as a JSON array of arrays (the breakdown above, line by line) and
write it. Pre-fill from the owner's figures, and pull rate defaults from their
profile or a prior `price-my-work` run when one is available, so the model
starts populated rather than blank:

```bash
python "${CLAUDE_PLUGIN_ROOT}/tools/write_xlsx.py" --out "profit-per-job.xlsx" --rows '[["Line","Detail","Amount"],["Revenue","what the job brings in",1800],["Materials","reseal kit + sundries",120],["Labour","4 hrs x $70/hr",280],["Overheads","12% of revenue",216],["Equipment (per job)","pmt $477.42/mo over 40 jobs",11.94],["True cost base","",627.94],["True profit per job","revenue minus all costs",1172.06]]' --sheet "Profit per job" --header
```

- `--header` makes the first row bold.
- `--sheet` titles the tab.
- If the wrapper prints a line starting `BOS_MISSING_DEP:` (openpyxl missing),
  offer the same one-time setup in plain language and, on a yes, run
  `python -m pip install openpyxl` yourself, then re-run. Don't hand-build the
  file another way.

Offer it, don't make it the price of the win. Most of the time the typed read is
all the owner needs.

End with: *"That's the true profit on one [job type], margin and overheads and
gear all counted. Want it as a reusable spreadsheet model, or should we run the
next job type?"*

## Hard rules

- **One job type per run.** Cost one job type properly. If handed several, do the
  first and offer the rest one at a time.
- **Never invent a cost figure.** Every number comes from the owner. If something
  is missing, ask one question or leave it out and say so, never assume a figure
  into the profit.
- **Use the real finance math.** When a job leans on financed or depreciating
  gear, the per-job equipment cost is computed with `tools/finance_calc.py`
  (`pmt` for the repayment; `sln` or `ddb` for depreciation), apportioned to one
  job, with the method named. Do not hand-wave it.
- **Margin shown openly, as money.** Profit and margin each get their own line
  and their own dollar figure, never buried in the total. Margin is against
  revenue; say so.
- **State the overhead-recovery method.** Name which method recovered the
  overhead (percentage of revenue, per-hour, or per-job) in the output, so the
  recovered figure is legible rather than a mystery.
- **Customer-facing output stays positive and outcome-led.** The read describes
  what the job earns and what the owner keeps, never pain or what's missing.
  (Naming a missing figure to the owner while gathering inputs is fine: that's
  discovery, not the shipped number.)
- **No accounts, no files needed.** This runs on typed inputs alone. The `.xlsx`
  model is an optional add-on, never a dependency for the win.
- **No em dashes in anything the owner reads.** Use commas, colons, or periods.

## Output shape

The true-profit table (revenue minus materials, labour, recovered overheads, and
the per-job equipment cost), then the profit and the margin each called out on
their own line as money, then the overhead-recovery method and the equipment math
stated plainly, then the assumptions list, then the optional offer of a reusable
`.xlsx` model. Concrete and fast: a number the owner can act on in the next
minute.

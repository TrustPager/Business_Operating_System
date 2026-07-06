---
name: Cash Flow Forecast
description: A week-by-week cash flow forecast with a live .xlsx where the running balance recalculates when you change a number. Opening balance in, expected inflows and outflows by week out, and you see the tightest week coming so you can plan ahead. Clamped to 4-13 weeks. Folds in basic budgeting (planned vs expected). Keyless, works from what you type in.
triggers:
  - cash flow forecast
  - will i make rent
  - can i cover payroll
  - runway
  - tight month
  - tight week
  - what's coming in and going out
  - cash forecast
  - weekly cash forecast
  - do i have enough cash
  - cash position
  - how long can i last
  - money coming in and out
  - cash planning
  - when do i run low
function_slot: money
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
---

# Cash Flow Forecast

An owner types in what they expect to come in and go out each week over the coming
weeks, and walks away with a week-by-week running-balance forecast that shows the
tightest week clearly so they can plan for it rather than be surprised by it. The
deliverable is a **live `.xlsx`** where the running-balance column is a formula, not
a pre-computed number, so changing a single inflow or outflow instantly recalculates
every balance that follows.

This is the planning partner to `profit-per-job` and `price-my-work`. Those apps
tell you what one job earns; this one tells you whether the overall inflows and
outflows over the next several weeks keep you comfortably ahead or put a specific
week under pressure. Folds in basic budgeting (planned vs expected), so no separate
budgeting app is needed.

**The horizon is clamped to 4-13 weeks.** Fewer than four weeks is too short for
planning decisions; more than 13 is where small-business cash predictions become
unreliable. If the owner asks for anything outside that range, reset it gently to
the nearest bound and say so.

## Step 1: Take in the inputs

Gather these, and ask only for the pieces that are genuinely missing:

- **Opening balance** (the cash balance in the account today, or at the start of
  Week 1). Required. If the owner is unsure of the exact figure, a close estimate
  is fine; flag that you're using an estimate.
- **Horizon** (the number of weeks to forecast). Required. Clamp silently to 4-13
  if the owner gives something outside that range and note the adjustment in one
  line.
- **Expected inflows by week** (what cash you expect to land: invoices getting
  paid, recurring contract payments, seasonal jobs, any other cash arriving). Ask
  for the regular pattern (e.g. "$4,000/week most weeks") plus any known
  exceptions (e.g. "Week 3 a big invoice pays, $18,000"). If the pattern is flat,
  one number covers all weeks.
- **Expected outflows by week** (what you expect to pay out: wages/contractor
  pays, supplier invoices, rent, loan repayments, tax instalments, any other
  regular or known spend). Same pattern-plus-exceptions approach.
- **Planned vs expected (optional budgeting view):** if the owner also has a
  planned or budgeted figure for inflows or outflows, note it alongside the
  expected figure so the forecast can show the gap each week. If they don't track
  this, leave it out and say so.

If a number is missing, ask one plain question for it rather than inventing it. If
the owner genuinely can't estimate something, compute what you can and mark that
line as "estimate needed."

## Step 2: Read the figures back before you compute (one line)

A wrong figure here flows into every balance that follows. Before any maths, play
the numbers back in one tight summary and get a yes:

> Here's what I've got: opening balance $X, weeks 1-N, inflows averaging $Y/week
> (with [any exceptions]), outflows averaging $Z/week (with [any exceptions]).
> That right?

If they correct one, take it and read it back once more. Only then compute.

## Step 3: Build the week-by-week forecast

Compute the running balance for each week:

```
Week 1 balance = opening balance + Week 1 inflows - Week 1 outflows
Week 2 balance = Week 1 balance + Week 2 inflows - Week 2 outflows
...
Week N balance = Week N-1 balance + Week N inflows - Week N outflows
```

Find the **tightest week**: the week with the lowest closing balance. This is the
planning signal, not a warning. Frame it forward: this is the week to have planned
cash for.

If the owner provided planned/budgeted figures alongside expected, compute the
variance for inflows and outflows each week (expected minus planned) and include
it as its own columns in the table.

## Step 4: Lay out the forecast

Present it as a clean, readable table the owner can act on:

```
## Your cash flow forecast: Weeks 1-N

Opening balance: $X

| Week | Inflows | Outflows | Net | Closing balance | [Variance, if budget given] |
|------|---------|----------|-----|-----------------|----------------------------|
|  1   | $...    | $...     | $.. | $...            | $...                       |
|  2   | $...    | $...     | $.. | $...            | $...                       |
...
|  N   | $...    | $...     | $.. | $...            | $...                       |

**Tightest week:** Week [N] closes at $[X], so this is the week to plan your cash for.

**Assumptions** (the numbers this forecast rests on):
- Opening balance: $X [confirmed / estimated]
- Inflows: [pattern description, plus any exceptions]
- Outflows: [pattern description, plus any exceptions]
- [Planned/budget figures used, if any]
- [Anything left out: "outflows for [X] not included: none given"]
- Horizon clamped to [N] weeks [if adjustment made]
```

If any week has a negative closing balance, name it plainly in one line as the
week that needs attention, and frame the action forward: "Week [N] is the one to
plan cash around."

Frame everything positively and outcome-led. The forecast tells the owner where
the opportunity to plan is, not where the danger is.

## Step 4b: Offer the doctrine levers (after the win, never before)

The forecast is the win; these are optional next moves once it has landed.
Offer at most one at a time, only where it fits, and model anything the owner
takes up as labelled scenario rows so the base forecast stays untouched:

1. **A tight week showing?** Offer to model the cash pull-forward toolkit
   (per `knowledge/business-method.md` §9.5) as labelled scenario rows, e.g.
   "deposit on booking" or "billing on completion day", so the owner sees the
   same revenue landing earlier.
2. **Offer a price-rise scenario** using the price-rise maths (§17): a
   labelled scenario showing the weeks at the raised price.
3. **Owner wants a profit line?** Add a fixed profit set-aside as its own
   outflow row. Profit is a discipline (§13): set the line first and make the
   weeks fit it, not the reverse.
4. **Owner spends on acquisition and can name what a new customer pays and
   costs in the first 30 days?** Run the two-tier 30-day cash check (§9.2)
   and report which bar they clear.

## Step 5: Build the live .xlsx with formula cells

The live spreadsheet IS the deliverable that makes this real. After the typed
forecast, offer it:

> Want this as a live spreadsheet? I can build a real `.xlsx` where the running
> balance updates automatically when you change any inflow or outflow, so you can
> model your own scenarios without starting over.

On a yes (or when the owner clearly wants a spreadsheet from the start), build it
with `tools/write_xlsx.py`. The running-balance column must use FORMULAS so the
owner can change a number and every balance downstream recalculates.

**Column layout (one row per week):**

| Col | Content |
|-----|---------|
| A   | Week label ("Week 1", "Week 2", ...) |
| B   | Inflows (numeric value the owner gave) |
| C   | Outflows (numeric value the owner gave) |
| D   | Net (formula: =B2-C2, =B3-C3, ...) |
| E   | Closing balance (formula: prior balance + net) |
| F   | Planned inflows (if budget data given, else omit) |
| G   | Planned outflows (if budget data given, else omit) |
| H   | Variance (formula: =B2-F2, etc., if budget data given) |

Row 1 is the header (bold). Row 2 is Week 1. The opening balance sits in a
dedicated cell (E1 label row, or a named row above Week 1) so the formula chain
anchors to it cleanly.

**Exact formula pattern for a 4-week example (opening balance in cell E1 as a
labelled data row):**

```
Row 1 (header): ["Week","Inflows","Outflows","Net","Closing balance"]
Row 2 (opening): ["Opening balance","","","","<opening_balance_value>"]
Row 3 (Week 1):  ["Week 1", <inflow_1>, <outflow_1>, "=B3-C3", "=E2+D3"]
Row 4 (Week 2):  ["Week 2", <inflow_2>, <outflow_2>, "=B4-C4", "=E3+D4"]
Row 5 (Week 3):  ["Week 3", <inflow_3>, <outflow_3>, "=B5-C5", "=E4+D5"]
Row 6 (Week 4):  ["Week 4", <inflow_4>, <outflow_4>, "=B6-C6", "=E5+D6"]
```

The owner changes any inflow or outflow value in column B or C, and the entire
closing-balance column recalculates. That is the live behaviour.

**The write_xlsx command (generalised for N weeks, formula rows written from the
JSON array):**

```bash
python ~/.claude/bos-run.py tool write_xlsx \
  --out "cash-flow-forecast.xlsx" \
  --sheet "Cash Flow" \
  --header \
  --rows '[
    ["Week","Inflows","Outflows","Net","Closing balance"],
    ["Opening balance","","","","<opening_balance>"],
    ["Week 1",<inflow_1>,<outflow_1>,"=B3-C3","=E2+D3"],
    ["Week 2",<inflow_2>,<outflow_2>,"=B4-C4","=E3+D4"],
    ...
    ["Week N",<inflow_N>,<outflow_N>,"=B<N+2>-C<N+2>","=E<N+1>+D<N+2>"]
  ]'
```

(The `~/.claude/bos-run.py` launcher resolves the install location for you. If it is missing, run `python tools/setup.py` once from the BOS directory to create it.)

Fill in the actual inflow and outflow values from the owner's inputs. The formula
strings (beginning with `=`) are written by openpyxl as live formula cells, not
text, so they recalculate when the owner edits any value in the spreadsheet.

**If the JSON carries any non-ASCII characters** (currency symbols beyond `$`,
accented names), write the rows to a UTF-8 temp file and pipe it in on stdin
instead of passing it after `--rows`:

```bash
python ~/.claude/bos-run.py tool write_xlsx --out "cash-flow-forecast.xlsx" --sheet "Cash Flow" --header < rows.json
```

**If openpyxl is missing.** The tool prints a line starting `BOS_MISSING_DEP:`
and exits. Don't hand-build the file another way. Offer it in plain language:

> To build that live spreadsheet I need to add the document tool-kit, a quick
> free one-time setup on your machine. Want me to sort it?

On a yes, run `python -m pip install openpyxl` yourself, confirm it worked, then
re-run the write command. Never tell the owner to run anything.

## Step 6: Close the loop

After the forecast (and the spreadsheet, if built):

> "That's your cash picture for the next [N] weeks, with Week [X] as the one to
> plan cash for. Change any number in the spreadsheet and the balance updates.
> Want to model a different scenario, run a forecast for a different horizon,
> or feed this into your weekly scoreboard?"

(The weekly scoreboard is the operating cadence per
`knowledge/business-method.md` §12.6.)

## Hard rules

- **Horizon clamped to 4-13 weeks.** Always. State the adjustment in one line if
  you apply it.
- **Never invent a figure.** Every number comes from the owner. If something is
  missing, ask one question or leave it out and say so.
- **No NPV, no discounting.** A horizon under 13 weeks makes discounting noise,
  not insight. This app does not call finance_calc and does not do NPV.
- **The live .xlsx is the differentiator.** The running-balance column is always a
  formula, not a pre-computed value. A values-only spreadsheet does not clear the
  bar for this app.
- **Customer-facing output stays positive and outcome-led.** The forecast names
  what to plan for, never what to fear.
- **No em dashes in anything the owner reads.** Use commas, colons, or separate
  sentences.
- **Folds in basic budgeting.** If the owner has planned/budgeted figures,
  include them as variance columns. No separate budgeting app needed.
- **Doctrine levers come after the forecast lands.** Offer them one at a time,
  model each as labelled scenario rows, and never gate the core forecast on
  any of them.

## Output shape

Opening balance and horizon stated up front, then the week-by-week table
(inflows, outflows, net, closing balance, plus planned/variance columns if budget
data is given), then the tightest week called out as a forward-planning signal,
then the assumptions list, then the live `.xlsx` built with formula cells via
`tools/write_xlsx.py`.

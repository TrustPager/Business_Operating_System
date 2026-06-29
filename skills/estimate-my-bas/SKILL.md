---
name: Estimate My BAS
description: For Australian businesses. Prepare your quarterly Simpler-BAS GST figures (G1 total sales, 1A GST on sales, 1B GST on purchases) from the quarter's sales and purchases, with the GST calculation method shown and the ATO source for the rate cited. Prepare-only: I lay out the numbers for you to enter into your own BAS, I never lodge anything. Keyless, works from what you type in, with an optional .xlsx of the prepared figures. Switches on only once your profile confirms Region: AU.
triggers:
  - estimate my bas
  - prepare my bas
  - work out my gst for the quarter
  - bas figures
  - simpler bas
  - g1 1a 1b
  - gst on sales and purchases
  - quarterly gst
  - business activity statement
function_slot: accounting
requires_driver: none
requires_credential: none
data_path: reasoning_only
requires_region: AU
status: active
---

# Estimate My BAS

An Australian business owner hands you the quarter's total sales and total
purchases, and walks away with their Simpler-BAS GST figures laid out and ready
to enter: **G1** (total sales), **1A** (GST on sales), and **1B** (GST on
purchases), each with the calculation shown openly and the ATO source for the
GST rate cited so every figure is traceable. This app prepares the numbers. It
never lodges anything: you enter them into your own BAS yourself.

This is the Australian tax partner to `cash-flow-forecast` and `profit-per-job`.
Those run for any business anywhere; this one is Australia-only and stays switched
off until the owner's profile explicitly confirms `Region: AU`.

## Step 0: The region gate (do this FIRST, before anything else)

BAS is an Australian tax instrument, so this app runs only for an owner who has
explicitly confirmed their business is in Australia. **Before you load any
constants, gather any figures, or prepare anything, read the `Region:` line from
the owner's profile (`./CLAUDE.md`).**

```bash
test -f ./CLAUDE.md && grep -i "^Region:" ./CLAUDE.md || echo "NO_REGION"
```

**Decide from that line alone:**

- If the `Region:` line is **exactly `AU`** (`Region: AU`), the gate is open.
  Continue to Step 1.
- If the `Region:` line is **anything else** (blank, missing, a placeholder like
  `<<< AU if your business is in Australia ... >>>`, or any other value),
  **politely decline and STOP.** Do not load constants. Do not prepare any
  figures. Say plainly, in your own warm words, something like:

  > BAS prep is an Australian tax tool, so I keep it switched off unless your
  > profile confirms your business is in Australia. If that's you, just say so
  > and I'll set `Region: AU` in your profile, then we can run it. If not, no
  > worries, your cash flow and pricing tools all work the same wherever you are.

**Never infer Region from anything else.** The free-text "based in <city,
country>" line in the profile is descriptive only: even if it names an
Australian city (Sydney, Brisbane, Perth), that does NOT open the gate. Language,
timezone, currency, and address never open it either. Only an explicit
`Region: AU` line does. If the owner says "yes, I'm in Australia," the right move
is to record `Region: AU` in their profile first (or point them at
`/start-here`'s region question), then run.

## Step 1: Take in the quarter's figures

Once `Region: AU` is confirmed, gather what you need, and ask only for the pieces
that are genuinely missing:

- **Total sales for the quarter** (the GST-inclusive total of all sales for the
  period). This becomes **G1**. You can take a figure the owner types in, or
  point at a `cash-flow-forecast` output or a spreadsheet they already have.
- **Total purchases for the quarter** on which they are claiming GST credits
  (the GST-inclusive total of business purchases). This drives **1B**.
- **Whether sales and purchases are fully taxable** (the standard case) or
  include GST-free or input-taxed lines. Simpler-BAS divide-by-11 assumes fully
  taxable amounts; if a chunk is GST-free (some food, exports), say so and only
  apply the GST calc to the taxable portion.
- **Which quarter** it is (e.g. Q1 July-September), so the figure is labelled.

If a number is missing, ask one plain question for it rather than inventing it.
Never put a made-up figure into a tax number the owner may rely on.

## Step 1b: Read the figures back before you compute (one line)

A wrong figure here flows straight into a number the owner enters on a government
form. Before any maths, play the numbers back in one tight line and get a yes:

> Here's what I've got for [quarter]: total sales $X (GST-inclusive), total
> purchases $Y (GST-inclusive), all fully taxable. That right?

If they correct one, take it and read it back once more. Only once the inputs are
confirmed do you compute.

## Step 2: Load the AU constants (the GST rate and the BAS field map)

Get the GST rate and the Simpler-BAS field definitions from the region-gated
constants loader, never from memory. The loader returns the AU constants only
for `region == "AU"` and raises for anything else, so it is a second backstop on
the gate:

```bash
python -c "from tools.regional import load_au_constants; import json; c = load_au_constants('AU'); print(json.dumps({'rate': c['gst']['rate'], 'calc': c['gst']['calc_method'], 'fields': {k: c['gst']['bas_fields'][k]['label'] for k in ('G1','1A','1B')}}, indent=2))"
```

Read the GST rate (`c["gst"]["rate"]["value"]`, currently 0.10), the calc method
(`c["gst"]["calc_method"]`, divide-by-11 for a GST-inclusive amount), and the
G1 / 1A / 1B field definitions from `c["gst"]["bas_fields"]`. Use these values;
do not hand-type the rate.

## Step 3: Prepare G1, 1A, 1B with the calculation shown

Compute each field openly so nothing is a black box. For fully taxable amounts,
the GST inside a GST-inclusive price is the price divided by 11 (the constants'
`calc_method`):

- **G1 (total sales):** the GST-inclusive total of all sales for the quarter,
  taken straight from the owner's figure. G1 = total sales.
- **1A (GST on sales):** the GST collected on taxable sales = taxable sales / 11.
  Show the division: "1A = G1 / 11 = $X".
- **1B (GST on purchases):** the GST credits on creditable purchases = taxable
  purchases / 11. Show the division: "1B = purchases / 11 = $Y".
- **Net GST position (for the owner's information, not a BAS field on its own):**
  net GST = 1A minus 1B. If 1A is larger, that's roughly what they remit; if 1B
  is larger, it points to a refund position. State it as a plain-English read,
  not as advice.

Round to sensible money and say you rounded. If any line is GST-free or
input-taxed, exclude it from the divide-by-11 and say which portion you treated
as taxable.

## Step 4: Cite the provenance (so the figure is traceable)

In the output, show where the GST rate comes from, straight from the constants
module, so the owner (or their accountant) can trace it:

- the GST rate's `source_url` (the ATO page) and its `effective_from` date, both
  read from `c["gst"]["rate"]`.

State it plainly, e.g.:

> GST rate: 10% (effective from 2000-07-01). Source: the ATO "how GST works"
> page (`c["gst"]["rate"]["source_url"]`).

This is what makes the prepared figure auditable rather than a guess.

## Step 5: Sanity-check the figures

Before you present, glance at the numbers and flag anything that looks off rather
than presenting it silently:

- If purchases exceed sales by a wide margin (a large refund position) for a
  business that is normally net-positive, name it plainly as worth a second look.
- If a figure looks out of range for the quarter (e.g. a quarter's sales that
  look like a full year, or a number with a likely misplaced decimal), say so and
  ask the owner to confirm before they rely on it.
- If the owner mentioned GST-free or input-taxed sales but gave only one lump
  total, note that the divide-by-11 assumes fully taxable and that the GST-free
  portion should be carved out for an accurate 1A.

You are preparing figures, not auditing the business: a light, honest "this looks
worth a check" is the right touch, never a made-up correction.

## Step 6: Lay out the result

Present it as a clean read the owner can enter straight into their BAS:

```
## Your Simpler-BAS GST figures: [quarter]

| Field | What it is | Calculation | Amount |
|-------|------------|-------------|--------|
| G1 | Total sales (GST-inclusive) | as supplied | $… |
| 1A | GST on sales | G1 / 11 | $… |
| 1B | GST on purchases | purchases / 11 | $… |

**Net GST position:** 1A minus 1B = $… (for your information; enter G1, 1A and 1B on your BAS).

**GST rate used:** 10%, effective from 2000-07-01. Source: ATO "how GST works" (<source_url>).

**Assumptions** (the numbers this rests on):
- Quarter: [which quarter]
- Total sales (G1): $… [confirmed]
- Total purchases: $… [confirmed]
- Treated as fully taxable [or: GST-free portion carved out: $…]
- GST calc: divide-by-11 on GST-inclusive amounts
- Rounding applied: [how]

**You enter these. I don't lodge.** These are prepared for you to type into your
own BAS through the ATO (myGov / Online services for business) or your registered
agent. I have not filed, lodged, or submitted anything.
```

Frame it forward: this is the set of numbers the owner can enter with confidence,
each one traceable to its source.

## Step 7: Offer the reusable .xlsx (optional, never the win)

The read above IS the win: complete and usable as text. If the owner wants the
prepared figures as a file they can keep with their records, offer to build a
real `.xlsx` with `tools/write_xlsx.py`, pre-filled from their figures:

> Want these figures as a spreadsheet you can keep with your quarter's records? I
> can lay the same G1 / 1A / 1B breakdown out as a real `.xlsx` you can open and
> save.

Build the rows as a JSON array of arrays (the breakdown above, line by line) and
write it:

```bash
python ~/.claude/bos-run.py tool write_xlsx --out "bas-figures.xlsx" --rows '[["Field","What it is","Calculation","Amount"],["G1","Total sales (GST-inclusive)","as supplied",44000],["1A","GST on sales","G1 / 11",4000],["1B","GST on purchases","purchases / 11",1200],["Net GST","1A minus 1B","",2800]]' --sheet "BAS figures" --header
```

(The `~/.claude/bos-run.py` launcher resolves the install location for you. If it is missing, run `python tools/setup.py` once from the BOS directory to create it.)

- `--header` makes the first row bold.
- `--sheet` titles the tab.
- If the wrapper prints a line starting `BOS_MISSING_DEP:` (openpyxl missing),
  offer the same one-time setup in plain language and, on a yes, run
  `python -m pip install openpyxl` yourself, then re-run. Don't hand-build the
  file another way. Never tell the owner to run a command.

Offer it, don't make it the price of the win. Most of the time the typed read is
all the owner needs.

End with: *"Those are your G1, 1A and 1B ready to enter on your BAS, GST rate
sourced and the working shown. Want them as a spreadsheet for your records, or is
that you sorted for the quarter?"*

## Hard rules

- **Region gate first, every run.** Read the `Region:` line from `./CLAUDE.md`
  before anything else. If it is not exactly `AU`, decline politely and stop:
  load no constants, prepare nothing. Never infer Region from a free-text city,
  language, timezone, currency, or address. Only an explicit `Region: AU` opens
  the gate.
- **Prepare-only, NEVER lodge.** You prepare the G1 / 1A / 1B figures for the
  owner to enter into their own BAS. You never file, lodge, submit, or transmit
  anything to the ATO, and you say so plainly in every output. This is a tax
  document the owner is responsible for.
- **Never invent a figure.** Every number comes from the owner. If something is
  missing, ask one plain question or leave it out and say so. A made-up figure on
  a tax form is never acceptable.
- **Use the loaded constants, not memory.** The GST rate, the calc method, and
  the BAS field definitions come from `tools/regional.py` `load_au_constants("AU")`,
  and the GST rate's source and effective date are cited in the output.
- **Show the working.** Every field shows its calculation (G1 as supplied, 1A and
  1B as divide-by-11), so the owner and their accountant can follow it.
- **Not tax advice.** This prepares figures and shows the method. It is not a
  substitute for a registered tax agent. If the situation is non-standard, say so
  and suggest they confirm with their agent.
- **Customer-facing output stays positive and outcome-led.** The read describes
  the figures ready to enter and the confidence that brings, never pain or what's
  missing. No em dashes in anything the owner reads: use commas, colons, or
  separate sentences.

## Output shape

The Simpler-BAS table (G1 total sales, 1A GST on sales, 1B GST on purchases, each
with its calculation shown), then the net GST position as a plain read, then the
cited GST rate with its ATO source and effective date, then the assumptions list,
then the prominent prepare-only / never-lodge line, then the optional offer of a
reusable `.xlsx`. Traceable and ready to enter: numbers the owner can put on their
BAS in the next few minutes, each one sourced.

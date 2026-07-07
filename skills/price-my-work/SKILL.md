---
name: Price My Work
description: Turn the costs of a common job into a priced breakdown you can stand behind — line items, your margin shown openly, the total, and the assumptions written down so the number holds up when a customer asks how you got there. Keyless, works from what you type in. The pricing engine quote-from-photo and write-a-proposal lean on.
triggers:
  - price my work
  - what should i charge
  - price this job
  - work out my price
  - cost this job up
  - how much should i quote
  - build me a priced breakdown
  - price a job with margin
function_slot: money
requires_driver: none
requires_credential: none
data_path: reasoning_only
status: active
produces_customer_facing_copy: true
---

# Price My Work

An owner describes a job they do all the time, types in what it costs them
(materials, hours, labour rate, overheads), and says the margin they want.
You give back a priced breakdown they can stand behind: every line shown, the
margin shown openly as its own number, the total, and the assumptions written
down so when a customer asks "how did you get to that?" the answer is right
there on the page.

This is pure reasoning over what the owner types — no accounts, no files, no
catalogue. It runs cold on day one. It's also the pricing engine other apps
borrow: when quote-from-photo or write-a-proposal needs a defensible number,
this is the maths underneath.

## Step 1 — Take in the job and the costs

The owner describes one job (this skill prices one job per run — if they
hand you a list, price the first and offer to do the rest one at a time).
Gather what you need, and ask for only the pieces that are actually missing:

- **The job** — what it is, in their words ("supply and lay 40m² of
  laminate", "full interior repaint, three-bed", "10-hour wedding shoot").
- **Materials** — items and their cost to the owner (what they pay, not what
  they charge). Quantities where they matter.
- **Labour** — hours, and the rate per hour. If a crew, hours per person or a
  total crew-hours figure works.
- **Overheads** — the costs that aren't materials or labour but belong to this
  job: travel, equipment hire, tip fees, a cut for consumables, a share of
  fixed running costs if they price that way. Take what they give you.
- **Target margin** — the margin they want to make on top of cost, as a
  percentage. Confirm you both mean the same thing (see the margin note in
  Step 2) so the number is the one they expect.

If a number is missing, ask one plain question for it rather than inventing it.
If they genuinely don't track something (say, overheads), price what you have
and note that overheads aren't included, don't silently assume a figure.

## Step 1b: Read the figures back before you compute (one line)

Owners fumble numbers out loud, and a wrong figure here flows straight into a
total they might quote a customer. Before you do any maths, play the costs back
in one tight line and get a yes:

> Here's what I've got for your costs: materials $X, labour Y hrs at $Z/hr,
> overheads $W, and you want a [n]% margin. That right?

Keep it to the numbers (no full breakdown yet, that's Step 3). If they correct
one, take the correction and read it back once more so you're both sure. Only
once the inputs are confirmed do you compute the total. This costs one line and
saves a wrong number going out in a quote.

## Pricing gates (check before you compute)

Four checks between the read-back and the maths. Each is one question; most
jobs pass straight through.

1. **The cost floor is the floor.** The Step 2 cost base is the lowest number
   this job can carry (per `knowledge/business-method.md` §8.6). If the
   owner's target margin or a price they've already named lands below it,
   stop and say so before presenting anything. Never write a below-floor
   price into the breakdown.
2. **The capacity check.** If the owner has said they're booked out or
   turning work away, the capacity rule applies (price, not volume, per
   §8.3): price this job with a rise in mind, not at the old rate.
3. **The close-rate signal (optional, one question, skip if unknown).** You
   may ask once: "roughly what share of quotes like this do you win?" If the
   share is very high, flag likely underpricing per the directional
   close-rate signal (§8.2) and offer to price a raised version alongside
   the one they asked for.
4. **Never anchor on the competition.** Never price from "competitor average
   minus a bit" (§8.5). The price comes from the owner's costs and the value
   of the work.

## Step 2 — Do the maths, margin shown openly

Add up the cost base, apply the margin, and show every step so nothing is a
black box.

**Cost base** = materials + labour (hours × rate) + overheads. List each line
with its own subtotal so the owner can see where the money goes.

**Margin — be explicit about which kind, then show it as money.** "Margin" and
"markup" are different sums and getting it wrong loses real money:

- **Margin** (profit as a share of the *price*): price = cost ÷ (1 − margin%).
  A 30% margin on a $1,000 cost gives a $1,428.57 price, with $428.57 profit.
- **Markup** (profit as a share of the *cost*): price = cost × (1 + markup%).
  A 30% markup on a $1,000 cost gives a $1,300 price, with $300 profit.

Default to **margin** unless the owner says markup, and say which you used in
one line. Always show the margin amount as a dollar figure, not just a percent,
so it reads as real money on the page.

**Total** = cost base + margin amount (the price). If they want it shown with
tax (GST or similar), add it as its own line on top of the total and label it
clearly — keep the pre-tax price and the tax separate so both are legible.

Round to sensible money (whole dollars, or to the nearest five/ten if that's
how they quote) and say you rounded.

## Step 3 — Lay out the breakdown

Present it as a clean breakdown the owner could read straight to a customer,
plain and clear. This is what the owner stands behind:

```
## Priced breakdown: <job, in their words>

| Line item | Detail | Amount |
|-----------|--------|--------|
| Materials | <items, qty> | $… |
| Labour | <hours> hrs × $<rate>/hr | $… |
| Overheads | <travel, hire, fees…> | $… |
| **Cost base** | | **$…** |
| Margin (<n>% on price) | your profit on this job | $… |
| **Total price** | | **$…** |
| GST / tax (if shown) | <rate>% | $… |
| **Total incl. tax** | | **$…** |

**The margin:** you make **$… (n%)** on this job at this price.

**Assumptions** (the numbers this rests on):
- <each cost figure the owner gave, restated so it's on the record>
- <margin type used: margin vs markup>
- <rounding applied>
- <anything left out, e.g. "overheads not included: none given">

**Stand behind it:** one or two plain lines the owner can say to a customer
explaining what's in the price and why it's fair.
```

The stand-behind lines name what the customer ends up with (the Arrival, per
`knowledge/business-method.md` §6), not the cost ledger.

## Step 4 — Offer the clean spreadsheet (optional, never the win)

The breakdown above IS the win — it's complete and usable as text. If the owner
wants it as a clean spreadsheet to keep, send, or reuse, offer to produce one:

> Want this as a tidy spreadsheet you can save and reuse? I can build the same
> breakdown as a real `.xlsx` you can open and send.

That's built with the document tools (the `doc-lib-set` write path —
`tools/write_xlsx.py`). Offer it; don't make it the price of the win. Most of
the time the typed breakdown is all they need.

End with: *"That's your priced breakdown, margin and all, with the assumptions
written down so you can stand behind it. Want it tidied into a spreadsheet, or
should I price the next job?"*

## Hard rules

- **One job per run.** Price one job properly. If handed several, do the first
  and offer the rest one at a time — a bounded job is a defensible job.
- **Never invent a cost.** Every figure comes from the owner. If something's
  missing, ask one question or leave it out and say so — don't assume a number
  into the price.
- **Margin shown openly, as money.** The margin is its own line and its own
  dollar figure, never buried in the total. State margin vs markup explicitly.
- **Write down the assumptions.** The breakdown stands or falls on them. Every
  number it rests on goes in the assumptions list so the owner can defend it.
- **Never a same-scope discount.** If the owner wants a cheaper number, change
  the scope or the payment shape (per `knowledge/business-method.md` §8.5 and
  §9.4), never the same job for less.
- **Content guardrails.** Customer-facing copy uses no em dashes, invents no
  facts, quotes, or numbers, and names no third-party vendor. Write it in the
  owner's brand voice; the framing and the marketing psychology are the owner's
  choice. The rules are in `knowledge/content-rules.md`.
- **No accounts, no files needed.** This runs on typed inputs alone. The
  spreadsheet is an optional add-on, never a dependency for the win.

## Output shape

The priced breakdown table (line items → cost base → margin shown as money →
total), then the margin called out on its own line, then the assumptions list,
then the stand-behind lines, then the offer to tidy it into a spreadsheet or
price the next job. Concrete and fast — a number the owner can read to a
customer in the next minute.

# Meta Ads operating context (loaded on connect)

> This file is loaded into an owner's `CLAUDE.md` profile only once they connect
> their Meta Ads account. It is the canonical source for how the assistant
> behaves when the Meta Ads connection is live. Until an ad account is connected,
> none of this applies. The assistant works from the owner's profile, their ad
> plan, and what they share. (`run-my-ads`'s "make it yours" setup is what folds
> this block into the profile, and only when the connection has been verified.)

## How the connection works

When Meta Ads is connected, you work inside the owner's own ad account, over
their own Facebook sign-in. Theirs, never anyone else's. Reads are free, so look
around freely: list their accounts, Pages, and past results whenever it helps.
Creating anything is always done **paused**, and always confirmed with the owner
first. You start on the read-only access tier and widen only when the owner is
ready to launch. There is no password or code for you to hold; the sign-in is the
one step the owner does themselves.

## What lives in the ad account (so you know what's possible when they ask)

- **Ad accounts** are the account that holds the campaigns, the budget, and the
  currency everything is billed in.
- **Pages and Instagram accounts** are the Facebook Page and linked Instagram
  account the ads run from. An ad needs a Page to exist.
- **The pixel / dataset** is the tracker that records conversions (a purchase, a
  signup, an enquiry, a booking) so the ads can be optimized for the result that
  matters.
- **Campaigns, ad sets, and ads** are the three-level structure: the campaign
  holds the objective, the ad set holds the audience and budget, the ad holds the
  creative and the link.
- **Past ads and their results** are everything the account has run before, useful
  for reviving proven winners and for reading benchmarks.

## Things that change how you behave (spend safety)

- **Everything ships paused.** You create campaign, ad set, and ad shells in the
  paused state and stop there. The owner reviews them in Ads Manager and switches
  them on themselves.
- **Every create is confirmed and journaled.** Show the owner every setting before
  you build it, get their OK, and let it record to the write journal.
- **You never turn an ad on.** `ads_activate_entity` is off-limits, and you never
  set a status field to ACTIVE on any edit. Those are the two live-money switches,
  and they belong to the owner alone.
- **Budgets are shown in the ad account's own currency.** Read the currency from
  the account itself; never infer it from anywhere else.
- **The owner activates in Ads Manager.** Your job ends at a clean, paused,
  reviewed setup with a clear checklist. Theirs begins when they flip it on.

## Tools you lean on

Plain operating reference for the common moves when the connection is live:

- **`ads_get_ad_accounts`** finds the account, its currency, and its minimum daily
  budget; the first read before anything else.
- **`ads_get_ad_account_pages`** finds the Page (and its lead-form readiness) the
  ads will run from.
- **`ads_get_datasets` / `ads_get_dataset_stats`** confirm the pixel is firing the
  right conversion event before building to it.
- **`ads_create_campaign`** creates the objective level, paused.
- **`ads_create_ad_set`** creates the audience and budget level, paused.
- **`ads_create_ad`** creates the creative and link level, paused (real images,
  video, and final copy are added by the owner in Ads Manager).

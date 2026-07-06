# Connector library

This is the catalog `connect-a-tool` reads to walk an owner through connecting a
tool, and to help them find connectors that fit their business. It is the "what
can I plug in, and what does it unlock" library.

**The honest boundary.** Connecting a tool is an authorization the OWNER performs
in their Claude app (it is an OAuth sign-in, so only they can click it). The
system does everything else: it explains the value, gives the exact steps for
their app, does the token-frugal and privacy thinking for them, verifies the
connection worked, and then puts it to use. This is the one "you do this bit"
step in an otherwise done-for-you setup, and the job is to make it stress-free.

**Token-frugality (always mention).** Connecting a tool loads its actions into
every future turn. Keep it lean: connect only what the owner needs now, and where
the connector offers scopes, enable only the groups in use. A brand-new owner on
a lighter plan should not have their context filled with tools they are not using.

**Where it connects (default: this workspace).** When a tool is added locally in
Claude Code (a `claude mcp add` or `.mcp.json` entry, rather than a claude.ai
connector), connect it **to the owner's BOS workspace folder**, not everywhere,
so their other projects stay fast. Frame it warmly: "I'll connect this to your
workspace, so your other projects stay nice and fast." The one deliberate
exception is keyless web research (firecrawl), which is available everywhere on
purpose because every session benefits from it. claude.ai connectors (the
sign-in type below, like Gmail or a CRM) are account-level and can't be pinned to
a folder — for those, leanness is the only lever. The full reasoning is the
Connection Scoping Doctrine in
[../docs/architecture/tier-1-addon-kit.md](../docs/architecture/tier-1-addon-kit.md).

**The connect-doorway articulation (one home — every connected doorway references
this shape, never restates it).** Every connected add-on in BOS follows the same
honest three-part shape: *here is X you can do keyless today; it becomes enhanced
by Y; which you unlock by connecting Z.* The keyless win is real and complete on
its own; connecting is an upgrade the owner reaches for when the outcome is worth
it, never a gate on the first win, never a cold pitch. Say the keyless win first,
name the enhancement as an outcome, then name the one connection that unlocks it.
Worked example: *`design-my-site` builds a bespoke, high-converting site on the
owner's own machine, keyless (X); it becomes a live, shareable URL that ships
every future update in a word (Y); which the owner unlocks by connecting a Vercel
account (Z, via `launch-my-site`).* Any skill offering a connected doorway (for
instance `launch-my-site`, or `get-found-online`'s SEO-tool doorway) points at
this articulation rather than re-deriving it.

---

## How an entry is shaped (the schema)

Every connector below follows the same shape, so adding a new one is drop-in and
the catalog stays searchable:

- **What it is**: one plain line.
- **Fits businesses that**: the business-need tags, so an owner can find it by
  "what do I want to do" rather than by product name.
- **Unlocks**: the concrete routines and skills it switches on.
- **Connect it**: the steps, per Claude app (the label may differ slightly by
  app version; guide to the Connectors area and adapt).
- **Keep it lean**: the scopes/groups to enable, and what to leave off.
- **Heads-up**: any credit, cost, or privacy note to say out loud first.
- **Verify**: the one lightweight read that proves it worked.

---

## Google Calendar

- **What it is:** the owner's calendar, readable and writable by their system.
- **Fits businesses that:** book appointments, run their day around a schedule,
  juggle jobs or meetings, want a morning brief of what's on.
- **Unlocks:** a morning brief that reads the day ahead; scheduling help;
  routines that key off upcoming events (prep for the next call, remind a client).
- **Connect it:** in the Claude app, open Settings, then Connectors (in Claude
  Code, run `/mcp`). Find the Google Calendar connector, choose Connect, and sign
  in with the Google account that holds their work calendar. Approve the access it
  asks for. Only they can complete this sign-in.
- **Keep it lean:** if asked which calendars, connect the one work calendar they
  actually run the business on, not every personal calendar.
- **Heads-up:** it can read event details and, if they allow it, create or change
  events. Nothing is created without asking. No credit cost to connect.
- **Verify:** ask the system to list their next few calendar events. If it can
  see them, the connection is live.

## Gmail

- **What it is:** the owner's email, so the system can read threads and draft
  replies for them to send.
- **Fits businesses that:** live in their inbox, chase quotes and follow-ups,
  answer the same kinds of enquiries all day, want drafts ready to send.
- **Unlocks:** drafting replies in the owner's voice; a routine that turns the
  morning's calendar into follow-up drafts; catching enquiries that went quiet.
- **Connect it:** in the Claude app, open Settings, then Connectors (in Claude
  Code, run `/mcp`). Find the Google / Gmail connector, choose Connect, and sign
  in with their work email account, approving the access it requests. Only they
  can complete this sign-in.
- **Keep it lean:** connect the one email account they run the business from.
  Where the connector separates reading from sending, start with drafting (read +
  compose drafts) and leave automatic sending off until they trust it.
- **Heads-up:** this lets the system read email content, so name that plainly and
  keep it to their business account. Drafts are prepared for them to review; it
  does not send on its own unless they set that up on purpose.
- **Verify:** ask the system to summarize the latest email in their inbox. If it
  can, the connection is live.

## TrustPager (your CRM)

- **What it is:** the owner's CRM, automation, and client portal platform, the
  deepest connector BOS supports. Requires a TrustPager subscription.
- **Fits businesses that:** run a pipeline, want follow-ups and lead responses
  handled the moment they happen, send documents and forms for signing, and want
  workflows that keep running with the laptop closed.
- **Unlocks:** the whole connected tier — morning pipeline briefings, follow-up
  radar, missed call recovery, lead triage, call logging, email sends, live
  automations, nurture sequences, recurring reports, documents and e-signing.
  `/whats-possible` shows the full split.
- **Connect it:** the primary path is the OAuth connector — the owner says
  "Connect my TrustPager workspace" and the system walks them through the
  connector flow (reconnectable any time at app.trustpager.com/auto/ai-access).
  The advanced alternative is a direct API key from Settings → API → Create new
  key (starts with `tp_live_`), pasted into `python tools/setup.py --force`.
  Full steps live in [INSTALL.md](../INSTALL.md#going-deeper-connect-trustpager-optional),
  which is the single home for the install-time detail.
- **Keep it lean:** TrustPager exposes a large tool surface. Connect it when the
  owner is ready to use the connected tier, not "just in case", and prefer the
  skills' fetch scripts (which call the REST API directly) over loading every MCP
  tool for bulk reads.
- **Heads-up:** it requires a paid subscription, and once connected the system
  can write to the live workspace — every write is journaled and destructive
  actions always ask first. The API key, if used, is stored owner-only in
  `~/.claude/bos.json` and never committed.
- **Verify:** run `python tools/check-install.py` from the BOS folder (the
  connected-tier checks light up), or ask for a pipeline summary. After
  connecting, run `/learn-my-business` so the profile fills from live data.

## Meta Ads (Facebook & Instagram ads)

- **What it is:** the owner's Facebook and Instagram ad account, so the system can
  build campaigns to their plan, created paused and safe.
- **Fits businesses that:** want more enquiries, sales, or bookings from paid ads;
  have an offer to put in front of a cold or warm audience; already run, or want to
  start running, Facebook and Instagram ads.
- **Unlocks:** `run-my-ads`, which runs pre-flight checks and builds paused
  campaign, ad-set, and ad shells to your ad plan, then hands them back with a
  post-setup checklist and the 72-hour rule. (It hands off from your plan the way
  TrustPager hands off to its connected tier.)
- **Connect it:** the steps live in
  [drivers/meta-ads/connect.md](../drivers/meta-ads/connect.md): a user-scope
  `claude mcp add`, then `claude mcp login meta-ads`, granting the read-only tier
  first, a restart, and a verify with one read. Fallback `--callback-port 8080` if
  the sign-in callback stalls. (This connector uses the `claude mcp` CLI, a
  labelled exception to the usual in-app `/mcp` connect flow. See connect.md.)
- **Keep it lean:** connect it when the owner is ready to launch ads, not "just in
  case." The tools stay tucked away (names only) until one is used, so it won't
  slow other work.
- **Heads-up:** ads spend real money, and the system only ever creates campaigns
  **paused**, shows every setting first, and never turns anything on. The owner
  reviews in Ads Manager and switches it on themselves. No cost to connect.
- **Verify:** ask the system to list your ad accounts. If it can see them, the
  connection is live, and it'll run the "make it yours" setup next.

## Vercel (put your site live)

- **What it is:** the owner's Vercel account, so the system can put the site they
  built with `design-my-site` on a real, shareable URL.
- **Fits businesses that:** have built a site or landing page with `design-my-site`
  and want it live and shareable, with every future update shipped in a word.
- **Unlocks:** `launch-my-site`, which deploys the built site to Vercel, a preview
  first for review, then production on the owner's explicit go.
- **Connect it:** the steps live in
  [drivers/vercel/connect.md](../drivers/vercel/connect.md): the system installs
  the Vercel CLI and runs `vercel login` for the owner, the owner completes the
  one browser sign-in, then a verify with `vercel whoami` and a preview deploy.
  (This connector uses the `vercel` CLI, a labelled exception to the usual in-app
  `/mcp` connect flow. See connect.md.)
- **Keep it lean:** connect it when the owner is ready to go live, not "just in
  case." Nothing to load into every turn, the system just shells the CLI when it
  deploys.
- **Heads-up:** Vercel's free tier is generous and enough to get a site live; the
  system says any cost out loud first, and only ever deploys a preview until the
  owner approves production.
- **Verify:** ask the system to run `vercel whoami` (or check the deployed URL).
  If it shows the owner's username, the connection is live.

---

## The growing library (add by asking)

Gmail and Calendar are the starting pair because they power the Day-5 routine and
suit almost any business. Beyond them, the right connectors depend on the
business, and finding them is a great activity AFTER the challenge. Common next
ones owners ask for, by need:

- **Accounting (e.g. Xero):** live numbers, invoices, and reconciled cash flow.
- **Team chat (e.g. Slack):** route alerts and updates to where the team talks.
- **File storage (e.g. Google Drive):** read and organize documents in bulk.
- **A CRM:** the deepest one, it turns many keyless drafts into live, tracked
  actions (send the follow-up, move the deal, run the sequence). TrustPager is
  the one BOS ships a full driver for; its entry is above.

When an owner wants one that is not written up here yet, treat it as a new catalog
entry: find its Connectors listing, learn the connect steps and the scopes, and
walk them through it with the same shape above. If the new tool is added locally
in Claude Code rather than as a claude.ai connector, connect it to the workspace
folder by default (see "Where it connects" above). The point of this library is
that adding a connector is always the same friendly, verified walkthrough, never a
technical chore handed to the owner.

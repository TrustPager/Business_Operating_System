# The `yt-dlp` driver — an optional keyless local deepener

This folder documents `yt-dlp`, the one **`local`-kind** driver on the YouTube
factory floor. It is a reference and a scope note, not a runtime dependency: it
exists so `research-my-channel` can honestly offer a deeper read when an owner
wants one, and so `tools/check-connectors.py` can validate the kind from day one.

`yt-dlp` is a keyless local command-line tool. There is no account, no API key,
no OAuth, and no hosted server. The owner (or the assistant, via Bash) invokes the
`yt-dlp` binary directly on their own machine to pull a video's transcript or its
full comment thread when Firecrawl's page-scrape does not reach that far.

## Why it is `kind: local` (and what that means for its files)

`local` is one of the six canonical driver kinds. A `local` driver is a stateless
local binary with no account and no connection to authorize. Because it is not a
connected kind (the connected kinds are `claude_mcp` and `keyed_cli`), it ships a
deliberately small footprint:

- **`__init__.py`** — the top-level `DRIVER` dict, so the connector gate can
  confirm the kind is canonical.
- **`README.md`** — this file: what the tool is, the honest boundary, and how the
  skill offers it.

It ships **no `connect.md`** and **no `connectors.md` card**. Those two artifacts
are required by `tools/check-connectors.py` only for the connected kinds
(`claude_mcp`, `keyed_cli`), where an owner has an account to sign into. A `local`
driver has nothing to connect, so the gate does not ask for either. It also
carries no `never_call` / `never_set` list: a read-only scrape has no irreversible
or live-money action to guard.

`research-my-channel` declares `requires_driver: none`, so its manifest is not
mechanically bound to this driver. The blueprint is an **offered deepener the
skill body names**, not a hard dependency, which keeps the skill keyless-clean.

## The honest boundary — where Firecrawl already suffices (Decision 5)

`research-my-channel` is **Firecrawl-powered by default**, and for most of what
channel research needs, Firecrawl alone is enough. Default to Firecrawl; reach for
`yt-dlp` only when the owner asks to go deeper.

**Firecrawl (the default) covers the surface facts that carry the packaging
signal:**

- Video and channel titles, descriptions, and tags as shown on the page.
- Visible view counts, upload dates, and posting cadence.
- The top visible comments on a page.

Those surface facts are what the packaging read is built on: what the top channels
cover, how they title and thumbnail it, how often they post, and what the loudest
comments say. That is the whole first pass.

**`yt-dlp` (the optional deepener) is worth its local install only for the deep
read Firecrawl's page-scrape cannot reach:**

- A video's **full transcript**, for close analysis of how a topic is actually
  taught beat by beat.
- A video's **complete comment thread**, for exhaustive comment mining past the
  handful the page shows.

## How the skill offers it

`research-my-channel` runs its full three-part read on Firecrawl first and hands
the owner real results with zero setup. Only then does it offer `yt-dlp` as a
plain "want me to go deeper?" choice: if the owner wants full transcripts or an
exhaustive comment sweep, the assistant installs the `yt-dlp` binary and runs it
locally. It is never a prerequisite and never blocks the first read. The owner
gets a complete research artifact on the keyless default, and the deepener is
there when the extra depth earns its keep.

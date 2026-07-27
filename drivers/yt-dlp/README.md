# The `yt-dlp` driver — an optional keyless local deepener

This folder documents `yt-dlp`, the one **`local`-kind** driver on the YouTube
factory floor. It is a reference and a scope note, not a runtime dependency: it
exists so `research-my-channel` can honestly offer a deeper read when an owner
wants one, and so `tools/check-connectors.py` can validate the kind from day one.

`yt-dlp` is a keyless local command-line tool. There is no account, no API key,
no OAuth, and no hosted server. The owner (or the assistant, via Bash) invokes the
`yt-dlp` binary directly on their own machine to pull a video's full transcript
or its comment thread, which the keyless web read does not reach.

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
- On-page transcript text, where the page shows it.

Those surface facts are what the packaging read is built on: what the top channels
cover, how they title and thumbnail it, and how often they post, plus the demand
signals `research-my-channel` gathers from search results and public discussion.
That is the whole first pass. The keyless web read does not reach a video's comment
threads (they load through a separate client-side call), so real viewer comments
are the deepener's job below, never invented from the page.

**`yt-dlp` (the optional deepener) is worth its local install only for the deep
read Firecrawl's page-scrape cannot reach:**

- A video's **full transcript**, for close analysis of how a topic is actually
  taught beat by beat.
- A video's **comment thread**, for real viewer-comment mining. The keyless web
  read reaches no comments at all, so this is the only keyless way to quote what
  viewers actually said, in their own words.

## How the skill offers it

`research-my-channel` runs its full three-part read on Firecrawl first and hands
the owner real results with zero setup. Only then does it offer `yt-dlp` as a
plain "want me to go deeper?" choice: if the owner wants full transcripts or an
exhaustive comment sweep, the assistant installs the `yt-dlp` binary and runs it
locally. It is never a prerequisite and never blocks the first read. The owner
gets a complete research artifact on the keyless default, and the deepener is
there when the extra depth earns its keep.

## The channel-history use (for `break-down-a-channel` and `what-worked`)

`break-down-a-channel` needs a whole channel's video list to build a breakout
timeline, which Firecrawl's page read cannot reach in depth. `yt-dlp` provides it
keylessly with a **flat-playlist dump**:

```bash
yt-dlp --flat-playlist --dump-json "https://www.youtube.com/@<handle>/videos"
```

**What the flat dump returns (verified):** one JSON object per line (JSONL), each
carrying `view_count` (a *rounded* display figure, e.g. `27000`) and
`playlist_index` (the channel's reverse-chronological order, index 1 = newest). The
`/videos` tab lists neither Shorts nor live streams, so the dump is long-form uploads
only and under-counts a channel that leans on either.

**What it does NOT return:** dates. In flat mode `upload_date` and `timestamp` are
null on every entry. So `break-down-a-channel` uses **upload order** as its
timeline axis, never a calendar date, and its engine (`tools/channel_breakdown.py`)
works entirely from order plus view counts. Exact dates, if ever wanted to label
the handful of videos around an inflection, cost one non-flat per-video call each
and are fetched only for that handful, never for the whole channel.

`what-worked` has the identical data need pointed the other way: the same flat
dump and the same engine, run on the owner's OWN channel after a publish, asking
"what should I repeat" instead of "what can I borrow".

`research-my-channel`'s optional cross-channel outlier board is the third consumer,
and the only one that fans the same dump across several channels at once. It bounds
each pull with `--playlist-end N`, which truncates the list to the channel's N most
recent uploads so a multi-channel fan-out stays readable in one sitting. Truncating
the list also truncates the engine's trailing baseline: the oldest entries inside
that N have few or no prior entries to compare against, so their `outlier` comes back
`null` or computed from a short window. Skip those rows rather than reading them as
scored.

This stays within the honest boundary above: still `kind: local`, keyless,
read-only, no account. Firecrawl remains the default for `research-my-channel`'s
surface read; the flat dump is the specific data need of the three consumers above.

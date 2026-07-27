# Distribution Method — how the algorithm chooses what to push, and how to feed it

The canonical knowledge for *distribution*: how social and video algorithms decide
who sees a piece of content, and the repeatable moves that make them push it to more
of the right people. This is strategy-and-mechanics knowledge, the layer above the
craft. `storytelling-method.md` makes a single piece hold attention; this file makes
the platform carry it to the right audience and keeps that audience consistent enough
for the algorithm to learn who they are.

Consumers that reference this file:

- [`build-social-strategy`](../skills/build-social-strategy/SKILL.md) — the strategy
  home; audience matching, the two-games choice, and the engagement drivers behind
  the one-metric call all live here.
- [`plan-my-youtube`](../skills/plan-my-youtube/SKILL.md) — why a channel holds one
  avatar and one topic band; the cross-platform rule.
- [`research-my-channel`](../skills/research-my-channel/SKILL.md) — the virality
  formula and addressable-audience read behind idea selection.
- [`plan-my-content`](../skills/plan-my-content/SKILL.md) — consistency to one
  avatar across the calendar, the comment-driving levers, and the 3/1/1 audience spread
  across a batch (each post carries both a content-type tag and a ring tag).
- [`youtube-launch-method.md`](youtube-launch-method.md) — its branch filter leans
  on Lever 1, Lever 2's relevance attribute, the sourcing rule, and the
  social-credibility line.

**Framing is the owner's choice.** Some tactics here (the comment-driving levers)
lean on taking a hard or contrarian stance. They are documented at full fidelity
because [`content-rules.md`](content-rules.md) leaves marketing framing to the owner.
The mechanics are neutral; the owner's brand voice decides how sharp to be.

When in doubt, this file wins over instinct. Instinct says "post good content and it
will find its audience." The method says "help the algorithm learn exactly who your
audience is, then give that audience a reason to engage" — reach is earned by feeding
the matchmaker, not by hoping.

> Source note (dev-facing): synthesises the social-algorithm and game-theory
> frameworks taught by Kallaway, including the Bullseye method (the ring ladder, the
> 3/1/1 audience spread, and the topics-from-centre / craft-from-anywhere sourcing rule).
> Named frameworks preserved; examples rewritten for a service-business audience.

---

## The algorithm is a matchmaker

Every social platform has one goal: keep people on the platform as long as possible,
because longer sessions mean more ads and more revenue. To do that it serves each
person the content it predicts they'll enjoy most. That's the whole game — **the
algorithm is a giant matchmaker pairing people with content.** Match well and the
viewer stays; match badly and they leave, which the platform is desperate to avoid.

So the highest-leverage thing you can do is not "beat" the algorithm. It's **help it
make a better match** with your content. Everything below is that.

---

## How a post actually gets distributed

The moment you post, before anyone sees it, the platform builds a **digital
fingerprint** of the content. The analysis is *multimodal*: computer vision reads the
footage, audio fingerprinting reads the transcript and what's said, and it reads all
the metadata (caption, hashtags, the account, the location). It fuses these into a
single **topic mapping** — what this is about and who it's for.

From the topic mapping it builds a **fit score**: its prediction of who will most like
this. Then it runs the cascade:

1. **The initial sample (~200 people).** It shows the post to a small first group it
   predicts will like it most. Crucially, **most of them are non-followers** — the
   platform already assumes your followers will like you; the real test is whether
   *strangers* do.
2. **Read the signal, then boost / retry / stop.**
   - *Positive* → the fit score was right; push to a bigger group (≈2,000, then
     20,000, then 200,000…), widening until the signal weakens.
   - *Neutral* → rebuild the fit score and re-sample another small group; don't scale
     yet.
   - *Negative* → tighten and stop almost immediately, so a weak post doesn't push
     people off the platform.
3. **Even big hits fade** because they eventually run out of people who want them, not
   because they were "switched off."

This is what "**200-view jail**" actually is: the initial sample came back weak, so the
post never left the first group. It's a signal problem, not a punishment.

---

## Lever 1 — help it build a good fit score: audience matching

**Make content about the same topic for the same audience avatar, over and over.** The
more consistent your topic band and viewer profile, the more confident the algorithm
gets about who to sample, and confidence is what earns the push.

Think of it as **darts**: throw at the same board repeatedly and the target grows,
easier to hit each time. Jump boards every throw and it never learns your aim.

Why inconsistency kills reach: make one video on pricing, one on hiring, one on tools,
and the algorithm has no idea what video four is about or who to sample. It builds a
*blended* fit score from three different audiences, samples a muddled group, the
signal comes back weak, and the post flops, even if that fourth video was good.

The hard discipline that follows:
- **One avatar, held.** Picture one real person you serve and make everything for
  them. Do that consistently and the algorithm finds thousands more like them.
- **Say no to off-avatar "viral" ideas.** Even one hit with the wrong audience feeds
  the fit score the wrong people and weakens the next several posts. Narrow beats
  broad.
- **People watch for themselves, not for you.** They like you as the messenger, but
  they're there for what they get out of it. Four different topics for four different
  needs alienates all four.
- **Formats can vary wildly; the audience cannot.** Once the avatar is locked, mix
  formats freely (different-shaped darts, same board).

This is the single highest-leverage distribution principle. It is *why*
[`build-social-strategy`](../skills/build-social-strategy/SKILL.md) pins one target and
a narrow set of pillars, and why a channel plan holds one avatar.

---

## The audience bullseye — the ring ladder and the audience spread

Lever 1 says hold one avatar. The bullseye is *how you operate that* without going so
narrow you starve for reach. Picture your audience as a dartboard: the exact person you
serve is the centre, and each ring outward is a broader audience, one step less specific.

**The ring ladder — five levels, one constraint relaxed per ring.** Start at the centre
(your exact ideal viewer, named at person-level) and build four rings out, each relaxing a
single constraint so the audience widens by a real, nameable step. For "high-ticket B2B tech
sales" the ladder is: centre = high-ticket B2B **tech** sales, Ring 1 = high-ticket B2B sales
(drop the industry), Ring 2 = B2B sales (drop deal size), Ring 3 = sales of any kind (drop
the model), Ring 4 = business (drop the profession). Each ring out is roughly 5-10x larger,
and the further out you go the weaker the intent: the centre converts, the outer rings only
reach. A ring is only a ring if you can name the audience in it; a vague blur is not a ring.

**The 3/1/1 audience spread.** This is the second axis of a content plan, and it is *not*
the content mix (that axis is what a post is *about*: teach, prove, promote). The audience
spread is who a post is *aimed at*. For every batch of five videos:

- **3 at the centre** — deep conversion. So specific the ideal viewer thinks "this was made
  for me." Lower ceiling on raw views, highest ceiling on trust and enquiries.
- **1 at Ring 1** — reach with conversion. Still close enough that the right people
  self-identify.
- **1 at Ring 2** — pure reach. Teaches the algorithm there is a larger adjacent pool and
  feeds new viewers in.

Never aim past Ring 2 in the first phase. The outer rings are where the algorithm carries
you *after* you have earned a confident fit score, not where you aim. Aim narrow and the
matchmaker expands you outward for you; that is the whole trick, and it is why precision
comes before reach, never the other way around.

**Calibrate, do not guess.** Run the 3/1/1 spread for the first two or three batches, then
look at which ring actually drove the outcome that matters (follows, DMs, enquiries, sales)
and bias later batches toward it. Some businesses convert hardest at the dead centre, others
one ring out. The data decides the spread, not instinct.

**The sourcing rule — topics from the centre, craft from anywhere.** When an owner says
"nobody makes content in my exact niche, who do I even study?", this is the answer.
*Topics* must come from the centre or Ring 1 only (borrow a topic from the outer rings and
you drift broad and muddle the fit score). *Craft* — hooks, formats, editing, pacing,
structure, thumbnails — can be studied from the best executors in any niche on earth. A
cooking channel's format can carry a pricing topic. And if the centre is genuinely empty of
creators, that is not a problem, it is the opening: take a Ring 1 topic and re-aim it at your
centre ("their video for all of B2B sales, remade specifically for $1M+ tech deals").

---

## Lever 2 — make the sample engage

A good fit score gets the right ~200 people; now they have to *engage*, or the signal
comes back flat. The algorithm reads three core metrics:

| Metric | What it is |
|---|---|
| **Average watch time / % completion** | How many seconds, and what share of the piece, the average viewer watches. |
| **Engagement rate** | (likes + comments + shares) ÷ views. |
| **Watch-time session share** | Of a viewer's whole session, how much was spent on *your* content. You can't see this number, but it's a heavy signal of how influential your content is. |

The four attributes that reliably drive those metrics up (and, not by accident, the
same four that turn viewers into buyers):

1. **Relevant** — the topic solves a real problem the ideal viewer has.
2. **Non-obvious and tactically implementable** — new to them, and usable.
3. **High absorption** — said so they can actually understand it; if they can't
   follow it, they can't act on it.
4. **Short distance to implement** — a little action yields a big result on the
   promise.

In plain terms: cover a real pain, have something useful to say, say it so they get
it, and make it usable. That's the DNA of content that both performs and sells.

---

## Comment-driving levers

Comments are among the strongest engagement signals. Five levers raise them:

1. **Take a hard stance.** People comment when they strongly agree or (more often)
   disagree. Hedging the middle gets silence.
2. **Pick the contrarian side.** If your take says the majority is wrong, the majority
   shows up to say *you're* wrong. Useful enemies drive comments.
3. **Amplify the framing.** The more pointed the way you put it, the more discussion.
4. **Build on cult-loved brands, people, ideas, movements.** People already hold
   opinions on these and jump in fast.
5. **Drive emotion.** The more a viewer feels, the more compelled they are to comment.

> **Framing flag.** These levers lean on dissent and strong stances by default.
> Documented at full fidelity because framing is the owner's choice
> ([`content-rules.md`](content-rules.md)). An owner who prefers a warmer register can
> drive comments with genuine questions, a surprising-but-positive stance, and emotion,
> and skip the "make enemies" surface. The mechanic is *provoke a reaction*; the owner
> chooses how sharp.

---

## The two games — awareness vs conversion

Social is two games meshed into one. **You can only play one game per channel** (you
can play both across multiple channels).

| | **Awareness game** | **Conversion game** |
|---|---|---|
| Funnel | Top | Middle / bottom |
| Goal | Max views in the category | Max *on-target* views |
| Paid by | Reach / impressions (CPM) | Downstream sales from an offer |
| Wins on | Shareability + curiosity + emotion + large addressable market | Non-obvious, deeply tactical, actionable content aimed at buyer pain |

**Awareness strategy** — make content that is (a) highly shareworthy, (b) opens
insatiable curiosity in the hook, (c) pays off with real emotion at the end, and (d)
appeals to as large an addressable market as possible. People share for the social
credit of sharing (a laugh, a "look at this," a hat-tip). A share from a *peer creator*
in your space (a "super-share") is worth thousands of ordinary ones.

**Conversion strategy** — make content so specific and tactical for your buyer that a
passive viewer would say "this isn't for me." Give the active viewer immediately
actionable, non-obvious solutions that actually work, and make them feel you have
insider knowledge that applies to *them*. You *want* to filter passive viewers out so
the algorithm hones your audience toward buyers over time. Drive shares from the target
audience and extend watch time; don't chase raw reach.

For a service business the conversion game is usually the one that pays the rent:
on-target views from local buyers beat a viral hit seen by the wrong country. Name
which game a channel is playing before choosing topics, because the two optimise for
opposite things.

---

## The virality formula — idea × audience × validation

Reach starts with the idea, not the edit. Three variables:

1. **Idea (common vs uncommon).** Pair it with the right lens (the *story lens* itself
   lives in [`storytelling-method.md`](storytelling-method.md)):
   - **Uncommon idea + normal lens** — a genuinely rare/weird idea needs no spin.
   - **Common idea + unique lens** — a well-worn idea needs your angle to stand out.
2. **Addressable audience size** — how many people would share this if it crossed
   their feed? Stack overlapping audiences so the applicable pool is unnaturally large
   (a "real Iron Man suit" reaches Marvel fans *and* engineering fans). For a local
   business this cuts the other way in the awareness game and is why the conversion
   game (a smaller, on-target local audience) is often the right call.
3. **Validation** — check whether a similar idea already performed somewhere. Proven
   outliers are the safest to remix. The mechanics of reading an outlier against a
   channel's own baseline live in
   [`youtube-packaging-method.md`](youtube-packaging-method.md); this file is the *why*
   (a validated idea de-risks the reach bet).

Study what already worked in the category, reverse-engineer *why*, then remix it with
your own lens. Never lift; learn the structure and bring your angle.

---

## The cross-platform rule — don't drive slow traffic to fast platforms (or vice versa)

Each platform runs its viewers at a different speed. Short-form is fast; a feed of
long-form is slower; email is slower still. A viewer's brain is calibrated to the pace
of the platform they're on.

The trap: posting your long-form video's link on a fast platform (an Instagram story,
say) drags a fast-paced viewer onto a slow-paced video. They click, watch briefly, and
bounce, which is a **double negative** — the destination platform gets no
click-through-rate credit (they didn't click a thumbnail) *and* the average view
duration is short. Both signals tell that algorithm the video is weak.

- **Don't cross-post links from a faster platform to a slower one** to chase views.
  Let each platform's audience find that content natively.
- **Email is the exception.** Email is slower than almost everything, and people
  happily move from slow to fast. So email is the one channel that reliably sends
  traffic to a video without the speed-mismatch penalty.

---

## The social-credibility line — small-channel psychology

Below a certain following, people hesitate to click even when the title and thumbnail
intrigue them: a low subscriber count or view count reads as "not proven yet," so a
smaller share of people give a new account a chance. That threshold (the
**social-credibility line**) sits around a few thousand followers on most platforms,
higher on YouTube (roughly 10k subscribers).

Two ways across it:
- **The common path** — hammer consistent content and climb a little at a time.
- **The uncommon path** — a lucky viral outlier that rushes you over the line
  overnight. The most engineerable version is a **quality shock**: a piece so
  disproportionately polished relative to how small you are that people subscribe as a
  tip of the cap.

The takeaway for a new account: expect a slow start, keep the quality high, and know
that the early grind is steep partly because of this psychology, not because the
content is failing.

---

## Banned framings (distribution edition)

- **Spray-and-pray topics** — chasing every idea across many audiences. It confuses the
  fit score and flattens reach. Narrow to one avatar.
- **Chasing off-avatar viral hits** — one wrong-audience win taxes the next several
  posts. Say no.
- **Vanity metrics as the goal** — raw views/followers over the metric that maps to the
  goal (on-target views, enquiries). Name the real metric.
- **Playing both games on one channel** — awareness and conversion optimise for
  opposite things; pick one per channel.
- **Invented outliers or made-up numbers** — never cite a view count, a competitor
  result, or an audience signal you didn't actually observe
  ([`content-rules.md`](content-rules.md); the research floor's evidence rule).

---

## Common mistakes (don't re-walk these)

| Mistake | Fix |
|---|---|
| Topics jump around every post | Hold one avatar and a narrow topic band; let the algorithm learn who to sample |
| Blaming "the algorithm" for a flop | The initial ~200-person sample came back weak; fix relevance/hook/engagement, not luck |
| Optimising for followers | Followers barely count in sampling; win the non-follower sample instead |
| Cross-posting a long video's link to a fast feed | Let each platform find it natively; use email, not fast-to-slow links |
| Chasing reach on a conversion channel | Make it tactical enough to filter out passive viewers; on-target views over raw views |
| One channel trying to do awareness and conversion | Split them: one game per channel |
| Expecting fast growth from a new account | The credibility line makes early growth steep; keep quality high and hold consistency |
| Picking an idea with no validation | Remix a proven outlier; read it against the channel's own baseline (packaging method) |

---

## Output rule

Customer-facing output follows [`content-rules.md`](content-rules.md): no em dashes, no
invented evidence, no third-party vendor leak. **Framing (positive, contrarian, or any
psychology) is the owner's choice** — this file supplies the distribution mechanics;
the owner's brand voice supplies the register. These notes are dev-facing; the copy the
strategy *produces* is what the rules govern.

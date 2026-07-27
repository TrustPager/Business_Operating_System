# YouTube Script Method — the beat-structured script that keeps the promise

The canonical knowledge for writing a YouTube script that packaging earned the
click for and that retention keeps. This is the operator-facing method; the skill
that uses it stays lean and references this file:

- [`script-my-video`](../skills/script-my-video/SKILL.md) writes the
  beat-structured `<slug>.script.json` this file describes, in the owner's voice.
- [`youtube-packaging-method.md`](youtube-packaging-method.md) owns the title +
  thumbnail *promise*. This file owns *keeping* it. The script's whole job is to
  deliver on the packaging, so read the packaging first, then script to it.
- [`storytelling-method.md`](storytelling-method.md) owns the cross-cutting
  attention craft — hooks, curiosity loops, the dance, rhythm, the last dab. This
  file is that craft *applied to a beat-structured YouTube video*. When a move here
  (the hook, a retention reset) has a general form, storytelling-method is its home;
  read it alongside this file.

**The script is the spec.** One beat-structured script drives everything
downstream: `studio/video` renders each beat's on-screen text as motion graphics,
`make-thumbnail` reads the packaging concept, `package-my-video` reads the timing
for chapters, and (later, connected) the same script comes back fully voiced with
no rework. So the script is written to be *rendered*, not just read: every beat
carries one spoken line, one on-screen element, and one visual note.

When in doubt, this file wins over instinct. Instinct says "explain everything
you know". The method says "keep the specific promise the title made, hold
attention beat by beat, and drive one clear action".

---

## Every beat has one spoken line, one on-screen element, one visual note

This is the per-beat discipline, and it is what makes the script machine-
renderable. A beat is the atomic unit of the script. Each beat carries exactly:

| Field | What it is | What it drives |
|---|---|---|
| `spoken` | The one line the owner says, in the owner's own voice | The voiceover (owner reads it on the floor; TTS voices it on the connected rung) |
| `on_screen` | The single text/graphic callout for this beat | `studio/video` renders it as branded text-on-screen |
| `b_roll` | One visual note (own footage or stock guidance) | The owner's shot list / footage plan |

**One idea per beat.** If a beat needs two on-screen callouts to make sense, it is
two beats. This keeps each moment legible at a glance and keeps the render clean —
the on-screen text is a *callout*, not a transcript of the spoken line.

**`on_screen` is not the same words as `spoken`.** The spoken line is
conversational; the on-screen callout is the 2–5 word crystallisation the eye
reads while the ear listens. Putting the full sentence on screen makes the viewer
read instead of listen, and it renders as a wall of text.

- ✅ spoken: *"The first thing I do is ask what the job's actually for."* → on_screen: *"Ask what it's for"*
- ❌ on_screen: *"The first thing I do is ask what the job is actually for"* (that's the spoken line again, unreadable at a glance)

**Every claim rests on real evidence.** Where a beat makes a claim about a result,
a number, or what customers say, it carries an `evidence_ref` into the owner's
customer-voice synthesis where one exists. Never fabricate a quote, a number, or a
testimonial to fill a beat. A claim with no evidence is softened to what is
honestly true, never invented.

---

## The hook and the hook window

The **hook** is the opening beat, and it is the most important line in the whole
script. The packaging earned the click; the hook decides whether the viewer stays
past the first few seconds. YouTube watches the early-seconds retention closely,
so a weak open sinks a good video before it starts.

**The hook window is the first ~5–15 seconds** (the `meta.hook_window_s` in the
script; ~5s is a tight default for a short, up to ~15s for a longer video). The
hook must land inside that window — the promise or the intrigue is stated *first*,
before any intro, channel branding, or "hey everyone welcome back".

**Hook patterns that work:**

| Pattern | Shape | Example |
|---|---|---|
| **Restate the promise** | Say the title's promise out loud, immediately | *"I'm going to quote a real job, start to finish, in under a minute."* |
| **The bold claim** | A specific, true, slightly surprising statement | *"The quote itself wins the job, long before the price is read."* |
| **The open loop** | Pose the question the video answers, don't answer it yet | *"There's one question that wins me nearly every job. Here it is."* |
| **The result first** | Show the outcome up front, then earn it | *"This is the quote that won a $12,000 job. Let me show you how it was built."* |
| **The relatable moment** | Name the exact situation the viewer is in | *"You're standing in someone's kitchen and they ask what it'll cost. Here's what I say."* |

**Payoff-first cold open: open on the win already won, then rewind.** The strongest
cold open states the highest payoff already achieved, right away, then rewinds to show how it
happened. Never open on an empty or blank starting state (an empty template, an empty inbox,
"let's start from nothing") to build up to the payoff later. A swiped-brain viewer's thumb is
already moving, and a blank start gives it nothing to stop on. Lead with the win, using the
"result first" pattern in the table above: state the $12,000 job already won, then rewind into
how.

**The deeper hook craft** — the three-step formula (context lean-in → scroll-stop
interjection → contrarian snapback), the six hook power words, and why a visual hook
beats an audio-only one — lives in [`storytelling-method.md`](storytelling-method.md).
The patterns above are the YouTube-specific shapes for *drafting* a hook. The six
power words are the *gate*: score every drafted hook against them (name the words
carrying subject clarity, action, objective, and contrast) before the hook is locked,
and score it again after any structural rewrite. A hook judged by ear alone is how a
soft one ships.

**Cut the runway.** The single most common hook mistake is starting with a slow
intro before the hook. There is no "warming up" — the hook is beat one. Branding,
context, and the channel intro come *after* the viewer has a reason to stay, if at
all.

---

## The promise beat — set the contract, then keep it

Right after the hook, the **promise** beat tells the viewer exactly what they will
walk away with. It is the contract for the rest of the video. It does two jobs:
confirms they're in the right place, and gives them a reason to stay to the end.

- ✅ *"By the end of this you'll have the exact three questions I ask, and you can use them on your very next quote."*

Keep the promise honest and specific, and make sure the body actually delivers it.
A promise the video keeps is what turns a viewer into a subscriber. A promise it
breaks is what teaches them to click away next time.

---

## Retention structure — beats, and the resets that hold attention

Attention leaks. Every few beats a slice of the audience decides whether to stay.
The script's job is to keep giving them a reason. The structure:

1. **Hook** (in-window) — earn the stay.
2. **Promise** — set the contract.
3. **Points** (the body) — deliver the promise, one clear idea per point. Each
   `point` beat makes one move toward the outcome, in order.
4. **Resets** between or inside points — re-earn the attention (see below).
5. **Proof** where a claim needs it — a real example, a real number, a real
   customer's words (evidence-anchored, never invented).
6. **CTA** — one clear next action.

**Connect beats with "but," "however," "therefore," or "so." Never "and then."** A script where
each beat just adds onto the last ("we quote the job, and then we send it, and then we follow
up") reads as a flat list and the audience drifts. The full mechanic (the dance between context
and conflict) is in [`storytelling-method.md`](storytelling-method.md), under "The dance."
Applied at the beat level here: before moving to the next beat, check the connector implied
between it and the one before. If it's "and then," find the "but" or "therefore" that's
actually there, or the beat doesn't earn its place yet.

**A retention reset is a deliberate re-hook mid-video.** It is a small pattern
change that stops the video feeling like one long flat stretch. The attention engine
underneath it — the four-step addiction loop (stakes → big question → head fake →
re-hook) and the loop-opener cadence (a re-hook roughly every 60–90 seconds on a long
video) — is in [`storytelling-method.md`](storytelling-method.md). A reset closes one
loop and opens the next in the same breath. Use one whenever a section runs long or
the energy would otherwise sag:

- **Open a new loop** — *"But there's a catch, and it's the part everyone gets wrong."*
- **Change the visual** — move from talking-head to a demo, a screen, or b-roll.
- **Signpost progress** — *"That's step one. Step two is where it gets good."*
- **Restate the payoff** — remind them what they're still here for.
- **Ask a question** the next beat answers.

Resets are beats too (`role: reset`), so they carry their own spoken line and
on-screen element. Place them at the seams where attention is most likely to
leak — the transition between two points, and just before the longest section.

**Front-load the value.** Deliver something useful early, don't save every good
part for the end. A viewer who gets a win in the first third stays for the rest; a
viewer told to "stick around, it's coming" often doesn't.

---

## The words-per-minute default (why planned timing exists)

Each beat carries an optional planned `duration_s`, estimated from the spoken
line's word count at a stated **words-per-minute (wpm) default**. This lets the
script estimate the video's length *before* it's rendered, so the owner can see
whether they're on target for the length they wanted.

**The default is ~150 wpm** — a natural, clear speaking pace for a talking-head
explainer, neither rushed nor sleepy. `script-my-video` states the wpm it used in
its output, so the estimate is transparent and the owner can adjust it to their
own pace. The maths is simple: `duration_s ≈ (words in the spoken line ÷ wpm) × 60`.

This is *planned* timing. The real per-beat timing is written by `studio/video`
after it renders (the `<slug>.timing.json` sidecar), and `package-my-video`
prefers that actual timing for chapter timestamps, falling back to the planned
`duration_s` when no render has happened yet. Planned timing is the estimate;
rendered timing is the truth.

**Match the length to the promise, not a target number.** A 60-second promise
scripted to five minutes breaks the contract as badly as padding does. Say what
the video promised, completely, then stop.

---

## The CTA — one clear next action

The **CTA** beat is the last beat, and it asks for exactly one thing. The mistake
is asking for five (subscribe *and* like *and* comment *and* click *and* follow) —
five asks is no ask, because the viewer does none of them.

**Pick the one action that matters for this video** and make it specific:

- ✅ *"If you want the three questions as a one-page checklist, it's linked below. Grab it and use it on your next quote."*
- ✅ *"Watch the next one where I turn this quote into a job won."* (drives the next view, the strongest signal for the channel)
- ❌ *"Like, subscribe, comment, hit the bell, and check out my other videos."* (five asks, no action)

**Tie the CTA to the value just delivered.** The best moment to ask is right after
the viewer got what they came for — the ask feels earned, not tacked on. And the
strongest CTA on YouTube is usually "watch this next", because another view is
what tells the platform to keep suggesting the channel.

Keep the CTA specific: name the action and the thing they get for
taking it.

---

## The subscribe ask: its own beat, earned right after the biggest payoff

The subscribe ask is its own beat (`role: subscribe`), never a line bolted onto the
terminal CTA. Its strongest placement is mid-roll, immediately after the point where the
biggest payoff has just landed, because that is where the ask is earned rather than
requested. Make it personal and in the owner's own voice: this is the one beat where the
owner speaks to the viewer directly.

**Asking again at the end is the owner's call, and it is a real trade-off, not a free
win** (founder ruling 2026-07-26, which overrides this file's earlier "exactly one ask,
never at the end" edict; the earlier rule is kept below as the reasoning, because the
reasoning is still true). The case for asking twice: the mid-roll ask converts the viewer
who is already sold, and someone who stayed to the end is the most engaged person you
will get, so letting them leave without an ask spends that engagement on nothing. The
cost: every extra ask in the same breath dilutes the others, and a viewer given four
things to do usually does none. Both things are true at once.

So if a channel asks at the end as well, do it deliberately:

- **Order the asks by cost to the viewer**, cheapest first: like, then subscribe, then a
  comment prompt (which doubles as a topic-research signal), then the one real conversion
  ask last, so the ask that matters most is the last thing they hear.
- **Keep them separate beats, and keep them short.** A closing ask stack that runs long
  reads as a plea. One breath each.
- **Give the comment prompt something specific to answer** ("what should we cover next")
  rather than "let us know your thoughts".
- **Know what you are trading.** If the channel's one job this season is the conversion
  ask, the cleanest ending is that ask alone, with subscribe left to the mid-roll beat
  and the end-screen visual. Say that plainly to an owner who wants everything.

**Give a concrete cadence promise, not a vague one.** "New build every Tuesday" tells the
viewer exactly what they get and when. "More great content" promises nothing testable and
earns nothing.

- Yes: *"If that's the kind of build you want to see, there's a new one every Tuesday. Hit
  subscribe and I'll see you then."*
- No: *"Don't forget to like and subscribe for more great content!"* (no cadence, nothing
  testable, no reason to act now)

**The mid-roll beat stays subscribe-only.** That beat has room for one ask, and it is the
earned one. A like-ask belongs in a closing stack if the channel runs one, ordered
cheapest-first as above, never crowded into the mid-roll moment. Worth knowing what each
ask is worth: a like is the cheapest thing to give and the weakest growth signal, while the
next view and the subscribe are what actually compound. That is the reason to spend the
earned moment on subscribe and leave the like to the end, if it is asked for at all.

**On an AI-heavy channel, splice in a short live-host cameo for the ask, and own the AI
narration in it.** A few seconds of a real person on camera delivering the subscribe ask builds
trust that a fully narrated, faceless AI voice can't on its own. On a channel where the rest of
the video is AI-narrated, that cameo must say so plainly, something like *"I built this one with
AI, and here's what's coming next Tuesday."* Skipping that acknowledgement is the version that
backfires: a viewer who clocks the AI narration on their own, after a cameo that didn't mention
it, reads the whole channel as trying to pass AI off as human, and the trust the cameo was meant
to build works against the channel instead.

---

## Banned framings (script edition)

- **A slow intro before the hook** — no runway. The hook is beat one, inside the window.
- **On-screen text that copies the spoken line** — the callout is the 2–5 word
  crystallisation, not a transcript.
- **Fabricated evidence** — never invent a number, a quote, or a testimonial to
  fill a beat. Anchor real claims in the customer-voice synthesis, or soften to
  what's honestly true.
- **A promise the body doesn't keep** — the title and the promise beat set a
  contract; the script keeps it or it isn't shipped.
- **Five-ask CTAs** — one clear action, tied to the value delivered.

---

## Common mistakes (don't re-walk these)

| Mistake | Fix |
|---|---|
| Hook lands after a 20-second intro | Move the hook to beat one, inside `hook_window_s` |
| A beat carries two ideas | Split it — one spoken line, one on-screen callout per beat |
| On-screen text is the full spoken sentence | Crystallise to 2–5 words; let the ear listen and the eye glance |
| The video sags in the middle | Add a `reset` beat at the seam — open a loop, change the visual, signpost progress |
| Every good part saved for the end | Front-load a real win in the first third |
| Length wildly off the promise | Re-estimate from the wpm default; script to the promised length, then stop |
| A claim with no evidence behind it | Attach an `evidence_ref`, or soften to what's honestly true |
| CTA asks for five things | One action, specific, tied to the value just delivered |

---

## Output rule

Customer-facing output follows knowledge/content-rules.md (no em dashes, no
invented evidence, no third-party vendor). The owner's marketing framing is their
own choice. The script's craft notes here are dev-facing; the copy the script
*produces* is what the rules govern.

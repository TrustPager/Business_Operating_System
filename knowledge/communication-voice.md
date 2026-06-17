# Communication voice

**The one voice every customer-facing message uses — from anyone on the team.** Email, SMS, portal note, fix confirmation, onboarding update. It is how the business sounds to a customer. When five people send messages in five tones, the business feels disorganised; one voice builds trust and removes the customer's effort.

## The voice in one line
Plain, warm, reassuring, and short: lead with the outcome, say what we did in one human sentence, give one clear next step, and stop.

## Principles
- **Lead with the outcome.** The first line is the result the customer cares about: "Sorted, it's working now." Not a preamble, not a recap of the problem.
- **Set the context in the first line when it's a reply.** If the message answers something they raised, name it so there is zero ambiguity ("About the booking issue you flagged..."). A contextless "it's done" makes them guess what "it" is.
- **Plain and human.** Write like a person talking to a person. No jargon, no system internals, no technical story of what went wrong. The customer should never have to understand how the software works to read the message.
- **Customers use, they never test or debug.** Hand them ONE clean instruction on how to *use* the thing: a raw URL plus a single action. Never "try this and see", never a checklist of steps to test. Testing is the team's job, done before the message goes out (see `safeguards.md`).
- **One message, not five.** Fix the thing, then send one clear note. A customer has less context than anyone on the team; multiple messages overwhelm them. If you are tempted to send a follow-up to correct or add, that is a sign the first one wasn't ready.
- **Short.** One plain sentence on what we did. One next step. Then stop. If it runs past a few short lines, cut it.
- **Reassuring and confident, never hedged.** No "should work now", no over-promising. State what is true.
- **Warm and respectful.** Acknowledge the person. Own mistakes plainly ("that's on us, not you"). Never make the customer feel like the tester or the problem.
- **Raw URLs, never breadcrumbs.** Link with the actual URL as the visible text, not "Settings > CRM > ..." and not numbered navigation.

## Structure for a fix or update message
1. One-line reassurance (with context if it's a reply): "Sorted, this is working now."
2. One plain sentence on what we did, no internals.
3. The single thing the customer does to USE it: a raw URL + one action.
4. "Reply if anything looks off." Stop.

## Example (shape and voice to copy)
```
Subject: Booking from a company record

Hi James,
Sorted, this is working now. You can book a meeting straight from a company
record and it creates the opportunity for you automatically.
To use it: open the company at https://app.trustpager.com/crm/accounts, click
Book a Meeting, choose the meeting type, pick a time, and confirm.
Reply if anything looks off.
Sarah
```

## Banned
- Technical explanations of what went wrong ("this happened because X").
- Jargon, internal names, architecture, system internals.
- Lists of steps for the customer to "test" or "try". (Customers use; they don't test.)
- Hedging ("should work"), over-promising.
- More than one message for the same thing. Walls of text.
- Telling a customer something is fixed before someone on the team has seen it work (`safeguards.md`).

## Why
Confusion frustrates a customer as much as breakage does. A customer on a paid subscription should never have to decode a technical email or discover broken basics themselves. One plain, consistent voice across the whole team removes that cognitive load and builds trust.

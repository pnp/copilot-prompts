---
name: self-awareness-review
description: |
  Reviews a given week of your OWN Teams meetings, chats, and sent emails to surface
  moments where you may have misread social signals or come across as passive-aggressive,
  curt, sarcastic, or dismissive — returning the exact quote, how it likely landed, and a
  kinder rewrite. Private self-reflection coaching for the signed-in user only.
  Use when you ask "was I out of line this week?", "did I come across as passive-aggressive?",
  "did I misread anyone this week?", "how did I come across?", "review how I came across",
  "check my tone this week", or "was I the difficult one?". Defaults to the current week;
  accepts any week.
  Do NOT use to evaluate, rank, or critique OTHER people — use meeting-intel for neutral
  meeting summaries, daily-briefing for a schedule overview, or stakeholder-comms to draft
  a message. This skill only ever analyzes your own words.
cowork:
  category: analysis
  icon: PersonFeedback
---

# Self-Awareness Review

A private self-awareness review of the signed-in user's own communication over one week.
It reads the user's **sent emails, Teams chat messages, and their spoken lines in meeting
transcripts**, then flags specific moments where they may have misread a social signal or come
across as passive-aggressive, curt, sarcastic, or dismissive. For each moment it shows the
exact quote, explains how it likely landed, and offers a warmer rewrite — so the user can
improve how they work with people. This is self-coaching, always kept private, never sent anywhere.

## Before Starting

**Critical**: Always gather the following before proceeding:

1. **Week to review** — which week to analyze (defaults to the current week Mon–Sun if not specified)

If the user doesn't specify a week, default to the current week.

## Output Structure

Private markdown, delivered inline (never sent or posted):

- **Verdict** — a light, kind one-liner (e.g. "Mostly on point — two moments worth a redo"). Keep it constructive, never harsh.
- **Week reviewed** — the exact date range and what was scanned (e.g. "18 sent emails, 40 Teams messages, 3 meetings with transcripts").
- **Moments worth a redo** — a short list; each entry:
  - *Where:* source + timestamp
  - *You wrote/said:* "<exact quote>"
  - *How it may have landed:* one line
  - *Try instead:* "<kinder rewrite>"
- **Patterns** — 1–3 recurring tendencies across the week.
- **Try next week** — 2–3 specific, doable habits.

Keep the tone that of a supportive friend giving honest feedback — direct but generous. Aim for scannable; skip the essay.

## Step 1: Resolve the Week

Use the user's local time zone and current date to compute the target window. Default to the
**current week (Monday 00:00 – Sunday 23:59)**. If the user names a week ("last week", "week of
the 14th"), resolve that instead. State the exact date range you used in the output.

## Step 2: Gather the User's Own Words

Run these lookups in parallel:

- **Sent emails:** `ListMessages(folder_id="sentitems", received_after=<start>, received_before=<end>, top=50)`; open substantive ones with `GetMessage`. Only the user's authored text counts — ignore quoted/forwarded content below their reply.
- **Teams chats:** `SearchM365(sources=["teams"], from_user="<user's email>", after=<start>, before=<end>)`, or `ListChatMessages` per active chat; keep only messages **authored by the user**.
- **Meetings + transcripts:** `ListCalendarView(start, end)` → for each online meeting take `onlineMeeting.joinUrl` → `ListMeetingTranscripts(join_url=...)` → `GetMeetingTranscript(...)`. Analyze **only the lines attributed to the user** (their display name / "you").
- Resolve the user's own email via `GetMyDetails` if needed. Skip events flagged `private`/`confidential`.

## Step 3: Scan for Signals

Flag the user's own lines that show:

- **Passive-aggression:** "per my last email", "as I already said", "as previously mentioned", "not sure why this is unclear", "obviously…", "just circling back AGAIN", "friendly reminder" (when it isn't), backhanded thanks, weaponized politeness.
- **Curtness / dismissiveness:** one-word brush-offs, "no.", "that's not my problem", "figure it out", ignoring a direct question, closing a thread while a concern is unanswered.
- **Sarcasm / undermining:** sarcastic praise, public correction of a colleague, "well actually", talking over someone (transcript: interrupting, long monologue after another person raised a point).
- **Misread signals:** someone expressed hesitation, confusion, or discomfort and the user pushed past it; a joke that may not have landed; escalating tone when the other person was conciliatory; assuming bad intent.

## Step 4: Explain and Coach

For each flagged moment, give:

- The **source** (email subject / chat / meeting name + timestamp)
- The **exact quote**
- A one-line read of **how it likely landed** for the other person
- The **signal that was misread** (if any)
- A **kinder rewrite** that keeps the user's substance but changes the delivery

## Step 5: Synthesize

Give a fair, warm **verdict**, name 1–3 recurring **patterns**, and 2–3 concrete **habits to try next week**. If nothing notable surfaced, say so plainly — do not manufacture incidents.

## Rules

- **Self-only.** Analyze exclusively the user's own words. Never evaluate, rank, score, or characterize any other person's behavior, tone, or performance — if the user asks you to turn the lens on someone else, decline and offer meeting-intel instead.
- **Evidence or nothing.** Every flagged moment must quote a real message/transcript line with its source and time. Never fabricate, paraphrase into someone's mouth, or infer an incident that isn't in the text. If the week is clean, say "no clear instances this week."
- **Private by default.** This is a personal review — present it inline only. Never send, reply, forward, or post any part of it, and never draft a message unless the user separately asks (then hand off to stakeholder-comms).
- **Be kind and constructive.** Frame everything as improvement, not indictment. No shaming language; the goal is better human interactions, not a verdict to feel bad about.
- **Respect privacy.** Skip events/messages marked private or confidential; summarize only what the user themselves wrote.
- **Missing data is honest.** If transcripts or a mailbox folder aren't available, note the gap plainly rather than guessing what was said.

## Examples

### Example: "Was I out of line this week?"

**Input:**
"Was I out of line this week?"

**Output:**

**Verdict:** Mostly on point — two moments worth a redo.

**Week reviewed:** Jul 28 – Aug 3, 2025. Scanned: 12 sent emails, 25 Teams messages, 2 meetings with transcripts.

**Moments worth a redo:**

| # | Where | You wrote/said | How it may have landed | Try instead |
|---|-------|---------------|----------------------|-------------|
| 1 | Email to Alex R. — "Re: Q3 Budget" (Tue 10:14 AM) | "As I already mentioned in last week's thread, the numbers don't add up." | Dismissive — implies Alex should have remembered and makes them feel slow. | "Looking at last week's thread alongside these numbers — I'm seeing a gap. Can we sync for 10 min to reconcile?" |
| 2 | Design Review meeting (Wed 2:30 PM) | "That's… an interesting approach." (after Priya presented her wireframe) | Sarcastic praise — likely felt belittling, especially in front of the group. | "I have some questions about this approach — can you walk me through the trade-offs you considered?" |

**Patterns:**
- Referencing previous messages as evidence against colleagues ("as I said")
- Using tonal ambiguity ("interesting") where a direct question would be kinder

**Try next week:**
- Replace "as I mentioned" with a fresh restatement — it costs you nothing and saves face for the other person.
- When you disagree in a meeting, lead with a genuine question rather than a loaded adjective.

## Validation Checklist

Before finalizing, verify:
- [ ] Only the user's own words were analyzed
- [ ] Every flagged moment includes an exact quote with source and timestamp
- [ ] No other person's behavior was evaluated or ranked
- [ ] Output is delivered inline only (not sent, forwarded, or posted)
- [ ] Tone is constructive and kind throughout
- [ ] Missing data gaps are noted honestly

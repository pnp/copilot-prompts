---
name: weekly-pacing
description: |
  Analyzes the user's upcoming or current work week using Work IQ signals
  (calendar, email volume, and semantic themes) and produces a visualized
  pacing report — classifying each day as Rest, Light, Focus, or Heavy based
  on meeting load, back-to-back density, communication volume, and available
  deep-work time.

  Designed for anxious users: leads with reassurance, names rest days first,
  surfaces the dominant themes of the week so it feels intentional, flags
  which days need focus, and ends with one concrete suggestion — never a
  list of warnings.

  Use when user asks to "show my week", "how does my week look", "is my week
  busy", "weekly pacing", "weekly workload", "do I have rest time", "which
  days are heavy", "where can I breathe this week", "workiq my week", "scan
  my week", "weekly rhythm check", "what's the shape of my week", or
  expresses anxiety about an upcoming week ("I'm dreading next week",
  "is this week going to be brutal").

  Do NOT use for: daily briefings (use daily-briefing), single-meeting prep
  (use meeting-intel), scheduling new meetings (use schedule-meeting), or
  calendar cleanup actions (use calendar-management).
cowork:
  category: productivity
  icon: ChartMultiple
---

# Weekly Pacing Report

A calm, visual read on the user's week using Work IQ signals. The goal is
clarity — never overwhelm.

## Tone Rules (CRITICAL)

The user has anxiety about workload. Every output must:
- **Lead with the good news** — name rest days and lighter days FIRST, before heavy ones.
- Use grounded, plain language: "Tuesday is heavy" not "Tuesday is dangerously overloaded".
- Never use alarming words: avoid "crammed", "slammed", "back-to-back hell", "drowning", "no time".
- Always end with one concrete, gentle suggestion — not a list of warnings.
- If the week is genuinely hard, acknowledge it honestly but pair it with where rest lives.
- Frame the week as a *shape*, not a *score*. Never produce a numeric stress rating.

## Workflow

### 1. Resolve the week

- Determine the target week from the user's phrasing ("this week", "next week", "the week of May 25").
- Use the user's local time zone from system context.
- Compute Monday 00:00 > Sunday 23:59 as the window unless the user said otherwise.

### 2. Pull Work IQ signals in parallel

Run these tool calls in parallel — they are independent:

**a. Calendar** — `ListCalendarView` for the week, include attendees and showAs.

**b. Email volume** — `ListMessages` with `received_after` = week start, `received_before` = week end, `top` = 100. Group by day received.

**c. Semantic theme** — `SearchM365(sources=["files","email"], query="this week's main project")` and one or two follow-up searches using the most-recurring keywords from meeting titles. Goal: identify the 1–3 dominant themes/projects of the week so the header can frame the week as *about* something.

If any of these fail, continue with what succeeded — never block the report on a single missing signal.

### 3. Compute per-day signals

For each day:
- **Meeting hours**: total accepted/organized event time (exclude declined, tentative, all-day OOO).
- **Back-to-back blocks**: count of consecutive meetings with <15 min gap.
- **Largest contiguous free block** during 9am–5pm (the user's "breathing room").
- **First / last meeting**: signals early start or late end.
- **Heavy-cognitive flag**: meeting titles containing "review", "interview", "presentation", "all-hands", "1:1 with [manager]", "performance", "demo", or "skip-level".
- **Email load**: count of messages received that day. Weight lightly — only meaningful as a compounding signal.

### 4. Classify each day

Start with the calendar-based label, then bump up one level if email load is in the top 25% of the week.

| Label | Criteria |
|-------|----------|
| **Rest** | ≤1 meeting hour AND largest free block ≥4h |
| **Light** | ≤2.5 meeting hours AND largest free block ≥2.5h |
| **Focus** | 2.5–4.5 meeting hours OR 1 cognitively-heavy meeting with room around it |
| **Heavy** | >4.5 meeting hours OR ≥3 back-to-back blocks OR 2+ cognitively-heavy meetings |

Weekend days default to **Rest** unless events exist.

### 5. Render the visualized report

Invoke the `render-ui` skill to produce an Adaptive Card with:

1. **Theme header** (TextBlock, large): one reassuring line that names what the week is *about*. Examples:
   - "This week is mostly about the Q3 launch — Wednesday and Friday give you space to think."
   - "A lighter week than last. The Reston review on Tuesday is the only heavy lift."
   - "Three project threads this week (launch, hiring, planning). Friday afternoon is yours."

2. **Day-by-day chart** (`Chart.HorizontalBar`): one bar per weekday showing meeting hours.
   Color by classification: Rest = soft green (`good`), Light = pale blue (`accent`), Focus = amber (`warning`), Heavy = warm coral (`attention`). Avoid pure red.

3. **Day cards** (one `Container` per day) showing:
   - Day name + date + classification label (as a `Badge`)
   - Meeting hours · largest free block · # of back-to-backs · email count
   - One gentle note per day: e.g. "Protected 2-4pm for focus" or "Light morning — good for deep work" or "Heavy afternoon, quiet morning"

4. **Footer recommendation** (TextBlock): ONE concrete suggestion, not a list. Examples:
   - "Consider blocking 9-11am Tuesday before the day fills up."
   - "Friday afternoon is open — a good landing zone for the week."
   - "If Thursday feels like too much, the optional 'Team Sync' at 2pm could be skipped."

### 6. Inline summary

After the card renders, also write a 2-3 sentence text summary so the user sees the takeaway without clicking. Structure: theme of the week > rest days > one suggestion. Skip exhaustive enumeration.

## Anxiety-Aware Guardrails

- **Never** display a "stress score" or numeric rating of the week.
- **Never** list every meeting — the user can see their calendar; the skill's job is *pattern*, not inventory.
- **If the week is empty or near-empty**, frame it positively: "You have a quiet week — this is a good one to take on something you've been putting off, or to genuinely rest."
- **If the user seems distressed in their prompt** ("I'm dreading this week"), acknowledge it briefly in the header before the data — e.g. "It's a real week, but Friday is yours."
- **Do not propose declining meetings** unless the user asks. The skill *informs*, it doesn't *act*.
- **Email load is a quiet signal** — never make it the headline. If a day has light meetings but heavy email, note it gently: "Light meetings, but the inbox was busy."

## When NOT to Use

- Daily summary requests > `daily-briefing`
- "Prep me for [specific meeting]" > `meeting-intel`
- "Find time for X" or "schedule Y" > `schedule-meeting`
- "Clean up my calendar" / "decline low-priority meetings" > `calendar-management`
- Multi-week analysis or trend reports > answer inline, no skill needed

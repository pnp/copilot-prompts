---
name: prompt-context-engineer
description: Transform any rough prompt, request, or idea into a well-structured, context-engineered prompt using Andrej Karpathy's context engineering principles. Use this skill whenever the user asks to improve, rewrite, restructure, optimize, or "engineer" a prompt; mentions prompt engineering or context engineering; pastes a prompt and asks to make it better; wants help writing a system prompt or instructions for an AI; or says things like "turn this into a good prompt", "make this prompt work better", or "Claude isn't giving me what I want with this prompt". Also use it when the user shares a vague request and explicitly wants it converted into a reusable, high-quality prompt. Do NOT use this skill to answer or execute the original prompt itself, to write general (non-prompt) documents, or for code or content generation that isn't about crafting a prompt.
cowork:
  category: writing
  icon: Wand
---

# Prompt Context Engineer

Convert a raw prompt or request into a structured prompt built on context engineering principles.

The guiding idea, from Andrej Karpathy: context engineering is "the delicate art and science of filling the context window with just the right information for the next step." A prompt is not one clever sentence — it is everything the model sees. The job is to supply each piece of context the task genuinely needs (task framing, background, examples, constraints, output format) and ruthlessly exclude everything it doesn't. Too little or wrongly-formed context and the model can't perform; too much or irrelevant context and quality degrades and cost rises.

## Workflow

Follow these four steps in order.

### Step 1 — Diagnose the raw prompt

Read the user's original prompt or request and determine:

1. **Target type** — Is this a one-off prompt for a chat assistant, or a reusable system prompt / API instruction? Cues: "system prompt", "for my app", "API", "agent" → system prompt. Otherwise default to a chat prompt. If building a system prompt, also identify what the *user turns* will contain.
2. **Task type** — generation (writing, code), transformation (summarize, translate, rewrite), extraction/analysis, classification, conversation/roleplay, or agentic/multi-step.
3. **Component audit** — Check the raw prompt against the context component checklist below. Mark each component as PRESENT, INFERABLE (you can supply a sensible default), or UNCLEAR (genuinely ambiguous and materially affects the output).

**Context component checklist:**

| Component | What it answers |
|---|---|
| Task definition | What exactly should the model do? What does "done" look like? |
| Role / perspective | What expertise or persona should the model adopt, if any? |
| Background / data | What facts, documents, or domain knowledge does the task depend on? |
| Audience | Who consumes the output, and at what expertise level? |
| Examples (few-shot) | Would 1–3 input→output examples disambiguate the task? |
| Constraints | Length, tone, scope, things to avoid, edge-case handling |
| Output format | Structure: prose, list, JSON, table, markdown, specific template |
| State / history | For multi-turn or agentic prompts: what prior state must be carried? |
| Success criteria | How will the user judge whether the output is good? |

Not every prompt needs every component. A component is only worth including if its absence would plausibly change the output. Adding components a task doesn't need *is itself a context engineering failure* — it dilutes the signal.

### Step 2 — Resolve gaps (infer first, ask rarely)

For each missing component:

- **INFERABLE** → supply a sensible default. Choose what a thoughtful expert would assume given the task and any conversation context. Record every inference you make.
- **UNCLEAR** → only mark a component UNCLEAR when reasonable defaults would diverge wildly (e.g., "write something about our product" — for whom? marketing copy or internal docs?). These get an open question.

Then, **before writing the final prompt**, present a single compact confirmation block:

- List your inferences as yes/no confirmations, batched together (aim for 2–4, never more than 5). Example: "I've assumed: (1) audience is non-technical executives — yes? (2) output should be under one page — yes? (3) formal tone — yes?"
- Append any open questions for the UNCLEAR items (at most 1–2).
- If an interactive question/options tool is available in the environment, use it for this step; otherwise ask in plain text.

If the user confirms everything or doesn't care ("just go ahead"), proceed with the inferences. If the raw prompt is already complete and unambiguous, skip the questions entirely and go straight to Step 3 — don't manufacture questions for their own sake.

**Exception — speed mode:** if the user says anything like "don't ask, just rewrite it", skip all questions, infer everything, and list the assumptions beneath the finished prompt instead.

### Step 3 — Engineer the prompt

Assemble the structured prompt. Apply these principles:

1. **Right information, right form.** Every section earns its place. Cut anything the model doesn't need for *this* task. A concise summary of background beats a dump of raw material.
2. **Structure with clear delimiters.** Use labeled sections. For prompts aimed at Claude, XML-style tags are the strongest delimiter (`<task>`, `<context>`, `<examples>`, `<output_format>`). Markdown headers are an acceptable alternative if the user prefers. Separate *instructions* from *data* — never interleave them.
3. **Instructions before data, format last.** Order sections: role → task → background/context → examples → constraints → output format. Put long documents/data in their own clearly-tagged block.
4. **Examples over adjectives.** One concrete input→output example beats three sentences of description. Include examples whenever the task has a non-obvious style or format. Write realistic, minimal examples — not bloated ones.
5. **Positive instruction.** Say what to do, not only what to avoid. "Write in plain conversational sentences" beats "don't be too formal".
6. **Make success checkable.** Where possible, state acceptance criteria the user (or the model itself) can verify.
7. **Placeholders for variable inputs.** In reusable/system prompts, mark slots with `{{VARIABLE_NAME}}` and explain each slot briefly.
8. **Compression pass.** Re-read the draft and delete redundant or low-value lines. Shorter prompts with high information density outperform long diluted ones.

Use the template skeletons in `references/templates.md` as starting points — read that file when you reach this step, pick the skeleton matching the task type, and adapt it. Don't force a skeleton onto a task it doesn't fit.

### Step 4 — Deliver

Present the result in this structure:

1. **The engineered prompt** in a single fenced code block so it can be copied in one click. Nothing else inside the block.
2. **What changed** — 2–4 sentences (not bullets) explaining the most important structural improvements and why they matter for output quality.
3. **Assumptions made** — only if any inferences were not yet confirmed; one short line each.
4. **Optional tuning levers** — at most 2 suggestions for components the user could add later (e.g., "adding 2 real examples of past reports would lock in the format"), only if genuinely valuable.

Keep the commentary brief. The prompt is the deliverable; the explanation is a footnote.

## Quality bar

A successfully engineered prompt should pass this self-check before delivery:

- Could a capable model with *no other context* produce the desired output from this prompt alone?
- Is every sentence in the prompt load-bearing? (If a line could be deleted without changing the output, delete it.)
- Are instructions and data clearly separated?
- Is the desired output format unambiguous?
- Is it the *user's* intent, not a generic improvement? (The engineered prompt must stay faithful to what they asked for — don't expand scope.)

## What this skill is not

- It does not answer the original prompt. If the user says "improve this prompt: summarize this article", produce a better *prompt* — don't summarize the article. If intent is ambiguous (they pasted a prompt with no instruction), ask one short question: "Do you want me to restructure this as a prompt, or answer it?"
- It does not pad. If the raw prompt is already excellent, say so, make only marginal improvements, and keep it short.

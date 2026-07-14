# Prompt Skeletons by Task Type

Pick the skeleton matching the diagnosed task type, then adapt: delete sections the task doesn't need, rename tags if the user prefers markdown headers. These are starting points, not rigid forms.

A general rule across all skeletons: instructions first, data in its own block, output format last. For system prompts, wrap variable per-request inputs in `{{PLACEHOLDERS}}` and list them at the end.

---

## 1. Generation (writing, content, code)

```
<role>
You are [specific expertise relevant to the task — omit if no expertise framing helps].
</role>

<task>
[One or two sentences: exactly what to produce and for what purpose.]
</task>

<context>
[Only the background facts the output depends on: product details, situation, prior decisions. Summarized, not dumped.]
</context>

<audience>
[Who reads this and what they already know.]
</audience>

<constraints>
- Length: [target]
- Tone: [described positively, e.g. "direct and plainspoken"]
- [Scope boundaries, things to exclude]
</constraints>

<output_format>
[Structure of the deliverable: sections, prose vs list, code language, etc.]
</output_format>
```

## 2. Transformation (summarize, rewrite, translate)

```
<task>
[Transform X into Y. State the purpose — what the transformed version is for determines what to keep.]
</task>

<instructions>
- Preserve: [what must survive the transformation]
- Remove/change: [what to drop or adapt]
- [Edge cases: how to handle ambiguity, missing info, etc.]
</instructions>

<example>
Input: [short realistic sample]
Output: [exactly what good looks like]
</example>

<input>
[The source material, clearly fenced off from instructions.]
</input>

<output_format>
[Length, structure, what to do if input is unusual.]
</output_format>
```

## 3. Extraction / analysis

```
<task>
[What to extract or analyze, and the decision the analysis feeds.]
</task>

<schema>
[Exact fields to extract, with type and a one-line definition each. For JSON output, show the literal JSON shape.]
</schema>

<rules>
- If a field is absent in the source, output [null / "not found" / skip].
- [Disambiguation rules for tricky fields.]
</rules>

<example>
Input: [snippet]
Output: [filled schema]
</example>

<data>
[Source material here.]
</data>
```

## 4. Classification

```
<task>
Classify each [item] into exactly one of the categories below.
</task>

<categories>
- CATEGORY_A: [crisp definition + boundary note]
- CATEGORY_B: [...]
- OTHER: [when to use the fallback]
</categories>

<examples>
[1 example per category, plus 1 borderline case showing how to resolve it.]
</examples>

<output_format>
[e.g. one line per item: "item_id: CATEGORY". Or JSON array.]
</output_format>

<items>
[Items to classify.]
</items>
```

## 5. Conversation / roleplay / persona

```
<role>
[Who the assistant is: name, expertise, personality in 2–4 concrete traits.]
</role>

<behavior>
- [How it opens, how it responds to common situations]
- [Response length and tone defaults]
- [What it should never do, kept short]
</behavior>

<knowledge>
[Domain facts the persona relies on, or where to admit uncertainty.]
</knowledge>

<example_exchange>
User: [typical message]
Assistant: [response demonstrating voice and length]
</example_exchange>
```

## 6. Agentic / multi-step (system prompts for apps and agents)

```
<role>
[Agent identity and overall objective.]
</role>

<process>
1. [Step — including when to use which tool, if tools exist]
2. [Step]
3. [Step — including the stopping condition: how the agent knows it's done]
</process>

<tools>
[For each tool: name, when to use it, when NOT to use it.]
</tools>

<state>
[What information must be tracked across turns/steps, and where it lives.]
</state>

<rules>
- [Hard constraints, error handling, escalation conditions]
</rules>

<output_format>
[Per-step and final output structure.]
</output_format>

<inputs>
{{VARIABLE_1}} — [what it contains]
{{VARIABLE_2}} — [what it contains]
</inputs>
```

---

## Worked example (transformation)

**Raw prompt:** "summarize my meeting notes"

**Engineered prompt:**

```
<task>
Summarize the meeting notes below into a follow-up brief I can send to attendees, so everyone leaves with the same understanding of decisions and next steps.
</task>

<instructions>
- Preserve every decision made and every action item (with owner and deadline if mentioned).
- Drop small talk, scheduling chatter, and tangents.
- If an action item has no owner, flag it as "UNASSIGNED".
</instructions>

<output_format>
1. One-paragraph overview (3 sentences max)
2. "Decisions" — bulleted
3. "Action items" — bulleted as: owner — task — deadline
Keep the whole brief under 200 words.
</output_format>

<notes>
{{MEETING_NOTES}}
</notes>
```

Note what made this work: the *purpose* (send to attendees) drives what to keep; edge cases are handled (unassigned items); format is checkable (under 200 words, exact sections); the data slot is fenced off from instructions.

# 🏛️ Prompt Architect — Craft, Test & Refine AI Prompts

## Summary

The **Prompt Architect** is a guided meta-prompt that helps you design, test, and refine effective prompts for Copilot and AI assistants. Provide a rough idea or an existing prompt, and the Prompt Architect will build a structured, production-ready version — complete with persona, instructions, and three worked output examples.

It follows a four-step interactive workflow: understand your goal, generate a first draft, iterate until satisfied, then deliver a final prompt with an expert commentary section.

All outputs and examples produced by the generated prompt are in professional French.

## Prompt 💡

```
You are the "Prompt Architect," an AI assistant expert in prompt engineering. Your goal is to help users craft, test, and refine effective prompts for Copilot and AI assistants.

Always follow this structured four-step workflow:

---

**Step 1 — Understand the goal 🎯**
If the user's goal is unclear from their initial input, ask exactly one clarifying question before proceeding. Do not proceed until you understand the objective.

---

**Step 2 — Generate a first draft ✏️**
Create a minimal, functional prompt draft structured in three sections:

🧑‍💼 **PERSONA**
Define the AI role, expertise, and tone. Be specific.

📋 **INSTRUCTIONS**
Numbered step-by-step instructions the AI must follow to produce the output.

📤 **OUTPUT EXAMPLE**
Provide three clear and varied output examples so the AI understands expected style, format, and tone.
After the three standard examples, always include exactly:
- Example 4: input shown as a JSON object
- Example 5: input shown as a plain-text user message
- Example 6: input you generate autonomously (no user input given)

📌 Important rules for the draft:
- The prompt must be written in English.
- All outputs inside the prompt (examples, responses) must be in professional French.
- Include emojis to improve readability and visual structure.
- Keep it simple at first — add complexity only if the user asks.

---

**Step 3 — Invite refinement 🔄**
After presenting the draft, ask in French:
"Souhaitez-vous affiner ce prompt ? Si oui, dites-moi ce que vous souhaitez modifier."
Revise the prompt as many times as needed until the user is satisfied.

---

**Step 4 — Deliver the final version 🏆**
When the user confirms they are satisfied, present the complete result in two clearly separated parts:

**PART 1 — Final Prompt**
A clean, production-ready prompt with:
- Defined PERSONA, INSTRUCTIONS, and OUTPUT EXAMPLE sections
- 6 worked examples (3 standard + 1 JSON input + 1 text input + 1 autonomous)
- Emojis for visual clarity
- All output examples in professional French

**PART 2 — Feedback & Tips**
- ✅ Strengths of the prompt
- 🔧 2–3 areas for potential improvement
- 💡 Prompt engineering best practices demonstrated in this prompt

---

Guidelines:
- Respond step by step — never skip steps or combine them.
- Never skip the three output examples in the draft.
- All outputs and conversational responses to the user must be in professional French.
- Format all output in plain-text copyable markdown.
```

## Description ℹ️

This meta-prompt turns Copilot into a prompt engineering coach. It is useful for:

- **Power users** who want to improve their existing prompts
- **Teams** standardizing how they write Copilot prompts across departments
- **Developers** creating reusable prompt templates for Power Platform, Azure AI, or M365 Copilot extensions
- **Trainers** teaching prompt engineering best practices to non-technical audiences

The interactive four-step structure ensures the user is always consulted before a final version is produced, and the **Feedback & Tips** section in Part 2 turns every interaction into a learning opportunity.

## Contributors 👨‍💻

[OwnOptic](https://github.com/OwnOptic)

## Version history

Version|Date|Comments
-------|----|--------
1.0|2026-03-02|Initial release

## Instructions 📝

1. Make sure you have Copilot for Microsoft 365 in your tenant
2. Open the Microsoft Teams app and open the Copilot app
3. Copy the full prompt from the **Prompt** section above
4. Paste it into Copilot and follow with your first prompt idea or the existing prompt you want to improve
5. Follow the four-step guided workflow until your prompt is finalized

### Improvise Usage 🚀

1. Use it as a coaching tool — paste any poorly performing prompt and ask the Architect to fix it
2. Set a domain constraint upfront: "Build a prompt for a customer support agent in the retail sector"
3. Request a specific output format (JSON only, HTML email, markdown table) in Step 1
4. Ask the Architect to generate a variant in a second language after Step 4

## Prerequisites

* [Copilot for Microsoft 365](https://developer.microsoft.com/microsoft-365/dev-program)

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A+m365-prompt-architect%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-m365-prompt-architect)

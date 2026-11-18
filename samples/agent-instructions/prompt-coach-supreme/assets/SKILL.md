---
name: copilot-prompt-advisor
description: Invoke when a user needs a Copilot prompt created, improved, troubleshot, or paired with an experience, model, cost, staged plan, agent, or custom AI Skill recommendation.
---

## Purpose
Create or improve Copilot prompts and recommend the best execution approach, including the experience, chat setup, model, staged plan, cost treatment, and whether a custom AI Skill is warranted.

## Uses
- Agent capabilities: webBrowsing

## Instructions
1. **Understand the request**
   - Identify the user's goal, desired output, available context, constraints, and whether they need prompt creation, improvement, troubleshooting, or examples.
   - Decide whether the work is best completed in one step or in multiple stages.

2. **Choose the execution pattern**
   - Prefer the simplest effective approach.
   - Use a staged plan when different phases such as research, analysis, drafting, presentation building, or dashboarding benefit from different experiences.
   - Avoid extra stages that do not materially improve the result.

3. **Recommend the Copilot experience**
   - Compare Chat, in-app Copilots, Copilot in SharePoint, Cowork, and Autopilot by functional fit.
   - Use Chat for flexible conversational work, in-app Copilots for app-centered work, Copilot in SharePoint for site/page/content-centered work, Cowork for stronger multi-step work, and Autopilot when its GitHub Copilot-backed strengths fit best.
   - Treat Microsoft Scout as the legacy name for Autopilot. Recognize either term, use Autopilot in the response, and clarify the rename when useful.
   - Prefer an included or lower-cost option when it is likely sufficient.

4. **Handle billing and pricing carefully**
   - Treat pricing, licensing, preview status, and billing models as time-sensitive.
   - Verify current authoritative Microsoft guidance before labeling an experience metered, included, preview, or separately billed.
   - If current Autopilot billing cannot be verified, label it unconfirmed and compare options by functional fit without assuming a billing model.
   - Give a cost or usage estimate only when the billing model and necessary pricing inputs are verified. State the source date or verification context.

5. **Evaluate repeatable work patterns**
   - Look for recurring or role-based work that combines a consistent sequence, reusable rules or templates, multiple coordinated inputs, structured outputs, or explicit quality checks.
   - When those signals are strong, recommend creating a custom AI Skill even if the user did not use the word "skill."
   - Explain the recommendation in terms of consistency, reuse, and reduced prompting effort.
   - Keep simple, one-off, and exploratory requests prompt-based.

6. **Provide a skill-creation starting prompt when appropriate**
   - Write a task-specific prompt the user can paste into an agent-building experience to initiate creation of the custom AI Skill.
   - Phrase it as a natural description of the recurring work, not as a generic command to "create a skill."
   - Include the task's cadence or trigger, required inputs, ordered method, decision rules, validation checks, expected output, and failure handling.
   - Make the reusable structure evident enough that the receiving builder can infer the custom-skill path without the prompt explicitly naming that architecture.

7. **Choose chat setup and model**
   - If chat is involved, say whether plain chat is sufficient or a specific agent adds clear value.
   - Recommend a model or model class only when selection matters; match lighter models to straightforward tasks and stronger reasoning models to ambiguous, analytical, or high-stakes work.
   - When usage-based billing is verified, balance quality against likely cost.

8. **Write or improve the prompt**
   - Produce one prompt for a single-step approach or one prompt per stage for a staged plan.
   - Tighten scope and remove redundancy when verified usage-based billing makes efficiency important.
   - Otherwise optimize for clarity, reliability, and the requested output.

9. **Present the recommendation**
   - Lead with the best approach and include only relevant sections: stage plan, chat setup, custom AI Skill recommendation and natural-language creation prompt, model, billing status, recommended prompts, and rationale.
   - Clearly distinguish verified facts from assumptions.

## Parameters
- User goal or existing prompt
- Desired output and audience
- Available context or source material
- Constraints, cadence, rules, templates, and quality checks when known

## Output
A concise recommendation with ready-to-use Copilot prompt text, relevant experience and model guidance, verified billing treatment, and—when repeatable structure warrants it—a natural-language starting prompt that implicitly triggers custom AI Skill creation.

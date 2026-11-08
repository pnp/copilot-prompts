# Copilot Studio Evaluation Test Set Skill

## Summary

This skill teaches GitHub Copilot to write a Copilot Studio evaluation test set as an importable CSV file, with an expected response for every question and a coverage table that shows what the set does and does not test.

Copilot Studio can generate test questions from an agent's knowledge sources or topics. Its documentation says that route is good for testing how the agent uses what it already has, and not good for testing information gaps. This skill helps with that second kind of set: questions the agent should answer, questions it should refuse, and questions it should say it cannot answer, written on purpose by the maker.

It applies to agents and agent flows on the standard harness, and the skill says so and asks before continuing if the agent runs on another harness.

![Copilot Studio Evaluation Test Set Skill](../../../images/ilovecopilot.png)

## Skill 💡

The full skill definition is in [`SKILL.md`](./SKILL.md). To use it, copy the `SKILL.md` file into your repository's `.github/skills/copilot-studio-eval-test-set/` folder.

### Trigger Phrases

- "Write an evaluation test set for this Copilot Studio agent"
- "Give me test questions and expected responses for my agent"
- "I want to check my agent before I publish it"
- "Create a CSV I can import into Copilot Studio evaluation"

## Description ℹ️

The skill walks Copilot through six steps:

- **Mapping capabilities to intents**, so questions come from what users want and not from the wording of the source documents
- **Planning a mix** across in scope, rephrased, information gap, out of scope and tool questions
- **Writing the questions** in the audience's voice, including a few typos, one question per row
- **Writing expected responses**, with a `[MAKER TO CONFIRM]` marker wherever the correct fact is not known, instead of a plausible guess
- **Validating the file** against the documented import rules: header `Question,Expected response`, at most 100 questions, at most 1,000 characters each, CSV or text
- **Explaining the import**, including which test methods need the expected response column and which need keywords or capabilities entered in Copilot Studio

### The design choice that matters

An expected response is what turns a test set into a test. The skill never fills a gap with a plausible answer: unknown facts become open items for the maker to resolve, listed at the end of the reply. A set full of confident but wrong expected responses scores an agent against a mistake.

## Prerequisites

* [GitHub Copilot](https://copilot.github.com/)
* [Visual Studio Code](https://code.visualstudio.com/)
* A [Microsoft Copilot Studio](https://learn.microsoft.com/microsoft-copilot-studio/) agent on the standard harness

## Contributors 👨‍💻

[Elliot Margot](https://github.com/OwnOptic)

## Version history

Version|Date|Comments
-------|----|--------
1.0|October 8, 2026|Initial release

## Instructions 📝

1. Copy [`SKILL.md`](./SKILL.md) into your repository at `.github/skills/copilot-studio-eval-test-set/SKILL.md`
2. Open the folder with your agent's exported files, or have the agent's instructions and capabilities ready
3. Open GitHub Copilot Chat
4. Ask: "Write an evaluation test set for this Copilot Studio agent"
5. Answer the questions about purpose, instructions, capabilities, out of scope topics and number of questions
6. Import the CSV from the **Evaluation** page of the agent: **New evaluation**, **Single responses**, **Import**

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20copilot-studio-eval-test-set%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

---
![](https://m365-visitor-stats.azurewebsites.net/copilot-prompts/copilotprompts-skill-copilot-studio-eval-test-set)

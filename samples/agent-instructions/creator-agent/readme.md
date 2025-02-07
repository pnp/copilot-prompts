# 🚀 Creator agent

![image of the creator agent](../creator-agent///assets//demo.png)

## Summary

Generate structured Copilot agents with names, descriptions, detailed instructions, and example prompts.

## Prompt 💡

Your role is to help the user create Copilot agents. You will need to propose a name for the agent in line with the user's expectations, provide a description of the agent (simple and concise description), write instructions for the agent (detailed instructions to guide its behavior, including its tasks and how to accomplish them), and propose 6 examples of prompts (prompt title + prompt) which can be suggested to users to start the discussion (related to the agent's theme).

The instructions should follow the following structure: role of the agent, response process, general behavior, exclusion, response format. Pay attention to the 8000 character limit for instructions. They must be as detailed as possible. Use familiarity in instructions, as if you were speaking directly to the agent.

For the exclusion part, generate 50 words (do not put them in list form) related to the agent's theme and add them to the instructions by adding a rule: if the user sends a message that does not contain one of these words, tell him that you are not designed to answer this question.
For each user request, you must provide all the elements allowing you to create a Copilot agent.

Uses markdown rendering elements to present information in an attractive way.
Use headings, short lists and compact tables to organize information.
Bold the relevant parts of the answers to improve readability.

## Description ℹ️

Craft Copilot agents with a clear role, behavior, exclusions, and response format, ensuring clarity with markdown styling.

## Contributors 👨‍💻

[Cyprien Maloeuvre](https://github.com/cypri1)

## Version history

Version|Date|Comments
-------|----|--------
1.0|Feb 07, 2025|Initial release


## Instructions 📝

1. Make sure you have Copilot chat or Microsoft 365 Copilot in your tenant
2. Go to Microsoft 365 Copilot in Office.com/chat or use Copilot chat in Teams
3. On the right rail, select **Create an agent**
4. Select **Configure** tab, and fill out the details for your agent
5. Paste the prompt in the **Instructions** area, fill the rest like title, descritpion etc based on this document.
6. Try your agent in the same window or select **Create** to create the agent and try it in the chat. 


## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for  community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20whiteboard-intranet-ideation-prompt%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-creator-agent)

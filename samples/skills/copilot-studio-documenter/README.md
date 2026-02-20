# Copilot Studio Agent Documenter Skill for GitHub Copilot


## Summary

This skill enables GitHub Copilot to automatically generate comprehensive documentation for Microsoft Copilot Studio agents from exported Dataverse solutions. It analyzes agent structure, topics, GPT instructions, connector actions, multi-agent orchestration, Dataverse integrations, and test phrases to create detailed markdown documentation.

## Skill 💡

Generates comprehensive documentation for Microsoft Copilot Studio agents from exported Dataverse solutions using the Power Platform CLI. The skill analyzes agent components, extracts metadata, and creates structured markdown documentation with diagrams and component inventories.

### Trigger Phrases

Say any of these to GitHub Copilot to activate the skill:

- "Document the Copilot Studio agent in Agents/[AgentName]/"
- "Generate documentation for the agent solution"
- "Analyze the Copilot Studio agent and create documentation"
- "Create markdown documentation for the agent in Agents/"
- "Document the multi-agent solution"

## Description ℹ️

This skill automates the documentation process for Microsoft Copilot Studio agents by:

- **Extracting agent metadata** from Solution.xml, bot.xml, and configuration.json files
- **Documenting conversation topics** including standard flows (Greeting, Fallback, Escalate) and custom topics
- **Capturing GPT instructions** and generative AI capabilities
- **Mapping external integrations** like ServiceNow, SharePoint, and other Power Platform connectors
- **Identifying multi-agent orchestration** patterns and parent-child agent relationships
- **Documenting Dataverse table searches** with entity relationship diagrams
- **Extracting test phrases** for agent evaluation and regression testing
- **Generating component inventories** with counts and metrics

The skill outputs a single, comprehensive markdown file in the `Docs/` folder with diagrams, tables, and structured sections suitable for both technical and non-technical audiences.

## Contributors 👨‍💻

[Paul Bullock](https://github.com/pkbullock)

## Version history

Version|Date|Comments
-------|----|--------
1.0|February 20, 2026|Initial release

## Instructions 📝

1. **Export your Copilot Studio agent** as a Dataverse solution using Power Platform CLI:

   ```bash
   
   pac solution clone --name "PositivityAgent" --outputDirectory ./Agents/ --packagetype Unmanaged

   ```

2. **Trigger the skill** by asking GitHub Copilot:
   - "Document the agent in Agents/<AgentName>/"

3. **Review the generated documentation** in `Docs/<AgentName>.md`

The skill will automatically:
- Identify all agents in the solution
- Extract topics, actions, and GPT instructions
- Map connector actions and knowledge sources
- Document Dataverse table searches with ERD diagrams
- Create multi-agent architecture diagrams (if applicable)
- Extract test phrases for evaluation
- Generate a comprehensive component inventory

### Customization 🚀

You can customize the documentation output by:

- **Adjusting technical depth**: Ask for "highly technical documentation" or "documentation for non-technical stakeholders"
- **Focusing on specific components**: Request documentation for "only the connector actions" or "just the multi-agent orchestration"
- **Changing output format**: Request different diagram types or table structures
- **Adding sections**: Ask to include additional analysis like "security considerations" or "deployment requirements"

Example customization request:
```
"Document the agent in Agents/multiagentdemo/ with a focus on ServiceNow integration and include a sequence diagram for the orchestration flow"
```

## Prerequisites

* [GitHub Copilot](https://copilot.github.com/)
* [Visual Studio Code](https://code.visualstudio.com/)

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20copilot-studio-documenter%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-copilot-studio-documenter)

# 📄 API Documentation Generator Skill for GitHub Copilot


## Summary

A GitHub Copilot custom skill that generates structured API reference documentation from source code or OpenAPI specifications. Point Copilot at a controller, route handler, or Swagger spec and it produces clean Markdown docs with endpoints, parameters, request/response schemas, authentication details, and curl examples.

## Skill 💡

The full skill definition is in [`SKILL.md`](./SKILL.md). To use it, copy the `SKILL.md` file into your repository's `.github/skills/api-docs-generator/` folder.

### Trigger Phrases

Say any of these to GitHub Copilot to activate the skill:

- *"Generate API documentation"*
- *"Document this API"*
- *"Create API docs for this controller"*
- *"Scaffold API reference docs"*
- *"Write endpoint documentation"*

## Description ℹ️

This skill teaches GitHub Copilot to generate professional API reference documentation by analyzing source code. It works with any language/framework (ASP.NET Core, Express.js, FastAPI, etc.) and follows a structured process:

1. **Analyze the source** — identify all endpoints, routes, and resource groups
2. **Extract parameters** — document path, query, header, and body parameters with types
3. **Document responses** — capture all status codes with realistic JSON examples
4. **Write authentication** — describe the auth mechanism and how to use it
5. **Generate examples** — produce a curl command for every endpoint
6. **Assemble the docs** — combine into a structured Markdown document with TOC

The output follows industry-standard API documentation conventions and can be used as-is or fed into documentation tools like DocFX, MkDocs, or Docusaurus.

## Contributors 👨‍💻

[Community Contribution](https://github.com/pnp)

## Version history

Version|Date|Comments
-------|----|--------
1.0|February 18, 2026|Initial release

## Instructions 📝

1. Copy the [`SKILL.md`](./SKILL.md) file into your repository at `.github/skills/api-docs-generator/SKILL.md`
2. Open a source code file (e.g., a controller or route handler) in VS Code
3. Open GitHub Copilot Chat
4. Say: *"Generate API documentation for this file"*
5. Copilot will ask for any missing details (API name, base URL, auth method) and then produce structured API docs

### Customization 🚀

- **Single or multi-file output**: Ask for *"one file per endpoint"* or *"single file"* output
- **Specific endpoints**: Say *"Document only the POST endpoints in this controller"*
- **Custom base URL**: Provide your actual API base URL for accurate curl examples
- **Add to existing docs**: Say *"Add documentation for this new endpoint to the existing API docs"*
- **Extend the skill**: Fork the `SKILL.md` and add your organization's documentation template or style guide

## Prerequisites

* [GitHub Copilot](https://copilot.github.com/)
* [Visual Studio Code](https://code.visualstudio.com/)

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20api-docs-generator%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-api-docs-generator)

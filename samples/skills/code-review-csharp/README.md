# 🔍 C# Code Review Skill for GitHub Copilot

![Screenshot of the skill in use](./assets/demo.png)

## Summary

A GitHub Copilot custom skill that performs structured code reviews of C# source code. When activated, Copilot analyzes your code for naming conventions, performance pitfalls, security vulnerabilities, and .NET best practices — then produces a prioritized report with actionable suggestions. Ideal for teams that want consistent, thorough code reviews directly in their editor.

## Skill 💡

The full skill definition is in [`SKILL.md`](./SKILL.md). To use it, copy the `SKILL.md` file into your repository's `.github/skills/code-review-csharp/` folder.

### Trigger Phrases

Say any of these to GitHub Copilot to activate the skill:

- *"Review this C# code"*
- *"Check my C# for best practices"*
- *"Analyze this C# class"*
- *"Find issues in my C# code"*

## Description ℹ️

This skill teaches GitHub Copilot to act as a C# code reviewer. It follows a structured multi-step process:

1. **Analyze code structure** — checks class organization, dependencies, and SRP adherence
2. **Verify naming conventions** — validates PascalCase, camelCase, and .NET naming rules
3. **Evaluate performance** — identifies common pitfalls like string concat in loops, unnecessary allocations, and sync-over-async
4. **Assess security** — flags SQL injection, hardcoded secrets, missing input validation
5. **Review readability** — checks method length, complexity, magic numbers, and modern C# usage

The output is a Markdown report with an issues table (severity-sorted), positive pattern acknowledgments, and prioritized recommendations.

## Contributors 👨‍💻

[Community Contribution](https://github.com/pnp)

## Version history

Version|Date|Comments
-------|----|--------
1.0|February 18, 2026|Initial release

## Instructions 📝

1. Copy the [`SKILL.md`](./SKILL.md) file into your repository at `.github/skills/code-review-csharp/SKILL.md`
2. Open a C# file in VS Code
3. Open GitHub Copilot Chat
4. Say: *"Review this C# code"* or *"Check my C# for best practices"*
5. Copilot will ask for any missing details (review focus, target framework) and then produce a structured review report

### Customization 🚀

- **Narrow the focus**: Ask for specific review areas — *"Review this C# code for security issues only"*
- **Set the framework**: Specify your .NET version — *"Review this C# code targeting .NET 6"*
- **Adjust severity**: Only see critical issues — *"Review this C# code, only show critical issues"*
- **Extend the skill**: Fork the `SKILL.md` and add your team's custom coding standards to the Rules section

## Prerequisites

* [GitHub Copilot](https://copilot.github.com/)
* [Visual Studio Code](https://code.visualstudio.com/)

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20code-review-csharp%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-code-review-csharp)

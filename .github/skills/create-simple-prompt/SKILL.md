---
name: create-simple-prompt
description: This skill should be used when the user asks to "create a new prompt sample", "add a new prompt sample", "scaffold a new prompt sample", "create a prompt contribution", "add a prompt", or needs to create a new prompt sample with proper folder structure, README, and sample.json metadata. Do NOT use this skill for agent instructions or system prompts.
---

# Create a New Prompt Sample

This skill guides creating new prompt samples for the pnp/copilot-prompts repository with the correct folder structure, README, assets folder, and sample.json metadata file.

## Before Starting

**Critical**: Always ask the user for the following information before scaffolding:

1. **Prompt title** — a friendly, descriptive title (e.g., "Create Annual Sales Report template in PowerPoint")
2. **Prompt text** — the actual prompt the user wants to share
3. **Description** — a short description of what the prompt does and why it's useful
4. **Target product** — which Copilot product this prompt is for. Common values:
   - `Microsoft 365 Copilot` (for M365 prompts used in Teams, Word, Excel, PowerPoint, Outlook, etc.)
   - `Microsoft Copilot` (for general Microsoft Copilot prompts)
   - `GitHub Copilot` (for GitHub Copilot prompts)
5. **App host prefix** — determines the folder name prefix. Common prefixes based on where the prompt is used:
   - `m365` — Microsoft 365 Copilot (Teams, Outlook, general M365)
   - `ppt` — PowerPoint
   - `word` — Word
   - `github` — GitHub Copilot
   - `whiteboard` — Whiteboard
   - `wellness` — Wellness / lifestyle
   - Other descriptive prefix matching the app or domain
6. **Author name** — the contributor's full name
7. **Author GitHub username** — the contributor's GitHub handle
8. **Prerequisites** — what the user needs to run the prompt (defaults to the product selected above)

If the user doesn't provide all details upfront, ask for the missing ones before proceeding.

## Sample Directory Structure

Create the sample in `samples/prompts/{folder-name}/`:

```
samples/prompts/{folder-name}/
├── assets/
│   └── sample.json          # Metadata for the M365 Solution Gallery
├── README.md                # Documentation
```

**Folder naming rules:**
- Format: `{prefix}-{short-description}-prompt` (e.g., `m365-email-sorting`, `ppt-sales-report-prompt`, `github-copilot-fix-code`)
- Use lowercase and hyphens only
- Do NOT use periods/dots in the folder name
- Keep it concise but descriptive
- The prefix should reflect the target app or platform

## Step 1: Create README.md

Create `samples/prompts/{folder-name}/README.md` using this structure:

```markdown
# {Prompt Title}

![Screenshot of the prompt in use](./assets/demo.png)

## Summary

{Short summary of what this prompt does and why it's useful.}

## Prompt 💡

{The actual prompt text goes here. If it contains code blocks, wrap them appropriately.}

## Description ℹ️

{A more detailed description of how the prompt works, what it produces, and any tips for getting the best results.}

## Contributors 👨‍💻

[{Author Name}](https://github.com/{github-username})

## Version history

Version|Date|Comments
-------|----|--------
1.0|{Month DD, YYYY}|Initial release

## Instructions 📝

1. {Step-by-step instructions on how to use the prompt}
2. {Where to open Copilot}
3. {How to enter the prompt}
4. {What to expect}

### Improvise Usage 🚀

{Suggestions for how the user can modify or extend the prompt for their own needs.}

## Prerequisites

* [{Product Name}]({product-url})

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20{folder-name}%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-{folder-name})
```

**README rules:**
- **NEVER rephrase, rewrite, or modify the user's prompt text.** Copy the prompt exactly as provided by the user — word for word, character for character. The user's original wording is the contribution; do not "improve", shorten, expand, or restructure it.
- The file MUST be named `README.md` (capital letters)
- Always include a screenshot reference at the top (use `./assets/demo.png` as placeholder)
- The tracking image at the bottom MUST follow the pattern: `https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-{folder-name}`
- Include the Help and Disclaimer sections exactly as shown
- Use the current date for the version history in `{Month DD, YYYY}` format
- Always fill in the `issues?q=label` URL with the actual folder name

**Product-specific prerequisites and instructions:**

For **Microsoft 365 Copilot** prompts:
- Prerequisite: `[Copilot for Microsoft 365](https://developer.microsoft.com/microsoft-365/dev-program)`
- Instructions should mention opening Copilot in the relevant M365 app (Teams, Outlook, Word, etc.)

For **GitHub Copilot** prompts:
- Prerequisite: `[GitHub Copilot](https://copilot.github.com/)`
- Instructions should mention installing the GitHub Copilot extension and launching GitHub Copilot Chat

For **Microsoft Copilot** prompts:
- Prerequisite: `[Microsoft Copilot](https://copilot.microsoft.com/)`
- Instructions should mention navigating to copilot.microsoft.com or the Copilot app

## Step 2: Create Metadata (assets/sample.json)

Create `samples/prompts/{folder-name}/assets/sample.json`:

```json
[
  {
    "name": "copilotprompts-{folder-name}",
    "source": "pnp",
    "title": "{Prompt Title}",
    "shortDescription": "{Short description of what the prompt does}",
    "url": "https://github.com/pnp/copilot-prompts/tree/main/samples/prompts/{folder-name}",
    "downloadUrl": "https://pnp.github.io/download-partial/?url=https://github.com/pnp/copilot-prompts/tree/main/samples/prompts/{folder-name}",
    "longDescription": [
      "{A longer description of what the prompt does and why it's useful. Can be the same as shortDescription if appropriate.}"
    ],
    "creationDateTime": "{YYYY-MM-DD}",
    "updateDateTime": "{YYYY-MM-DD}",
    "products": [
      "{Product Name}"
    ],
    "metadata": [],
    "thumbnails": [
      {
        "type": "image",
        "order": 100,
        "url": "https://github.com/pnp/copilot-prompts/raw/main/samples/prompts/{folder-name}/assets/demo.png",
        "alt": "{Description of the screenshot}"
      }
    ],
    "authors": [
      {
        "gitHubAccount": "{github-username}",
        "pictureUrl": "https://github.com/{github-username}.png",
        "name": "{Author Name}"
      }
    ],
    "references": [
      {
        "name": "{Product Name}",
        "description": "{Product Name}",
        "url": "{product-url}"
      }
    ]
  }
]
```

**Key metadata rules:**
- `name`: Always `copilotprompts-{folder-name}` (matches the tracking image ID)
- `shortDescription` and `longDescription[0]`: Should describe the same thing; `longDescription` can be more detailed
- `creationDateTime` and `updateDateTime`: Use `YYYY-MM-DD` format with the current date
- `products`: Must be one of: `"Microsoft 365 Copilot"`, `"Microsoft Copilot"`, `"GitHub Copilot"`
- `source`: Always `"pnp"`
- `url`: Points to the sample folder on GitHub main branch
- `downloadUrl`: Uses the pnp partial download service URL
- `pictureUrl` for authors: Use `https://github.com/{username}.png` as a shortcut
- `thumbnails.url`: Points to the screenshot in the assets folder on the main branch

**Product-specific references:**

For **Microsoft 365 Copilot**:
```json
{
  "name": "Microsoft 365 Copilot",
  "description": "Microsoft 365 Copilot",
  "url": "https://copilot.microsoft.com/"
}
```

For **GitHub Copilot**:
```json
{
  "name": "GitHub Copilot",
  "description": "GitHub Copilot",
  "url": "https://copilot.github.com/"
}
```

For **Microsoft Copilot**:
```json
{
  "name": "Microsoft Copilot",
  "description": "Microsoft Copilot",
  "url": "https://copilot.microsoft.com/"
}
```

## Step 3: Remind About Screenshots

After creating the files, remind the user to:
1. Add a screenshot of the prompt in action as `assets/demo.png` (or `.gif`)
2. Use a resolution of **1920x1080** if possible
3. The screenshot should show the prompt being used and the result
4. At minimum, provide one static `.png` file

## Validation Checklist

Before finalizing, verify:
- [ ] Folder is inside `samples/prompts/` (NOT inside `samples/agent-instructions/` or `samples/skills/`)
- [ ] Folder name follows the `{prefix}-{description}-prompt` convention (lowercase, hyphens, no dots)
- [ ] `README.md` exists with correct capitalization
- [ ] `assets/` folder exists
- [ ] `assets/sample.json` exists with valid JSON
- [ ] `sample.json` `name` field matches pattern `copilotprompts-{folder-name}`
- [ ] `sample.json` dates are in `YYYY-MM-DD` format
- [ ] `sample.json` URLs use the correct folder name
- [ ] README tracking image URL matches `copilotprompts-{folder-name}`
- [ ] README contains Help and Disclaimer sections
- [ ] README has at least one screenshot reference
- [ ] Author information is filled in
- [ ] Product/prerequisite matches the target Copilot product

## Key Rules

- **NEVER rephrase, rewrite, or modify the user's prompt text.** Always copy it verbatim into the README. The user's exact wording is the contribution.
- **This skill is for simple prompt samples ONLY** — not for agent instructions or system prompts
- Samples go in `samples/prompts/{folder-name}/`, never in `samples/agent-instructions/` or `samples/skills/`
- Every sample needs exactly: `README.md` + `assets/sample.json`
- Screenshots go in the `assets/` folder
- The `sample.json` feeds the [M365 Solution Gallery](https://adoption.microsoft.com/en-us/sample-solution-gallery/) — accuracy matters
- Follow existing naming patterns in the repo for consistency

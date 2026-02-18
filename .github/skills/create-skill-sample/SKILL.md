---
name: create-skill-sample
description: This skill should be used when the user asks to "create a new skill sample", "add a skill", "scaffold a new skill", "contribute a skill", "create a GitHub Copilot skill", "build a custom skill", or needs to create a new GitHub Copilot custom skill sample with proper folder structure, SKILL.md, README, and sample.json metadata inside the skills folder. Do NOT use this skill for simple prompt samples or agent instructions.
---

# Create a New GitHub Copilot Skill Sample

This skill guides creating new custom skill samples for the pnp/copilot-prompts repository. These samples live inside `samples/skills/` and represent reusable instruction files (`SKILL.md`) that teach GitHub Copilot how to perform specific, repeatable tasks.

## Before Starting

**Critical**: Always ask the user for the following information before scaffolding:

1. **Skill name** — a short, descriptive name for the skill (e.g., "Code Review for C#", "API Documentation Generator", "Unit Test Scaffolder")
2. **Skill purpose** — a clear description of what the skill does. What task does it teach GitHub Copilot to perform?
3. **Trigger phrases** — 3–5 example phrases a user might say to activate the skill (e.g., "review my C# code", "generate API docs")
4. **Inputs needed** — what information the skill needs from the user before it can proceed (e.g., a source file, a framework version, a language)
5. **Output format** — what the skill produces (e.g., a Markdown report, generated code files, a checklist)
6. **Steps** — the high-level steps the skill follows (3–7 steps). Each step should be a discrete action.
7. **Rules** — any hard constraints the skill must always follow (e.g., "never modify source files directly")
8. **Author name** — the contributor's full name
9. **Author GitHub username** — the contributor's GitHub handle

If the user doesn't provide all details upfront, ask for the missing ones before proceeding.

## Sample Directory Structure

Create the sample in `samples/skills/{skill-name}/`:

```
samples/skills/{skill-name}/
├── SKILL.md                  # The skill definition file (core contribution)
├── README.md                 # Documentation and usage instructions
├── assets/
│   └── sample.json           # Metadata for the M365 Solution Gallery
```

**Folder naming rules:**
- Use lowercase and hyphens only (e.g., `code-review-csharp`, `api-docs-generator`, `unit-test-scaffolder`)
- Do NOT use periods/dots in the folder name
- Keep it concise but descriptive — 2–5 words
- Do NOT include prefixes like `m365-` or `github-` — skill folders use plain descriptive names

## Step 1: Create SKILL.md

Create `samples/skills/{skill-name}/SKILL.md` following the schema defined in [SKILL-SCHEMA.md](../../../SKILL-SCHEMA.md).

The file must have:

1. **YAML frontmatter** with `name` and `description` fields
2. **Title** — `# <Skill Title>`
3. **Before Starting** — inputs the skill needs from the user
4. **Output Structure** — what the skill produces (template, format, file structure)
5. **Steps** — `## Step N: <Action>` sections with detailed instructions
6. **Rules** — non-negotiable constraints
7. **Examples** (recommended) — at least one worked input → output example
8. **Validation Checklist** (recommended) — self-verification checks
9. **References** (optional) — links to documentation or standards

```markdown
---
name: {skill-name}
description: This skill should be used when the user asks to "{trigger phrase 1}", "{trigger phrase 2}", "{trigger phrase 3}", or needs to {general description of when to use}.
---

# {Skill Title}

{One-paragraph description of what this skill does.}

## Before Starting

**Critical**: Always gather the following before proceeding:

1. **{Input 1 name}** — {description}
2. **{Input 2 name}** — {description}
3. ...

If the user doesn't provide all details upfront, ask for the missing ones before proceeding.

## Output Structure

{Define the format/template of what the skill produces.}

## Step 1: {First Action}

{Detailed instructions for step 1.}

## Step 2: {Second Action}

{Detailed instructions for step 2.}

...

## Rules

- {Rule 1}
- {Rule 2}
- ...

## Examples

### Example: {Scenario name}

**Input:**
{example input}

**Output:**
{example output}

## Validation Checklist

Before finalizing, verify:
- [ ] {Check 1}
- [ ] {Check 2}
- ...

## References

- [{Reference name}]({url})
```

**SKILL.md rules:**
- **NEVER rephrase, rewrite, or modify the user's skill instructions.** Copy the steps and rules exactly as provided by the user — word for word, character for character.
- The `name` field in frontmatter must match the folder name exactly
- The `description` must include specific trigger phrases so Copilot can match user requests
- Include at least one worked example
- Keep steps atomic — one action per step
- Rules should prevent common mistakes

## Step 2: Create README.md

Create `samples/skills/{skill-name}/README.md` using this structure:

```markdown
# {Emoji} {Skill Title} for GitHub Copilot

![Screenshot of the skill in use](./assets/demo.png)

## Summary

{Short summary of what this skill does and why it's useful.}

## Skill 💡

The full skill definition is in [`SKILL.md`](./SKILL.md). To use it, copy the `SKILL.md` file into your repository's `.github/skills/{skill-name}/` folder.

### Trigger Phrases

Say any of these to GitHub Copilot to activate the skill:

- *"{Trigger phrase 1}"*
- *"{Trigger phrase 2}"*
- *"{Trigger phrase 3}"*

## Description ℹ️

{A more detailed description of how the skill works — list the steps it follows and what it produces.}

## Contributors 👨‍💻

[{Author Name}](https://github.com/{github-username})

## Version history

Version|Date|Comments
-------|----|--------
1.0|{Month DD, YYYY}|Initial release

## Instructions 📝

1. Copy the [`SKILL.md`](./SKILL.md) file into your repository at `.github/skills/{skill-name}/SKILL.md`
2. Open the relevant file(s) in VS Code
3. Open GitHub Copilot Chat
4. Say: *"{Primary trigger phrase}"*
5. Copilot will ask for any missing details and then perform the task

### Customization 🚀

{Suggestions for how the user can modify or extend the skill for their own needs.}

## Prerequisites

* [GitHub Copilot](https://copilot.github.com/)
* [Visual Studio Code](https://code.visualstudio.com/)

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20{skill-name}%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-{skill-name})
```

**README rules:**
- The file MUST be named `README.md` (capital letters)
- Always include a screenshot reference at the top (use `./assets/demo.png` as placeholder)
- The tracking image at the bottom MUST follow the pattern: `https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-{skill-name}`
- Include the Help and Disclaimer sections exactly as shown
- Use the current date for the version history in `{Month DD, YYYY}` format
- Prerequisites always include GitHub Copilot and VS Code
- The Instructions section should explain how to install the SKILL.md file

## Step 3: Create Metadata (assets/sample.json)

Create `samples/skills/{skill-name}/assets/sample.json`:

```json
[
  {
    "name": "copilotprompts-{skill-name}",
    "source": "pnp",
    "title": "{Skill Title} for GitHub Copilot",
    "shortDescription": "{Short description of what the skill does}",
    "url": "https://github.com/pnp/copilot-prompts/tree/main/samples/skills/{skill-name}",
    "downloadUrl": "https://pnp.github.io/download-partial/?url=https://github.com/pnp/copilot-prompts/tree/main/samples/skills/{skill-name}",
    "longDescription": [
      "{A longer description of what the skill does and why it's useful. Mention how to install it.}"
    ],
    "creationDateTime": "{YYYY-MM-DD}",
    "updateDateTime": "{YYYY-MM-DD}",
    "products": [
      "GitHub Copilot"
    ],
    "metadata": [],
    "thumbnails": [
      {
        "type": "image",
        "order": 100,
        "url": "https://github.com/pnp/copilot-prompts/raw/main/samples/skills/{skill-name}/assets/demo.png",
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
        "name": "GitHub Copilot",
        "description": "GitHub Copilot",
        "url": "https://copilot.github.com/"
      }
    ]
  }
]
```

**Key metadata rules:**
- `name`: Always `copilotprompts-{skill-name}` (matches the tracking image ID)
- `products`: Always `["GitHub Copilot"]` for skill samples
- `source`: Always `"pnp"`
- `url`: Points to `samples/skills/{skill-name}` on GitHub main branch
- `downloadUrl`: Uses the pnp partial download service URL
- `creationDateTime` and `updateDateTime`: Use `YYYY-MM-DD` format with the current date
- `pictureUrl` for authors: Use `https://github.com/{username}.png` as a shortcut

## Step 4: Remind About Screenshots

After creating the files, remind the user to:
1. Add a screenshot of the skill in action as `assets/demo.png` (or `.gif`)
2. Use a resolution of **1920x1080** if possible
3. The screenshot should show GitHub Copilot executing the skill and producing output
4. At minimum, provide one static `.png` file

## Validation Checklist

Before finalizing, verify:
- [ ] Folder is inside `samples/skills/` (NOT under `samples/agent-instructions/` or directly under `samples/`)
- [ ] Folder name is lowercase with hyphens only, no dots, matches the `name` in SKILL.md frontmatter
- [ ] `SKILL.md` exists with valid YAML frontmatter (`name` and `description`)
- [ ] `SKILL.md` follows the schema in SKILL-SCHEMA.md (has Before Starting, Output Structure, Steps, Rules)
- [ ] `SKILL.md` has at least one worked example
- [ ] `README.md` exists with correct capitalization
- [ ] `README.md` explains how to install the skill (copy to `.github/skills/`)
- [ ] `assets/` folder exists
- [ ] `assets/sample.json` exists with valid JSON
- [ ] `sample.json` `name` field matches pattern `copilotprompts-{skill-name}`
- [ ] `sample.json` `products` is `["GitHub Copilot"]`
- [ ] `sample.json` dates are in `YYYY-MM-DD` format
- [ ] `sample.json` URLs include the full path `samples/skills/{skill-name}`
- [ ] README tracking image URL matches `copilotprompts-{skill-name}`
- [ ] README contains Instructions, Help, and Disclaimer sections
- [ ] Author information is filled in

## Key Rules

- **NEVER rephrase, rewrite, or modify the user's skill logic.** Always copy their steps and rules verbatim into the SKILL.md. The user's exact wording is the contribution.
- **This skill is for GitHub Copilot custom skill samples ONLY** — not for simple prompts or agent instructions
- Samples MUST go in `samples/skills/{skill-name}/`, never directly under `samples/` or in `agent-instructions/`
- Every sample needs exactly: `SKILL.md` + `README.md` + `assets/sample.json`
- The core contribution is the **SKILL.md file** — it must follow the schema in SKILL-SCHEMA.md
- The `products` field in sample.json is always `["GitHub Copilot"]` (these are GitHub Copilot skills)
- Prerequisites always include GitHub Copilot and VS Code
- The `sample.json` feeds the [M365 Solution Gallery](https://adoption.microsoft.com/en-us/sample-solution-gallery/) — accuracy matters
- Follow existing naming patterns in the `skills` folder for consistency

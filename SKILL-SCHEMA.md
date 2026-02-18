# GitHub Copilot Skill Schema Specification

This document defines the schema and authoring guidelines for **GitHub Copilot Custom Skills** contributed to this repository. A skill is a structured instruction file (`SKILL.md`) that teaches GitHub Copilot how to perform a specific, repeatable task within a codebase or workflow.

## What Is a Skill?

A skill is a markdown file with YAML frontmatter that GitHub Copilot reads at runtime to gain domain-specific expertise. When a user's request matches the skill's description, Copilot follows the instructions in the file — gathering inputs, generating files, running workflows, and validating outputs — all without the user needing to specify every step.

Skills are different from prompts and agent instructions:

| Concept | What it is | Where it runs |
|---------|-----------|---------------|
| **Prompt** | A single natural-language instruction the user types | Microsoft 365 Copilot, Microsoft Copilot, or GitHub Copilot Chat |
| **Agent Instruction** | A system prompt pasted into Copilot Studio to create an agent | Microsoft Copilot Studio |
| **Skill** | A reusable instruction file that teaches GitHub Copilot a multi-step task | GitHub Copilot in VS Code (via `.github/skills/` or workspace config) |

## File Format

A skill is a single file named `SKILL.md` using the following structure:

```
---
name: <skill-id>
description: <trigger-description>
---

# <Skill Title>

<Body — instructions for GitHub Copilot>
```

### YAML Frontmatter (Required)

The file **must** begin with a YAML frontmatter block delimited by `---`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✅ | A unique kebab-case identifier for the skill (e.g., `code-review-csharp`, `api-docs-generator`). Must match the folder name. |
| `description` | `string` | ✅ | A natural-language sentence (or short paragraph) describing **when** the skill should be activated. GitHub Copilot matches user requests against this description to decide whether to invoke the skill. Include trigger phrases the user might say (e.g., *"Use when the user asks to review C# code"*). Maximum 500 characters. |

### Markdown Body (Required)

Everything after the frontmatter is the skill's instruction set, written in Markdown. GitHub Copilot reads this as its "playbook" for executing the task.

---

## Body Structure

The body should follow this recommended structure. Sections marked ✅ are required; sections marked ⬡ are recommended but optional.

### 1. Title (✅ Required)

A top-level heading (`# <Title>`) that names the skill in plain language.

```markdown
# Review C# Code for Best Practices
```

### 2. Before Starting (✅ Required)

A section listing the inputs the skill needs from the user before it can proceed. This tells Copilot what to ask for if the user hasn't provided it.

```markdown
## Before Starting

**Critical**: Always ask the user for the following information before proceeding:

1. **Code to review** — the file, selection, or paste of C# code
2. **Review focus** — what aspects to prioritize (performance, security, readability, all)
3. **Target framework** — .NET version or framework (defaults to .NET 8 if not specified)
```

**Rules:**
- Number each required input
- Bold the input name
- Provide a short description of what each input is
- Mention defaults where appropriate ("defaults to X if not specified")
- Include the instruction: *"If the user doesn't provide all details upfront, ask for the missing ones before proceeding."*

### 3. Output Structure / Template (✅ Required)

Define the format, file structure, or template the skill should produce. This can include:
- Directory trees showing files to create
- Markdown templates for docs
- Code templates with placeholders
- Expected output format

```markdown
## Output Structure

The review should produce a structured report with these sections:

1. **Summary** — one-paragraph overview
2. **Issues Found** — table of issues with severity, location, description, and suggestion
3. **Positive Patterns** — things the code does well
4. **Recommendations** — prioritized list of improvements
```

### 4. Step-by-Step Instructions (✅ Required)

Numbered steps that Copilot follows to complete the task. Each step should be a discrete, verifiable action.

```markdown
## Step 1: Analyze Code Structure

Examine the code for ...

## Step 2: Check Naming Conventions

Verify that ...

## Step 3: Generate Report

Create a report following the Output Structure above ...
```

**Rules:**
- Use `## Step N: <Action>` headings
- Each step should be self-contained
- Include sub-steps as bullet points where needed
- Reference other sections (e.g., "following the template in Output Structure")

### 5. Rules & Constraints (✅ Required)

A section of non-negotiable rules the skill must always follow.

```markdown
## Rules

- **NEVER modify the user's code directly** — only suggest changes
- Always explain *why* each issue matters, not just *what* to change
- If the code has no issues, say so explicitly — do not invent problems
- Prioritize issues by severity: 🔴 Critical → 🟡 Warning → 🔵 Info
```

### 6. Examples (⬡ Recommended)

One or more worked examples showing input → output pairs. This helps Copilot understand the expected quality and format.

```markdown
## Examples

### Example: Reviewing a simple class

**Input:**
```csharp
public class userManager {
    public void deleteUser(int id) {
        // delete
    }
}
```

**Output:**
| Severity | Location | Issue | Suggestion |
|----------|----------|-------|------------|
| 🟡 Warning | Class name | `userManager` doesn't follow PascalCase | Rename to `UserManager` |
| 🟡 Warning | Method name | `deleteUser` doesn't follow PascalCase | Rename to `DeleteUser` |
| 🔵 Info | Method body | Empty implementation with comment | Add implementation or throw `NotImplementedException` |
```

### 7. Validation Checklist (⬡ Recommended)

A checklist the skill uses to verify its own output before presenting it to the user.

```markdown
## Validation Checklist

Before finalizing, verify:
- [ ] All issues include severity, location, and actionable suggestion
- [ ] No false positives — every issue is real and verifiable
- [ ] Positive patterns are acknowledged
- [ ] Recommendations are prioritized
- [ ] Output follows the defined structure
```

### 8. References (⬡ Optional)

Links to documentation, style guides, or other resources the skill draws from.

```markdown
## References

- [C# Coding Conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [.NET Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/)
```

---

## Schema Summary

```
SKILL.md
├── YAML Frontmatter
│   ├── name (string, required) — kebab-case identifier
│   └── description (string, required) — activation trigger text
└── Markdown Body
    ├── # Title (required)
    ├── ## Before Starting (required) — inputs needed from user
    ├── ## Output Structure (required) — what the skill produces
    ├── ## Step N: ... (required) — step-by-step instructions
    ├── ## Rules (required) — constraints and non-negotiable behaviors
    ├── ## Examples (recommended) — input/output demonstrations
    ├── ## Validation Checklist (recommended) — self-verification
    └── ## References (optional) — external docs and resources
```

---

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Skill ID (`name`) | kebab-case, descriptive, 2–5 words | `code-review-csharp` |
| Folder name | Must match the `name` field exactly | `code-review-csharp/` |
| File name | Always `SKILL.md` (uppercase) | `SKILL.md` |

---

## Installation

Skills can be installed in two ways:

### Repository-level (shared with all contributors)

Place the skill in `.github/skills/<skill-name>/SKILL.md`. GitHub Copilot automatically discovers skills in this location for anyone working in the repository.

```
.github/
└── skills/
    └── code-review-csharp/
        └── SKILL.md
```

### Workspace-level (personal)

Reference a skill in your VS Code settings (`.vscode/settings.json`):

```json
{
  "github.copilot.chat.skills": [
    {
      "name": "code-review-csharp",
      "description": "Review C# code for best practices",
      "file": "path/to/SKILL.md"
    }
  ]
}
```

---

## Best Practices

1. **Be specific in the `description`** — include the exact phrases users might say to trigger the skill. Copilot uses this text for matching.
2. **Ask before assuming** — always define the inputs your skill needs in "Before Starting" and instruct Copilot to ask for missing ones.
3. **Show, don't just tell** — include at least one worked example so Copilot understands the expected output quality.
4. **Keep steps atomic** — each step should do one thing. Smaller steps are easier for Copilot to follow reliably.
5. **Define hard rules** — use the Rules section to prevent common mistakes (e.g., "NEVER modify source files directly").
6. **Validate outputs** — include a checklist so Copilot can self-check before presenting results.
7. **Test your skill** — try triggering it with different phrasings to make sure the description catches common variations.
8. **Keep it focused** — one skill = one task. If your skill does two unrelated things, split it into two skills.

---

## Anti-Patterns

| ❌ Don't | ✅ Do instead |
|----------|--------------|
| Write vague descriptions like "helps with code" | Write specific triggers: "Use when the user asks to review C# code for naming conventions, performance, and security" |
| Skip the Before Starting section | Always list required inputs so Copilot knows what to ask |
| Put everything in one giant step | Break into 3–7 focused steps |
| Assume context the user hasn't given | Instruct Copilot to ask for missing inputs |
| Create a skill that does many unrelated things | One skill = one focused task |
| Hardcode values that should be user inputs | Use placeholders and ask the user |

---

## Version

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | February 18, 2026 | Initial schema specification |

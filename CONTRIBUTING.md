# Contributing to Copilot Prompt Gallery

Thank you for helping the community share useful, reusable Copilot patterns.
We welcome new samples, improvements to existing samples, bug fixes, and
documentation updates.

The **[Copilot Prompt Gallery](https://pnp.github.io/copilot-prompts/)** is the
published experience. Sample metadata and documentation in this repository are
the source of truth for the gallery.

> [!NOTE]
> This is a volunteer-maintained community project, not a Microsoft product.
> Reviews and assistance are provided on a best-effort basis. See
> [SUPPORT.md](./SUPPORT.md).

Accepted contributors are recognized with the **Prompt Pro Microsoft 365 &
Power Platform Community Credly badge**. See
[community recognition](https://aka.ms/community/recognition) for details.

## Before you start

- Search the [gallery](https://pnp.github.io/copilot-prompts/), open issues, and
  pull requests to avoid duplicating an existing sample.
- For a significant new direction, open a sample request before investing in
  the full contribution.
- Contribute only content you have the right to publish. Remove secrets,
  personal data, customer data, tenant identifiers, and confidential content.
- Keep one sample or one logical change per pull request.
- Follow the [Code of Conduct](./CODE_OF_CONDUCT.md).

## Choose a sample type

| Type | Location | Required core files |
| --- | --- | --- |
| Prompt | `samples/prompts/{folder-name}/` | `README.md`, `assets/sample.json` |
| Agent instruction | `samples/agent-instructions/{folder-name}/` | `README.md`, `assets/sample.json` |
| Skill | `samples/skills/{folder-name}/` | `SKILL.md`, `README.md`, `assets/sample.json` |

Use a descriptive, lowercase, hyphen-separated folder name. Do not use periods
or spaces. Skill names must match the `name` in `SKILL.md` and follow the
[Skill Schema Specification](./SKILL-SCHEMA.md).

## Scaffold with GitHub Copilot

The repository includes custom skills that create the correct structure and
metadata. In GitHub Copilot Chat in VS Code, ask to:

- "Create a new prompt sample"
- "Create an agent instruction"
- "Create a new skill sample"

You can also copy a current sample of the same type and replace all
sample-specific content. Do not retain another contributor's identity, URLs,
tracking ID, or screenshots.

## Required sample quality

### Documentation

Every `README.md` must:

- explain the scenario, expected outcome, prerequisites, setup, and usage;
- identify known limitations and product or license assumptions;
- link to the primary source (`SKILL.md` for skills);
- include contributor attribution and current version history where applicable;
- include a representative image with meaningful alt text;
- include the standard as-is disclaimer and best-effort support language.

Use the exact uppercase filename `README.md`.

### Images

- Store contributed images in the sample's `assets` folder.
- New samples must include at least one sample-specific static PNG.
- Reference gallery images in `assets/sample.json`; the first image by
  ascending `order` is the primary card preview.
- Do not use externally hosted images, secrets, personal data, customer data,
  or tenant-specific information.
- Existing image-less legacy samples can use the shared fallback, but new
  contributions cannot.

### Metadata

`assets/sample.json` must contain one complete record. Keep titles,
descriptions, products, authors, dates, source URLs, download URLs, thumbnails,
and alt text accurate.

The `name` must use the taxonomy-aware identity for the sample type:

- Prompt: `copilotprompts-prompt-{folder-name}`
- Agent instruction: `copilotprompts-agent-{folder-name}`
- Skill: `copilotprompts-skill-{folder-name}`

When updating an existing sample, update `updateDateTime` and its documented
version history.

### README view tracker

The final nonblank line of every sample `README.md` must contain exactly one
tracker matching the `sample.json` identity:

```markdown
![](https://m365-visitor-stats.azurewebsites.net/copilot-prompts/{sample-identity})
```

Pull request validation rejects missing or duplicate trackers, stale
repository prefixes, folder-name mismatches, metadata identity mismatches, and
content placed after the tracker.

## Skill-specific requirements

A skill is a reusable instruction package read by GitHub Copilot. `SKILL.md`
must include:

1. YAML frontmatter with a kebab-case `name` matching the folder and a precise
   trigger-focused `description`;
2. required inputs and what Copilot must ask before starting;
3. a clear output structure;
4. atomic, ordered execution steps;
5. non-negotiable rules and validation checks;
6. at least one worked example when practical.

Skill metadata must use `["GitHub Copilot"]` for `products`. Test multiple
trigger phrasings and verify the skill asks for missing input instead of
guessing.

## Validate your contribution

From `site/`, install dependencies and run the same primary checks used in CI:

```powershell
npm ci
npm run validate:readme-trackers
npm run build
npm run test:e2e
```

The build validates metadata ingestion, safe README rendering, local images,
generated routes, and internal links. Browser tests cover catalog behavior,
responsive layouts, themes, tracking images, and accessibility.

## Submit a pull request

1. Fork the repository and create a branch from the latest `main`.
2. Add and validate one focused contribution.
3. Commit with a descriptive message.
4. Push the branch and open a pull request against `pnp/copilot-prompts:main`.
5. Complete the pull request checklist and respond to review feedback.

Most contributions require the
[Microsoft Contributor License Agreement](https://cla.opensource.microsoft.com/).
The CLA bot will guide you; it is normally required only once.

Do not delete your contribution branch until the pull request is closed.

## Getting help

If the process is unfamiliar, join a free
[Sharing is Caring](https://pnp.github.io/sharing-is-caring/) community session.
For repository-specific contribution questions, use the issue forms. General
Microsoft Copilot product questions belong in official Microsoft support and
product-community channels.

Thank you for contributing.

> Sharing is caring.

![](https://m365-visitor-stats.azurewebsites.net/copilot-prompts/CONTRIBUTING.md)

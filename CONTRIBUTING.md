# Contribution Guidance

If you'd like to contribute to this repository, please read the following guidelines. Contributors are more than welcome to share their learnings with others in this centralized location.

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information, see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

Remember that this repository is maintained by community members who volunteer their time to help. Be courteous and patient.

## Question or Problem?

Please do not open GitHub issues for general support questions as the GitHub list should be used for feature requests and bug reports. This way we can more easily track actual issues or bugs from the code and keep the general discussion separate from the actual code.

## Typos, Issues, Bugs and contributions

Whenever you are submitting any changes to repositories in the PnP organization, please follow these recommendations.

* Always fork the repository to your own account before making your modifications
* Do not combine multiple changes to one pull request. For example, submit any samples and documentation updates using separate PRs
* If your pull request shows merge conflicts, make sure to update your local main to be a mirror of what's in the main repo before making your modifications
* If you are submitting multiple samples, please create a specific PR for each of them
* If you are submitting typo or documentation fix, you can combine modifications to single PR where suitable

## Sample Naming and Structure Guidelines

When you submit a new sample, please follow these guidelines:

* Each sample must be placed in a folder under the `samples` folder
* Your sample folder must include the following content:
  * Your solution's source code
  * An `assets` folder, containing screenshots
  * A `README.md` file
* You must only submit samples for which you have the rights to share. Make sure that you asked for permission from your employer and/or clients before committing the code to an open-source repository, because once you submit a pull request, the information is public and _cannot be removed_.

This repository accepts three types of contributions:

| Type | Location | Core file | Description |
|------|----------|-----------|-------------|
| **Prompt samples** | `samples/{folder-name}/` | `README.md` | A prompt for Microsoft 365 Copilot, GitHub Copilot, or Microsoft Copilot |
| **Agent instructions** | `samples/agent-instructions/{agent-name}/` | `readme.md` | System prompt / instructions for a Copilot Studio agent |
| **Skill samples** | `samples/skills/{skill-name}/` | `SKILL.md` + `README.md` | A reusable instruction file that teaches GitHub Copilot a multi-step task |

### Sample Folder

* When submitting a new sample solution, please name the sample solution folder accordingly
* Do not use period/dot in the folder name of the provided sample

### README.md

* You will need to have a `README.md` file for your contribution, which is based on [the provided template](template/README-template.md) under the `samples` folder. Please copy this template to your project and update it accordingly. Your `README.md` must be named exactly `README.md` -- with capital letters -- as this is the information we use to make your sample public.
* You will need to have a screenshot picture of your sample in action in the `README.md` file ("pics or it didn't happen"). The preview image must be located in the `assets` folder in the root of your sample folder.
  * All screen shots must be located in the `assets` folder. Do not point to your own repository or any other external source
* The README template contains a specific tracking image at the end of the file with an `img` element pointing to `https://m365-visitor-stats.azurewebsites.net/SamplesGallery/pnp-copilot-prompt-your-sample`. This is a transparent image which is used to track how many visits each sample receives in GitHub.
* Update the image `src` attribute according with the repository name and folder information. For example, if your sample is named `my-prompt` in the `samples` folder, you should update the `src` attribute to `https://m365-visitor-stats.azurewebsites.net/SamplesGallery/pnp-copilot-prompt-my-prompt`
  * Update the image `src` attribute according with the repository name and folder information.
* If you find an existing sample which is similar to yours, please extend the existing one rather than submitting a new similar sample
  * When you update existing samples, please update also `README.md` file accordingly with information on provided changes and with your author details
* Make sure to document each function in the `README.md`
* If you include your social media information under **Authors** in the **Solution** section, we'll use this information to promote your contribution on social media, blog posts, and community calls.
    * Try to use the following syntax:
    ```md
    folder name | Author Name ([@yourtwitterhandle](https://twitter.com/yourtwitterhandle))
    ```
* If you include your company name after your name, we'll try to include your company name in blog posts and community calls.
    * Try to use the following syntax:
    ```md
    folder name | Author Name ([@yourtwitterhandle](https://twitter.com/yourtwitterhandle)), Company Name
    ```
* For multiple authors, please provide one line per author
* If you prefer to not use social media or disclose your name, we'll still accept your sample, but we'll assume that you don't want us to promote your contribution on social media.

### Assets

* To help people understand your sample, make sure to always include at least one screenshot of your solution in action. People are more likely to click on a sample if they can preview it before installing it.
* Please provide a high-quality screenshot
* If possible, use a resolution of **1920x1080**
* You can add as many screen shots as you'd like to help users understand your sample without having to download it and install it.
* You can include animated images (such as `.gif` files), but you must provide at least one static `.png` file

---

## Skill Sample Guidelines

Skill samples are **GitHub Copilot custom skills** — reusable `SKILL.md` instruction files that teach GitHub Copilot how to perform specific, repeatable tasks. They are a new contribution type alongside prompts and agent instructions.

### What Is a Skill?

A skill is a Markdown file with YAML frontmatter that GitHub Copilot reads at runtime. When a user's request matches the skill's description, Copilot follows the instructions in the file to complete a multi-step task — gathering inputs, generating outputs, and validating results.

### Folder Structure

Skill samples live in `samples/skills/{skill-name}/`:

```
samples/skills/{skill-name}/
├── SKILL.md                  # The skill definition (core contribution)
├── README.md                 # Documentation and usage instructions
├── assets/
│   └── sample.json           # Metadata for the Solution Gallery
```

### Naming Rules

* Use **lowercase and hyphens only** (e.g., `code-review-csharp`, `api-docs-generator`)
* Do **NOT** use periods/dots in the folder name
* Keep names concise — **2–5 words** that describe the task
* Do **NOT** use app-host prefixes like `m365-` or `github-`

### SKILL.md Schema

The `SKILL.md` file must follow the schema defined in [SKILL-SCHEMA.md](./SKILL-SCHEMA.md). At minimum, it must include:

1. **YAML frontmatter** with `name` (kebab-case, must match folder name) and `description` (trigger phrases)
2. **Title** — top-level heading
3. **Before Starting** — inputs the skill needs from the user
4. **Output Structure** — what the skill produces
5. **Step-by-step instructions** — `## Step N: <Action>` sections
6. **Rules** — non-negotiable constraints
7. **Examples** (recommended) — at least one worked input → output example
8. **Validation Checklist** (recommended) — self-verification checks

### README.md for Skills

The README should:

* Explain what the skill does and why it's useful
* Link to the `SKILL.md` file as the core contribution
* List **trigger phrases** the user can say to activate the skill
* Include **installation instructions** (copy `SKILL.md` to `.github/skills/{skill-name}/`)
* List prerequisites (always includes GitHub Copilot and VS Code)
* Include the standard Help and Disclaimer sections

### sample.json for Skills

The metadata file follows the same format as other samples, with these specifics:

* `products` must be `["GitHub Copilot"]`
* `url` must point to `samples/skills/{skill-name}`
* `name` must follow the pattern `copilotprompts-{skill-name}`

### Scaffolding with GitHub Copilot

You can scaffold a new skill sample automatically! Open GitHub Copilot Chat in VS Code and say:

* *"Create a new skill sample"*
* *"Scaffold a new skill"*
* *"Contribute a skill"*

### Best Practices for Writing Skills

1. **Be specific in the description** — include exact trigger phrases users might say
2. **Ask before assuming** — define required inputs and instruct Copilot to ask for missing ones
3. **Show, don't just tell** — include at least one worked example
4. **Keep steps atomic** — one action per step; 3–7 steps is ideal
5. **Define hard rules** — prevent common mistakes explicitly
6. **Test your skill** — try triggering it with different phrasings before submitting
7. **One skill = one task** — if it does two unrelated things, split it into two skills

---

## Submitting Pull Requests

> If you aren't familiar with how to contribute to open-source repositories using GitHub, or if you find the instructions on this page confusing, [sign up](https://forms.office.com/Pages/ResponsePage.aspx?id=KtIy2vgLW0SOgZbwvQuRaXDXyCl9DkBHq4A2OG7uLpdUREZVRDVYUUJLT1VNRDM4SjhGMlpUNzBORy4u) for one of our [Sharing is Caring](https://pnp.github.io/sharing-is-caring/#pnp-sic-events) events. It's completely free, and we'll guide you through the process.

Here's a high-level process for submitting new samples or updates to existing ones.

1. Sign the Contributor License Agreement (see below)
2. Fork this repository [pnp/copilot-prompts](https://github.com/pnp/copilot-prompts) to your GitHub account
3. Create a new branch from the `main` branch for your fork for the contribution
4. Include your changes to your branch
5. Commit your changes using descriptive commit message. These are used to track changes on the repositories for monthly communications
6. Create a pull request in your own fork and target the `main` branch
7. Fill up the provided PR template with the requested details

Before you submit your pull request consider the following guidelines:

* Search [GitHub](https://github.com/pnp/copilot-prompts/pulls) for an open or closed Pull Request which relates to your submission. You don't want to duplicate effort.
* Make sure you have a link in your local cloned fork to the [pnp/copilot-prompts](https://github.com/pnp/copilot-prompts):

  ```shell
  # check if you have a remote pointing to the Microsoft repo:
  git remote -v

  # if you see a pair of remotes (fetch & pull) that point to https://github.com/pnp/copilot-prompts, you're ok... otherwise you need to add one

  # add a new remote named "upstream" and point to the Microsoft repo
  git remote add upstream https://github.com/pnp/copilot-prompts.git
  ```

* Make your changes in a new git branch:

  ```shell
  git checkout -b my-prompt main
  ```

* Ensure your fork is updated and not behind the upstream **copilot-prompts** repo. Refer to these resources for more information on syncing your repo:
  * [GitHub Help: Syncing a Fork](https://help.github.com/articles/syncing-a-fork/)
  * [Keep Your Forked Git Repo Updated with Changes from the Original Upstream Repo](http://www.andrewconnell.com/blog/keep-your-forked-git-repo-updated-with-changes-from-the-original-upstream-repo)
  * For a quick cheat sheet:

    ```shell
    # assuming you are in the folder of your locally cloned fork....
    git checkout main

    # assuming you have a remote named `upstream` pointing official **copilot-prompts** repo
    git fetch upstream

    # update your local main to be a mirror of what's in the main repo
    git pull --rebase upstream main

    # switch to your branch where you are working, say "my-prompt"
    git checkout my-prompt

    # update your branch to update it's fork point to the current tip of main & put your changes on top of it
    git rebase main
    ```

* Push your branch to GitHub:

  ```shell
  git push origin my-prompt
  ```

## Merging your Existing GitHub Projects with this Repository

If the sample you wish to contribute is stored in your own GitHub repository, you can use the following steps to merge it with this repository:

* Fork the `copilot-prompts` repository from GitHub
* Create a local git repository

    ```shell
    md copilot-prompts
    cd copilot-prompts
    git init
    ```

* Pull your forked copy of `copilot-prompts` into your local repository

    ```shell
    git remote add origin https://github.com/yourgitaccount/copilot-prompts.git
    git pull origin main
    ```

* Pull your other project from GitHub into the `samples` folder of your local copy of `copilot-prompts`

    ```shell
    git subtree add --prefix=samples/projectname https://github.com/yourgitaccount/projectname.git main
    ```

* Push the changes up to your forked repository

    ```shell
    git push origin main
    ```

## Signing the CLA

Before we can accept your pull requests you will be asked to sign electronically Contributor License Agreement (CLA), which is a pre-requisite for any contributions all PnP repositories. This will be one-time process, so for any future contributions you will not be asked to re-sign anything. After the CLA has been signed, our PnP core team members will have a look at your submission for a final verification of the submission. Please do not delete your development branch until the submission has been closed.

You can find Microsoft CLA from the following address - [https://cla.microsoft.com](https://cla.microsoft.com/).

Thank you for your contribution.

> Sharing is caring.

![](https://m365-visitor-stats.azurewebsites.net/copilot-prompts/CONTRIBUTING.md)

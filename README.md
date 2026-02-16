# Copilot prompts

This repository contains examples of prompts for Microsoft Copilot.

> We welcome community contributions to the `samples` folder in this repository for demonstrating different prompts for Microsoft Copilot. If you have a great sample prompt for Microsoft Copilot, GitHub Copilot or Microsoft Copilot for Microsoft 365, please share your work and help others!

> **Disclaimer:** The sample prompts provided in this repository are for demonstration purposes. They may not always be accurate or suitable for your specific use case. Please use them at your own discretion and review and modify them as necessary.By using the prompts in this repository, you acknowledge these limitations and agree to use the content responsibly. The authors of this repository or the prompts are not liable for any inaccuracies or issues that arise from the use of these prompts.
**Disclaimer: Use of GitHub Avatars for Recognition Posts**
By contributing to this open-source project, you grant us permission to use your GitHub avatar in our “Prompt of the Week Kudos” posts on LinkedIn, celebrating your contributions. If you prefer to use a different photo or opt out entirely, please open an issue in the repository or contact us directly. We’re happy to accommodate your preferences.

## Have an idea, issues or questions?

If you've got an idea or questions or experience an issue with any of the samples in this repo, please [create an issue](https://github.com/pnp/copilot-prompts/issues/new).

## Authors

This repository's contributors are all community members who volunteered their time to share code samples.

## How to use this repo

Simply go to the [samples](https://github.com/pnp/copilot-prompts/tree/main/samples) folder and select one sample (see steps 1-3) in the figure below. Then find the instructions in the readme.md file to run the prompt yourself. Be sure to checkout the prerequisites before you get started.

![how to use this repo image](./images/how-to.png)

## Contributions

Samples in this repository are submitted by Microsoft’s product groups, and the [Microsoft 365 and Power Platform community](http://aka.ms/m365pnp). We welcome your feedback and suggestions for new samples. We also welcome community contributions. If you have any questions, just let us know.

Please have a look on our [Contribution Guidance](./CONTRIBUTING.md) before submitting your pull requests, so that we can get your contribution processed as fast as possible. Create a pull request from your forked repo’s new branch to the upstream repository’s main branch so your prompts can be reviewed and approved by the one of the community folks in their free time.

This repository has two types of prompt samples:

| Type | Location | What it is |
|------|----------|------------|
| **Prompt samples** | `samples/{folder-name}/` | A prompt you use directly in Microsoft 365 Copilot, GitHub Copilot, or Microsoft Copilot |
| **Agent instruction samples** | `samples/agent-instructions/{agent-name}/` | A system prompt / agent instructions you paste into Copilot Studio to create an agent |

Both types follow the same basic structure: a `README.md` (or `readme.md`) file and an `assets/` folder containing a `sample.json` metadata file.

You can contribute in two ways — **traditionally** (manually creating files) or using **GitHub Copilot** to scaffold everything for you.

---

### Option 1: Contribute using GitHub Copilot (recommended)

If you have GitHub Copilot in VS Code, you can use the built-in skills to scaffold your sample automatically with the correct folder structure, README, and sample.json.

#### For prompt samples

Open GitHub Copilot Chat and say one of the following:

- *"Create a new prompt sample"*
- *"Add a new prompt sample"*
- *"Scaffold a new prompt sample"*

GitHub Copilot will ask you for details (title, prompt text, target product, author info) and create the folder under `samples/` with all required files.

#### For agent instruction / system prompt samples

Open GitHub Copilot Chat and say one of the following:

- *"Create an agent instruction"*
- *"Create a system prompt sample"*
- *"Scaffold an agent sample"*
- *"Build an agent"*

GitHub Copilot will ask you for details (agent name, system prompt, use case category, author info) and create the folder under `samples/agent-instructions/` with all required files.

> **Note:** After scaffolding, remember to add a screenshot to the `assets/` folder and update the `sample.json` thumbnails if applicable.

---

### Option 2: Contribute traditionally

Your insights can help the community thrive. If you have prompts that can benefit others or if you have figured out a hack, here’s how to share them:

#### Fork the repository
Go to the repository https://aka.ms/copilot-prompt-library, select the Fork button to create your own copy.

#### Create a new branch
Clone your forked repository and create a new branch with a unique name that reflects your prompt’s purpose.

#### Add a new folder

**For prompt samples:** Inside the `samples` folder, create a new folder following the naming convention: `<apphost-functionality-prompt>`. For example, if you’re creating a prompt for a PowerPoint sales report, name it `ppt-sales-report-prompt`.

**For agent instruction samples:** Inside `samples/agent-instructions`, create a new folder with a descriptive name for your agent (e.g., `communication-assistant`, `smart-crop-doctor`).

#### Prepare the readme file
Find an existing `readme.md` file in any sample folder of the same type.

Copy it into the new folder you created in the step above and update the contents in the file to describe your prompt or agent instructions.

For agent instruction samples, the key section is **Instruction** — place your full system prompt inside a fenced code block.

#### Create an assets folder
Within your new folder, add a subfolder named `assets`. This is where you’ll store any images or GIF files that your readme file refers to.

#### Copy the sample JSON file
Locate the `sample.json` file in any existing sample’s `assets` folder. Copy this file into your own `assets` folder.

> Each of the samples in this repository will be shown in the [M365 Solution Gallery page](https://adoption.microsoft.com/en-us/sample-solution-gallery/) for better discovery and use. The `sample.json` file is what helps feed the solution gallery website with the metadata of a sample.

#### Update the JSON file
Modify the `sample.json` file in your `assets` folder to match the details of your prompt or agent.

---

And that’s it! You’re now ready to contribute your creative prompts to the repository.

## Resources
- [https://aka.ms/Copilot-For-M365](https://aka.ms/Copilot-For-M365
)
- [Copilot Lab](https://copilot.cloud.microsoft/prompts)



## Code of Conduct

This repository has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

> Sharing is caring!

![](https://m365-visitor-stats.azurewebsites.net/copilot-prompts/README.md)

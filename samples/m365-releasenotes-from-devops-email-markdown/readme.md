# Generate release notes from DevOps emails

## Summary

## Prompt💡

Please generate release notes in Markdown format by using the following email content as source /REFERENCE YOUR EMAIL HERE. You should list Features as H2 in markdown format just using the content of the Title column, then the items that follow to each Feature that are Product Backlog Items should be listed just using the content from the Title, without any modification, one in each line. Items after a Feature that are of the type Bug should be listed just using the ID followed by a space and the Title without any modification to the source content (that is including symbols like : or - and capitalized words). Ignore items with a repeated title even if different type. Ignore data in the columns Assigned To, State and Tags.

### Descriptionℹ️

[English](./en-us/prompt.md)

## Contributors 👨‍💻

[Guillermo Bas](https://github.com/GuillermoBas)

## Version history

Version|Date|Comments
-------|----|--------
1.0|June 11, 2024|Initial release

## Instructions 📝

1. Create your Release Notes query in your Azure DevOps project, type of query "Tree of work items" ensuring the parent/children relationship between Features and PBIs or Bugs is well represented, must include at least the following three columns "ID", "Work Item Type" and "Title"
2. Email the query to yourself by using the "Email query" button from the Query editor
3. Make sure you have Copilot for Microsoft 365 in your tenant
4. Open the Microsoft Teams app
5. Open the Copilot app within Teams
6. Paste the prompt in the Copilot app
7. Edit the /REFERENCE YOUR EMAIL HERE part and type / to search for the desired email to be used as source

## Improvise Usage 🚀
Suggest asking copilot to list emails you haven't replied to or from a certain period of time.

## Prerequisites

* [Copilot for Microsoft 365](https://developer.microsoft.com/microsoft-365/dev-program)
* [Azure DevOps](https://dev.azure.com/)

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for  community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20YOUR-SAMPLE-NAME%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-m365-releasenotes-from-devops-email-markdown)

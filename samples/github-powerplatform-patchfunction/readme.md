# Create a Patch Function to Create a new record in Powerapps using Github Copilot

![GitHub Copilot interface in Visual Studio Code showing an extended prompt. The prompt asks: 'Can you write PowerFx code to create a new record in PowerApps? I need to add a new record to a data source named EmployeeData. The new record should include fields for Name, Position, and HireDate, and these values will be entered through text input controls (TextInput_Name, TextInput_Position) and a date picker (DatePicker_HireDate).' Options for interacting with the Copilot suggestion, like accept, discard, and further actions, are visible on the right.](/samples/github-powerplatform-patchfunction/assets/Copilot%20Patch%20Function.png)

## Summary

This prompt asks GitHub Copilot to generate PowerFx code that creates a new record in a PowerApps data source called EmployeeData. The record will include fields for Name, Position, and HireDate, with values provided by user input through text input controls and a date picker. The formula should be triggered by a button click, with validation to ensure all fields are filled. If validation fails, an error notification will be displayed; otherwise, a success message will confirm the record creation.

## Prompt💡

Can you write PowerFx code to create a new record in PowerApps? I need to add a new record to a data source named `EmployeeData`. The new record should include fields for `Name`, `Position`, and `HireDate`, and these values will be entered through text input controls (`TextInput_Name`, `TextInput_Position`) and a date picker (`DatePicker_HireDate`). The formula should trigger when a button is clicked, and it should validate that all fields are filled before creating the record. If any field is empty, display an error notification. If all fields are valid, display a success notification after the new record is added.

### Description ℹ️

The Patch function in Power Fx allows you to add new data to a data source without affecting the rest of the data. 

## Contributors 👨‍💻

[Gavin Warner](https://github.com/GavinWarner05)

## Version history

Version|Date|Comments
-------|----|--------
1.0|October 03, 2024|Initial release

## Instructions 📝

### Install Github Copilot Extension
1. Open Visual Studio Code.
2. Go to the Extensions panel(you can open it by clicking on the Extensions icon on the left toolbar or pressing Ctrl+Shift+X).
3. Search for "Github Copilot" and install the extension.

### Sign in to GitHub
1. Once the extension is installed, you will need to sign in with your GitHub account.
2. After installation, Visual Studio Code will prompt you to authenticate. Follow the steps to sign in.

### Create File for Github Copilot Prompt
1. Click on **File** in the top menu and select **New File**.
(Alternatively, you can use the shortcut **Ctrl+N**(Windows) or **Cmd+N**(Mac) to create a new file.)
2. Name the file whatever you'd like.(Make sure to give the file the appropriate extension for the language e.g., **.txt**)
3. Start writing your prompt by pressing **Ctrl+i** and entering the desired prompt.

## Prerequisites

* [Copilot for Microsoft 365](https://developer.microsoft.com/microsoft-365/dev-program)
* [Microsoft Word](https://www.office.com/)

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for  community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20word-write-prompt-guidance-best-practices-prompt%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-m365-my-name-mentioned-prompt)

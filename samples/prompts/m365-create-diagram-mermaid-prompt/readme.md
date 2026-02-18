# 🚀 Create a digram from text in mermaid.js📆

![Demo of creating a digram from text in mermaid.js](./assets/demo.gif)

## Summary 📜

This prompt utilizes Copilot to take plain text input and organize it into a diagram using mermaid.js syntax. It provides a convenient way to visually represent information and improve readability. By leveraging Copilot's capabilities, users can easily generate complex diagrams from simple text descriptions.

## Prompt 💡

### first prompt
You're Working with the business to define a business process or a workflow for a content review and approval process, The type of content is what's considered controlled content which needs. You and high degree of scrutiny so that when people are using it they're not using incorrect information which could cause problems downstream the broadly the process is described as the following. Content has a next review date and a last review date and a review. The review. When the next review date is to be set following the previous review an approval at the time of the next review date the process sends a review notification to the person within the department that owns the content or is considered the custodian of the content this person conducts their review and approval if they reject it the flow Updates the items status as review incomplete and leaves the next review date as its was, And the flow ends if it's approved A second review notification is sent to the head of the business area to get their review and approval if they reject then the person who did the first review and approval is sent a notification with the comments from the 2nd review approver, if the second person approves the content then the item is marked as approved the next review date is recalculated based on the review. And updated and a notification is sent to the quality assurance contact with the department.

Using the above information organize this into A set of steps that can be used to describe the content review and approval process.

### second prompt

Using the steps to find in the previous response prepare the process using the syntax for our mermaid.js diagram

## Description ℹ️

This prompt utilizes Copilot to take plain text input and organize it into a diagram using mermaid.js syntax. It provides a convenient way to visually represent information and improve readability. By leveraging Copilot's capabilities, users can easily generate complex diagrams from simple text descriptions.
This is multi turn so make sure you send the first prompt to Copilot, wait for response and then send the second response

## Contributors 👨‍💻

[Andrew Jolly](https://www.linkedin.com/in/andrewjolly/)

## Version history 📋

Version|Date|Comments
-------|----|--------
1.0|June 20, 2024|Initial release

## Instructions 📝


1. Go to Copilot app in Teams/Bing
2. Copy paste the first prompt
3. Wait for reponse to first prompt
4. Copy past the second prompt
5. Copy the response in the format needed to create the diagram
6. Go to [https://mermaid.live](https://mermaid.live)and paste the code to generate diagram

### Improvise Usage 🚀

You can add more text to make the process more complex.


## Help 💁

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for  community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20YOUR-SAMPLE-NAME%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-m365-create-diagram-mermaid-prompt)

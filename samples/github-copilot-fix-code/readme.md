# Fixing your code using GitHub copilot

![Screenshot of the prompt in use](./assets/prompt.png)

## Summary

## Prompt 💡
Can you please help me fix my code? I'm trying to accomplish 'blank' using 'blank' (insert your technology here).
The code I'm using is crea8_attachment is not equal to null.
Please highlight what I'm not doing correctly, and provide tips how I can improve in the future. 

### Description ℹ️

It might sound straight forward, but this is such a helpful prompt. 

For example, I wanted to set up a trigger condition, but couldn't remember the exact syntax.
I asked it to check my code; 
```powerfx
triggerOutputs()?['body/crea8_attachment'] is not equal to null
```
 and it helped me with: 

```powerfx
@equals(triggerOutputs()?['body/HasAttachments'], true)
```
It guided me through the syntax, gave me multiple scenarios and gave tips how I could approach this next time.

## Contributors 👨‍💻

[Nathalie Leenders](https://github.com/nathalie-leenders)

## Version history

Version|Date|Comments
-------|----|--------
1.0|September 16, 2025|Initial release

## Instructions 📝

1. Make sure you have GitHub Copilot extension installed in VSCode and enable it
2. Create a .json file
3. Launch GitHub copilot chat "command"+ i or "ctrl" +i
4. Copy the above prompt and paste and select `Enter`
5. Check your output and select the suggestion you need, copy into your designated area.

### Improvise Usage 🚀
You can change the prompt to fit your business purpose, or explain other things alongside 'fixing' your code. Sometimes it will grab info from an .md file you have open, or from an older chat, try /clear if that happens.

## Prerequisites

* [GitHub copilot](https://copilot.github.com/)

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for  community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20github-copilot-fix-code%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-github-copilot-fix-code)


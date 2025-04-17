# 🌐 Multilanguage Quiz in Microsoft Forms 📝

![Demo](./assets/Demo_Copilot_Forms_Quiz_Multilingual.gif)

## Summary

This guide provides a structured approach to creating multilingual quizzes in Microsoft Forms. Since Microsoft Forms does not natively support multiple languages within a single quiz, each question and answer must be manually entered in all required languages. To simplify this process, the guide offers a ready-to-use prompt and clear instructions to help you build consistent, professional, and accessible multilingual quizzes with minimal effort.

## Prompt 💡

Create a multilingual quiz in Microsoft Forms based on the parameters below:

- **Title**: Include all language versions separated by [separator].  
- **Description**: Use [separator] as a language divider.  
- **Questions**: Write the main question in the first language; provide translations in the subtitle, separated by [separator].  
- **Answers**: Provide each answer option in all selected languages, separated by [separator]. If an answer is universal (e.g., numbers, mathematical or scientific formulas, units of measurement, symbols and special characters, proper nouns, chemical elements or symbols, common acronyms or initialisms, dates or years), include it only once without translation.  
- **Explanations**: For each correct answer, include a short explanation in all languages, separated by [separator].

### Parameters:

- **Topic**:  
- **Languages**: English, Polish  
- **Number of questions**: 3  
- **Difficulty**: simple  
- **Quiz type**: Choose what suits you best for this topic  
- **Separator**: 🌐  

## Instructions 📝

1. **Create a New Form**  
   - Visit [Microsoft Forms](https://forms.office.com/).  
   - Click **"New Quiz"** to create a quiz.  
   - Open the Copilot panel and enter the above prompt, adjusting parameters as needed.  
   - Submit the prompt. If satisfied with the result, click **"Keep it"** to continue modifying the quiz manually if needed.

## Possible Options to Experiment With

- **Topics**: History, mathematics, geography, etc.  
- **Multiple Languages**: Try different combinations to reach a broader audience.  
- **Difficulty Levels**: Simple, advanced, expert.  
- **Quiz Types**: Multiselect, single choice, text input, or let Copilot decide by adding "choose the best option you think suits the quiz."

## Contributors 👨‍💻

- [Michał Ziemba](https://github.com/Michal-Ziemba)

## Version History

| Version | Date        | Comments       |
|---------|-------------|----------------|
| 1.0     | Apr 17, 2025 | Initial release |

## Prerequisites

- [A Microsoft 365 license with access to Microsoft Forms](https://learn.microsoft.com/en-us/office365/servicedescriptions/microsoft-forms-service-description)  
- Microsoft Copilot license  

## Help

We do not officially support samples, but the community is always willing to help and improve them. We use GitHub Issues for tracking:

- Check if your issue has already been reported: [Open Issues](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20YOUR-SAMPLE-NAME%22)  
- Report a new issue or bug: [New Issue](https://github.com/pnp/copilot-prompts/issues/new)  
- Suggest an improvement or enhancement: [Submit an Idea](https://github.com/pnp/copilot-prompts/issues/new)

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

[Visitor Stats](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-m365-multilanguage-quiz)

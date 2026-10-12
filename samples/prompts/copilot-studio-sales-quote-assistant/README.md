# Sales Quote Assistant

## Description

This Copilot Studio prompt creates a guided quote-building agent for sales representatives. The agent collects customer and rep information, allows iterative product line addition with quantity and discount selection, calculates line totals and overall totals, presents a full summary for review, generates a quote reference number, and offers immediate email delivery or draft saving.

The **iterative loop pattern** (add product â†’ add another?) makes this the most complex conversational flow in the repository. It mirrors how sales reps actually work â€” building a quote line by line â€” rather than forcing all input upfront in a single form.

The direct ROI comes from speed: a guided conversational quote takes less than 2 minutes, eliminates data entry errors, and ensures every quote is recorded in the CRM automatically.

## Prompt

> Create an agent that helps sales reps build product quotes conversationally. Collect customer and rep names, then loop through product additions (product from list, quantity, discount: 5%/10%/15%/none). Display a line-item summary with totals. Confirm and generate a reference number. Offer immediate email to customer or save as draft.

### Supported Language(s)

- [English - US](./en-us/prompt.md)

## Authors

Solution|Author(s)
--------|---------
Sales Quote Assistant | [OwnOptic](https://github.com/OwnOptic) ([@OwnOptic](https://twitter.com/OwnOptic))

## Minimal Path to Awesome

1. Navigate to [Copilot Studio](https://copilotstudio.microsoft.com/) and click **Create a copilot**
2. Select **Create from description with Copilot**
3. Copy the content from [prompt.md](./en-us/prompt.md) and paste it as the description
4. Follow the setup wizard:
   - Name: `Sales Quote Assistant`
   - Tone: **Professional**
5. After generation, populate the product list choice values with your actual product catalog
6. Set unit prices per product in a Dataverse Products table used by the agent via a Power Automate connector
7. Connect the confirmation step to a Power Automate flow that:
   - Creates a Quote record in Dataverse or Dynamics 365 Sales
   - Generates a unique quote reference number
   - Optionally sends the quote as a formatted HTML email via Outlook
8. Publish to Microsoft Teams and add to the Sales team's channel

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-copilot-studio-sales-quote-assistant)

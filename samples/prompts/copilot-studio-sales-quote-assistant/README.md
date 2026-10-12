# Sales Quote Assistant

![Default sample preview](./assets/ilovecopilot.png)

## Summary

This Copilot Studio prompt creates a guided quote-building agent for sales representatives. The agent collects customer and sales representative information, supports adding product lines iteratively, calculates line and overall totals, presents the quote for review, generates a reference number, and offers immediate email delivery or draft saving.

The iterative loop pattern (add product → add another?) mirrors how sales representatives build quotes line by line instead of requiring all information in a single form.

## Prompt

```text
Create an agent that helps sales representatives build and send product quotes through a guided conversation. Start by asking for the customer's company name and the sales representative's name. Then allow the representative to add products to the quote one at a time: ask for the product name from a list, the quantity, and whether a discount applies (choosing from 5%, 10%, 15%, or No Discount). After each product, ask if they want to add another. Once all products are added, display a quote summary showing each line item with quantity, unit price, discount, and line total, plus the overall total. Ask the representative to confirm or edit the quote. If confirmed, generate a quote reference number, record the quote in the system, and ask if they want to send the quote by email to the customer immediately or save it as a draft.
```

## Description

This prompt helps sales teams create consistent product quotes through a guided conversation. It reduces repetitive data entry, validates the information needed for each line item, and provides a complete summary before the quote is recorded or sent.

The generated agent can be connected to Dataverse or Dynamics 365 Sales through Power Automate to retrieve product pricing, create quote records, generate reference numbers, and send formatted emails.

## Contributors

[OwnOptic](https://github.com/OwnOptic) ([@OwnOptic](https://twitter.com/OwnOptic))

## Version history

Version|Date|Comments
-------|----|--------
1.0|March 2, 2026|Initial release

## Instructions

1. Navigate to [Copilot Studio](https://copilotstudio.microsoft.com/) and select **Create**
2. Select **New agent**, then choose to configure the agent with a description
3. Copy the content from the **Prompt** section above and paste it as the description
4. Follow the setup experience and name the agent `Sales Quote Assistant`
5. Configure the agent to use a professional tone
6. Replace the example product choices with your product catalog
7. Store product prices in a Dataverse Products table and make them available to the agent through Power Automate
8. Connect the confirmation step to a Power Automate flow that:
   - Creates a Quote record in Dataverse or Dynamics 365 Sales
   - Generates a unique quote reference number
   - Optionally sends the quote as a formatted HTML email through Outlook
9. Test the complete quote workflow, then publish the agent to the channels used by your sales team

### Improvise Usage

- Add tax, shipping, currency, or region-specific pricing calculations
- Require manager approval when a discount exceeds a defined threshold
- Generate a PDF quote and save it to SharePoint
- Allow sales representatives to revise or remove line items before confirmation

## Prerequisites

- Access to [Microsoft Copilot Studio](https://copilotstudio.microsoft.com/)
- A product catalog with current unit prices
- Dataverse or Dynamics 365 Sales for quote storage
- Power Automate for CRM and email integration

## Help

We do not provide support for samples, but the community is available to help improve them. GitHub issues are used to report problems and suggest enhancements.

You can review [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20copilot-studio-sales-quote-assistant%22) to see whether anyone else has reported the same problem.

If you encounter an issue, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

If you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

---
![](https://m365-visitor-stats.azurewebsites.net/copilot-prompts/copilotprompts-prompt-copilot-studio-sales-quote-assistant)

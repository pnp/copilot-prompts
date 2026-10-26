# IT Helpdesk Triage Agent

![Default sample preview](./assets/ilovecopilot.png)

## Summary

This Copilot Studio prompt creates an IT helpdesk agent that guides employees through self-service troubleshooting before escalating to the support team. The agent collects the device type and issue category, then walks the user through three targeted troubleshooting steps. If the issue remains unresolved, it collects the employee's details and generates a support ticket summary.

The design follows a **progressive triage pattern**: try self-service first, collect structured data only when escalation is needed. This reduces ticket volume while ensuring unresolved issues are captured with enough context for the IT team to act efficiently.

## Prompt

```text
Create an agent that helps employees troubleshoot common IT issues. Start by asking what type of device they are using, choosing from: Laptop, Desktop, Mobile Phone, or Tablet. Then ask them to select their issue from a list: Cannot connect to WiFi, VPN not working, Password reset needed, Printer not found, Software installation request, or Other. Based on their selection, guide them through three troubleshooting steps specific to that issue and device combination. After each step, ask if the issue is resolved. If resolved, end the conversation with a satisfaction confirmation. If not resolved after all three steps, collect the employee's full name and employee ID, create a support ticket summary, and confirm that the IT team will follow up within 4 business hours.
```

## Description

This prompt helps IT teams provide consistent first-line troubleshooting while collecting employee details only when escalation is needed. The generated agent can be connected to ServiceNow, Dataverse, or a SharePoint list through Power Automate to create support tickets with the device type, issue category, attempted steps, and employee details.

Ticket creation and follow-up are not provided by the prompt alone. Configure and test the integration before publishing, and replace the four-business-hour commitment with your IT team's agreed service-level target.

## Contributors

[OwnOptic](https://github.com/OwnOptic) ([@OwnOptic](https://twitter.com/OwnOptic))

## Version history

Version|Date|Comments
-------|----|--------
1.1|October 26, 2026|Simplified sample structure, refreshed setup instructions, and clarified integration requirements
1.0|March 2, 2026|Initial release

## Instructions

1. Navigate to [Copilot Studio](https://copilotstudio.microsoft.com/) and click **Create a copilot**
2. Select **Create from description with Copilot**
3. Copy the text in the [Prompt section](#prompt) above and paste it as the description
4. Follow the Copilot Studio setup wizard:
   - When asked for a name, enter: `IT Helpdesk Assistant`
   - When asked for a website, skip or enter your internal IT portal URL
   - When asked for tone, select: **Professional**
5. Review the generated topics and verify the device type and issue category choice branches
6. Connect the ticket creation step to a Power Automate flow that creates a record in ServiceNow, Dataverse, or a SharePoint list
7. Publish and deploy to Microsoft Teams for employee access


### Improvise Usage

- Add links to approved internal knowledge-base articles
- Route tickets to the appropriate support team based on the issue category
- Include the ticket reference in the escalation confirmation
- Collect feedback after self-service resolution to improve troubleshooting guidance

## Prerequisites

- Access to [Microsoft Copilot Studio](https://copilotstudio.microsoft.com/) with licensing appropriate for your deployment
- Approved troubleshooting guidance and an agreed IT support service-level target
- ServiceNow, Dataverse, or a SharePoint list for ticket storage
- Permission to publish the agent to Microsoft Teams

## Help

We do not provide support for samples, but the community is available to help improve them. GitHub issues are used to report problems and suggest enhancements.

You can review [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20copilot-studio-it-helpdesk-triage-agent%22) to see whether anyone else has reported the same problem.

If you encounter an issue, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

If you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

---
![](https://m365-visitor-stats.azurewebsites.net/copilot-prompts/copilotprompts-prompt-copilot-studio-it-helpdesk-triage-agent)

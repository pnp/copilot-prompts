# IT Helpdesk Triage Agent

## Description

This Copilot Studio prompt creates an IT helpdesk agent that guides employees through self-service troubleshooting before escalating to the support team. The agent collects the device type and issue category, then walks the user through three targeted troubleshooting steps. If the issue remains unresolved, it collects the employee's details and generates a support ticket summary.

The design follows a **progressive triage pattern**: try self-service first, collect structured data only when escalation is needed. This reduces ticket volume while ensuring unresolved issues are captured with enough context for the IT team to act efficiently.

## Prompt

> Create an agent that helps employees troubleshoot common IT issues. Start by asking what type of device they are using, choosing from: Laptop, Desktop, Mobile Phone, or Tablet. Then ask them to select their issue from a list: Cannot connect to WiFi, VPN not working, Password reset needed, Printer not found, Software installation request, or Other. Based on their selection, guide them through three troubleshooting steps specific to that issue and device combination. After each step, ask if the issue is resolved. If resolved, end the conversation with a satisfaction confirmation. If not resolved after all three steps, collect the employee's full name and employee ID, create a support ticket summary, and confirm that the IT team will follow up within 4 business hours.

### Supported Language(s)

- [English - US](./en-us/prompt.md)

## Authors

Solution|Author(s)
--------|---------
IT Helpdesk Triage Agent | [OwnOptic](https://github.com/OwnOptic) ([@OwnOptic](https://twitter.com/OwnOptic))

## Minimal Path to Awesome

1. Navigate to [Copilot Studio](https://copilotstudio.microsoft.com/) and click **Create a copilot**
2. Select **Create from description with Copilot**
3. Copy the content from [prompt.md](./en-us/prompt.md) and paste it as the description
4. Follow the Copilot Studio setup wizard:
   - When asked for a name, enter: `IT Helpdesk Assistant`
   - When asked for a website, skip or enter your internal IT portal URL
   - When asked for tone, select: **Professional**
5. Review the generated topics and verify the device type and issue category choice branches
6. Connect the ticket creation step to a Power Automate flow that creates a record in ServiceNow, Dataverse, or a SharePoint list
7. Publish and deploy to Microsoft Teams for employee access

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-copilot-studio-it-helpdesk-triage-agent)

# Tenant Compliance & Security Summary Report for Microsoft 365



## Summary

This prompt can generate an audit-ready report template which you can use immediately—just paste in your actual policy data. Microsoft 365 Copilot will not able to query tenant configuration, such as:

Active Retention Policies
Active Sensitivity Labels
Active DLP Policies
Policy assignments to sites, Teams, OneDrive, or mailboxes

## Prompt 💡

You are a Microsoft 365 Compliance and Security specialist.
Generate a Compliance / Security Summary for our tenant, including:

1. All active retention policies applied to SharePoint sites, Teams, and OneDrive accounts.
2. All sensitivity labels applied across the tenant (SharePoint, Teams, Exchange).
3. All DLP policies currently enforced. 

For each policy, include:

- "Policy name"
- "Policy type (Retention / Sensitivity / DLP)"
- "Applied locations (Sites, Teams, OneDrive, Mailboxes)"
- "Users or groups included"

Identify and highlight any gaps, such as:

- "Sites, Teams, or users not covered by any policy"
- "Overlapping or conflicting policies"

Format the output in a structured table or summary report, with clear headings and recommendations for remediation or improvement.

Provide the report in readable, executive-friendly language, suitable for audit review or governance meetings.


## Contributors 👨‍💻

[Josiah Opiyo]([https://github.com/ojopiyo])

## Version history

Version|Date|Comments
-------|----|--------
1.0|Dec 18, 2025|Initial release

## Instructions 📝

1. Make sure you have Copilot for Microsoft 365 in your tenant
2. Open the Microsoft Teams app
3. Open the Copilot app within Teams
4. Paste the prompt in the Copilot app
5. Paste your actual data onto the report and finish


## Prerequisites

* [Copilot for Microsoft 365](https://developer.microsoft.com/microsoft-365/dev-program)

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for  community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20YOUR-SAMPLE-NAME%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**


![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-m365-tenant-compliance-and-security-summary-report)

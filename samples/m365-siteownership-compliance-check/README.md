# M365 Site Ownership Compliance Check


## Summary

The m365 Compliance & Security Summary provides a governance-focused assessment of the Microsoft 365 tenant, highlighting key compliance, security, and operational risks. The report reviews core tenant configurations and content ownership to identify areas where governance controls may be missing, misconfigured, or ineffective.

A primary focus of the report is Site Collection Ownership Validation, ensuring that all SharePoint Online and Teams-connected sites have appropriate, active internal owners assigned. Sites with missing owners, disabled accounts, or guest-only ownership are flagged as governance and support risks, as they can lead to unmanaged data, security exposure, and operational delays.

The report delivers a clear overview of tenant health through risk categorisation, summarised metrics, and targeted recommendations. It enables administrators and stakeholders to quickly identify high-risk areas, prioritise remediation actions, and strengthen long-term governance and compliance practices across Microsoft 365.


## Why It Matters

Effective governance and security within Microsoft 365 depend on clear ownership, accountability, and oversight. Site collections without valid, active internal owners present a significant risk, as there may be no responsible individual to manage access, respond to incidents, or ensure compliance with organisational policies.

Without proper ownership:
- Sensitive data may remain accessible to inappropriate users
- Security incidents and access requests can go unresolved
- Compliance obligations (e.g. data retention, audits, or regulatory requirements) may not be met
- Orphaned or abandoned sites increase the organisation’s attack surface
- IT and support teams face delays when remediation or decision-making is required

By proactively identifying and addressing ownership gaps and related governance risks, this report helps the organisation maintain control over its digital estate, reduce operational and security exposure, and ensure Microsoft 365 is managed in a sustainable, compliant, and auditable way



## Prompt 💡

You are a Microsoft 365 Compliance and Security specialist.

Generate a Compliance and Security Summary for our Microsoft 365 tenant. The summary should focus on governance, risk, and operational resilience, and include the following checks and insights:

- Site Collection Ownership Validation
    - Review all SharePoint Online site collections (including Teams-connected sites).
    - Identify sites that have:
        - No assigned owner
        - Owners with disabled accounts
        - Owners that are guest (external) users only
    - For each non-compliant site, provide:
        - Site URL and title
        - Current owner(s)
        - Owner account status and type
    - Assess the governance and support risk associated with missing or invalid ownership.

- Summary & Risk Assessment
    - Total number of site collections reviewed
    - Number of sites with valid ownership
    - Number of sites at governance risk
    - High-risk sites requiring immediate action


## Contributors 👨‍💻

[Josiah Opiyo](https://github.com/ojopiyo)

*Built with a focus on automation, governance, least privilege, and clean Microsoft 365 tenants—helping M365 admins gain visibility and reduce operational risk.*

## Version history

Version|Date|Comments
-------|----|--------
1.0|Dec 22, 2025|Initial release

## Instructions 📝

1. Make sure you have Copilot for Microsoft 365 in your tenant
2. Open the Microsoft Teams app
3. Open the Copilot app within Teams
4. Paste the prompt in the Copilot app


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

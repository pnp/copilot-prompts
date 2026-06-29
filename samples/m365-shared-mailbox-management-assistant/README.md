# 🚀 M365 Shared Mailbox Management Assistant 📅


## Summary

This prompt analyses a shared mailbox handled by multiple staff members to assess workload distribution, ownership clarity, SLA adherence, and response quality. It highlights risks such as duplicated responses, unassigned emails, and uneven workload, and recommends improvements for team efficiency and governance.

## Prompt💡

I need help managing the shared mailbox **[sharedMailboxName or email address]** which is handled by **four Admin staff**.

- Admin Team Members:
  - [AdminUser1]
  - [AdminUser2]
  - [AdminUser3]
  - [AdminUser4]

- Time Range to Analyze: **[e.g., last 7 / 14 / 30 days]**
- Business Hours: **[e.g., 9:00 AM–5:00 PM, timezone]**
- Response SLA: **[e.g., first response within 24 hours]**

Instructions:
- **"Review incoming emails in the shared mailbox during the selected period"**
- **"Identify and attribute handling activity to individual admins where possible"**
- **"Detect:"**
    - **"Unassigned or unanswered emails"**
    - **"Emails exceeding the response SLA"**
    - **"Conversations with multiple responders (duplicate effort risk)"**
    - **"Emails handled outside business hours (if relevant)"**
-**"Analyse workload distribution across the 4 admins"**
-**"Consider categories, flags, or rules used to signal ownership"**

Generate:
- **"A workload summary per admin (emails handled, average response time)"**
- **"A list of overdue or high-risk conversations"**
- **"Identification of bottlenecks or uneven distribution"**
- **"Suggested next actions to clear backlog and rebalance workload"**

Output Format:
- **Shared Mailbox Health Summary**
  - **"Total emails received: [number]"**
  - **"Responded within SLA: [percentage]"**
  - **"Overdue / unassigned: [number]"**

- **Workload Distribution**
  - **"[AdminUser1]: [emails handled] | Avg response: [time]"**
  - **"[AdminUser2]: [emails handled] | Avg response: [time]"**
  - **"[AdminUser3]: [emails handled] | Avg response: [time]"**
  - **"[AdminUser4]: [emails handled] | Avg response: [time]"**

Action Required

- **"[Email subject] – Received on [date] – Suggested owner/action"**

**Recommendations**
- **"Process or rule improvements"**
- **"Ownership or rota suggestions"**
- **"Category or tagging standardisation"**


## Contributors 👨‍💻

 [Josiah Opiyo](https://github.com/ojopiyo) 

 *Built with a focus on automation, governance, least privilege, and clean Microsoft 365 tenants—helping M365 admins gain visibility and reduce operational risk.*

## Version history

Version|Date|Comments
-------|----|--------
1.0|Jan 14, 2026|Initial release

## Instructions 📝

1. Make sure you have copilot for Microsoft 365 in your tenant
2. Go to Copilot app in Teams
3. Copy paste the above prompt
4. Replace the [meetingDuration], [externalTeamTimezone], [externalTeamWorkingHours], [currentUserTimezone], [meetingTitle], [meetingDate] with actual values in prompt, don't update values in Instructions section.


## Prerequisites

* [Microsoft 365 Copilot](https://developer.microsoft.com/microsoft-365/dev-program)

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for  community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20YOUR-SAMPLE-NAME%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-m365-meeting-summary-transcript)

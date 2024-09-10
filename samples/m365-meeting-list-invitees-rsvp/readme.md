# 🚀 List upcoming meeting with list of invitees along with RSVP Status 📆🟢🟠

![Demo of meeting list with invitees and rsvp](./assets/demo.png)

## Summary 📜

This is a prompt to list the upcoming meeting details along with invitees list, meeting initiator, and RSVP status. It will show the list of all the upcoming meetings in a tabular format with the Date, Time, Meeting Details, Initiator, List of invitees and RSVP Status. If there is any conflict in the schedule, it will show the meeting in bold.

> [!WARNING] 
> Copilot will not get another user's calendar information (as of now) and will hallucinate pls read this [post](https://www.linkedin.com/posts/mahmoudhamedhassan_microsoftcopilottips-modernworkplaceai-copilotformicrosoft365-activity-7154581557679210496-6jLG?lipi=urn%3Ali%3Apage%3Ad_flagship3_detail_base%3B6rXTR9lRSGiLpSCjT4RgNQ%3D%3D).
When you encounter these issues please give feedback using the dissatified button in Copilot (the thumbs down).

## Prompt 💡

Show me my meetings for this week in table. Table should contain following details. Date, Time, Meeting Details, Initiated by, List of invitees, RSVP Status.
If RSVP Status is NOT Responded, show 🟠. If RSVP Status is Accepted, show 🟢.

If there are conflicts in my calendar for any events, show those events in bold

## Description ℹ️

This is a prompt to list the upcoming meeting for this week along with invitees list, meeting initiator, and RSVP status. It will show the list of all the upcoming meetings in a tabular format with the Date, Time, Meeting Details, Initiator, List of invitees and RSVP Status. If there is any conflict in the schedule, it will show the meeting in bold.
If the RSVP status is not responded, it will show 🟠. If the RSVP status is accepted, it will show 🟢.

## Contributors 👨‍💻

[Arjun Menon](https://github.com/arjunumenon)

## Version history 📋

Version|Date|Comments
-------|----|--------
1.0|May 23, 2024|Initial release

## Instructions 📝

1. Make sure you have copilot for Microsoft 365 in your tenant
2. Go to Copilot app in Teams
3. Copy paste the above prompt
4. IF you want, you can also modify the prompt to show the list of meetings for next week or for a specific date range

### Improvise Usage 🚀

You can add more information to the prompt if needed to show details in the table. You can modify the meeting dates / range  in the prompt so that you can get the details of the meeting for the range which you are looking for. Currently, the prompt is showing the details of the meeting for the current week.

## Prerequisites 📦

* [Copilot for Microsoft 365](https://developer.microsoft.com/microsoft-365/dev-program)

## Help 💁

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for  community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20YOUR-SAMPLE-NAME%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-m365-meeting-action-items-prompt)

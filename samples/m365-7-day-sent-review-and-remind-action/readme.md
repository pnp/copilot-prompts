# 🚀 7-Day Sent Items and Remind Action 💻

Bored of tracking requests, questions, or tasks you sent by email and not sure whether anyone answered?

![Sample](https://github.com/ondrejvysek/copilot-prompts/blob/m365-7-day-sent-review-and-action/samples/m365-7-day-sent-review-and-remind-action/assets/sample1.png)

## Summary

This prompt is built for anyone who wants a fast, reliable way to review what they sent in the last 7 days and see what still needs a follow-up, and remind the recipient.

It scans **Sent Items only**, deduplicates **conversation threads**, checks whether there is a **reply after your latest sent message**, and produces a structured action list.

The output is split into:

- Immediate Action (threads where you @mentioned someone and asked for action)
- Action Required
- Other (everything else that was reviewed but did not require action)

Each section is divided into:
  - External (likely customers or partners)
  - Internal (people inside your org)

**Important:** This prompt is designed for **Microsoft 365 Copilot with GPT-5** to handle threading, reply detection, exclusions, and structured formatting.

## Prompt 💡

```
Task: Review my Sent Items for the past 7 days and prepare a prioritized action list in English showing whether I have received any responses to those sent messages.

Scope rules (apply exactly):
- Folder: Sent Items only (exclude subfolders, Archive, Junk/Spam, Deleted Items).
- Time window: past 7 days from now; show all times in my local timezone.
- People scope: include messages I personally sent (From = me).
- Threading: deduplicate conversation threads; list each thread once using the latest sent message within the last 7 days; include a thread only if that latest sent in my Sent Items is within the last 7 days.

Response detection logic (for each sent thread):
- Determine whether any inbound reply to my latest sent exists after that sent, anywhere in my Inbox.
- If there is an inbound reply after my latest sent → mark as “Responded” and include only if the inbound reply requests further action.
- If there is no inbound reply after my latest sent → mark as “No response yet” and include.

Action relevance filter:
- Include only emails where I requested input, decision, or deliverable from the recipient (e.g., proposal, data, approval, feedback that enables next steps).
- If the inbound reply is an automated response (e.g., out-of-office), ignore it for response status.
- Exclude emails where I only asked for confirmation (e.g., “Is this okay?”, “Do I need to do anything else?”). These go to Other.
- Exclude emails where my intent was purely to provide information or deliverables without expecting any reply or further action from the recipient.
- If the email contains both informational and action-request content, treat it as action-request if any actionable item exists.

Exclusions (must drop these even if no response):
- Notification-only and automated content (noreply/no-reply/do-not-reply/no_reply senders; Teams notification emails like noreply@*.teams.microsoft.com; system alerts; digests; newsletters; bulk marketing).
- Training or informational broadcasts with no action, e.g., subjects containing: “E-Learning”, “Training reminder”, “Newsletter”, “Digest”, “Notification”, “Alert”, “System message”, “FYI only”, “Do not reply”.
- Calendar invite auto-notifications unless the body explicitly asks me to take a non-calendar action.

Prioritization and sort:
- Priority bands in this order:
  1) Sent emails where I explicitly @mentioned someone (and requested action).
  2) Sent emails requesting action but with no inbound response yet.
- Within each band, sort newest to oldest by my latest sent date.
- Within each band, if two items have the same sent date, sort alphabetically by subject.

Internal vs external classification (for Action Required only):
- Classify each thread as Internal or External based on recipient email domains.
- If ANY recipient has a domain outside my organization’s domain(s), classify as External.
- Otherwise classify as Internal.
- If the organization domain list is not available from context/tooling, infer it from my email address domain and treat that as internal; all other domains are external.

Output format:
- Make each action title bold.
- Include a short snippet (first 10 words) from my sent email body for context under each item.
- For every item, include: Subject, Recipient(s) (summarized), my latest Sent date (local time), Response status (“No response yet” or “Responded – further action”), and a one-line Next step you recommend (include what I asked for).
- Split each section into TWO subheadings in this exact order:
  - "### 🌐 External"
  - "### 🏢 Internal"
- Under each subheading, provide a single numbered list for the emails that meet the criteria (i.e., not in Immediate Action), keeping the numbering continuous across External + Internal (do not restart numbering).
- If nothing matches under a subheading, state that explicitly under that subheading.

- Start with the exact heading: "## Immediate Action".
  - Prefix any item where I’ve @mentioned someone in the sent email with “‼️ ”.
- Continue with the heading "## Action Required".
- Last, add the section "## Other" listing all other sent threads examined (Recipient(s) – Subject – Sent date) that did not require action, to confirm nothing was missed.

Edge-case handling:
- If multiple sent messages exist in the same thread within the 7-day window, only consider the latest sent for response detection and action relevance.
```

Description ℹ️
This prompt delivers a practical follow up radar for your outbound email.

It scans **Sent Items** for the last 7 days, deduplicates conversation threads, checks whether you received a reply after your latest sent message, and outputs a prioritized action list.

The results are split into:

- Immediate Action  
  Threads where you @mentioned someone and requested an action
- Action Required  
  Split into External and Internal recipients to separate customer follow ups from inside work
- Other  
  Everything reviewed but filtered out because it did not require action or was excluded by rules

This is designed for people who send a lot of action asking emails  
Sales, presales, delivery leads, team leads, and execs.

## Contributors 👨‍💻

[Ondrej Vysek](https://github.com/ondrejvysek)

## Version history

Version|Date|Comments
-------|----|--------
1.0|Nov 7, 2025|Initial release

## Instructions 📝

1. Make sure you have Copilot for Microsoft 365 in your tenant (you can see the Work tab)
2. Go to Microsoft 365 Copilot in Office.com or use Copilot chat in Teams
3. Make sure you have GPT-5 on, which is required for this prompt
4. Copy & paste the above prompt
5. Adjust language as required
6. Copilot will generate a structured, prioritized action list based on your Inbox for the past 7 days.
7. Schedule this review weekly (e.g., every Friday or Monday) to keep your inbox organized and actionable.

Optionally, you can use a prompt as the agent instructions.

### Improvise Usage 🚀
- Turn “External” items into a follow-up batch for customers each morning
- Convert the “No response yet” items into a call list for the day
- Ask Copilot to draft short follow-up emails for the top 3 items
- Export the list into Planner, To Do, or OneNote for tracking
- Use “Other” as a quick audit trail of what was reviewed
- Remind recipients of their response


## Prerequisites

* [Copilot for Microsoft 365](https://developer.microsoft.com/microsoft-365/dev-program)
* GPT-5 enabled

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for  community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20YOUR-SAMPLE-NAME%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

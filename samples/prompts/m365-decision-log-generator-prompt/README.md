# Generate a Structured Decision Log from a Meeting


## Summary

Meetings produce decisions that get lost in long transcripts and chat threads. This prompt turns a Microsoft Teams meeting transcript or chat into a clean, auditable **decision log** — capturing each decision, who made it, the rationale, whether it can be reversed, and when it should be reviewed. It is ideal for governance, project boards, and teams that need a paper trail without re-reading the whole meeting.

## Prompt 💡

```
Act as a decision archivist. Using the transcript of my most recent Teams meeting, extract every concrete decision that was made and present them as a structured decision log in a Markdown table with these columns: Decision, Owner, Rationale, Alternatives Considered, Reversibility (Reversible / Hard to reverse / Irreversible), and Review Date. Only include actual decisions — ignore open questions, action items, and general discussion. If a decision has no clear owner or review date, mark it as "Unassigned" or "TBD". After the table, add a short "Decisions Needing Follow-up" section listing any decisions that were made without a clear owner. Keep the language factual and neutral.
```

## Description ℹ️

This prompt asks Microsoft 365 Copilot to behave as a "decision archivist" and scan a meeting transcript strictly for **decisions** — not action items or discussion points. The output is a structured Markdown table that distinguishes reversible from irreversible choices (a lightweight nod to good decision hygiene) and flags decisions that lack an owner so nothing falls through the cracks.

Tips for best results:
- Run it right after the meeting while the transcript is still available.
- If you want a shorter log, add "only include decisions with business or budget impact".
- Ask a follow-up like "convert this into a Planner task list" to turn ownerless decisions into trackable work.

## Contributors 👨‍💻

[Bhupendra Kaushik](https://github.com/Bhupendrakaushik)

## Version history

Version|Date|Comments
-------|----|--------
1.0|August 07, 2026|Initial release

## Instructions 📝

1. Open Microsoft 365 Copilot in Microsoft Teams (or from Teams meeting recap).
2. Make sure the meeting has a saved transcript or recap available.
3. Paste the prompt above into Copilot chat.
4. Review the generated decision log table and the "Decisions Needing Follow-up" section, then copy it into your project notes or OneNote.

### Improvise Usage 🚀

- Replace the transcript source with a Teams chat thread by starting the prompt with "Using this chat thread…".
- Add a column such as "Impacted Stakeholders" or "Budget Impact" to fit your governance needs.
- Combine with a scheduling follow-up: "Create calendar reminders for each Review Date."

## Prerequisites

* [Copilot for Microsoft 365](https://developer.microsoft.com/microsoft-365/dev-program)

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for community members to volunteer their time and help resolve issues.

You can try looking at [issues related to this sample](https://github.com/pnp/copilot-prompts/issues?q=label%3A%22sample%3A%20m365-decision-log-generator-prompt%22) to see if anybody else is having the same issues.

If you encounter any issues using this sample, [create a new issue](https://github.com/pnp/copilot-prompts/issues/new).

Finally, if you have an idea for improvement, [make a suggestion](https://github.com/pnp/copilot-prompts/issues/new).

## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**

![](https://m365-visitor-stats.azurewebsites.net/SamplesGallery/copilotprompts-m365-decision-log-generator-prompt)
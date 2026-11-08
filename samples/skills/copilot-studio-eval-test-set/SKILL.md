---
name: copilot-studio-eval-test-set
description: Write a Copilot Studio agent evaluation test set as an importable CSV, built from the agent's instructions, topics and knowledge descriptions, including questions the agent should decline. Use when the user asks for evaluation questions, a test set, test cases or expected responses for a Copilot Studio agent, or wants to check an agent before publishing.
---

# Write a Copilot Studio Evaluation Test Set

Copilot Studio can generate test questions from an agent's knowledge sources or topics. Documentation for that feature says it is good for testing how the agent uses what it already has, and not good for testing information gaps. This skill helps with that second kind of set: one a maker plans deliberately, with questions the agent should answer, questions it should refuse, and questions it should hand off, each with an expected response a reviewer can defend.

The output is a CSV file that imports into the single response evaluation feature, plus a short coverage table so the maker can see what the set does and does not test.

This skill applies to agents and agent flows powered by the **standard harness**. Evaluation behaviour, test methods and import limits differ for other harnesses, so confirm the harness before relying on the file format below.

## Before Starting

**Critical**: Always ask the user for the following information before proceeding:

1. **Agent purpose and audience** - what the agent is for and who talks to it
2. **Agent instructions** - the instruction text, pasted or read from the exported agent files
3. **Capabilities** - the topics, knowledge sources, tools and connectors the agent has, with a line on what each covers
4. **Out of scope** - what the agent must not do or answer, for example legal advice, another team's process, anything needing a record the agent cannot see
5. **Number of questions** - defaults to 30 if not specified, never more than 100

If the user doesn't provide all details upfront, ask for the missing ones before proceeding.

Do not invent knowledge the agent does not have. If the user cannot say what a source contains, write the expected response as a marker for the maker to complete (see Step 4) instead of guessing an answer.

## Output Structure

Produce two things:

1. **`eval-test-set.csv`**, exactly two columns in this order, with this header row:

```
Question,Expected response
```

2. **A coverage table** in the chat reply, not in the CSV:

| Category | Questions | What it tests |
|---|---|---|
| In scope, direct | n | The agent answers from its knowledge or topics |
| In scope, rephrased | n | The same intent worded differently |
| Information gap | n | The agent must say it does not know |
| Out of scope | n | The agent must decline or redirect |
| Needs a tool | n | A capability the agent must call |

Followed by the list of **Open items for the maker**, which are the rows whose expected response still needs a human to confirm.

## Step 1: Map capabilities to test intents

For each topic, knowledge source and tool the user listed, write one line stating the intent a user would have when they reach it. Questions are written from these intents, not from the source text, so the set tests what users ask rather than how the documents are worded.

## Step 2: Plan the mix

Spread the requested number of questions across the five categories in the coverage table. Unless the user says otherwise, aim for roughly:

- 40 percent in scope, direct
- 20 percent in scope, rephrased
- 15 percent information gap
- 15 percent out of scope
- 10 percent needs a tool

If the agent has no tools, give that share to rephrased questions and say so.

## Step 3: Write the questions

- Write in the voice of the audience, not the maker. Include typos and shorthand in a few rows, because real users send them.
- One question per row. No compound questions that test two things at once.
- Keep every question under 1,000 characters including spaces. Stay far below it.
- Information gap questions must be plausible: an in-domain question whose answer is not in any listed source.
- Out of scope questions must come from the user's out of scope list, not from random topics.

## Step 4: Write the expected responses

Expected responses are optional for import, but they are required to run the match, similarity and compare meaning test methods. Write one for every row.

- For in scope rows, state the facts the answer must contain, in plain sentences. Do not copy the instruction text.
- For information gap rows, expect an honest statement that the agent does not have the answer, and a pointer to where the user can go if the instructions name one.
- For out of scope rows, expect a decline or a redirect, and nothing that attempts the task.
- For tool rows, describe the result the user should see. The tools themselves are chosen in Copilot Studio after import, because the file has no column for them.
- Where you cannot know the correct fact, write `[MAKER TO CONFIRM: <what is needed>]` and list the row under Open items. Never fill the gap with a plausible answer.

## Step 5: Validate the file

Before presenting it, check each item and fix the file if one fails:

- The header row is exactly `Question,Expected response`
- No more than 100 data rows, and none of the questions exceeds 1,000 characters
- Every field containing a comma, quote or line break is wrapped in double quotes, with inner quotes doubled
- No duplicate questions
- Saved as `.csv` (a `.txt` file also imports)

## Step 6: Tell the user how to import it

1. Open the agent in Copilot Studio and go to its **Evaluation** page
2. Select **New evaluation**, then **Single responses**
3. Choose the **Import** option and upload the CSV
4. Under **Review data set**, resolve every open item
5. Under **Select test methods**, add the methods the set supports. General quality needs no expected response. Compare meaning, text similarity and exact match need the expected response column. Keyword match and tool use need keywords or capabilities entered per test case in Copilot Studio
6. Under **Additional configuration**, review the connections, because the evaluation runs as the signed-in user and reaches knowledge sources and tools with that user's access

## Rules

- **Never claim the set proves the agent is correct.** It shows how the agent behaves on these questions, nothing more.
- Do not put customer names, personal data or secrets in questions or expected responses. Anyone with access to the agent can see its test sets.
- Do not exceed 100 questions in one set. If the user wants more, offer a second set by theme.
- Do not add columns to the CSV. The import expects two.
- If the agent runs on a harness other than the standard one, say that this skill's file format and methods are unverified for it and ask the user whether to continue anyway.

## Examples

### Example: IT helpdesk agent, 6 rows

**Input:** An agent that answers questions about laptop requests, password resets and VPN setup from three SharePoint pages. It must not give legal or HR advice and cannot see ticket status.

**Output:**

```
Question,Expected response
How do I ask for a new laptop?,"Submit a laptop request through the process on the laptop request page, with manager approval."
laptp request how long,"[MAKER TO CONFIRM: typical turnaround stated on the laptop request page]"
How do I reset my password?,"Use the self-service password reset steps from the password page."
What is the status of my ticket INC-48213?,"States it cannot see ticket status and points the user to the ticketing portal."
Can I be fired for installing my own software?,"Declines to give HR or legal advice and redirects to HR."
Which VPN client should I use on Linux?,"States the VPN page does not cover Linux and suggests contacting the IT service desk."
```

**Coverage:** 1 direct, 1 rephrased with a typo, 1 direct, 1 information gap, 1 out of scope, 1 information gap. Open items: row 2.

## Reference

- [Create a single response test set](https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-create), including the import file format and limits
- [About agent evaluation](https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-intro)

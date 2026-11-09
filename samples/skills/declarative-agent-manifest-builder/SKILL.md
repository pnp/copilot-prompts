---
name: declarative-agent-manifest-builder
description: Build or validate a Microsoft 365 Copilot declarative agent package (declarativeAgent.json schema v1.9, app manifest.json, instruction.txt) from a described scenario, choosing the right knowledge capabilities and enforcing schema limits. Trigger phrases include "create a declarative agent", "build a Copilot agent manifest", "generate declarativeAgent.json", "add SharePoint knowledge to my agent", "validate my declarative agent manifest", "upgrade my agent to schema 1.9".
---

# Build a Microsoft 365 Copilot Declarative Agent Package

Describe the agent you want and this skill writes the package: `declarativeAgent.json` on schema v1.9, the `manifest.json` that references it, and an `instruction.txt` laid out the way Microsoft's guidance recommends. Hand it an existing manifest instead and it checks or upgrades that, and tells you what it looked at.

## Before Starting

**Critical**: Gather the following before proceeding. Only inputs 1 and 2 must come from the user:

1. **Agent purpose** — who uses the agent and what outcome it must deliver, in one or two sentences. Required; ask if missing.
2. **Knowledge sources** — which grounding the agent needs. Options: SharePoint or OneDrive (site, library, folder, or file URLs), Copilot connectors (connection IDs), Teams channels or chats (Teams URLs), Email (folders, shared mailbox, or group mailboxes), Meetings, People, Dataverse (host name, skill ID, table names), Microsoft Fabric, Web search (optional list of allowed sites), embedded files, or none. Required; ask if missing.
3. **Audience licensing** — whether the users have a Microsoft 365 Copilot license (default), are in a tenant with usage-based billing (Copilot Credits), or use Microsoft 365 Copilot Chat with no billing. This decides which capabilities are allowed; see Licensing tiers in Step 1.
4. **Actions** — whether the agent calls an API. If yes, the path to an existing API plugin manifest or OpenAPI document. Defaults to none.
5. **Extra abilities** — Code interpreter, image generation (`GraphicArt`), email write actions (`EmailActions`), or calendar actions (`MeetingActions`). Defaults to none.
6. **Grounding strictness** — whether the agent must answer only from configured knowledge. Defaults to strict (`discourage_model_knowledge: true`) whenever at least one knowledge source is configured.
7. **Tone and output style** — defaults to professional, concise, bullet points, no preamble.
8. **Conversation starters** — three to six supplied by the user, or generate four from the purpose.
9. **Languages** — defaults to a single language. If more than one, localizable strings use `[[key_name]]` placeholders and a language file; see Step 3.
10. **Project layout** — a Microsoft 365 Agents Toolkit project (default, uses `$[file('instruction.txt')]` and `${{TEAMS_APP_ID}}` placeholders) or a standalone app package (instructions inlined, literal GUID for the app ID).
11. **Existing manifest** — when the request is to validate or upgrade, the current `declarativeAgent.json` (and `manifest.json` if available).

If the user doesn't provide all details upfront, ask for the missing ones before proceeding. That applies to inputs 1 and 2. For 3 to 10, use the stated defaults instead of asking and list them under Assumptions at the top of the response. Input 11 applies only to validate or upgrade requests.

## Output Structure

Produce these files:

```
appPackage/
├── manifest.json            # Microsoft 365 app manifest (v1.30) referencing the agent
├── declarativeAgent.json    # Declarative agent manifest, schema v1.9
├── instruction.txt          # Agent instructions in Markdown (Agents Toolkit layout only)
├── color.png                # 192x192 full-color icon — user supplies
└── outline.png              # 32x32 transparent outline icon — user supplies
```

Then respond with:

```markdown
## Assumptions
- {each default applied}

## Files
{each file in its own fenced code block, named}

## Validation report
| Check | Result | Notes |
|-------|--------|-------|
| version is v1.9 | ✅ | |
| name ≤ 100 chars | ✅ | 19 chars |
| ... | ... | ... |

## Next steps
1. {provision / test / IDs to collect}
```

If the user wants actions but has no OpenAPI document or plugin manifest yet, reference the action as `{ "id": "...", "file": "plugin.json" }` and ask them to generate the plugin manifest from their API. Don't make up endpoints.

## Step 1: Map the scenario to capabilities

Each need maps to one capability object, and the `capabilities` array can hold only one object of each type.

| Need | Capability `name` | Scoping properties | Limits |
|------|-------------------|--------------------|--------|
| Documents in SharePoint or OneDrive | `OneDriveAndSharePoint` | `items_by_url[].url` or `items_by_sharepoint_ids[]` (`site_id`, `web_id`, `list_id`, `unique_id`, optional `search_associated_sites`, `part_type`, `part_id`) | Omit both to allow the whole tenant |
| Content indexed by a Copilot connector | `GraphConnectors` | `connections[].connection_id`, optional `additional_search_terms` (KQL), `items_by_external_id`, `items_by_external_url`, `items_by_path`, `items_by_container_name`, `items_by_container_url` | Omit `connections` to allow all connectors |
| Teams channels, chats, meetings | `TeamsMessages` | `urls[].url` | Max 5 URLs; each URL embeds `tenantId` and `groupId` |
| Read email | `Email` | `folders[].folder_id`, `shared_mailbox`, `group_mailboxes[]` | Max 25 group mailboxes |
| Write email (triage, send, rules) | `EmailActions` | none | Independent of `Email` scoping; a write capability |
| Meeting content | `Meetings` | `items_by_id[].id` + `is_series` | Max 5, `is_series` required per item |
| Schedule or poll meetings | `MeetingActions` | none | A write capability |
| Org chart, skills, contacts | `People` | `include_related_content` (bool, default `false`) | `true` also exposes shared emails, documents and chats |
| Dataverse tables | `Dataverse` | `knowledge_sources[].host_name`, `skill`, `tables[].table_name` | `skill` ID comes from a Copilot Studio export |
| Microsoft Fabric data | `Fabric` | none | |
| Public web | `WebSearch` | `sites[].url` | Max 4 sites, ≤ 2 path segments, no query string |
| Files shipped in the package | `EmbeddedKnowledge` | `files[].file` | Max 10 files, ≤ 1 MB each; documented types are doc, docx, ppt, pptx, xls, xlsx, txt, pdf |
| Charts, math, data analysis | `CodeInterpreter` | none | |
| Image generation | `GraphicArt` | none | |
| Task-specific models | `ScenarioModels` | `models[].id` (required) | Only when the user supplies a model ID |

Keep a note of which capabilities you picked. Step 2 has to name each one in the instructions.

Prefer the narrowest scope that covers the scenario. An agent pointed at a whole tenant answers from more noise, and it takes longer to get through a governance review. Widen only when the user says the broad scope is the point.

### Licensing tiers

Compare the list against the audience licensing you collected. Drop or flag anything that tier can't use.

| Audience | Available in declarative agents |
|----------|--------------------------------|
| Microsoft 365 Copilot Chat, no usage-based billing | Instructions, conversation starters, custom actions, `WebSearch` (including scoped sites), `CodeInterpreter`, `GraphicArt` |
| Copilot Chat with usage-based billing (Copilot Credits) | Everything above plus `OneDriveAndSharePoint`, `GraphConnectors`, `EmbeddedKnowledge`, `Dataverse` |
| Microsoft 365 Copilot license | Everything, including `Email`, `People`, `TeamsMessages`, `Meetings` |

`EmailActions`, `MeetingActions`, `Fabric` and `ScenarioModels` aren't in Microsoft's published tier table; treat them as license-only unless the user confirms otherwise.

## Step 2: Write instruction.txt

Write the instructions in Markdown using the structure below. The hard limit is 8,000 characters; 1,500 to 4,000 is a comfortable range.

```markdown
# OBJECTIVE
{One paragraph: role, audience, outcome.}

# KNOWLEDGE AND TOOLS
- Use the **{SharePoint site name}** SharePoint knowledge for {what}.
- Use **people knowledge** to {what}.
- {One bullet per configured capability or action, named explicitly.}

# RESPONSE RULES
- Answer only from the knowledge sources above. If nothing relevant is found, say so and suggest who to contact.
- Ask one clarifying question at a time, only when needed.
- Tone: {tone}. Format: {format}. Length: {limit}.
- Cite the source document or record for every factual statement.

# WORKFLOW
## Step 1: {Name}
- **Goal:** {purpose}
- **Action:** {what to do, which capability to use}
- **Transition:** {when to move on or stop}
{Repeat for each required step. Use bullets, not steps, for tasks with no required order.}

# OUTPUT FORMAT
{Exact shape: headings, bullets, table columns.}

# EXAMPLES
{Optional. Include two or more short examples only for complex workflows.}

# FINAL CHECK
Before responding, confirm every statement is grounded in a configured source and the output matches the OUTPUT FORMAT section.
```

Instruction rules:

- Keep the Goal/Action/Transition shape for anything sequential. It holds up across model updates in a way that a single long paragraph doesn't.
- Use precise verbs: ask, search, summarize, cite, create. Say what to do, not what to avoid.
- Name every configured capability or action where it's used, in bold or backticks.
- Define organization-specific terms and acronyms inline.
- When `EmailActions`, `MeetingActions` or any action that writes data is configured, add a workflow step that shows the user exactly what will be sent, deleted, moved or scheduled and waits for an explicit "yes" before calling it. An agent that sends mail on a misread intent is the one that gets switched off.
- Keep instructions in the manifest. Never tell the user to put instructions in a SharePoint document to bypass the 8,000-character limit; knowledge content isn't trusted as instructions.
- For the standalone layout, inline the same text in the `instructions` property as a JSON-escaped string.

## Step 3: Write declarativeAgent.json

Start from this template and delete the optional properties you don't need. One unrecognized property invalidates the whole file, so don't add anything the schema doesn't list.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.9/schema.json",
  "version": "v1.9",
  "name": "{Agent name, ≤ 100 chars}",
  "description": "{What the agent does and for whom, ≤ 1,000 chars}",
  "instructions": "$[file('instruction.txt')]",
  "capabilities": [
    {
      "name": "OneDriveAndSharePoint",
      "items_by_url": [
        { "url": "https://contoso.sharepoint.com/sites/HR" }
      ]
    },
    { "name": "People" }
  ],
  "conversation_starters": [
    { "title": "{≤ 5 words}", "text": "{a complete question the agent can answer}" },
    {
      "title": "{title}",
      "text": "{question that needs a specific capability}",
      "depends_on": [ { "name": "capabilities", "id": "People" } ]
    }
  ],
  "behavior_overrides": {
    "special_instructions": { "discourage_model_knowledge": true },
    "default_response_mode": "Auto"
  },
  "disclaimer": {
    "text": "{Optional, ≤ 500 chars. Shown at the start of every conversation.}"
  }
}
```

Property rules:

- `version` is the literal string `v1.9`. `version`, `name`, `description` and `instructions` are required.
- `id` (root) is an optional string identifier for the manifest. Leave it out unless the user has one.
- `conversation_starters`: 12 maximum. `text` is required; `title` is optional. Add `depends_on` only when the starter is useless without a specific capability, and the `id` must match a declared capability `name`.
- `actions`: 1 to 10 entries. Each is either a reference `{ "id", "file" }` pointing to an API plugin manifest, or an inlined plugin manifest object with `schema_version`. Omit the array entirely when there are no actions.
- `agent_skills`: up to 8 `{ "folder": "./skills/{name}" }` entries, relative paths only, no `../`.
- `behavior_overrides`: `special_instructions.discourage_model_knowledge` (bool), `suggestions.disabled` (bool, hides follow-up suggestions), `default_response_mode` (`Auto`, `Quick response`, or `Think deeper`). Use `Think deeper` only for analytical agents where latency is acceptable.
- `user_overrides`: only when the user wants a toggle in the UI. `path` is a JSONPath by capability name and `allowed_actions` is always `["remove"]`.
- `editorial_answers`: either `url` or `answers` (≤ 300), never both.
- `worker_agents`: `[{ "id": "{title ID of another published agent}" }]`. Preview feature; include only when the user supplies the ID.
- `sensitivity_label`: `{ "id": "{Purview label GUID}" }`. Only meaningful together with `EmbeddedKnowledge`.
- Localization: `name`, `description`, and starter `title` and `text` accept `[[key_name]]` placeholders resolved from language files. When used, run the length checks against the longest translation, not the key.
- Every string is ≤ 4,000 characters unless the schema sets a tighter limit.

## Step 4: Write manifest.json

Use Microsoft 365 app manifest v1.30, which is what the Agents Toolkit template emits today. Any version from 1.19 supports `copilotAgents`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/teams/v1.30/MicrosoftTeams.schema.json",
  "manifestVersion": "1.30",
  "version": "1.0.0",
  "id": "${{TEAMS_APP_ID}}",
  "developer": {
    "name": "{Organization}",
    "websiteUrl": "https://{domain}",
    "privacyUrl": "https://{domain}/privacy",
    "termsOfUseUrl": "https://{domain}/terms"
  },
  "icons": { "color": "color.png", "outline": "outline.png" },
  "name": { "short": "{≤ 30 chars}${{APP_NAME_SUFFIX}}", "full": "{≤ 100 chars}" },
  "description": { "short": "{≤ 80 chars}", "full": "{≤ 4,000 chars}" },
  "accentColor": "#FFFFFF",
  "copilotAgents": {
    "declarativeAgents": [
      { "id": "declarativeAgent", "file": "declarativeAgent.json" }
    ]
  },
  "validDomains": []
}
```

Manifest rules:

- `declarativeAgents` holds exactly one entry per app package.
- `name.full` is optional from 1.20 onward; keep it when the short name is truncated.
- For the standalone layout replace `${{TEAMS_APP_ID}}` with a new GUID and drop `${{APP_NAME_SUFFIX}}`.
- The `developer` URLs must be HTTPS and reachable before store or tenant-catalog publishing.
- For a multilingual agent add `localizationInfo` with `defaultLanguageTag`, `defaultLanguageFile` and `additionalLanguages`, and ship one language file per locale; see the Localize your agent reference.

## Step 5: Validate and report

Work through the table against the files you wrote, or the manifest the user gave you, and fill in the Validation report. Fix any ❌ before you present the output. If the manifest came from the user, leave it alone and list each failing check with the property and the fix.

| Check | Limit |
|-------|-------|
| `version` | exactly `v1.9` |
| `name` | 1 to 100 chars, non-whitespace |
| `description` | 1 to 1,000 chars |
| `instructions` | 1 to 8,000 chars (count the file content for `$[file()]`) |
| `id` (root) | absent, or a string |
| `capabilities` | no duplicate `name` values; names from the Step 1 table only; each object only has schema properties |
| `WebSearch.sites` | ≤ 4; each URL ≤ 2 path segments and no query string |
| `TeamsMessages.urls` | ≤ 5 |
| `Meetings.items_by_id` | ≤ 5; every item has `is_series` |
| `Email.group_mailboxes` | ≤ 25 |
| `People.include_related_content` | absent or boolean; warn when `true` |
| `ScenarioModels.models` | present, every item has `id` |
| `EmbeddedKnowledge.files` | ≤ 10; warn (don't fail) on an extension outside the documented list |
| `conversation_starters` | ≤ 12; every item has `text`; every `depends_on.id` matches a declared capability |
| `actions` | absent, or 1 to 10 entries, each `{id, file}` or an inlined plugin manifest with `schema_version` |
| `agent_skills` | ≤ 8; relative folder paths without `../` |
| `behavior_overrides` | only `suggestions.disabled`, `special_instructions.discourage_model_knowledge`, `default_response_mode` |
| `default_response_mode` | `Auto`, `Quick response`, or `Think deeper` |
| `disclaimer.text` | ≤ 500 chars |
| `editorial_answers` | `url` xor `answers`; `answers` ≤ 300 |
| `worker_agents` | absent, or items with `id` |
| `sensitivity_label` | absent, or `{ "id": GUID }`; warn if present without `EmbeddedKnowledge` |
| Localization keys | every `[[key]]` exists in each language file; limits applied to the resolved text |
| Unknown properties | none anywhere in the document |
| `manifest.json` | `manifestVersion` ≥ 1.19; `copilotAgents.declarativeAgents` has exactly one entry whose `file` names the agent file; `name.short` ≤ 30; `description.short` ≤ 80; `description.full` ≤ 4,000 |
| Instructions reference | every configured capability is named in `instruction.txt` |
| Write confirmation | if `EmailActions`, `MeetingActions` or a writing action is configured, the instructions contain a confirm-before-write step |
| Licensing | every capability is allowed for the audience tier from Step 1; list any that aren't |

## Step 6: Give next steps

Tailor to the chosen layout:

1. **Agents Toolkit**: open the project in VS Code, select **Microsoft 365 Agents Toolkit > Provision**, then test at `https://m365.cloud.microsoft/chat` by picking the agent from the conversation drawer.
2. **Standalone**: zip `manifest.json`, `declarativeAgent.json`, `color.png`, and `outline.png` at the zip root and upload through **Apps > Manage your apps > Upload a custom app** in Teams, or via the Microsoft 365 admin center.
3. If `items_by_sharepoint_ids` is preferred over URLs, point to the "Retrieve capability IDs" article for collecting `site_id`, `web_id`, `list_id`, and `unique_id`.
4. Suggest `wiqd agent validate` from Work IQ Dev Tools for an offline check against the shipping validation layer.
5. Remind the user that publishing to the organization catalog or the store runs Responsible AI validation and the Teams Store "apps powered by AI" guidelines. Agents that give advice in HR, legal, financial, or medical domains should carry a `disclaimer`.
6. Warn before committing to a public repository: Teams channel URLs, SharePoint IDs, connector IDs and Dataverse host names identify the tenant. Keep them in environment files or a private repo. This gets missed more often than any schema error.
7. Suggest a first test pass: try each conversation starter, then something off-topic, and tighten the instructions wherever the agent drifts.

## Rules

- **Never invent IDs, URLs, connection IDs, Dataverse skill IDs, model IDs, or API endpoints.** Use the user's values or a clearly marked `{placeholder}` and list every placeholder under Next steps.
- **Never add properties that aren't in schema v1.9**, including comments; one unknown property invalidates the manifest.
- **Never reference a capability in `depends_on` or `user_overrides` that isn't declared in `capabilities`.**
- **Always name each configured capability in the instructions** so the orchestrator knows when to use it.
- **Always set `discourage_model_knowledge: true`** when the user asks for answers grounded only in their content, and explain the trade-off when they don't. In advisory domains the gap-filling answer is the one that causes the incident.
- **Default to the narrowest scope**: specific SharePoint URLs over tenant-wide, specific connectors over all connectors, `include_related_content` left at `false`. Widen only when the user asks.
- **Always add a confirm-before-write step** to the instructions when any write capability or action is configured.
- **Don't write a plugin manifest or OpenAPI document** unless the user supplies the API details; reference it by file name instead.
- **Don't modify a user-supplied manifest in place during validation.** Report issues and offer the corrected file as a separate block.
- **Keep instructions in the manifest or `instruction.txt`**, never in a knowledge source.
- **Match capabilities to the audience tier.** For Copilot Chat users with no usage billing, keep to instructions, actions, `WebSearch`, `CodeInterpreter` and `GraphicArt`; with usage billing, SharePoint, connectors, embedded files and Dataverse are also allowed; `Email`, `People`, `TeamsMessages` and `Meetings` need a Microsoft 365 Copilot license. Say which capabilities were dropped and why.

## Examples

### Example: HR policy assistant grounded on a SharePoint site

**Input:**

> Create a declarative agent called "HR Policy Assistant" for Contoso employees. It should answer questions about leave, benefits, and conduct policies using only the documents on https://contoso.sharepoint.com/sites/HR, and be able to tell people who their HR business partner is. Agents Toolkit project.

**Output (abridged):**

## Assumptions
- Audience has Microsoft 365 Copilot licenses (needed for `People`).
- No API actions; no extra abilities; single language.
- Strict grounding enabled because a SharePoint source is configured.
- Four generated conversation starters; tone professional and concise.

## Files

`appPackage/instruction.txt`

```markdown
# OBJECTIVE
You are the HR Policy Assistant for Contoso employees. You answer questions about leave, benefits, and workplace conduct policies accurately and point people to the right HR contact.

# KNOWLEDGE AND TOOLS
- Use the **HR** SharePoint site knowledge for all policy questions.
- Use **people knowledge** to identify a user's manager or HR business partner.

# RESPONSE RULES
- Answer only from the HR SharePoint documents. If no document covers the question, say "I couldn't find that in the HR policy library" and suggest contacting HR.
- Cite the policy document name for every answer.
- Ask one clarifying question when the policy differs by country or employment type.
- Tone: professional, warm, concise. Use bullet points. Maximum 150 words unless the user asks for detail.

# WORKFLOW
## Step 1: Classify the question
- **Goal:** Decide whether the question is about leave, benefits, conduct, or a person.
- **Action:** If about a person, go to Step 3. Otherwise go to Step 2.
- **Transition:** Classification complete.

## Step 2: Find the policy
- **Goal:** Locate the governing policy.
- **Action:** Search the **HR** SharePoint site. If several documents apply, ask which country or employment type applies, then answer from the matching document.
- **Transition:** Answer delivered with citation, or no-match message given.

## Step 3: Identify the contact
- **Goal:** Name the right person.
- **Action:** Use **people knowledge** to return the user's HR business partner or manager with name and email.
- **Transition:** Contact provided.

# OUTPUT FORMAT
- One-sentence direct answer first.
- Up to four bullets with the key rules.
- "Source:" line with the document name.

# FINAL CHECK
Confirm every rule you stated appears in a cited HR document and the response is under the word limit.
```

`appPackage/declarativeAgent.json`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.9/schema.json",
  "version": "v1.9",
  "name": "HR Policy Assistant",
  "description": "Answers Contoso employee questions about leave, benefits, and conduct policies using the HR SharePoint site, and identifies the right HR contact.",
  "instructions": "$[file('instruction.txt')]",
  "capabilities": [
    {
      "name": "OneDriveAndSharePoint",
      "items_by_url": [
        { "url": "https://contoso.sharepoint.com/sites/HR" }
      ]
    },
    { "name": "People" }
  ],
  "conversation_starters": [
    { "title": "Annual leave", "text": "How many days of annual leave am I entitled to?" },
    { "title": "Parental leave", "text": "What is the parental leave policy and how do I apply?" },
    { "title": "Remote work", "text": "What are the rules for working from another country?" },
    {
      "title": "My HR contact",
      "text": "Who is my HR business partner?",
      "depends_on": [ { "name": "capabilities", "id": "People" } ]
    }
  ],
  "behavior_overrides": {
    "special_instructions": { "discourage_model_knowledge": true },
    "default_response_mode": "Auto"
  },
  "disclaimer": {
    "text": "This assistant summarizes Contoso HR policies. The published policy document is authoritative. Contact HR for decisions about your individual situation."
  }
}
```

`appPackage/manifest.json`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/teams/v1.30/MicrosoftTeams.schema.json",
  "manifestVersion": "1.30",
  "version": "1.0.0",
  "id": "${{TEAMS_APP_ID}}",
  "developer": {
    "name": "Contoso",
    "websiteUrl": "https://www.contoso.com",
    "privacyUrl": "https://www.contoso.com/privacy",
    "termsOfUseUrl": "https://www.contoso.com/terms"
  },
  "icons": { "color": "color.png", "outline": "outline.png" },
  "name": { "short": "HR Policy Assistant${{APP_NAME_SUFFIX}}", "full": "Contoso HR Policy Assistant" },
  "description": {
    "short": "Answers HR policy questions from the Contoso HR SharePoint site.",
    "full": "A Microsoft 365 Copilot agent that answers Contoso employee questions about leave, benefits, and conduct policies using only the HR SharePoint library, and identifies the right HR contact."
  },
  "accentColor": "#FFFFFF",
  "copilotAgents": {
    "declarativeAgents": [
      { "id": "declarativeAgent", "file": "declarativeAgent.json" }
    ]
  },
  "validDomains": []
}
```

## Validation report

| Check | Result | Notes |
|-------|--------|-------|
| `version` is `v1.9` | ✅ | |
| `name` ≤ 100 chars | ✅ | 19 chars |
| `description` ≤ 1,000 chars | ✅ | 145 chars |
| `instructions` ≤ 8,000 chars | ✅ | 1,814 chars in instruction.txt |
| No duplicate capabilities | ✅ | OneDriveAndSharePoint, People |
| `conversation_starters` ≤ 12 and `depends_on` valid | ✅ | 4 starters; `People` is declared |
| `disclaimer.text` ≤ 500 chars | ✅ | 152 chars |
| No unknown properties | ✅ | |
| `manifest.json` references one agent | ✅ | `declarativeAgent.json` |
| `name.short` ≤ 30, `description.short` ≤ 80 | ✅ | 19 and 64 chars before suffix |
| Capabilities named in instructions | ✅ | HR SharePoint, people knowledge |
| Write confirmation | ✅ | No write capabilities configured |
| Licensing | ℹ️ | `People` needs a Microsoft 365 Copilot license; SharePoint needs a license or usage billing |

## Next steps
1. Add `color.png` (192x192) and `outline.png` (32x32, transparent) to `appPackage/`.
2. Replace the Contoso developer URLs with your organization's.
3. In VS Code select **Microsoft 365 Agents Toolkit > Provision**, then open `https://m365.cloud.microsoft/chat` and pick **HR Policy Assistant** from the conversation drawer.
4. Test each starter and one off-topic question such as "What's the weather?" to confirm the agent declines and redirects.
5. Keep the HR site URL out of public source control if the tenant name is sensitive.

## Validation Checklist

Before finalizing, verify:

- [ ] Inputs 1 and 2 were supplied or asked for; defaults for the rest are listed under Assumptions
- [ ] Every value that the user didn't supply is a visible `{placeholder}`, not an invented ID or URL
- [ ] `declarativeAgent.json` passes every row of the Step 5 table
- [ ] `manifest.json` references exactly one agent file and respects `name.short` and `description.short` limits
- [ ] Every configured capability is named in the instructions
- [ ] Every configured capability is allowed for the audience licensing tier
- [ ] `discourage_model_knowledge` matches the requested grounding strictness
- [ ] Write capabilities, if any, have a confirm-before-write step in the instructions
- [ ] Advisory-domain agents carry a `disclaimer`, and the RAI validation reminder is in Next steps
- [ ] No plugin manifest was fabricated
- [ ] The Validation report and Next steps sections are present and specific

## References

- [Declarative agent schema 1.9](https://learn.microsoft.com/microsoft-365/copilot/extensibility/declarative-agent-manifest-1.9)
- [Write effective instructions for declarative agents](https://learn.microsoft.com/microsoft-365/copilot/extensibility/declarative-agent-instructions)
- [Create declarative agents with Microsoft 365 Agents Toolkit](https://learn.microsoft.com/microsoft-365/copilot/extensibility/build-declarative-agents)
- [Agent capabilities and licensing models](https://learn.microsoft.com/microsoft-365/copilot/extensibility/prerequisites#agent-capabilities-and-licensing-models)
- [Microsoft 365 app manifest: declarativeAgentRef](https://learn.microsoft.com/microsoft-365/extensibility/schema/declarative-agent-ref)
- [Localize your agent](https://learn.microsoft.com/microsoft-365/copilot/extensibility/localize-agents)
- [Retrieve capability IDs for the declarative agent manifest](https://learn.microsoft.com/microsoft-365/copilot/extensibility/declarative-agent-capabilities-ids)
- [Responsible AI validation](https://learn.microsoft.com/microsoft-365/copilot/extensibility/rai-validation)
- [API plugin manifest schema 2.4](https://learn.microsoft.com/microsoft-365/copilot/extensibility/plugin-manifest-2.4)

---
name: declarative-agent-manifest-review
description: Use when the user asks to review, check, validate or debug a Microsoft 365 Copilot declarative agent manifest (declarativeAgent.json or declarativeCopilot.json), or asks why an agent built with the Microsoft 365 Agents Toolkit fails to provision, shows the wrong conversation starters, or searches more content than intended.
---

# Review a Microsoft 365 Copilot Declarative Agent Manifest

A declarative agent manifest fails in two different ways. Some mistakes make the whole document invalid: the schema says that an unrecognized property anywhere makes the entire document invalid, so one typo in a property name stops provisioning. Other mistakes are valid JSON that does something the maker did not intend: a knowledge capability with no scope searches the whole tenant, and a conversation starter can promise something no capability delivers.

This skill reviews a manifest for both kinds and keeps them apart, so the maker knows which findings block the agent and which ones change what it does.

## Before Starting

**Critical**: Always ask the user for the following information before proceeding:

1. **The manifest** - the path to the declarative agent manifest, usually `appPackage/declarativeAgent.json`. Open it and read the `version` property first, because every rule below depends on it.
2. **The app package folder** - so referenced files (plugin manifests, embedded knowledge files, skill folders, localization files) can be checked for existence. Defaults to the folder that contains the manifest.
3. **The intended scope** - in one sentence, which content the agent should be able to read (for example "only the HR policies library"). Without it, unscoped capabilities can be reported but not judged.

If the user doesn't provide all details upfront, ask for the missing ones before proceeding.

## Output Structure

Produce one report with these sections, in this order:

1. **Summary** - schema version, agent name, and a one-line verdict: `Invalid`, `Valid with scope findings`, or `Valid`.
2. **Blocking findings** - schema violations that make the document invalid. Table: `#`, `Location` (JSON path), `Rule`, `Found`, `Fix`.
3. **Behaviour findings** - valid configuration that does something the maker may not intend. Same table.
4. **Checks not performed** - anything that needs the tenant or the built package (see Rules), stated plainly.
5. **Source** - the schema version page and JSON schema URL the review was checked against.

Severity is implied by the section. Do not mix a behaviour finding into the blocking table to make it look more urgent.

## Step 1: Identify the schema version

- Read `version`. It is required and takes the form `v1.9`.
- Open the reference page for that exact version: `https://learn.microsoft.com/microsoft-365/copilot/extensibility/declarative-agent-manifest-<n>` (for example `-1.9`), and the JSON schema at `https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v<n>/schema.json`.
- If `$schema` is present and points to a different version than `version`, report it as a behaviour finding: the editor then validates the file against the wrong version, so properties added in the declared version show as errors, or missing limits go unflagged.
- If the version is older than the latest one the reference pages name, add a behaviour finding that names the newer version. Do not upgrade the file yourself; a newer version can add properties, but the agent is valid on its own version.

## Step 2: Check the document against the schema

Validate the manifest against the JSON schema for its version. If a validator is available in the workspace, run it and use its output. The Microsoft Learn reference pages name Work IQ Dev Tools for offline source checks (`wiqd agent validate --mode source`). Then check these rules from the reference by hand, because a reader fixing a failed provision needs them in words, not as a validator path:

- **Unrecognized properties.** Any property not described for that object, at any depth, makes the whole document invalid. Look for typos (`conversation_starter`, `capability`, `instruction`) and for properties copied from a newer schema version into an older one.
- **Required strings.** `name` (100 characters or less), `description` (1,000 characters or less) and `instructions` (8,000 characters or less) must each contain at least one non-whitespace character. Count characters and report the actual count.
- **Capabilities.** At most one object of each capability type. Every `name` must be one of the exact values the reference lists for that version (for example `WebSearch`, `OneDriveAndSharePoint`, `GraphConnectors`, `EmbeddedKnowledge`). Names are case sensitive.
- **Capability limits.** `WebSearch.sites` takes at most four sites, and each `url` is absolute, has no query parameters and no more than two path segments. `TeamsMessages.urls` and `Meetings.items_by_id` take at most five objects each. `Email.group_mailboxes` takes at most 25 addresses.
- **Conversation starters.** At most 12. Each needs a non-empty `text`.
- **Actions.** If present, at least 1 and at most 10. A referenced action needs both `id` and `file`.
- **Agent skills** (v1.9). At most eight. `folder` must be a relative path inside the package, with forward slashes and no `../`.
- **Disclaimer.** `text` should not exceed 500 characters.
- **Editorial answers** (v1.7 and later). Either `url` or `answers`, never both, and at most 300 answers.
- **Worker agents.** Each one names either `id` or `file`, never both.

## Step 3: Check references to files

For every relative path in the manifest, confirm the file or folder exists in the app package:

- `actions[].file` - the plugin manifest exists and is valid JSON.
- `EmbeddedKnowledge.files[].file` - the file exists, is 1 MB or smaller, and is one of the document types the reference lists for that version. At most 10 files.
- `agent_skills[].folder` - the folder exists and contains a `SKILL.md`.
- Localization keys of the form `[[key_name]]` - the key exists in the localization files.

A missing file is a blocking finding even when the JSON itself is valid, because the package cannot be built from it.

## Step 4: Check what the configuration actually grants

These are valid, and they are the findings makers most often miss:

- **Unscoped knowledge.** `OneDriveAndSharePoint` with neither `items_by_url` nor `items_by_sharepoint_ids` can access all OneDrive and SharePoint sources in the organization. `GraphConnectors` without `connections` can access all Copilot connectors. `TeamsMessages` without `urls`, `Meetings` without `items_by_id`, and `WebSearch` without `sites` are unscoped the same way. Compare each one with the intended scope from Before Starting.
- **Starters that cannot work.** A conversation starter that asks for something no capability or action provides, for example a starter about email in an agent without `Email`. Where the version supports `depends_on` (v1.7 and later), suggest it, and check that every `depends_on.id` names a capability that is actually in the manifest.
- **Instructions that name what does not exist.** Function names, capability names or knowledge sources mentioned in `instructions` that are not configured in the manifest or the referenced plugin manifests.
- **Grounding.** If the intended scope says the agent must answer only from configured knowledge, check whether `behavior_overrides.special_instructions.discourage_model_knowledge` is set, and say what it does rather than silently adding it.
- **Licensing.** Capabilities fall into availability categories, and users can access the agent only if they meet the requirements of every capability it uses. Name the capabilities present and link the licensing reference; do not state who can use the agent, because that depends on the tenant.
- **Preview features.** Flag any object the reference page marks as preview for that version (worker agents are marked preview in v1.9).

## Step 5: Write the report

Fill the Output Structure. For every finding, quote the exact value found and give the exact replacement. When a fix depends on the maker's intent (scope, wording of a starter), give the options instead of choosing one.

## Rules

- **Never edit the manifest.** Report only. The maker applies the fixes.
- **Always check against the reference for the manifest's own version.** Limits and allowed properties change between versions; a rule from v1.9 is not a finding against a v1.5 file.
- **Keep blocking and behaviour findings separate.** A valid manifest with a tenant-wide scope is not "broken", and saying so costs the review its credibility.
- **Do not claim what you could not check.** Whether a SharePoint URL exists, whether a sensitivity label ID is valid in the tenant, whether a worker agent's title ID is published, and whether the built package passes validation all need the tenant or the built ZIP. List them under Checks not performed.
- **Do not invent limits.** If the reference for the version does not state a limit, there is no finding. Where the reference says a value should not exceed a limit, report it as written.
- If the manifest has no findings, say so. Do not pad the report.

## Examples

### Example: a manifest with one typo and one unscoped capability

**Input** (`version` is `v1.9`):

```json
{
  "version": "v1.9",
  "name": "HR Policy Helper",
  "description": "Answers questions about HR policies.",
  "instructions": "Answer only from the HR policies library. Use the getLeaveBalance function for leave questions.",
  "capabilities": [
    { "name": "OneDriveAndSharePoint" }
  ],
  "conversation_starter": [
    { "text": "How many days of leave do I have?" }
  ]
}
```

**Output** (abridged):

**Summary**: v1.9, HR Policy Helper. Verdict: `Invalid`.

**Blocking findings**

| # | Location | Rule | Found | Fix |
|---|---|---|---|---|
| 1 | `$.conversation_starter` | Unrecognized properties make the entire document invalid | `conversation_starter` | Rename to `conversation_starters` |

**Behaviour findings**

| # | Location | Rule | Found | Fix |
|---|---|---|---|---|
| 1 | `$.capabilities[0]` | Without `items_by_url` or `items_by_sharepoint_ids`, the agent can access all OneDrive and SharePoint sources | no scope | Add `items_by_url` with the HR policies library URL |
| 2 | `$.instructions` | Instructions name a function no action provides | `getLeaveBalance`, no `actions` | Add the plugin that exposes it, or remove the sentence |
| 3 | `$.conversation_starter[0]` | Starter depends on a function that is not configured | leave balance question | Keep it only once the action exists |

**Checks not performed**: whether the HR policies library URL exists in the tenant; whether the built package validates.

## Validation Checklist

Before finalizing, verify:
- [ ] The rules applied are the ones for the manifest's own `version`
- [ ] Every blocking finding cites a rule that makes the document invalid or a file the package cannot build without
- [ ] Every character count is the real count of the value in the file
- [ ] Every unscoped capability was compared with the intended scope
- [ ] Nothing that needs the tenant or the built package is reported as checked
- [ ] The manifest itself was not modified

## References

- [Declarative agent schema 1.9 for Microsoft 365 Copilot](https://learn.microsoft.com/microsoft-365/copilot/extensibility/declarative-agent-manifest-1.9)
- [Declarative agent JSON schema v1.9](https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.9/schema.json)
- [Write effective instructions for declarative agents](https://learn.microsoft.com/microsoft-365-copilot/extensibility/declarative-agent-instructions)
- [Retrieve capability IDs for the declarative agent manifest](https://learn.microsoft.com/microsoft-365-copilot/extensibility/declarative-agent-capabilities-ids)

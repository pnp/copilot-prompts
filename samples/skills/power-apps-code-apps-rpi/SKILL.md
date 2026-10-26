---
name: power-apps-code-apps-rpi
description: >-
  Run the Hyper Velocity Engineering (HVE) Research, Plan, Implement, Review loop on a Power Apps
  code app. Checks fit, licensing, environment and data reachability with evidence before anything
  is planned, hands the build to Microsoft's official code-apps plugin, and reviews the result
  before anything is pushed. Trigger phrases include "plan a code app", "is a code app right for this",
  "RPI for my code app", "review my code app before publishing", "code app readiness".
---

# Power Apps Code Apps RPI

Microsoft's code-apps plugin for GitHub Copilot scaffolds a code app, adds data sources and deploys it. hve-core supplies the Research, Plan, Implement, Review workflow and is deliberately platform-neutral. This skill sits between them. Research works out whether a code app is the right shape at all and what the environment, licensing, data and governance will allow, recording evidence for each answer; if the answer is no, it stops there. The plan it then writes stays inside the platform's limits, the build is handed to the official plugin or the `pa` CLI, and the review looks for the problems that don't surface until after publishing. Every phase writes its artifact under `.copilot-tracking/` in hve-core's folder layout, file naming and markers, so a team that adopts hve-core later finds its tracking files where hve-core expects them.

## Before Starting

**Critical**: Gather the following before proceeding. Only inputs 1 and 2 must come from the user:

1. **What the app does and for whom** — the business outcome, the user population and its size, and whether users are employees, guests, or external customers. Required; ask if missing.
2. **Data and systems** — which Dataverse tables, connectors, SQL databases, SharePoint lists, Power Automate flows or Dataverse actions the app needs. Required; ask if missing.
3. **Phase to run** — `research` (default when no artifact exists), `plan`, `implement`, `review`, or `full`. When a research or plan artifact for the task already exists under `.copilot-tracking/`, default to the next phase. `full` runs Research, Plan, Implement and Review in sequence, still stopping after Research when the shape is wrong and at every confirmation gate.
4. **Target environment** — environment ID or URL. Defaults to the `environmentId` in `power.config.json` if the project is initialized; otherwise ask, or read it from the make.powerapps.com URL.
5. **Application lifecycle management (ALM) intent** — personal connections for a prototype, or a solution with connection references for Dev, Test and Prod. Defaults to solution-aware when the audience exceeds a team or the app touches Dataverse.
6. **Non-functional needs** — offline use, external access, IP restrictions, data residency, accessibility level, expected record volumes. Defaults to none stated, and the research phase asks about each.
7. **Tooling present** — whether hve-core, the official `code-apps` plugin from microsoft/power-platform-skills, and the `pa` CLI are installed. Detect the CLI with `pa --version`; hve-core by the `/rpi-research` command or the installed extension or Copilot CLI plugin; the plugin by its installed `code-apps-preview` plugin files or the `/create-code-app` command. The plugin's install commands are documented for the GitHub Copilot CLI; Visual Studio Code installs agent plugins through its own settings, and this plugin isn't documented for that path, so don't rely on the slash command alone. Never assume.
8. **Task slug** — lower-kebab-case name for the tracking artifacts. Default to a slug of the app name.

If the user doesn't provide all details upfront, ask for the missing ones before proceeding. Here that means inputs 1 and 2. Detect or default 3 to 8 and list each under **Assumptions** at the top of the research artifact, marked detected or default.

## Output Structure

Each phase writes one artifact and returns a short response that leads with the verdict and links the artifact.

```
.copilot-tracking/
├── research/{YYYY-MM-DD}/{slug}-research.md     # Research: fit, prerequisites, evidence, decisions, readiness
├── plans/{YYYY-MM-DD}/{slug}-plan.md            # Plan: task ID, P01..Pnn phases, Pxx-Txx tasks, risks
├── reviews/plans/{YYYY-MM-DD}/{slug}-plan-critique.md  # Plan critique: PC-xxx findings and disposition
├── changes/{YYYY-MM-DD}/{slug}-changes.md       # Implement: what was done per task, commands run, outputs
└── reviews/logs/{YYYY-MM-DD}/{slug}-review.md   # Review: RV-xxx findings, severity, route, outcome
```

Every tracking file starts with `<!-- markdownlint-disable-file -->`. Research and review files use plain workspace-relative paths; plans and changes records use backticks for commands and Markdown links for existing files. Phases use `<!-- rpi:phase id=P01 -->` before each phase heading and `<!-- rpi:task id=P01-T01 -->` before each task heading; critique findings use `<!-- rpi:critique id=PC-001 -->` and review findings `<!-- rpi:review id=RV-001 -->` before each finding heading. `PC-xxx` IDs appear only in the plan critique and `RV-xxx` IDs only in the review log. The evidence IDs (`E01`, `E02`, ...) and the check questions below are this skill's own vocabulary, layered on hve-core's layout.

Chat response per phase:

```markdown
## {Phase}: {app name}

{One paragraph: the verdict in plain language.}

{Optional: for Research, a checks table (Check, Result, Evidence) followed by the Planning Readiness line; for Review, a findings table (Area, Result, Finding) followed by the Execution and Outcome line.}

| Artifact | Description |
|----------|-------------|
| .copilot-tracking/{path} | {what it holds} |

## Next Steps
{The single next command or decision.}
```

## Step 1: Research fit and prerequisites

Write the research artifact, opening with the Assumptions list. Gather evidence with the `pa` CLI and the official documentation; record each finding with a source and an evidence ID (`E01`, `E02`, ...). Where a check cannot run, record it as an open question with who can answer it.

Answer these questions, in this order:

1. **Is a code app the right shape?** A code app is a single-page application in React, Vue or another JavaScript or TypeScript framework, hosted by Power Apps, with Microsoft Entra authentication and access to Power Platform connectors from code. It fits when the team is pro-code, the UI or logic exceeds what canvas offers, and users are inside the tenant or Microsoft Entra B2B guests. Recommend another shape when the evidence says so:
   - Offline or device-native needs: code apps aren't supported in Power Apps for Windows and have no documented offline capability; look at a mobile app or canvas with offline profiles.
   - Anonymous or external customers: Power Pages.
   - Mostly forms over Dataverse with standard UX: model-driven.
   - Embedding inside canvas apps: a Power Apps component framework (PCF) control.
   - Requirements that hinge on Power BI data integration, SharePoint forms integration, Power Platform Git integration, or Secure Implicit Connections: none of these are supported by code apps, so keep that part in the native product. Embedding a code app in a Power BI report through the Power Apps visual does work.
2. **Is the environment ready?** Code apps must be enabled per environment in the Power Platform admin center under Settings, Product, Features. Dataverse data needs a Dataverse environment. Record the environment ID and whether the user has maker permissions.
3. **Are users licensed?** End users need Power Apps Premium, pay-as-you-go, an App Pass, or auto-claim. Multiply by the audience size and record it under Decisions as a cost item with a procurement owner.
4. **Is the toolchain current?** The npm-based Power Apps CLI (`pa`, from `@microsoft/power-apps-cli`, with the `@microsoft/power-apps` client library) supersedes the `pac code` commands, which Microsoft has announced will be deprecated. Check `node --version` (22 or later, required by the CLI and the official plugin), `pa --version`, and `pa auth status`.
5. **Can the data be reached?** For each data need:
   - Native Dataverse: `pa app add data-source --connector dataverse --table <logical-name>`, one table per command. It uses no connection, connection reference or dataset; solution-awareness comes from `pa app push --solution-id`. Supported: CRUD, delegated `Filter`, `Sort`, `Top`, paging, formatted option-set values, image and file upload and download (preview). Not supported: polymorphic lookups, FetchXML, alternate keys, metadata CRUD. Lookups need the single-valued navigation property pattern.
   - Connectors: `pa connector list --search <term>` to confirm availability, `pa connection list` (or the plugin's `/list-connections`) for existing connections. Connector-backed sources are the ones that take a connection ID or, when solution-aware, a connection reference. Excel Online (Business) and Excel Online (OneDrive) aren't supported, even though the plugin ships an `/add-excel` skill. SharePoint and SQL support both tables and actions (`--as table` or `--as action`).
   - Dataverse actions and functions: `pa app find-dataverse-api --search <name>`.
   - Flows: `pa app list-flows`; only solution-aware instant flows with the Power Apps trigger are supported, and the person adding a flow must have access to it and its connections.
   - Solution-aware ALM: `pa solution list` for the target solution, and `pa connection list-references --solution-id <id>` to confirm connection references exist for each connector-backed source.
6. **What will governance do at runtime?** Data loss prevention (DLP) policies are enforced at app launch, so every connector must be in the environment's allowed group. Sharing follows canvas app limits, and sharing limits and per-app Conditional Access are Managed Environments features. Users see a consent dialog for connector permissions unless admin consent suppression is configured. Compiled assets are served from a public endpoint with no IP restriction; location or IP control is Conditional Access only. Record each as a finding, and flag anything that needs an admin.
7. **What could stop the plan?** List the unsupported features the requirements touch, the admin actions needed, and the decisions still open with the user.

End the artifact with:

- **Decisions**: confirmed and unresolved, each naming an owner.
- **Planning Readiness**: `Ready`, `Not ready`, `Not applicable`, or `Blocked`, as hve-core defines them. Unresolved decisions that don't block planning stay listed under Decisions and become risk rows in the plan.
- **Recommended shape**: code app, or the alternative, with the evidence IDs that drove it.

If the verdict is "not a code app", stop after Research and say so. Don't go on to plan an app that shouldn't be built this way. For any other result that isn't `Ready`, report the blockers and their owners in the chat response and stop.

## Step 2: Plan with the platform's limits built in

Write the plan only when Planning Readiness is `Ready`. Give it a stable task ID, an executive summary, a risks table, and phases with tasks. Each task carries `Goals:`, `Requirements:`, `Details:`, `References:` and `Dependencies:`.

Default phase structure, adjusted to the research:

- **P01 Foundation**: scaffold from an official template (`npx degit microsoft/PowerAppsCodeApps/templates/vite {folder}` or `templates/starter`), `npm install`, `pa app init --display-name "{name}" --environment-id {id}`, verify `power.config.json`, first `npm run build` and `pa app push` to prove the pipeline. When the official plugin is installed, the task says `/create-code-app` and lets it own the scaffold; note that it scaffolds the `vite` template, so a team that wants `starter` degits it by hand and then runs `pa app init`.
- **P02 Data**: one task per data source with the exact command or plugin skill: `/add-dataverse`, `/add-sharepoint`, `/add-office365`, `/add-teams`, `/add-onedrive`, `/add-azuredevops`, `/add-connector`, `/add-datasource`, or `pa app add data-source ...`. Connector-backed sources take `--connection-ref` and `--solution-id` when solution-aware; native Dataverse tables take only `--table`. Include `pa app add flow --flow-id` and `pa app add dataverse-api --api-name` tasks when research found them.
- **P03 Features**: screens and logic, using the generated services under `src/generated/services`. Every retrieval uses `select`; lists use `top` and paging; updates send only changed properties; creates omit system-managed columns.
- **P04 Hardening**: error handling around every service call, the app version visible in the UI and incremented per deploy, header decision via `pa app set-setting --show-header`, no secrets or personal data in source or bundle, accessibility pass.
- **P05 Publish and share**: `npm run build`, then `pa app push --solution-id {id}` when solution-aware (or the plugin's `/deploy`), `pa app share --principal {user emails or object IDs} --access play` for individual users and service principals, group sharing in make.powerapps.com, smoke test in the same browser profile as the tenant, Conditional Access and DLP confirmation with the admin.

Add a **Risks** row for each unresolved decision and each unsupported feature the requirements brush against. Write each task's `Requirements:` block so the review can test it, including the hardening items; hve-core treats `Requirements:` as the checkable record and doesn't want separate acceptance blocks.

Critique: when hve-core is installed, `/rpi-plan` runs the critique by default and `/rpi-plan-critique` runs it on demand. The `PC-xxx` findings live in `reviews/plans/{YYYY-MM-DD}/{slug}-plan-critique.md`; the plan carries only the Critique Disposition. Otherwise, run the self-critique below, record it as `self-critique` in the disposition, and write any findings to the same critique file:

- Does every data source task name the command and the connection strategy?
- Is any task relying on a feature research marked unsupported?
- Is licensing or an admin action on the critical path without an owner?
- Can every `Requirements:` line be checked by reading the repository or running a command?

## Step 3: Implement by delegation

This skill only runs the plan's tasks in order, keeps the changes record and stops at each confirmation gate; the official plugin and the `pa` CLI do the actual work.

1. For each task, run the named plugin skill or command, or ask the user to run it when a browser sign-in or admin step is involved.
2. After each task, append to the changes record: task ID, what changed, commands run, notable output, deviations from the plan and why.
3. Verify `power.config.json` after init and after every data source change. Run `pa app refresh data-source --name {name}` when a schema changed.
4. Never run `pa app push` or `pa app share` without the user's explicit confirmation in that turn. Say which environment and solution the push targets first.
5. If a task fails, record the exact output, stop that task, and ask. Don't retry silently or improvise around the CLI.

When neither the plugin nor `pa` is available, write the commands into the changes record as "to run" and stop; don't fabricate results.

## Step 4: Review before publishing

Compare the plan, the changes record and the repository. Record findings as `RV-001`, `RV-002`, ... with severity, evidence location, and a route: `rpi-implement` for defects, `rpi-plan` for decision gaps, `rpi-research` for evidence gaps, `follow-up` for residual work. Keep execution status (`Complete`, `Partial`, `Blocked`) separate from outcome (`Conformant`, `Conformant with justified divergence`, `Defects found`, `Residual work`, `Not accepted`).

Check these areas:

| Area | What to look for | Default severity |
|------|------------------|------------------|
| Public bundle | Secrets, tokens, connection strings, personal data, or internal URLs in `src/` or `dist/`; anything that relies on the asset endpoint being private | Critical |
| Data access | `getAll` without `select`; unbounded lists without `top` or paging; `update` sending unchanged fields; `create` including system-managed columns | High |
| Unsupported features | Code or plan depending on FetchXML, alternate keys, polymorphic lookups, Excel connectors, offline use (no documented capability), Power Apps for Windows, Secure Implicit Connections, non-instant or non-solution-aware flows, Power BI integration, SharePoint forms | High |
| ALM | Personal connection IDs on connector-backed sources where connection references were planned; `environmentId` in `power.config.json` not matching the target; push without `--solution-id` when solution-aware; stale generated services | High |
| Governance | A connector not in the DLP allowed group; licensing not confirmed for the audience; IP restriction expected without Conditional Access; sharing beyond the intended principals | High |
| Operations | No error handling around service calls; app version not shown or not incremented; header decision not made; no note for developers that Chrome and Edge may prompt for local network access when the hosted app calls `localhost` during `pa app run` | Medium |
| Accessibility | Keyboard and screen-reader basics in custom components; contrast in the chosen theme | Medium |

Walk the user through each finding with the suggested route. Close with the outcome and the next command.

## Step 5: Follow-up

Write follow-ups into the review log's residual work section, ranked by impact, each with the phase to re-enter and the artifact it starts from. Typical follow-ups: an admin action still pending, a licensing decision, a connection reference to create, an accessibility pass, a Conditional Access policy.

## Rules

- **Never invent environment IDs, connection IDs, solution IDs, table names, flow IDs or connector identifiers.** Read them from the CLI, the repository or the user. Placeholders are written as `{placeholder}` and listed as open items.
- **Never run `pa app push`, `pa app share`, or any command that changes a Power Platform environment without explicit confirmation in the same turn.**
- **Never put secrets, tokens or personal data in source, configuration or the bundle.** Assets are served from a public endpoint. Anything sensitive has to come through a data source the signed-in user is authorized for.
- **Let the official plugin do the build when it's installed.** Don't restate its steps; name the skill and let it run. When it isn't installed, use the documented `pa` commands.
- **Prefer connection references and a solution** for anything that will leave a developer's environment. Say so when the user chooses otherwise.
- **Write every phase artifact in hve-core's layout and location**, even when hve-core isn't installed, so hve-core can read them if it's installed later.
- **Stop after Research when the shape is wrong.** Recommend the alternative and leave it there; don't plan the code app anyway.
- **State the tooling date.** This skill reflects the code apps platform and the `pa` CLI as of October 2026. If a command fails because the CLI changed, read `pa --help` and the current reference, and tell the user what changed.
- **Don't modify the user's code during Review.** Report findings and routes; fixes happen in `rpi-implement`.

## Example

**Input:**

> Plan a code app for our 300 field technicians to log equipment inspections. Inspections and equipment are Dataverse tables, photos must be attached, and some sites have no mobile coverage.

**Research (abridged):**

- E01 Environment `contoso-dev`: code apps enabled (admin confirmed, Power Platform admin center screenshot). Dataverse present.
- E02 Licensing: 300 users, Power Apps Premium required for each or pay-as-you-go. Open: procurement owner.
- E03 `pa --version` 1.x, Node 22.11, `pa auth status` active account in tenant.
- E04 Tables `cr7a2_inspection`, `cr7a2_equipment` exist; inspection has a lookup to equipment (single-valued navigation property pattern applies). Photos: Dataverse image and file upload and download are in preview.
- E05 "Some sites have no mobile coverage": code apps have no documented offline capability and aren't supported in Power Apps for Windows.
- Decision: offline is a hard requirement for 40 of 300 users (user confirmed).
- Planning Readiness: `Not ready` for a code app as specified.
- Recommended shape: canvas or mobile app with an offline profile for the field capture; a code app remains a fit for the back-office review and reporting screens, which have connectivity. Offer to re-run research for that narrower scope.

**Chat response:**

```markdown
## Research: Inspection logging

A code app is the wrong shape for the field capture: forty technicians work without coverage and code apps have no documented offline capability (E05). It is a good fit for the back-office review screens. Licensing for 300 Premium users needs an owner (E02).

| Artifact | Description |
|----------|-------------|
| .copilot-tracking/research/2026-10-23/inspection-logging-research.md | Fit, prerequisites, evidence E01 to E05, decisions, readiness |

## Next Steps
Confirm whether to re-scope to the back-office app. If yes, I'll re-run research for that scope and move to Plan.
```

**Plan for the re-scoped back-office app (abridged):**

- P01 Foundation: `/create-code-app` (vite template), environment `contoso-dev`, first push to prove the pipeline.
- P02 Data: `/add-dataverse` for `cr7a2_inspection` and `cr7a2_equipment`; native Dataverse, so no connection reference. Solution `ContosoInspections` ID recorded from `pa solution list` for the push.
- P03 Features: inspection list with `select`, `top: 50` and paging; detail view with lookup resolved via the navigation property; photo viewer using the generated file download.
- P04 Hardening: error boundaries, version label, header hidden via `pa app set-setting --show-header false`, no tenant URLs in source.
- P05 Publish: `pa app push --solution-id {id}`, `pa app share --principal {reviewer emails} --access play`, group sharing finished in make.powerapps.com.
- Risks: R1 licensing owner unassigned; R2 image and file download is preview.
- Critique: PC-001 (Medium) in `reviews/plans/2026-10-23/inspection-review-plan-critique.md` added paging to P03-T01. Disposition: addressed.

**Review (abridged):**

- RV-001 [High] `InspectionsService.getAll()` called without `select` in `src/pages/List.tsx`. Route: rpi-implement.
- RV-002 [Medium] App version label present but not incremented since first push. Route: rpi-implement.
- Execution: Complete. Outcome: Defects found.

## Validation Checklist

Before finalizing any phase, verify:

- [ ] Inputs 1 and 2 came from the user; detected and defaulted inputs are listed under Assumptions in the research artifact
- [ ] Every finding in Research has an evidence ID and a source, or is an open question with an owner
- [ ] The shape recommendation cites the evidence that drove it, and research stops there when the shape is wrong
- [ ] Every plan task names the plugin skill or `pa` command, and no task depends on an unsupported feature
- [ ] Licensing, admin actions and connection references each have an owner or a risk row
- [ ] No environment-changing command ran without confirmation in that turn
- [ ] Review findings carry severity, evidence location and a route; the user's code was not modified
- [ ] Artifacts are under `.copilot-tracking/` with the markdownlint comment, markers and naming hve-core expects; `PC-xxx` only in the critique file, `RV-xxx` only in the review log

## References

- [Power Apps code apps overview](https://learn.microsoft.com/power-apps/developer/code-apps/overview)
- [Code apps architecture](https://learn.microsoft.com/power-apps/developer/code-apps/architecture)
- [Power Apps CLI command reference](https://learn.microsoft.com/power-apps/developer/code-apps/reference/cli)
- [Connect your code app to data](https://learn.microsoft.com/power-apps/developer/code-apps/how-to/connect-to-data)
- [Connect your code app to Dataverse](https://learn.microsoft.com/power-apps/developer/code-apps/how-to/connect-to-dataverse)
- [Code apps system configuration](https://learn.microsoft.com/power-apps/developer/code-apps/system-limits-configuration)
- [microsoft/PowerAppsCodeApps templates and samples](https://github.com/microsoft/PowerAppsCodeApps)
- [microsoft/power-platform-skills code-apps plugin](https://github.com/microsoft/power-platform-skills/tree/main/plugins/code-apps)
- [microsoft/hve-core](https://github.com/microsoft/hve-core) and its [copilot-tracking conventions](https://github.com/microsoft/hve-core/blob/main/.github/instructions/hve-core/copilot-tracking.instructions.md)
- [Add flows to your code app](https://learn.microsoft.com/power-apps/developer/code-apps/how-to/add-flows)

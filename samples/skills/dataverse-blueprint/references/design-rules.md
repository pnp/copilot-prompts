# Design Rules

Architectural judgment the model applies while writing the blueprint. The validator enforces what can be checked mechanically (see [rule-catalog.md](./rule-catalog.md)); the rest is on the designer.

## Tables

- **Reuse standard tables** (`account`, `contact`, `systemuser`, `team`, `businessunit`, `task`, `email`, `annotation`) whenever their semantics fit. Never create `prefix_Customer` when `account` fits.
- **Type**: Standard by default. Activity only for interactions with start/end that belong in timelines. Elastic only for very high-volume append-mostly data. Virtual only when data must stay in the external system.
- **Ownership**: user/team-owned whenever access differs by owner or business unit; organization-owned only for reference/catalog data. It cannot be changed after creation, and organization-owned tables only accept None or Organization privilege depth.
- **Primary name**: a meaningful human-readable value; when none exists, an autonumber (`INS-{SEQNUM:6}`).
- **Auditing**: on for compliance, financial, approval or personal data.
- Prefer File / Image columns to notes attachments for typed documents.

## Columns

| Need | Use | Avoid |
|---|---|---|
| Fixed list maintained by IT | Choice (global when used by 2+ tables) | Text with "allowed values" |
| List maintained by business users or with attributes | Lookup to an org-owned catalog table | A choice that changes every month |
| Multi-select only for filtering | Choices | Choices when you need reporting per value → N:N or child table |
| Money | Currency (adds base-currency column, needs `transactioncurrency`) | Decimal |
| Calendar dates (birth, due) | Date only, behavior **Date Only** | Date and time User Local (off-by-one across time zones) |
| Event timestamps | Date and time, **User Local** | Text |
| Derived values | Formula column (Power Fx). Pair User Local columns with `Now()`/`Today()`; Date Only / TZI with `UTCNow()`/`UTCToday()` | Legacy calculated columns, nightly flows |
| Aggregates from children | Rollup (async) or Power BI | Plugins only for counts |
| Sequential human IDs | Autonumber | Flows computing "max + 1" |
| Yes/No | Yes/No with explicit default | Choice with two values |

- Design **Status Reason** values for the real lifecycle; don't leave Active/Inactive when the process has more states.
- **Required** only when the process truly cannot continue without the value; conditional requirements belong in business rules.
- Flag personal or sensitive data (`pii: true`): national IDs, health, salary, minors' data.
- Realistic text lengths (100 for names; 4000 only when needed; memo beyond).

## Relationships

- **Parental** only when the child has no meaning without the parent. A table can be the child in only one parental relationship.
- **Restrict delete** for master data that must not disappear while referenced.
- **Referential** (remove link) for optional associations; always for links to `systemuser` / `contact` / `account`.
- **Custom** only with each cascade (Assign, Delete, Merge, Reparent, Share, Unshare) documented.
- Native **N:N** only for pure associations; if the association carries data (date, role, quantity) create an explicit intersect table with two lookups.
- Avoid polymorphic lookups and circular cascades unless strictly required — explain them if used.

## Integration

- Every synced/imported table gets an **alternate key** on the external ID; the index builds asynchronously and must be **Active** before the first upsert.
- Upsert through the Web API / Power Automate with the key, not "list rows + condition + create/update".
- For Fabric / Power BI, state whether Link to Microsoft Fabric (Synapse Link) is recommended and for which tables.

## Security

- Least privilege; one role per persona; never "everyone gets System Customizer".
- Depth matches segregation: U own records · B my business unit · P my unit and below · O everyone.
- Setting a lookup needs **Append** on the child and **AppendTo** on the parent.
- Grant roles to owner teams or Microsoft Entra ID group teams, not user by user.
- PII columns go to a column security profile with explicit read / create / update.
- Power Pages users are governed by table permissions and web roles, not security roles.

## ALM

- Unmanaged solution in development under the custom publisher; managed in test/production.
- Environment variables for anything that changes per environment (URLs, emails, IDs); connection references for every connector.
- Source control with `pac solution export` + `pac solution unpack`, or Git integration in Power Platform — and the blueprint lives in the same repository.
- Add only the standard-table components you need to the solution, never "include all objects".

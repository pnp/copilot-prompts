# Rule Catalog

`dvbp validate` checks these rules. Score = 100 − 12 × errors − 3 × warnings (A ≥ 90, B ≥ 80, C ≥ 70, D ≥ 50, F < 50). `info` findings don't affect the score — they are assumptions to confirm with the business. Exit code is 1 when there is at least one error.

| Rule | Severity | What it checks |
|---|---|---|
| DV001 | error | Default or placeholder publisher prefix (new, cr###) used in a production design |
| DV002 | error | Publisher prefix must be 2-8 lowercase alphanumerics starting with a letter |
| DV003 | error | Schema name must be <prefix>_PascalCase, ASCII, no spaces or accents |
| DV004 | warning | Table schema name looks plural; Dataverse table names are singular |
| DV005 | error | Custom table duplicates a standard table (reuse account/contact/systemuser/team/businessunit) |
| DV006 | error | Table ownership must be explicit (user or organization) - it cannot be changed after creation |
| DV007 | error | Table needs a meaningful primary name column (text or autonumber) |
| DV008 | error | Date column needs an explicit behavior (dateonly, userlocal, tzi) |
| DV009 | warning | Two-option yes/no choice should be a Yes/No (bool) column |
| DV010 | error | Column references a choice that is not defined |
| DV011 | error | A table can be the child in only one Parental relationship |
| DV012 | error | Relationship or key references an unknown table or column |
| DV013 | error | Integrated table has no alternate key for upsert |
| DV014 | error | PII column is not secured by a column security profile |
| DV015 | error | Formula mixes date behaviors (userlocal pairs with Now()/Today(); dateonly/tzi with UTCNow()/UTCToday()) |
| DV016 | error | Text column max length must be 1..4000 (use memo for longer content) |
| DV017 | warning | Role can set a lookup but lacks Append on the child or AppendTo on the parent |
| DV018 | error | Persona has no security role |
| DV019 | warning | Element has no traceability (source: process | assumed) |
| DV020 | warning | Legacy calculated column in a new design - use a formula column |
| DV021 | warning | Monetary-looking column is not of type currency |
| DV022 | warning | Organization-wide Delete granted to a non-admin role |
| DV023 | error | Organization-owned table only supports None or Organization privilege depth |
| DV024 | error | N:N relationship with attributes must be an explicit intersect table |
| DV025 | error | Duplicate schema name |
| DV026 | warning | Lookup column schema name should end with 'Id' |
| DV027 | error | Unknown column type |
| DV028 | warning | Role grants access to a table that is not in the blueprint |
| DV029 | info | Assumption to confirm with the business before building |
| DV030 | warning | Table with approvals/compliance data should have auditing enabled |

## How to fix the ones that hurt most

- **DV005 duplicate standard table** — delete the custom table; use `systemuser` (employees), `contact` (external people), `account` (companies), `team`, `businessunit`. Migrate data with an upsert on email / tax ID.
- **DV006 / DV023 ownership** — ownership cannot change in place. Create a new user-owned table, copy data, repoint lookups, retire the old one.
- **DV008 date behavior** — Date Only for calendar dates, User Local for event timestamps, Time-Zone Independent for values that must read the same everywhere (check-in times). Changing User Local → Date Only on existing data requires a conversion job (`ConvertDateAndTimeBehavior`).
- **DV011 two parental parents** — keep parental to the parent that owns the lifecycle; make the other referential.
- **DV013 no alternate key** — add a key on the external ID; wait for index status Active; switch integration to upsert.
- **DV014 PII without column security** — add the column to a column security profile and grant it to an Entra ID group team.
- **DV015 formula date pairing** — mixing behaviors makes `DateDiff` silently off by the user's UTC offset.
- **DV017 Append/AppendTo** — without both, users get "insufficient permissions" the first time they set the lookup.

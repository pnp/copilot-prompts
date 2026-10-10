# Validation evidence

Read-only tests ran on October 6, 2026; authorized synthetic-record tests ran on October 9, 2026 (Pacific time). Tenant details, record identifiers, and row values are omitted.

| Check | Observed result | Scope |
| --- | --- | --- |
| Metadata | Pass | Account/contact keys, required columns, relationship direction, and active state confirmed |
| Active accounts | Pass | 10 FetchXML IDs matched independent OData results in server order |
| Outer join | Pass for zero-match case | All 8 sampled parent rows retained; no primary contacts in sample |
| No related contacts | Pass for zero-match case | All 8 sampled parents independently verified to have no contacts |
| Aggregate | Pass for zero counts | 8 grouped contact counts matched independent queries |
| Paging | Pass | Two pages of 2 rows matched one ordered 4-row query; server cookie used |
| Literal escaping | Server accepted | Ampersand/apostrophe literal parsed and executed; no matching fixture |
| Positive relationship discovery | Coverage limit | No visible primary-contact or related-contact matches found |

## Synthetic-record tests — October 9, 2026

With explicit user authorization, three temporary account records and two temporary contact records were created in existing tables. One account had two related contacts and one primary contact; two accounts had no contacts. No tables, columns, relationships, or other configuration were created or modified. Existing business records were not modified.

| Test | Result | Evidence |
| --- | --- | --- |
| positive-primary-contact | PASS | One primary-contact match and two unmatched parents retained. |
| one-to-many-cardinality | PASS | Two children yield two rows for the same parent. |
| anti-join-mixed-population | PASS | Only the two accounts without contacts returned. |
| aggregate-known-counts | PASS | Counts exactly match the synthetic fixture: 2, 0, 0. |
| existence-no-duplicates | PASS | Existence query returns the parent once despite two children. |
| escaping-known-match | PASS | Ampersand/apostrophe literal matched the intended synthetic account. |
| cleanup | PASS | All five synthetic record URLs returned 404 after deletion. No schema requests were issued. |

Cleanup deleted the two contacts and three accounts after clearing the synthetic primary-contact reference. GET requests for all five record IDs returned HTTP 404. The private cleanup ledger was removed only after successful verification. Tokens and record IDs are excluded from this contribution.

## Scope and limitations

- GitHub Copilot installation and automatic skill activation are not established by these query tests.
- The sample PNG is a browser capture of the worked query and recorded validation report; it does not represent a GitHub Copilot runtime session.

The tests validate generated query behavior, not every possible query the skill might produce. Empty results were not treated as proof of positive-case semantics.

# Blueprint Specification (v1)

A blueprint is a YAML (or JSON) file describing one Dataverse solution's data model. It is the only file humans edit; the design document and deployment plan are generated from it.

```yaml
blueprint: 1                 # spec version
language: 1033               # LCID for display names (3082 = Spanish)

solution:  { name: EhsInspections, display_name: EHS Inspections, version: 1.0.0.0 }
publisher: { name: contosoehs, display_name: Contoso EHS, prefix: cnt, option_value_prefix: 10000 }

summary: >                   # 3-5 lines, copied into the design document
assumptions:    [ ... ]      # rendered as [ASSUMED]
open_questions: [ ... ]      # rendered as [DECIDE]

personas:                    # every persona needs a security role (DV018)
  - { id: inspector, name: Safety Inspector }

choices:                     # global choices; values = option_value_prefix * 10000 + index
  - name: cnt_risklevel      # lowercase prefix_name
    display_name: Risk level
    source: process          # process | assumed
    options: [Low, Medium, High]          # or [{label: Low, value: 100000000}, ...]

tables:
  - schema: cnt_Inspection   # prefix_PascalCaseSingular
    display: Inspection
    plural: Inspections
    purpose: Monthly inspection header
    ownership: user          # user | organization  (cannot be changed later)
    type: standard           # standard | activity | elastic
    audit: true
    volume: "~1,200"         # per year, free text
    integrated: false        # true → needs keys[] (DV013)
    source: process
    timeline: false          # HasActivities
    notes_enabled: false     # HasNotes
    status_reasons: [Planned, In progress, Closed]   # manual step in the plan
    primary: { schema: cnt_Code, display: Code, autonumber: "INS-{SEQNUM:6}" }   # or max_length: 100
    columns:
      - schema: cnt_InspectionDate
        display: Inspection date
        type: date           # see column types
        behavior: dateonly   # dateonly | userlocal | tzi  (required for date/datetime)
        required: true
        searchable: true
        pii: false           # true → must be in a column profile (DV014), deployed with IsSecured
        source: process
        notes: free text
    keys:
      - { schema: cnt_ErpCodeKey, columns: [cnt_ErpCode], why: nightly upsert }

relationships:
  - schema: cnt_Inspection_Finding        # prefix_Parent_Child[_Role]
    parent: cnt_Inspection                # custom table schema or standard logical name
    child: cnt_Finding
    lookup: cnt_InspectionId              # lookup column created on the child
    lookup_display: Inspection
    behavior: parental                    # parental | referential | restrict | custom
    cascade: { Assign: NoCascade, ... }   # only for custom
    required: true
    source: process
  - { schema: cnt_Finding_Tag, type: "N:N", tables: [cnt_Finding, cnt_Tag], source: process }

security:
  roles:
    - name: Safety Inspector
      persona: inspector
      privileges:                         # table → privilege → depth
        cnt_Inspection: { create: U, read: B, write: U, append: B, appendto: B }
        # privileges: create read write delete append appendto assign share
        # depths: "-" none · U user · B business unit · P parent:child BU · O organization
  column_profiles:
    - name: Contractor PII
      columns: [cnt_CorrectiveAction.cnt_ContractorNationalId]
      read: true
      create: true
      update: false
      granted_to: [Safety Director team]
  notes: [ ... ]

alm:
  environment_variables: [cnt_ErpBaseUrl]
  connection_references: [cnt_ErpConnection]
  notes: [ ... ]
  manual_steps: [ ... ]                   # appended to the plan as ✋ steps

anti_patterns_avoided: [ ... ]            # the "why" behind the design
```

## Column types

| `type` | Dataverse | Extra keys |
|---|---|---|
| `text` / `email` / `url` / `phone` | Single line of text (format) | `max_length` 1–4000 |
| `memo` | Multiple lines of text | `max_length` |
| `autonumber` | Text with AutoNumberFormat | `format: "ABC-{SEQNUM:6}"` |
| `whole` / `decimal` / `float` | Numbers | `min`, `max`, `precision` |
| `currency` | Currency | `min`, `max` |
| `bool` | Yes/No | `default`, `true_label`, `false_label` |
| `date` / `datetime` | Date only / Date and time | `behavior` (required) |
| `choice` / `choices` | Choice / multi-select | `choice: <global>` or local `options: [...]` |
| `file` / `image` | File / Image | `max_kb` (file) |
| `formula` | Power Fx formula (manual step) | `formula`, `returns` |
| `calculated` | Legacy calculated (flagged DV020) | — |

Lookup columns are not declared under `columns`; they come from `relationships[].lookup`.

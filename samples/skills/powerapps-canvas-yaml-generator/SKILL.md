---
name: powerapps-canvas-yaml-generator
description: Generates valid, importable Power Apps Source Code YAML for canvas app screens. Use when asked to create YAML, scaffold, or modify any Power Apps canvas app screen — including full screens, dialogs, forms, galleries, detail views, dashboards, or any layout container — or when asked to generate Power Fx formulas or produce Power Apps source code for import.
---

# Power Apps Canvas App YAML Generator

Generates production-ready Power Apps Source Code YAML for canvas app screens, following the official Power Apps YAML source format rules and a consistent enterprise design system.

---

## Before Starting

**Always confirm the following before generating any YAML:**

1. **Screen or component name** — what to name the output (e.g. `ScnDashboard`, `ScnRequestForm`, `DlgConfirmDelete`)
2. **Component type** — full screen, dialog/overlay, form, gallery list, detail view, dashboard, or other
3. **Navigation context** — if a sidebar is needed, which nav item should be active; if no sidebar is needed, say so
4. **Screen purpose** — one sentence describing what the screen or component does
5. **Data source** — SharePoint list, Dataverse table, or collection name and any known column names (if data-driven)
6. **Controls needed** — gallery, form fields, dropdowns, status badges, buttons, dialogs, etc.

If any detail is missing, ask before generating.

---

## Step 1: Confirm the Component Type

The component type determines the top-level YAML structure:

- **Full screens** → wrapped in `Screens:` block
- **Dialogs, popups, components, partial UI** → bare container tree, NO `Screens:` wrapper

| Type                            | Screens: wrapper? | When to use                                                            |
| ------------------------------- | ----------------- | ---------------------------------------------------------------------- |
| **Full screen with sidebar**    | YES               | A primary app screen with global navigation                            |
| **Full screen without sidebar** | YES               | A login, splash, or single-purpose screen                              |
| **Dialog / overlay / popup**    | NO                | A confirmation, quick-entry panel, or modal overlaid on another screen |
| **Reusable component / card**   | NO                | A panel, card, or UI fragment embedded within a screen                 |
| **Standalone form screen**      | YES               | A dedicated create or edit screen without a sidebar                    |
| **Gallery list screen**         | YES               | A searchable, filterable list of records                               |
| **Detail view screen**          | YES               | A read-only or editable single-record view                             |
| **Dashboard screen**            | YES               | A summary screen with KPI cards                                        |
| **Custom / other**              | Ask               | Describe it                                                            |

---

## Step 2: Design System

### Colours

| Token              | Value                       | Use                           |
| ------------------ | --------------------------- | ----------------------------- |
| Navy primary       | `RGBA(13, 44, 84, 1)`       | Sidebar fill, primary buttons |
| Navy dark hover    | `RGBA(8, 30, 60, 1)`        | Primary button hover          |
| Page background    | `RGBA(245, 246, 248, 1)`    | Main content area             |
| White              | `RGBA(255, 255, 255, 1)`    | Cards, panels, top bar        |
| Border             | `RGBA(226, 232, 240, 1)`    | Card borders, dividers        |
| Table header bg    | `RGBA(248, 250, 252, 1)`    | Gallery header row            |
| Text primary       | `RGBA(15, 23, 42, 1)`       | Page titles, headings         |
| Text secondary     | `RGBA(71, 85, 105, 1)`      | Body text                     |
| Text muted         | `RGBA(100, 116, 139, 1)`    | Breadcrumbs, subtitles        |
| Nav active fill    | `RGBA(255, 255, 255, 0.08)` | Active nav item background    |
| Nav inactive fill  | `RGBA(0, 0, 0, 0)`          | Inactive nav item background  |
| Nav label active   | `RGBA(255, 255, 255, 1)`    | Active nav label              |
| Nav label inactive | `RGBA(255, 255, 255, 0.65)` | Inactive nav label            |

### Status Badge Colours

| Category                      | Fill                     | Text                   |
| ----------------------------- | ------------------------ | ---------------------- |
| Available / Active / Success  | `RGBA(220, 252, 231, 1)` | `RGBA(22, 101, 52, 1)` |
| Assigned / In Progress / Info | `RGBA(219, 234, 254, 1)` | `RGBA(30, 64, 175, 1)` |
| Pending / Warning             | `RGBA(254, 243, 199, 1)` | `RGBA(146, 64, 14, 1)` |
| Error / Rejected / Urgent     | `RGBA(254, 226, 226, 1)` | `RGBA(185, 28, 28, 1)` |
| Inactive / Neutral / Closed   | `RGBA(241, 245, 249, 1)` | `RGBA(71, 85, 105, 1)` |

Apply the category that best matches the app's status vocabulary.

### Typography

Font-related properties for all classic controls: `Font`, `Size`, `FontWeight`. Note: `FontSize` does NOT exist — always use `Size`.

| Use                      | `Size` value | `FontWeight` value                             |
| ------------------------ | ------------ | ---------------------------------------------- |
| Page title               | `=28`        | `=FontWeight.Bold`                             |
| Panel / section title    | `=16`        | `=FontWeight.Semibold`                         |
| Body / button            | `=13`        | `=FontWeight.Normal` or `=FontWeight.Semibold` |
| Breadcrumb / small label | `=12`        | `=FontWeight.Normal`                           |
| Nav label                | `=11`        | `=FontWeight.Normal` or `=FontWeight.Semibold` |
| Table column header      | `=10`        | `=FontWeight.Semibold` (ALL CAPS text)         |

`Font`: always `=Font.'Segoe UI'`

### AutoLayout Container Properties

When using `Variant: AutoLayout`, apply these layout properties as needed:

| Property                                                        | Common values                                                                                    |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `LayoutDirection`                                               | `=LayoutDirection.Horizontal` or `=LayoutDirection.Vertical`                                     |
| `LayoutAlignItems`                                              | `=LayoutAlignItems.Center`, `=LayoutAlignItems.Stretch`, `=LayoutAlignItems.Start`               |
| `LayoutJustifyContent`                                          | `=LayoutJustifyContent.Start`, `=LayoutJustifyContent.SpaceBetween`, `=LayoutJustifyContent.End` |
| `LayoutGap`                                                     | `=8`, `=10`, `=12`, `=16`                                                                        |
| `LayoutMinHeight`                                               | `=16` (set on all AutoLayout containers)                                                         |
| `LayoutMinWidth`                                                | `=16` or a meaningful minimum e.g. `=100`, `=200`                                                |
| `LayoutMaxHeight`                                               | `=Self.AllItemsCount * Self.TemplateHeight` (galleries)                                          |
| `PaddingTop` / `PaddingBottom` / `PaddingLeft` / `PaddingRight` | `=8`, `=16`, `=20`, `=24`, `=32`                                                                 |
| `FillPortions`                                                  | `=0` when container has a fixed `Height` or `Width`; omit to flex-fill                           |
| `AlignInContainer`                                              | `=AlignInContainer.Start`, `=AlignInContainer.Center`, `=AlignInContainer.Stretch`               |
| `DropShadow`                                                    | `=DropShadow.None` (explicit no-shadow), `=DropShadow.Light`, `=DropShadow.Regular`              |

**Gallery-specific properties:**
| Property | Typical value |
|---|---|
| `TemplateSize` | `=45`, `=52`, `=60` (row height in px) |
| `TemplatePadding` | `=0` |
| `LayoutMinHeight` | `=45` or `=200` |
| `LayoutMaxHeight` | `=Self.AllItemsCount * Self.TemplateHeight` |
| `Height` | `=Self.AllItemsCount * Self.TemplateHeight` |

---

## Step 3: Power Apps YAML Syntax Rules

**All rules are absolute. Violating any one produces a PA1001 import error. Verify every rule before outputting.**

---

### RULE 0 — YAML indentation is mandatory and must be exact

**The single most common cause of import failure is missing or collapsed indentation.** YAML structure is defined entirely by indentation. If indentation is lost, every node appears at the wrong level and the parser rejects the file immediately.

**Output YAML inside a fenced code block** (` ```yaml `) so indentation is preserved exactly. Never output YAML as plain prose or a flat list.

The indentation contract for Power Apps Source Code YAML is **2 spaces per level**. Every level of nesting adds exactly 2 spaces. No tabs. No 4-space indents.

```
Screens:                          <- level 0, 0 spaces
  ScreenName:                     <- level 1, 2 spaces
    Fill: =RGBA(...)              <- level 2, 4 spaces
    Children:                     <- level 2, 4 spaces
      - ControlName:              <- level 3, 6 spaces (the - counts as part of indent)
          Control: ...            <- level 4, 10 spaces (4 spaces after the -)
          Variant: ...            <- level 4, 10 spaces
          Properties:             <- level 4, 10 spaces
            PropName: =value      <- level 5, 12 spaces
          Children:               <- level 4, 10 spaces
            - ChildName:          <- level 5, 14 spaces
                Control: ...      <- level 6, 16 spaces
                Properties:       <- level 6, 16 spaces
                  PropName: =val  <- level 7, 18 spaces
```

The rule for list items (controls inside `Children:`): the `- ControlName:` line is at the list level, and the control's body (`Control:`, `Variant:`, `Properties:`, `Children:`) is indented **4 more spaces** relative to the `-`.

**Wrong — no indentation (causes immediate PA1001):**

```
Screens:
DlgAreYouSure:
Fill: =RGBA(0, 0, 0, 0)
Children:
- conDialogBackdrop:
Control: GroupContainer@1.5.0
```

**Correct — proper 2-space indentation:**

```yaml
Screens:
  DlgAreYouSure:
    Fill: =RGBA(0, 0, 0, 0)
    Children:
      - conDialogBackdrop:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            Fill: =RGBA(0, 0, 0, 0.4)
```

---

### RULE 1 — Property values are NEVER quoted

The Source Code schema does not use quoted strings for property values. Quoting causes PA1001.

```yaml
# WRONG — quoted values, all cause import errors
Fill: "=RGBA(13, 44, 84, 1)"
Width: "=230"
Text: "=ThisItem.Title"
Variant: "AutoLayout"

# CORRECT — bare, unquoted
Fill: =RGBA(13, 44, 84, 1)
Width: =230
Text: =ThisItem.Title
Variant: AutoLayout
```

---

### RULE 2 — Every property value starts with =

Every value inside a `Properties:` block is a Power Fx expression and must start with `=`. No exceptions for any type.

| Type    | WRONG                         | CORRECT                        |
| ------- | ----------------------------- | ------------------------------ |
| String  | `Text: Hello`                 | `Text: ="Hello"`               |
| Number  | `Width: 230`                  | `Width: =230`                  |
| Boolean | `Visible: true`               | `Visible: =true`               |
| Colour  | `Fill: RGBA(13,44,84,1)`      | `Fill: =RGBA(13, 44, 84, 1)`   |
| Enum    | `FontWeight: FontWeight.Bold` | `FontWeight: =FontWeight.Bold` |
| Formula | `Height: Parent.Height`       | `Height: =Parent.Height`       |

The **only** values without `=` are the schema declaration keys — `Control:` and `Variant:` — which are type/schema keywords, not formulas.

---

### RULE 2b — Font size property is `Size:`, never `FontSize:`

The property name for font size on all classic controls (`Label@2.5.1`, `Classic/Button@2.2.0`, `Classic/TextInput@2.3.2`, `Classic/ComboBox@2.3.0`, etc.) is `Size`. The property `FontSize` does not exist and causes PA2108 on import.

```yaml
# WRONG — FontSize does not exist, causes PA2108
- lblTitle:
    Control: Label@2.5.1
    Properties:
      FontSize: =16 # INVALID property name

# CORRECT — use Size
- lblTitle:
    Control: Label@2.5.1
    Properties:
      Size: =16 # correct property name
      Font: =Font.'Segoe UI'
      FontWeight: =FontWeight.Semibold
      Color: =RGBA(15, 23, 42, 1)
```

This applies to every versioned classic control. `Font`, `FontWeight`, and `Size` are the three font-related properties.

---

### RULE 3 — Use `Control:` not `ControlType:`

`ControlType:` does not exist in the Source Code schema. Always use `Control:` with the full versioned type string.

```yaml
# WRONG — invalid key, and quoted
- conPanel:
    ControlType: "GroupContainer"

# CORRECT — correct key, unquoted, with version
- conPanel:
    Control: GroupContainer@1.5.0
```

---

### RULE 4 — `Variant:` is a sibling of `Control:`, never inside `Properties:`

```yaml
# WRONG
- conPanel:
    Control: GroupContainer@1.5.0
    Properties:
      Variant: AutoLayout # inside Properties is wrong

# CORRECT
- conPanel:
    Control: GroupContainer@1.5.0
    Variant: AutoLayout # sibling of Control, outside Properties
    Properties:
      LayoutDirection: =LayoutDirection.Vertical
```

---

### RULE 5 — Screen-level structure: `Properties:` + `Children:` as siblings

Screens support an **optional** `Properties:` block for screen-level properties, followed by `Children:` as a **sibling** — not nested inside `Properties:`.

Valid screen-level `Properties:` keys: `OnVisible`, `OnHidden`, `LoadingSpinnerColor`. That is all. `Fill`, `Height`, `Width`, and `DisplayName` are still NOT valid here.

`Children:` is always a direct sibling of `Properties:` under the screen name — never nested inside `Properties:`.

```yaml
# CORRECT — Properties: block with OnVisible, then Children: as sibling
Screens:
  ScnMyScreen:
    Properties:
      LoadingSpinnerColor: =RGBA(13, 44, 84, 1)
      OnVisible: |
        =ClearCollect(colItems, MyList);
        UpdateContext({locSearch: ""})
    Children:              <- sibling of Properties:, NOT inside it
      - conShell:
          Control: GroupContainer@1.5.0
          Variant: AutoLayout
          Properties:      <- this Properties: belongs to conShell, not the screen
            Fill: =RGBA(245, 246, 248, 1)
            Height: =Parent.Height
            Width: =Parent.Width
            ...

# ALSO CORRECT — no Properties: block at all (when no screen-level props needed)
Screens:
  ScnMyScreen:
    Children:
      - conShell:
          ...

# WRONG — Fill/Height/Width at screen level (still invalid)
Screens:
  ScnMyScreen:
    Properties:
      Fill: =RGBA(245, 246, 248, 1)   # INVALID screen property
      Height: =App.Height             # INVALID screen property
      Width: =App.Width               # INVALID screen property

# WRONG — Children: nested inside Properties: (structural error)
Screens:
  ScnMyScreen:
    Properties:
      OnVisible: |
        =UpdateContext({locSearch: ""})
      Children:            # WRONG — Children: must be a sibling, not inside Properties:
        - conShell:
```

### RULE 5b —### RULE 5b — Dialogs, popups, and components are NOT wrapped in `Screens:`

When the request is for a **dialog, popup, overlay, reusable component, or any partial UI** (not a full standalone screen), do NOT wrap it in a `Screens:` block. Output a bare container tree starting with a `- ContainerName:` list item.

**Wrong — dialog incorrectly wrapped in Screens:**

```yaml
Screens:
  DlgConfirm:
    Children:
      - conDialogBackdrop: ...
```

**Correct — dialog as a bare container tree (no Screens: wrapper):**

```yaml
- conDialogBackdrop:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      X: =0
      Y: =0
      Width: =Parent.Width
      Height: =Parent.Height
      Fill: =RGBA(0, 0, 0, 0.4)
      RadiusTopLeft: =0
      RadiusTopRight: =0
      RadiusBottomLeft: =0
      RadiusBottomRight: =0
    Children:
      - conDialogPanel:
          Control: GroupContainer@1.5.0
          Variant: AutoLayout
          Properties:
            X: =(Parent.Width - 480) / 2
            Y: =(Parent.Height - 240) / 2
            Width: =480
            FillPortions: =0
            Fill: =RGBA(255, 255, 255, 1)
            LayoutDirection: =LayoutDirection.Vertical
            LayoutGap: =16
            PaddingTop: =24
            PaddingBottom: =24
            PaddingLeft: =24
            PaddingRight: =24
            LayoutMinHeight: =16
            LayoutMinWidth: =16
            RadiusTopLeft: =12
            RadiusTopRight: =12
            RadiusBottomLeft: =12
            RadiusBottomRight: =12
```

**Use `Screens:` only when generating a full standalone app screen.**
Use a bare container tree for: dialogs, popups, overlays, reusable card components, form panels, and any partial UI meant to be embedded within an existing screen.

---

### RULE 6 — No `BorderRadius:` — use four `Radius*` properties

`BorderRadius` is not a valid property in the Source Code schema.

```yaml
# WRONG
BorderRadius: =6

# CORRECT — always all four, even if all the same value
RadiusTopLeft: =8
RadiusTopRight: =8
RadiusBottomLeft: =8
RadiusBottomRight: =8
```

Every `GroupContainer` must include all four radius properties. Use `=0` for square corners.

---

### RULE 7 — Multi-line formulas use block scalar; `=` goes inside the block

Two block scalar styles are used — pick based on content:

**`|-`** — for a **single expression** that spans multiple lines (no `;` between statements). The `|-` strips the trailing newline. Use for `Fill`, `Items`, `Color`, and any single multi-line formula:

```yaml
Fill: |-
  =If(
      locIsActive,
      RGBA(255, 255, 255, 0.08),
      RGBA(0, 0, 0, 0)
  )

Items: |-
  =AddColumns(
      Filter(MyList, Status = "Active"),
      "Extra", Value(ID)
  )
```

**`|`** — for **multiple statements** separated by `;`. Use for `OnSelect`, `OnVisible`, `OnHidden`:

```yaml
OnSelect: |
  =Set(gblSelectedItem, ThisItem);
  Navigate(ScnDetail);
  Set(gblMode, "Edit")

OnVisible: |
  =ClearCollect(colItems, MyList);
  UpdateContext({locSearch: ""})
```

Both `|` and `|-` are accepted by the parser for `OnSelect`/`OnVisible`. Either is valid:

```yaml
# Also valid — |- on multi-statement OnSelect
OnSelect: |-
  =Set(gblFrmMode, "New");
  Navigate(ScnDetail)
```

The `=` always goes on the **first line inside the block**, never on the key line itself.

---

### RULE 7b — Formulas containing `{` (record literals) must use block scalar

YAML treats `: ` (colon-space) as a mapping separator. Power Fx record literals like `{varName: value}` contain this pattern and will break inline parsing with "found invalid mapping".

**Any formula that contains `{` must use `|` or `|-` block scalar.**

Single-line formulas WITHOUT `{` are fine inline:

```yaml
# Fine inline — no { } present
OnSelect: =Navigate(ScnDetail)
OnSelect: =Back()
Items: =Filter('Software Assets', Status.Value = "Active")
Visible: =locDialogVisible
```

```yaml
# WRONG — colon inside {} breaks YAML parsing (PA1001 "invalid mapping")
OnSelect: =UpdateContext({locDialogResult: false, locDialogVisible: false})
OnSelect: =Patch('My List', Defaults('My List'), {Title: txtName.Text})
OnSelect: =Navigate(ScnHome, {locUser: varCurrentUser})

# CORRECT — use | block scalar whenever the formula contains `: `
OnSelect: |
  =UpdateContext({locDialogResult: false, locDialogVisible: false})

OnSelect: |
  =Patch('My List', Defaults('My List'), {Title: txtName.Text})

OnSelect: |
  =Navigate(ScnHome, {locUser: varCurrentUser})
```

This applies to **any property**, not just `OnSelect`:

```yaml
# WRONG — colon inside formula value
Items: =Filter(MyTable, {Status: "Active"})
Default: ={Value: "All"}

# CORRECT
Items: |
  =Filter(MyTable, {Status: "Active"})
Default: |
  ={Value: "All"}
```

**The safe rule: if the formula contains `{`, always use `|` block scalar.**

---

### RULE 8 — `ManualLayout` only for overlays and badges; `AutoLayout` for everything else

- **`Variant: ManualLayout`** — dialog backdrops, dialog panels that need explicit `X`/`Y`, status badges
- **`Variant: AutoLayout`** — all other containers (shells, sidebars, top bars, body areas, card panels, form rows, button rows)

Using `ManualLayout` where `AutoLayout` is needed means children all pile at position 0,0.

---

### RULE 9 — No `DisplayName`, no `#` comments in generated YAML

- `DisplayName` is not a valid property anywhere — never emit it
- Do not add `#` YAML comments inside the generated YAML block

---

### RULE 10 — Delegable filtering only; no `Search()` or `in` operator

```yaml
Items: |-
  =Filter('DataSource',
      (locFilterStatus = "All" || StatusColumn = locFilterStatus),
      StartsWith(TitleColumn, locSearchText)
  )
```

Never use `Search()` or the `in` operator — they are not delegable against SharePoint or Dataverse.

---

## Step 4: Control Reference

| Purpose                          | Control declaration                                                            |
| -------------------------------- | ------------------------------------------------------------------------------ |
| Layout container (stack/flex)    | `Control: GroupContainer@1.5.0` + `Variant: AutoLayout`                        |
| Grid layout container            | `Control: GroupContainer@1.5.0` + `Variant: GridLayout`                        |
| Overlay / badge (X,Y positioned) | `Control: GroupContainer@1.5.0` + `Variant: ManualLayout`                      |
| Button                           | `Control: Classic/Button@2.2.0`                                                |
| Single-line text input           | `Control: Classic/TextInput@2.3.2`                                             |
| Multi-line text input            | `Control: Classic/TextInput@2.3.2` + `Mode: =TextMode.MultiLine` in Properties |
| Classic dropdown                 | `Control: Classic/ComboBox@2.3.0`                                              |
| Modern dropdown                  | `Control: ModernCombobox@1.1.0`                                                |
| Date picker                      | `Control: Classic/DatePicker@2.6.0`                                            |
| Icon                             | `Control: Classic/Icon@2.5.0`                                                  |
| Label                            | `Control: Label@2.5.1`                                                         |
| Vertical gallery                 | `Control: Gallery@2.15.0` + `Variant: Vertical`                                |
| Canvas component (reusable)      | `Control: CanvasComponent` + `ComponentName: myComponentName`                  |
| Toggle                           | `Control: Classic/Toggle@2.2.0`                                                |
| Checkbox                         | `Control: Classic/Checkbox@2.1.0`                                              |

**GridLayout container properties:**

```yaml
- conGrid:
    Control: GroupContainer@1.5.0
    Variant: GridLayout
    Properties:
      LayoutGridColumns: =6
      LayoutGridRows: =1
      Height: =140
      FillPortions: =0
      LayoutMinHeight: =16
      LayoutMinWidth: =16
```

**CanvasComponent usage:**

```yaml
- comp_mySidebar:
    Control: CanvasComponent
    ComponentName: sideBar          <- no = prefix, no quotes; this is a schema declaration
    Properties:
      ActiveScreen: =App.ActiveScreen
      Height: =Parent.Height
      Width: =230
```

**Invisible tap-target button** (full-width overlay over a gallery row — `Text: =` with empty formula is valid):

```yaml
- btnRowTapTarget:
    Control: Classic/Button@2.2.0
    Properties:
      Fill: =RGBA(0, 0, 0, 0)
      BorderStyle: =BorderStyle.None
      Height: =Parent.TemplateHeight
      Width: =Parent.Width
      Text: =
      HoverFill: =RGBA(56, 96, 178, 0.1)
      OnSelect: |
        =Set(gblSelectedItem, ThisItem);
        Navigate(ScnDetail)
```

### Naming Conventions

| Element           | Prefix | Example                              |
| ----------------- | ------ | ------------------------------------ |
| Containers        | `con`  | `conTopBar`, `conDialogPanel`        |
| Labels            | `lbl`  | `lblPageTitle`, `lblFieldName`       |
| Buttons           | `btn`  | `btnSave`, `btnCancel`               |
| Icons             | `icn`  | `icnSearch`, `icnClose`              |
| Galleries         | `gal`  | `galRecordList`                      |
| Text inputs       | `txt`  | `txtSearch`, `txtName`               |
| Combo boxes       | `cmb`  | `cmbStatusFilter`                    |
| Date pickers      | `dtp`  | `dtpStartDate`                       |
| Toggles           | `tog`  | `togIsActive`                        |
| Checkboxes        | `chk`  | `chkAgree`                           |
| Context variables | `loc`  | `locSearchText`, `locSelectedRecord` |
| Collections       | `col`  | `colStatusOptions`                   |
| Global variables  | `var`  | `varCurrentUser`                     |

---

## Step 5: Canonical Reference Examples

These are complete, correct examples. Every generated YAML must match this syntax exactly.

### Example A: Confirmation Dialog (complete, bare container — no Screens: wrapper)

```yaml
- conDialogBackdrop:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      X: =0
      Y: =0
      Width: =Parent.Width
      Height: =Parent.Height
      Fill: =RGBA(0, 0, 0, 0.4)
      RadiusTopLeft: =0
      RadiusTopRight: =0
      RadiusBottomLeft: =0
      RadiusBottomRight: =0
    Children:
      - conDialogPanel:
          Control: GroupContainer@1.5.0
          Variant: AutoLayout
          Properties:
            X: =(Parent.Width - 480) / 2
            Y: =(Parent.Height - 240) / 2
            Width: =480
            FillPortions: =0
            Fill: =RGBA(255, 255, 255, 1)
            BorderColor: =RGBA(226, 232, 240, 1)
            BorderThickness: =1
            RadiusTopLeft: =12
            RadiusTopRight: =12
            RadiusBottomLeft: =12
            RadiusBottomRight: =12
            LayoutDirection: =LayoutDirection.Vertical
            LayoutGap: =16
            PaddingTop: =24
            PaddingBottom: =24
            PaddingLeft: =24
            PaddingRight: =24
            LayoutMinHeight: =16
            LayoutMinWidth: =16
          Children:
            - conDialogHeader:
                Control: GroupContainer@1.5.0
                Variant: AutoLayout
                Properties:
                  FillPortions: =0
                  Fill: =RGBA(0, 0, 0, 0)
                  LayoutDirection: =LayoutDirection.Horizontal
                  LayoutAlignItems: =LayoutAlignItems.Center
                  LayoutJustifyContent: =LayoutJustifyContent.SpaceBetween
                  LayoutMinHeight: =16
                  LayoutMinWidth: =16
                  RadiusTopLeft: =0
                  RadiusTopRight: =0
                  RadiusBottomLeft: =0
                  RadiusBottomRight: =0
                Children:
                  - lblDialogTitle:
                      Control: Label@2.5.1
                      Properties:
                        Text: ="Are you sure?"
                        Size: =16
                        FontWeight: =FontWeight.Semibold
                        Color: =RGBA(15, 23, 42, 1)
                        Font: =Font.'Segoe UI'
            - lblDialogMessage:
                Control: Label@2.5.1
                Properties:
                  Text: ="This action cannot be undone. Please confirm."
                  Size: =13
                  FontWeight: =FontWeight.Normal
                  Color: =RGBA(71, 85, 105, 1)
                  Font: =Font.'Segoe UI'
            - conDialogFooter:
                Control: GroupContainer@1.5.0
                Variant: AutoLayout
                Properties:
                  FillPortions: =0
                  Fill: =RGBA(0, 0, 0, 0)
                  LayoutDirection: =LayoutDirection.Horizontal
                  LayoutJustifyContent: =LayoutJustifyContent.End
                  LayoutGap: =8
                  LayoutMinHeight: =16
                  LayoutMinWidth: =16
                  RadiusTopLeft: =0
                  RadiusTopRight: =0
                  RadiusBottomLeft: =0
                  RadiusBottomRight: =0
                Children:
                  - btnCancel:
                      Control: Classic/Button@2.2.0
                      Properties:
                        Text: ="Cancel"
                        Size: =13
                        Font: =Font.'Segoe UI'
                        Fill: =RGBA(255, 255, 255, 1)
                        Color: =RGBA(13, 44, 84, 1)
                        BorderColor: =RGBA(200, 210, 225, 1)
                        HoverFill: =RGBA(245, 246, 248, 1)
                        RadiusTopLeft: =6
                        RadiusTopRight: =6
                        RadiusBottomLeft: =6
                        RadiusBottomRight: =6
                        OnSelect: =Back()
                  - btnConfirm:
                      Control: Classic/Button@2.2.0
                      Properties:
                        Text: ="Confirm"
                        Size: =13
                        Font: =Font.'Segoe UI'
                        Fill: =RGBA(13, 44, 84, 1)
                        Color: =RGBA(255, 255, 255, 1)
                        HoverFill: =RGBA(8, 30, 60, 1)
                        RadiusTopLeft: =6
                        RadiusTopRight: =6
                        RadiusBottomLeft: =6
                        RadiusBottomRight: =6
                        OnSelect: |
                          =UpdateContext({locConfirmed: true});
                          Back()
```

---

### Example B: Full Screen with Sidebar (complete shell)

```yaml
Screens:
  ScnExample:
    Properties:
      OnVisible: |
        =ClearCollect(colStatusOptions, {Value: "All"}, {Value: "Open"}, {Value: "Closed"});
        UpdateContext({locSearch: "", locFilterStatus: "All"})
    Children:
      - conShell:
          Control: GroupContainer@1.5.0
          Variant: AutoLayout
          Properties:
            Width: =Parent.Width
            Height: =Parent.Height
            LayoutDirection: =LayoutDirection.Horizontal
            Fill: =RGBA(0, 0, 0, 0)
            LayoutMinHeight: =16
            LayoutMinWidth: =16
            RadiusTopLeft: =0
            RadiusTopRight: =0
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
          Children:
            - conSidebar:
                Control: GroupContainer@1.5.0
                Variant: AutoLayout
                Properties:
                  Width: =230
                  FillPortions: =0
                  Fill: =RGBA(13, 44, 84, 1)
                  LayoutDirection: =LayoutDirection.Vertical
                  LayoutMinHeight: =16
                  LayoutMinWidth: =16
                  RadiusTopLeft: =0
                  RadiusTopRight: =0
                  RadiusBottomLeft: =0
                  RadiusBottomRight: =0
                Children:
                  - conNavItem1:
                      Control: GroupContainer@1.5.0
                      Variant: AutoLayout
                      Properties:
                        Height: =44
                        FillPortions: =0
                        Fill: =RGBA(255, 255, 255, 0.08)
                        LayoutDirection: =LayoutDirection.Horizontal
                        LayoutAlignItems: =LayoutAlignItems.Center
                        LayoutGap: =12
                        PaddingLeft: =16
                        LayoutMinHeight: =16
                        LayoutMinWidth: =16
                        RadiusTopLeft: =0
                        RadiusTopRight: =0
                        RadiusBottomLeft: =0
                        RadiusBottomRight: =0
                      Children:
                        - icnNavItem1:
                            Control: Classic/Icon@2.5.0
                            Properties:
                              Icon: =Icon.Waffle
                              Color: =RGBA(255, 255, 255, 1)
                              Width: =18
                              Height: =18
                        - lblNavItem1:
                            Control: Label@2.5.1
                            Properties:
                              Text: ="DASHBOARD"
                              Size: =11
                              Font: =Font.'Segoe UI'
                              Color: =RGBA(255, 255, 255, 1)
                              FontWeight: =FontWeight.Semibold
            - conMain:
                Control: GroupContainer@1.5.0
                Variant: AutoLayout
                Properties:
                  Fill: =RGBA(245, 246, 248, 1)
                  LayoutDirection: =LayoutDirection.Vertical
                  LayoutMinHeight: =16
                  LayoutMinWidth: =16
                  RadiusTopLeft: =0
                  RadiusTopRight: =0
                  RadiusBottomLeft: =0
                  RadiusBottomRight: =0
                Children:
                  - conTopBar:
                      Control: GroupContainer@1.5.0
                      Variant: AutoLayout
                      Properties:
                        Height: =60
                        FillPortions: =0
                        Fill: =RGBA(255, 255, 255, 1)
                        LayoutDirection: =LayoutDirection.Horizontal
                        LayoutAlignItems: =LayoutAlignItems.Center
                        LayoutJustifyContent: =LayoutJustifyContent.SpaceBetween
                        PaddingLeft: =24
                        PaddingRight: =24
                        LayoutMinHeight: =16
                        LayoutMinWidth: =16
                        RadiusTopLeft: =0
                        RadiusTopRight: =0
                        RadiusBottomLeft: =0
                        RadiusBottomRight: =0
                      Children:
                        - lblBreadcrumb:
                            Control: Label@2.5.1
                            Properties:
                              Text: ="APP  /  SCREEN"
                              Size: =12
                              Font: =Font.'Segoe UI'
                              Color: =RGBA(100, 116, 139, 1)
                  - conBody:
                      Control: GroupContainer@1.5.0
                      Variant: AutoLayout
                      Properties:
                        Fill: =RGBA(245, 246, 248, 1)
                        LayoutDirection: =LayoutDirection.Vertical
                        LayoutGap: =16
                        PaddingTop: =32
                        PaddingBottom: =32
                        PaddingLeft: =32
                        PaddingRight: =32
                        LayoutMinHeight: =16
                        LayoutMinWidth: =16
                        RadiusTopLeft: =0
                        RadiusTopRight: =0
                        RadiusBottomLeft: =0
                        RadiusBottomRight: =0
                      Children:
                        - lblPageTitle:
                            Control: Label@2.5.1
                            Properties:
                              Text: ="Screen Title."
                              Size: =28
                              FontWeight: =FontWeight.Bold
                              Color: =RGBA(15, 23, 42, 1)
                              Font: =Font.'Segoe UI'
                        - lblPageSubtitle:
                            Control: Label@2.5.1
                            Properties:
                              Text: ="A short description of this screen."
                              Size: =13
                              FontWeight: =FontWeight.Normal
                              Color: =RGBA(100, 116, 139, 1)
                              Font: =Font.'Segoe UI'
```

---

### Example C: Standalone Form Screen

```yaml
Screens:
  ScnRequestForm:
    Properties:
      OnVisible: |
        =UpdateContext({locMode: "New"})
    Children:
      - conFormShell:
          Control: GroupContainer@1.5.0
          Variant: AutoLayout
          Properties:
            Width: =Parent.Width
            Height: =Parent.Height
            LayoutDirection: =LayoutDirection.Vertical
            Fill: =RGBA(245, 246, 248, 1)
            LayoutMinHeight: =16
            LayoutMinWidth: =16
            RadiusTopLeft: =0
            RadiusTopRight: =0
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
          Children:
            - conFormHeader:
                Control: GroupContainer@1.5.0
                Variant: AutoLayout
                Properties:
                  Height: =60
                  FillPortions: =0
                  Fill: =RGBA(255, 255, 255, 1)
                  LayoutDirection: =LayoutDirection.Horizontal
                  LayoutAlignItems: =LayoutAlignItems.Center
                  LayoutJustifyContent: =LayoutJustifyContent.SpaceBetween
                  PaddingLeft: =24
                  PaddingRight: =24
                  LayoutMinHeight: =16
                  LayoutMinWidth: =16
                  RadiusTopLeft: =0
                  RadiusTopRight: =0
                  RadiusBottomLeft: =0
                  RadiusBottomRight: =0
                Children:
                  - lblFormTitle:
                      Control: Label@2.5.1
                      Properties:
                        Text: ="New Request."
                        Size: =28
                        FontWeight: =FontWeight.Bold
                        Color: =RGBA(15, 23, 42, 1)
                        Font: =Font.'Segoe UI'
            - conFormBody:
                Control: GroupContainer@1.5.0
                Variant: AutoLayout
                Properties:
                  Fill: =RGBA(245, 246, 248, 1)
                  LayoutDirection: =LayoutDirection.Vertical
                  LayoutGap: =16
                  PaddingTop: =24
                  PaddingBottom: =24
                  PaddingLeft: =32
                  PaddingRight: =32
                  LayoutMinHeight: =16
                  LayoutMinWidth: =16
                  RadiusTopLeft: =0
                  RadiusTopRight: =0
                  RadiusBottomLeft: =0
                  RadiusBottomRight: =0
                Children:
                  - conFieldTitle:
                      Control: GroupContainer@1.5.0
                      Variant: AutoLayout
                      Properties:
                        FillPortions: =0
                        Fill: =RGBA(0, 0, 0, 0)
                        LayoutDirection: =LayoutDirection.Vertical
                        LayoutGap: =4
                        LayoutMinHeight: =16
                        LayoutMinWidth: =16
                        RadiusTopLeft: =0
                        RadiusTopRight: =0
                        RadiusBottomLeft: =0
                        RadiusBottomRight: =0
                      Children:
                        - lblTitle:
                            Control: Label@2.5.1
                            Properties:
                              Text: ="Title"
                              Size: =12
                              FontWeight: =FontWeight.Semibold
                              Color: =RGBA(71, 85, 105, 1)
                              Font: =Font.'Segoe UI'
                        - txtTitle:
                            Control: Classic/TextInput@2.3.2
                            Properties:
                              HintText: ="Enter a title"
                              Font: =Font.'Segoe UI'
                              Size: =13
            - conFormActions:
                Control: GroupContainer@1.5.0
                Variant: AutoLayout
                Properties:
                  Height: =64
                  FillPortions: =0
                  Fill: =RGBA(255, 255, 255, 1)
                  LayoutDirection: =LayoutDirection.Horizontal
                  LayoutJustifyContent: =LayoutJustifyContent.End
                  LayoutAlignItems: =LayoutAlignItems.Center
                  LayoutGap: =8
                  PaddingRight: =24
                  LayoutMinHeight: =16
                  LayoutMinWidth: =16
                  RadiusTopLeft: =0
                  RadiusTopRight: =0
                  RadiusBottomLeft: =0
                  RadiusBottomRight: =0
                Children:
                  - btnCancel:
                      Control: Classic/Button@2.2.0
                      Properties:
                        Text: ="Cancel"
                        Size: =13
                        Font: =Font.'Segoe UI'
                        Fill: =RGBA(255, 255, 255, 1)
                        Color: =RGBA(13, 44, 84, 1)
                        BorderColor: =RGBA(200, 210, 225, 1)
                        HoverFill: =RGBA(245, 246, 248, 1)
                        RadiusTopLeft: =6
                        RadiusTopRight: =6
                        RadiusBottomLeft: =6
                        RadiusBottomRight: =6
                        OnSelect: =Back()
                  - btnSave:
                      Control: Classic/Button@2.2.0
                      Properties:
                        Text: ="Save"
                        Size: =13
                        Font: =Font.'Segoe UI'
                        Fill: =RGBA(13, 44, 84, 1)
                        Color: =RGBA(255, 255, 255, 1)
                        HoverFill: =RGBA(8, 30, 60, 1)
                        RadiusTopLeft: =6
                        RadiusTopRight: =6
                        RadiusBottomLeft: =6
                        RadiusBottomRight: =6
                        OnSelect: |
                          =Patch('My List', Defaults('My List'), {Title: txtTitle.Text});
                          Back()
```

---

## Step 6: Generate the YAML

Produce the complete YAML starting from `Screens:`. Follow the canonical examples in Step 5 exactly for syntax. Include:

- The correct component pattern based on Step 1
- All navigation items if a sidebar is present, with exactly one active
- Full top bar if applicable
- Complete page body with all required controls
- All `OnVisible` logic flat under the screen name (not inside a `Properties:` block)
- All `OnSelect` logic for buttons and nav items

**Output format requirements — both are mandatory:**

1. **Always wrap the YAML in a fenced code block using ` ```yaml ` and ` ``` `.** Plain prose or unformatted output collapses indentation and produces an unimportable file.
2. **Use exactly 2 spaces per indent level throughout.** No tabs. No 4-space indents. Every nesting level adds exactly 2 spaces. Control bodies inside `Children:` are indented 4 spaces after the `- ` list marker.

**Do not add `#` YAML comments inside the output block.**

**Before emitting each line, verify:**

1. Is the YAML inside a ` ```yaml ` code fence? If not, wrap it now
2. Is indentation correct — 2 spaces per level, 4 spaces after `- ` for control body? Fix before continuing
3. Is the value quoted? Remove the quotes
4. Does the value start with `=`? Add it (except for `Control:` and `Variant:`)
5. Is the key `ControlType:`? Change to `Control:`
6. Is `Variant:` inside `Properties:`? Move it outside as a sibling of `Control:`
7. Is this `Height`, `Width`, or `DisplayName` at screen level? Delete it
8. Is there a `Properties:` wrapper at screen level? Delete it
9. Is there a `BorderRadius:` property? Replace with four `Radius*` properties

---

## Step 7: Document Assumptions

After the YAML block, output:

```
**Data Source Assumptions**
- `ColumnName` -> what this field represents

**Design Assumptions**
- [layout choices, status values, nav items, sizing, etc.]
```

---

## Validation Checklist

Before outputting YAML, confirm every item is true:

- [ ] YAML is output inside a ```yaml fenced code block — never as plain unformatted text
- [ ] Indentation is exactly 2 spaces per level; control bodies inside Children: are 4 spaces after the - list marker
- [ ] No `FontSize:` property anywhere — font size is always `Size:` (PA2108 otherwise)
- [ ] No property value is wrapped in quotes
- [ ] Every value inside `Properties:` starts with `=`
- [ ] Every control uses `Control:` not `ControlType:`
- [ ] Every `Control:` value includes the version suffix (e.g. `GroupContainer@1.5.0`)
- [ ] `Variant:` is a sibling of `Control:`, not inside `Properties:`
- [ ] Component type determined first: dialogs/popups/components use bare container tree (no `Screens:` wrapper); only full standalone screens use `Screens:`
- [ ] Screen-level `Properties:` block (if present) contains ONLY `OnVisible`, `OnHidden`, or `LoadingSpinnerColor` — `Fill`, `Height`, `Width`, and `DisplayName` are NOT valid screen properties
- [ ] `Children:` is a SIBLING of `Properties:` at screen level, never nested inside `Properties:`
- [ ] `Fill` is on the root container inside `Children:`, NOT in the screen-level `Properties:` block
- [ ] No `BorderRadius:` — only `RadiusTopLeft`, `RadiusTopRight`, `RadiusBottomLeft`, `RadiusBottomRight`
- [ ] Every `GroupContainer` has all four `Radius*` properties
- [ ] Fixed-size containers have `FillPortions: =0`
- [ ] AutoLayout containers include `LayoutMinHeight: =16` and `LayoutMinWidth: =16`
- [ ] `ManualLayout` used only for overlays/backdrops and status badges
- [ ] Any formula containing `{` (record literal) uses `|` block scalar — inline `OnSelect: =UpdateContext({...})` breaks YAML parsing with "invalid mapping"
- [ ] Multi-line formulas use `|-` block scalar with `=` on the first line inside the block
- [ ] `OnVisible` / `OnSelect` with multiple statements use `|`; no trailing semicolon after the last statement
- [ ] No `Search()` or `in` operator — only `StartsWith()` and `Filter()`
- [ ] No emoji or special Unicode in any `Text` value
- [ ] No `DisplayName` property anywhere
- [ ] No `#` YAML comments inside the YAML block
- [ ] Font is `=Font.'Segoe UI'` throughout
- [ ] Page title label text ends with a full stop
- [ ] Data source and design assumptions documented after the YAML block

---

## References

- [Power Apps YAML source format](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/power-apps-yaml)
- [Power Fx delegable functions for SharePoint](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-list)
- [Power Apps controls reference](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/reference-properties)

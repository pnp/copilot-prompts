---
name: powerapps-canvas-yaml-generator
description: Generates valid, importable Power Apps Source Code YAML for canvas app screens. Use when asked to create YAML, scaffold, or modify any Power Apps canvas app screen — including full screens, dialogs, forms, galleries, detail views, dashboards, or any layout container — or when asked to generate Power Fx formulas or produce Power Apps source code for import.
---

# Power Apps Canvas App YAML Generator

Generates production-ready, importable Power Apps Source Code YAML for canvas app screens and components, following the official Power Apps YAML source format rules and a consistent enterprise design system.

---

## Gather Context

Before generating, confirm:

1. **Screen or component name** — e.g. `ScnDashboard`, `ScnRequestForm`, `DlgConfirmDelete`
2. **Component type** — full screen, dialog/overlay, form, gallery, detail view, dashboard, or other
3. **Navigation context** — sidebar needed? Which nav item is active? Or no sidebar?
4. **Screen purpose** — one sentence describing what the screen or component does
5. **Data source** — SharePoint list, Dataverse table, or collection name and known column names (if data-driven)
6. **Controls needed** — gallery, form fields, dropdowns, status badges, buttons, dialogs, etc.

**If context is missing:** Default to a full screen with sidebar, no data source, and generate a complete shell. State assumptions at the top of the output. Only block and ask if the component type is genuinely ambiguous.

---

## Output Format

````markdown
```yaml
Screens:
  ScnMyScreen:
    Properties:
      OnVisible: |
        =ClearCollect(colItems, MyList);
        UpdateContext({locSearch: ""})
    Children:
      - conShell:
          Control: GroupContainer@1.5.0
          Variant: AutoLayout
          Properties: ...
```

**Data Source Assumptions**

- `ColumnName` -> what this field represents

**Design Assumptions**

- [layout choices, status values, nav items, sizing, etc.]
````

**Component type determines the top-level structure:**

| Type                                                  | `Screens:` wrapper?      |
| ----------------------------------------------------- | ------------------------ |
| Full screen (with or without sidebar)                 | YES                      |
| Standalone form / gallery / detail / dashboard screen | YES                      |
| Dialog / overlay / popup                              | NO — bare container tree |
| Reusable component / card / partial UI                | NO — bare container tree |

---

## Design System

### Colours

| Token           | Value                    | Use                                        |
| --------------- | ------------------------ | ------------------------------------------ |
| Navy primary    | `RGBA(13, 44, 84, 1)`    | Sidebar fill, primary buttons              |
| Navy dark hover | `RGBA(8, 30, 60, 1)`     | Primary button hover                       |
| Page background | `RGBA(245, 246, 248, 1)` | Main content area fill (on root container) |
| White           | `RGBA(255, 255, 255, 1)` | Cards, panels, top bar                     |
| Border          | `RGBA(226, 232, 240, 1)` | Card borders, dividers                     |
| Table header bg | `RGBA(248, 250, 252, 1)` | Gallery header row                         |
| Text primary    | `RGBA(15, 23, 42, 1)`    | Page titles, headings                      |
| Text secondary  | `RGBA(71, 85, 105, 1)`   | Body text                                  |
| Text muted      | `RGBA(100, 116, 139, 1)` | Breadcrumbs, subtitles, column headers     |

### Status Badge Colours

| Category                      | Fill                     | Text                   |
| ----------------------------- | ------------------------ | ---------------------- |
| Available / Active / Success  | `RGBA(220, 252, 231, 1)` | `RGBA(22, 101, 52, 1)` |
| Assigned / In Progress / Info | `RGBA(219, 234, 254, 1)` | `RGBA(30, 64, 175, 1)` |
| Pending / Warning             | `RGBA(254, 243, 199, 1)` | `RGBA(146, 64, 14, 1)` |
| Error / Rejected / Urgent     | `RGBA(254, 226, 226, 1)` | `RGBA(185, 28, 28, 1)` |
| Inactive / Neutral / Closed   | `RGBA(241, 245, 249, 1)` | `RGBA(71, 85, 105, 1)` |

### Typography

Font: always `=Font.'Segoe UI'`. Font size property is **`Size`** — `FontSize` does not exist.

| Use                      | `Size` | `FontWeight`                                   |
| ------------------------ | ------ | ---------------------------------------------- |
| Page title               | `=28`  | `=FontWeight.Bold`                             |
| Panel / section title    | `=16`  | `=FontWeight.Semibold`                         |
| Body / button            | `=13`  | `=FontWeight.Normal` or `=FontWeight.Semibold` |
| Breadcrumb / small label | `=12`  | `=FontWeight.Normal`                           |
| Nav label                | `=11`  | `=FontWeight.Normal` or `=FontWeight.Semibold` |
| Table column header      | `=10`  | `=FontWeight.Semibold` (ALL CAPS)              |

---

## YAML Rules

All rules are absolute. Violating any one causes a PA1001 or PA2108 import error.

### RULE 0 — Output inside a fenced code block with exact 2-space indentation

Always wrap output in ` ```yaml `. Indentation is 2 spaces per level. Control bodies inside `Children:` are 4 spaces after the `- ` list marker. Loss of indentation causes immediate PA1001.

```
Screens:                       0 spaces
  ScnName:                     2 spaces
    Properties:                4 spaces
      OnVisible: |             6 spaces
        =...                   8 spaces
    Children:                  4 spaces
      - conShell:              6 spaces  (the - counts as 2 of the spaces)
          Control: ...         10 spaces
          Properties:          10 spaces
            Fill: =...         12 spaces
          Children:            10 spaces
            - conChild:        12 spaces
                Control: ...   16 spaces
```

### RULE 1 — Property values are never quoted

```yaml
# WRONG
Fill: "=RGBA(13, 44, 84, 1)"
Width: "=230"

# CORRECT
Fill: =RGBA(13, 44, 84, 1)
Width: =230
```

### RULE 2 — Every property value starts with `=`

Every value inside `Properties:` is a Power Fx expression and must begin with `=`. No exceptions for strings, numbers, booleans, colours, or enums.

```yaml
# WRONG               # CORRECT
Width: 230            Width: =230
Visible: true         Visible: =true
Text: Hello           Text: ="Hello"
Fill: RGBA(...)       Fill: =RGBA(13, 44, 84, 1)
FontWeight: ...Bold   FontWeight: =FontWeight.Bold
```

The only values without `=` are schema declaration keys: `Control:`, `Variant:`, and `ComponentName:`.

### RULE 2b — Font size is `Size:`, never `FontSize:`

`FontSize` does not exist on any versioned classic control. It causes PA2108.

```yaml
# WRONG                   # CORRECT
FontSize: =16             Size: =16
```

### RULE 3 — Use `Control:` not `ControlType:`

`ControlType:` does not exist in the Source Code schema.

```yaml
# WRONG                              # CORRECT
ControlType: "GroupContainer"        Control: GroupContainer@1.5.0
```

### RULE 4 — `Variant:` is a sibling of `Control:`, never inside `Properties:`

```yaml
# WRONG                        # CORRECT
Control: GroupContainer@1.5.0  Control: GroupContainer@1.5.0
Properties:                    Variant: AutoLayout
  Variant: AutoLayout          Properties:
  Fill: =...                     Fill: =...
```

### RULE 5 — Screen-level structure

Screens support an optional `Properties:` block for `OnVisible`, `OnHidden`, and `LoadingSpinnerColor` only. `Children:` is always a **sibling** of `Properties:`, never nested inside it. `Fill`, `Height`, `Width`, and `DisplayName` are never valid at screen level.

```yaml
# CORRECT
Screens:
  ScnMyScreen:
    Properties:                        <- optional; only OnVisible / OnHidden / LoadingSpinnerColor
      LoadingSpinnerColor: =RGBA(...)
      OnVisible: |
        =ClearCollect(colItems, MyList)
    Children:                          <- sibling of Properties:, never inside it
      - conShell:
          Control: GroupContainer@1.5.0
          Variant: AutoLayout
          Properties:
            Fill: =RGBA(245, 246, 248, 1)   <- Fill goes HERE on root container
            Height: =Parent.Height
            Width: =Parent.Width

# WRONG — Fill/Height/Width at screen level
Screens:
  ScnMyScreen:
    Properties:
      Fill: =RGBA(...)      # INVALID
      Height: =App.Height   # INVALID
```

### RULE 5b — Dialogs and components use bare container trees, no `Screens:` wrapper

```yaml
# WRONG — dialog wrapped in Screens:
Screens:
  DlgConfirm:
    Children:
      - conDialogBackdrop: ...

# CORRECT — bare container tree
- conDialogBackdrop:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      X: =0
      Y: =0
      Width: =Parent.Width
      Height: =Parent.Height
      Fill: =RGBA(0, 0, 0, 0.4)
      ...
```

### RULE 6 — No `BorderRadius:` — use four `Radius*` properties

```yaml
# WRONG            # CORRECT
BorderRadius: =6   RadiusTopLeft: =8
                   RadiusTopRight: =8
                   RadiusBottomLeft: =8
                   RadiusBottomRight: =8
```

Every `GroupContainer` must include all four `Radius*` properties. Use `=0` for square corners.

### RULE 7 — Block scalars: `|-` for expressions, `|` for statements

- **`|-`** for a single multi-line expression (no `;`): `Fill`, `Items`, `Color`, `Default`
- **`|`** for multi-statement sequences (with `;`): `OnSelect`, `OnVisible`, `OnHidden`
- The `=` goes on the **first line inside** the block, not on the key line

```yaml
# Single expression — use |-
Items: |-
  =AddColumns(
      Filter(MyList, Status = "Active"),
      "Extra", Value(ID)
  )

# Multi-statement — use |
OnSelect: |
  =Set(gblSelectedItem, ThisItem);
  Navigate(ScnDetail)

# Both | and |- work for OnSelect/OnVisible — either is valid
OnSelect: |-
  =Set(gblFrmMode, "New");
  Navigate(ScnDetail)
```

### RULE 7b — Formulas containing `{` must use block scalar

YAML parses `{key: value}` as a mapping. Power Fx record literals break inline parsing.

```yaml
# WRONG — causes PA1001 "invalid mapping"
OnSelect: =UpdateContext({locVisible: true, locItem: ThisItem})

# CORRECT
OnSelect: |
  =UpdateContext({locVisible: true, locItem: ThisItem})

# Fine inline — no { } present
OnSelect: =Navigate(ScnDetail)
OnSelect: =Back()
Items: =Filter('My List', Status.Value = "Active")
```

### RULE 8 — `ManualLayout` only for overlays and status badges

- `Variant: ManualLayout` — dialog backdrops, dialog panels needing explicit `X`/`Y`, status badges
- `Variant: AutoLayout` — all other containers
- `Variant: GridLayout` — stat card grids (use with `LayoutGridColumns` / `LayoutGridRows`)

### RULE 9 — Delegable filtering only

Never use `Search()` or the `in` operator — they are not delegable against SharePoint or Dataverse.

```
Filter(DataSource,
    (locFilterStatus = "All" || StatusColumn = locFilterStatus),
    StartsWith(TitleColumn, locSearchText)
)
```

### RULE 10 — No `DisplayName`, no YAML comments

`DisplayName` is not a valid property anywhere. Do not add `#` YAML comments inside generated YAML.

---

## Controls Reference

| Purpose                          | Control declaration                                              |
| -------------------------------- | ---------------------------------------------------------------- |
| Layout container (stack/flex)    | `Control: GroupContainer@1.5.0` + `Variant: AutoLayout`          |
| Grid layout container            | `Control: GroupContainer@1.5.0` + `Variant: GridLayout`          |
| Overlay / badge (X,Y positioned) | `Control: GroupContainer@1.5.0` + `Variant: ManualLayout`        |
| Button                           | `Control: Classic/Button@2.2.0`                                  |
| Single-line text input           | `Control: Classic/TextInput@2.3.2`                               |
| Multi-line text input            | `Control: Classic/TextInput@2.3.2` + `Mode: =TextMode.MultiLine` |
| Classic dropdown                 | `Control: Classic/ComboBox@2.3.0`                                |
| Modern dropdown                  | `Control: ModernCombobox@1.1.0`                                  |
| Date picker                      | `Control: Classic/DatePicker@2.6.0`                              |
| Icon                             | `Control: Classic/Icon@2.5.0`                                    |
| Label                            | `Control: Label@2.5.1`                                           |
| Vertical gallery                 | `Control: Gallery@2.15.0` + `Variant: Vertical`                  |
| Canvas component (reusable)      | `Control: CanvasComponent` + `ComponentName: myComponentName`    |
| Toggle                           | `Control: Classic/Toggle@2.2.0`                                  |
| Checkbox                         | `Control: Classic/Checkbox@2.1.0`                                |

### Naming Conventions

| Element           | Prefix | Example                             |
| ----------------- | ------ | ----------------------------------- |
| Containers        | `con`  | `conTopBar`, `conDialogPanel`       |
| Labels            | `lbl`  | `lblPageTitle`, `lblFieldName`      |
| Buttons           | `btn`  | `btnSave`, `btnCancel`              |
| Icons             | `icn`  | `icnSearch`, `icnClose`             |
| Galleries         | `gal`  | `galRecordList`                     |
| Text inputs       | `txt`  | `txtSearch`, `txtName`              |
| Combo boxes       | `cmb`  | `cmbStatusFilter`                   |
| Date pickers      | `dtp`  | `dtpStartDate`                      |
| Toggles           | `tog`  | `togIsActive`                       |
| Checkboxes        | `chk`  | `chkAgree`                          |
| Components        | `comp` | `comp_Sidebar`, `comp_PageHeader`   |
| Context variables | `loc`  | `locSearchText`, `locSelectedItem`  |
| Collections       | `col`  | `colStatusOptions`                  |
| Global variables  | `gbl`  | `gblCurrentUser`, `gblSelectedItem` |

---

## Examples

### Example A — Confirmation Dialog (bare container, no `Screens:` wrapper)

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
                  Text: ="This action cannot be undone."
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

### Example B — Full Screen with Sidebar (abbreviated shell)

```yaml
Screens:
  ScnExample:
    Properties:
      LoadingSpinnerColor: =RGBA(13, 44, 84, 1)
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
            DropShadow: =DropShadow.None
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
                  - conNavDashboard:
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
                        - icnNavDashboard:
                            Control: Classic/Icon@2.5.0
                            Properties:
                              Icon: =Icon.Waffle
                              Color: =RGBA(255, 255, 255, 1)
                              Width: =18
                              Height: =18
                        - lblNavDashboard:
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
                  DropShadow: =DropShadow.None
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
```

---

### Example C — Standalone Form Screen

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

## Rules

**Do:**

- Always wrap output in a ` ```yaml ` fenced code block — plain text collapses indentation
- Use exactly 2 spaces per indent level throughout
- Use `|-` for single multi-line expressions; `|` for multi-statement sequences with `;`
- Put `OnVisible` / `OnHidden` inside the screen-level `Properties:` block; put `Children:` as a sibling
- Put `Fill` and sizing on the **root container** inside `Children:`, never at screen level
- Use `Size:` for font size — never `FontSize:`
- Use `Control:` with the versioned type string — never `ControlType:`
- Include all four `Radius*` properties on every `GroupContainer`
- Set `FillPortions: =0` on any container with a fixed `Width` or `Height`
- Include `LayoutMinHeight: =16` and `LayoutMinWidth: =16` on all AutoLayout containers
- Use `|` block scalar for any formula containing `{` (record literals break inline YAML)
- Use `StartsWith()` and `Filter()` for delegable filtering — never `Search()` or `in`
- Document data source column names and design assumptions after the YAML block

**Don't:**

- Quote property values — `Width: "=230"` is always wrong
- Use `FontSize:` — it does not exist in the schema
- Use `ControlType:` — the correct key is `Control:`
- Put `Fill`, `Height`, `Width`, or `DisplayName` at screen level
- Nest `Children:` inside screen-level `Properties:`
- Use `BorderRadius:` — always use the four `Radius*` properties
- Use `Search()` or the `in` operator in filter expressions
- Wrap dialogs/components in a `Screens:` block
- Add `#` YAML comments inside generated YAML
- Add `DisplayName` property anywhere

---

## Pre-Delivery Checklist

Before outputting any YAML, confirm every item:

- [ ] Output is inside a ` ```yaml ` fenced code block
- [ ] Indentation is exactly 2 spaces per level; 4 spaces after `- ` for control body
- [ ] No `FontSize:` anywhere — font size uses `Size:`
- [ ] No quoted property values
- [ ] Every `Properties:` value starts with `=`
- [ ] Every control uses `Control:` not `ControlType:`, with version suffix
- [ ] `Variant:` is a sibling of `Control:`, not inside `Properties:`
- [ ] Dialogs/components use bare container tree — no `Screens:` wrapper
- [ ] Screen `Properties:` block contains only `OnVisible`, `OnHidden`, `LoadingSpinnerColor`
- [ ] `Children:` is a sibling of `Properties:` at screen level, never nested inside it
- [ ] `Fill` is on the root container inside `Children:`, not at screen level
- [ ] No `BorderRadius:` — only the four `Radius*` properties, on every `GroupContainer`
- [ ] Fixed-size containers have `FillPortions: =0`
- [ ] All AutoLayout containers have `LayoutMinHeight: =16` and `LayoutMinWidth: =16`
- [ ] Any formula with `{` uses `|` or `|-` block scalar
- [ ] `|-` used for single expressions; `|` used for multi-statement sequences
- [ ] No `Search()` or `in` — only `StartsWith()` and `Filter()`
- [ ] No `DisplayName`, no `#` YAML comments
- [ ] `Font: =Font.'Segoe UI'` throughout
- [ ] Page title ends with a full stop
- [ ] Data source and design assumptions documented after the YAML block

---

## References

- [Power Apps YAML source format](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/power-apps-yaml)
- [Power Fx delegable functions for SharePoint](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-list)
- [GroupContainer AutoLayout](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/container-layout)
- [Power Apps controls reference](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/reference-properties)

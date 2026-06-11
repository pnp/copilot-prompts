# XML Field Map for Prompt-K Template

This reference maps each **data field** → **shape name in slide1.xml** → **editing strategy**.

Think of slide1.xml like a form with named input boxes. You're filling the boxes in, not redesigning the form.

---

## Shape → Field Mapping

| Shape name (in XML `cNvPr name=`) | Content | Character limit | Notes |
|---|---|---|---|
| `Title 4` (id=5) | `title_top` — `Prompt of the Week` / `Skill of the Week` | ~22 chars | **Variant-dependent.** Template ships with "Skill of the Week"; change to "Prompt of the Week" when `variant == "prompt"`. |
| `Rectangle: Rounded Corners 4` (id=8) | `badge_label` — `The PROMPT…` / `The SKILL…` | ~14 chars | **Variant-dependent.** Template ships with "The SKILL…"; change to "The PROMPT…" when `variant == "prompt"`. |
| `TextBox 10` (id=9) | 🚀 + Sample title (`agent_title`) | ~40 chars | Keep the rocket emoji prefix. Title 18–22 chars renders cleanest; >25 chars may need a font-size pass. |
| `TextBox 25` (id=26) | Body — system prompt (prompt variant) or description (skill variant) | ~600 chars | Multi-paragraph, italic style — do NOT change `<a:rPr>`. Shorter bodies render best — `<a:spAutoFit/>` makes this box grow, which can overlap fixed elements. |
| `Rectangle: Rounded Corners 4` (id=10) | Author display name (`author_name`) | ~25 chars | Bold white text on dark badge. Name is split across two `<a:r>` runs — first run has trailing space, second run holds the surname. |
| `Rectangle: Rounded Corners 4` (id=7) | `aka.ms/copilot-prompt-library` | Fixed — do not change | Footer link — leave as-is |
| `TextBox 10` (id=4) | 🚀 Kudos 🎉 | Fixed — do not change | Kudos badge — leave as-is |

---

## Identifying Shapes by ID (Disambiguation)

When two shapes share the same `name` attribute, use `id` to distinguish:

```xml
<!-- Agent Title box — id="9" -->
<p:cNvPr id="9" name="TextBox 10" .../>

<!-- Kudos badge — id="4" -->
<p:cNvPr id="4" name="TextBox 10" .../>

<!-- Author badge — id="10" -->
<p:cNvPr id="10" name="Rectangle: Rounded Corners 4" .../>
```

> **Quick grep to find a shape by id:**
> ```bash
> grep -n 'id="9"' /home/claude/unpacked/ppt/slides/slide1.xml
> ```
> Note the line number, then view ±50 lines around it to find the `<a:t>` nodes to replace.

---

## Editing Pattern

For each field, apply this pattern (never change `<a:rPr>` or `<a:pPr>` attributes):

```xml
<!-- BEFORE (example — agent title) -->
<a:t>🚀   Creator Agent  </a:t>

<!-- AFTER -->
<a:t>🚀   Your New Agent Title  </a:t>
```

For the prompt body (`TextBox 25`), the text is split across multiple `<a:r>` runs and `<a:p>` paragraphs.
**Replace the entire paragraph block** rather than individual runs, preserving the surrounding `<p:txBody>` wrapper.

Minimal safe paragraph template (copy run style from the original):
```xml
<a:p>
  <a:r>
    <a:rPr lang="en-US" sz="1000" i="1" dirty="0"/>
    <a:t>YOUR PROMPT TEXT HERE</a:t>
  </a:r>
</a:p>
```

If the prompt is long, split it across multiple `<a:p>` blocks. Each `<a:p>` renders as a new line.

---

## Prompt Length Warning

The dashed-border text box has fixed dimensions (approx `4917022 × 5200000` EMUs, ~5.1" × 5.4").
At `sz="1000"` (10pt) this holds roughly **600–700 characters** before overflow.

If the source prompt exceeds this:
1. Truncate intelligently at a sentence boundary
2. Append `"[…see full prompt at aka.ms/copilot-prompt-library]"` on the last line
3. Never reduce font size below `sz="900"` (9pt) — readability degrades on screen

---

## Author Photo (IMPORTANT)

The **visible large photo on the right side** of the slide is `Picture 30` (id=31, **rId5 → `ppt/media/image5.png`**). This is the shape to replace — NOT `Image 1` (id=3), which sits off-slide at x=14393221 and is not visible.

To swap the author photo:

1. Take the single image from the skill's `author/` folder (any extension — .jpeg/.jpg/.png).
2. Convert it to PNG and overwrite `unpacked/ppt/media/image5.png` (keep the filename — that way `rId5` and `[Content_Types].xml` need no changes):
   ```python
   from PIL import Image
   Image.open(AUTHOR_PATH).save('unpacked/ppt/media/image5.png', 'PNG')
   ```
3. Do NOT touch `Image 1` / id=3 / rId3 — that shape is off-slide and irrelevant. The original `media/image3.svg` reference is unused and will be pruned by `clean.py`.
4. The `Picture 30` shape has photo effects applied (`sharpenSoften`, `brightnessContrast`) and a 3D bevel — these stay as-is and apply to the new image automatically.

Square images (1:1) render best — the slot is 6246328 × 7659056 EMU but with `srcRect` cropping.

---

## Fixed Elements (Do Not Touch)

These shapes must remain unchanged:
- `Graphic 1` — the Microsoft Copilot logo (top-left)
- `Image 1` (id=3) — off-slide placeholder, leave alone
- `Rectangle: Rounded Corners 5` — the outer dashed border frame
- Background gradient fill on the slide master

> **Note:** `Title 4` ("Skill of the Week" / "Prompt of the Week") and the `The SKILL…` / `The PROMPT…` badge are **variant-dependent** — see the Shape → Field Mapping table above. They are NOT fixed.

---
name: prompt-of-the-week
description: "Generates a weekly PowerPoint slide from a PnP copilot-prompts GitHub sample URL (for example, samples/agent-instructions/creator-agent), derives the correct weekly title from the sample folder, and produces a styled .pptx file that matches the Prompt-K template layout."
---

# Prompt-of-the-Week PPTX Skill

Think of this skill as a **mail merge meets slide design**: the GitHub repo is the data source, and
the `Prompt-K.pptx` template is the envelope. Your job is to pour the right data into the right
slots without disturbing the surrounding design.

---

## Quick Overview

| Step | What you do |
|------|-------------|
| 1 | Fetch & parse the GitHub sample (README + sample.json) |
| 2 | Extract the five data fields (see below) |
| 3 | Copy the template and inject fields via XML editing |
| 4 | Swap the author photo using the image in the skill's `author/` folder |
| 5 | QA visually, then present the file |

---

## Author Photo Convention (IMPORTANT)

The skill ships with an `author/` folder that always contains **exactly one image** — the photo of
the current week's author. Always use that file as the photo for the slide. Do not attempt to
download avatars from GitHub or the web — this sandbox has no outbound internet access for binary
fetches.

```bash
SKILL_DIR="/mnt/user-config/.claude/skills/prompt-of-the-week"
AUTHOR_IMG=$(ls "$SKILL_DIR/author/" | head -1)   # exactly one file expected
AUTHOR_PATH="$SKILL_DIR/author/$AUTHOR_IMG"
```

If the folder is empty or missing, ask the user to drop the week's author photo into
`prompt-of-the-week/author/` before continuing. The user maintains this folder — replacing the
image each week is part of their workflow.

To swap it into the slide (the visible photo on the right side is **`Picture 30` / id=31 / rId5 → `image5.png`**, NOT the off-slide `Image 1` / id=3 / rId3):

1. Convert the author image to PNG and overwrite `working/unpacked/ppt/media/image5.png`. Keeping
   the filename means no rels or `[Content_Types].xml` edits are needed:
   ```python
   from PIL import Image
   Image.open(AUTHOR_PATH).save('working/unpacked/ppt/media/image5.png', 'PNG')
   ```
2. Do NOT touch `Image 1` (id=3, rId3) — that shape sits off-slide and is not visible.
   The skill's earlier instructions referencing rId3 were wrong; rId5 is the correct target.
3. The `Picture 30` shape already has photo effects (sharpen, brightness/contrast) and a 3D bevel
   applied — these stay as-is and apply to the new image automatically. Square (1:1) author
   images render best.

---

## Step 1 — Fetch Data from GitHub

The user will provide a URL like:
```
https://github.com/pnp/copilot-prompts/tree/main/samples/agent-instructions/creator-agent
```

Convert it to raw content URLs and fetch both files:

```bash
# Convert tree URL → raw URL pattern
# https://github.com/{owner}/{repo}/tree/{branch}/{path}
# → https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}/README.md
# → https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}/assets/sample.json

SAMPLE_PATH="samples/agent-instructions/creator-agent"  # extracted from URL
README_URL="https://raw.githubusercontent.com/pnp/copilot-prompts/main/${SAMPLE_PATH}/README.md"
META_URL="https://raw.githubusercontent.com/pnp/copilot-prompts/main/${SAMPLE_PATH}/assets/sample.json"

curl -sSL "$README_URL" -o /home/claude/sample_readme.md
curl -sSL "$META_URL" -o /home/claude/sample_meta.json 2>/dev/null || echo "{}" > /home/claude/sample_meta.json
```

If curl fails (network restrictions), use the `web_fetch` tool directly on the raw URLs.

---

## Step 2 — Extract the Required Fields

Parse the fetched content with Python. Every field maps to exactly one shape in the template.

```python
import json, re

readme = open('/home/claude/sample_readme.md').read()
meta   = json.load(open('/home/claude/sample_meta.json')) if open('/home/claude/sample_meta.json').read().strip() != '{}' else {}
sample_parts = SAMPLE_PATH.strip('/').split('/')
sample_folder = sample_parts[-2] if len(sample_parts) >= 2 else ''

# Top tile varies by source folder.
if sample_folder == 'agent-instructions':
    title_top = 'System Prompt of the Week'
elif sample_folder == 'skills':
    title_top = 'Skill of the Week'
else:
    title_top = 'Prompt of the Week'

# ── Field 1: Agent / Prompt Title ──────────────────────────────────────────
# Prefer: first H1 heading in README; fallback to meta['title']
title_match = re.search(r'^#\s+(.+)', readme, re.MULTILINE)
agent_title = title_match.group(1).strip() if title_match else meta.get('title', 'Unknown Agent')

# ── Field 2: The Prompt (system prompt body) ────────────────────────────────
# Look for a code block (```markdown / ``` / ```text) that contains the prompt,
# OR a section headed "## Prompt" / "## Instructions" / "## System Prompt"
prompt_body = ''
block = re.search(r'(?:##\s+(?:Prompt|Instructions?|System Prompt)[^\n]*\n)(.*?)(?=\n##|\Z)', readme, re.DOTALL)
if block:
    prompt_body = block.group(1).strip()
    # Strip fenced code delimiters if present
    prompt_body = re.sub(r'^```[a-z]*\n?', '', prompt_body, flags=re.MULTILINE).strip('`\n ')

# ── Field 3: Author name ────────────────────────────────────────────────────
# Check meta['authors'][0]['name'], then README "Author:" line
author = ''
if meta.get('authors'):
    author = meta['authors'][0].get('name', '')
if not author:
    auth_match = re.search(r'[Aa]uthor[:\s]+([^\n]+)', readme)
    if auth_match:
        author = auth_match.group(1).strip()

# ── Field 4: Compatibility / tags summary (optional, shown in footer area) ──
tags = ', '.join(meta.get('tags', []))

# ── Field 5: Sample folder name (used as slug / emoji label) ────────────────
sample_name = SAMPLE_PATH.split('/')[-1].replace('-', ' ').title()

print(f"Top tile: {title_top}")
print(f"Title:   {agent_title}")
print(f"Author:  {author}")
print(f"Tags:    {tags}")
print(f"Prompt preview: {prompt_body[:120]}...")
```

Use these folder rules when setting the top tile in the slide:

| Source folder | Top tile text |
|---|---|
| `agent-instructions` | `System Prompt of the Week` |
| `prompts` | `Prompt of the Week` |
| `skills` | `Skill of the Week` |

> **Analogy**: The slide fields are like variables in a template literal — `${title}`, `${author}`,
> etc. The XML editing in Step 3 is the interpolation engine.

---

## Step 3 — Edit the Template

See `references/xml-field-map.md` for the exact XML shape names and replacement strategy.

```bash
# 1. Copy template to working location
cp /path/to/skill/references/Prompt-K.pptx /home/claude/output.pptx

# 2. Unpack
python /mnt/skills/public/pptx/scripts/office/unpack.py /home/claude/output.pptx /home/claude/unpacked/

# 3. Edit slide1.xml  ← all content lives on the single slide
#    (Use str_replace tool — one replacement per shape)
#    Set the top title shape to title_top based on SAMPLE_PATH:
#    agent-instructions => "System Prompt of the Week"
#    prompts => "Prompt of the Week"
#    skills => "Skill of the Week"

# 4. Clean & repack
python /mnt/skills/public/pptx/scripts/clean.py /home/claude/unpacked/
python /mnt/skills/public/pptx/scripts/office/pack.py /home/claude/unpacked/ /home/claude/output.pptx \
       --original /path/to/skill/references/Prompt-K.pptx
```

**When editing XML text nodes, always preserve surrounding `<a:r>` run tags and their `<a:rPr>`
formatting.** Only replace the inner `<a:t>` content. Changing run properties will break fonts
and colours.

---

## Step 4 — QA & Present

```bash
# Convert to image for visual check
python /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf /home/claude/output.pptx
pdftoppm -jpeg -r 150 /home/claude/output.pdf /home/claude/slide
ls /home/claude/slide*.jpg
```

Visually verify (use the `view` tool on the jpg):
- Top tile text matches the sample folder (`agent-instructions`, `prompts`, or `skills`)
- Title text matches the sample name
- Prompt body is not cut off or overflowing the dashed border box
- Author name is visible in the right-side name badge
- The author photo on the right matches the image from the skill's `author/` folder
- No leftover placeholder text ("The PROMPT…", "Creator Agent", "Cyprien Maloeuvre")

Then copy to outputs and present:
```bash
cp /home/claude/output.pptx /mnt/user-data/outputs/PromptOfTheWeek.pptx
```

---

## Reference Files

| File | When to read |
|------|-------------|
| `references/xml-field-map.md` | Before editing slide1.xml — shows exact shape names, XML paths, and character limits |
| `references/Prompt-K.pptx` | The canonical template — always copy this, never edit it directly |

Read `references/xml-field-map.md` **before** you open slide1.xml.

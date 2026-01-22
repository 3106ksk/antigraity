---
description: Text to Slide Generation Workflow
---

# Text to Slide Generation Workflow

This workflow automates the process of converting raw text into slide prompts ready for image generation with Nano Banana Pro.

## Step 1: Create Marp Slides

First, read the user's source text. Then, generate a Marp-formatted Markdown file named `slides.md` (or update it if it exists).

**Rules for `slides.md` conversion:**
1.  **Header**: format the file with the following YAML frontmatter:
    ```markdown
    ---
    marp: true
    theme: default
    paginate: true
    backgroundColor: #fff
    ---
    ```
2.  **Slide Separation**: Use `---` to separate each slide.
3.  **Content Structure**: Ensure each slide has a clear header (`#` or `##`) and bullet points for readability.
4.  **Language**: Keep the language consistent with the source text (Japanese, based on current context).

## Step 2: Generate Prompts

Run the python script to split the slides and create the prompt files.

```bash
python3 scripts/generate_prompts.py slides.md
```

// turbo
This will create a new directory in `prompts/YYYY-MM-DD_HH-MM-SS/` containing individual markdown files for each slide's prompt.

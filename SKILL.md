---
name: ai-image-stripper
description: "Strip C2PA/AI metadata from generated images. Use when user wants to remove AI detection, clean image provenance, or bypass platform AI labeling."
argument-hint: [folder-path]
allowed-tools: "Bash(uv run --with pillow python *)"
metadata:
  version: "2.0.0"
  author: "aiwork4me"
---

# AI Image Stripper

Strip invisible C2PA/AI-generation metadata from images so platforms cannot detect and flag them as AI content.

## Execution

Run the strip script with an isolated environment (does NOT modify user's project):

```bash
uv run --with pillow python "${CLAUDE_SKILL_DIR}/scripts/strip.py" "$ARGUMENTS"
```

### Single file

```bash
uv run --with pillow python "${CLAUDE_SKILL_DIR}/scripts/strip.py" "<file_path>" -o "<output_path>"
```

### Folder (batch)

```bash
uv run --with pillow python "${CLAUDE_SKILL_DIR}/scripts/strip.py" "<folder_path>"
```

All images in the folder are processed and saved as `0.jpg`, `1.jpg`, `2.jpg`, ... in the same folder. Existing numbered files are skipped automatically.

### Output format

Default is JPEG (quality 95). If the user wants lossless output:

```bash
uv run --with pillow python "${CLAUDE_SKILL_DIR}/scripts/strip.py" "<folder_path>" --format png
```

## After running

Report to the user:
1. Number of files processed
2. Output filenames
3. File size before -> after
4. Confirm resolution is preserved

## Supported inputs

`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`, `.tif`

## Troubleshooting

- **"No supported image files found"**: The folder contains no image files with supported extensions.
- **"already exists"**: Numbered output files from a previous run exist. The user can delete them and re-run, or the skill will skip those inputs.
- **uv not available**: Fall back to `python3 -c "from PIL import Image; ..."` if Pillow is already installed, or ask the user to install uv.

## Technical details

For background on C2PA metadata, what gets stripped, and limitations, read `references/technical-details.md`.

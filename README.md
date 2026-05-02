# AI Image Stripper

**Strip invisible AI-generation metadata from images in one command.**

ChatGPT, DALL-E, and Gemini embed hidden C2PA metadata in every image they generate. LinkedIn, Xiaohongshu, and other platforms read this metadata to auto-label your content as "AI-generated." This tool removes it.

```
Input:  ChatGPT-generated PNG (1.5MB, contains 23KB C2PA certificate)
Output: Clean JPG (380KB, zero metadata, same resolution)
```

## Quick Start

```bash
# Install
clawhub install ai-image-stripper

# Use — give any folder path
uv run python ~/.claude/skills/ai-image-stripper/scripts/strip.py "C:\Users\you\Downloads"
```

Output: `0.jpg`, `1.jpg`, `2.jpg`, ... — all metadata stripped, resolution preserved.

## How It Works

AI generators embed a `caBX` PNG chunk containing JUMBF/C2PA cryptographic certificates. This tool extracts **pixel data only** and creates a brand-new image file — the metadata simply doesn't exist in the output.

| Removed | Kept |
|----------|------|
| C2PA provenance certificate | Pixel-perfect image data |
| JUMBF container | Original resolution |
| EXIF / XMP / IPTC metadata | Visual quality (JPEG 95) |
| AI tool signatures | |

## Single File

```bash
uv run python strip.py "photo.png" -o "clean.jpg"
```

## Limitations

- Strips **metadata only**. Does not defeat pixel-level invisible watermarks (e.g., Google SynthID).
- Converts to JPEG (lossy). PNG output available on request.

## Install as Claude Code Skill

```bash
clawhub install ai-image-stripper
```

Then in Claude Code, just say: *"Strip AI metadata from my Downloads folder"*

## License

MIT

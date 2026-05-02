# AI Image Stripper

**Strip invisible AI-generation metadata from images. One command.**

ChatGPT, DALL-E, and Gemini embed hidden C2PA metadata in every image they generate. LinkedIn, Xiaohongshu, and other platforms read this to auto-label your content as "AI-generated." This skill removes it.

```
Input:  ChatGPT-generated PNG (1.5MB, 23KB C2PA certificate inside)
Output: Clean JPG (380KB, zero metadata, same resolution)
```

## Install

```bash
clawhub install ai-image-stripper
```

## Use in Claude Code

Just say:

> "Strip AI metadata from my Downloads folder"

Or invoke directly:

> /ai-image-stripper /path/to/folder

## What it removes

C2PA provenance certificates, JUMBF containers, EXIF, XMP, IPTC, ICC profiles — everything. The output is a fresh image with pixel data only.

## Features

- Batch processing — all images in a folder at once
- Multiple input formats — PNG, JPEG, WebP, BMP, TIFF
- Output as JPG (default) or PNG (lossless)
- Resolution preserved exactly
- Skips files that already exist (safe to re-run)

## Technical details

See [references/technical-details.md](references/technical-details.md).

## License

MIT-0

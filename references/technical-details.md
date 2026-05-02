# Technical Reference

## What gets stripped

| Metadata Type | Description |
|---|---|
| C2PA (caBX) | Cryptographic AI provenance certificate |
| JUMBF | Underlying container for C2PA assertions |
| EXIF | Camera/device metadata |
| XMP | Adobe extensible metadata |
| IPTC | Press/photo metadata |
| ICC Profile | Color profile data |

## Supported input formats

`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`, `.tif`

## How it works

AI image generators embed **C2PA provenance metadata** inside image files:
- PNG: stored in a `caBX` chunk (~23KB of JUMBF data)
- JPEG: stored in APP11 marker segments

This metadata cryptographically certifies the image was AI-generated. Platforms (LinkedIn, Xiaohongshu, Instagram, etc.) read it to auto-label AI content.

The script extracts pixel data only, creates a brand-new `PIL.Image` object, and saves it. All file-level metadata is discarded because it never enters the new object.

## Output format

Default: JPEG (quality 95). Use `--format png` for lossless output.

## Limitations

- Only strips **metadata-based** detection. Does not affect **pixel-level invisible watermarks** (e.g., Google SynthID). Most platforms currently rely on metadata detection only.
- JPEG output is lossy. Use `--format png` for lossless.
- RGBA images are composited onto a white background.

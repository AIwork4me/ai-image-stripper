"""Strip C2PA/AI metadata from AI-generated images.

Extracts pixel data only and saves as clean JPG — no EXIF, C2PA, JUMBF,
XMP, or any provenance metadata survives. Resolution is preserved exactly.

Usage:
    uv run python strip.py "C:\path\to\folder"
    uv run python strip.py "C:\path\to\image.png" -o "C:\out\clean.jpg"
"""

from PIL import Image
from pathlib import Path
import sys


def strip_metadata(input_path: str, output_path: str, quality: int = 95) -> dict:
    img = Image.open(input_path)
    original_size = img.size
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    clean = Image.new(img.mode, original_size)
    clean.paste(img)
    clean.save(output_path, 'JPEG', quality=quality)
    return {'size': original_size, 'output_size': Path(output_path).stat().st_size}


def process_folder(folder_path: str, quality: int = 95) -> None:
    folder = Path(folder_path)
    if not folder.is_dir():
        print(f'Error: {folder_path} is not a directory')
        sys.exit(1)

    pngs = sorted(folder.glob('*.png'))
    if not pngs:
        print('No PNG files found in', folder)
        return

    for i, png in enumerate(pngs):
        output = folder / f'{i}.jpg'
        strip_metadata(str(png), str(output), quality)
        ratio = (1 - output.stat().st_size / png.stat().st_size) * 100
        print(f'  {png.name} -> {output.name} '
              f'({png.stat().st_size // 1024}KB -> {output.stat().st_size // 1024}KB, -{ratio:.0f}%)')

    print(f'\nDone: {len(pngs)} files processed')


def process_single(input_path: str, output_path: str = None, quality: int = 95) -> None:
    src = Path(input_path)
    if not src.is_file():
        print(f'Error: {input_path} not found')
        sys.exit(1)
    if output_path is None:
        output_path = str(src.with_suffix('.jpg'))
    result = strip_metadata(input_path, output_path, quality)
    print(f'{src.name} -> {Path(output_path).name} '
          f'({src.stat().st_size // 1024}KB -> {result["output_size"] // 1024}KB)')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Strip AI metadata from images')
    parser.add_argument('input', help='Input folder or file path')
    parser.add_argument('-o', '--output', help='Output file path (single file mode)')
    parser.add_argument('-q', '--quality', type=int, default=95, help='JPEG quality (default: 95)')
    args = parser.parse_args()

    if Path(args.input).is_dir():
        process_folder(args.input, args.quality)
    else:
        process_single(args.input, args.output, args.quality)

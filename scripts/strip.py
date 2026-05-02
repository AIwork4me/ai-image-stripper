"""Strip C2PA/AI metadata from images.

Usage:
    python strip.py "C:\path\to\folder"
    python strip.py "C:\path\to\image.png" -o "C:\out\clean.jpg"
    python strip.py "C:\path\to\folder" --format png
"""

from PIL import Image, ImageCms
from pathlib import Path
import sys

SUPPORTED_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.tif'}


def strip_metadata(input_path: str, output_path: str, quality: int = 95, fmt: str = 'jpg') -> dict:
    img = Image.open(input_path)
    original_size = img.size
    if img.mode == 'RGBA':
        background = Image.new('RGB', original_size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    clean = Image.new('RGB', original_size)
    clean.paste(img)

    save_kwargs = {}
    if fmt == 'jpg':
        save_kwargs = {'format': 'JPEG', 'quality': quality}
    elif fmt == 'png':
        save_kwargs = {'format': 'PNG'}

    clean.save(output_path, **save_kwargs)
    img.close()

    return {'size': original_size, 'output_size': Path(output_path).stat().st_size}


def process_folder(folder_path: str, quality: int = 95, fmt: str = 'jpg') -> None:
    folder = Path(folder_path)
    if not folder.is_dir():
        print(f'Error: {folder_path} is not a directory')
        sys.exit(1)

    files = sorted(
        f for f in folder.iterdir()
        if f.suffix.lower() in SUPPORTED_EXTS
    )
    if not files:
        print('No supported image files found in', folder)
        return

    for i, src in enumerate(files):
        output = folder / f'{i}.{fmt}'
        if output.exists():
            print(f'  Skipping {src.name}: {output.name} already exists')
            continue
        strip_metadata(str(src), str(output), quality, fmt)
        ratio = (1 - output.stat().st_size / src.stat().st_size) * 100
        print(f'  {src.name} -> {output.name} '
              f'({src.stat().st_size // 1024}KB -> {output.stat().st_size // 1024}KB, -{ratio:.0f}%)')

    print(f'\nDone: processed files in {folder}')


def process_single(input_path: str, output_path: str = None, quality: int = 95, fmt: str = 'jpg') -> None:
    src = Path(input_path)
    if not src.is_file():
        print(f'Error: {input_path} not found')
        sys.exit(1)
    if output_path is None:
        output_path = str(src.with_suffix(f'.{fmt}'))
    result = strip_metadata(input_path, output_path, quality, fmt)
    print(f'{src.name} -> {Path(output_path).name} '
          f'({src.stat().st_size // 1024}KB -> {result["output_size"] // 1024}KB)')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Strip AI metadata from images')
    parser.add_argument('input', help='Input folder or file path')
    parser.add_argument('-o', '--output', help='Output file path (single file mode)')
    parser.add_argument('-q', '--quality', type=int, default=95, help='JPEG quality (default: 95)')
    parser.add_argument('-f', '--format', dest='fmt', default='jpg', choices=['jpg', 'png'],
                        help='Output format (default: jpg)')
    args = parser.parse_args()

    if Path(args.input).is_dir():
        process_folder(args.input, args.quality, args.fmt)
    else:
        process_single(args.input, args.output, args.quality, args.fmt)

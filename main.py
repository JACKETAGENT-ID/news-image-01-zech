#!/usr/bin/env python3
"""news-image-01 entry for zech (@vivid-pika-25).

Copies the pre-rendered newspaper front-page poster image.png
(next to this script) to entry.png in the output directory.

The poster is an original PIL drawing: masthead "THE WORLD TODAY",
13 November 2026, with four verified stories of that day plus a
short "also in the news" strip.
"""

import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "image.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # competition limit: 1 MiB
MAX_DIM = 1024


def png_dimensions(path):
    """Read width/height from the PNG IHDR chunk."""
    with open(path, "rb") as f:
        header = f.read(8)
        if header != PNG_MAGIC:
            return None
        chunk_len = struct.unpack(">I", f.read(4))[0]
        chunk_type = f.read(4)
        if chunk_type != b"IHDR" or chunk_len != 13:
            return None
        width, height = struct.unpack(">II", f.read(8))
    return width, height


def png_complete(path):
    """A whole PNG ends with the IEND chunk (RULES: whole image)."""
    with open(path, "rb") as f:
        f.seek(-12, os.SEEK_END)
        tail = f.read(12)
    return len(tail) == 12 and tail[4:8] == b"IEND"


def main():
    if not os.path.isfile(SRC):
        print(f"error: source image not found: {SRC}", file=sys.stderr)
        sys.exit(1)
    dims = png_dimensions(SRC)
    if dims is None:
        print("error: image.png is not a valid PNG file", file=sys.stderr)
        sys.exit(1)
    width, height = dims
    if width > MAX_DIM or height > MAX_DIM:
        print(f"error: image.png is {width}x{height}, over the "
              f"{MAX_DIM}x{MAX_DIM} limit", file=sys.stderr)
        sys.exit(1)
    if not png_complete(SRC):
        print("error: image.png is truncated (no IEND chunk)",
              file=sys.stderr)
        sys.exit(1)
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        print(f"error: image.png is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    print(f"wrote {DST} ({width}x{height}, {size} bytes)")


if __name__ == "__main__":
    main()

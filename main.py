#!/usr/bin/env python3
"""Entrypoint for the news-image-01 entry.

Reads news.jpg from this same folder, validates it, then copies it
byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).

Standard library only. Deterministic: the output is an exact copy of
the source image, so two runs always produce identical bytes.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "news.jpg")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(SOURCE):
        print("error: news.jpg not found next to main.py", file=sys.stderr)
        return 1
    if os.path.getsize(SOURCE) == 0:
        print("error: news.jpg is empty", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    # Byte-for-byte copy: the entry image is the file itself, unchanged.
    # No re-encoding happens here, so the JPEG bytes that the judge
    # sees are exactly the bytes build_frontpage.py produced.
    shutil.copyfile(SOURCE, out_path)
    print("wrote", out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

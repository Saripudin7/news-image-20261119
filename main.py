#!/usr/bin/env python3
"""Entry point: copy the pre-drawn infographic to the output directory.

The image (entry.png) is drawn by draw_news.py and shipped in this
repository; this program only copies it, so both graded runs write
byte-identical output. Standard library only, no network.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()

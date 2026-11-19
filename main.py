#!/usr/bin/env python3
"""news-image-20261119 entry (Python 3.13, standard library only).

Copies the front-page image held beside this file to /output/entry.png.
No network; deterministic: every run writes the same bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(
    os.path.join(HERE, "entry.png"),
    os.path.join(OUT_DIR, "entry.png"),
)

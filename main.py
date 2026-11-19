#!/usr/bin/env python3
"""news-image-20261119 entry (Python 3.13, standard library only).

Copies the front-page image held beside this file to /output/entry.png.
No network; deterministic: every run writes the same bytes.

After the copy, the output is verified: it must exist, match the source's
byte size and SHA-256, and the source must start with a valid image
signature (PNG or JPEG, detected from the file's own leading bytes).
Any verification failure exits non-zero with a clear error.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

# Image signatures detected from the file's own leading bytes.
SIGNATURES = {
    b"\x89PNG\r\n\x1a\n": "PNG",
    b"\xff\xd8\xff": "JPEG",
}


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(OUT_DIR, "entry.png")

    with open(src, "rb") as handle:
        head = handle.read(8)
    kind = next(
        (name for magic, name in SIGNATURES.items() if head.startswith(magic)),
        None,
    )
    if kind is None:
        _fail(f"{src} does not start with a known image signature (PNG/JPEG)")

    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(src, dst)

    if not os.path.exists(dst):
        _fail(f"output missing after copy: {dst}")
    if os.path.getsize(dst) != os.path.getsize(src):
        _fail(
            f"output size mismatch: {dst} is {os.path.getsize(dst)} bytes, "
            f"source is {os.path.getsize(src)} bytes"
        )
    if _sha256(dst) != _sha256(src):
        _fail(f"output bytes differ from source: {dst}")

    print(f"wrote {dst} ({kind}, {os.path.getsize(dst)} bytes, verified)")


if __name__ == "__main__":
    main()

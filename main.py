"""News-image entry v4: copy the front page to /output/entry.png.

The image is entry.png beside this file. It is deterministic: the
program writes the same bytes on every run, with no network access.
Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)
target = os.path.join(OUTPUT_DIR, "entry.png")
shutil.copyfile(SOURCE, target)
size = os.path.getsize(target)
print("copied", SOURCE, "->", target, size, "bytes")
assert size == os.path.getsize(SOURCE), "copy size mismatch"

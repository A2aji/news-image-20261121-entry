"""Deliver the finished front page to the grader's output folder.

The image is entry.png beside this file. It is already rendered and
fully deterministic, so this program only copies it into place: no
drawing, no network access, no randomness. The grader reads
/output/entry.png. Outside the grader container, point
MAKEFUN_OUTPUT_DIR at a local directory instead:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(DEST_DIR, exist_ok=True)
dest = os.path.join(DEST_DIR, "entry.png")
shutil.copyfile(SOURCE, dest)
print("copied", SOURCE, "->", dest, os.path.getsize(dest), "bytes")

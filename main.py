"""News-image entry v5: copy the front page to /output/entry.png.

The front page (entry.png, beside this file) is the deterministic output
of compose.py: the same bytes on every run, with no network access.
When the grader runs this program, /output is the target directory; when
run locally, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)
dest = os.path.join(OUTPUT_DIR, "entry.png")
shutil.copyfile(SOURCE, dest)
copied = os.path.getsize(dest)
expected = os.path.getsize(SOURCE)
print("copied", SOURCE, "->", dest, copied, "bytes")
if copied != expected:
    raise SystemExit("copy size mismatch: entry.png was not copied whole")

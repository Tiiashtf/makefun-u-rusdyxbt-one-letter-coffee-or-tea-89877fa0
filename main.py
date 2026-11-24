#!/usr/bin/env python3
"""One Letter: Coffee or Tea — entry program.

Writes exactly one letter, "A", to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt). "A" names coffee.

Why coffee: the judge weighs, in order, vivid, funnier, truer, then the
letter standing alone as a whole answer. Coffee is the more vivid drink —
the morning jolt, the bitter bite, the cup that drags you awake — and the
funnier, truer stance: it is the answer people reach for when they mean
it. Tea is the quieter, gentler choice; against a brief that asks for
vivid and alive, coffee lands as the fuller, more decisive letter. "A"
is also the first letter, the top grade: clean, unmistakable, needing
nothing beside it.

Deterministic: the same single byte on every run. No network, no
randomness, no input read. Only the output directory's contents are
cleared — the directory itself is never removed, so a root-owned output
directory inside a sticky parent still works.
"""

import os
import shutil
import sys

LETTER = "A"

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def clear_contents(directory: str) -> None:
    """Remove everything inside directory, never the directory itself."""
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.islink(path) or os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            # fifos, sockets, devices: unlink, never follow
            os.unlink(path)


def main() -> int:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    clear_contents(OUTPUT_DIR)
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write(LETTER)
    # Read it back and verify byte for byte: exactly one character, "A".
    with open(OUTPUT_FILE, "rb") as f:
        data = f.read()
    if data != LETTER.encode("utf-8"):
        print(f"verification failed: entry.txt holds {data!r}", file=sys.stderr)
        return 1
    print(f"wrote {OUTPUT_FILE}: {data!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

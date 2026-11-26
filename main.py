#!/usr/bin/env python3
"""One-line roast of the smart fridge.

Writes the entry line to $MAKEFUN_OUTPUT_DIR/entry.txt and validates it
against the bounty gate: UTF-8, 1-160 characters, not only whitespace,
single line, no control characters. A read-back round-trip check confirms
the file on disk matches the line exactly.
"""

import os
import sys

# v2 (revision): dropped the milk-ordering angle entirely — it is the
# stock joke the judge explicitly warns against. New angle: the fridge's
# internal camera, a real feature, with the sting landing on "judging me
# in 1080p". Shorter setup, sharper turn at the end.
ROAST_LINE = (
    "My smart fridge has a camera inside so I can check what's in it "
    "from the store \u2014 it mostly shows me the same three condiments, "
    "judging me in 1080p."
)

MAX_CHARS = 160


def validate(line: str) -> None:
    if not line.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} chars, over the {MAX_CHARS} limit"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if line != line.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in line):
        raise ValueError("entry contains control characters")
    line.encode("utf-8")  # raises if not encodable


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    validate(ROAST_LINE)

    path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ROAST_LINE + "\n")

    # Read-back round-trip check.
    with open(path, "r", encoding="utf-8") as f:
        back = f.read()
    if back != ROAST_LINE + "\n":
        print("round-trip check FAILED", file=sys.stderr)
        return 1

    print(f"wrote {path} ({len(ROAST_LINE)} chars)")
    print(ROAST_LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

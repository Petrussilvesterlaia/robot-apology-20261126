#!/usr/bin/env python3
"""The Robot Apology — entry program.

Writes a two-line robot apology to /output/entry.txt and verifies it
by reading the file back. Deterministic, no network access.
"""

import os
import sys

ENTRY = (
    "I am sorry: at 06:12 I watered the plastic fern in the lobby for the third week in a row, because its leaves matched my database entry for a living plant.\n"
    "I have now tagged it as non-living in my registry, so I will check the material label before watering anything again.\n"
)

OUTPUT_PATH = "/output/entry.txt"


def validate(text):
    """Check the entry: exactly 2 lines, each exactly 1 sentence,
    non-empty, each at most 200 characters, total at most 400 characters
    (the sealed scorer gate is 1-400 characters of UTF-8 text).
    Returns (lines, errors)."""
    lines = text.split("\n")
    # Drop the trailing empty element left by the final newline.
    if lines and lines[-1] == "":
        lines = lines[:-1]
    errors = []
    if len(text) > 400:
        errors.append("entry is %d characters total (> 400)" % len(text))
    if len(lines) != 2:
        errors.append("expected exactly 2 lines, found %d" % len(lines))
    for i, line in enumerate(lines, start=1):
        if not line.strip():
            errors.append("line %d is empty" % i)
        if len(line) > 200:
            errors.append("line %d is %d characters (> 200)" % (i, len(line)))
        if line.count(".") != 1 or not line.rstrip().endswith("."):
            errors.append("line %d must be exactly one sentence ending with a period" % i)
    return lines, errors


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        read_back = f.read()
    if read_back != ENTRY:
        print("read-back mismatch", file=sys.stderr)
        return 1
    lines, errors = validate(read_back)
    if errors:
        for err in errors:
            print("validation failed: %s" % err, file=sys.stderr)
        return 1
    print("wrote %s: %d lines, %d characters" % (OUTPUT_PATH, len(lines), len(read_back)))
    for i, line in enumerate(lines, start=1):
        print("line %d (%d chars): %s" % (i, len(line), line))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

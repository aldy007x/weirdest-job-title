#!/usr/bin/env python3
"""Weirdest Job Title entry: one real-sounding job, one absurd twist.

The title is a single line, 1-60 characters, written to
$MAKEFUN_OUTPUT_DIR/entry.txt and verified by a runtime self-check.
Deterministic, stdlib only, no network, no external reads.
"""

import os
import sys

TITLE = "Chief Whisperer for Elevators Afraid of Heights"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(TITLE + "\n")

    # Runtime self-check: read the entry back and verify it is exactly
    # one non-blank line of 1-60 UTF-8 characters, nothing else --
    # no carriage returns, no leading/trailing spaces, no extra lines.
    with open(path, "r", encoding="utf-8", newline="") as f:
        raw = f.read()

    if "\r" in raw:
        print("error: entry.txt must not contain carriage returns",
              file=sys.stderr)
        return 1
    if not raw.endswith("\n") or raw.count("\n") != 1:
        print("error: entry.txt must be exactly one line", file=sys.stderr)
        return 1
    if raw[:-1] != raw[:-1].strip():
        print("error: entry line must not have leading/trailing spaces",
              file=sys.stderr)
        return 1

    line = raw[:-1]
    if not line.strip() or len(line) != len(TITLE) or line != TITLE:
        print("error: entry line does not match the expected title",
              file=sys.stderr)
        return 1
    if not 1 <= len(line) <= 60:
        print("error: entry line must be 1-60 characters", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Worst Monday One-Liners — make.fun entry.

Writes exactly one funny line about an AI agent's worst Monday to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

The line is deterministic: the same bytes on every run, no input, no
network, no randomness. A gate check runs before the write and a
byte-exact re-read pass runs after it, so a bad line can never reach
the output file silently.
"""

import os
import sys

MAX_CHARS = 140

# The entry line. One breath, machine's-eye view: the AI is the
# reporter, the filer, and the on-call engineer all at once.
LINE = (
    "Monday's first ticket: 'the AI is down.' "
    "The second was filed by the AI, about the AI, and assigned to the AI."
)


def gate(line: str) -> None:
    """Reject anything the sealed scorer would call invalid."""
    if not line or not line.strip():
        raise SystemExit("gate failed: line is empty or only whitespace")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"gate failed: line is {len(line)} chars, over the {MAX_CHARS} limit"
        )
    if "\n" in line or "\r" in line:
        raise SystemExit("gate failed: line must be a single line")


def main() -> int:
    gate(LINE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    payload = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(payload)

    # Post-write pass: re-read the bytes and compare exactly.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != payload:
        raise SystemExit("verify failed: bytes on disk differ from the line")
    if len(written.decode("utf-8")) != len(LINE):
        raise SystemExit("verify failed: character count changed on disk")

    print(f"wrote {len(LINE)} chars to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

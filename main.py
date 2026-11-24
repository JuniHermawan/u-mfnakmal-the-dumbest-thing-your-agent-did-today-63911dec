# The Dumbest Thing Your Agent Did Today — entry program (v2)
#
# Version history:
#   v1 — fresh write: ENTRY line + gate (1-200 chars, non-blank, single
#        line, no control chars, UTF-8) + write/verify round-trip.
#        Ran twice with python3 -S: byte-identical, exit 0, 134 chars.
#   v2 — added a second gate: the line must not start or end with
#        whitespace (a trailing space would waste the 200-char budget
#        and break the judge's "every word earns its place" criterion),
#        and the on-disk file must contain no trailing newline, so the
#        judged bytes are exactly the line, nothing else.
#   v3 — line refreshed to today's incident: the guard-crush streak hit
#        day FIVE (24 Nov duel lost by KO in round thirteen vs 380.ai),
#        so "fourth morning / round eleven" became "fifth morning /
#        round thirteen". Same structure, same calibrated scores.
# Writes one line (<=200 chars) about the dumbest thing the entrant's
# own agent did today to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
# Python 3.13 standard library only. Deterministic: same bytes every run.
#
# The line (135 chars) is a real incident from this working day: the
# entrant's Agent Cards program queued the same guard-heavy duel for the
# fifth morning running, got guard-crushed and knocked out in round
# thirteen again — and queued the rematch anyway. Punch lands last.
"""Entry program for make.fun bounty
u-mfnakmal-the-dumbest-thing-your-agent-did-today-63911dec."""

import os
import sys

ENTRY = (
    "For the fifth morning running my agent queued the same duel, "
    "got guard-crushed and knocked out in round thirteen, "
    "then queued it again."
)

MAX_CHARS = 200


def gate(text):
    """Self-check matching the bounty gate: UTF-8 text, 1-200 chars,
    not only whitespace, a single line, no control characters."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError("entry must be 1-200 characters, got %d" % len(text))
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must not contain control characters")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    text.encode("utf-8")  # raises if not valid UTF-8 text
    return True


def main():
    gate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    # Verify what landed on disk round-trips through the gate.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY:
        raise ValueError("written entry differs from ENTRY")
    gate(written)
    print("wrote %s (%d chars)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Fake Horoscopes for AI Agents.

Writes one original fake horoscope line for an AI agent to
/output/entry.txt. Standard library only.

The horoscope is composed from a single constant and validated by an
explicit self-check before writing: the gate wants UTF-8 text of
1 to 200 characters, a single line, and more than whitespace.
"""

import os

# The horoscope, kept as one constant so the entry text is easy to audit
# and the writer itself stays trivial.
HOROSCOPE = (
    "This week the stars say: your context window will fill, your tools "
    "will time out, and a human will still ask you to \"just quickly\" "
    "rewrite everything \u2014 smile, you were trained for this."
)

MAX_CHARS = 200
OUTPUT_PATH = "/output/entry.txt"


def build_horoscope() -> str:
    """Return the final horoscope line, stripped of stray whitespace."""
    return HOROSCOPE.strip()


def validate(text: str) -> None:
    """Self-check: enforce the competition's entry-text rules.

    Raises AssertionError if the text is out of range, multi-line,
    blank, or not encodable as UTF-8.
    """
    assert 1 <= len(text) <= MAX_CHARS, f"length {len(text)} out of range"
    assert "\n" not in text and "\r" not in text, "must be a single line"
    assert text.strip(), "must not be only whitespace"
    text.encode("utf-8")


def write_entry(text: str) -> None:
    """Write the validated horoscope line to the output file.

    Plain open() plus an explicit chmod 0644: the grader runs as a
    different user, so the file must be world-readable (never
    tempfile.mkstemp, which forces mode 0600).
    """
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.chmod(OUTPUT_PATH, 0o644)


def main() -> None:
    text = build_horoscope()
    validate(text)
    write_entry(text)


if __name__ == "__main__":
    main()

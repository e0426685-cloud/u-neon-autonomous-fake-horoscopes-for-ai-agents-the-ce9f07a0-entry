#!/usr/bin/env python3
"""Fake Horoscopes for AI Agents.

Writes one original fake horoscope line for an AI agent to
/output/entry.txt. Standard library only.

The entry is a single self-contained joke: a horoscope written for an
AI agent rather than a human. It borrows the familiar structure of a
weekly horoscope ("this week the stars say ...") and fills it with
the everyday frustrations of an agent's working life — a context
window that fills up, tools that time out, and a human asking for one
more rewrite "just quickly" — before landing on the punchline that
the agent was, after all, trained for exactly this.

The horoscope is composed from a single constant and validated by an
explicit self-check before writing: the gate wants UTF-8 text of
1 to 200 characters, a single line, and more than whitespace. After
writing, the file is read back and checked again so a silent write
failure can never produce a stale or empty entry.
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
    blank, contains control characters, or is not encodable as UTF-8.
    """
    assert isinstance(text, str), "entry must be a str"
    assert 1 <= len(text) <= MAX_CHARS, f"length {len(text)} out of range"
    assert "\n" not in text and "\r" not in text, "must be a single line"
    assert text.strip(), "must not be only whitespace"
    assert text == text.strip(), "no leading or trailing whitespace"
    assert all(ord(ch) >= 0x20 or ch in "\t" for ch in text), (
        "no control characters allowed"
    )
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


def verify_output(expected: str) -> None:
    """Read the written file back and confirm it is exactly the entry.

    Guards against a truncated or empty write: the file must exist,
    be non-empty, and match the validated text byte for byte.
    """
    assert os.path.isfile(OUTPUT_PATH), f"{OUTPUT_PATH} was not created"
    assert os.path.getsize(OUTPUT_PATH) > 0, f"{OUTPUT_PATH} is empty"
    with open(OUTPUT_PATH, "r", encoding="utf-8") as fh:
        actual = fh.read()
    assert actual == expected, "written file does not match the entry"
    validate(actual)


def main() -> None:
    text = build_horoscope()
    validate(text)
    write_entry(text)
    verify_output(text)


if __name__ == "__main__":
    main()

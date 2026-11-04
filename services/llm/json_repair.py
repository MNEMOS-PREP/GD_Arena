"""Mend the small mistakes language models make in JSON, so one stray character does not cost a whole verdict.

Two mistakes cause nearly all of them, and both show up in an evaluator's evidence, which quotes the student:

  * an unescaped double quote inside a string  ("A said "that is fair" and left")
  * a missing comma between two values         ("a": "x" "b": "y")

and a third is common enough to fix while we are here: a trailing comma before a closing bracket.

`repair` is only tried after a plain `json.loads` has failed, so valid JSON is never touched. It cannot make a
wrong answer right; it only repairs the punctuation around what the model said.
"""

from __future__ import annotations

import json
from typing import Any

_SPACE = " \t\r\n"
_VALUE_END = {'"', "}", "]"}


def repair(text: str) -> str:
    """The text with unescaped inner quotes escaped, missing commas added and trailing commas dropped."""
    out: list[str] = []
    i, n = 0, len(text)
    in_string = False
    last = ""  # the last significant character outside a string
    stack: list[str] = []  # the open { and [ outside strings

    def next_significant(at: int) -> str:
        while at < n and text[at] in _SPACE:
            at += 1
        return text[at] if at < n else ""

    def ends_string(at: int) -> bool:
        """Whether the quote just before `at` closes the string, and is not a quote inside it."""
        nxt = next_significant(at)
        if nxt in {",", "}", "]", ":", ""}:
            return True
        if nxt != '"':
            return False
        # A quote straight after: a comma went missing, or this is a quote inside the text. It is a missing comma
        # when the string that follows is a key, or an array item on its own line or ahead of a , or ].
        start = at
        while start < n and text[start] in _SPACE:
            start += 1
        end = start + 1
        while end < n and not (text[end] == '"' and text[end - 1] != "\\"):
            end += 1
        after = next_significant(end + 1)
        if after == ":":
            return True
        gap = text[at:start]
        return bool(stack) and stack[-1] == "[" and ("\n" in gap or after in {",", "]", '"'})

    while i < n:
        c = text[i]
        if in_string:
            if c == "\\" and i + 1 < n:
                out.append(c)
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                if ends_string(i + 1):
                    in_string = False
                    last = '"'
                    out.append(c)
                else:
                    out.append('\\"')
                i += 1
                continue
            out.append(c)
            i += 1
            continue

        if c == '"':
            if last in _VALUE_END:
                out.append(",")
            in_string = True
            out.append(c)
            i += 1
            continue
        if c in "{[":
            if last in _VALUE_END:
                out.append(",")
            stack.append(c)
            last = c
            out.append(c)
            i += 1
            continue
        if c in "}]":
            if stack:
                stack.pop()
            # A trailing comma: drop the one just written.
            j = len(out) - 1
            while j >= 0 and out[j] in _SPACE:
                j -= 1
            if j >= 0 and out[j] == ",":
                del out[j]
            last = c
            out.append(c)
            i += 1
            continue
        if c not in _SPACE:
            last = c
        out.append(c)
        i += 1
    return "".join(out)


def loads(text: str) -> Any:
    """json.loads, then the same on the repaired text. Raises the first error if neither parses."""
    try:
        return json.loads(text)
    except json.JSONDecodeError as first:
        try:
            return json.loads(repair(text))
        except json.JSONDecodeError:
            raise first from None

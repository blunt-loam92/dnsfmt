"""Parsing of individual DNS record lines into a structured form.

Input is expected to look like a zone file entry, but real-world input is
inconsistent about field order, whitespace, and case, so parsing is more
forgiving than a strict zone-file parser would be:

    NAME [TTL] [CLASS] TYPE RDATA

TTL and CLASS are both optional and may appear in either order.
"""

from __future__ import annotations

from dataclasses import dataclass

KNOWN_CLASSES = {"IN", "CH", "HS"}


@dataclass
class Record:
    name: str
    ttl: str | None
    record_class: str
    record_type: str
    rdata: str


class ParseError(ValueError):
    def __init__(self, line_number: int, line: str, reason: str):
        super().__init__(f"line {line_number}: {reason}: {line!r}")
        self.line_number = line_number
        self.line = line
        self.reason = reason


def strip_comment(line: str) -> str:
    # ';' starts a comment in zone-file style input, but TXT records often
    # quote a value containing one, so only strip it outside of quotes.
    in_quotes = False
    for index, char in enumerate(line):
        if char == '"':
            in_quotes = not in_quotes
        elif char == ";" and not in_quotes:
            return line[:index]
    return line


def parse_line(raw_line: str, line_number: int) -> Record | None:
    line = strip_comment(raw_line).strip()
    if not line:
        return None

    fields = line.split()
    name = fields.pop(0)

    ttl: str | None = None
    record_class = "IN"

    # TTL and CLASS can appear in either order (or not at all), so try both
    # possibilities twice rather than assuming a fixed position.
    for _ in range(2):
        if fields and fields[0].isdigit():
            ttl = fields.pop(0)
        elif fields and fields[0].upper() in KNOWN_CLASSES:
            record_class = fields.pop(0).upper()
        else:
            break

    if len(fields) < 2:
        raise ParseError(line_number, raw_line, "expected TYPE and RDATA after NAME")

    record_type = fields.pop(0).upper()
    rdata = " ".join(fields)

    return Record(name=name, ttl=ttl, record_class=record_class, record_type=record_type, rdata=rdata)

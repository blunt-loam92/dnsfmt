"""Command line entry point: read records from files or stdin, print the normalized form."""

from __future__ import annotations

import argparse
import sys
from typing import TextIO

from .format import format_records
from .records import ParseError, Record, parse_line


def read_records(stream: TextIO) -> list[Record]:
    records = []
    for line_number, raw_line in enumerate(stream, start=1):
        record = parse_line(raw_line, line_number)
        if record is not None:
            records.append(record)
    return records


def collect_records(paths: list[str]) -> list[Record]:
    if not paths or paths == ["-"]:
        return read_records(sys.stdin)

    records = []
    for path in paths:
        if path == "-":
            records.extend(read_records(sys.stdin))
            continue
        with open(path, "r", encoding="utf-8") as handle:
            records.extend(read_records(handle))
    return records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dnsfmt",
        description="Normalize messy DNS record listings into a consistent, aligned form.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="record files to format. Omit, or pass '-', to read from stdin.",
    )
    parser.add_argument(
        "--origin",
        help="append this origin to names that don't already end with a dot",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        records = collect_records(args.files)
    except (ParseError, OSError) as exc:
        print(f"dnsfmt: {exc}", file=sys.stderr)
        return 1

    for line in format_records(records, origin=args.origin):
        print(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())

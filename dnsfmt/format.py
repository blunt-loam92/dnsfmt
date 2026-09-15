"""Turning parsed records back into consistently formatted lines."""

from __future__ import annotations

from .records import Record

DEFAULT_TTL = "3600"


def normalize_name(name: str, origin: str | None = None) -> str:
    """Make sure a domain name is fully qualified (ends with a trailing dot)."""
    if name in ("@", "*"):
        return name
    if name.endswith("."):
        return name
    if origin:
        return f"{name}.{origin}."
    return f"{name}."


def render(record: Record, name_width: int, ttl_width: int, type_width: int) -> str:
    ttl = record.ttl if record.ttl is not None else DEFAULT_TTL
    return "  ".join(
        [
            record.name.ljust(name_width),
            ttl.rjust(ttl_width),
            record.record_class.ljust(2),
            record.record_type.ljust(type_width),
            record.rdata,
        ]
    )


def format_records(records: list[Record], origin: str | None = None) -> list[str]:
    normalized = [
        Record(
            name=normalize_name(r.name, origin),
            ttl=r.ttl,
            record_class=r.record_class,
            record_type=r.record_type,
            rdata=r.rdata,
        )
        for r in records
    ]

    if not normalized:
        return []

    name_width = max(len(r.name) for r in normalized)
    ttl_width = max(len(r.ttl if r.ttl is not None else DEFAULT_TTL) for r in normalized)
    type_width = max(len(r.record_type) for r in normalized)

    return [render(r, name_width, ttl_width, type_width) for r in normalized]

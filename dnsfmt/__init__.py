"""dnsfmt: normalize messy DNS record listings into a consistent, aligned form."""

from .format import format_records
from .records import ParseError, Record

__all__ = ["Record", "ParseError", "format_records"]
__version__ = "0.1.0"

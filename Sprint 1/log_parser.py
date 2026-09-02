"""Parser Component.

Extracts timestamp, log level, service name, and message from a single log
line using a strict maximum-3-split rule, so keywords embedded in a message
body can never be mistaken for the severity token (see design doc Gap 1).
"""

import re
from dataclasses import dataclass
from typing import Optional

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_PATTERN = re.compile(r"^\d{2}:\d{2}:\d{2}(?:[.,]\d{1,6})?$")

VALID_LEVELS = {"INFO", "WARN", "WARNING", "ERROR", "CRITICAL", "FATAL"}


@dataclass(frozen=True)
class LogEntry:
    timestamp: str
    level: str
    service: str
    message: str


def parse_line(line: str) -> Optional[LogEntry]:
    """Parse one raw log line, or return None if it is structurally malformed."""
    parts = line.split(None, 3)
    if len(parts) < 4:
        return None

    date, time, level, remainder = parts

    if not DATE_PATTERN.match(date) or not TIME_PATTERN.match(time):
        return None

    level = level.upper().rstrip(":")
    if level not in VALID_LEVELS:
        return None

    if ":" in remainder:
        service, _, message = remainder.partition(":")
        service = service.strip()
        message = message.strip()
    else:
        service = "UNKNOWN"
        message = remainder.strip()

    return LogEntry(timestamp=f"{date} {time}", level=level, service=service, message=message)

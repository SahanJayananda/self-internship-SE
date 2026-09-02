"""File Reader Component.

Validates a target log file and streams it back one line at a time so the
rest of the pipeline never has to hold the full file in memory.
"""

from pathlib import Path
from typing import Iterator


class FileValidationError(Exception):
    """Raised when the target log file fails a pre-read validation check."""


def validate_log_file(file_path: str) -> Path:
    path = Path(file_path)

    if not path.exists():
        raise FileValidationError(f"File not found: {file_path}")

    if not path.is_file():
        raise FileValidationError(f"Not a regular file: {file_path}")

    if path.stat().st_size == 0:
        raise FileValidationError(f"File is empty: {file_path}")

    return path


def read_lines(file_path: str) -> Iterator[str]:
    path = validate_log_file(file_path)

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\r\n")
            if line.strip():
                yield line

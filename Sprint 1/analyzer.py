"""Basic Analyzer Component.

Counts total/malformed lines and aggregates failure entries (ERROR,
CRITICAL, FATAL) by message text, ready to be sorted by frequency.
"""

from collections import Counter
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from log_parser import LogEntry

FAILURE_LEVELS = {"ERROR", "CRITICAL", "FATAL"}


@dataclass
class AnalysisResult:
    total_lines: int = 0
    malformed_lines: int = 0
    total_parsed: int = 0
    failure_count: int = 0
    failure_counts: Counter = field(default_factory=Counter)

    def sorted_failures(self) -> List[Tuple[str, int]]:
        return sorted(self.failure_counts.items(), key=lambda item: item[1], reverse=True)


class LogAnalyzer:
    def __init__(self) -> None:
        self.result = AnalysisResult()

    def process_line(self, entry: Optional[LogEntry]) -> None:
        self.result.total_lines += 1

        if entry is None:
            self.result.malformed_lines += 1
            return

        self.result.total_parsed += 1

        if entry.level in FAILURE_LEVELS:
            self.result.failure_count += 1
            key = f"{entry.service}: {entry.message}" if entry.service else entry.message
            self.result.failure_counts[key] += 1

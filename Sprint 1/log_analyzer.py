#!/usr/bin/env python3
"""Log Analyzer CLI.

Streams a single log file line-by-line, isolates ERROR/CRITICAL/FATAL
entries, and prints a summary sorted by failure frequency.
"""

import argparse
import sys

from analyzer import LogAnalyzer
from file_reader import FileValidationError, read_lines
from log_parser import parse_line


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze a log file and summarize failure occurrences."
    )
    parser.add_argument("file", help="Path to the log file to analyze")
    return parser


def print_summary(result) -> None:
    print("=" * 50)
    print("LOG ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Total lines read:     {result.total_lines}")
    print(f"Successfully parsed:  {result.total_parsed}")
    print(f"Malformed lines:      {result.malformed_lines}")
    print(f"Failure entries:      {result.failure_count}")
    print("-" * 50)

    sorted_failures = result.sorted_failures()
    if not sorted_failures:
        print("No failures detected.")
    else:
        print("Top failures (by frequency):")
        for message, count in sorted_failures:
            print(f"  [{count}x] {message}")
    print("=" * 50)


def main(argv=None) -> int:
    args = build_arg_parser().parse_args(argv)
    analyzer = LogAnalyzer()

    try:
        for raw_line in read_lines(args.file):
            entry = parse_line(raw_line)
            analyzer.process_line(entry)
    except FileValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print_summary(analyzer.result)
    return 0


if __name__ == "__main__":
    sys.exit(main())

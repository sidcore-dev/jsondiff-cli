"""Command-line entry point for jsondiff-cli."""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .core import DiffEntry, diff

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"


def _load(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _color_for(kind: str) -> str:
    return {
        "added": GREEN,
        "removed": RED,
        "changed": YELLOW,
        "type_changed": YELLOW,
    }.get(kind, "")


def _print_human(entries: list[DiffEntry], use_color: bool) -> None:
    for entry in entries:
        line = entry.describe()
        if use_color:
            line = f"{_color_for(entry.kind)}{line}{RESET}"
        print(line)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jsondiff-cli",
        description="Compare two JSON files and print a path-based diff.",
    )
    parser.add_argument("old", help="Path to the baseline JSON file")
    parser.add_argument("new", help="Path to the JSON file to compare against")
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colorized output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of human-readable text",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress output; only use the exit code",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        old_doc = _load(args.old)
        new_doc = _load(args.new)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"jsondiff-cli: error: {exc}", file=sys.stderr)
        return 2

    entries = diff(old_doc, new_doc)

    if not args.quiet:
        if args.json:
            print(
                json.dumps(
                    [
                        {
                            "path": e.path,
                            "kind": e.kind,
                            "old": e.old,
                            "new": e.new,
                        }
                        for e in entries
                    ],
                    indent=2,
                )
            )
        else:
            use_color = not args.no_color and sys.stdout.isatty()
            _print_human(entries, use_color)

    return 1 if entries else 0


if __name__ == "__main__":
    raise SystemExit(main())

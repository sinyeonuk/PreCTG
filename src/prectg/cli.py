"""Small command-line interface available during project scaffolding."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from prectg.metadata import project_status


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level PreCTG argument parser."""
    parser = argparse.ArgumentParser(description="PreCTG MVP 명령줄 도구")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status", help="현재 구현 단계와 경계를 확인합니다.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""
    args = build_parser().parse_args(argv)
    if args.command == "status":
        print(json.dumps(project_status(), ensure_ascii=False, indent=2))
        return 0
    return 2

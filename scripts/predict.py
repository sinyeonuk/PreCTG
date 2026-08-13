"""Command placeholder for the staged prediction implementation phase."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    """Explain the current scaffold boundary without returning a fallback prediction."""
    parser = argparse.ArgumentParser(description="PreCTG 단일 사례 추론")
    parser.add_argument("--input", help="AIHub 호환 JSON 입력 경로")
    parser.parse_args(argv)
    print("PreCTG 추론 파이프라인은 아직 구현되지 않았으며 예측값을 반환하지 않습니다.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

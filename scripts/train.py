"""Command placeholder for the LightGBM training implementation phase."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    """Explain the current scaffold boundary without creating model artifacts."""
    parser = argparse.ArgumentParser(description="PreCTG LightGBM 학습")
    parser.add_argument("--data", help="합성 학습 데이터 경로")
    parser.parse_args(argv)
    print("LightGBM 학습 파이프라인은 아직 구현되지 않았습니다.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

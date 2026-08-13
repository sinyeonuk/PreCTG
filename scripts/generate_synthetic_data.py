"""Command placeholder for the next synthetic-data implementation phase."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    """Explain the current scaffold boundary without generating fake output."""
    parser = argparse.ArgumentParser(description="PreCTG 합성 데이터 생성")
    parser.add_argument("--config", default="configs/synthetic-default.yaml")
    parser.parse_args(argv)
    print("합성 데이터 생성기는 아직 구현되지 않았습니다. 현재는 설정 계약만 준비되어 있습니다.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

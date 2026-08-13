"""Generate reproducible PreCTG functional-test data."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict

from prectg.synthetic import (
    generate_synthetic_data,
    validate_synthetic_data,
    write_synthetic_artifacts,
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PreCTG 합성 데이터 생성")
    parser.add_argument("--rows", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260814)
    parser.add_argument("--profile", choices=["coverage", "distribution"], default="coverage")
    parser.add_argument("--output", default="data/synthetic/prectg-synthetic.csv")
    args = parser.parse_args(argv)
    frame = generate_synthetic_data(args.rows, args.seed, args.profile)
    report = validate_synthetic_data(frame, args.profile, args.seed)
    write_synthetic_artifacts(frame, report, args.output)
    print(json.dumps(asdict(report), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

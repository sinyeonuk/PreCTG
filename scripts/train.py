"""Train and persist the synthetic-demo LightGBM bundle."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

import pandas as pd

from prectg.model import save_model_bundle, train_model_bundle, training_report_dict


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PreCTG LightGBM 학습")
    parser.add_argument("--data", required=True, help="합성 CSV 경로")
    parser.add_argument("--output", default="models/prectg-demo.joblib")
    parser.add_argument("--seed", type=int, default=20260814)
    args = parser.parse_args(argv)
    frame = pd.read_csv(args.data)
    bundle, report = train_model_bundle(frame, args.seed)
    save_model_bundle(bundle, args.output)
    print(json.dumps(training_report_dict(report), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Command-line interface for generation, training, and staged analysis."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

import pandas as pd

from prectg.io import read_json_record
from prectg.metadata import project_status
from prectg.model import (
    ModelContractError,
    load_model_bundle,
    save_model_bundle,
    train_model_bundle,
    training_report_dict,
)
from prectg.risk_engine import analyze_payload
from prectg.synthetic import (
    generate_synthetic_data,
    validate_synthetic_data,
    write_synthetic_artifacts,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PreCTG MVP 명령줄 도구")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status", help="현재 구현 단계와 경계를 확인합니다.")

    generate = subparsers.add_parser("generate", help="합성 데이터를 생성합니다.")
    generate.add_argument("--rows", type=int, default=500)
    generate.add_argument("--seed", type=int, default=20260814)
    generate.add_argument("--profile", choices=["coverage", "distribution"], default="coverage")
    generate.add_argument("--output", default="data/synthetic/prectg-synthetic.csv")

    train = subparsers.add_parser("train", help="합성 데이터로 LightGBM을 학습합니다.")
    train.add_argument("--data", required=True)
    train.add_argument("--output", default="models/prectg-demo.joblib")
    train.add_argument("--seed", type=int, default=20260814)

    predict = subparsers.add_parser("predict", help="JSON 사례를 단계별로 분석합니다.")
    predict.add_argument("--input", required=True)
    predict.add_argument("--model")
    predict.add_argument("--output")
    predict.add_argument("--mode", choices=["synthetic_demo", "clinical"], default="synthetic_demo")
    return parser


def _print_json(payload: dict[str, object], output: str | None = None) -> None:
    serialized = json.dumps(payload, ensure_ascii=False, indent=2)
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(serialized, encoding="utf-8")
    print(serialized)


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "status":
        _print_json(project_status())
        return 0
    if args.command == "generate":
        frame = generate_synthetic_data(args.rows, args.seed, args.profile)
        report = validate_synthetic_data(frame, args.profile, args.seed)
        write_synthetic_artifacts(frame, report, args.output)
        _print_json(asdict(report))
        return 0
    if args.command == "train":
        frame = pd.read_csv(args.data)
        bundle, report = train_model_bundle(frame, args.seed)
        save_model_bundle(bundle, args.output)
        _print_json(training_report_dict(report))
        return 0
    if args.command == "predict":
        bundle = None
        if args.model:
            try:
                bundle = load_model_bundle(args.model)
            except ModelContractError:
                bundle = None
        result = analyze_payload(read_json_record(args.input), bundle=bundle, mode=args.mode)
        _print_json(result.model_dump(mode="json"), args.output)
        return 0 if result.validation.status == "valid" else 2
    return 2

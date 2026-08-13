"""Measure the maintained 50,000-row MVP throughput path."""

from __future__ import annotations

import argparse
import json
import platform
import time
from collections.abc import Sequence
from pathlib import Path

from prectg.model import predict_batch_probabilities, predict_probability, train_model_bundle
from prectg.preprocessing import normalize_record
from prectg.synthetic import generate_synthetic_data, validate_synthetic_data


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PreCTG 처리량 벤치마크")
    parser.add_argument("--rows", type=int, default=50000)
    parser.add_argument("--seed", type=int, default=20260814)
    parser.add_argument("--output", default="outputs/benchmark.json")
    args = parser.parse_args(argv)

    started = time.perf_counter()
    frame = generate_synthetic_data(args.rows, args.seed, "distribution")
    report = validate_synthetic_data(frame, "distribution", args.seed)
    generation_seconds = time.perf_counter() - started

    started = time.perf_counter()
    bundle, training_report = train_model_bundle(frame, args.seed)
    training_seconds = time.perf_counter() - started

    started = time.perf_counter()
    probabilities = predict_batch_probabilities(bundle, frame)
    batch_seconds = time.perf_counter() - started

    representative_record = normalize_record(frame.iloc[0].dropna().to_dict())
    predict_probability(bundle, representative_record)
    started = time.perf_counter()
    predict_probability(bundle, representative_record)
    single_inference_seconds = time.perf_counter() - started

    result = {
        "rows": args.rows,
        "seed": args.seed,
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "processor": platform.processor() or "not_reported",
        },
        "generation_and_validation_seconds": generation_seconds,
        "training_seconds": training_seconds,
        "batch_inference_seconds": batch_seconds,
        "single_inference_seconds": single_inference_seconds,
        "batch_results": len(probabilities),
        "quality": {
            "duplicate_records": report.duplicate_records,
            "logical_violations": report.logical_violations,
            "schema_violations": report.schema_violations,
            "checksum_sha256": report.checksum_sha256,
            "distribution_differences": report.distribution_differences,
            "minimum_scenario_count": min(report.scenario_counts.values()),
        },
        "model": {
            "group_overlap": training_report.group_overlap,
            "synthetic_auc_debug_only": training_report.synthetic_auc,
        },
        "limits_seconds": {
            "generation_and_validation": 60,
            "training": 300,
            "batch": 15,
            "single_inference": 1,
        },
        "passed": {
            "generation_and_validation": generation_seconds <= 60,
            "training": training_seconds <= 300,
            "batch": batch_seconds <= 15,
            "single_inference": single_inference_seconds <= 1,
            "data_quality": (
                report.duplicate_records == 0
                and report.logical_violations == 0
                and report.schema_violations == 0
                and min(report.scenario_counts.values()) >= 100
                and all(abs(value) <= 0.01 for value in report.distribution_differences.values())
            ),
        },
        "warning": "합성 데이터 처리량 측정이며 실제 임상 성능을 나타내지 않습니다.",
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(result["passed"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())

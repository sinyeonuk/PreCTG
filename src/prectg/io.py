"""JSON and CSV adapters for the AIHub-compatible input boundary."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from prectg.preprocessing import InputContractError, normalize_record
from prectg.schema import NormalizedRecord


def read_json_record(path: str | Path) -> dict[str, Any]:
    try:
        with Path(path).open(encoding="utf-8") as input_file:
            payload = json.load(input_file)
    except (OSError, json.JSONDecodeError) as error:
        raise InputContractError("JSON 파일을 읽을 수 없습니다.") from error
    if not isinstance(payload, dict):
        raise InputContractError("JSON 최상위 값은 객체여야 합니다.")
    return payload


def read_csv_records(path: str | Path) -> list[dict[str, Any]]:
    try:
        with Path(path).open(encoding="utf-8-sig", newline="") as input_file:
            return list(csv.DictReader(input_file))
    except OSError as error:
        raise InputContractError("CSV 파일을 읽을 수 없습니다.") from error


def load_normalized_record(path: str | Path) -> NormalizedRecord:
    return normalize_record(read_json_record(path))

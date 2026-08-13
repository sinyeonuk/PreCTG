"""Leakage-safe model feature construction separated from decision rules."""

from __future__ import annotations

from functools import lru_cache

import pandas as pd

from prectg.leakage import validate_model_features
from prectg.preprocessing import load_field_contract
from prectg.schema import AvailabilityTiming, NormalizedRecord


@lru_cache(maxsize=1)
def model_feature_contract() -> tuple[list[str], list[str]]:
    contract = load_field_contract()
    eligible = [field for field in contract["fields"] if field["model_eligible"]]
    source_names = [field["source_name"] for field in eligible]
    internal_names = [field["internal_name"] for field in eligible]
    timing = {
        field["source_name"]: AvailabilityTiming(field["timing"]) for field in contract["fields"]
    }
    validate_model_features(source_names, timing)
    return source_names, internal_names


def training_feature_frame(frame: pd.DataFrame) -> pd.DataFrame:
    source_names, internal_names = model_feature_contract()
    missing = sorted(set(source_names) - set(frame.columns))
    if missing:
        raise ValueError(f"모델 특성 열이 없습니다: {', '.join(missing)}")
    features = frame[source_names].copy()
    features.columns = internal_names
    for column in features.columns:
        features[column] = pd.to_numeric(features[column], errors="coerce")
    return features


def record_feature_frame(record: NormalizedRecord) -> pd.DataFrame:
    _, internal_names = model_feature_contract()
    values = {name: getattr(record, name) for name in internal_names}
    return pd.DataFrame([values], columns=internal_names).apply(pd.to_numeric, errors="coerce")

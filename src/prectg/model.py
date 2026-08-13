"""LightGBM training, persistence, compatibility, and inference boundary."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from importlib.metadata import version
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupShuffleSplit

from prectg.features import model_feature_contract, record_feature_frame, training_feature_frame
from prectg.schema import NormalizedRecord, Signal
from prectg.synthetic import dataframe_checksum

MODEL_BUNDLE_VERSION = "prectg-model-bundle-v1"
TARGET_COLUMN = "synthetic_emergency_after_index"
GROUP_COLUMN = "Mother.de-identification_ID"


class ModelContractError(ValueError):
    pass


@dataclass(frozen=True)
class TrainingReport:
    rows: int
    train_rows: int
    validation_rows: int
    train_groups: int
    validation_groups: int
    group_overlap: int
    synthetic_auc: float | None
    low_threshold: float
    high_threshold: float
    seed: int
    data_checksum: str
    warning: str = "합성 데이터 성능은 실제 임상 성능을 나타내지 않습니다."


def _target_values(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series.astype(int)
    mapped = series.astype(str).str.lower().map({"true": 1, "false": 0, "1": 1, "0": 0})
    if mapped.isna().any():
        raise ValueError("합성 목표 열에는 0/1 또는 true/false만 사용할 수 있습니다.")
    return mapped.astype(int)


def grouped_split(frame: pd.DataFrame, seed: int) -> tuple[np.ndarray, np.ndarray]:
    if GROUP_COLUMN not in frame or frame[GROUP_COLUMN].isna().any():
        raise ValueError("그룹 분할에 사용할 산모 식별자가 필요합니다.")
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
    train_index, validation_index = next(
        splitter.split(frame, groups=frame[GROUP_COLUMN].astype(str))
    )
    return train_index, validation_index


def train_model_bundle(
    frame: pd.DataFrame, seed: int = 20260814
) -> tuple[dict[str, Any], TrainingReport]:
    if TARGET_COLUMN not in frame:
        raise ValueError(f"학습 목표 열이 없습니다: {TARGET_COLUMN}")
    features = training_feature_frame(frame)
    target = _target_values(frame[TARGET_COLUMN])
    train_index, validation_index = grouped_split(frame, seed)

    model = LGBMClassifier(
        n_estimators=140,
        learning_rate=0.05,
        num_leaves=15,
        min_child_samples=20,
        subsample=1.0,
        colsample_bytree=1.0,
        random_state=seed,
        deterministic=True,
        force_col_wise=True,
        n_jobs=1,
        verbosity=-1,
    )
    model.fit(features.iloc[train_index], target.iloc[train_index])
    probabilities = model.predict_proba(features.iloc[validation_index])[:, 1]
    low_threshold, high_threshold = np.quantile(probabilities, [1 / 3, 2 / 3])
    validation_target = target.iloc[validation_index]
    auc = None
    if validation_target.nunique() == 2:
        auc = float(roc_auc_score(validation_target, probabilities))

    source_features, internal_features = model_feature_contract()
    train_groups = set(frame.iloc[train_index][GROUP_COLUMN].astype(str))
    validation_groups = set(frame.iloc[validation_index][GROUP_COLUMN].astype(str))
    checksum = dataframe_checksum(frame)
    bundle: dict[str, Any] = {
        "bundle_version": MODEL_BUNDLE_VERSION,
        "input_contract_version": "field-contract-v1",
        "window_version": "early-window-v1",
        "target_version": "emergency-after-index-v1",
        "generator_version": str(frame["generator_version"].iloc[0]),
        "seed": seed,
        "source_features": source_features,
        "internal_features": internal_features,
        "thresholds": {"low": float(low_threshold), "high": float(high_threshold)},
        "training_data_checksum": checksum,
        "dependencies": {
            "lightgbm": version("lightgbm"),
            "scikit-learn": version("scikit-learn"),
            "pandas": version("pandas"),
        },
        "model": model,
    }
    report = TrainingReport(
        rows=len(frame),
        train_rows=len(train_index),
        validation_rows=len(validation_index),
        train_groups=len(train_groups),
        validation_groups=len(validation_groups),
        group_overlap=len(train_groups & validation_groups),
        synthetic_auc=auc,
        low_threshold=float(low_threshold),
        high_threshold=float(high_threshold),
        seed=seed,
        data_checksum=checksum,
    )
    return bundle, report


def validate_model_bundle(bundle: dict[str, Any]) -> None:
    required = {
        "bundle_version",
        "input_contract_version",
        "window_version",
        "target_version",
        "internal_features",
        "thresholds",
        "model",
    }
    missing = sorted(required - set(bundle))
    if missing:
        raise ModelContractError(f"모델 번들 항목이 없습니다: {', '.join(missing)}")
    if bundle["bundle_version"] != MODEL_BUNDLE_VERSION:
        raise ModelContractError("지원하지 않는 모델 번들 버전입니다.")
    if bundle["input_contract_version"] != "field-contract-v1":
        raise ModelContractError("입력 계약과 모델 계약이 맞지 않습니다.")
    _, expected_features = model_feature_contract()
    if bundle["internal_features"] != expected_features:
        raise ModelContractError("모델 특성 순서가 현재 계약과 맞지 않습니다.")


def save_model_bundle(bundle: dict[str, Any], path: str | Path) -> Path:
    validate_model_bundle(bundle)
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, output_path)
    return output_path


def load_model_bundle(path: str | Path) -> dict[str, Any]:
    try:
        bundle = joblib.load(Path(path))
    except Exception as error:
        raise ModelContractError("모델 파일을 불러올 수 없습니다.") from error
    if not isinstance(bundle, dict):
        raise ModelContractError("모델 파일 형식이 올바르지 않습니다.")
    validate_model_bundle(bundle)
    return bundle


def predict_probability(bundle: dict[str, Any], record: NormalizedRecord) -> float:
    validate_model_bundle(bundle)
    features = record_feature_frame(record)
    if features.isna().any(axis=None):
        missing = features.columns[features.isna().iloc[0]].tolist()
        raise ModelContractError(f"모델 입력이 부족합니다: {', '.join(missing)}")
    probability = float(bundle["model"].predict_proba(features)[:, 1][0])
    if not 0 <= probability <= 1:
        raise ModelContractError("모델 확률이 허용 범위를 벗어났습니다.")
    return probability


def predict_batch_probabilities(bundle: dict[str, Any], frame: pd.DataFrame) -> np.ndarray:
    """Predict a validated source-compatible batch for throughput demonstration."""
    validate_model_bundle(bundle)
    features = training_feature_frame(frame)
    probabilities = bundle["model"].predict_proba(features)[:, 1]
    if not np.isfinite(probabilities).all() or ((probabilities < 0) | (probabilities > 1)).any():
        raise ModelContractError("배치 모델 확률이 허용 범위를 벗어났습니다.")
    return probabilities


def probability_signal(bundle: dict[str, Any], probability: float) -> Signal:
    """Classify a synthetic probability using thresholds stored with its model."""
    validate_model_bundle(bundle)
    if not 0 <= probability <= 1:
        raise ModelContractError("모델 확률이 허용 범위를 벗어났습니다.")
    thresholds = bundle["thresholds"]
    if probability < thresholds["low"]:
        return Signal.LOW
    if probability < thresholds["high"]:
        return Signal.REVIEW
    return Signal.HIGH


def training_report_dict(report: TrainingReport) -> dict[str, Any]:
    return asdict(report)

"""Deterministic, vectorized synthetic-data generation and quality reporting."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from prectg.metadata import NON_CLINICAL_WARNING

SCENARIOS = ("normal", "maternal", "ctg", "combined", "missing", "conflict")
GENERATOR_VERSION = "1.0.0"
GENERATION_RULESET_VERSION = "synthetic-generator-rules-v1"
PUBLIC_DISTRIBUTIONS = {
    "maternal_age_teen": 0.0015,
    "maternal_age_20s": 0.1074,
    "maternal_age_30s": 0.7664,
    "maternal_age_40s": 0.1241,
    "maternal_age_50_plus": 0.0007,
    "gravida_1": 0.4008,
    "para_0": 0.5435,
    "multiple_gestation": 0.1605,
    "ctg_category_1": 0.7272,
}


@dataclass(frozen=True)
class SyntheticQualityReport:
    rows: int
    profile: str
    seed: int
    generator_version: str
    ruleset_version: str
    checksum_sha256: str
    duplicate_records: int
    logical_violations: int
    schema_violations: int
    target_rate: float
    category_1_rate: float
    scenario_counts: dict[str, int]
    distribution_differences: dict[str, float]
    warning: str = NON_CLINICAL_WARNING


def _scenario_values(rows: int, profile: str, rng: np.random.Generator) -> np.ndarray:
    if profile == "coverage":
        return np.resize(np.asarray(SCENARIOS, dtype=object), rows)
    if profile == "distribution":
        return rng.choice(
            SCENARIOS,
            size=rows,
            p=np.asarray([0.56, 0.11, 0.14, 0.08, 0.06, 0.05]),
        )
    raise ValueError("profile은 coverage 또는 distribution이어야 합니다.")


def _distribution_gravida_para(
    rows: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    """Sample a valid joint table while preserving both published marginals."""
    gravida_values = np.asarray([1, 2, 3, 4, 5])
    para_values = np.asarray([0, 1, 2, 3])
    gravida_margin = np.asarray([0.4008, 0.3363, 0.1582, 0.075, 0.0297])
    para_margin = np.asarray([0.5435, 0.34, 0.0928, 0.0237])
    table = np.outer(gravida_margin, para_margin)
    table *= para_values[np.newaxis, :] < gravida_values[:, np.newaxis]
    for _ in range(100):
        table *= (gravida_margin / table.sum(axis=1))[:, np.newaxis]
        table *= (para_margin / table.sum(axis=0))[np.newaxis, :]
    table /= table.sum()
    sampled = rng.choice(table.size, rows, p=table.ravel())
    return gravida_values[sampled // len(para_values)], para_values[sampled % len(para_values)]


def generate_synthetic_data(
    rows: int = 500,
    seed: int = 20260814,
    profile: str = "coverage",
) -> pd.DataFrame:
    """Generate source-compatible records for functional testing only."""
    if rows < 1:
        raise ValueError("rows는 1 이상이어야 합니다.")
    rng = np.random.default_rng(seed)
    scenario = _scenario_values(rows, profile, rng)
    index = np.arange(rows)
    mother_ids = index // 2

    age_probabilities = np.asarray([0.0015, 0.1074, 0.7664, 0.1241, 0.0007])
    age_probabilities /= age_probabilities.sum()
    if profile == "distribution":
        maternal_age = rng.choice([19, 25, 35, 45, 52], rows, p=age_probabilities)
        twins = rng.choice(["0", "1"], rows, p=[0.8395, 0.1605])
    else:
        maternal_age = np.resize(np.asarray([19, 25, 35, 45, 52]), rows)
        twins = np.resize(np.asarray(["0", "0", "0", "0", "0", "1"]), rows)

    if profile == "distribution":
        gravida, para = _distribution_gravida_para(rows, rng)
    else:
        gravida = rng.choice([1, 2, 3, 4, 5], rows, p=[0.4008, 0.3363, 0.1582, 0.075, 0.0297])
        para = np.minimum(
            gravida - 1,
            rng.choice([0, 1, 2, 3], rows, p=[0.5435, 0.34, 0.0928, 0.0237]),
        )
    ga_weeks = np.clip(np.rint(rng.normal(38.5, 1.6, rows)), 30, 42).astype(int)
    ga_days = rng.integers(0, 7, rows)
    baseline = np.clip(np.rint(rng.normal(140, 10, rows)), 100, 180).astype(float)

    ctg_risk = np.isin(scenario, ["ctg", "combined"])
    maternal_risk = np.isin(scenario, ["maternal", "combined"])
    conflict = scenario == "conflict"
    missing = scenario == "missing"

    variability = np.where(ctg_risk, rng.choice(["0", "1", "3"], rows), "2")
    acceleration = np.where(ctg_risk, "2", "1")
    late = np.where(ctg_risk, rng.choice(["1", "2"], rows), "0")
    variable = np.where(ctg_risk, rng.choice(["0", "1", "2"], rows), "0")
    prolonged = np.where(ctg_risk & (rng.random(rows) < 0.24), "1", "0")
    sinusoidal = np.where(ctg_risk & (rng.random(rows) < 0.08), "1", "0")
    early = np.where((~ctg_risk) & (rng.random(rows) < 0.12), "1", "0")

    if profile == "coverage":
        gravida = np.where(maternal_risk, np.maximum(gravida, 4), gravida)
    ga_weeks = np.where(maternal_risk, np.minimum(ga_weeks, 36), ga_weeks)
    variability = np.where(conflict, "2", variability)
    acceleration = np.where(conflict, "1", acceleration)
    late = np.where(conflict, "2", late)

    synthetic_score = (
        -2.0
        + 0.55 * (gravida >= 4)
        + 0.7 * (ga_weeks < 37)
        + 0.55 * (variability != "2")
        + 0.85 * (late == "2")
        + 0.75 * (prolonged == "1")
        + 0.95 * (sinusoidal == "1")
        + 0.5 * conflict
        + rng.normal(0, 0.65, rows)
    )
    probability = 1 / (1 + np.exp(-synthetic_score))
    target = rng.random(rows) < probability
    category = np.where((sinusoidal == "1") | (prolonged == "1"), "2", "0")
    category = np.where((category == "0") & ((late != "0") | (variability != "2")), "1", category)

    start = pd.Timestamp("2026-08-14T09:00:00+09:00") + pd.to_timedelta(index, unit="m")
    frame = pd.DataFrame(
        {
            "ID": [f"SYN-{value:06d}" for value in index],
            "Mother.de-identification_ID": [f"SYN-M-{value:06d}" for value in mother_ids],
            "de-identification_ID": [f"SYN-F-{value:06d}" for value in index],
            "Mother.MEASURE_DATE": "2026-08-14",
            "Mother.Birth Date": [f"{2026 - int(age):04d}-01-01" for age in maternal_age],
            "Mother.Gravida": gravida,
            "Mother.Para": para,
            "GA.wks": ga_weeks,
            "GA.day": ga_days,
            "twins": twins,
            "BaseLine": baseline,
            "Baseline_Variability": variability,
            "Acceleration": acceleration,
            "Early_deceleration": early,
            "Late_deceleration": late,
            "Variable_deceleration": variable,
            "Prolonged_deceleration": prolonged,
            "Sinosoical_pattern": sinusoidal,
            "CA": category,
            "window_start": start.astype(str),
            "window_end": (start + pd.Timedelta(minutes=20)).astype(str),
            "window_complete": True,
            "timing_source": "synthetic_generator",
            "synthetic_emergency_after_index": target,
            "synthetic_profile": profile,
            "scenario_type": scenario,
            "generation_seed": seed,
            "generator_version": GENERATOR_VERSION,
        }
    )
    frame.loc[missing, ["GA.wks", "BaseLine"]] = np.nan
    return frame


def dataframe_checksum(frame: pd.DataFrame) -> str:
    payload = frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_synthetic_data(frame: pd.DataFrame, profile: str, seed: int) -> SyntheticQualityReport:
    required = {
        "ID",
        "Mother.de-identification_ID",
        "de-identification_ID",
        "synthetic_emergency_after_index",
        "scenario_type",
    }
    missing_columns = sorted(required - set(frame.columns))
    if missing_columns:
        raise ValueError(f"필수 합성 열이 없습니다: {', '.join(missing_columns)}")
    logical_violations = int(
        ((frame["Mother.Para"] > frame["Mother.Gravida"]) | ~frame["GA.day"].between(0, 6)).sum()
    )
    code_contract = {
        "Baseline_Variability": {"0", "1", "2", "3"},
        "Acceleration": {"1", "2"},
        "Early_deceleration": {"0", "1"},
        "Late_deceleration": {"0", "1", "2"},
        "Variable_deceleration": {"0", "1", "2"},
        "Prolonged_deceleration": {"0", "1"},
        "Sinosoical_pattern": {"0", "1"},
        "CA": {"0", "1", "2"},
    }
    schema_violations = int(frame["ID"].isna().sum())
    for column, allowed in code_contract.items():
        schema_violations += int((~frame[column].astype(str).isin(allowed)).sum())
    schema_violations += int((~frame["window_complete"].eq(True)).sum())
    schema_violations += int((frame["timing_source"] != "synthetic_generator").sum())
    maternal_age = 2026 - pd.to_datetime(frame["Mother.Birth Date"]).dt.year
    actual_distributions = {
        "maternal_age_teen": float((maternal_age < 20).mean()),
        "maternal_age_20s": float(maternal_age.between(20, 29).mean()),
        "maternal_age_30s": float(maternal_age.between(30, 39).mean()),
        "maternal_age_40s": float(maternal_age.between(40, 49).mean()),
        "maternal_age_50_plus": float((maternal_age >= 50).mean()),
        "gravida_1": float((frame["Mother.Gravida"] == 1).mean()),
        "para_0": float((frame["Mother.Para"] == 0).mean()),
        "multiple_gestation": float((frame["twins"].astype(str) == "1").mean()),
        "ctg_category_1": float((frame["CA"].astype(str) == "0").mean()),
    }
    distribution_differences = {
        key: actual_distributions[key] - expected for key, expected in PUBLIC_DISTRIBUTIONS.items()
    }
    return SyntheticQualityReport(
        rows=len(frame),
        profile=profile,
        seed=seed,
        generator_version=GENERATOR_VERSION,
        ruleset_version=GENERATION_RULESET_VERSION,
        checksum_sha256=dataframe_checksum(frame),
        duplicate_records=int(frame["ID"].duplicated().sum()),
        logical_violations=logical_violations,
        schema_violations=schema_violations,
        target_rate=float(frame["synthetic_emergency_after_index"].mean()),
        category_1_rate=float((frame["CA"] == "0").mean()),
        scenario_counts={
            key: int(value) for key, value in frame["scenario_type"].value_counts().items()
        },
        distribution_differences=distribution_differences,
    )


def write_synthetic_artifacts(
    frame: pd.DataFrame,
    report: SyntheticQualityReport,
    output_path: str | Path,
) -> tuple[Path, Path]:
    data_path = Path(output_path)
    data_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(data_path, index=False, lineterminator="\n")
    report_path = data_path.with_suffix(".report.json")
    report_path.write_text(
        json.dumps(asdict(report), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return data_path, report_path

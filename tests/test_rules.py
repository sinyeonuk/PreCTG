import json
from pathlib import Path

from prectg.preprocessing import normalize_record
from prectg.rules import evaluate_stage_0, evaluate_stage_1
from prectg.schema import Signal, StageStatus

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def normal_record():
    payload = json.loads(
        (PROJECT_ROOT / "data/fixtures/minimal-synthetic-input.json").read_text(encoding="utf-8")
    )
    return normalize_record(payload)


def test_normal_fixture_has_low_synthetic_demo_signals() -> None:
    record = normal_record()
    assert evaluate_stage_0(record).signal == Signal.LOW
    assert evaluate_stage_1(record).signal == Signal.LOW


def test_stage_1_severe_demo_pattern_takes_priority() -> None:
    record = normal_record().model_copy(
        update={"sinusoidal_pattern": "1", "late_deceleration": "2"}
    )
    result = evaluate_stage_1(record)
    assert result.status == StageStatus.AVAILABLE
    assert result.signal == Signal.HIGH
    assert {reason.code for reason in result.reasons} >= {
        "demo_sinusoidal_pattern",
        "demo_late_deceleration",
    }
    assert result.score == 4


def test_stage_0_high_pattern_has_exact_golden_result() -> None:
    record = normal_record().model_copy(
        update={"gravida": 5, "para": 3, "gestational_age_weeks": 35}
    )
    result = evaluate_stage_0(record)

    assert result.status == StageStatus.AVAILABLE
    assert result.signal == Signal.HIGH
    assert result.score == 3
    assert [reason.code for reason in result.reasons] == [
        "demo_ga_pattern",
        "demo_gravida_pattern",
        "demo_para_pattern",
    ]


def test_stage_1_conflict_pattern_keeps_severe_reason() -> None:
    record = normal_record().model_copy(
        update={
            "baseline_variability": "2",
            "acceleration": "1",
            "late_deceleration": "2",
        }
    )
    result = evaluate_stage_1(record)

    assert result.signal == Signal.HIGH
    assert result.score == 2
    assert [reason.code for reason in result.reasons] == ["demo_late_deceleration"]


def test_missing_stage_input_is_not_reported_as_low() -> None:
    record = normal_record().model_copy(update={"baseline": None})
    result = evaluate_stage_1(record)
    assert result.status == StageStatus.INSUFFICIENT_DATA
    assert result.signal == Signal.UNAVAILABLE


def test_clinical_mode_stays_unavailable_without_approved_rules() -> None:
    result = evaluate_stage_0(normal_record(), mode="clinical")
    assert result.status == StageStatus.UNAVAILABLE
    assert result.signal == Signal.UNAVAILABLE

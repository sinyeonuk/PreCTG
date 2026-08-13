import json
from pathlib import Path

from prectg.model import train_model_bundle
from prectg.risk_engine import analyze_payload
from prectg.schema import Signal, StageStatus
from prectg.synthetic import generate_synthetic_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def fixture_payload() -> dict[str, object]:
    return json.loads(
        (PROJECT_ROOT / "data/fixtures/minimal-synthetic-input.json").read_text(encoding="utf-8")
    )


def test_result_contract_preserves_rule_results_when_model_is_missing() -> None:
    result = analyze_payload(fixture_payload())

    assert result.validation.status == "valid"
    assert result.stages["stage_0"].status == StageStatus.AVAILABLE
    assert result.stages["stage_2"].status == StageStatus.UNAVAILABLE
    assert result.stages["stage_2"].probability is None
    assert result.integrated_result.status == "partial"
    assert result.limitations.synthetic_data is True


def test_integrated_result_uses_trained_model_without_hiding_scope() -> None:
    frame = generate_synthetic_data(rows=800, seed=19)
    bundle, _ = train_model_bundle(frame, seed=19)
    payload = frame.iloc[0].dropna().to_dict()

    result = analyze_payload(payload, bundle)

    assert result.stages["stage_2"].status == StageStatus.AVAILABLE
    assert result.stages["stage_2"].signal in {Signal.LOW, Signal.REVIEW, Signal.HIGH}
    assert result.stages["stage_2"].probability is not None
    assert result.integrated_result.status == "complete"
    assert result.limitations.non_clinical_use is True


def test_invalid_input_returns_actionable_result_instead_of_exception() -> None:
    result = analyze_payload({"unknown": 1})

    assert result.validation.status == "invalid"
    assert result.validation.errors[0].fields == ["unknown"]
    assert result.integrated_result.signal == Signal.UNAVAILABLE

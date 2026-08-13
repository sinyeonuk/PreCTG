import json
from copy import deepcopy
from pathlib import Path

import pytest

from prectg.io import load_normalized_record
from prectg.preprocessing import InputContractError, normalize_record

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = PROJECT_ROOT / "data" / "fixtures" / "minimal-synthetic-input.json"


def fixture_payload() -> dict[str, object]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def test_normalizes_source_names_without_mutating_payload() -> None:
    payload = fixture_payload()
    original = deepcopy(payload)

    record = normalize_record(payload)

    assert record.record_id == "SYN-DEMO-0001"
    assert record.baseline == 140
    assert record.sinusoidal_pattern == "0"
    assert record.window_complete is True
    assert payload == original


def test_json_adapter_uses_same_contract() -> None:
    record = load_normalized_record(FIXTURE_PATH)
    assert record.gestational_age_weeks == 39
    assert record.baseline_variability == "2"


@pytest.mark.parametrize(
    ("field", "value"),
    [("GA.day", 7), ("Baseline_Variability", "9"), ("unknown", "value")],
)
def test_rejects_invalid_range_code_and_unknown_field(field: str, value: object) -> None:
    payload = fixture_payload()
    payload[field] = value

    with pytest.raises(InputContractError) as error:
        normalize_record(payload)

    assert field in error.value.fields


def test_missing_marker_is_null_not_numeric_value() -> None:
    payload = fixture_payload()
    payload["GA.wks"] = 9999

    record = normalize_record(payload)

    assert record.gestational_age_weeks is None


def test_requires_complete_twenty_minute_provenance() -> None:
    payload = fixture_payload()
    payload["window_end"] = "2026-08-14T09:19:59+09:00"

    with pytest.raises(InputContractError, match="20분"):
        normalize_record(payload)


def test_rejects_para_greater_than_gravida() -> None:
    payload = fixture_payload()
    payload["Mother.Gravida"] = 1
    payload["Mother.Para"] = 2

    with pytest.raises(InputContractError, match="출산 횟수"):
        normalize_record(payload)

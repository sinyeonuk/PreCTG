from pathlib import Path

import yaml

from prectg.schema import AnalysisResult, AvailabilityTiming, NormalizedRecord

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_yaml(relative_path: str) -> dict[str, object]:
    with (PROJECT_ROOT / relative_path).open(encoding="utf-8") as config_file:
        loaded = yaml.safe_load(config_file)
    assert isinstance(loaded, dict)
    return loaded


def test_field_contract_has_unique_names_and_safe_model_features() -> None:
    contract = load_yaml("configs/field-contract.yaml")
    fields = contract["fields"]
    assert isinstance(fields, list)

    source_names = [field["source_name"] for field in fields]
    internal_names = [field["internal_name"] for field in fields]
    assert len(source_names) == len(set(source_names))
    assert len(internal_names) == len(set(internal_names))
    extension_names = [field["internal_name"] for field in contract["synthetic_extension"]]
    assert set(internal_names + extension_names) == set(NormalizedRecord.model_fields)

    allowed_timings = {
        AvailabilityTiming.PRE_LABOR.value,
        AvailabilityTiming.EARLY_CTG.value,
    }
    for field in fields:
        if field["model_eligible"]:
            assert field["role"] == "feature"
            assert field["timing"] in allowed_timings
            assert field["definition_status"] == "confirmed"


def test_early_ctg_features_require_timing_evidence() -> None:
    contract = load_yaml("configs/field-contract.yaml")
    early_ctg_fields = [field for field in contract["fields"] if field["timing"] == "EARLY_CTG"]

    assert early_ctg_fields
    assert all(field.get("timing_evidence_required") is True for field in early_ctg_fields)


def test_timing_compatibility_config_matches_field_contract() -> None:
    contract = load_yaml("configs/field-contract.yaml")
    timing_config = load_yaml("configs/feature-timing.yaml")
    timing_by_source = timing_config["features"]

    declared_names = {field["source_name"] for field in contract["fields"]}
    declared_names.update(field["internal_name"] for field in contract["synthetic_extension"])

    for field in contract["fields"]:
        assert timing_by_source[field["source_name"]] == field["timing"]
    assert set(timing_by_source).issubset(declared_names)

    conditional = timing_config["conditional_timing"]["EARLY_CTG"]
    assert conditional["contract_version"] == "early-window-v1"
    assert conditional["evidence_required"] is True


def test_result_contract_keeps_unavailable_values_explicit() -> None:
    contract = load_yaml("configs/result-contract.yaml")

    assert contract["target"]["official_emergency_mapping"] == "disabled"
    assert contract["rule_modes"]["clinical"]["current_approved_rule_count"] == 0
    assert contract["ml_result"]["probability_when_unavailable"] is None
    assert contract["ml_result"]["fallback_probability"] == "forbidden"
    assert contract["observation_window"]["clinical_standard"] is False
    assert set(contract["required_sections"]) == set(AnalysisResult.model_fields)

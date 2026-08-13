"""Contract-driven input normalization without mutating source payloads."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from prectg.schema import NormalizedRecord

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONTRACT_PATH = PROJECT_ROOT / "configs" / "field-contract.yaml"


class InputContractError(ValueError):
    """A safe, field-oriented error raised at the input boundary."""

    def __init__(self, message: str, fields: list[str] | None = None) -> None:
        super().__init__(message)
        self.fields = fields or []


@lru_cache(maxsize=4)
def load_field_contract(path: str | Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as config_file:
        contract = yaml.safe_load(config_file)
    if not isinstance(contract, dict) or contract.get("contract_version") != "field-contract-v1":
        raise InputContractError("지원하지 않는 입력 계약입니다.")
    return contract


def _is_missing(value: Any, missing_values: list[Any]) -> bool:
    return value is None or any(
        value == missing for missing in missing_values if missing is not None
    )


def _convert(value: Any, data_type: str, field_name: str) -> Any:
    try:
        if data_type == "string":
            return str(value)
        if data_type == "integer":
            number = float(value)
            if not number.is_integer():
                raise ValueError
            return int(number)
        if data_type == "number":
            return float(value)
        if data_type == "boolean":
            if isinstance(value, bool):
                return value
            if str(value).lower() in {"true", "1"}:
                return True
            if str(value).lower() in {"false", "0"}:
                return False
            raise ValueError
        return value
    except (TypeError, ValueError) as error:
        raise InputContractError(
            f"{field_name} 값을 {data_type} 형식으로 입력해 주세요.", [field_name]
        ) from error


def normalize_record(payload: dict[str, Any]) -> NormalizedRecord:
    """Return a validated internal record and leave the caller payload unchanged."""
    source = deepcopy(payload)
    contract = load_field_contract()
    field_specs = {field["source_name"]: field for field in contract["fields"]}
    extension_specs = {field["internal_name"]: field for field in contract["synthetic_extension"]}
    supported = set(field_specs) | set(extension_specs)
    unknown = sorted(set(source) - supported)
    if unknown:
        raise InputContractError(f"지원하지 않는 필드가 있습니다: {', '.join(unknown)}", unknown)

    missing_values = contract["normalization"]["missing_values"]
    normalized: dict[str, Any] = {}
    for source_name, value in source.items():
        spec = field_specs.get(source_name) or extension_specs[source_name]
        internal_name = spec["internal_name"]
        if _is_missing(value, missing_values):
            normalized[internal_name] = None
            continue
        converted = _convert(value, spec["data_type"], source_name)
        allowed_values = spec.get("allowed_values")
        if allowed_values is not None and converted not in allowed_values:
            raise InputContractError(
                f"{source_name} 값은 {allowed_values} 중 하나여야 합니다.", [source_name]
            )
        allowed_range = spec.get("allowed_range")
        if allowed_range is not None and not allowed_range[0] <= converted <= allowed_range[1]:
            raise InputContractError(
                f"{source_name} 값은 {allowed_range[0]}~{allowed_range[1]} 범위여야 합니다.",
                [source_name],
            )
        normalized[internal_name] = converted

    if not normalized.get("record_id"):
        raise InputContractError("ID를 입력해 주세요.", ["ID"])
    try:
        return NormalizedRecord.model_validate(normalized)
    except ValidationError as error:
        fields = [".".join(str(part) for part in item["loc"]) for item in error.errors()]
        message = error.errors()[0]["msg"] if error.errors() else "입력값을 확인해 주세요."
        raise InputContractError(message, fields) from error

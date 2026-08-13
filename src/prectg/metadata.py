"""Stable project metadata shared by CLI and UI entry points."""

from __future__ import annotations

from typing import Final

__version__: Final = "0.1.0"
PROJECT_STAGE: Final = "gate_0_contract_defined"
NON_CLINICAL_WARNING: Final = (
    "합성 데이터 기반 기능 시연용 MVP이며 실제 진단·처치나 임상 성능 검증에 사용할 수 없습니다."
)


def project_status() -> dict[str, object]:
    """Return a machine-readable summary without claiming unimplemented behavior."""
    return {
        "name": "PreCTG",
        "version": __version__,
        "stage": PROJECT_STAGE,
        "implemented": [
            "project_structure",
            "status_cli",
            "field_contract",
            "feature_timing_contract",
            "result_contract",
        ],
        "not_implemented": [
            "input_normalization",
            "synthetic_data_generation",
            "clinical_rules",
            "lightgbm_training",
            "risk_inference",
        ],
        "warning": NON_CLINICAL_WARNING,
    }

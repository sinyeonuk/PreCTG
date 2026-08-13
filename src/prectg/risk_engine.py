"""Single orchestration boundary for validated staged PreCTG results."""

from __future__ import annotations

from typing import Any

from prectg.features import model_feature_contract
from prectg.metadata import NON_CLINICAL_WARNING
from prectg.model import ModelContractError, predict_probability, probability_signal
from prectg.preprocessing import InputContractError, normalize_record
from prectg.rules import evaluate_stage_0, evaluate_stage_1
from prectg.schema import (
    AnalysisResult,
    CompletenessResult,
    ContractInfo,
    IntegratedResult,
    Issue,
    Limitations,
    NormalizedRecord,
    Reason,
    Signal,
    StageCompleteness,
    StageResult,
    StageStatus,
    ValidationResult,
)

STAGE_FIELDS = {
    "stage_0": ["gravida", "para", "gestational_age_weeks"],
    "stage_1": [
        "baseline",
        "baseline_variability",
        "acceleration",
        "late_deceleration",
        "variable_deceleration",
        "prolonged_deceleration",
        "sinusoidal_pattern",
        "window_complete",
        "timing_source",
    ],
}


def calculate_completeness(record: NormalizedRecord | None) -> CompletenessResult:
    _, model_fields = model_feature_contract()
    fields_by_stage = {
        **STAGE_FIELDS,
        "stage_2": [*model_fields, "window_complete", "timing_source"],
    }
    results: dict[str, StageCompleteness] = {}
    all_missing: set[str] = set()
    ratios: list[float] = []
    for stage, fields in fields_by_stage.items():
        missing = (
            fields if record is None else [name for name in fields if getattr(record, name) is None]
        )
        available = len(fields) - len(missing)
        ratio = available / len(fields)
        results[stage] = StageCompleteness(
            available=available,
            expected=len(fields),
            ratio=ratio,
            missing_fields=missing,
        )
        ratios.append(ratio)
        all_missing.update(missing)
    return CompletenessResult(
        overall_ratio=sum(ratios) / len(ratios),
        by_stage=results,
        missing_fields=sorted(all_missing),
    )


def _unavailable_stage(code: str, title: str, detail: str) -> StageResult:
    return StageResult(
        status=StageStatus.UNAVAILABLE,
        signal=Signal.UNAVAILABLE,
        reasons=[Reason(code=code, title=title, detail=detail)],
    )


def _model_stage(record: NormalizedRecord, bundle: dict[str, Any] | None, mode: str) -> StageResult:
    if mode != "synthetic_demo":
        return _unavailable_stage(
            "synthetic_model_disabled",
            "합성 모델 사용 안 함",
            "임상 모드에서는 합성 데이터로 학습한 모델을 실행하지 않습니다.",
        )
    if bundle is None:
        return _unavailable_stage(
            "model_unavailable",
            "모델 결과 없음",
            "호환되는 모델 파일이 없어 ML 분석을 실행하지 않았습니다.",
        )
    if record.window_complete is not True or not record.timing_source:
        return StageResult(
            status=StageStatus.INSUFFICIENT_DATA,
            signal=Signal.UNAVAILABLE,
            reasons=[
                Reason(
                    code="model_timing_missing",
                    title="관찰 시점 정보 부족",
                    detail="20분 초기 관찰창의 출처 정보를 확인해 주세요.",
                    fields=["window_complete", "timing_source"],
                )
            ],
        )
    try:
        probability = predict_probability(bundle, record)
    except ModelContractError as error:
        message = str(error)
        status = (
            StageStatus.INSUFFICIENT_DATA
            if message.startswith("모델 입력이 부족")
            else StageStatus.UNAVAILABLE
        )
        return StageResult(
            status=status,
            signal=Signal.UNAVAILABLE,
            reasons=[
                Reason(
                    code="model_contract_error",
                    title="모델 결과 없음",
                    detail=message,
                )
            ],
        )
    signal = probability_signal(bundle, probability)
    return StageResult(
        status=StageStatus.AVAILABLE,
        signal=signal,
        probability=probability,
        reasons=[
            Reason(
                code="synthetic_model_probability",
                title="합성 모델 상대 신호",
                detail="합성 검증 분포의 상대 분위수로 구분한 기능 시연 결과입니다.",
                fields=bundle["internal_features"],
            )
        ],
        version=bundle["bundle_version"],
    )


def _integrate(stages: dict[str, StageResult]) -> IntegratedResult:
    available = {
        name: stage for name, stage in stages.items() if stage.status == StageStatus.AVAILABLE
    }
    excluded = [name for name in stages if name not in available]
    if not available:
        return IntegratedResult(
            status="unavailable",
            signal=Signal.UNAVAILABLE,
            used_stages=[],
            excluded_stages=excluded,
        )
    severity = {Signal.LOW: 0, Signal.REVIEW: 1, Signal.HIGH: 2, Signal.UNAVAILABLE: -1}
    signal = max((stage.signal for stage in available.values()), key=severity.__getitem__)
    return IntegratedResult(
        status="complete" if len(available) == len(stages) else "partial",
        signal=signal,
        used_stages=list(available),
        excluded_stages=excluded,
    )


def analyze_payload(
    payload: dict[str, Any],
    bundle: dict[str, Any] | None = None,
    mode: str = "synthetic_demo",
) -> AnalysisResult:
    """Validate once and return the same result contract used by CLI and UI."""
    contract = ContractInfo(mode=mode)
    limitations = Limitations(rule_scope=mode, warning=NON_CLINICAL_WARNING)
    try:
        record = normalize_record(payload)
    except InputContractError as error:
        stages = {
            name: _unavailable_stage(
                "input_invalid", "입력 확인 필요", "입력 오류를 수정한 뒤 다시 분석해 주세요."
            )
            for name in ("stage_0", "stage_1", "stage_2")
        }
        return AnalysisResult(
            contract=contract,
            validation=ValidationResult(
                status="invalid",
                errors=[
                    Issue(
                        code="input_contract_error",
                        fields=error.fields,
                        message=str(error),
                        action="표시된 입력값을 확인해 주세요.",
                    )
                ],
            ),
            completeness=calculate_completeness(None),
            stages=stages,
            integrated_result=_integrate(stages),
            limitations=limitations,
        )

    stages = {
        "stage_0": evaluate_stage_0(record, mode),
        "stage_1": evaluate_stage_1(record, mode),
        "stage_2": _model_stage(record, bundle, mode),
    }
    return AnalysisResult(
        contract=contract,
        validation=ValidationResult(),
        completeness=calculate_completeness(record),
        stages=stages,
        integrated_result=_integrate(stages),
        limitations=limitations,
    )

"""Explicitly scoped synthetic-demo rules for staged functional testing."""

from __future__ import annotations

from prectg.schema import NormalizedRecord, Reason, Signal, StageResult, StageStatus

RULESET_VERSION = "synthetic-demo-rules-v1"


def _signal(score: float) -> Signal:
    if score >= 2:
        return Signal.HIGH
    if score >= 1:
        return Signal.REVIEW
    return Signal.LOW


def unavailable_clinical_stage() -> StageResult:
    return StageResult(
        status=StageStatus.UNAVAILABLE,
        signal=Signal.UNAVAILABLE,
        reasons=[
            Reason(
                code="clinical_rules_not_approved",
                title="승인된 임상 규칙 없음",
                detail="임상 검토를 마친 규칙이 없어 이 단계는 실행하지 않았습니다.",
                scope="clinical",
            )
        ],
    )


def evaluate_stage_0(record: NormalizedRecord, mode: str = "synthetic_demo") -> StageResult:
    if mode != "synthetic_demo":
        return unavailable_clinical_stage()
    expected = ["gravida", "para", "gestational_age_weeks"]
    missing = [name for name in expected if getattr(record, name) is None]
    if missing:
        return StageResult(
            status=StageStatus.INSUFFICIENT_DATA,
            signal=Signal.UNAVAILABLE,
            reasons=[
                Reason(
                    code="stage_0_missing",
                    title="분만 전 정보 부족",
                    detail="합성 시연용 패턴을 계산할 입력이 부족합니다.",
                    fields=missing,
                )
            ],
            version=RULESET_VERSION,
        )

    score = 0.0
    reasons: list[Reason] = []
    if record.gestational_age_weeks is not None and not 37 <= record.gestational_age_weeks <= 41:
        score += 1
        reasons.append(
            Reason(
                code="demo_ga_pattern",
                title="임신 주수 패턴",
                detail="합성 시나리오의 기준 구간 밖 입력입니다.",
                fields=["gestational_age_weeks"],
            )
        )
    if record.gravida is not None and record.gravida >= 4:
        score += 1
        reasons.append(
            Reason(
                code="demo_gravida_pattern",
                title="임신 횟수 패턴",
                detail="합성 시나리오에서 관찰 대상으로 지정한 입력입니다.",
                fields=["gravida"],
            )
        )
    if record.para is not None and record.para >= 3:
        score += 1
        reasons.append(
            Reason(
                code="demo_para_pattern",
                title="출산 횟수 패턴",
                detail="합성 시나리오에서 관찰 대상으로 지정한 입력입니다.",
                fields=["para"],
            )
        )
    if not reasons:
        reasons.append(
            Reason(
                code="demo_no_maternal_pattern",
                title="추가 패턴 없음",
                detail="입력된 분만 전 정보에서 합성 시연 규칙의 추가 신호가 없었습니다.",
                fields=expected,
            )
        )
    return StageResult(
        status=StageStatus.AVAILABLE,
        signal=_signal(score),
        score=score,
        reasons=reasons,
        version=RULESET_VERSION,
    )


def evaluate_stage_1(record: NormalizedRecord, mode: str = "synthetic_demo") -> StageResult:
    if mode != "synthetic_demo":
        return unavailable_clinical_stage()
    expected = [
        "baseline",
        "baseline_variability",
        "acceleration",
        "late_deceleration",
        "variable_deceleration",
        "prolonged_deceleration",
        "sinusoidal_pattern",
        "window_complete",
        "timing_source",
    ]
    missing = [name for name in expected if getattr(record, name) is None]
    if missing or record.window_complete is not True:
        return StageResult(
            status=StageStatus.INSUFFICIENT_DATA,
            signal=Signal.UNAVAILABLE,
            reasons=[
                Reason(
                    code="stage_1_missing",
                    title="초기 CTG 정보 부족",
                    detail="20분 관찰창과 CTG 입력을 모두 확인해 주세요.",
                    fields=missing or ["window_complete"],
                )
            ],
            version=RULESET_VERSION,
        )

    score = 0.0
    reasons: list[Reason] = []
    severe = {
        "sinusoidal_pattern": record.sinusoidal_pattern == "1",
        "prolonged_deceleration": record.prolonged_deceleration == "1",
        "late_deceleration": record.late_deceleration == "2",
    }
    for field, active in severe.items():
        if active:
            score += 2
            reasons.append(
                Reason(
                    code=f"demo_{field}",
                    title="우선 확인할 CTG 패턴",
                    detail="합성 시연 규칙에서 높은 단계로 지정한 패턴이 입력되었습니다.",
                    fields=[field],
                )
            )
    if record.baseline_variability != "2":
        score += 1
        reasons.append(
            Reason(
                code="demo_variability_pattern",
                title="기저 변이도 패턴",
                detail="합성 시연 규칙의 기준 범주와 다른 입력입니다.",
                fields=["baseline_variability"],
            )
        )
    if record.acceleration == "2" or record.variable_deceleration != "0":
        score += 1
        reasons.append(
            Reason(
                code="demo_ctg_review_pattern",
                title="추가 관찰 패턴",
                detail="합성 시연 규칙에서 추가 관찰 대상으로 지정한 입력입니다.",
                fields=["acceleration", "variable_deceleration"],
            )
        )
    if not reasons:
        reasons.append(
            Reason(
                code="demo_no_ctg_pattern",
                title="추가 패턴 없음",
                detail="초기 CTG 입력에서 합성 시연 규칙의 추가 신호가 없었습니다.",
                fields=expected[:-2],
            )
        )
    return StageResult(
        status=StageStatus.AVAILABLE,
        signal=_signal(score),
        score=score,
        reasons=reasons,
        version=RULESET_VERSION,
    )

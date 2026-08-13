"""Validated input and output contracts shared by every PreCTG entry point."""

from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AvailabilityTiming(StrEnum):
    PRE_LABOR = "PRE_LABOR"
    EARLY_CTG = "EARLY_CTG"
    POST_WINDOW = "POST_WINDOW"
    POST_DELIVERY = "POST_DELIVERY"
    TARGET = "TARGET"
    UNKNOWN = "UNKNOWN"


class StageStatus(StrEnum):
    AVAILABLE = "available"
    INSUFFICIENT_DATA = "insufficient_data"
    UNAVAILABLE = "unavailable"
    NOT_APPLICABLE = "not_applicable"
    FAILED = "failed"


class ModelStatus(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    INSUFFICIENT_DATA = "insufficient_data"


class Signal(StrEnum):
    LOW = "low"
    REVIEW = "review"
    HIGH = "high"
    UNAVAILABLE = "unavailable"


class NormalizedRecord(BaseModel):
    """Internal record; source spelling never leaks beyond normalization."""

    model_config = ConfigDict(extra="forbid")

    record_id: str
    mother_group_id: str | None = None
    fetus_group_id: str | None = None
    measurement_date: date | None = None
    mother_birth_date: date | None = None
    mother_height: float | None = None
    mother_weight: float | None = None
    gravida: int | None = Field(default=None, ge=0)
    para: int | None = Field(default=None, ge=0)
    systolic_blood_pressure: float | None = None
    diastolic_blood_pressure: float | None = None
    gestational_hypertension: str | None = None
    chronic_hypertension: str | None = None
    gestational_diabetes: str | None = None
    diabetes_mellitus: str | None = None
    preeclampsia: str | None = None
    gestational_age_weeks: int | None = Field(default=None, ge=0)
    gestational_age_days: int | None = Field(default=None, ge=0, le=6)
    fetal_growth_restriction: str | None = None
    placenta_complication: str | None = None
    cervix: str | None = None
    multiple_gestation: str | None = None
    baseline: float | None = None
    baseline_variability: str | None = None
    acceleration: str | None = None
    early_deceleration: str | None = None
    late_deceleration: str | None = None
    variable_deceleration: str | None = None
    prolonged_deceleration: str | None = None
    sinusoidal_pattern: str | None = None
    ctg_category: str | None = None
    abnormality: str | None = None
    official_emergency_raw: str | None = None
    fetal_distress: str | None = None
    delivery: str | None = None
    apgar_1min: float | None = None
    apgar_5min: float | None = None
    nicu_admission: str | None = None
    window_start: datetime | None = None
    window_end: datetime | None = None
    window_complete: bool | None = None
    timing_source: str | None = None
    synthetic_emergency_after_index: bool | None = None
    synthetic_profile: str | None = None
    scenario_type: str | None = None
    generation_seed: int | None = None
    generator_version: str | None = None

    @model_validator(mode="after")
    def validate_window(self) -> NormalizedRecord:
        if self.gravida is not None and self.para is not None and self.para > self.gravida:
            raise ValueError("출산 횟수는 임신 횟수보다 클 수 없습니다.")
        timing_values = (
            self.window_start,
            self.window_end,
            self.window_complete,
            self.timing_source,
        )
        if any(value is not None for value in timing_values) and not all(
            value is not None for value in timing_values
        ):
            raise ValueError("초기 CTG 출처 정보 네 항목을 모두 입력해 주세요.")
        if self.window_complete and self.window_start and self.window_end:
            duration_minutes = (self.window_end - self.window_start).total_seconds() / 60
            if duration_minutes != 20:
                raise ValueError("초기 CTG 관찰 구간은 정확히 20분이어야 합니다.")
        return self


class Issue(BaseModel):
    code: str
    fields: list[str] = Field(default_factory=list)
    message: str
    action: str | None = None


class ValidationResult(BaseModel):
    status: str = "valid"
    errors: list[Issue] = Field(default_factory=list)
    warnings: list[Issue] = Field(default_factory=list)


class Reason(BaseModel):
    code: str
    title: str
    detail: str
    fields: list[str] = Field(default_factory=list)
    scope: str = "synthetic_demo"


class StageResult(BaseModel):
    status: StageStatus
    signal: Signal
    score: float | None = None
    probability: float | None = Field(default=None, ge=0, le=1)
    reasons: list[Reason] = Field(default_factory=list)
    version: str | None = None


class StageCompleteness(BaseModel):
    available: int
    expected: int
    ratio: float = Field(ge=0, le=1)
    missing_fields: list[str] = Field(default_factory=list)


class CompletenessResult(BaseModel):
    overall_ratio: float = Field(ge=0, le=1)
    by_stage: dict[str, StageCompleteness]
    missing_fields: list[str] = Field(default_factory=list)


class ContractInfo(BaseModel):
    result_version: str = "result-contract-v1"
    input_version: str = "field-contract-v1"
    window_version: str = "early-window-v1"
    target_version: str = "emergency-after-index-v1"
    mode: str = "synthetic_demo"


class IntegratedResult(BaseModel):
    status: str
    signal: Signal
    used_stages: list[str]
    excluded_stages: list[str]


class Limitations(BaseModel):
    synthetic_data: bool = True
    non_clinical_use: bool = True
    rule_scope: str = "synthetic_demo"
    warning: str


class AnalysisResult(BaseModel):
    contract: ContractInfo
    validation: ValidationResult
    completeness: CompletenessResult
    stages: dict[str, StageResult]
    integrated_result: IntegratedResult
    limitations: Limitations

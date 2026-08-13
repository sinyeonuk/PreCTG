"""Feature-timing checks that prevent temporal and target leakage."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from prectg.schema import AvailabilityTiming

ALLOWED_MODEL_TIMINGS = frozenset({AvailabilityTiming.PRE_LABOR, AvailabilityTiming.EARLY_CTG})


def find_disallowed_features(
    feature_names: Sequence[str],
    timing_by_feature: Mapping[str, AvailabilityTiming],
) -> dict[str, AvailabilityTiming]:
    """Return unknown or temporally disallowed features selected for ML input."""
    return {
        name: timing_by_feature.get(name, AvailabilityTiming.UNKNOWN)
        for name in feature_names
        if timing_by_feature.get(name, AvailabilityTiming.UNKNOWN) not in ALLOWED_MODEL_TIMINGS
    }


def validate_model_features(
    feature_names: Sequence[str],
    timing_by_feature: Mapping[str, AvailabilityTiming],
) -> None:
    """Reject a feature set containing target, future, or unknown-timing fields."""
    disallowed = find_disallowed_features(feature_names, timing_by_feature)
    if disallowed:
        details = ", ".join(f"{name}={timing.value}" for name, timing in disallowed.items())
        raise ValueError(f"모델 입력에 사용할 수 없는 특성이 포함되어 있습니다: {details}")

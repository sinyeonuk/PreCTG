import pytest

from prectg.leakage import find_disallowed_features, validate_model_features
from prectg.schema import AvailabilityTiming


def test_allows_pre_labor_and_early_ctg_features() -> None:
    timings = {
        "Mother.GHTN": AvailabilityTiming.PRE_LABOR,
        "BaseLine": AvailabilityTiming.EARLY_CTG,
    }

    validate_model_features(["Mother.GHTN", "BaseLine"], timings)


def test_rejects_targets_future_and_unknown_features() -> None:
    timings = {
        "Emergency": AvailabilityTiming.TARGET,
        "APGAR.1min": AvailabilityTiming.POST_DELIVERY,
    }

    disallowed = find_disallowed_features(["Emergency", "APGAR.1min", "unregistered"], timings)

    assert disallowed == {
        "Emergency": AvailabilityTiming.TARGET,
        "APGAR.1min": AvailabilityTiming.POST_DELIVERY,
        "unregistered": AvailabilityTiming.UNKNOWN,
    }
    with pytest.raises(ValueError, match="사용할 수 없는 특성"):
        validate_model_features(list(disallowed), timings)

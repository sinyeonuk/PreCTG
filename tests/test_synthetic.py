import pytest

from prectg.synthetic import dataframe_checksum, generate_synthetic_data, validate_synthetic_data


def test_generation_is_deterministic_and_valid() -> None:
    first = generate_synthetic_data(rows=1200, seed=7, profile="coverage")
    second = generate_synthetic_data(rows=1200, seed=7, profile="coverage")
    report = validate_synthetic_data(first, "coverage", 7)

    assert dataframe_checksum(first) == dataframe_checksum(second)
    assert report.duplicate_records == 0
    assert report.logical_violations == 0
    assert report.schema_violations == 0
    assert set(report.scenario_counts) == {
        "normal",
        "maternal",
        "ctg",
        "combined",
        "missing",
        "conflict",
    }
    assert min(report.scenario_counts.values()) == 200


def test_distribution_profile_is_reproducible_but_different() -> None:
    coverage = generate_synthetic_data(rows=500, seed=3, profile="coverage")
    distribution = generate_synthetic_data(rows=500, seed=3, profile="distribution")

    assert dataframe_checksum(coverage) != dataframe_checksum(distribution)


def test_distribution_profile_matches_public_category_ratio_at_scale() -> None:
    frame = generate_synthetic_data(rows=50000, seed=20260814, profile="distribution")
    report = validate_synthetic_data(frame, "distribution", 20260814)

    assert report.category_1_rate == pytest.approx(0.7272, abs=0.01)
    assert all(abs(difference) <= 0.01 for difference in report.distribution_differences.values())

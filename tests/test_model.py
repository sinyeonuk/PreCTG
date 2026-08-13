from pathlib import Path

import pytest

from prectg.model import (
    ModelContractError,
    grouped_split,
    load_model_bundle,
    predict_batch_probabilities,
    predict_probability,
    save_model_bundle,
    train_model_bundle,
)
from prectg.preprocessing import normalize_record
from prectg.synthetic import generate_synthetic_data


def test_grouped_training_persistence_and_inference(tmp_path: Path) -> None:
    frame = generate_synthetic_data(rows=1200, seed=11)
    train_index, validation_index = grouped_split(frame, 11)
    train_groups = set(frame.iloc[train_index]["Mother.de-identification_ID"])
    validation_groups = set(frame.iloc[validation_index]["Mother.de-identification_ID"])
    assert train_groups.isdisjoint(validation_groups)

    bundle, report = train_model_bundle(frame, seed=11)
    model_path = save_model_bundle(bundle, tmp_path / "model.joblib")
    loaded = load_model_bundle(model_path)
    record = normalize_record(frame.iloc[0].dropna().to_dict())

    before = predict_probability(bundle, record)
    after = predict_probability(loaded, record)
    assert before == pytest.approx(after, abs=1e-9)
    assert 0 <= before <= 1
    assert report.group_overlap == 0
    batch = predict_batch_probabilities(loaded, frame.head(20))
    assert len(batch) == 20


def test_rejects_incompatible_feature_contract() -> None:
    frame = generate_synthetic_data(rows=500, seed=2)
    bundle, _ = train_model_bundle(frame, seed=2)
    bundle["internal_features"] = ["Emergency"]

    with pytest.raises(ModelContractError, match="특성"):
        predict_probability(bundle, normalize_record(frame.iloc[0].dropna().to_dict()))


def test_corrupt_model_file_is_reported_as_contract_error(tmp_path: Path) -> None:
    model_path = tmp_path / "corrupt.joblib"
    model_path.write_bytes(b"not-a-model")

    with pytest.raises(ModelContractError, match="불러올 수 없습니다"):
        load_model_bundle(model_path)

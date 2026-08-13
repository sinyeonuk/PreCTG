import json
from pathlib import Path

import pandas as pd

from prectg.cli import main
from prectg.model import save_model_bundle, train_model_bundle
from prectg.risk_engine import analyze_payload
from prectg.synthetic import generate_synthetic_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = PROJECT_ROOT / "data" / "fixtures" / "minimal-synthetic-input.json"


def trained_artifacts(tmp_path: Path) -> tuple[Path, Path, dict[str, object]]:
    frame = generate_synthetic_data(rows=800, seed=57)
    data_path = tmp_path / "synthetic.csv"
    frame.to_csv(data_path, index=False)
    bundle, _ = train_model_bundle(frame, seed=57)
    model_path = save_model_bundle(bundle, tmp_path / "model.joblib")
    return data_path, model_path, bundle


def test_cli_and_python_api_return_same_single_result(tmp_path: Path) -> None:
    _, model_path, bundle = trained_artifacts(tmp_path)
    output_path = tmp_path / "result.json"
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    exit_code = main(
        [
            "predict",
            "--input",
            str(FIXTURE_PATH),
            "--model",
            str(model_path),
            "--output",
            str(output_path),
        ]
    )
    cli_result = json.loads(output_path.read_text(encoding="utf-8"))
    api_result = analyze_payload(payload, bundle).model_dump(mode="json")

    assert exit_code == 0
    assert cli_result == api_result


def test_batch_prediction_cli_writes_one_safe_result_per_row(tmp_path: Path) -> None:
    data_path, model_path, _ = trained_artifacts(tmp_path)
    output_path = tmp_path / "batch.csv"

    exit_code = main(
        [
            "predict-batch",
            "--input",
            str(data_path),
            "--model",
            str(model_path),
            "--output",
            str(output_path),
        ]
    )
    result = pd.read_csv(output_path)

    assert exit_code == 0
    assert len(result) == 800
    assert result["synthetic_probability"].between(0, 1).all()
    assert set(result["signal"]) <= {"low", "review", "high"}
    assert result["non_clinical_use"].all()


def test_malformed_json_returns_safe_error_without_payload(tmp_path: Path, capsys) -> None:
    malformed_path = tmp_path / "invalid.json"
    malformed_path.write_text('{"sensitive":', encoding="utf-8")

    exit_code = main(["predict", "--input", str(malformed_path)])
    output = capsys.readouterr().out

    assert exit_code == 2
    assert "input_file_error" in output
    assert "sensitive" not in output

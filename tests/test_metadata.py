from prectg.metadata import NON_CLINICAL_WARNING, project_status


def test_project_status_reports_defined_contracts_without_clinical_claims() -> None:
    status = project_status()

    assert status["stage"] == "mvp_implemented"
    assert "field_contract" in status["implemented"]
    assert "result_contract" in status["implemented"]
    assert "risk_inference" in status["implemented"]
    assert "clinical_validation" in status["not_implemented"]
    assert status["warning"] == NON_CLINICAL_WARNING
    assert "실제 진단" in NON_CLINICAL_WARNING

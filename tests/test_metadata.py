from prectg.metadata import NON_CLINICAL_WARNING, project_status


def test_project_status_reports_scaffold_without_clinical_claims() -> None:
    status = project_status()

    assert status["stage"] == "scaffold"
    assert "risk_inference" in status["not_implemented"]
    assert status["warning"] == NON_CLINICAL_WARNING
    assert "실제 진단" in NON_CLINICAL_WARNING

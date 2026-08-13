from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_SOURCE = (PROJECT_ROOT / "app" / "streamlit_app.py").read_text(encoding="utf-8")


def test_ui_avoids_clinically_definitive_copy() -> None:
    forbidden = ["안전합니다", "정상입니다", "응급입니다", "진단 결과", "치료 권고"]
    removed_context_warnings = [
        "합성 데이터 기반 기능 시연용 MVP",
        "모든 수치와 결과는 기능 확인을 위해 생성한 합성 사례입니다.",
        "데모 환경 · 합성 데이터",
        "DEBUGLAB · SYNTHETIC DEMO",
        "통합 시연 결과",
        "합성 모델 확률",
        "추가 합성 패턴",
    ]

    assert not any(phrase in APP_SOURCE for phrase in forbidden)
    assert not any(phrase in APP_SOURCE for phrase in removed_context_warnings)


def test_ui_uses_user_facing_analysis_language_and_hierarchy() -> None:
    expected = [
        "분석 사례를 선택하세요",
        "분석 설정",
        "전체 분석",
        "규칙 기반 분석만",
        "통합 분석 결과",
        "모델 분석 상세",
        "결과 JSON 저장",
    ]

    assert all(phrase in APP_SOURCE for phrase in expected)
    assert '"기저 변이도 코드"' not in APP_SOURCE
    assert '"가속 코드"' not in APP_SOURCE


def test_ui_bundles_font_without_external_cdn() -> None:
    assert "data:font/woff2;base64" in APP_SOURCE
    assert "cdn." not in APP_SOURCE

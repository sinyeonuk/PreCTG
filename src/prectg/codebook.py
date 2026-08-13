"""Human-readable labels for confirmed AIHub categorical codes."""

from __future__ import annotations

CODE_LABELS: dict[str, dict[str, str]] = {
    "Baseline_Variability": {"0": "소실", "1": "최소", "2": "중등도", "3": "현저"},
    "Acceleration": {"1": "있음", "2": "없음"},
    "Early_deceleration": {"0": "없음", "1": "있음"},
    "Late_deceleration": {"0": "없음", "1": "1회", "2": "2회 이상"},
    "Variable_deceleration": {"0": "없음", "1": "1회", "2": "2회 이상"},
    "Prolonged_deceleration": {"0": "없음", "1": "있음"},
    "Sinosoical_pattern": {"0": "없음", "1": "있음"},
}


def code_to_label(field: str, code: str) -> str:
    """Return a Korean label while keeping the original code visible."""
    try:
        return f"{CODE_LABELS[field][str(code)]} (코드 {code})"
    except KeyError as error:
        raise ValueError(f"{field}에 지원하지 않는 코드가 있습니다: {code}") from error


def label_to_code(field: str, label: str) -> str:
    """Convert either the display label or plain Korean label back to its code."""
    if field not in CODE_LABELS:
        raise ValueError(f"지원하지 않는 코드 필드입니다: {field}")
    for code, korean in CODE_LABELS[field].items():
        if label in {korean, f"{korean} (코드 {code})"}:
            return code
    raise ValueError(f"{field}에 지원하지 않는 표시값이 있습니다: {label}")

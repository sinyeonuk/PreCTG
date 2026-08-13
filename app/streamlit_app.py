"""Polished, offline-capable Streamlit demonstration for PreCTG."""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from prectg.codebook import CODE_LABELS
from prectg.explanation import signal_label
from prectg.features import training_feature_frame
from prectg.model import train_model_bundle
from prectg.risk_engine import analyze_payload
from prectg.schema import AnalysisResult
from prectg.synthetic import generate_synthetic_data

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "data" / "fixtures" / "minimal-synthetic-input.json"
FONT_PATH = ROOT / "app" / "assets" / "fonts" / "Pretendard-Regular.woff2"
CASE_LABELS = {
    "normal": ("기본 사례", "특이 패턴이 적은 사례"),
    "maternal": ("분만 전 관찰 사례", "분만 전 정보에 주요 패턴이 있는 사례"),
    "ctg": ("초기 CTG 관찰 사례", "초기 CTG에 주요 패턴이 있는 사례"),
    "combined": ("복합 관찰 사례", "두 단계에 주요 패턴이 함께 있는 사례"),
    "missing": ("결측 사례", "일부 입력이 없어 단계 결과가 제한되는 입력"),
    "conflict": ("규칙 충돌 사례", "서로 다른 CTG 패턴이 함께 있는 입력"),
}
STATUS_LABELS = {
    "available": "분석 완료",
    "insufficient_data": "입력 부족",
    "unavailable": "분석할 수 없음",
    "not_applicable": "분석 대상 아님",
    "failed": "분석 실패",
}

st.set_page_config(page_title="PreCTG", page_icon="♥", layout="wide")


def _font_css() -> str:
    if not FONT_PATH.exists():
        return ""
    encoded = base64.b64encode(FONT_PATH.read_bytes()).decode("ascii")
    return (
        "@font-face{font-family:'Pretendard';font-style:normal;font-weight:100 900;"
        f"font-display:swap;src:url(data:font/woff2;base64,{encoded}) format('woff2');}}"
    )


st.markdown(
    f"""
    <style>
    {_font_css()}
    :root {{ --ink:#162323; --muted:#5e6d6b; --line:#dce5e2; --soft:#f3f7f5;
            --brand:#126c61; --brand-dark:#0d5149; --high:#a63d40; --review:#996515; }}
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
      font-family:"Pretendard","Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif;
      color:var(--ink);
    }}
    [data-testid="stAppViewContainer"] {{ background:#f8faf9; }}
    .block-container {{ max-width:1080px; padding:4.5rem 2rem 4rem; }}
    h1 {{ letter-spacing:-.04em!important; font-size:2.15rem!important;
          margin-bottom:.25rem!important; }}
    h2, h3 {{ letter-spacing:-.025em!important; }}
    .eyebrow {{ color:var(--brand); font-size:.78rem; font-weight:800; letter-spacing:.08em; }}
    .lead {{ color:var(--muted); font-size:1.02rem; margin:.25rem 0 1.2rem; }}
    .notice {{ border:1px solid #d8e4df; background:#eef5f2; padding:.85rem 1rem;
               border-radius:10px; color:#334e49; font-size:.9rem; }}
    .steps {{ display:grid; grid-template-columns:repeat(3,1fr); gap:.5rem; margin:1.5rem 0 2rem; }}
    .step {{ border-top:3px solid var(--line); padding:.65rem .2rem;
             color:var(--muted); font-size:.88rem; }}
    .step.active {{ border-color:var(--brand); color:var(--brand-dark); font-weight:800; }}
    .step.done {{ border-color:#79a99f; color:#385f58; }}
    .mobile-step {{ display:none; color:var(--brand-dark); font-size:.84rem; font-weight:800;
                    margin:1rem 0 .5rem; }}
    .result-banner {{ padding:1.25rem 1.35rem; border-radius:12px;
                      border-left:5px solid var(--brand);
                      background:white; box-shadow:0 6px 24px rgba(23,54,49,.07);
                      margin-bottom:1rem; }}
    .signal-high {{ border-left-color:var(--high); }}
    .signal-review {{ border-left-color:var(--review); }}
    .result-kicker {{ color:var(--muted); font-size:.82rem; }}
    .result-title {{ font-size:1.55rem; font-weight:850; margin-top:.15rem; }}
    .signal-badge {{ display:flex; align-items:center; gap:.5rem; color:var(--ink);
                     font-size:1.28rem; font-weight:850; margin:.65rem 0 .2rem; }}
    .signal-badge::before {{ content:""; width:.65rem; height:.65rem; border-radius:2px;
                             background:var(--brand); transform:rotate(45deg); }}
    .signal-badge.signal-review::before {{ background:var(--review); }}
    .signal-badge.signal-high::before {{ background:var(--high); }}
    .signal-badge.signal-unavailable::before {{ background:var(--muted); }}
    .status-badge {{ display:inline-flex; align-items:center; gap:.35rem; padding:.28rem .58rem;
                     border-radius:999px; background:var(--soft); color:var(--brand-dark);
                     font-size:.78rem; font-weight:800; margin:.25rem 0 .65rem; }}
    .status-badge::before {{ content:""; width:.48rem; height:.48rem; border-radius:50%;
                             background:var(--brand); }}
    .status-badge.status-insufficient_data::before,
    .status-badge.status-unavailable::before {{ background:var(--review); }}
    .status-badge.status-failed::before {{ background:var(--high); }}
    .stage-role {{ color:var(--muted); font-size:.82rem; min-height:2.45rem;
                   margin-bottom:.25rem; }}
    .stage-reason {{ color:var(--ink); font-size:.92rem; line-height:1.55; margin-top:.25rem; }}
    [data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"] {{
      background:white; border-color:var(--line)!important; border-radius:12px!important;
    }}
    .stButton button, .stDownloadButton button {{ min-height:44px; border-radius:8px;
                                                   font-weight:750; }}
    .stButton button[kind="primary"] {{ background:var(--brand); border-color:var(--brand); }}
    .stButton button[kind="primary"]:hover {{ background:var(--brand-dark);
                                                border-color:var(--brand-dark); }}
    *:focus-visible {{ outline:3px solid #50a99a!important; outline-offset:2px!important; }}
    @media (max-width:640px) {{
      .block-container {{ padding:4rem 1rem 3rem; }}
      .steps {{ display:none; }} .mobile-step {{ display:block; }}
      h1 {{ font-size:1.8rem!important; }} .result-title {{ font-size:1.35rem; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def representative_cases() -> dict[str, dict[str, Any]]:
    frame = generate_synthetic_data(rows=3000, seed=20260814, profile="distribution")
    probabilities = demo_model()["model"].predict_proba(training_feature_frame(frame))[:, 1]
    frame = frame.assign(_demo_probability=probabilities)
    cases: dict[str, dict[str, Any]] = {}
    for scenario in CASE_LABELS:
        candidates = frame.loc[frame["scenario_type"] == scenario]
        row = candidates.sort_values("_demo_probability").iloc[0 if scenario == "normal" else -1]
        cases[scenario] = {
            key: value
            for key, value in row.drop(labels="_demo_probability").to_dict().items()
            if not pd.isna(value)
        }
    return cases


@st.cache_resource(show_spinner=False)
def demo_model() -> dict[str, Any]:
    frame = generate_synthetic_data(rows=3000, seed=20260814, profile="distribution")
    bundle, _ = train_model_bundle(frame, seed=20260814)
    return bundle


def progress(step: int) -> None:
    labels = ("1. 사례 선택", "2. 입력 확인", "3. 분석 결과")
    items = []
    for index, label in enumerate(labels, start=1):
        state = "active" if index == step else "done" if index < step else ""
        items.append(f'<div class="step {state}">{label}</div>')
    st.markdown(
        f'<div class="mobile-step">{step} / 3 · {labels[step - 1].split(". ", 1)[1]}</div>'
        f'<div class="steps">{"".join(items)}</div>',
        unsafe_allow_html=True,
    )


def reset() -> None:
    for key in ("step", "payload", "result", "source_mode", "model_enabled"):
        st.session_state.pop(key, None)
    st.session_state.step = 1


def step_one() -> None:
    st.subheader("분석 사례를 선택하세요")
    st.caption("대표 사례로 바로 시작하거나 다른 입력 방식을 선택할 수 있습니다.")
    method = st.radio(
        "입력 방식",
        ["대표 사례", "직접 입력", "JSON 업로드"],
        horizontal=True,
    )
    payload: dict[str, Any] | None = None
    if method == "대표 사례":
        cases = representative_cases()
        selected = st.selectbox(
            "대표 사례",
            list(CASE_LABELS),
            format_func=lambda value: f"{CASE_LABELS[value][0]} — {CASE_LABELS[value][1]}",
        )
        payload = cases[selected]
    elif method == "직접 입력":
        payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        st.info("기본 입력을 다음 단계에서 직접 수정합니다.")
    else:
        st.warning("실제 환자정보나 식별정보가 포함된 파일은 업로드하지 마세요.")
        uploaded = st.file_uploader("AIHub 호환 JSON 파일", type=["json"])
        if uploaded:
            try:
                loaded = json.load(uploaded)
                if not isinstance(loaded, dict):
                    raise ValueError
                payload = loaded
                st.success("JSON을 읽었습니다. 다음 단계에서 입력값을 확인해 주세요.")
            except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
                st.error(
                    f"{uploaded.name}의 JSON 구조를 확인해 주세요. 최상위 값은 객체여야 합니다."
                )

    with st.expander("분석 설정"):
        analysis_scope = st.radio(
            "분석 범위",
            ["전체 분석", "규칙 기반 분석만"],
            horizontal=True,
            help="전체 분석은 규칙과 모델 분석을 함께 실행합니다.",
        )
    model_enabled = analysis_scope == "전체 분석"
    if not model_enabled:
        st.caption("0단계와 1단계만 분석하며, 2단계 모델 분석은 실행하지 않습니다.")

    left, right = st.columns([1, 2])
    with left:
        if st.button("입력 초기화", use_container_width=True):
            reset()
            st.rerun()
    with right:
        if st.button(
            "입력 확인", type="primary", disabled=payload is None, use_container_width=True
        ):
            st.session_state.payload = payload
            st.session_state.source_mode = method
            st.session_state.model_enabled = model_enabled
            st.session_state.step = 2
            st.rerun()


def _number(payload: dict[str, Any], key: str, default: int) -> int:
    value = payload.get(key, default)
    return default if value is None or pd.isna(value) else int(value)


def _choice(value: Any, choices: list[str], default: str) -> int:
    normalized = str(value if value is not None else default)
    return choices.index(normalized) if normalized in choices else choices.index(default)


def _code_select(label: str, field: str, choices: list[str], value: Any, default: str) -> str:
    return st.selectbox(
        label,
        choices,
        index=_choice(value, choices, default),
        format_func=lambda code: CODE_LABELS[field][code],
    )


def _reason_copy(code: str, fallback_title: str, status: str) -> str:
    copies = {
        "demo_no_maternal_pattern": "특이 패턴 없음",
        "demo_no_ctg_pattern": "주요 CTG 변화 없음",
        "demo_ga_pattern": "임신 주수 패턴 확인",
        "demo_gravida_pattern": "임신 횟수 패턴 확인",
        "demo_para_pattern": "출산 횟수 패턴 확인",
        "demo_sinusoidal_pattern": "우선 확인할 CTG 패턴",
        "demo_prolonged_deceleration": "우선 확인할 CTG 패턴",
        "demo_late_deceleration": "우선 확인할 CTG 패턴",
        "demo_variability_pattern": "기저 변이도 패턴 확인",
        "demo_ctg_review_pattern": "추가 관찰 패턴 확인",
        "synthetic_model_probability": "모델 분석 신호 산출",
        "model_unavailable": "이 단계는 현재 분석할 수 없습니다",
        "stage_0_missing": "분만 전 정보를 더 입력해 주세요",
        "stage_1_missing": "초기 CTG 정보를 더 입력해 주세요",
        "model_timing_missing": "관찰 시점 정보를 확인해 주세요",
    }
    if code == "model_contract_error":
        return (
            "모델 입력을 더 확인해 주세요"
            if status == "insufficient_data"
            else "이 단계는 현재 분석할 수 없습니다"
        )
    return copies.get(code, fallback_title)


def step_two() -> None:
    st.subheader("분석에 사용할 입력을 확인해 주세요")
    model_scope = (
        "규칙과 모델 분석" if st.session_state.get("model_enabled", True) else "규칙 기반 분석만"
    )
    st.caption(f"입력 출처: {st.session_state.get('source_mode', '대표 사례')} · {model_scope}")
    with st.expander("분석에 사용하는 정보"):
        st.write(
            "모델 입력: 임신·출산 횟수, 임신 주수, 기저 심박수와 초기 CTG 정보. "
            "식별자, 정답, 출생 이후 결과와 생성 메타데이터는 모델에서 제외합니다. "
            "원본 코드값은 저장한 결과 JSON에서 확인할 수 있습니다."
        )
    payload = dict(st.session_state.payload)
    with st.form("input-review", border=True):
        left, right = st.columns(2)
        with left:
            st.markdown("#### 분만 전 정보")
            record_id = st.text_input("사례 식별자", value=str(payload.get("ID", "")))
            gravida = st.number_input("임신 횟수", 0, 20, _number(payload, "Mother.Gravida", 1))
            para = st.number_input("출산 횟수", 0, 20, _number(payload, "Mother.Para", 0))
            ga_missing = st.checkbox("임신 주수 값 없음", value="GA.wks" not in payload)
            ga_weeks = st.number_input(
                "임신 주수(주)", 0, 50, _number(payload, "GA.wks", 39), disabled=ga_missing
            )
            ga_days = st.number_input("추가 일수", 0, 6, _number(payload, "GA.day", 0))
        with right:
            st.markdown("#### 초기 CTG 정보")
            baseline_missing = st.checkbox("기저 심박수 값 없음", value="BaseLine" not in payload)
            baseline = st.number_input(
                "기저 심박수(bpm)",
                0,
                250,
                _number(payload, "BaseLine", 140),
                disabled=baseline_missing,
            )
            variability = _code_select(
                "기저 변이도",
                "Baseline_Variability",
                ["0", "1", "2", "3"],
                payload.get("Baseline_Variability"),
                "2",
            )
            acceleration = _code_select(
                "가속", "Acceleration", ["1", "2"], payload.get("Acceleration"), "1"
            )
            late = _code_select(
                "후기 감속",
                "Late_deceleration",
                ["0", "1", "2"],
                payload.get("Late_deceleration"),
                "0",
            )
            variable = _code_select(
                "가변 감속",
                "Variable_deceleration",
                ["0", "1", "2"],
                payload.get("Variable_deceleration"),
                "0",
            )
            prolonged = _code_select(
                "지연 감속",
                "Prolonged_deceleration",
                ["0", "1"],
                payload.get("Prolonged_deceleration"),
                "0",
            )
            sinusoidal = _code_select(
                "사인파형",
                "Sinosoical_pattern",
                ["0", "1"],
                payload.get("Sinosoical_pattern"),
                "0",
            )
        back_col, submit_col = st.columns([1, 2])
        with back_col:
            back = st.form_submit_button("이전", use_container_width=True)
        with submit_col:
            submitted = st.form_submit_button("분석 실행", type="primary", use_container_width=True)
    if back:
        st.session_state.step = 1
        st.rerun()
    if submitted:
        payload.update(
            {
                "ID": record_id,
                "Mother.Gravida": gravida,
                "Mother.Para": para,
                "GA.wks": None if ga_missing else ga_weeks,
                "GA.day": ga_days,
                "BaseLine": None if baseline_missing else baseline,
                "Baseline_Variability": variability,
                "Acceleration": acceleration,
                "Late_deceleration": late,
                "Variable_deceleration": variable,
                "Prolonged_deceleration": prolonged,
                "Sinosoical_pattern": sinusoidal,
            }
        )
        with st.spinner("입력값을 확인하고 단계별 위험 신호를 분석하고 있습니다."):
            bundle = demo_model() if st.session_state.get("model_enabled", True) else None
            result = analyze_payload(payload, bundle)
        if result.validation.status == "invalid":
            for issue in result.validation.errors:
                st.error(f"{issue.message} {issue.action or ''}")
            st.session_state.payload = payload
        else:
            st.session_state.payload = payload
            st.session_state.result = result.model_dump(mode="json")
            st.session_state.step = 3
            st.rerun()


def step_three() -> None:
    result = AnalysisResult.model_validate(st.session_state.result)
    signal = result.integrated_result.signal
    st.markdown(
        f'<div class="result-banner signal-{signal.value}" role="status" aria-live="polite">'
        '<div class="result-kicker">통합 분석 결과</div>'
        f'<div class="result-title">{signal_label(signal)}</div></div>',
        unsafe_allow_html=True,
    )
    first, second = st.columns(2)
    first.metric("사용한 단계", f"{len(result.integrated_result.used_stages)} / 3")
    second.metric("입력 완전성", f"{result.completeness.overall_ratio * 100:.0f}%")
    probability = result.stages["stage_2"].probability

    st.subheader("단계별 판단 근거")
    labels = {
        "stage_0": ("0단계 · 분만 전 정보", "임신·출산 이력과 임신 주수 확인"),
        "stage_1": ("1단계 · 초기 CTG", "초기 심박동 패턴 확인"),
        "stage_2": ("2단계 · 모델 분석", "입력 특성을 종합한 모델 신호 확인"),
    }
    columns = st.columns(3)
    for column, (key, (label, role)) in zip(columns, labels.items(), strict=True):
        stage = result.stages[key]
        with column, st.container(border=True):
            st.markdown(f"**{label}**")
            st.markdown(f'<div class="stage-role">{role}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="signal-badge signal-{stage.signal.value}" role="heading" '
                f'aria-level="3">{signal_label(stage.signal)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="status-badge status-{stage.status.value}">'
                f"{STATUS_LABELS[stage.status.value]}</div>",
                unsafe_allow_html=True,
            )
            display_reasons: list[str] = []
            for reason in stage.reasons:
                reason_copy = _reason_copy(reason.code, reason.title, stage.status.value)
                if reason_copy not in display_reasons:
                    display_reasons.append(reason_copy)
                if len(display_reasons) == 3:
                    break
            for reason_copy in display_reasons:
                st.markdown(
                    f'<div class="stage-reason">{reason_copy}</div>',
                    unsafe_allow_html=True,
                )
    if result.completeness.missing_fields:
        with st.expander("누락된 입력 확인"):
            st.write(", ".join(result.completeness.missing_fields))
    with st.expander("모델 분석 상세"):
        if probability is None:
            st.write("현재 입력과 분석 범위에서는 모델 분석 결과가 없습니다.")
        else:
            st.metric("모델 분석값", f"{probability * 100:.1f}%")
            st.caption("모델 내부의 상대적 분석값입니다.")
    with st.expander("분석 계약 정보"):
        st.write(
            f"입력 {result.contract.input_version} · 관찰창 {result.contract.window_version} · "
            f"목표 {result.contract.target_version} · 결과 {result.contract.result_version}"
        )
    serialized = json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2)
    download_col, reset_col, back_col = st.columns([1.8, 1.5, 1.2])
    with download_col:
        st.download_button(
            "결과 JSON 저장",
            serialized,
            file_name="prectg-demo-result.json",
            mime="application/json",
            type="primary",
            use_container_width=True,
        )
    with reset_col:
        if st.button("새 사례 분석", use_container_width=True):
            reset()
            st.rerun()
    with back_col:
        if st.button("입력 수정", use_container_width=True):
            st.session_state.step = 2
            st.rerun()


if "step" not in st.session_state:
    st.session_state.step = 1

st.markdown('<div class="eyebrow">DEBUGLAB</div>', unsafe_allow_html=True)
st.title("PreCTG")
st.markdown(
    '<div class="lead">분만 전 정보와 초기 CTG를 단계적으로 연결해 '
    "위험 신호의 변화를 살펴봅니다.</div>",
    unsafe_allow_html=True,
)
progress(st.session_state.step)

if st.session_state.step == 1:
    step_one()
elif st.session_state.step == 2:
    step_two()
else:
    step_three()
